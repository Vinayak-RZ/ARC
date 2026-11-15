from __future__ import annotations

import pytest

from electrical_engineer.catalog import load_recipe_meta
from electrical_engineer.runner.execute import execute

_RECIPES = (
    "bjt-bias-study",
    "opamp-amplifier-study",
    "kmap-minimization-study",
    "bridge-balance-study",
    "meter-range-extension-study",
)


@pytest.mark.parametrize("recipe_id", _RECIPES)
def test_electronics_measurements_checked(tmp_path, recipe_id: str) -> None:
    meta = load_recipe_meta(recipe_id)
    problem = dict(meta["sample_problem"])
    out = execute(recipe_id, problem=problem, run_root=tmp_path)
    assert out["summary"]["unchecked"] is False