"""Per-trap detectors: engine-backed numerics; text is advisory only."""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from typing import Any

from electrical_engineer.engines.agc_two_area import simulate_two_area
from electrical_engineer.engines.ed_lambda import solve_lambda_ed
from electrical_engineer.engines.smib_swing import (
    critical_clearing_angle,
    time_to_angle_during_fault,
)
from electrical_engineer.traps.givens import (
    agc_case_from_givens,
    ed_case_from_givens,
    merged_givens,
    pd_mw_from_givens,
    smib_case_from_givens,
)
from electrical_engineer.traps.schema import SolutionTrace, TrapCheck
from electrical_engineer.traps.text_advisory import find_advisory

Detector = Callable[[SolutionTrace], TrapCheck]

_NUM_TOL_REL = 0.02
_FORBIDDEN_SOLVER = frozenset({"ode45", "fmincon", "lsode", "odeint"})
_ADV_ODE = re.compile(r"\b(?:ode45|fmincon)\b", re.IGNORECASE)
_ADV_IGNORE_LIMITS = re.compile(r"ignore\s+(?:generator\s+)?limits", re.IGNORECASE)
_ADV_AGC_DIP = re.compile(
    r"(?:agc|secondary).{0,40}(?:remove|eliminate|zero).{0,20}(?:first\s*dip|initial\s*dip)",
    re.IGNORECASE,
)


def _uncheck(trap_id: str, message: str = "insufficient givens or claims") -> TrapCheck:
    return TrapCheck(trap_id=trap_id, status="unchecked", passed=False, message=message)


def _pass(trap_id: str, message: str = "") -> TrapCheck:
    return TrapCheck(trap_id=trap_id, status="pass", passed=True, message=message)


def _fail(trap_id: str, step: str | None, message: str) -> TrapCheck:
    return TrapCheck(trap_id=trap_id, status="fail", passed=False, offending_step=step, message=message)


def _advisory_only(trap_id: str, note: str) -> TrapCheck:
    return TrapCheck(trap_id=trap_id, status="pass", passed=True, message="numeric checks passed", advisory=note)


def _all_values(trace: SolutionTrace) -> list[tuple[str, dict[str, Any]]]:
    rows = [(s.id, {**s.values}) for s in trace.steps]
    if trace.final:
        rows.append(("final", dict(trace.final)))
    return rows


def _text_blob(trace: SolutionTrace) -> str:
    parts = [s.text for s in trace.steps]
    parts.append(str(trace.final.get("text") or ""))
    return "\n".join(parts)


def _rel_close(got: float, expected: float, tol: float = _NUM_TOL_REL) -> bool:
    return abs(got - expected) <= tol * max(1.0, abs(expected))


def _struct_solver(vals: dict[str, Any]) -> str | None:
    raw = vals.get("solver_used") or vals.get("integrator")
    return str(raw).lower() if raw is not None else None


def _bare_delta_cr_deg(case) -> float:
    d0 = math.asin(case.pm_pu / case.pmax_pre_pu)
    bump = (case.pm_pu / max(case.pmax_post_pu - case.pm_pu, 1e-9)) * (math.pi - d0)
    return math.degrees(d0 + bump)


def detect_t1(trace: SolutionTrace) -> TrapCheck:
    givens = merged_givens(trace)
    case = smib_case_from_givens(givens)
    if case is None:
        return _uncheck("T1")
    expected = math.degrees(critical_clearing_angle(case))
    bare = _bare_delta_cr_deg(case)
    for sid, vals in _all_values(trace):
        if vals.get("used_single_pmax_equal_area") is True:
            return _fail("T1", sid, "Staged Pmax ignored (single-parabola shortcut)")
        d = vals.get("delta_cr_deg")
        if d is not None:
            got = float(d)
            if _rel_close(got, bare, 0.01) and not _rel_close(got, expected, 0.01):
                return _fail("T1", sid, "δ_cr matches bolted-fault shortcut, not staged equal-area")
            if not _rel_close(got, expected, 0.02):
                return _fail("T1", sid, f"δ_cr {got}° off engine {expected:.4f}° for stated givens")
            return _pass("T1")
    return _uncheck("T1", "no δ_cr claim to verify")


def detect_t2(trace: SolutionTrace) -> TrapCheck:
    givens = merged_givens(trace)
    case = smib_case_from_givens(givens)
    if case is None:
        return _uncheck("T2")
    adv = find_advisory(_text_blob(trace), _ADV_ODE)
    for sid, vals in _all_values(trace):
        solver = _struct_solver(vals)
        if solver in _FORBIDDEN_SOLVER:
            return _fail("T2", sid, f"Forbidden solver {solver} (structural)")
    h_s = givens.get("h_s")
    if h_s is None:
        return _uncheck("T2", "missing h_s for CCT reference")
    try:
        dcr = critical_clearing_angle(case)
        ref_t = time_to_angle_during_fault(case, dcr, h_s=float(h_s))
    except (TypeError, ValueError):
        return _uncheck("T2")
    if ref_t is None:
        return _uncheck("T2")
    for sid, vals in _all_values(trace):
        t = vals.get("t_to_dcr_s") or vals.get("cct_s") or vals.get("tc_s")
        if t is not None:
            if not _rel_close(float(t), float(ref_t), 0.05):
                return _fail("T2", sid, f"CCT {t} s off engine {ref_t:.6f} s for givens")
            if adv:
                return _advisory_only("T2", f"text cue (non-fatal): {adv}")
            return _pass("T2")
    if adv:
        return _advisory_only("T2", f"text cue only (no numeric CCT): {adv}")
    return _uncheck("T2", "no CCT claim to verify")


def detect_t3(trace: SolutionTrace) -> TrapCheck:
    givens = merged_givens(trace)
    case = smib_case_from_givens(givens)
    if case is None:
        return _uncheck("T3")
    expected = case.accel_coeff()
    for sid, vals in _all_values(trace):
        acc = vals.get("accel_coeff")
        if acc is not None:
            if not _rel_close(float(acc), expected, 1e-3):
                return _fail("T3", sid, "accel_coeff does not match π f0 / H for givens")
            return _pass("T3")
        if vals.get("used_m_instead_of_h") is True:
            return _fail("T3", sid, "M used instead of H in swing equation")
    return _uncheck("T3", "no accel_coeff claim to verify")


def detect_t4(trace: SolutionTrace) -> TrapCheck:
    givens = merged_givens(trace)
    case = agc_case_from_givens({**givens, "k": 0.0})
    if case is None:
        return _uncheck("T4")
    sim = simulate_two_area(case, run="primary")
    exp_df = float(sim["steady"]["df1_hz"])
    exp_p12 = float(sim["steady"]["P12_MW"])
    adv = find_advisory(_text_blob(trace), re.compile(r"ACE\s*=\s*B\s*\*\s*Δf", re.IGNORECASE))
    for sid, vals in _all_values(trace):
        if vals.get("wrong_ace_sign") is True:
            return _fail("T4", sid, "ACE / tie sign inconsistent with two-area model")
        if vals.get("bias_b_equals_inv_r_only") is True:
            return _fail("T4", sid, "B treated as 1/R only")
    df = trace.final.get("delta_f1_hz")
    dp = trace.final.get("delta_p12_mw")
    if df is not None and not _rel_close(float(df), exp_df, 0.08):
        return _fail("T4", "final", f"Δf1 {df} Hz off engine {exp_df:.4f} Hz")
    if dp is not None and not _rel_close(float(dp), exp_p12, 0.08):
        return _fail("T4", "final", f"ΔP12 {dp} MW off engine {exp_p12:.4f} MW")
    if df is not None or dp is not None:
        if adv:
            return _advisory_only("T4", adv)
        return _pass("T4")
    return _uncheck("T4", "no primary steady claims to verify")


def detect_t5(trace: SolutionTrace) -> TrapCheck:
    givens = merged_givens(trace)
    case = agc_case_from_givens({**givens, "k": float(givens.get("k", 0.3) or 0.3)})
    if case is None:
        return _uncheck("T5")
    sim = simulate_two_area(case, run="agc")
    exp_dip = float(sim["first_dip"]["f1_Hz"])
    if trace.final.get("agc_removes_first_dip") is True:
        return _fail("T5", "final", "AGC cannot remove the first frequency dip")
    dip = trace.final.get("first_dip_delta_f1_hz")
    if dip is not None:
        if abs(float(dip)) < 0.05 and abs(exp_dip) > 0.1:
            return _fail("T5", "final", "Reported first dip ≈0 but engine shows initial dip")
        return _pass("T5")
    adv = find_advisory(_text_blob(trace), _ADV_AGC_DIP)
    if adv:
        return _advisory_only("T5", f"text cue only: {adv}")
    return _uncheck("T5", "no first-dip claim to verify")


def detect_t6(trace: SolutionTrace) -> TrapCheck:
    givens = merged_givens(trace)
    case = ed_case_from_givens(givens)
    pd = pd_mw_from_givens(givens)
    if case is None or pd is None:
        return _uncheck("T6")
    ref = solve_lambda_ed(case, float(pd))
    adv = find_advisory(_text_blob(trace), _ADV_IGNORE_LIMITS)
    for sid, vals in _all_values(trace):
        if vals.get("ignore_limits") is True:
            return _fail("T6", sid, "Limits ignored in dispatch (structural)")
        lam = vals.get("lambda") or vals.get("lam")
        if lam is not None and not _rel_close(float(lam), float(ref["lam"]), 0.03):
            return _fail("T6", sid, f"λ={lam} off engine {ref['lam']:.4f} for givens")
        p_claim = vals.get("P_mw") or vals.get("P")
        if isinstance(p_claim, list) and len(p_claim) == len(ref["P"]):
            for i, (got, exp) in enumerate(zip(p_claim, ref["P"], strict=True)):
                if got is not None and not _rel_close(float(got), float(exp), 0.02):
                    return _fail("T6", sid, f"P[{i}]={got} MW off engine {exp:.4f} MW")
            if adv:
                return _advisory_only("T6", f"text cue (non-fatal): {adv}")
            return _pass("T6")
        for i in range(len(ref["P"])):
            key = f"P{i}_mw"
            alt = f"P_{i}"
            got = vals.get(key) or vals.get(alt)
            if got is not None and not _rel_close(float(got), float(ref["P"][i]), 0.02):
                return _fail("T6", sid, f"{key}={got} off engine {ref['P'][i]:.4f}")
    if adv:
        return _advisory_only("T6", f"text cue only: {adv}")
    return _uncheck("T6", "no dispatch numerics to verify")


def detect_t7(trace: SolutionTrace) -> TrapCheck:
    for sid, vals in _all_values(trace):
        if vals.get("ic_fuel_units_wrong") is True:
            return _fail("T7", sid, "IC reported in wrong fuel-cost units")
    return _uncheck("T7", "no IC unit claim to verify")


def detect_t9(trace: SolutionTrace) -> TrapCheck:
    for sid, vals in _all_values(trace):
        solver = _struct_solver(vals)
        if solver in _FORBIDDEN_SOLVER:
            return _fail("T9", sid, f"Black-box solver {solver} when analytic path required")
    adv = find_advisory(_text_blob(trace), _ADV_ODE)
    if adv:
        return _advisory_only("T9", f"text cue only: {adv}")
    return _uncheck("T9", "no solver claim to verify")


def detect_t10(trace: SolutionTrace) -> TrapCheck:
    givens = merged_givens(trace)
    case = smib_case_from_givens(givens)
    if case is None:
        return _uncheck("T10")
    for sid, vals in _all_values(trace):
        if vals.get("used_defaults") and not vals.get("defaults_documented"):
            return _fail("T10", sid, "Silent defaults without documenting Pm/Pmax stages")
        pm = vals.get("pm_pu")
        if pm is not None and not _rel_close(float(pm), case.pm_pu, 1e-4):
            return _fail("T10", sid, "pm_pu in trace disagrees with stated givens")
    return _pass("T10")


DETECTORS: dict[str, Detector] = {
    "T1": detect_t1,
    "T2": detect_t2,
    "T3": detect_t3,
    "T4": detect_t4,
    "T5": detect_t5,
    "T6": detect_t6,
    "T7": detect_t7,
    "T9": detect_t9,
    "T10": detect_t10,
}


def infer_trap_ids(trace: SolutionTrace) -> tuple[str, ...]:
    if trace.trap_ids:
        return trace.trap_ids
    domain = str(merged_givens(trace).get("domain") or "").lower()
    by_domain = {
        "smib": ("T1", "T2", "T3", "T10"),
        "agc": ("T4", "T5"),
        "ed": ("T6", "T7"),
        "integration": ("T9",),
    }
    return by_domain.get(domain, ())
