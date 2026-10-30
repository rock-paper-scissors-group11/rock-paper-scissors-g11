"""Hand Pointer - use the index fingertip like a mouse, click by waiting.

Move your index fingertip over a button and KEEP it there for DWELL_SECONDS
seconds. A progress bar fills on the button. When it is full = click.

This file does NOT draw anything and does NOT open the camera.
"""
import math
import time

from src import config
from src.config import DWELL_EDGE_TOLERANCE_PX, DWELL_GRACE_SECONDS, DWELL_SECONDS

INDEX_TIP = 8


def index_tip_normalized(landmarks, frame_width, frame_height):
    """Return the fingertip as (x, y) between 0 and 1, or None if no hand.

    Works if the tracker gives 0-1 values OR pixel values.
    """
    if landmarks is None or len(landmarks) != 21:
        return None
    x, y = landmarks[INDEX_TIP][0], landmarks[INDEX_TIP][1]
    if x > 1.5 or y > 1.5:                      # pixels -> 0..1
        x, y = x / frame_width, y / frame_height
    return (min(max(x, 0.0), 1.0), min(max(y, 0.0), 1.0))


class Pointer:
    """Turns the fingertip into an adaptive, smooth cursor."""

    def __init__(self, width, height, margin=0.12, smoothing=None) -> None:
        self.width = width
        self.height = height
        self.margin = margin          # the camera edges are hard to reach
        self.smoothing = smoothing    # Optional legacy exponential smoothing.
        self._pos = None
        self._filtered = None
        self._raw_previous = None
        self._derivative = (0.0, 0.0)
        self._filter_time = None
        self._last_seen = None

    @staticmethod
    def _alpha(cutoff, dt):
        tau = 1.0 / (2.0 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

    def _filter(self, normalized, now):
        if self.smoothing is not None:
            return normalized

        if self._filtered is None or self._filter_time is None:
            self._filtered = normalized
            self._raw_previous = normalized
            self._derivative = (0.0, 0.0)
            self._filter_time = now
            return self._filtered

        dt = now - self._filter_time
        if dt <= 0.0:
            return self._filtered

        filtered = []
        derivatives = []
        for value, raw_previous, previous, previous_derivative in zip(
                normalized, self._raw_previous, self._filtered, self._derivative):
            derivative = (value - raw_previous) / dt
            derivative_alpha = self._alpha(config.POINTER_D_CUTOFF, dt)
            filtered_derivative = (
                derivative_alpha * derivative
                + (1.0 - derivative_alpha) * previous_derivative
            )
            cutoff = (
                config.POINTER_MIN_CUTOFF
                + config.POINTER_BETA * abs(filtered_derivative)
            )
            value_alpha = self._alpha(cutoff, dt)
            filtered.append(
                value_alpha * value + (1.0 - value_alpha) * previous
            )
            derivatives.append(filtered_derivative)

        self._filtered = tuple(filtered)
        self._raw_previous = normalized
        self._derivative = tuple(derivatives)
        self._filter_time = now
        return self._filtered

    def _reset_filter(self):
        self._filtered = None
        self._raw_previous = None
        self._derivative = (0.0, 0.0)
        self._filter_time = None

    def update(self, normalized, now=None):
        """Give (x, y) from index_tip_normalized (or None). Get screen (x, y)."""
        if now is None:
            now = time.monotonic()
        if normalized is None:
            if self._last_seen is not None:
                if now - self._last_seen <= config.POINTER_HOLD_SECONDS:
                    return self._pos
                self._pos = None
                self._last_seen = None
                self._reset_filter()
            return None

        if (self._last_seen is not None
                and now - self._last_seen > config.POINTER_HOLD_SECONDS):
            self._reset_filter()
            self._pos = None

        self._last_seen = now
        filtered_x, filtered_y = self._filter(normalized, now)
        span = 1.0 - 2 * self.margin
        nx = min(max((filtered_x - self.margin) / span, 0.0), 1.0)
        ny = min(max((filtered_y - self.margin) / span, 0.0), 1.0)
        target = (nx * self.width, ny * self.height)
        if self._pos is None:
            self._pos = target
        elif self.smoothing is not None:
            self._pos = (self._pos[0] + self.smoothing * (target[0] - self._pos[0]),
                         self._pos[1] + self.smoothing * (target[1] - self._pos[1]))
        else:
            self._pos = target
        return self._pos


class Button:
    def __init__(self, name, label, x, y, w, h) -> None:
        self.name = name        # what the program uses, e.g. "START"
        self.label = label      # what the player reads
        self.x, self.y, self.w, self.h = x, y, w, h

    def contains(self, point) -> bool:
        return (point is not None
                and self.x <= point[0] <= self.x + self.w
                and self.y <= point[1] <= self.y + self.h)


class DwellClicker:
    """Counts how long the cursor stays on one button."""

    def __init__(self, dwell_seconds: float = DWELL_SECONDS) -> None:
        self.dwell = dwell_seconds
        self._target = None       # button name being held now
        self._start = 0.0
        self._locked = None       # just clicked: leave the button before again
        self._outside_since = None

    @staticmethod
    def _button(buttons, name):
        return next((button for button in buttons if button.name == name), None)

    @staticmethod
    def _within_tolerance(point, button):
        if point is None or button is None:
            return False
        dx = max(button.x - point[0], 0, point[0] - (button.x + button.w))
        dy = max(button.y - point[1], 0, point[1] - (button.y + button.h))
        return dx * dx + dy * dy <= DWELL_EDGE_TOLERANCE_PX ** 2

    def update(self, point, buttons, now):
        """Call once per frame. Returns the clicked button's name, or None."""
        hit = None
        for button in buttons:
            if button.contains(point):
                hit = button.name
                break

        if self._locked is not None and hit == self._locked:
            if self._outside_since is None:
                return None
            if now - self._outside_since <= DWELL_GRACE_SECONDS:
                self._outside_since = None
                return None
            self._outside_since = None
            self._locked = None
        elif self._locked is not None:
            locked_button = self._button(buttons, self._locked)
            if self._within_tolerance(point, locked_button):
                if self._outside_since is None:
                    self._outside_since = now
                if now - self._outside_since <= DWELL_GRACE_SECONDS:
                    return None
            self._outside_since = None
            self._locked = None

        if self._target is not None:
            if hit == self._target:
                if (self._outside_since is not None
                        and now - self._outside_since > DWELL_GRACE_SECONDS):
                    self._target = None
                self._outside_since = None
            else:
                target_button = self._button(buttons, self._target)
                if self._within_tolerance(point, target_button):
                    if self._outside_since is None:
                        self._outside_since = now
                    if now - self._outside_since <= DWELL_GRACE_SECONDS:
                        if now - self._start >= self.dwell:
                            self._locked = self._target
                            clicked = self._target
                            self._target = None
                            self._outside_since = None
                            return clicked
                        return None
                self._target = None
                self._outside_since = None

        if hit is None or hit == self._locked:
            return None

        if hit != self._target:
            self._target = hit
            self._start = now
        self._outside_since = None
        if now - self._start >= self.dwell:
            self._locked = hit
            self._target = None
            self._outside_since = None
            return hit
        return None

    def progress(self, button_name, now) -> float:
        """0.0 to 1.0 for the progress bar of one button."""
        if button_name != self._target:
            return 0.0
        return min(1.0, (now - self._start) / self.dwell)