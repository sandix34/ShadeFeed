# Automated tests

Run from the repository root with Python 3:

```bash
python3 -m unittest discover -s tests -v
```

No pytest installation, FFmpeg binary, camera, network access or real credentials
are required. The tests use the standard-library unittest runner and mocks.
Each test supplies an isolated fictitious RTSP_URL, or explicitly removes it.

Eleven test methods cover network success/refusal/timeout, decoded video frames,
FFmpeg failure, absent/zero/malformed frame counts, subprocess timeout, missing
FFmpeg, missing URL, explicit startup failure, and transition-only logging.
The success test also checks video selection, timeout and suppression of stderr.

These tests validate application logic, not real FFmpeg or camera behavior.
See [deployment and hardware validation](../docs/camera-monitor-systemd.md).
The original six pytest-style tests were replaced after the 7 November audit
found two failures and a false-positive timeout test when RTSP_URL was absent.
Never use real secrets or wildlife coordinates in fixtures.
