"""Step settling status for studio charts."""

from __future__ import annotations

import numpy as np
import pytest

from electrical_engineer.control_studio.goldens import GOLDENS
from electrical_engineer.control_studio.simulate import _step_metrics, simulate
from electrical_engineer.engines.control_runner import control_available


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_pid_dc_motor_step_settled() -> None:
    out = simulate(GOLDENS["pid_dc_motor"](), t_final=10.0)
    assert out["ok"]
    m = out["step_series"]["metrics"]
    assert m["status"] == "settled"
    assert m["settled"] is True


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_unity_first_order_settled_off_target() -> None:
    out = simulate(GOLDENS["unity_first_order"](), t_final=10.0)
    assert out["ok"]
    m = out["step_series"]["metrics"]
    assert m["status"] == "settled_off_target"
    assert m["settled"] is False
    assert abs(m["final_value"] - 0.909) < 0.02


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_open_loop_low_gain_not_settled() -> None:
    out = simulate(GOLDENS["open_loop_low_gain"](), t_final=10.0)
    assert out["ok"]
    m = out["step_series"]["metrics"]
    assert m["status"] in ("settled_off_target", "not_settled")
    assert m["settled"] is False


def test_flat_tail_off_target_not_unsettled() -> None:
    t = np.linspace(0, 10, 200)
    y = np.full_like(t, 0.909)
    m = _step_metrics(t, y, 1.0, 10.0)
    assert m["status"] == "settled_off_target"


def test_rising_tail_is_not_settled() -> None:
    t = np.linspace(0, 10, 200)
    y = 0.2 + 0.03 * t
    m = _step_metrics(t, y, 1.0, 10.0)
    assert m["status"] == "not_settled"


def _first_order(k: float, t_end: float = 5.0, n: int = 50001):
    """Unity feedback around k/(s+1): closed loop k/(s+k+1), y_ss = k/(k+1), pole at -(k+1)."""
    t = np.linspace(0.0, t_end, n)
    y_ss = k / (k + 1.0)
    return t, y_ss * (1.0 - np.exp(-(k + 1.0) * t)), y_ss


def test_k10_settles_against_final_value_not_setpoint() -> None:
    t, y, y_ss = _first_order(10.0)
    m = _step_metrics(t, y, 1.0, float(t[-1]))
    assert y_ss == pytest.approx(10.0 / 11.0)
    assert m["final_value"] == pytest.approx(10.0 / 11.0, rel=1e-4)
    # first-order, 2% of the final value: ts = ln(50) / (K + 1), from theory, not from the solver
    ts_theory = float(np.log(50.0) / 11.0)
    assert m["t_settle_s"] is not None
    assert m["t_settle_s"] == pytest.approx(ts_theory, rel=0.01)
    assert m["overshoot_pct"] == pytest.approx(0.0, abs=1e-6)
    assert m["steady_state_error_pct"] == pytest.approx(100.0 / 11.0, abs=0.05)
    assert m["status"] == "settled_off_target"
    assert m["on_target"] is False


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_k10_golden_through_simulate_matches_theory_within_sampling() -> None:
    out = simulate(GOLDENS["unity_first_order"](), t_final=10.0)
    s = out["step_series"]
    m = s["metrics"]
    dt = s["t"][1] - s["t"][0]
    assert m["final_value"] == pytest.approx(10.0 / 11.0, abs=5e-4)
    # sampled equivalent: the last sample outside the band sits at most one step before the true time
    assert abs(m["t_settle_s"] - float(np.log(50.0) / 11.0)) <= 1.5 * dt


@pytest.mark.parametrize("k", [39.0, 60.0])
def test_k39_and_k60_are_treated_consistently(k: float) -> None:
    t, y, _ = _first_order(k, t_end=1.0)
    m = _step_metrics(t, y, 1.0, float(t[-1]))
    assert m["final_value"] == pytest.approx(k / (k + 1.0), rel=1e-4)
    assert m["t_settle_s"] == pytest.approx(float(np.log(50.0) / (k + 1.0)), rel=0.01)
    assert m["overshoot_pct"] == pytest.approx(0.0, abs=1e-6)
    assert m["steady_state_error_pct"] == pytest.approx(100.0 / (k + 1.0), abs=0.06)
    # both have a settling time and a band; only the on-target flag follows the 2% e_ss rule
    assert m["band_pct"] == 2.0
    assert m["on_target"] is (100.0 / (k + 1.0) <= 2.0)


def test_underdamped_overshoot_is_relative_to_final_value() -> None:
    zeta, wn = 0.3, 5.0
    wd = wn * np.sqrt(1 - zeta**2)
    t = np.linspace(0.0, 10.0, 20001)
    base = 1 - np.exp(-zeta * wn * t) * (np.cos(wd * t) + zeta * wn / wd * np.sin(wd * t))
    expected = float(np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2)) * 100.0)  # textbook Mp
    m = _step_metrics(t, base, 1.0, 10.0)
    assert m["overshoot_pct"] == pytest.approx(expected, rel=0.01)
    # same shape scaled to a final value of 2 with setpoint 1: overshoot percent must not change
    m2 = _step_metrics(t, 2.0 * base, 1.0, 10.0)
    assert m2["overshoot_pct"] == pytest.approx(expected, rel=0.01)
    assert m2["status"] == "settled_off_target"
    assert m2["peak_t_s"] == pytest.approx(np.pi / wd, rel=0.01)


def test_unsettled_response_has_no_band_or_settle_marker() -> None:
    t = np.linspace(0, 10, 200)
    m = _step_metrics(t, 0.2 + 0.03 * t, 1.0, 10.0)
    assert m["status"] == "not_settled"
    assert m["t_settle_s"] is None and m["overshoot_pct"] is None and m["band_pct"] is None
