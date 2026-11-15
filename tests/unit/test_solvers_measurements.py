from __future__ import annotations

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_wheatstone_bridge() -> None:
    out = _solve("bridge_balance", bridge="wheatstone", r1=100, r2=200, r3=50)
    assert out["value"] == pytest.approx(100.0, rel=1e-9)


def test_ammeter_shunt() -> None:
    out = _solve("meter_range_extension", kind="ammeter_shunt", rm=50, im_fs=0.001, i_range=1.0)
    assert out["value"] == pytest.approx(0.05005, rel=1e-4)