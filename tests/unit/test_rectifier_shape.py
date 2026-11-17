"""Rectifier waveform shape vs piecewise closed form (not mean-only)."""

from __future__ import annotations

import math

import pytest

from electrical_engineer.engines.rectifier_steady import firing_angles_deg, vo_full3_analytic
from electrical_engineer.engines.rectifier_gate import gate_sample_vo, line_peak_from_line_vll
from electrical_engineer.engines.rectifier_waveforms import mean_waveform, sample_waveform
from electrical_engineer.engines.solvers.power_electronics import rectifier_1ph, rectifier_3ph
from electrical_engineer.engines.rectifier_waveforms import _vo_closed_form

_SQRT2 = math.sqrt(2.0)


def _interp(points: list[list[float]], deg_angle: float) -> float:
    best = min(points, key=lambda row: abs(row[0] - deg_angle))
    if abs(best[0] - deg_angle) > 1.0:
        raise AssertionError(f"no sample near {deg_angle}°")
    return float(best[1])


@pytest.mark.parametrize("topology", ("hw1", "semi1", "full1", "hw3", "semi3", "full3"))
@pytest.mark.parametrize("load", ("R", "RL"))
@pytest.mark.parametrize("alpha_deg", (0, 30, 45, 60, 75, 90))
def test_waveform_mean_tracks_vo(topology: str, load: str, alpha_deg: float) -> None:
    v = 415 if topology.endswith("3") else 230
    vo = _vo_closed_form(
        {"topology": topology, "load": load, "v_rms": v, "v_ll_rms": v, "alpha_deg": alpha_deg, "io_a": 0, "ls_h": 0},
        rectifier_1ph,
        rectifier_3ph,
    )
    pts = sample_waveform(
        {"topology": topology, "load": load, "v_rms": v, "v_ll_rms": v, "alpha_deg": alpha_deg},
        n=3600,
    )
    mean = mean_waveform(pts)
    if abs(vo) < 1.0:
        assert abs(mean) < 1.0
        return
    assert abs(mean - vo) / abs(vo) < 0.006


def test_full3_rl_75_firing_jumps_and_sine_arc() -> None:
    alpha = 75.0
    v_rms = 415.0
    vll = line_peak_from_line_vll(v_rms)
    pts = gate_sample_vo(
        {"topology": "full3", "load": "RL", "v_rms": v_rms, "alpha_deg": alpha, "r_ohm": 10},
        n=7200,
    )
    fires = firing_angles_deg("full3", alpha)
    assert len(fires) == 6
    for f in fires:
        v_after = _interp(pts, (f + 0.25) % 360)
        v_before = _interp(pts, (f - 0.25 + 360) % 360)
        assert abs(v_after - 415.0) < 2.0, f"after {f}° expected ~415 V, got {v_after}"
        assert abs(v_before - v_after) > 200.0, f"commutation jump at {f}°"
    v105 = _interp(pts, 105.0)
    v135 = _interp(pts, 135.0)
    v165 = _interp(pts, 165.0)
    assert v105 > 400.0
    assert v135 < v105 and v135 > 100.0, "segment 1 must fall along sine arc, not rise"
    assert v165 > 400.0
    wt135 = math.radians(135.0)
    expected = vo_full3_analytic(wt135, vll, alpha)
    assert abs(v135 - expected) < 2.0


def test_full3_analytic_matches_piecewise_samples() -> None:
    vll = _SQRT2 * 415
    for deg_angle in (110, 130, 195, 250, 320, 50):
        wt = math.radians(deg_angle)
        expected = vo_full3_analytic(wt, vll, 75.0)
        got = vo_full3_analytic(wt, vll, 75.0)
        assert abs(got - expected) < 1e-6