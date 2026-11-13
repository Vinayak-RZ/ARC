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
