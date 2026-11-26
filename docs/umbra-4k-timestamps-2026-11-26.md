# Umbra 4K recording timestamps — 26 November 2026

## Decision and scope

Keep the current RTSP-over-TCP video stream copy into Matroska (MKV) and keep FFmpeg warnings visible. Both traced recordings decoded to completion on the Raspberry Pi 5. Preserve both frames when timestamps coincide. A repeated timestamp alone is insufficient evidence for deleting a frame.

The bench used the Reolink RLC-811A main 3840 × 2160 HEVC stream and FFmpeg 7.1.5-0+deb13u1+rpt2. The MKV video track used a 1/1000 time base (one millisecond per tick). PTS indicates when to present an image. DTS sets its decoding time. Both refer to the media timeline.

## Reproducing the earlier warning

The [22 November report](umbra-4k-recording-validation-2026-11-22.md) describes a one-minute clip and a separate ten-minute capture. The old ten-minute file was absent from its temporary path. Today's ten-minute result comes from a fresh capture.

Decoding the saved one-minute clip to FFmpeg's null output produced 28 log lines, including equal-DTS warnings, with exit status 0. Repeating the decode with only the output encoder time base changed to `-enc_time_base:v 1:1000` produced an empty warning log and exit status 0. Copying the saved video stream to another MKV also completed with an empty warning log. The time-base option was used only for this diagnostic decode.

A fresh one-minute capture lasted 60.021 s and contained 1,501 video packets. The Matroska writer warned of an unset packet timestamp. On readback every packet had a PTS and DTS. Two pairs shared both values, at 30.153 s and 52.088 s.

## Traced captures

| Measurement | Two-minute capture | Ten-minute capture |
| --- | ---: | ---: |
| Packets presented to the writer | 3,002 | 14,999 |
| Packets read from MKV | 3,002 | 14,999 |
| Decoded frames | 3,002 | 14,999 |
| Missing PTS at writer input | First packet only | First packet only |
| Missing DTS at writer input | 0 | 0 |
| DTS equal to previous DTS at writer input | 3 | 0 |
| DTS moving backwards at writer input | 0 | 0 |
| Full frame-count exit status | 0 | 0 |

The ten-minute file measured 600.007 s and 462,558,340 bytes. The two-minute trace showed the first packet reaching the writer with PTS unset and DTS zero. Reading that file back gave PTS zero and DTS zero for its first packet. Reading the finished file alone would have missed the startup condition.

### Why three pairs shared a timestamp

The following adjusted input DTS values were distinct before conversion. Each pair rounded to the same millisecond at the writer and retained that value on MKV readback. Packet numbers start at one.

| Packet pair | Adjusted input DTS (s) | Separation | MKV DTS (s) |
| --- | --- | ---: | ---: |
| 854–855 | 34.050700 and 34.051378 | 0.678 ms | 34.051 |
| 1,403–1,404 | 56.062578 and 56.063422 | 0.844 ms | 56.063 |
| 2,703–2,704 | 108.042589 and 108.043378 | 0.789 ms | 108.043 |

SHA-256 hashes of the decoded pixels differed within each pair. All six images were present, and each pair contained two distinct images. Rounding explains these three equalities. The cause of the close spacing upstream remains open. These measurements cover the saved clips. They do not establish sensor-to-file completeness or unattended endurance.

## Repeating the check on the bench

With the authenticated main-stream URL already prepared locally in `RTSP_MAIN`, use a fresh output path under the operator's home directory. Keep the raw debug log local because it can contain connection details.

```bash
trace10="$HOME/shadefeed-tests/rtsp-10min-$(date +%Y%m%d-%H%M%S)"
timeout 660s ffmpeg -n -hide_banner -nostats -loglevel verbose -debug_ts \
  -rtsp_transport tcp -i "$RTSP_MAIN" -map 0:v:0 -t 600 \
  -c:v copy "${trace10}.mkv" 2>"${trace10}.log"
```

After a successful capture, count decoded frames and packets independently and read the duration and file size.

```bash
ffprobe -v error -select_streams v:0 -count_frames -count_packets \
  -show_entries stream=time_base,nb_read_frames,nb_read_packets:format=duration,size \
  -of default=noprint_wrappers=1 "${trace10}.mkv"
```

For trace analysis on this build, inspect `pkt_dts` on video `demuxer ->` lines, `pkt_dts_time` on `demuxer+ffmpeg ->` lines and `pts` / `dts` on `muxer <-` lines. Compare consecutive numeric DTS values within each stage. Count missing timestamps separately. Check packet positions against `ffprobe -show_packets` and compare decoded frame hashes if equal timestamps need investigation.

## Next bench test

Trigger a short 4K event clip manually while an object enters and leaves the scene. Review the first and last useful frames and check that the file closes and decodes. Monitor whether an unset PTS remains confined to startup. Repeat with automatic detection later to measure trigger delay and decide how much footage to retain before and after each event.
