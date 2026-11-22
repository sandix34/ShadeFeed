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
