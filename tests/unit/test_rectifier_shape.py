"""Rectifier waveform shape vs piecewise closed form (not mean-only)."""

from __future__ import annotations

import math

import pytest

from electrical_engineer.engines.rectifier_gate import line_peak_from_line_vll
from electrical_engineer.engines.rectifier_steady import firing_angles_deg, vo_full3_analytic
from electrical_engineer.engines.rectifier_waveforms import (
    _vo_closed_form,
    mean_waveform,
    sample_waveform,
)
from electrical_engineer.engines.solvers.power_electronics import rectifier_1ph, rectifier_3ph
from tests.unit.rectifier_mean_tolerance import rectifier_mean_rel_tol, rectifier_mean_skip


def _interp(points: list[list[float]], deg_angle: float) -> float:
    best = min(points, key=lambda row: abs(row[0] - deg_angle))
    if abs(best[0] - deg_angle) > 1.0:
        raise AssertionError(f"no sample near {deg_angle}°")
    return float(best[1])


def _vll_pk(v_ll_rms: float = 415.0) -> float:
    return line_peak_from_line_vll(v_ll_rms)


def _expected_full3(wt_deg: float, alpha_deg: float, v_ll_rms: float = 415.0) -> float:
    return vo_full3_analytic(math.radians(wt_deg), _vll_pk(v_ll_rms), alpha_deg)


@pytest.mark.parametrize("topology", ("hw1", "semi1", "full1", "hw3", "semi3", "full3"))
@pytest.mark.parametrize("load", ("R", "RL"))
@pytest.mark.parametrize("alpha_deg", (0, 30, 45, 60, 75, 90))
def test_waveform_mean_tracks_vo(topology: str, load: str, alpha_deg: float) -> None:
    if rectifier_mean_skip(topology, load, alpha_deg):
        return
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
    if abs(vo) < 1e-6:
        return
    tol = rectifier_mean_rel_tol(topology, load, alpha_deg)
    assert abs(mean - vo) / abs(vo) < tol


def test_full3_phase_a_firing_marks_and_falling_arcs() -> None:
    """Phase-a ωt: firings at 30+α + 60k; segments are falling line-voltage sines."""
    alpha = 75.0
    v_rms = 415.0
    fire0 = 30.0 + alpha
    vo_avg = _vo_closed_form(
        {"topology": "full3", "load": "RL", "v_rms": v_rms, "v_ll_rms": v_rms, "alpha_deg": alpha, "io_a": 0, "ls_h": 0},
        rectifier_1ph,
        rectifier_3ph,
    )
    pts = sample_waveform(
        {"topology": "full3", "load": "RL", "v_rms": v_rms, "alpha_deg": alpha},
        n=7200,
    )
    mean = mean_waveform(pts)
    assert abs(mean - vo_avg) / abs(vo_avg) < 0.006

    fires = firing_angles_deg("full3", alpha)
    assert fires == [105.0, 165.0, 225.0, 285.0, 345.0, 45.0]

    omega_seg_end = fire0 + 60.0 - 0.05
    vll = _vll_pk(v_rms)
    v_line_start = vll * math.sin(math.radians(fire0 + 30.0))
    v_line_end = vll * math.sin(math.radians(omega_seg_end + 30.0))
    assert abs(_expected_full3(fire0, alpha, v_rms) - v_line_start) < 1.0
    assert abs(_expected_full3(omega_seg_end, alpha, v_rms) - v_line_end) < 2.0
    assert v_line_start > 400.0 and v_line_end < -100.0

    for f in fires:
        v_before = _expected_full3((f - 0.05) % 360, alpha, v_rms)
        v_after = _expected_full3((f + 0.05) % 360, alpha, v_rms)
        assert v_after - v_before > 200.0, f"jump at firing {f}°"
        assert abs(_interp(pts, (f + 0.05) % 360) - v_after) < 2.5
        assert abs(_interp(pts, (f - 0.05 + 360) % 360) - v_before) < 2.5

    mid_first = fire0 + 30.0
    v_mid_lo = _expected_full3(mid_first - 5, alpha, v_rms)
    v_mid_hi = _expected_full3(mid_first + 5, alpha, v_rms)
    assert v_mid_lo > v_mid_hi, "first segment is a falling sine arc, not rising"

    for wt_deg in (fire0 + 2, fire0 + 20, mid_first, fire0 + 50, fire0 + 59.5):
        exp = _expected_full3(wt_deg, alpha, v_rms)
        got = _interp(pts, wt_deg)
        assert abs(got - exp) < 2.5, f"ωt={wt_deg}° sample vs analytic"


def test_full3_sample_matches_analytic_sweep() -> None:
    alpha = 75.0
    pts = sample_waveform({"topology": "full3", "load": "RL", "v_rms": 415, "alpha_deg": alpha}, n=7200)
    for i, (wt_deg, got) in enumerate(pts):
        exp = _expected_full3(wt_deg, alpha)
        assert abs(got - exp) < 0.5, f"ωt={wt_deg}° (i={i})"