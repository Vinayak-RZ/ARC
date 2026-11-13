"""Advisory text helpers."""

from __future__ import annotations

import re

from electrical_engineer.traps.text_advisory import find_advisory


def test_agc_dip_negation() -> None:
    pat = re.compile(r"remove.{0,12}first\s+dip", re.IGNORECASE)
    assert find_advisory("Note: AGC does not remove the first dip.", pat) is None
