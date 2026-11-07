# Configuration

`systemd/shadefeed-camera-monitor.service` is the version-controlled service
for the ShadeFeed bench. It uses the local user and repository path documented
in the [installation guide](../docs/camera-monitor-systemd.md).

The mandatory `/etc/shadefeed/camera-monitor.env` supplies RTSP_URL. Keep it
root-owned, mode 0600, outside Git. This file is read by systemd, not automatically
by Python during a manual run. Shell exports do not configure the system service.

No real credentials, authenticated URLs or field coordinates belong here.
The bench IP and timing are still constants in camera_monitor.py.
