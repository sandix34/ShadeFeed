"""Hardware-independent tests; run with python3 -m unittest discover -s tests -v."""
import os
import subprocess
import unittest
from unittest.mock import patch
from src.wildlife_station import camera_monitor as monitor


class CameraMonitorTests(unittest.TestCase):
    def setUp(self):
        # Isolate every test from real credentials and the caller's environment.
        self.env = patch.dict(os.environ, {"RTSP_URL": "rtsp://example.invalid/test"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_camera_online(self):
        # A successful connection reports network availability.
        with patch.object(monitor.socket, "create_connection") as connect:
            self.assertTrue(monitor.check_camera())
        connect.assert_called_once_with((monitor.CAMERA_HOST, 554), timeout=5)

    def test_camera_offline(self):
        # A refused connection is handled without crashing.
        with patch.object(monitor.socket, "create_connection", side_effect=ConnectionRefusedError):
            self.assertFalse(monitor.check_camera())

    def test_camera_timeout(self):
        # A network timeout is also a normal unavailable result.
        with patch.object(monitor.socket, "create_connection", side_effect=TimeoutError):
            self.assertFalse(monitor.check_camera())

    def test_stream_ok(self):
        # Success requires decoded frames and an explicit video stream mapping.
        with patch.object(monitor.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "frame=250\nprogress=end\n")
            self.assertTrue(monitor.check_rtsp_stream())
        run.assert_called_once()
        args, kwargs = run.call_args
        command = args[0]
        self.assertEqual(command[command.index("-map") + 1], "0:v:0")
        self.assertEqual(command[command.index("-progress") + 1], "pipe:1")
        self.assertEqual(kwargs["timeout"], 25)
        self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)

    def test_stream_failed(self):
        # Decoded frames do not override a failing FFmpeg exit status.
        with patch.object(monitor.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 1, "frame=5\n")
            self.assertFalse(monitor.check_rtsp_stream())
        run.assert_called_once()

    def test_stream_without_frames(self):
        # Exit code zero alone must never produce a healthy stream result.
        for output in ("", "frame=0\n", "frame=invalid\n", "progress=end\n"):
            with self.subTest(output=output), patch.object(monitor.subprocess, "run") as run:
                run.return_value = subprocess.CompletedProcess([], 0, output)
                self.assertFalse(monitor.check_rtsp_stream())
                run.assert_called_once()

    def test_stream_timeout(self):
        # Ensure the timeout path is actually reached, even without a real URL.
        with patch.object(monitor.subprocess, "run", side_effect=subprocess.TimeoutExpired("ffmpeg", 25)) as run:
            self.assertFalse(monitor.check_rtsp_stream())
        run.assert_called_once()

    def test_missing_ffmpeg(self):
        # A missing executable reports failure rather than crashing the loop.
        with patch.object(monitor.subprocess, "run", side_effect=FileNotFoundError) as run:
            self.assertFalse(monitor.check_rtsp_stream())
        run.assert_called_once()

    def test_missing_url(self):
        # No subprocess should run when configuration is missing.
        with patch.dict(os.environ, {}, clear=True), patch.object(monitor.subprocess, "run") as run:
            self.assertFalse(monitor.check_rtsp_stream())
        run.assert_not_called()

    def test_main_rejects_missing_url(self):
        # Startup explicitly distinguishes missing configuration from camera failure.
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(SystemExit, "RTSP_URL is missing"):
                monitor.main()

    def test_main_logs_transitions_only(self):
        # Repeated healthy observations are not appended; a network loss is.
        with patch.object(monitor, "check_camera", side_effect=[True, True, False]), \
             patch.object(monitor, "check_rtsp_stream", return_value=True) as stream, \
             patch.object(monitor.time, "sleep", side_effect=[None, None, KeyboardInterrupt]), \
             patch.object(monitor, "log_event") as log, patch("builtins.print"):
            monitor.main()
        self.assertEqual(stream.call_count, 2)
        self.assertEqual(log.call_count, 2)
        self.assertIn("Network: ONLINE | Stream: OK", log.call_args_list[0].args[0])
        self.assertIn("Network: OFFLINE | Stream: FAILED", log.call_args_list[1].args[0])


if __name__ == "__main__":
    unittest.main()
