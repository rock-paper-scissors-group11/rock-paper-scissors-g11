"""Tests for camera read failures."""
from src.camera import Camera


class RaisingCapture:
    def isOpened(self):
        return True

    def read(self):
        raise RuntimeError("camera backend failed")


def test_read_returns_none_when_capture_raises():
    camera = Camera()
    camera.cap = RaisingCapture()

    assert camera.read() is None


def test_open_succeeds_when_capture_has_no_set_method(monkeypatch):
    class OpenCapture:
        def isOpened(self):
            return True

    monkeypatch.setattr("src.camera.cv2.VideoCapture", lambda *args: OpenCapture())

    camera = Camera()

    assert camera.open() is True
