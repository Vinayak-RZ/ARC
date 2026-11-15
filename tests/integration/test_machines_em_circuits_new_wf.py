from __future__ import annotations

import pytest

from electrical_engineer.catalog import load_recipe_meta
from electrical_engineer.runner.execute import execute

_RECIPES = (
    "transformer-tests-study",
    "induction-torque-slip-study",
    "synchronous-regulation-study",
    "line-parameters-study",
    "capacitance-geometry-study",
    "thevenin-equivalent-study",
    "max-power-transfer-study",
    "two-port-study",
    "resonance-study",
)


@pytest.mark.parametrize("recipe_id", _RECIPES)
def test_machines_em_circuits_checked(tmp_path, recipe_id: str) -> None:
    meta = load_recipe_meta(recipe_id)
    problem = dict(meta["sample_problem"])
    out = execute(recipe_id, problem=problem, run_root=tmp_path)
    assert out["summary"]["unchecked"] is False