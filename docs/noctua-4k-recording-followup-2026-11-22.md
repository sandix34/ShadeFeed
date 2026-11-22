# Noctua — Additional 4K RTSP recording check (2026-11-22)

## Scope

Additional, separate 60-second Raspberry Pi recording test of the Reolink RLC-811A main RTSP stream. Evidence is based on operator terminal screenshots. This is **not** the previously documented `umbra-4k-20261122-160926.mkv` test; do not combine their sizes or observations.

## Capture

- Local output: `/tmp/noctua-test/reolink-4k-60s.mkv` (not committed).
- Source: authenticated RTSP URL loaded from a local root-controlled environment file; substream endpoint replaced with the main HEVC endpoint.
- Command approach: `ffmpeg -rtsp_transport tcp -i "$main_url" -t 60 -map 0:v:0 -c:v copy -an ...` (stream copy, no video re-encoding).
- Video: HEVC/H.265, 3840 × 2160, reported 25 fps.
- Audio intentionally excluded from the output.

## Observed results

| Check | Observation | Assessment |
| --- | --- | --- |
| MKV duration (ffprobe) | Approximately 60.039 s | Pass for short capture |
| MKV size (ffprobe) | 52,168,928 bytes | Recorded |
| Frame count during recording | 1,501 frames shown by FFmpeg | Recorded |
| Decoded frame count (ffprobe -count_frames) | `nb_read_frames=1501` | Pass |
| Full decode to null (ffmpeg) | Process completed with exit code 0 | Pass with warnings |
| Timestamp behavior | Repeated `Application provided invalid, non monotonically increasing dts to muxer` during decode-to-null | Open |

The decode-to-null warning does **not**, by itself, prove that source-file DTS values are out of order: the null output muxer can emit these warnings while receiving decoded frames. Packet-level DTS/PTS inspection of **this specific file** has not yet been recorded. The earlier separate 60-second MKV had 1,501 packets, zero non-increasing DTS and a 0.088 s maximum PTS gap; those results must not be attributed to this file.

## Conclusion

Short-duration 4K stream-copy capture and full frame decoding succeeded. Temporal integrity, missing/duplicated frame analysis, unattended stability, file rotation and power/endurance performance remain **unvalidated**. No claim of 72-hour readiness.

## Next controlled checks

1. Inspect source MKV packet DTS/PTS ordering and gaps, separately from output-muxer warnings.
2. Check available disk space and record a controlled 10-minute 4K sample.
3. Validate recording duration, frame count, packet timing, and decoding of that sample.
4. Later test service supervision, interruption recovery, disk management, day/night operation, power and temperature.

## Security

Never commit recordings, camera credentials, authenticated RTSP URLs, local environment files, or sensitive wildlife site coordinates. Rotate any credentials that were exposed in shared screenshots before deployment.
