from __future__ import annotations

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_thevenin_divider() -> None:
    netlist = "V1 1 0 DC 10\nR1 1 2 1000\nR2 2 0 1000"
    out = _solve("thevenin_dc", netlist=netlist, port_a="2", port_b="0")
    assert out["value"] == pytest.approx(5.0, rel=1e-9)
    assert out["result"]["Rth_ohm"] == pytest.approx(500.0, rel=1e-9)


def test_max_power_transfer() -> None:
    out = _solve("max_power_transfer", vth_rms=10, rth=50)
    assert out["value"] == pytest.approx(0.5, rel=1e-9)


def test_two_port_z_to_y() -> None:
    out = _solve("two_port_convert", from_set="z", to_set="y", m=[[10, 5], [5, 20]])
    assert out["value"] == pytest.approx(20.0 / 175.0, rel=1e-4)


def test_resonance_series() -> None:
    out = _solve("resonance", r=10, l=0.01, c=1e-6, config="series")
    assert out["value"] == pytest.approx(1591.55, rel=1e-3)