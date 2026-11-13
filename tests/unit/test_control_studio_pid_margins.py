"""PID · DC motor open-loop margins match python-control."""

from __future__ import annotations

import math

import pytest

from electrical_engineer.control_studio.compose import open_loop_with_controller
from electrical_engineer.control_studio.goldens import pid_dc_motor
from electrical_engineer.control_studio.margins import extract_margins
from electrical_engineer.engines.control_runner import control_available


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_pid_dc_motor_margins_match_stability_margins() -> None:
    import control

    diagram = pid_dc_motor()
    ol, _ = open_loop_with_controller(diagram)
    ref = control.stability_margins(ol)
    gm_lin, pm_deg, _sm, wpc, wgc, _wst = ref
    got = extract_margins(ol)

    if gm_lin is not None and math.isinf(gm_lin):
        assert got["gain_margin_infinite"] is True
        assert got["display"]["gm_db"] == "Infinite"
    elif gm_lin is not None and math.isfinite(gm_lin):
        assert got["gain_margin_linear"] == pytest.approx(float(gm_lin), rel=1e-4)

    if pm_deg is not None and math.isinf(pm_deg):
        assert got["phase_margin_infinite"] is True
        assert got["display"]["pm_deg"] == "Infinite"
    elif pm_deg is not None and math.isfinite(pm_deg):
        assert got["phase_margin_deg"] == pytest.approx(float(pm_deg), rel=1e-3)

    if wpc is None or (isinstance(wpc, float) and math.isnan(wpc)):
        assert got["phase_crossover_rad_s"] is None
        assert got["display"]["wcp"] == "No crossover"
    else:
        assert got["phase_crossover_rad_s"] == pytest.approx(float(wpc), rel=1e-3)

    if wgc is None or (isinstance(wgc, float) and math.isnan(wgc)):
        assert got["gain_crossover_rad_s"] is None
        assert got["display"]["wcg"] == "No crossover"
    else:
        assert got["gain_crossover_rad_s"] == pytest.approx(float(wgc), rel=1e-3)
