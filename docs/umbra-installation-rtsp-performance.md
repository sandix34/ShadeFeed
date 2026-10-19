# Umbra — camera installation, RTSP and Raspberry Pi 5 performance tests

**Project:** Noctua, autonomous wildlife monitoring station  
**Test period:** October 2026  
**Status:** Local video reception and short performance tests completed. Autonomous field operation has **not** been validated.

> **Beginner's guide.** This document reconstructs observed procedures, explains the commands and separates confirmed results from steps that still require verification. No actual passwords are included.

## 1. Hardware and its purpose

- **Reolink RLC-811A**, named **Umbra**: IP camera with Ethernet and PoE connectivity.
- **PLANET IPOE-162**: industrial PoE injector supplying network data and power to the camera.
- **Raspberry Pi 5**, named **Noctua**: receives and processes the video stream.
- **LEICKE NT03242**, 24 V / 2 A: supply output previously measured at **24.46 V DC**.
- **Kali Linux computer**: used to access the Raspberry Pi through SSH.

**Electrical safety:** 24.46 V is a measurement at the **power supply output**, not at the PoE output. Before connecting anything, verify the injector's exact input specifications, polarity, connector type, port labels and camera compatibility using the device manuals. Never connect a 24 V supply directly to an Ethernet port or the camera's 12 V input.

### PoE connections — inspection still required

1. Identify the injector's **LAN/Data In** port and **PoE/Data+Power Out** port; check the labels on the actual unit.
2. Connect the local network to the data input.
3. Connect the camera to the PoE output.
4. Connect the correctly specified power supply to the injector.
5. Check the indicators and confirm that the camera appears on the network.

These are the **general connections to verify**, not a complete photographic record of the original assembly. Cable types, lengths, labels and LED states have not yet been archived.

## 2. Initial camera setup

1. Install the **Reolink** application on a phone.
2. Add the camera and create a strong, unique administrator password.
3. Name the camera **Umbra**.
4. Enable **RTSP** in the camera's network settings. The exact menu location may vary with firmware and still needs to be recorded.
5. Find the camera's local IP address. In our test network it was `192.168.1.28`; **your address may differ**.
6. Check TCP port **554**, the RTSP service port.

On a machine with `nmap` installed:

```bash
nmap -p 554 192.168.1.28
```

**Observed:** TCP port 554 was open. An unauthenticated RTSP request returned **401 Unauthorized**, meaning credentials were required.

## 3. Connect to Noctua from Kali Linux

Open a terminal **on the Kali computer**:

```bash
ssh sandrine@noctua.home
```

- `ssh`: opens an encrypted remote terminal session.
- `sandrine`: the Raspberry Pi account used in these tests; replace it with your account name.
- `noctua.home`: the Pi's local hostname; use its IP address if name resolution does not work.

Enter the SSH password if prompted. No characters will appear while typing: **this is normal**.

Unless otherwise stated, the following commands are run **on the Raspberry Pi in this SSH session**, not on Kali.

## 4. Install and verify the video tools

Check whether FFmpeg and FFprobe are installed:

```bash
ffmpeg -version
ffprobe -version
```

If either command is missing:

```bash
sudo apt update
sudo apt install ffmpeg
```

- **FFmpeg** processes video streams.
- **FFprobe** reports stream properties.
- **FFplay** plays video on a computer with a graphical display.

VLC was tried without success in our setup, while FFplay worked. This does **not** imply that VLC is generally incompatible with Reolink cameras.

## 5. RTSP authentication without publishing the password

In the Raspberry Pi's SSH terminal, enter:

```bash
read -rsp "Umbra password: " CAM_PASS; echo
```

Type the password and press Enter. It is not displayed. `CAM_PASS` is a temporary shell variable, available in **this terminal session only**.

**Historical detail:** the test password contained the character `>`, which must be encoded as `%3E` when placed in a URL. The commands below reproduce the tested method **only if `>` is the only reserved character requiring URL encoding**:

```bash
CAM_IP="192.168.1.28"
RTSP_SUB="rtsp://admin:${CAM_PASS//>/%3E}@${CAM_IP}:554/Preview_01_sub"
RTSP_MAIN="rtsp://admin:${CAM_PASS//>/%3E}@${CAM_IP}:554/Preview_01_main"
```

- `CAM_IP`: the camera's local IP address.
- `RTSP_SUB`: the secondary, lower-resolution video stream.
- `RTSP_MAIN`: the main, high-resolution video stream.
- `${CAM_PASS//>/%3E}`: replaces every `>` in the password with `%3E`.

**Limitations:** other reserved characters such as `@`, `:`, `/`, `?`, `#` and `%` require appropriate URL encoding. Do not use this simplified substitution for an arbitrary password. A password embedded in a command-line URL may also be visible in process listings or diagnostic logs. This was a **controlled local test method**, not a hardened production authentication design.

**Never commit an expanded RTSP URL containing the real password.** Never publish a terminal screenshot that reveals it.

## 6. Inspect the secondary stream

Run:

```bash
ffprobe -v error -rtsp_transport tcp \
  -i "$RTSP_SUB" \
  -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1
```

**What the options mean:**
- `-v error`: show only errors.
- `-rtsp_transport tcp`: use TCP to transport RTSP video.
- `-i "$RTSP_SUB"`: connect to the secondary stream.
- `-select_streams v:0`: inspect the first video stream.
- `-show_entries ...`: show codec, dimensions and reported frame rate.
- `-of default=noprint_wrappers=1`: print readable key/value output.

**Observed:** H.264 video, **640 × 360**, reported frame rate **25/1**. Another playback displayed approximately 10 fps; that discrepancy remains to be investigated.

To view video on a computer with a graphical desktop and FFplay:

```bash
ffplay -rtsp_transport tcp -i "$RTSP_SUB"
```

An ordinary headless SSH session does not display an FFplay window on the Raspberry Pi.

## 7. Inspect the main 4K stream

```bash
ffprobe -v error -rtsp_transport tcp \
  -i "$RTSP_MAIN" \
  -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1
```

**Actual output:**

```text
codec_name=hevc
width=3840
height=2160
r_frame_rate=51/2
```

This is **H.265/HEVC**, **3840 × 2160 (4K)** video with a reported frame rate of **25.5 fps**.

## 8. Decode video without saving a file

`/dev/null` discards output. The `framemd5` format computes hashes of decoded frames, which forces FFmpeg to decode the video before the output is discarded.

### Secondary stream, 30 seconds

```bash
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_SUB" \
  -t 30 -map 0:v:0 -f framemd5 - > /dev/null
```

**Observed:** 300 frames processed in 30 seconds, final processing speed around 1.08×, exit status 0.

### Main 4K stream, 30 seconds

```bash
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_MAIN" \
  -t 30 -map 0:v:0 -f framemd5 - > /dev/null
```

**Observed:** exit status 0. A successful short decode is **not** evidence that continuous 4K analysis can run for months.

**Option explanations:** `-t 30` limits the test to 30 seconds; `-map 0:v:0` selects the first video stream; `-f framemd5` forces decoded-frame hashing; `> /dev/null` discards the generated hashes.

## 9. Check Raspberry Pi health

```bash
vcgencmd measure_temp
free -h
uptime
top
```

- `vcgencmd measure_temp`: SoC temperature.
- `free -h`: RAM and swap use.
- `uptime`: time since boot and system load.
- `top`: live process activity; press **q** to quit.

**Observed at idle:** **43.9 °C**, approximately **7.9 GiB** total RAM, around **246 MiB** used, and a near-zero load average.

## 10. Install the resource measurement tool

The external `/usr/bin/time` utility was initially missing. It was installed using:

```bash
sudo apt update
sudo apt install time
```

Verify it:

```bash
/usr/bin/time -v true
```

Unlike the shell's built-in `time`, `/usr/bin/time` can report detailed CPU use, elapsed time and peak resident memory.

## 11. Compare 4K with and without decoding

### A. Full 4K decoding

```bash
/usr/bin/time -f 'User CPU: %U s
System CPU: %S s
Average CPU: %P
Elapsed time: %e s
Maximum resident memory: %M KB
Exit status: %x' \
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_MAIN" \
  -t 30 -map 0:v:0 -f framemd5 - > /dev/null
```

**Measured results:**

| Metric | Full decode |
| --- | ---: |
| User CPU | 49.83 s |
| System CPU | 0.27 s |
| Average FFmpeg CPU | **163%** |
| Elapsed time | 30.66 s |
| Peak resident memory | 372,368 KB (~364 MiB) |
| Exit status | 0 |

CPU percentages above 100% mean that the process used more than one logical CPU core on average. This is **process CPU usage**, not the percentage of the entire Raspberry Pi's capacity.

### B. Copy compressed 4K packets without decoding

```bash
/usr/bin/time -f 'User CPU: %U s
System CPU: %S s
Average CPU: %P
Elapsed time: %e s
Maximum resident memory: %M KB
Exit status: %x' \
ffmpeg -hide_banner -loglevel error \
  -rtsp_transport tcp -i "$RTSP_MAIN" \
  -t 30 -map 0:v:0 -c:v copy -f null - > /dev/null
```

**Measured results:**

| Metric | Compressed stream copy |
| --- | ---: |
| User CPU | 0.21 s |
| System CPU | 0.09 s |
| Average FFmpeg CPU | **1%** |
| Elapsed time | 31.60 s |
| Peak resident memory | 60,144 KB (~59 MiB) |
| Exit status | 0 |

Here, `-c:v copy` tells FFmpeg **not to decode or re-encode** the video. `-f null` sends the packets to a test output without creating a video recording.

**Warning observed twice:** `Application provided invalid, non monotonically increasing dts`. This indicates non-increasing timestamps. The process still returned exit status 0. Real recordings must be tested separately to determine whether timestamps affect the saved files.

### Interpretation

On this short test bench, **receiving and copying compressed 4K video** required much less CPU and memory than **decoding every 4K frame**. The results do not measure electrical power draw and do not validate Internet streaming, long-term reliability or recording integrity.

A future design may analyze the H.264 secondary stream while recording selected high-resolution H.265 video without transcoding. This is a **design hypothesis**, not a completed feature.

## 12. Problems encountered and troubleshooting

| Symptom | Explanation or action |
| --- | --- |
| `rstp://` fails | Typo: use `rtsp://`. |
| `401 Unauthorized` | Valid RTSP credentials are required. |
| Password contains `>` | Encode it as `%3E` in a URL; never reveal the password. |
| VLC does not play the stream | FFplay/FFmpeg worked in this particular setup. |
| FFplay window is partly off-screen | On some Linux desktops, hold **Alt + left mouse button** to move a window; press **f** for fullscreen in FFplay. |
| `non monotonically increasing dts` | Timestamp warning observed during stream copy; requires further investigation. |
| `/usr/bin/time` is missing | Install the `time` package. |
| `ps ... | grep ffmpeg` shows no process | Normal after FFmpeg has finished the test. |

## 13. Security and privacy

- **Change Umbra's administrator password:** it appeared in a terminal photograph during testing and must be treated as exposed.
- Do not publish passwords, device pairing QR codes, authenticated RTSP URLs or screenshots containing credentials.
- Do not commit passwords to GitHub, even in a private repository.
- Do not publish wildlife observation site coordinates or sensitive camera placement locations.
- At the end of the session, clear the temporary variables:

```bash
unset CAM_PASS RTSP_SUB RTSP_MAIN
```

This does **not** remove any secret already saved in a screenshot, process log or shell history.

## 14. Progress checklist

- [x] Camera initialized in Reolink and named Umbra
- [x] RTSP enabled and TCP port 554 reachable
- [x] RTSP authentication tested
- [x] Secondary H.264 stream received
- [x] Main 4K HEVC stream identified
- [x] 30-second video decoding tested on Raspberry Pi 5
- [x] CPU and memory measured with and without 4K decoding
- [ ] Verify and photograph exact PoE wiring
- [ ] Record Reolink menus and firmware versions
- [ ] Rotate exposed camera password
- [ ] Reserve a stable IP address for Umbra
- [ ] Measure the complete system's electrical power consumption
- [ ] Test long-duration RTSP stability and timestamp behavior
- [ ] Test real recordings, secure remote streaming and restart recovery
- [ ] Run Noctua's planned 72-hour endurance test

**Working method:** Observe → Test → Measure → Document → Improve.
