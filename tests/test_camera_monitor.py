from unittest.mock import patch
from src.wildlife_station.camera_monitor import check_camera, check_rtsp_stream

# TEST 1 — Camera online
# Simulates a successful network connection to the camera.
# Verifies that check_camera() returns True.
# Ensures that the connection is attempted exactly once.
def test_camera_online():
    with patch(
        "src.wildlife_station.camera_monitor.socket.create_connection"
    ) as mock_connection:
        result = check_camera()

    assert result is True
    mock_connection.assert_called_once()

# TEST 2 — Camera offline
# Simulates a refused network connection.
# Verifies that check_camera() returns False.
# Ensures that the connection error is handled gracefully.
def test_camera_offline():
    with patch(
        "src.wildlife_station.camera_monitor.socket.create_connection",
        side_effect=ConnectionRefusedError
    ):
        result = check_camera()

    assert result is False

# TEST 3 — RTSP stream available
# Simulates a successful FFmpeg execution (exit code 0).
# Verifies that check_rtsp_stream() returns True.
# Ensures that FFmpeg is called exactly once.
def test_rtsp_stream_ok():
    with patch(
        "src.wildlife_station.camera_monitor.subprocess.run"
    ) as mock_run:
        mock_run.return_value.returncode = 0
        result = check_rtsp_stream()

    assert result is True
    mock_run.assert_called_once()

# TEST 4 — RTSP stream failure
# Simulates an FFmpeg failure (exit code 1).
# Verifies that check_rtsp_stream() returns False.
# Ensures that a stream failure is correctly detected.    
def test_rtsp_stream_failed():
    with patch(
        "src.wildlife_station.camera_monitor.subprocess.run"
    ) as mock_run:
        mock_run.return_value.returncode = 1
        result = check_rtsp_stream()

    assert result is False
    mock_run.assert_called_once()


# TEST 5 — RTSP stream timeout
# Simulates an FFmpeg process exceeding its timeout.
# Verifies that the TimeoutExpired exception is handled.
# Ensures that the function returns False without crashing.
import subprocess

def test_rtsp_stream_timeout():
    with patch(
        "src.wildlife_station.camera_monitor.subprocess.run",
        side_effect=subprocess.TimeoutExpired(
            cmd="ffmpeg", timeout=25
        )
    ):
        result = check_rtsp_stream()

    assert result is False

# TEST 6 — Network connection timeout
# Simulates a camera that does not respond within the timeout.
# Verifies that the TimeoutError exception is handled.
# Ensures that the function returns False without crashing.
def test_camera_network_timeout():
    with patch(
        "src.wildlife_station.camera_monitor.socket.create_connection",
        side_effect=TimeoutError
    ):
        result = check_camera()

    assert result is False