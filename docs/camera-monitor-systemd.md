# Camera monitor — systemd service

## Validation — 2026-11-07

- Installed and enabled shadefeed-camera-monitor.service.
- Configuration checked with systemd-analyze verify: no messages.
- Service initially active, with Umbra ONLINE.
- Rebooted the Raspberry Pi.
- Service started automatically at 14:39:10 CET.
- Umbra reported ONLINE at 14:39:10 and 14:39:40 CET.
- Recovery after a forced SIGKILL was validated on 2026-11-07.
  systemd restarted the monitor automatically at 14:55:16 CET.
  Restart counter: 1. Service active; Umbra ONLINE.

## Configuration

Service file: config/systemd/shadefeed-camera-monitor.service

This configuration uses the local user sandrine and the project
directory /home/sandrine/autonomous-wildlife-camera.
Adapt both before installing on another machine.

The service runs the Python monitor in the background.
Restart=on-failure requests a restart after 10 seconds if it fails.

## Limitations and next steps

- Automatic startup after reboot is validated.
- Monitoring checks TCP port 554, not actual video frames.
- Long-duration reliability remains to be tested.
