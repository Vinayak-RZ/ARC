from __future__ import annotations

import pytest

from electrical_engineer.catalog import load_recipe_meta
from electrical_engineer.runner.execute import execute

_PE_RECIPES = (
    "rectifier-1ph-study",
    "rectifier-3ph-study",
    "boost-converter-study",
    "buck-boost-converter-study",
    "six-step-inverter-study",
    "spwm-inverter-study",
)


@pytest.mark.parametrize("recipe_id", _PE_RECIPES)
def test_power_electronics_study_checked(tmp_path, recipe_id: str) -> None:
    meta = load_recipe_meta(recipe_id)
    problem = dict(meta["sample_problem"])
    out = execute(recipe_id, problem=problem, run_root=tmp_path)
    assert out["summary"]["unchecked"] is False