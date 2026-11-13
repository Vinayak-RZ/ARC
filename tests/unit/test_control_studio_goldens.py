"""Golden diagram parity vs independent python-control."""

from __future__ import annotations

import pytest

from electrical_engineer.control_studio.compose import compose_closed_loop
from electrical_engineer.control_studio.goldens import GOLDENS
from electrical_engineer.control_studio.simulate import simulate
from electrical_engineer.control_studio.validate import validate
from electrical_engineer.engines.block_diagram import compose_plant
from electrical_engineer.engines.control_runner import control_available


@pytest.mark.skipif(not control_available(), reason="python-control missing")
@pytest.mark.parametrize("name", list(GOLDENS))
def test_golden_validate_ok(name: str) -> None:
    diagram = GOLDENS[name]()
    if name == "lead_compensator":
        # open-loop shaping reference; validation relaxed (no sum)
        assert validate(diagram)["ok"] or not validate(diagram)["issues"]
        return
    rep = validate(diagram)
    assert rep["ok"], rep


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_unity_first_order_step_ss() -> None:
    import control

    diagram = GOLDENS["unity_first_order"]()
    legacy = diagram["meta"]["unity_feedback"]
    ref_sys, _ = compose_plant(legacy)
    ref_ss = float(control.step_response(ref_sys)[1][-1])
    out = simulate(diagram)
    assert out["ok"]
    assert abs((out["y_ss"] or 0) - ref_ss) < 0.05 * max(1.0, abs(ref_ss))


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_pid_dc_motor_compose() -> None:
    diagram = GOLDENS["pid_dc_motor"]()
    sys, meta = compose_closed_loop(diagram)
    assert meta.get("mode") in ("wired_unity", "unity_feedback")
    assert len(sys.den[0][0]) >= 2


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_lead_meta_tf() -> None:
    import control

    diagram = GOLDENS["lead_compensator"]()
    sys, _ = compose_closed_loop(diagram)
    meta = diagram["meta"]
    ref = control.tf(meta["num"], meta["den"])
    n1 = [float(x) for x in sys.num[0][0].tolist()]
    n2 = [float(x) for x in ref.num[0][0].tolist()]
    d1 = [float(x) for x in sys.den[0][0].tolist()]
    d2 = [float(x) for x in ref.den[0][0].tolist()]
    assert len(n1) == len(n2)
    assert all(abs(a - b) < 1e-6 for a, b in zip(n1, n2, strict=True))
    assert all(abs(a - b) < 1e-6 for a, b in zip(d1, d2, strict=True))


@pytest.mark.skipif(not control_available(), reason="python-control missing")
def test_agc_golden_simulate() -> None:
    diagram = GOLDENS["two_area_agc"]()
    out = simulate(diagram, t_final=5.0)
    assert out["ok"]
    assert out.get("y_ss") is not None
