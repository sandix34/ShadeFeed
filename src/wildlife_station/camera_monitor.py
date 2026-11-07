
"""Network availability and sampled RTSP video checks for Umbra."""

import os
import socket
import subprocess
import time
from datetime import datetime
from pathlib import Path

CAMERA_HOST = "192.168.1.28"
CAMERA_PORT = 554
TIMEOUT_SECONDS = 5


def check_camera():
    """Check whether the camera's RTSP port is reachable."""
    try:
        with socket.create_connection(
            (CAMERA_HOST, CAMERA_PORT),
            timeout=TIMEOUT_SECONDS,
        ):
            return True
    except OSError:
        return False

def check_rtsp_stream():
    """Request a 10-second sample; require successful decoding of video frames."""
    rtsp_url = os.environ.get("RTSP_URL")
    if not rtsp_url:
        return False

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-nostdin",
                "-nostats",
                "-progress", "pipe:1",
                "-rtsp_transport", "tcp",
                "-i", rtsp_url,
                "-map", "0:v:0",
                "-t", "10",
                "-an",
                "-f", "null",
                "-"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=25,
            check=False,
        )
        frames = []
        for line in result.stdout.splitlines():
            key, _, value = line.partition("=")
            if key == "frame":
                try:
                    frames.append(int(value.strip()))
                except ValueError:
                    pass
        return result.returncode == 0 and any(count > 0 for count in frames)
    except (subprocess.TimeoutExpired, OSError):
        return False

LOG_FILE = Path("logs/camera_monitor.log")


def log_event(message):
    """Save a timestamped event to the monitoring log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as log:
        log.write(message + "\n")

def main():
    if not os.environ.get("RTSP_URL"):
        raise SystemExit("ShadeFeed | Configuration error: RTSP_URL is missing")
    print("ShadeFeed | Camera monitoring started")
    previous_status = None

    try:
        while True:
            timestamp = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )

            network_ok = check_camera()

            if network_ok:
                stream_ok = check_rtsp_stream()
            else:
                stream_ok = False

            network_status = "ONLINE" if network_ok else "OFFLINE"
            stream_status = "OK" if stream_ok else "FAILED"

            status = (network_status, stream_status)

            message = (
                f"{timestamp} | Umbra | "
                f"Network: {network_status} | Stream: {stream_status}"
            )
            print(message, flush=True)

            if status != previous_status:
                log_event(message)
                previous_status = status

            time.sleep(30)

    except KeyboardInterrupt:
        print("\nShadeFeed | Camera monitoring stopped")


if __name__ == "__main__":
    main()
