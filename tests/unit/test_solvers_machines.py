from __future__ import annotations

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_synchronous_regulation_lag_pf() -> None:
    out = _solve(
        "synchronous_regulation",
        v_phase=1,
        i_a=1,
        pf=0.8,
        pf_type="lag",
        xs=1,
        ra=0,
    )
    assert out["value"] == pytest.approx(78.885, rel=1e-3)


def test_transformer_eta() -> None:
    out = _solve(
        "transformer_oc_sc",
        kva=100,
        v_lv=400,
        v_hv=11000,
        oc_v=400,
        oc_i=2,
        oc_p=300,
        sc_v=500,
        sc_i=5,
        sc_p=1500,
    )
    assert out["value"] == pytest.approx(93.832, rel=1e-3)


def test_induction_torque_slip() -> None:
    kw = {
        "v_ll": 400,
        "f_hz": 50,
        "poles": 4,
        "r1": 0.2,
        "x1": 0.5,
        "r2": 0.15,
        "x2": 0.4,
        "xm": 15,
        "slip": 0.05,
    }
    out = _solve("induction_torque_slip", **kw)
    assert out["value"] == pytest.approx(261.447, rel=1e-3)