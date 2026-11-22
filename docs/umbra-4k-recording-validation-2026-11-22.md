# Umbra — 4K recording validation (2026-11-22)

## Scope

A local Raspberry Pi 5 test of the Reolink RLC-811A (Umbra) main RTSP video stream. This record distinguishes terminal evidence from the operator's visual inspection. It does not establish unattended recording reliability.

## Test evidence

| Check | Observation | Status |
| --- | --- | --- |
| Recording duration | 60-second recording; probed duration 60.040000 s | Pass |
| Video codec | HEVC / H.265 | Pass |
| Frame dimensions | 3840 × 2160 | Pass |
| Recorded file size | 73,024,818 bytes | Pass |
| Complete video decode | FFmpeg completed and printed `Full video decode: OK` | Pass |
| Playback on operator's computer | Operator watched the complete recording and reported no visible freezes, stutters or image degradation | Pass (subjective) |
| Packet timestamp integrity | Repeated `Application provided invalid, non monotonically increasing dts to muxer` warnings during full decode to null output | Open investigation |

The local recording was named `umbra-4k-20261122-160926.mkv` and stored under `~/shadefeed-tests/` on the Raspberry Pi. The recording itself is **not** tracked in Git.

## Interpretation

The station successfully captured a short 4K HEVC clip that decoded completely and played normally in a manual visual review. Non-monotonic DTS warnings still require investigation; successful playback does not prove correct timestamp ordering, frame continuity, or reliable multi-day recording. The warning appeared while remuxing decoded output to FFmpeg's null muxer and should not be treated as proof that the original MKV file is corrupt.

## Follow-up checks

- [ ] Inspect packet/frame timestamps in the original MKV and distinguish source timing from FFmpeg output-muxer warnings.
- [ ] Check for dropped/duplicated frames and audio/video synchronization if audio is used.
- [ ] Repeat recordings over longer intervals, including day/night transitions.
- [ ] Validate file rotation, disk-space management, interrupted writes and recovery.
- [ ] Revalidate deployed RTSP monitoring, reboot behavior and failure recovery on hardware.
- [ ] Measure power consumption and temperatures before the 72-hour endurance test.

## Security and evidence retention

Keep recordings, local environment files, passwords, authenticated RTSP URLs and site coordinates outside the public repository. The operator's terminal screenshots and playback report are the source for this entry; no automated frame-integrity audit or extended endurance test was performed.

**Outcome:** 60-second recording and manual playback accepted; timestamp investigation remains open.

## Additional packet timestamp checks (2026-11-22)

The operator ran `ffprobe` on the saved MKV, selecting video stream `v:0`, and checked all packet DTS values with an AWK comparison against the preceding packet. A separate check measured consecutive PTS differences.

| Metric | Observed result |
| --- | ---: |
| Video packets with DTS analyzed | 1,501 |
| Non-increasing DTS values | 0 |
| Largest consecutive PTS interval | 0.088 s |
| Consecutive PTS intervals above 0.100 s | 0 |

**Interpretation:** No non-increasing packet DTS values or PTS gaps above the selected 100 ms threshold were detected in this 60-second MKV. These checks do not independently prove absence of dropped frames or explain the earlier FFmpeg null-muxer warnings. Keep the timestamp investigation open pending reproduction and packet/frame-level review.

**Next controlled test:** Capture 10 minutes of the main 4K stream, inspect duration, size, DTS/PTS continuity and full decode, and retain the recording outside Git. Check free disk space before capture. Longer tests and unattended operation remain unvalidated.

## Ten-minute RTSP recording follow-up (2026-11-22)

The operator recorded the main 4K HEVC stream using FFmpeg stream copy on the Raspberry Pi, saving a local test artifact at `/tmp/noctua-test/reolink-4k-10min.mkv`. The authenticated RTSP URL and credentials are intentionally omitted.

| Check | Observed result |
| --- | --- |
| Video | HEVC / H.265, 3840 × 2160, nominal 25 fps |
| Probed file duration | 600.038 s |
| Probed file size | 684,599,304 bytes (~653 MiB) |
| Complete frame count using `ffprobe -count_frames` | 15,003 decoded/read video frames |
| Approximate expected count at 25 fps for exactly 600 s | 15,000 (reference only) |
| FFmpeg stream-copy test | Exit code 0; repeated non-monotonically increasing DTS warnings from the Matroska muxer |
| Remux to null | Exit code 0; repeated non-monotonically increasing DTS warnings |
| Longer-term integrity | Not established |

The frame count is consistent with approximately ten minutes at 25 fps, but it is **not** evidence of correct packet DTS/PTS ordering, absence of dropped or duplicated frames, or stable long-term operation. An additional `ffprobe` inspection of individual frame timestamps was proposed but not completed before the session ended. The 60-second file's prior DTS results must not be conflated with this separate ten-minute recording.

**Open issue:** Determine whether the warnings originate from source packet timestamps, FFmpeg timestamp handling or muxer behavior. Next session: inspect original video packet DTS/PTS and frame presentation timestamps separately; preserve the original file, capture FFmpeg/version and command details, and compare controlled remux methods before changing the recording pipeline. Avoid assuming a fix from a successful exit status alone.

**Session stop point:** Investigation deliberately paused on 22 November 2026. No timestamp correction was validated and the 10-minute recording is not accepted as fully qualified evidence for unattended operation. Keep video files and credentials outside Git.
