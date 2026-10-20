# Raspberry Pi 5 Setup — Noctua

**Initial setup:** 2026-09-08  
**Reviewed:** 2026-10-19  
**Status:** Basic system setup completed; camera RTSP tests completed later. Long-term operation is not yet validated.

## Purpose

Document the Raspberry Pi 5 setup used for the Noctua wildlife observation test bench, including reproducible commands and observed results.

## Hardware

- Raspberry Pi 5, 8 GB RAM
- SanDisk Extreme PRO 256 GB microSD
- 27 W USB-C power supply for initial setup
- Kali Linux computer for remote administration

## Operating system

- Raspberry Pi OS Lite, 64-bit, headless
- Observed base: Debian GNU/Linux 13 (Trixie), version 13.5 at first validation
- Hostname: `noctua`
- Time zone: `Europe/Paris`
- French keyboard and locale configuration

Raspberry Pi Imager was used from Kali Linux. Wi-Fi and SSH were configured during imaging. Raspberry Pi Connect was disabled.

## Remote administration

**Observed working local hostname:** `noctua.home`.

From Kali Linux:

```bash
ssh sandrine@noctua.home
```

Replace the account name and hostname to match your own environment. During initial setup, `noctua.local` did not resolve, so `noctua.home` or the current local IP address was used.

SSH password authentication was enabled during initial imaging. Review authentication settings and key-based access before field deployment. Never publish passwords or private SSH keys.

## Initial validation — 2026-09-08

| Item | Observed result |
| --- | --- |
| Local IPv4 address | `192.168.1.37` at first boot; may change |
| Hostname | `noctua` |
| Local name | `noctua.home` |
| OS | Debian GNU/Linux 13 (Trixie) |
| Debian version | 13.5 |
| Architecture | 64-bit ARM |
| Idle CPU temperature | 48.8 °C |
| Throttling status | `0x0` |
| Root filesystem size | 235 GB |
| Available storage | 223 GB |
| Git | 2.47.3 |
| Python environment | `.venv` |
| GitHub access | SSH authentication confirmed |

These values are historical observations, not a claim about the current software versions, IP address or temperature.

## Useful checks

Run these on the Raspberry Pi:

```bash
hostnamectl
cat /etc/os-release
uname -m
vcgencmd measure_temp
vcgencmd get_throttled
free -h
df -h
uptime
git --version
python3 --version
```

The commands display the host configuration, operating system, CPU architecture, temperature, throttling flags, memory, disk usage, uptime and tool versions. No changes are made by these checks.

## Completed milestones

- [x] microSD prepared and OS installed
- [x] First boot and SSH access
- [x] System update and basic health checks
- [x] Git and GitHub SSH access
- [x] Python virtual environment created
- [x] Umbra RTSP stream reception and short FFmpeg tests (October 2026)

## Next steps

- [ ] Document the Python environment and its actual dependencies
- [x] Create and test the first project-specific Python script: Umbra TCP/554 availability monitor (2026-10-20)
- [ ] Validate stable camera network addressing
- [ ] Review SSH security before remote Internet access
- [ ] Configure and test automatic monitoring startup and recovery with systemd
- [ ] Complete the planned 72-hour endurance test

For video commands and measured results, see the [Umbra guide](umbra-installation-rtsp-performance.md).
