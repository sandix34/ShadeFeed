# Raspberry Pi 5 setup

## Purpose

This document records the initial software setup of the Raspberry Pi 5 used in the Autonomous Wildlife Camera project.

## Hardware

- Raspberry Pi 5
- SanDisk Extreme PRO 256 GB microSD
- USB-C 27 W power supply

## Operating system

- Raspberry Pi OS Lite
- 64-bit
- Debian-based Linux
- No desktop environment

## Installation tool

Raspberry Pi Imager was used from Kali Linux to prepare the microSD card.

## System configuration

Hostname:

`noctua`

Locale:

- Country: France
- Time zone: Europe/Paris
- Keyboard: French

Network:

- Wi-Fi configured during imaging
- SSH enabled
- Password authentication enabled

Raspberry Pi Connect:

- Disabled

## Administration

The Raspberry Pi will normally be administered remotely from Kali Linux using SSH.

Example:

```bash
ssh sandrine@noctua.local
```

## Status

- [x] microSD prepared
- [x] Raspberry Pi OS Lite 64-bit installed
- [x] hostname configured as `noctua`
- [x] Wi-Fi configured
- [x] SSH enabled
- [ ] first Raspberry Pi boot
- [ ] first SSH connection
- [ ] system update
- [ ] system temperature check
- [ ] storage check
- [ ] first Python test

## Next steps

Once the Raspberry Pi 5 and its power supply are available:

1. Insert the prepared microSD card.
2. Power on the Raspberry Pi.
3. Wait for the first boot to complete.
4. Check network availability from Kali Linux.
5. Connect to Noctua using SSH:

```bash
ssh sandrine@noctua.local
```

6. Verify the operating system and hardware.
7. Update the system.
8. Check CPU temperature and storage.
9. Run the first Python test.

## Notes

The Raspberry Pi is configured as a headless system.

No monitor, keyboard or mouse should be required for normal operation.

Administration will primarily be performed remotely from Kali Linux using SSH.