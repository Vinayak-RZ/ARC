"""SolverSpec registry and default_solver injection."""

from __future__ import annotations

import pytest

from electrical_engineer.engines import ee_v2_runner as runner
from electrical_engineer.engines.solvers import SPECS, build_kwargs
from electrical_engineer.engines.solvers.spec import Param, SolverSpec
from electrical_engineer.nodes.sim import _problem_with_default_solver


def test_build_kwargs_required_and_choices() -> None:
    def fn(a: float, mode: str) -> dict:
        return {"v": a, "mode": mode}

    spec = SolverSpec(
        fn=fn,
        params=(
            Param("a", kind="num"),
            Param("mode", kind="str", choices=("x", "y")),
        ),
        value_key="v",
        unit="1",
    )
    with pytest.raises(KeyError, match="missing a"):
        build_kwargs(spec, {"mode": "x"})
    with pytest.raises(ValueError, match="must be one of"):
        build_kwargs(spec, {"a": 1, "mode": "z"})
    kw = build_kwargs(spec, {"a": 2, "mode": "x"})
    assert kw == {"a": 2.0, "mode": "x"}


def test_no_id_collisions() -> None:
    assert set(SPECS).isdisjoint(set(runner.DEFAULT_VALUE_KEY) - set(SPECS))
    # legacy ids still present
    assert "ccm_buck" in runner.SOLVER_IDS


def test_default_solver_injection() -> None:
    problem = _problem_with_default_solver(
        {"default_solver": "ccm_buck", "problem": {"vin": 12, "vout": 5, "l": 1e-4, "c": 1e-5, "fs": 1e5}}
    )
    assert problem["solver"] == "ccm_buck"
    # explicit solver wins
    problem2 = _problem_with_default_solver(
        {
            "default_solver": "ccm_buck",
            "problem": {"solver": "rc_step", "v": 1, "r": 1, "c": 1, "t": 1},
        }
    )
    assert problem2["solver"] == "rc_step"


def test_registry_dispatch_roundtrip(monkeypatch) -> None:
    def add(a: float, b: float = 1.0) -> dict:
        return {"sum": a + b}

    spec = SolverSpec(
        fn=add,
        params=(Param("a"), Param("b", default=1.0)),
        value_key="sum",
        unit="1",
    )
    SPECS["test_add"] = spec
    runner.DEFAULT_VALUE_KEY["test_add"] = "sum"
    runner.SOLVER_IDS = frozenset(runner.DEFAULT_VALUE_KEY)
    try:
        out = runner.solve_ee_v2({"solver": "test_add", "a": 3, "b": 4})
        assert out["value"] == 7.0
        assert out["unit"] == "1"
    finally:
        SPECS.pop("test_add", None)
        runner.DEFAULT_VALUE_KEY.pop("test_add", None)
        runner.SOLVER_IDS = frozenset(runner.DEFAULT_VALUE_KEY)
