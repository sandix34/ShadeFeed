
"""Basic network availability check for Umbra."""

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
    """Check whether FFmpeg can decode 10 seconds of video."""
    import os

    rtsp_url = os.environ.get("RTSP_URL")
    if not rtsp_url:
        return False

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-rtsp_transport", "tcp",
                "-i", rtsp_url,
                "-t", "10",
                "-an",
                "-f", "null",
                "-"
            ],
            capture_output=True,
            timeout=25,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False

LOG_FILE = Path("logs/camera_monitor.log")


def log_event(message):
    """Save a timestamped event to the monitoring log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as log:
        log.write(message + "\n")

def main():
    print("Noctua | Camera monitoring started")
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
        print("\nNoctua | Camera monitoring stopped")


if __name__ == "__main__":
    main()
