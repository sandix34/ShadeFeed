# Umbra — 10-minute secondary-stream recording validation (2026-11-22)

## Scope
Local Raspberry Pi 5 recording test of the Reolink RLC-811A (Umbra) RTSP secondary stream, conducted during the Noctua / ShadeFeed test bench. This is a separate test from the 60-second **main 4K HEVC** recording documented in `umbra-4k-recording-validation-2026-11-22.md`.

## Observed evidence

| Check | Observation | Assessment |
| --- | --- | --- |
| RTSP capture | FFmpeg completed a 600-second stream-copy recording | Pass for this session |
| File | `~/shadefeed-tests/umbra-4k-10min-20261122-164408.mkv` | Exists; filename says 4K but content is not 4K |
| Probed duration | 600.600000 seconds | Pass |
| File size | 19,723,647 bytes | Recorded |
| Video codec | H.264 | Secondary stream |
| Resolution | 640 × 360 | Secondary stream, not main 4K |
| Full decode | FFmpeg command reported `Full video decode: OK` | Pass |
| Video packets checked for DTS | 6,001 | Analyzed |
| Non-increasing DTS | 1, at packet 55 (5.320000 s repeated) | Open issue |
| Largest consecutive PTS gap | 0.179 s | Measured |
| PTS gaps greater than 0.200 s | 0 | Pass against this threshold |
| FFmpeg warnings | `Timestamps are unset`, `Non-monotonous DTS`, and repeated null-muxer warnings | Investigate |

## Interpretation
The 10-minute secondary H.264 stream was successfully saved and decoded. The file name is misleading: the probed video is 640 × 360, not 3840 × 2160. One repeated packet DTS was detected in the saved MKV. A successful decode and absence of PTS gaps above 200 ms do not establish perfect frame continuity, correct timestamps, or unattended reliability. The repeated warnings emitted while decoding to the null muxer must be distinguished from the single DTS anomaly measured in the original file.

## Main-stream test status
A separate 60-second **main 4K HEVC** recording was previously validated; see the linked 4K report. A 10-minute main-stream recording has **not** been validated by this test.

An attempt to derive a main-stream RTSP URL from the root-only `RTSP_URL` environment variable failed with `No such file or directory`. The environment variable was subsequently confirmed loaded, but the diagnostic endpoint extraction printed an empty string. This does not invalidate the working secondary-stream capture. No change to the working camera-monitor configuration was made as part of this investigation.

## Next controlled steps
- [ ] Inspect the local `RTSP_URL` structure without disclosing credentials, and construct the main-stream URL safely; do not overwrite the working monitor configuration.
- [ ] Record and probe 10 minutes of the actual main 4K HEVC stream; verify codec, dimensions, duration, size, DTS/PTS and full decode.
- [ ] Investigate the repeated DTS at packet 55 and distinguish capture timestamps from FFmpeg null-muxer warnings.
- [ ] Perform longer-duration, reboot, storage-recovery and power/temperature tests before claiming unattended reliability.

## Evidence handling
This document is based on operator terminal screenshots. Keep video files, authenticated URLs, passwords, environment files and sensitive field locations out of the public repository. Do not publish raw diagnostic output containing credentials.

**Outcome:** 10-minute secondary-stream capture accepted with timestamp anomaly; 10-minute main-stream validation remains pending.
