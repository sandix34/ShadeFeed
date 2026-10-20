# Umbra Camera Availability Monitor

**First manual validation:** 2026-10-20  
**Implementation:** [`src/wildlife_station/camera_monitor.py`](../src/wildlife_station/camera_monitor.py)  
**Status:** Basic network check validated; unattended operation not yet implemented.

## Purpose

The monitor checks whether the camera's RTSP TCP port (554) is reachable on the test-bench local network. It is a first supervision component, **not** a video-quality or stream-decoding test.

## Current behavior

- Attempts a TCP connection to the configured camera address and port, with a five-second timeout.
- Repeats every 30 seconds while the script is running.
- Prints a timezone-aware timestamp and `ONLINE` or `OFFLINE` for each check.
- Appends an event to `logs/camera_monitor.log` only when the observed status changes, including the first observation.
- Stops gracefully on Ctrl+C (`KeyboardInterrupt`).

The current camera address is a hard-coded private LAN address used only for the bench. It must be configurable before deployment. The log path is relative to the working directory; run the command from the repository root.

## Run manually

From the Raspberry Pi, in the repository root:

```bash
python3 src/wildlife_station/camera_monitor.py
```

Stop with **Ctrl+C**. Inspect the event log:

```bash
cat logs/camera_monitor.log
```

No third-party Python packages are required by this version.

## Manual validation evidence — 2026-10-20

The camera was initially reachable. Disconnecting only its network connection and then reconnecting it produced these observations (Europe/Paris local time):

```text
2026-10-20T17:28:36+02:00 | Umbra | ONLINE
2026-10-20T17:29:06+02:00 | Umbra | OFFLINE
2026-10-20T17:29:41+02:00 | Umbra | ONLINE
```

The event log contained the transitions but not the repeated unchanged `ONLINE` observation. An earlier `ONLINE` entry was also present from a previous run.

## Known limitations and next steps

1. An open TCP port does **not** guarantee valid RTSP authentication, frame delivery or image quality.
2. No systemd service, automatic startup, process restart policy or boot test has been implemented.
3. The monitor does not attempt to reconnect or repair the camera; it only reports reachability.
4. A brief outage between checks may be missed; the exact detection time depends on polling and connection timeout.
5. The IP address, check interval, logging policy and storage path should become configurable.
6. Add tests for the monitoring logic and assess long-duration reliability before field use.

**Security:** Do not commit camera credentials, full authenticated RTSP URLs, logs containing sensitive data or precise wildlife site locations.
