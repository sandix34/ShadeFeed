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
- [x] first Raspberry Pi boot
- [x] first SSH connection
- [x] system update
- [x] system temperature check
- [x] power / throttling check
- [x] storage check
- [x] Git installed and configured
- [x] Python virtual environment created
- [x] GitHub SSH authentication configured
- [ ] first Python test

## First boot validation — 2026-09-08

- Hostname: `noctua`
- Operating system: Debian GNU/Linux 13 (trixie)
- Debian version: 13.5
- Architecture: 64-bit ARM
- Initial IPv4 address: `192.168.1.37`
- Local network hostname: `noctua.home`
- SSH access: operational
- Idle CPU temperature: 48.8 °C
- Throttling status: `0x0`
- Root filesystem size: 235 GB
- Available storage: 223 GB
- Git version: 2.47.3
- Python virtual environment: `.venv`
- GitHub access: SSH authentication operational

### Network note

During the first boot, `noctua.local` did not resolve from Kali Linux.

The Raspberry Pi was discovered on the local network at `192.168.1.37`.

The home router resolves the Raspberry Pi as `noctua.home`.

## Next steps

1. Complete the initial software project structure.
2. Run the first Python test.
3. Validate the development workflow between Kali Linux, GitHub and Noctua.
4. Prepare camera connectivity tests.
5. Continue test-bench integration as hardware becomes available.

## Notes

The Raspberry Pi is configured as a headless system.

No monitor, keyboard or mouse should be required for normal operation.

Administration will primarily be performed remotely from Kali Linux using SSH.