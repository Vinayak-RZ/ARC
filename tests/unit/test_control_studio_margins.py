"""Regression: margin crossover frequencies must not swap GM/PM vs dB."""

from __future__ import annotations

import pytest

from electrical_engineer.control_studio.margins import extract_margins
from electrical_engineer.engines.control_runner import control_available


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_open_loop_40_over_s_cubic_margins() -> None:
    import control

    sys = control.tf([40.0], [1.0, 12.0, 20.0, 0.0])
    m = extract_margins(sys)
    assert abs(m["phase_crossover_rad_s"] - 4.472135955) < 0.02
    assert abs(m["gain_margin_db"] - 15.563025) < 0.15
    assert abs(m["gain_crossover_rad_s"] - 1.5586864) < 0.03
    assert abs(m["phase_margin_deg"] - 43.209845) < 0.25
    assert abs(m["gain_margin_linear"] - 6.0) < 0.01
