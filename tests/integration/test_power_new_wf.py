from __future__ import annotations

import pytest

from electrical_engineer.catalog import load_recipe_meta
from electrical_engineer.engines.solvers.power import _idmt_psm, _idmt_time
from electrical_engineer.runner.execute import execute

_POWER_RECIPES = (
    "idmt-relay-study",
    "idmt-coordination-study",
    "differential-protection-study",
    "distance-mho-study",
    "circuit-breaker-rrrv-study",
    "critical-clearing-study",
    "lfc-single-area-study",
)


@pytest.mark.parametrize("recipe_id", _POWER_RECIPES)
def test_power_study_checked(tmp_path, recipe_id: str) -> None:
    meta = load_recipe_meta(recipe_id)
    problem = dict(meta["sample_problem"])
    if recipe_id == "idmt-coordination-study":
        i_fault = float(problem["i_fault_a"])
        psm1 = _idmt_psm(i_fault, problem["r1_ct_primary_a"], 1.0, problem["r1_plug_setting"])
        t1 = _idmt_time(psm1, problem["r1_tms"], problem["r1_curve"])
        psm2 = _idmt_psm(i_fault, problem["r2_ct_primary_a"], 1.0, problem["r2_plug_setting"])
        k, a = 0.14, 0.02
        problem["expected"] = (t1 + problem["cti_s"]) * (psm2**a - 1.0) / k
    out = execute(recipe_id, problem=problem, run_root=tmp_path)
    assert out["summary"]["unchecked"] is False