"""Runnable bare-vs-Arc checks for traps T1, T2, T6 (dramatic deltas)."""

from __future__ import annotations

import math

import yaml

from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed
from electrical_engineer.engines.smib_swing import SmibCase, critical_clearing_angle, time_to_angle_during_fault
from electrical_engineer.engines.eec301_goldens import load_exp06_golden


def _bare_t1_wrong_delta_cr() -> float:
    """Bolted-fault Pmax_fault=0 parabola (wrong for this lab)."""
    case = SmibCase()
    d0 = math.asin(case.pm_pu / case.pmax_pre_pu)
    # parabolic approx during fault: delta_cr from zero electrical output
    return math.degrees(d0 + (case.pm_pu / (case.pmax_post_pu - case.pm_pu)) * (math.pi - d0))


def test_ablation_t1_arc_beats_bare_on_delta_cr() -> None:
    gold = load_exp06_golden()["equal_area"]
    arc = math.degrees(critical_clearing_angle(SmibCase()))
    bare = _bare_t1_wrong_delta_cr()
    assert abs(arc - gold["delta_cr_deg"]) < 0.01
    assert abs(bare - gold["delta_cr_deg"]) > 5.0


def test_ablation_t2_time_to_dcr_matches_json() -> None:
    gold = load_exp06_golden()
    t = time_to_angle_during_fault(
        SmibCase(),
        gold["equal_area"]["delta_cr_rad"],
        h_s=gold["time_to_delta_cr"]["h"],
    )
    assert t is not None
    assert abs(t - gold["time_to_delta_cr"]["t_to_dcr"]) < 1e-4


def test_ablation_t6_ed_limit_case() -> None:
    r = solve_lambda_ed(EdCase.eec301_default(), 500.0)
    assert r["P"][1] == 150.0
    assert r["IC"][1] < r["lam"]


def test_trap_prompts_catalog_loads() -> None:
    data = yaml.safe_load(open("proofs/ablation/trap_prompts.yaml", encoding="utf-8"))
    assert "T1" in data["traps"] and "T6" in data["traps"]
