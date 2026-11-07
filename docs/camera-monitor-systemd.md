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

## Scope of the evidence

The observations above concern the **network-only version** running at those
times. PR #1 subsequently introduced RTSP checks. The revised configuration
and frame-count check must be deployed and revalidated on the Raspberry Pi.
A repository commit does not update `/etc/systemd/system` automatically.

## Requirements

Python 3, FFmpeg on PATH, the camera's local credentials and network access.
The provided unit uses user `sandrine` and repository path
`/home/sandrine/autonomous-wildlife-camera`; adapt both for another installation.
It requests network-online ordering, but this does not guarantee camera availability.

## Install or upgrade on the Raspberry Pi

From the repository root, with a clean working tree:

```bash
git pull --ff-only
sudo install -d -m 700 /etc/shadefeed
sudo touch /etc/shadefeed/camera-monitor.env
sudo chmod 600 /etc/shadefeed/camera-monitor.env
sudoedit /etc/shadefeed/camera-monitor.env
```

Keep the real file outside the repository. Add exactly one assignment using
actual credentials entered locally, without `export`:

```text
RTSP_URL="rtsp://USER:PERCENT_ENCODED_PASSWORD@192.168.1.28:554/h264Preview_01_sub"
```

Replace USER and PERCENT_ENCODED_PASSWORD. Percent-encode each credential
component separately (for example `@` becomes `%40`, `#` becomes `%23`).
Do not encode the URL separators. Do not paste the real URL into shell history,
Git, screenshots or messages. systemd reads this root-only file before switching
to the configured user. The URL remains available to the running process and
FFmpeg arguments; this is not protection against privileged local inspection.

The environment file is mandatory: a missing file prevents service startup;
a missing/empty RTSP_URL causes an explicit configuration error.

```bash
sudo install -m 644 config/systemd/shadefeed-camera-monitor.service /etc/systemd/system/
sudo systemd-analyze verify /etc/systemd/system/shadefeed-camera-monitor.service
sudo systemctl daemon-reload
sudo systemctl enable shadefeed-camera-monitor.service
sudo systemctl restart shadefeed-camera-monitor.service
systemctl status shadefeed-camera-monitor.service --no-pager
sudo journalctl -u shadefeed-camera-monitor.service -n 20 --no-pager
```

Allow up to 25 seconds for a sample. Confirm `active (running)` **and**
`Network: ONLINE | Stream: OK`. A running service alone is not proof of video.
Do not run a second manual monitor alongside the service.

## Revalidation checklist — pending for the revised RTSP service

1. Verify a healthy sample, then a camera-network interruption and restoration.
   Confirm status transitions and continued monitoring.
2. Reboot with `sudo reboot`, reconnect and check service status and fresh logs
   without manually launching the script.
3. Simulate a monitor failure:

```bash
sudo systemctl kill --signal=SIGKILL --kill-whom=main shadefeed-camera-monitor.service
```

Wait about 40 seconds (10-second restart delay plus video sampling), then inspect
status and logs. Record restart counter, timestamps and fresh stream status.
4. Record results and software revision before claiming hardware validation.

`Restart=on-failure` handles process failure, not a reported stream failure.
Stop intentionally with `sudo systemctl stop shadefeed-camera-monitor.service`.
Start again with `sudo systemctl start shadefeed-camera-monitor.service`.
Long-duration reliability, log rotation and the 72-hour bench test remain pending.
