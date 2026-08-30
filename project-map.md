---
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 3
---

# Projet caméra animalière autonome

## 1. Objectif du projet

### Finalité
- Concevoir une station caméra animalière autonome
- Permettre une observation longue durée sur le terrain
- Pouvoir superviser le système à distance
- Documenter chaque choix technique

### Objectifs principaux
- Autonomie longue durée
- Vision jour / nuit
- Connexion 4G
- Stockage local
- Alimentation solaire
- Système fiable et évolutif

### Principe de travail
- Concevoir
- Tester
- Mesurer
- Corriger
- Documenter
- Déployer seulement après validation

## 2. Architecture générale

### Caméra
- Reolink RLC-811A
- Ethernet
- PoE
- Vision nocturne

### Cerveau du système
- Raspberry Pi 5
- Linux
- Scripts Python
- Supervision
- Journalisation

### Stockage
- SSD USB 3
- Stockage local des données

### Communication
- Routeur 4G Teltonika RUT241
- Accès distant
- Réseau local du système

### Énergie
- Architecture 12 V
- Batterie
- Solaire
- Régulation
- Dimensionnement final après mesures réelles

## 3. Pourquoi un banc de test

### Problème
- Les consommations réelles ne sont pas encore connues
- Le comportement de nuit peut modifier fortement la consommation
- La stabilité réseau doit être vérifiée
- Les redémarrages et coupures doivent être testés

### Décision
- Construire un banc de test avant de figer l'installation terrain

### Objectif du banc
- Valider l'architecture complète
- Mesurer les consommations
- Tester la stabilité
- Identifier les points faibles
- Corriger avant le déploiement

## 4. Banc de test V1

### Durée cible
- 72 heures

### Périmètre
- Une seule caméra
- Raspberry Pi
- SSD
- Réseau
- 4G
- PoE
- Mesures
- Pas de solaire dans un premier temps

### Critère de réussite
- Système stable
- Mesures exploitables
- Redémarrage maîtrisé
- Consommation connue
- Stockage connu
- Architecture comprise et documentée

## 5. Raspberry Pi

### Choix
- Raspberry Pi 5

### Matériel associé
- Active Cooler
- Boîtier
- Alimentation adaptée

### Rôle
- Piloter les tests
- Communiquer avec la caméra
- Exécuter les scripts Python
- Enregistrer les résultats
- Produire les logs
- Préparer une future interface

## 6. Alimentation / PoE

### Éléments étudiés
- IPOE-162
- Bloc d'alimentation
- Connecteur jack femelle avec fils
- Câbles nécessaires
- Ethernet

### Sécurité
- Prise murale standard côté secteur
- Pas de manipulation dangereuse côté 230 V
- Travail côté basse tension pour les essais

### Mesure
- Multimètre
- Vérification tension
- Vérification continuité
- Diagnostic du câblage

## 7. Réseau

### Développement à la maison
- Raspberry connecté au Wi-Fi de la maison
- Ordinateur sur le même réseau
- Pas de routeur dédié nécessaire pour la V1 de développement

### Accès au Raspberry
- SSH
- VS Code Remote

### Terrain
- RUT241 pour la 4G
- Réseau local de la station
- Accès distant à définir précisément

## 8. Logiciel

### Poste de travail
- Kali Linux
- Windows
- VS Code

### Raspberry
- Linux
- Python
- Git

### Python
- Apprentissage au fil du projet
- Scripts simples au départ
- Automatisation progressive

### GitHub
- Versionnement
- Documentation
- Historique des décisions
- Partage futur du projet

### Sécurité
- Aucun mot de passe dans le dépôt
- Variables d'environnement
- Fichiers locaux exclus
- `.gitignore`

## 9. Mesures prévues

### Énergie
- Tension
- Consommation
- Consommation moyenne
- Pics
- Différence jour / nuit

### Réseau
- Connectivité
- Latence
- Déconnexions
- Reconnexion
- Stabilité 4G

### Caméra
- Fonctionnement jour
- Fonctionnement nuit
- IR
- Qualité d'image
- Stabilité du flux

### Stockage
- Volume produit
- Débit
- Espace utilisé sur 72 h

### Fiabilité
- Température
- Fonctionnement prolongé
- Redémarrage Raspberry
- Redémarrage caméra
- Reprise après coupure

## 10. Énergie définitive

### Avant validation
- Batterie et solaire non figés définitivement

### Après le test 72 h
- Calcul du besoin quotidien réel
- Dimensionnement batterie
- Dimensionnement solaire
- Marges de sécurité
- Choix du régulateur / MPPT

## 11. Documentation du projet

### Documents
- README
- Markmap
- Schémas
- BOM
- Procédures de test
- Résultats
- Journal des décisions

### Règle
- Chaque choix important doit être daté
- Chaque changement doit expliquer pourquoi
- Les pistes abandonnées doivent rester visibles

## 12. V2

### Évolutions possibles
- Deux caméras
- Automatisation avancée
- Comparaison des résultats
- Interface de supervision
- Analyse automatique
- IA embarquée

## 13. État actuel

### Déjà défini
- Projet de station caméra animalière autonome
- Raspberry Pi 5
- Reolink RLC-811A
- SSD USB 3
- Teltonika RUT241
- Architecture 12 V
- Banc de test 72 h
- Une caméra pour la V1
- Kali Linux + VS Code
- Python
- GitHub
- Documentation Markmap

### À finaliser
- Schéma électrique du banc
- Alimentation exacte
- Choix final du multimètre
- Achat Raspberry Pi 5
- Boîtier et refroidissement
- Montage PoE
- Procédure de test 72 h
- Structure du dépôt GitHub