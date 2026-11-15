from __future__ import annotations

import math

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2

control = pytest.importorskip("control")


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_zn_ultimate_pid() -> None:
    out = _solve("zn_ultimate", ku=10, pu_s=2, mode="PID")
    assert out["value"] == pytest.approx(6.0, rel=1e-9)
    assert out["result"]["ti_s"] == pytest.approx(1.0, rel=1e-9)
    assert out["result"]["td_s"] == pytest.approx(0.25, rel=1e-9)


def test_zn_reaction_pid() -> None:
    out = _solve("zn_reaction_curve", k_plant=2, l_s=1, t_s=10, mode="PID")
    assert out["value"] == pytest.approx(6.0, rel=1e-9)


def test_lead_compensator_alpha_band() -> None:
    out = _solve(
        "lead_compensator",
        num=[1],
        den=[1, 1, 0],
        kv_target=10,
        pm_target_deg=45,
        epsilon_deg=8,
    )
    alpha = out["value"]
    assert 3.0 <= alpha <= 5.5
    assert out["result"]["pm_comp_deg"] >= 43.0


def test_lag_compensator_pm() -> None:
    out = _solve(
        "lag_compensator",
        num=[1],
        den=[1, 1, 0],
        k=10,
        pm_target_deg=45,
        epsilon_deg=5,
    )
    assert out["result"]["pm_comp_deg"] >= 43.0


def test_second_order_overshoot() -> None:
    out = _solve("second_order_specs", zeta=0.5, wn=1)
    assert out["value"] == pytest.approx(16.30, rel=1e-2)


def test_routh_hurwitz_rhp() -> None:
    out = _solve("routh_hurwitz", coeffs=[1, 1, 2, 8])
    assert out["value"] == pytest.approx(2.0, abs=1e-9)