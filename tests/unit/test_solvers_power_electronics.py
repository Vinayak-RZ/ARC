from __future__ import annotations

import math

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})["value"]


def test_rectifier_1ph_golden() -> None:
    v = _solve(
        "rectifier_1ph",
        v_rms=230,
        alpha_deg=30,
        topology="full",
        load="continuous",
    )
    assert v == pytest.approx(179.33, rel=1e-3)


def test_rectifier_3ph_golden() -> None:
    v = _solve("rectifier_3ph", v_ll_rms=415, alpha_deg=45, topology="full")
    assert v == pytest.approx(396.29, rel=1e-3)


def test_boost_ccm_golden() -> None:
    v = _solve("boost_ccm", vin=12, d=0.5, l=1e-4, c=1e-5, fs=1e5, r=10)
    assert v == pytest.approx(24.0, rel=1e-6)


def test_buck_boost_golden() -> None:
    v = _solve("buck_boost_ccm", vin=12, d=0.6, l=1e-4, c=1e-5, fs=1e5, r=10)
    assert v == pytest.approx(-18.0, rel=1e-6)


def test_six_step_inverter() -> None:
    v = _solve("inverter_six_step", vdc=600)
    assert v == pytest.approx(math.sqrt(6) / math.pi * 600, rel=1e-3)


def test_spwm_overmodulation() -> None:
    with pytest.raises(ValueError, match="overmodulation"):
        solve_ee_v2({"solver": "spwm_inverter", "vdc": 100, "ma": 1.1, "mf": 10, "phases": "3"})


def test_spwm_3ph_golden() -> None:
    v = _solve("spwm_inverter", vdc=600, ma=0.8, mf=21, phases="3")
    assert v == pytest.approx(293.95, rel=1e-3)