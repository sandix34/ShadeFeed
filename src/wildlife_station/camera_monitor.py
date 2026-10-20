
"""Basic network availability check for Umbra."""

import socket
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

            if check_camera():
                status = "ONLINE"
            else:
                status = "OFFLINE"

            message = f"{timestamp} | Umbra | {status}"
            print(message, flush=True)

            if status != previous_status:
                log_event(message)
                previous_status = status

            time.sleep(30)

    except KeyboardInterrupt:
        print("\nNoctua | Camera monitoring stopped")


if __name__ == "__main__":
    main()
