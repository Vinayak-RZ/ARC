"""Open-loop L(s)=C(s)G(s) for PID·DC motor must include controller (Ki → low-f req gain, 0 dB cross)."""

from __future__ import annotations

import math

import numpy as np
import pytest

from electrical_engineer.control_studio.compose import open_loop_with_controller
from electrical_engineer.control_studio.goldens import pid_dc_motor
from electrical_engineer.control_studio.layout import layout_chain
from electrical_engineer.control_studio.library import dc_motor_tf, pid_tf
from electrical_engineer.control_studio.margins import extract_margins
from electrical_engineer.engines.control_runner import control_available


def _hand_built_cg(diagram: dict) -> object:
    import control

    p = next(b for b in diagram["blocks"] if b["type"] == "pid")
    m = next(b for b in diagram["blocks"] if b["type"] == "plant_dc_motor")
    return control.series(pid_tf(p["params"]), dc_motor_tf(m["params"] or {}))


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_pid_dc_motor_open_loop_matches_hand_built_margins() -> None:
    import control

    diagram = layout_chain(pid_dc_motor())
    ol, meta = open_loop_with_controller(diagram)
    assert meta["mode"] == "open_loop_cg"
    assert "pid1" in meta["forward_chain"]
    assert "motor" in meta["forward_chain"]

    l_ref = _hand_built_cg(diagram)
    w_low = 1e-4
    mag_lo, _, _ = control.bode(l_ref, omega=[w_low], plot=False)
    assert float(20 * np.log10(mag_lo[0])) >= 40.0

    gm, pm, wpc, wgc = control.margin(ol)
    gm_r, pm_r, wpc_r, wgc_r = control.margin(l_ref)

    assert wgc is not None and math.isfinite(float(wgc))
    assert abs(float(wgc) - float(wgc_r)) < 1e-6

    if gm is not None and math.isfinite(float(gm)) and math.isfinite(float(gm_r)):
        assert abs(float(gm) - float(gm_r)) < 1e-6
    if pm is not None and math.isfinite(float(pm)) and math.isfinite(float(pm_r)):
        assert abs(float(pm) - float(pm_r)) < 1e-6
    if wpc is not None and wpc_r is not None and math.isfinite(float(wpc)) and math.isfinite(float(wpc_r)):
        assert abs(float(wpc) - float(wpc_r)) < 1e-6

    got = extract_margins(ol)
    assert got["gain_crossover_rad_s"] is not None
    assert abs(got["gain_crossover_rad_s"] - float(wgc)) < 1e-5
    assert got["display"]["wcg"] != "No crossover"
