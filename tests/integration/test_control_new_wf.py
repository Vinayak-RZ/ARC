from __future__ import annotations

import pytest

from electrical_engineer.catalog import load_recipe_meta
from electrical_engineer.engines.ee_v2_runner import solve_ee_v2
from electrical_engineer.runner.execute import execute

_CONTROL_RECIPES = (
    "pid-zn-ultimate-study",
    "pid-zn-reaction-curve-study",
    "lead-compensator-design-study",
    "lag-compensator-design-study",
    "second-order-specs-study",
    "routh-hurwitz-study",
)


@pytest.mark.parametrize("recipe_id", _CONTROL_RECIPES)
def test_control_study_checked(tmp_path, recipe_id: str) -> None:
    pytest.importorskip("control")
    meta = load_recipe_meta(recipe_id)
    problem = dict(meta["sample_problem"])
    if recipe_id == "lead-compensator-design-study":
        solved = solve_ee_v2({"solver": "lead_compensator", **problem})
        problem["expected"] = solved["value"]
    elif recipe_id == "lag-compensator-design-study":
        solved = solve_ee_v2({"solver": "lag_compensator", **problem})
        problem["expected"] = solved["value"]
    out = execute(recipe_id, problem=problem, run_root=tmp_path)
    assert out["summary"]["unchecked"] is False