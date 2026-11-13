from __future__ import annotations

from electrical_engineer.engines.ee_v2_runner import recompute_scalar, solve_ee_v2


def test_rc_step_dispatch() -> None:
    problem = {
        "solver": "rc_step",
        "v": 10,
        "r": 1000,
        "c": 0.001,
        "t": 1.0,
        "value_key": "vc_V",
        "expected": 6.321205588615618,
    }
    out = solve_ee_v2(problem)
    assert out["unit"] == "V"
    assert abs(out["value"] - problem["expected"]) < 1e-6
    assert abs(recompute_scalar(problem) - problem["expected"]) < 1e-6


def test_breakaway_pick_sigma() -> None:
    problem = {
        "solver": "breakaway_real_axis",
        "poles": [0, -3, -6],
        "zeros": [],
        "pick_sigma": -1.268,
    }
    out = solve_ee_v2(problem)
    assert abs(out["value"] + 1.268) < 0.02
