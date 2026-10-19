# Umbra — installation, RTSP et mesures du Raspberry Pi 5

**Projet :** Noctua, station autonome d'observation de la faune  
**Période :** octobre 2026  
**Statut :** réception vidéo et mesures de performance validées sur banc d'essai ; fonctionnement autonome non encore validé.

> Guide rédigé pour une personne débutante. Il distingue les manipulations observées des étapes à vérifier. Les commandes ne contiennent aucun mot de passe réel.

## 1. Matériel reçu et rôle de chaque élément

- **Reolink RLC-811A**, baptisée **Umbra** : caméra IP Ethernet et PoE.
- **PLANET IPOE-162** : injecteur PoE industriel, permettant d'acheminer alimentation et réseau vers la caméra.
- **Raspberry Pi 5**, baptisé **Noctua** : reçoit et traite le flux vidéo.
- **Alimentation LEICKE NT03242**, 24 V / 2 A : tension à vide précédemment mesurée à **24,46 V DC**.
- **Ordinateur Kali Linux** : accès SSH au Raspberry Pi.

**Sécurité électrique :** la mesure 24,46 V concerne l'alimentation, pas le port PoE. Avant tout raccordement, vérifier les caractéristiques exactes de l'entrée de l'injecteur, la polarité, les connecteurs et les ports indiqués sur l'appareil. Ne jamais brancher directement 24 V sur une prise Ethernet ou une entrée caméra 12 V.

### Montage PoE : points à confirmer et photographier

1. Identifier le port de données entrant (**LAN/Data In**) et le port sortant (**PoE/Data+Power Out**) sur l'injecteur.
2. Raccorder le réseau local à l'entrée de données.
3. Raccorder la caméra à la sortie PoE.
4. Brancher l'alimentation adaptée à l'injecteur.
5. Contrôler les voyants et vérifier l'apparition de la caméra sur le réseau.

Cette liste décrit le principe de câblage, **pas un relevé exhaustif du branchement historique**. Les photos détaillées, longueurs de câbles et états des voyants restent à consigner.

## 2. Initialisation de la caméra

1. Installer l'application **Reolink** sur le téléphone.
2. Ajouter la caméra et définir un mot de passe administrateur fort et unique.
3. Nommer la caméra **Umbra**.
4. Activer le service **RTSP** dans les paramètres réseau de la caméra (le chemin exact du menu dépend du firmware et reste à relever).
5. Relever son adresse IP locale. Lors de notre essai, il s'agissait de `192.168.1.28` ; cette adresse doit être adaptée sur un autre réseau.
6. Vérifier que le port **554/TCP** est ouvert.

Pour vérifier le port depuis un terminal disposant de `nmap` :

```bash
nmap -p 554 192.168.1.28
```

**Observation :** le port 554 était ouvert. Sans authentification, une première tentative RTSP a retourné **401 Unauthorized** : la caméra demandait des identifiants.

## 3. Se connecter à Noctua depuis Kali Linux

Sur Kali, ouvrir un terminal :

```bash
ssh sandrine@noctua.home
```

- `ssh` : connexion chiffrée à une autre machine.
- `sandrine` : compte utilisé sur notre Raspberry Pi ; à adapter.
- `noctua.home` : nom de machine sur notre réseau ; à remplacer par l'IP du Pi si nécessaire.

Saisir le mot de passe SSH lorsqu'il est demandé. Les caractères ne s'affichent pas : **c'est normal**.

Les commandes des sections suivantes sont exécutées **sur Noctua via SSH**, sauf indication contraire.

## 4. Installer et vérifier les outils

```bash
ffmpeg -version
ffprobe -version
```

Si l'un de ces outils est absent :

```bash
sudo apt update
sudo apt install ffmpeg
```

- **FFmpeg** traite les flux vidéo.
- **ffprobe** affiche leurs caractéristiques techniques.
- **ffplay** permet de les visionner sur une machine dotée d'un écran graphique.

VLC a été essayé sans succès dans notre configuration. FFplay a permis la lecture ; cela ne signifie pas que VLC est incompatible avec toutes les caméras Reolink.

## 5. Authentification RTSP : ne jamais publier le secret

Dans le terminal SSH de Noctua :

```bash
read -rsp "Mot de passe Umbra : " CAM_PASS; echo
```

La saisie est invisible. `CAM_PASS` est une variable temporaire, utilisable dans **ce terminal seulement**.

**Particularité constatée :** le mot de passe employé pendant les tests contenait `>`. Dans une URL, ce caractère doit être encodé sous la forme `%3E`. Les exemples suivants reproduisent la méthode testée, **uniquement si `>` est le seul caractère réservé nécessitant un encodage** :

```bash
CAM_IP="192.168.1.28"
RTSP_SUB="rtsp://admin:${CAM_PASS//>/%3E}@${CAM_IP}:554/Preview_01_sub"
RTSP_MAIN="rtsp://admin:${CAM_PASS//>/%3E}@${CAM_IP}:554/Preview_01_main"
```

**Limite importante :** d'autres caractères (`@`, `:`, `/`, `?`, `#`, `%`, etc.) exigent un encodage adapté. Ne pas utiliser cette substitution simplifiée avec un mot de passe différent sans vérifier son encodage. La présence du secret dans une URL de ligne de commande peut aussi l'exposer dans la liste des processus : il s'agit d'une méthode de **banc d'essai local**, pas d'une configuration de production sécurisée.

**Ne jamais copier dans GitHub une URL RTSP développée avec le vrai mot de passe.**

## 6. Tester le flux secondaire

```bash
ffprobe -v error -rtsp_transport tcp \
  -i "$RTSP_SUB" \
  -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1
```

**Résultat observé :** flux secondaire H.264, **640 × 360**, fréquence déclarée **25/1**. Dans une autre lecture, le lecteur indiquait environ 10 images/s ; ce point reste à clarifier.

Pour visualiser le flux depuis une machine avec interface graphique et FFplay :

```bash
ffplay -rtsp_transport tcp -i "$RTSP_SUB"
```

Attention : une session SSH sans affichage graphique n'ouvre pas automatiquement de fenêtre vidéo sur le Raspberry Pi.

## 7. Tester le flux principal 4K

```bash
ffprobe -v error -rtsp_transport tcp \
  -i "$RTSP_MAIN" \
  -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1
```

**Résultat réellement obtenu :**

```text
codec_name=hevc
width=3840
height=2160
r_frame_rate=51/2
```

Le flux principal est donc en **H.265/HEVC**, résolution **3840 × 2160 (4K)**, fréquence déclarée **25,5 images/s**.

## 8. Décoder la vidéo sans créer de fichier

Le périphérique `/dev/null` élimine les données. Le format `framemd5` oblige FFmpeg à décoder les images pour calculer des empreintes, qui sont ensuite jetées.

### Flux secondaire, 30 secondes

```bash
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_SUB" \
  -t 30 -map 0:v:0 -f framemd5 - > /dev/null
```

**Observation :** 300 images traitées en 30 secondes, vitesse finale environ 1,08×, code de sortie 0.

### Flux principal 4K, 30 secondes

```bash
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_MAIN" \
  -t 30 -map 0:v:0 -f framemd5 - > /dev/null
```

**Observation :** le décodage a terminé avec un code de sortie 0. Ce test court ne démontre pas une capacité d'analyse 4K continue pendant des mois.

## 9. Vérifier la santé du Raspberry Pi

```bash
vcgencmd measure_temp
free -h
uptime
top
```

- `vcgencmd measure_temp` : température du processeur.
- `free -h` : mémoire vive et swap.
- `uptime` : durée de fonctionnement et charge moyenne.
- `top` : consommation CPU en direct ; quitter en appuyant sur **q**.

**Mesures au repos observées :** température **43,9 °C**, RAM totale environ **7,9 Gio**, mémoire utilisée environ **246 Mio**, charge moyenne presque nulle.

## 10. Installer l'outil de mesure des ressources

La commande `/usr/bin/time` n'était pas installée au départ. Nous l'avons installée avec :

```bash
sudo apt update
sudo apt install time
```

Contrôle :

```bash
/usr/bin/time -v true
```

Elle mesure notamment le temps CPU, le temps réel et le pic de mémoire.

## 11. Comparer 4K avec et sans décodage

### A. Avec décodage

```bash
/usr/bin/time -f 'CPU utilisateur : %U s
CPU système : %S s
CPU moyen : %P
Durée réelle : %e s
Mémoire maximale : %M Ko
Code de sortie : %x' \
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_MAIN" \
  -t 30 -map 0:v:0 -f framemd5 - > /dev/null
```

**Résultats mesurés :**

| Indicateur | Avec décodage |
| --- | ---: |
| CPU utilisateur | 49,83 s |
| CPU système | 0,27 s |
| CPU moyen | **163 %** |
| Durée réelle | 30,66 s |
| Mémoire maximale | 372368 Ko (~364 Mio) |
| Code de sortie | 0 |

Un pourcentage CPU supérieur à 100 % signifie que plusieurs cœurs sont mobilisés.

### B. Sans décodage (copie du flux compressé)

```bash
/usr/bin/time -f 'CPU utilisateur : %U s
CPU système : %S s
CPU moyen : %P
Durée réelle : %e s
Mémoire maximale : %M Ko
Code de sortie : %x' \
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_MAIN" \
  -t 30 -map 0:v:0 -c:v copy -f null - > /dev/null
```

**Résultats mesurés :**

| Indicateur | Sans décodage |
| --- | ---: |
| CPU utilisateur | 0,21 s |
| CPU système | 0,09 s |
| CPU moyen | **1 %** |
| Durée réelle | 31,60 s |
| Mémoire maximale | 60144 Ko (~59 Mio) |
| Code de sortie | 0 |

Deux avertissements **`Application provided invalid, non monotonically increasing dts`** sont apparus pendant ce dernier essai. Ils signalent des horodatages non croissants. Le code de sortie était néanmoins 0. La fréquence de ces anomalies devra être vérifiée lors d'un essai prolongé.

### Interprétation

La **réception et copie d'un flux 4K compressé** demandent très peu de CPU sur ce banc d'essai. Le **décodage des images 4K** demande nettement plus de ressources. Ces résultats ne constituent **pas encore** une mesure de la consommation électrique ni une validation de la retransmission Internet.

## 12. Problèmes rencontrés et solutions

| Problème | Explication ou correction |
| --- | --- |
| `rstp://` ne fonctionne pas | Faute de frappe : utiliser `rtsp://`. |
| Erreur `401 Unauthorized` | Fournir les bons identifiants RTSP. |
| Mot de passe contenant `>` | Encoder `>` en `%3E` dans une URL, sans publier le secret. |
| VLC ne lit pas le flux | FFplay/FFmpeg ont fonctionné dans notre configuration. |
| Fenêtre FFplay inaccessible en haut de l'écran | Sous certains bureaux Linux, maintenir **Alt + clic gauche** pour déplacer la fenêtre ; touche **f** pour plein écran. |
| `non monotonically increasing dts` | Avertissement d'horodatage, surtout visible lors de la copie sans décodage. |
| `/usr/bin/time` introuvable | Installer le paquet `time`. |
| `ps ... | grep ffmpeg` ne montre rien | Normal si FFmpeg a déjà terminé son test. |

## 13. Sécurité et confidentialité

- **Changer le mot de passe d'Umbra** : il a été visible dans une photographie de terminal au cours de la phase d'essai. Le considérer comme exposé.
- Ne jamais publier le mot de passe, un QR code de configuration, des URL RTSP contenant les identifiants ou des captures de terminal montrant ces données.
- Ne pas stocker les mots de passe dans le dépôt, même privé.
- Ne pas publier les coordonnées des emplacements de suivi de la faune ou les lieux de pose sensibles.
- En fin de session, supprimer les variables temporaires :

```bash
unset CAM_PASS RTSP_SUB RTSP_MAIN
```

Cette commande ne supprime **pas** les secrets éventuellement présents dans des captures, des journaux ou l'historique déjà enregistré.

## 14. État d'avancement et prochaines vérifications

- [x] Caméra initialisée dans Reolink et nommée Umbra.
- [x] RTSP activé et port 554 accessible.
- [x] Authentification RTSP fonctionnelle.
- [x] Flux secondaire H.264 reçu.
- [x] Flux principal 4K HEVC identifié.
- [x] Décodage de 30 secondes testé sur le Raspberry Pi 5.
- [x] Charge CPU comparée avec et sans décodage.
- [ ] Vérifier et photographier le câblage PoE exact.
- [ ] Relever les menus Reolink et versions de firmware.
- [ ] Renouveler le mot de passe exposé.
- [ ] Réserver une adresse IP stable à Umbra.
- [ ] Mesurer la consommation électrique de la chaîne complète.
- [ ] Tester la stabilité RTSP sur une longue durée.
- [ ] Tester l'enregistrement, la retransmission sécurisée et les redémarrages.
- [ ] Réaliser l'essai d'endurance de 72 heures prévu pour Noctua.

**Méthode :** observer → tester → mesurer → documenter → améliorer.