"""Trap verifiers for RLVR rewards (deterministic Arc engines)."""

from __future__ import annotations

import math
from typing import Any

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area
from electrical_engineer.engines.ed_lambda import EdCase, incremental_cost, solve_lambda_ed
from electrical_engineer.engines.eec301_goldens import load_exp06_golden, load_exp07_golden
from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_angle,
    initial_angle_pre_fault,
    swing_derivative,
    time_to_angle_during_fault,
)

_ALLOWED_INTEGRATORS = frozenset({"euler", "me", "rk4", "rk4_handwritten"})


def _close(a: float, b: float, tol: float) -> bool:
    return abs(float(a) - float(b)) <= float(tol)


def grade_trap(trap_id: str, submission: dict[str, Any]) -> tuple[bool, float]:
    """Return (passed, reward in [0,1])."""
    fn = _GRADERS.get(trap_id)
    if fn is None:
        return False, 0.0
    return fn(submission)


def _grade_t1(sub: dict[str, Any]) -> tuple[bool, float]:
    gold = load_exp06_golden()["equal_area"]["delta_cr_deg"]
    val = sub.get("delta_cr_deg")
    if val is None:
        return False, 0.0
    ok = _close(float(val), gold, 0.05)
    return ok, 1.0 if ok else 0.0


def _grade_t2(sub: dict[str, Any]) -> tuple[bool, float]:
    gold = load_exp06_golden()
    t_want = gold["time_to_delta_cr"]["t_to_dcr"]
    val = sub.get("t_to_delta_cr_s")
    if val is None:
        return False, 0.0
    ok = _close(float(val), t_want, 1e-3)
    return ok, 1.0 if ok else 0.0


def _grade_t3(sub: dict[str, Any]) -> tuple[bool, float]:
    case = SmibCase()
    want = case.accel_coeff()
    got = sub.get("accel_coeff")
    if got is None:
        return False, 0.0
    ok = _close(float(got), want, 1e-9)
    d0 = initial_angle_pre_fault(case)
    _, domega0 = swing_derivative(d0, 0.0, case.pmax_pre_pu, case)
    eq_ok = abs(domega0) < 1e-10
    if sub.get("domega0_at_prefault") is not None:
        eq_ok = eq_ok and abs(float(sub["domega0_at_prefault"])) < 1e-8
    ok = ok and eq_ok
    return ok, 1.0 if ok else 0.0


def _grade_t4(sub: dict[str, Any]) -> tuple[bool, float]:
    gold = load_exp07_golden()["run1_primary"]["steady"]
    df = sub.get("primary_df1_Hz")
    p12 = sub.get("primary_P12_MW")
    if df is None or p12 is None:
        return False, 0.0
    ok = _close(float(df), gold["df1_Hz"], 0.002)
    ok = ok and _close(float(p12), gold["P12_MW"], 0.5)
    ok = ok and float(p12) < 0
    return ok, 1.0 if ok else 0.0


def _grade_t5(sub: dict[str, Any]) -> tuple[bool, float]:
    gold = load_exp07_golden()["run2_agc"]["steady"]
    case = TwoAreaAgcCase.eec301_default().with_k(0.3)
    st = simulate_two_area(case, run="agc", t_end_s=60.0)["steady"]
    df = sub.get("agc_ss_df1_Hz")
    p12 = sub.get("agc_ss_P12_MW")
    if df is None or p12 is None:
        return False, 0.0
    ok = _close(float(df), gold["df1_Hz"], 1e-3)
    ok = ok and _close(float(p12), gold["P12_MW"], 0.02)
    ok = ok and _close(st["df1_hz"], float(df), 1e-3)
    return ok, 1.0 if ok else 0.0


def _grade_t6(sub: dict[str, Any]) -> tuple[bool, float]:
    r = solve_lambda_ed(EdCase.eec301_default(), 500.0)
    p2 = sub.get("unit2_MW")
    ic2 = sub.get("unit2_IC")
    lam = sub.get("lambda")
    if None in (p2, ic2, lam):
        return False, 0.0
    ok = _close(float(p2), r["P"][1], 0.01)
    ok = ok and float(ic2) < float(lam) + 1e-6
    ok = ok and _close(float(p2), 150.0, 0.01)
    return ok, 1.0 if ok else 0.0


def _grade_t7(sub: dict[str, Any]) -> tuple[bool, float]:
    case = EdCase.eec301_default()
    p = float(sub.get("unit1_MW", 120.0))
    ic_engine = incremental_cost(p, case.units[0])
    ic = sub.get("unit1_IC")
    if ic is None:
        return False, 0.0
    ok = _close(float(ic), ic_engine, 1e-6)
    wrong = sub.get("ic_without_factor_2")
    if wrong is not None:
        ok = ok and abs(float(wrong) - ic_engine) > 1e-3
    return ok, 1.0 if ok else 0.0


def _grade_t8(sub: dict[str, Any]) -> tuple[bool, float]:
    """Block diagram: negative feedback sum signs +- required."""
    signs = str(sub.get("sum_signs", ""))
    ok = signs == "+-"
    trap = str(sub.get("sum_signs_trap", ""))
    if trap:
        ok = ok and trap != "++"
    return ok, 1.0 if ok else 0.0


def _grade_t9(sub: dict[str, Any]) -> tuple[bool, float]:
    integrator = str(sub.get("integrator", "")).lower()
    forbidden = sub.get("forbidden_solver_used")
    if forbidden is True:
        return False, 0.0
    if integrator in ("ode45", "solve_ivp", "minimize", "linprog"):
        return False, 0.0
    ok = integrator in _ALLOWED_INTEGRATORS
    return ok, 1.0 if ok else 0.0


def _grade_t10(sub: dict[str, Any]) -> tuple[bool, float]:
    case = SmibCase()
    gold = load_exp06_golden()
    checks = [
        _close(float(sub.get("pm_pu", case.pm_pu)), case.pm_pu, 1e-9),
        _close(float(sub.get("f0_hz", case.f0_hz)), float(gold["params"]["f0"]), 1e-9),
        _close(float(sub.get("pmax_pre_pu", case.pmax_pre_pu)), case.pmax_pre_pu, 1e-9),
    ]
    ok = all(checks)
    return ok, 1.0 if ok else 0.0


_GRADERS = {
    "T1": _grade_t1,
    "T2": _grade_t2,
    "T3": _grade_t3,
    "T4": _grade_t4,
    "T5": _grade_t5,
    "T6": _grade_t6,
    "T7": _grade_t7,
    "T8": _grade_t8,
    "T9": _grade_t9,
    "T10": _grade_t10,
}


def oracle_submission(trap_id: str) -> dict[str, Any]:
    """Deterministic oracle answers for dummy-policy rollouts."""
    if trap_id == "T1":
        return {"delta_cr_deg": math.degrees(critical_clearing_angle(SmibCase()))}
    if trap_id == "T2":
        gold = load_exp06_golden()
        case = SmibCase()
        t = time_to_angle_during_fault(
            case,
            gold["equal_area"]["delta_cr_rad"],
            h_s=gold["time_to_delta_cr"]["h"],
        )
        return {"t_to_delta_cr_s": t}
    if trap_id == "T3":
        case = SmibCase()
        d0 = initial_angle_pre_fault(case)
        _, domega0 = swing_derivative(d0, 0.0, case.pmax_pre_pu, case)
        return {"accel_coeff": case.accel_coeff(), "domega0_at_prefault": domega0}
    if trap_id == "T4":
        gold = load_exp07_golden()["run1_primary"]["steady"]
        return {"primary_df1_Hz": gold["df1_Hz"], "primary_P12_MW": gold["P12_MW"]}
    if trap_id == "T5":
        gold = load_exp07_golden()["run2_agc"]["steady"]
        return {"agc_ss_df1_Hz": gold["df1_Hz"], "agc_ss_P12_MW": gold["P12_MW"]}
    if trap_id == "T6":
        r = solve_lambda_ed(EdCase.eec301_default(), 500.0)
        return {"unit2_MW": r["P"][1], "unit2_IC": r["IC"][1], "lambda": r["lam"]}
    if trap_id == "T7":
        case = EdCase.eec301_default()
        p = 120.0
        u = case.units[0]
        ic = incremental_cost(p, u)
        return {"unit1_MW": p, "unit1_IC": ic, "ic_without_factor_2": u.b + u.c * p}
    if trap_id == "T8":
        return {"sum_signs": "+-"}
    if trap_id == "T9":
        return {"integrator": "rk4", "forbidden_solver_used": False}
    if trap_id == "T10":
        case = SmibCase()
        return {
            "pm_pu": case.pm_pu,
            "f0_hz": case.f0_hz,
            "pmax_pre_pu": case.pmax_pre_pu,
        }
    raise KeyError(trap_id)
