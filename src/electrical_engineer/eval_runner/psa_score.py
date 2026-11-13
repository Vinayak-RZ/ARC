"""Score engine-mode gold items (EEC-301 PSA trilogy). Schema v2."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area
from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed
from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_time_bisection,
    eec301_reference,
    time_to_angle_during_fault,
)


def _close(a: float, b: float, tol: float) -> bool:
    return abs(float(a) - float(b)) <= float(tol)


def _fixture_case(item: Path) -> dict[str, Any]:
    path = item / "fixtures" / "case.json"
    if path.is_file():
        return json.loads(path.read_text())
    return {}


def score_smib(expect: dict[str, Any], item: Path) -> dict[str, Any]:
    case = SmibCase(**_fixture_case(item))
    ref = eec301_reference(case)
    tol_deg = float(expect.get("tolerance_deg", 1e-6))
    tol_t = float(expect.get("tolerance_tcr_s", 0.002))
    tol_t_to = float(expect.get("tolerance_t_to_s", tol_t))
    ok = _close(ref["delta0_deg"], expect["delta0_deg"], tol_deg)
    ok = ok and _close(ref["delta_cr_deg"], expect["delta_cr_deg"], tol_deg)
    t_kernel = critical_clearing_time_bisection(case, h_s=0.001, tol_s=1e-6, t_hi=0.35)
    ok = ok and _close(t_kernel, expect["tcr_s"], tol_t)
    delta_cr_rad = math.radians(ref["delta_cr_deg"])
    t_at = time_to_angle_during_fault(case, delta_cr_rad, h_s=0.001, integrator="rk4")
    ok = ok and t_at is not None
    if t_at is not None:
        ok = ok and _close(t_at, expect["t_to_delta_cr_s"], tol_t_to)
    summary = {
        "engine": "smib_swing",
        "recipe_id": expect.get("recipe_id"),
        "schema": expect.get("schema", "arc.eval.expect.v2"),
        "delta0_deg": ref["delta0_deg"],
        "delta_cr_deg": ref["delta_cr_deg"],
        "tcr_s": t_kernel,
        "t_to_delta_cr_s": t_at,
        "golden_file": expect.get("golden_file"),
    }
    return {"ok": bool(ok), "summary": summary, "expect": expect}


def score_agc(expect: dict[str, Any]) -> dict[str, Any]:
    case = TwoAreaAgcCase.eec301_default()
    primary = simulate_two_area(case, run="primary", t_end_s=30.0)["steady"]
    agc = simulate_two_area(case.with_k(0.3), run="agc", t_end_s=60.0)["steady"]
    div = simulate_two_area(case.with_k(float(expect.get("K_diverges", 1.0))), run="agc", t_end_s=60.0)
    ok = _close(primary["df1_hz"], expect["primary_df1_Hz"], 0.002)
    ok = ok and _close(primary["P12_MW"], expect["primary_P12_MW"], 0.5)
    ok = ok and _close(agc["df1_hz"], expect["agc_ss_df1_Hz"], 1e-4)
    ok = ok and _close(agc["Pm1_MW"], expect["agc_ss_Pm1_MW"], 0.05)
    ok = ok and bool(div.get("diverged"))
    summary = {
        "engine": "agc_two_area",
        "recipe_id": expect.get("recipe_id"),
        "schema": expect.get("schema", "arc.eval.expect.v2"),
        "primary_df1_Hz": primary["df1_hz"],
        "primary_P12_MW": primary["P12_MW"],
        "agc_ss_df1_Hz": agc["df1_hz"],
        "agc_ss_Pm1_MW": agc["Pm1_MW"],
        "diverged_at_K": div.get("diverged"),
    }
    return {"ok": bool(ok), "summary": summary, "expect": expect}


def score_ed(expect: dict[str, Any]) -> dict[str, Any]:
    case = EdCase.eec301_default()
    ok = True
    rows: list[dict[str, Any]] = []
    for key in expect.get("cases") or []:
        pd = float(str(key).removeprefix("PD_"))
        r = solve_lambda_ed(case, pd)
        rows.append({"case": key, "lam": r["lam"], "P": r["P"], "status": r["status"]})
    if "PD_500" in (expect.get("cases") or []):
        r500 = solve_lambda_ed(case, 500.0)
        want_bind = bool(expect.get("unit2_binds_at_PD_500"))
        ok = (r500["status"][1] == "at_max") == want_bind
        if want_bind:
            ok = ok and _close(r500["P"][1], 150.0, 1e-6)
    summary = {
        "engine": "ed_lambda",
        "recipe_id": expect.get("recipe_id"),
        "schema": expect.get("schema", "arc.eval.expect.v2"),
        "cases": rows,
    }
    return {"ok": bool(ok), "summary": summary, "expect": expect}


def run_psa_item(item: Path, expect: dict[str, Any]) -> dict[str, Any]:
    engine = str(expect.get("engine") or "")
    if engine == "smib_swing":
        scored = score_smib(expect, item)
    elif engine == "agc_two_area":
        scored = score_agc(expect)
    elif engine == "ed_lambda":
        scored = score_ed(expect)
    else:
        scored = {
            "ok": False,
            "summary": {"error": f"unknown engine {engine!r}"},
            "expect": expect,
        }
    scored["item"] = str(item)
    scored["run_id"] = None
    return scored
