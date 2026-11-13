"""Margin tooltip copy matches crossover facts."""

from __future__ import annotations

import pytest

from electrical_engineer.control_studio.compose import open_loop_with_controller
from electrical_engineer.control_studio.goldens import pid_dc_motor
from electrical_engineer.control_studio.layout import layout_chain
from electrical_engineer.control_studio.margins import _gain_band_note_from_db, extract_margins
from electrical_engineer.engines.control_runner import control_available


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_infinite_gain_margin_explains_phase() -> None:
    diagram = layout_chain(pid_dc_motor())
    m = extract_margins(open_loop_with_controller(diagram)[0])
    assert m["display"]["gm_db"] == "Infinite"
    tip = m["margin_tooltips"]["gm_db"] or ""
    assert "−180" in tip or "-180" in tip
    assert "above 0 dB" not in tip


def test_gain_crossover_note_below_db() -> None:
    note = _gain_band_note_from_db(-20.0, -15.0)
    assert "below 0 dB" in note
