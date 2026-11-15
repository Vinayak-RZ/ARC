from __future__ import annotations

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2
from electrical_engineer.engines.solvers.electronics import _eval_sop


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_bjt_divider_bias_ic() -> None:
    out = _solve(
        "bjt_divider_bias",
        vcc=12,
        r1=10_000,
        r2=2200,
        rc=1000,
        re=220,
        beta=100,
    )
    assert out["value"] == pytest.approx(6.094e-3, rel=1e-3)
    assert out["result"]["region"] == "active"


def test_opamp_inverting_gain() -> None:
    out = _solve("opamp_config", config="inverting", vin=[1], rf=10_000, r1=1000)
    assert out["value"] == pytest.approx(-10.0, rel=1e-9)


def test_kmap_minimize_literals_and_truth() -> None:
    minterms = [0, 1, 2, 5, 6, 7, 8, 9, 10, 14]
    out = _solve("kmap_minimize", n_vars=4, minterms=minterms)
    assert out["value"] <= 9.0
    sop = out["result"]["sop"]
    mt = set(minterms)
    for m in range(16):
        assign = {chr(65 + i): format(m, "04b")[i] == "1" for i in range(4)}
        assert _eval_sop(sop, assign) == (m in mt)