from src.config import DWELL_EDGE_TOLERANCE_PX, DWELL_GRACE_SECONDS, DWELL_SECONDS
from src.hand_pointer import Button, DwellClicker


BUTTON = Button("START", "START", 100, 100, 200, 80)
BUTTONS = [BUTTON]


def test_edge_jitter_within_tolerance_and_grace_keeps_dwell():
    clicker = DwellClicker(DWELL_SECONDS)
    clicker.update((110, 120), BUTTONS, 0.0)

    assert clicker.update(
        (100 - DWELL_EDGE_TOLERANCE_PX, 120), BUTTONS, 0.1,
    ) is None
    assert clicker.update((110, 120), BUTTONS, 0.2) is None
    assert clicker.progress("START", 0.2) == 0.2
    assert clicker.update((110, 120), BUTTONS, 1.0) == "START"


def test_leaving_beyond_tolerance_resets_dwell():
    clicker = DwellClicker(DWELL_SECONDS)
    clicker.update((110, 120), BUTTONS, 0.0)

    clicker.update(
        (100 - DWELL_EDGE_TOLERANCE_PX - 1, 120), BUTTONS, 0.1,
    )
    assert clicker.progress("START", 0.1) == 0.0
    assert clicker.update((110, 120), BUTTONS, 0.2) is None
    assert clicker.update((110, 120), BUTTONS, 1.19) is None
    assert clicker.update((110, 120), BUTTONS, 1.2) == "START"


def test_edge_outside_longer_than_grace_resets_dwell():
    clicker = DwellClicker(DWELL_SECONDS)
    clicker.update((110, 120), BUTTONS, 0.0)

    clicker.update((100 - 5, 120), BUTTONS, 0.1)
    clicker.update((100 - 5, 120), BUTTONS, 0.1 + DWELL_GRACE_SECONDS + 0.01)

    assert clicker.progress("START", 0.1 + DWELL_GRACE_SECONDS + 0.01) == 0.0


def test_click_still_requires_full_dwell_seconds():
    clicker = DwellClicker(DWELL_SECONDS)
    assert clicker.update((110, 120), BUTTONS, 0.0) is None
    assert clicker.update((110, 120), BUTTONS, DWELL_SECONDS - 0.001) is None
    assert clicker.update((110, 120), BUTTONS, DWELL_SECONDS) == "START"
