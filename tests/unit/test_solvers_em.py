from __future__ import annotations

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_line_parameters_equilateral() -> None:
    out = _solve("line_parameters", config="three_phase_equilateral", r_m=0.01, d_m=2)
    assert out["value"] == pytest.approx(1.1097e-3, rel=1e-3)


def test_parallel_plate_capacitance() -> None:
    out = _solve(
        "capacitance_geometry",
        geometry="parallel_plate",
        eps_r=1,
        area_m2=1,
        d_m=0.001,
    )
    assert out["value"] == pytest.approx(8.854187817e-9, rel=1e-6)