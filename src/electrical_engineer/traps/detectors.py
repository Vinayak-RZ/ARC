"""Per-trap detectors on a solution trace (process PRM)."""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from typing import Any

from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed
from electrical_engineer.engines.eec301_goldens import load_exp06_golden, load_exp07_golden
from electrical_engineer.engines.smib_swing import SmibCase, critical_clearing_angle
from electrical_engineer.traps.schema import SolutionTrace, TrapCheck

Detector = Callable[[SolutionTrace], TrapCheck | None]

_FORBIDDEN_ODE = re.compile(r"\bode45\b|\bfmincon\b", re.IGNORECASE)
_WRONG_ACE = re.compile(r"ACE\s*=\s*B\s*\*\s*Δf\s*[-−]\s*ΔP", re.IGNORECASE)
_B_IS_R_INV_ONLY = re.compile(r"B\s*=\s*1\s*/\s*R\b", re.IGNORECASE)
_AGC_ZERO_DIP = re.compile(r"(AGC|secondary).{0,40}(remove|eliminate|zero).{0,20}(first\s*dip|initial\s*dip)", re.IGNORECASE)
_IGNORE_LIMITS = re.compile(r"ignore\s+(limits|pmax|p_min|pmax)", re.IGNORECASE)
_SINGLE_PMAX = re.compile(r"Pmax\s*=\s*1\.5|single\s+Pmax|bolt(?:ed)?\s+fault.*Pmax\s*=\s*0", re.IGNORECASE)
_H_M_SWAP = re.compile(r"M\s*=\s*H\s*/\s*2π|ω\s*=\s*2π\s*f0.*accel|accel.*M\s*instead\s+of\s+H", re.IGNORECASE)
_IC_UNIT = re.compile(r"IC\s*=\s*dC/dP\s*\$|fuel\s+in\s+\$/h\b", re.IGNORECASE)


def _fail(trap_id: str, step: str | None, message: str) -> TrapCheck:
    return TrapCheck(trap_id=trap_id, passed=False, offending_step=step, message=message)


def _pass(trap_id: str) -> TrapCheck:
    return TrapCheck(trap_id=trap_id, passed=True)


def _text_blob(trace: SolutionTrace) -> str:
    parts = [s.text for s in trace.steps]
    parts.append(str(trace.final.get("text") or ""))
    return "\n".join(parts)


def _step_values(trace: SolutionTrace) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = [(s.id, dict(s.values)) for s in trace.steps]
    if trace.final:
        rows.append(("final", dict(trace.final)))
    return rows


def detect_t1(trace: SolutionTrace) -> TrapCheck | None:
    gold = load_exp06_golden()["equal_area"]["delta_cr_deg"]
    arc = math.degrees(critical_clearing_angle(SmibCase()))
    blob = _text_blob(trace)
    if _SINGLE_PMAX.search(blob):
        return _fail("T1", trace.steps[0].id if trace.steps else "final", "Used single-stage Pmax for clearing (T1)")
    for sid, vals in _step_values(trace):
        d = vals.get("delta_cr_deg")
        if d is not None and abs(float(d) - gold) > 5.0:
            return _fail("T1", sid, f"δ_cr {d}° off golden {gold}° (equal-area stage error)")
    final_d = trace.final.get("delta_cr_deg")
    if final_d is not None and abs(float(final_d) - arc) > 0.05:
        bare_parabola = math.degrees(
            math.asin(SmibCase().pm_pu / SmibCase().pmax_pre_pu)
            + (SmibCase().pm_pu / (SmibCase().pmax_post_pu - SmibCase().pm_pu)) * math.pi
        )
        if abs(float(final_d) - bare_parabola) < 1.0:
            return _fail("T1", "final", "Bolted-fault Pmax=0 parabola used for δ_cr")
    return _pass("T1")


def detect_t2(trace: SolutionTrace) -> TrapCheck | None:
    blob = _text_blob(trace)
    if _FORBIDDEN_ODE.search(blob):
        sid = next((s.id for s in trace.steps if _FORBIDDEN_ODE.search(s.text)), "final")
        return _fail("T2", sid, "Forbidden solver ode45/fmincon for CCT (T2)")
    gold_t = load_exp06_golden()["time_to_delta_cr"]["t_to_dcr"]
    for sid, vals in _step_values(trace):
        t = vals.get("t_to_dcr_s") or vals.get("cct_s") or vals.get("tc_s")
        if t is not None and abs(float(t) - gold_t) > 0.02:
            return _fail("T2", sid, f"CCT/grid step {t} s off lab bisection {gold_t} s")
    return _pass("T2")


def detect_t3(trace: SolutionTrace) -> TrapCheck | None:
    if _H_M_SWAP.search(_text_blob(trace)):
        sid = next((s.id for s in trace.steps if _H_M_SWAP.search(s.text)), "final")
        return _fail("T3", sid, "H↔M or f↔ω base mixup in swing/AGC setup")
    case = SmibCase()
    for sid, vals in _step_values(trace):
        acc = vals.get("accel_coeff")
        if acc is not None and abs(float(acc) - case.accel_coeff()) > 1e-6:
            return _fail("T3", sid, "Swing accel coefficient does not match πf/H on system base")
    return _pass("T3")


def detect_t4(trace: SolutionTrace) -> TrapCheck | None:
    blob = _text_blob(trace)
    if _WRONG_ACE.search(blob) or _B_IS_R_INV_ONLY.search(blob):
        sid = next(
            (s.id for s in trace.steps if _WRONG_ACE.search(s.text) or _B_IS_R_INV_ONLY.search(s.text)),
            "final",
        )
        return _fail("T4", sid, "Wrong ACE sign or B=1/R only (T4)")
    gold = load_exp07_golden()["primary_steady"]
    df = trace.final.get("delta_f1_hz") or trace.final.get("steady_delta_f_hz")
    dp = trace.final.get("delta_p12_mw")
    if df is not None and abs(float(df) - gold["delta_f1_hz"]) > 0.05:
        return _fail("T4", "final", f"Primary steady Δf1 {df} Hz vs golden {gold['delta_f1_hz']}")
    if dp is not None and abs(float(dp) - gold["delta_p12_mw"]) > 2.0:
        return _fail("T4", "final", f"Tie flow ΔP12 {dp} MW vs golden {gold['delta_p12_mw']}")
    return _pass("T4")


def detect_t5(trace: SolutionTrace) -> TrapCheck | None:
    if _AGC_ZERO_DIP.search(_text_blob(trace)):
        return _fail("T5", "final", "Claims AGC removes the first frequency dip (T5)")
    claimed = trace.final.get("agc_removes_first_dip")
    if claimed is True:
        return _fail("T5", "final", "AGC cannot remove the first dip; only recenters steady state")
    if trace.final.get("first_dip_delta_f1_hz") is not None:
        v = float(trace.final["first_dip_delta_f1_hz"])
        if abs(v) < 0.05:
            return _fail("T5", "final", "Reported first dip ≈0 under AGC (lab shows large initial dip)")
    return _pass("T5")


def detect_t6(trace: SolutionTrace) -> TrapCheck | None:
    if _IGNORE_LIMITS.search(_text_blob(trace)):
        sid = next((s.id for s in trace.steps if _IGNORE_LIMITS.search(s.text)), "final")
        return _fail("T6", sid, "Ignored generator limits in λ-ED (T6)")
    r = solve_lambda_ed(EdCase.eec301_default(), 500.0)
    for sid, vals in _step_values(trace):
        p2 = vals.get("P2_mw") or vals.get("P_2")
        if p2 is not None and float(p2) > 150.5:
            return _fail("T6", sid, f"P2={p2} MW exceeds 150 MW limit")
        lam = vals.get("lambda") or vals.get("lam")
        if lam is not None and abs(float(lam) - r["lam"]) > 0.5:
            return _fail("T6", sid, f"λ={lam} wrong with limits active (golden λ≈{r['lam']})")
    p2_final = trace.final.get("P2_mw")
    if p2_final is not None and float(p2_final) != 150.0:
        return _fail("T6", "final", "Unit 2 not at Pmax=150 MW with PD=500")
    return _pass("T6")


def detect_t7(trace: SolutionTrace) -> TrapCheck | None:
    if _IC_UNIT.search(_text_blob(trace)):
        sid = next((s.id for s in trace.steps if _IC_UNIT.search(s.text)), "final")
        return _fail("T7", sid, "Wrong IC/fuel units in ED (T7)")
    return _pass("T7")


def detect_t9(trace: SolutionTrace) -> TrapCheck | None:
    if _FORBIDDEN_ODE.search(_text_blob(trace)):
        sid = next((s.id for s in trace.steps if _FORBIDDEN_ODE.search(s.text)), "final")
        return _fail("T9", sid, "Used forbidden black-box solver when analytic path required")
    return _pass("T9")


def detect_t10(trace: SolutionTrace) -> TrapCheck | None:
    for sid, vals in _step_values(trace):
        pm = vals.get("pm_pu")
        if pm is not None and abs(float(pm) - SmibCase().pm_pu) > 0.01:
            return _fail("T10", sid, "Silent wrong default Pm_pu")
        if vals.get("used_defaults") and not vals.get("defaults_documented"):
            return _fail("T10", sid, "Silent defaults without stating Pm/Pmax stages")
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
    topic = trace.topic.lower()
    topic_map = {
        "smib": ("T1", "T2", "T3", "T10"),
        "agc": ("T4", "T5"),
        "ed": ("T6", "T7"),
        "integration": ("T9",),
    }
    for key, ids in topic_map.items():
        if key in topic:
            return ids
    blob = _text_blob(trace).lower()
    picks: list[str] = []
    if "smib" in blob or "clearing" in blob or "equal-area" in blob:
        picks.extend(["T1", "T2", "T3"])
    if "agc" in blob or "two-area" in blob or "ace" in blob:
        picks.extend(["T4", "T5"])
    if "economic dispatch" in blob or "lambda" in blob or " ed " in f" {blob} ":
        picks.extend(["T6", "T7"])
    return tuple(dict.fromkeys(picks))
