---
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 3
---

# Noctua — Autonomous Wildlife Camera

## 1. Mission

### Field observation
- Long-term, low-disturbance wildlife monitoring
- Day and night operation
- Live video accessible remotely
- Protect sensitive observation locations

### Method
- Observe
- Test
- Measure
- Document
- Improve
- Deploy only after validation

## 2. Current status — October 2026

### Completed
- Raspberry Pi 5 purchased and initialized
- Linux updates and health checks
- SSH access and GitHub SSH configuration
- Python virtual environment
- Reolink RLC-811A camera received and named Umbra
- PLANET IPOE-162 received
- RTSP connectivity and video stream identification
- Initial 4K CPU and memory comparison
- Beginner-friendly RTSP documentation

### Not yet validated
- Exact PoE wiring documentation and full electrical checks
- Stable recording and timestamp handling
- Long-duration network and thermal performance
- Complete power consumption
- Cellular connectivity and secure remote viewing
- Solar and battery sizing
- 72-hour endurance test
- Unattended field operation

## 3. Test-bench architecture

### Camera — Umbra
- Reolink RLC-811A
- Ethernet and PoE
- Secondary RTSP: H.264, 640 × 360
- Main RTSP: H.265, 3840 × 2160
- Night and infrared behavior to be measured

### Main computer — Noctua
- Raspberry Pi 5
- Linux, Python and FFmpeg
- SSH administration
- Monitoring and future automation

### Power and PoE
- PLANET IPOE-162 injector
- LEICKE NT03242 24 V / 2 A supply
- Measured supply output: 24.46 V DC
- Confirm wiring and electrical compatibility before reproducing
- Complete energy measurements pending

### Storage — planned
- USB 3 SSD
- Recordings and logs
- Retention and capacity tests pending

### Connectivity — planned
- Teltonika RUT241
- 4G connection
- Secure remote access
- Network recovery tests

## 4. Initial video results

### Main 4K stream, 30 seconds
- Decoding: FFmpeg CPU 163%, peak RSS approximately 364 MiB
- Compressed stream copy: FFmpeg CPU 1%, peak RSS approximately 59 MiB
- Both tests exited with status 0
- Non-monotonic DTS warnings observed during copy
- Short tests do not prove endurance

### Working architecture hypothesis
- Lower-resolution H.264 stream for analysis
- Main 4K H.265 stream for selected recordings
- No unnecessary full-frame 4K transcoding
- Implementation and validation still pending

## 5. Planned 72-hour test bench

### Monitoring
- Power draw and day/night differences
- Video stream continuity
- Camera and Raspberry Pi temperatures
- Network interruptions and reconnection
- Storage growth and integrity
- Reboot and power-loss recovery

### Success criteria
- Documented measurements
- Reproducible test procedure
- Known energy and storage requirements
- Explicit record of failures and limitations

## 6. Field power — not finalized

### Proposed components
- Battery
- Solar panel
- Charge controller / MPPT
- Suitable power regulation

### Design requirements
- Several months without manual intervention
- Forest shade and difficult access may limit solar generation
- Size only after realistic consumption and site measurements

## 7. Documentation and security

### Files
- README.md
- project-map.md
- docs/umbra-installation-rtsp-performance.md
- docs/project-map.svg (simplified visual overview)

### Rules
- English documentation
- Beginner-reproducible commands and explanations
- Mark tested vs planned steps
- Never commit passwords, private keys or expanded authenticated URLs
- Never publish sensitive field coordinates
- Date important decisions and measurements

## 8. Possible future development
- Wildlife event detection
- Audio recording / AudioMoth integration
- Automated monitoring and reports
- Multi-camera expansion
- Embedded AI
