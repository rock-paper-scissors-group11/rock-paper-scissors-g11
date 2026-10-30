"""Camera Manager - opens the webcam and gives frames. (Phase 2)"""
"""Camera Manager - opens the webcam and gives frames.

It never crashes: if the camera is missing or disconnected, read() simply
returns None and the game can show a friendly message.
"""
import sys

import cv2

from src import config


class Camera:
    def __init__(self, index: int = config.CAMERA_INDEX):
        self.index = index
        self.cap = None

    def open(self) -> bool:
        """Try to open the webcam. Returns True if it works."""
        try:
            # On Windows, CAP_DSHOW opens the camera much faster.
            if sys.platform.startswith("win"):
                self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(self.index)

            if not self.cap.isOpened():
                self.cap = None
                return False

            settings = (
                (cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH),
                (cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT),
                (cv2.CAP_PROP_BUFFERSIZE, 1),
                (cv2.CAP_PROP_FPS, 30),
            )
            for property_id, value in settings:
                try:
                    self.cap.set(property_id, value)
                except Exception:
                    pass
            try:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            except Exception:
                pass
            return True
        except Exception as error:  # never crash because of the camera
            print(f"[Camera] Could not open camera: {error}")
            self.cap = None
            return False

    def is_opened(self) -> bool:
        return self.cap is not None and self.cap.isOpened()

    def read(self):
        """Return one frame (BGR image), or None if the camera failed."""
        if not self.is_opened():
            return None
        try:
            success, frame = self.cap.read()
        except Exception:
            return None
        if not success:
            return None
        if config.MIRROR_VIEW:
            frame = cv2.flip(frame, 1)  # flip like a mirror
        return frame

    def release(self) -> None:
        """Always call this before exiting, so other apps can use the camera."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    # Allows:  with Camera() as cam: ...
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()
