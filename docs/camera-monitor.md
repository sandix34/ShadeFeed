# Umbra network and RTSP monitoring

## Current behavior — 7 November 2026

`src/wildlife_station/camera_monitor.py` first checks the camera's TCP port
554 (5-second timeout). If reachable, it runs FFmpeg over TCP, explicitly
selecting video stream `0:v:0`, requesting a 10-second decoded sample and
applying a 25-second process timeout. No recording file is created.

A healthy sample requires both exit code zero and a positive decoded-frame
count in FFmpeg's progress output. This proves some video was decoded; it
does not guarantee a full ten seconds, image quality, freshness of the scene,
or uninterrupted video between samples. FFmpeg errors and URLs are not printed.

Output contains `Network: ONLINE/OFFLINE | Stream: OK/FAILED`.
An unreachable network skips FFmpeg and reports Stream FAILED; this does not
independently diagnose a camera video fault. Only status transitions, including
the first observation, are appended to `logs/camera_monitor.log`.

The loop sleeps 30 seconds **after** each check. Check start times are therefore
roughly 40 seconds apart for a normal 10-second sample, with additional startup
overhead; timeouts can increase this. The timestamp marks the start of the check.
Logs are append-only; retention/rotation remains to be implemented for endurance use.

## Configuration and operation

- Python 3 and the `ffmpeg` executable on PATH are required.
- `RTSP_URL` must contain the authenticated camera stream URL. Startup fails
  explicitly if it is missing; it is not read from a shell session by systemd.
- The bench IP `192.168.1.28`, port and timing remain code constants.
- Run from the repository root so the relative log path is correct.
- Manual execution: `python3 src/wildlife_station/camera_monitor.py`, after
  supplying RTSP_URL locally. Ctrl+C stops a manual run.
- Use the [systemd guide](camera-monitor-systemd.md) for unattended execution.
- Run [unit tests](../tests/README.md) without a camera or real credentials.

## Evidence and limits

On 2026-10-20 the network-only monitor detected intentional network disconnection
and reconnection: ONLINE at 17:28:36, OFFLINE at 17:29:06, ONLINE at 17:29:41
(Europe/Paris). Only transitions were retained in the file log.

On 2026-11-07 the network-only service boot and SIGKILL recovery were observed.
PR #1 later added RTSP monitoring and reported a successful Raspberry Pi stream
test. The subsequent audit adds frame-count validation and explicit systemd
configuration: deployment and hardware revalidation of this revision are pending.

The monitor reports availability; it does not repair the camera or restart it.
systemd restarts a failed monitor process, not a camera that reports FAILED.
The 72-hour test, power measurements, recording integrity and field operation
remain unvalidated. Never commit credentials or sensitive site locations.
