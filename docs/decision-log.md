# Technical Decision Log

This document records **decisions**, their rationale and their validation status. A design choice is not the same as a completed installation.

## 2026-08 — One camera for V1

**Status:** Accepted.

**Decision:** Build and validate a single-camera station before considering a second camera.

**Rationale:** Limit integration complexity and make faults easier to diagnose.

**Consequence:** Multi-camera operation is deferred.

## 2026-08 — 72-hour test bench before final power sizing

**Status:** Accepted; test not yet performed.

**Decision:** Measure the assembled station for 72 hours before final battery and solar sizing.

**Rationale:** Real day/night loads, IR illumination and network behavior must be measured.

**Consequence:** Battery, solar panel and charge controller remain provisional.

## 2026-08 — USB 3 SSD for local storage

**Status:** Architecture decision accepted; integration pending.

**Decision:** Plan local recording on a USB 3 SSD.

**Rationale:** Provide dedicated recording storage while keeping the Raspberry Pi PCIe interface available for possible future extensions.

**Consequence:** Capacity, endurance, file integrity and power draw still require validation.

## 2026-09 — Headless Raspberry Pi OS Lite

**Status:** Accepted and initially validated.

**Decision:** Use Raspberry Pi OS Lite 64-bit on Raspberry Pi 5.

**Rationale:** The station will usually be administered remotely over SSH and does not require a graphical desktop.

**Observed:** Debian GNU/Linux 13 (Trixie), SSH operational, hostname `noctua`.

**Consequence:** Administration uses the local network initially; secure remote access remains to be designed.

## 2026-10 — Separate video acquisition from full-resolution decoding

**Status:** Provisional technical direction; not yet implemented as a continuous pipeline.

**Evidence:** The main 4K HEVC stream was received and processed during 30-second tests. Full-frame decoding averaged **163% FFmpeg CPU** and approximately **364 MiB peak RSS**; compressed stream copy averaged **1% CPU** and approximately **59 MiB peak RSS**.

**Direction:** Prefer the secondary H.264 stream for future analysis and preserve the compressed 4K stream for selected recordings where appropriate.

**Open questions:** Stream-copy timestamp warnings, recording integrity, synchronization, actual energy consumption and long-term stability.

**Reference:** [Umbra RTSP and performance guide](umbra-installation-rtsp-performance.md).

## 2026-10 — Reassess the test-bench power topology

**Status:** Open; **no final electrical decision**.

**Reason:** The original conceptual test-bench diagram uses a 12 V distribution concept, while a LEICKE 24 V / 2 A supply has been measured and used during the recent camera integration phase.

**Decision:** Do not treat the historical 12 V diagram as a validated wiring instruction. Verify the actual PLANET IPOE-162 input requirements, the camera's PoE mode and all power conversions before choosing the final topology.

**Consequence:** Final distribution voltage, converters, fuse ratings and battery/solar design remain pending.

**Reference:** [V1 test-bench plan](test-bench-v1.md).

## 2026-10 — English documentation and protected field locations

**Status:** Accepted documentation policy.

**Decision:** Keep repository documentation in English, label measured versus planned features, and never publish credentials or sensitive wildlife locations.

**Consequence:** Technical records can be shared publicly without disclosing field sites or secrets.

## 2026-10-20 — Initial camera network availability monitoring

**Status at 2026-10-20:** Implemented and manually tested; automatic startup was pending. See the 7 November update below.

**Implementation:** `src/wildlife_station/camera_monitor.py` checks whether Umbra's TCP port 554 accepts connections every 30 seconds. It prints each check and appends only state changes to `logs/camera_monitor.log`.

**Observed:** An intentional network disconnection produced `ONLINE → OFFLINE → ONLINE` on 2026-10-20, and the log retained the transitions. The log is excluded from Git.

**Limitation:** A successful TCP connection does not prove that RTSP authentication or video frames are working. The script is currently run manually, does not recover itself after a process or system restart, and uses a test-bench LAN address.

**Next steps:** Document and test a systemd service, validate startup/restart behavior, then add an actual video-stream health check.

**Reference:** [Camera monitor guide](camera-monitor.md).

## 2026-11-07 — Supervised network and video monitoring

**Observed:** Network-only service boot at 14:39:10 CET and automatic restart
following SIGKILL at 14:55:16 CET; Umbra ONLINE in both cases.

**Implemented:** PR #1 merged network and RTSP checks plus six initial tests.
Its validation notes report a successful Raspberry Pi RTSP test.

**Audit corrections:** Require a video stream and positive decoded-frame count,
load RTSP_URL through a mandatory root-only local environment file, explicitly
reject missing configuration at startup, isolate unit tests from real environment
variables, and document the actual check-duration-plus-30-second cadence.
Eleven standard-library tests replace the six environment-dependent tests.

**Validation boundary:** Unit tests cover mocked behavior. Revised service
installation, real video samples, reboot and failure recovery must be revalidated
on the Raspberry Pi. No endurance or off-grid readiness is claimed.

**References:** [Monitor](camera-monitor.md), [deployment](camera-monitor-systemd.md),
[tests](../tests/README.md).
