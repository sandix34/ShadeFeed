# Tests

This directory is reserved for automated tests of the Noctua software.

**Current status:** No automated test suite is published here yet. The RTSP and performance measurements in the documentation were **manual test-bench experiments**.

Future tests should distinguish:
- Unit tests that run without hardware
- Integration tests that require a Raspberry Pi or camera
- Long-running endurance tests with explicit start/end times and measurements

Do not place credentials, sensitive coordinates or raw wildlife recordings in test fixtures.

See [Umbra's documented manual tests](../docs/umbra-installation-rtsp-performance.md).
