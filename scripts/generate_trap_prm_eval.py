#!/usr/bin/env python3
"""Generate trap PRM eval traces from engines only (independent of detector logic)."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area
from electrical_engineer.engines.ed_lambda import EdCase, EdUnit, solve_lambda_ed
from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_angle,
    time_to_angle_during_fault,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "eval/fixtures/trap_prm/eval_traces.json"
RNG = random.Random(20261113)


def _smib_givens() -> dict:
    pm = round(RNG.uniform(0.7, 0.95), 3)
    pre = round(RNG.uniform(1.6, 2.2), 3)
    post = round(RNG.uniform(1.2, 1.7), 3)
    return {
        "domain": "smib",
        "h_mj_mva": round(RNG.uniform(4.0, 6.5), 3),
        "f0_hz": RNG.choice([50.0, 60.0]),
        "pm_pu": pm,
        "pmax_pre_pu": pre,
        "pmax_fault_pu": round(RNG.uniform(0.3, 0.7), 3),
        "pmax_post_pu": post,
        "h_s": round(RNG.choice([0.001, 0.01, 0.015]), 4),
    }


def _ed_givens() -> dict:
    n = 3
    units = []
    for _ in range(n):
        units.append(
            {
                "a": round(RNG.uniform(300, 600), 1),
                "b": round(RNG.uniform(4.5, 6.5), 2),
                "c": round(RNG.uniform(0.003, 0.012), 4),
                "pmin": round(RNG.uniform(20, 60), 1),
                "pmax": round(RNG.uniform(100, 320), 1),
            }
        )
    pd = round(RNG.uniform(0.85 * sum(u["pmax"] for u in units), 0.95 * sum(u["pmax"] for u in units)), 1)
    return {"domain": "ed", "pd_mw": pd, "units": units}


def main() -> int:
    cases: list[dict] = []

    for i in range(12):
        g = _smib_givens()
        case = SmibCase(**{k: g[k] for k in g if k not in ("domain", "h_s")})
        dcr = math.degrees(critical_clearing_angle(case))
        dcr_rad = critical_clearing_angle(case)
        t_ref = time_to_angle_during_fault(case, dcr_rad, h_s=float(g["h_s"]))
        cases.append(
            {
                "id": f"correct-smib-{i}",
                "expect": "correct",
                "trace": {
                    "trap_ids": ["T1", "T2", "T3"],
                    "givens": g,
                    "steps": [{"id": "eq", "text": "equal-area", "delta_cr_deg": dcr, "accel_coeff": case.accel_coeff()}],
                    "final": {"delta_cr_deg": dcr, "t_to_dcr_s": t_ref, "accel_coeff": case.accel_coeff()},
                },
            }
        )
        wrong_d = dcr + RNG.uniform(8, 15)
        cases.append(
            {
                "id": f"wrong-t1-smib-{i}",
                "expect": "wrong",
                "expect_fail_traps": ["T1"],
                "trace": {
                    "trap_ids": ["T1"],
                    "givens": g,
                    "final": {"delta_cr_deg": wrong_d, "used_single_pmax_equal_area": True},
                },
            }
        )

    for i in range(8):
        g = _ed_givens()
        case = EdCase(tuple(EdUnit(**u) for u in g["units"]))
        ref = solve_lambda_ed(case, float(g["pd_mw"]))
        cases.append(
            {
                "id": f"correct-ed-{i}",
                "expect": "correct",
                "trace": {
                    "trap_ids": ["T6"],
                    "givens": g,
                    "final": {"lambda": ref["lam"], "P_mw": ref["P"]},
                },
            }
        )
        bad_p = list(ref["P"])
        bad_p[1] = bad_p[1] + 30
        cases.append(
            {
                "id": f"wrong-t6-ed-{i}",
                "expect": "wrong",
                "expect_fail_traps": ["T6"],
                "trace": {
                    "trap_ids": ["T6"],
                    "givens": g,
                    "final": {"lambda": ref["lam"], "P_mw": bad_p, "ignore_limits": True},
                },
            }
        )

    for i in range(6):
        g = {"domain": "agc", "agc_preset": "eec301", "k": 0.3}
        case = TwoAreaAgcCase.eec301_default().with_k(0.0)
        prim = simulate_two_area(case, run="primary")
        agc = simulate_two_area(TwoAreaAgcCase.eec301_default().with_k(0.3), run="agc")
        cases.append(
            {
                "id": f"correct-agc-{i}",
                "expect": "correct",
                "trace": {
                    "trap_ids": ["T4", "T5"],
                    "givens": g,
                    "final": {
                        "delta_f1_hz": prim["steady"]["df1_hz"],
                        "delta_p12_mw": prim["steady"]["P12_MW"],
                        "first_dip_delta_f1_hz": agc["first_dip"]["f1_Hz"],
                        "text": "Note: AGC does not remove the first dip; we did not use ode45.",
                    },
                },
            }
        )
        cases.append(
            {
                "id": f"wrong-t5-agc-{i}",
                "expect": "wrong",
                "expect_fail_traps": ["T5"],
                "trace": {
                    "trap_ids": ["T5"],
                    "givens": g,
                    "final": {"agc_removes_first_dip": True, "first_dip_delta_f1_hz": 0.0},
                },
            }
        )

    for i in range(4):
        g = _smib_givens()
        case = SmibCase(**{k: g[k] for k in g if k not in ("domain", "h_s")})
        dcr = math.degrees(critical_clearing_angle(case))
        cases.append(
            {
                "id": f"negation-text-smib-{i}",
                "expect": "correct",
                "trace": {
                    "trap_ids": ["T2", "T9"],
                    "givens": g,
                    "steps": [{"id": "n", "text": "We did not use ode45; RK4 only."}],
                    "final": {"delta_cr_deg": dcr, "solver_used": "rk4"},
                },
            }
        )

    cases.append({"id": "empty-trace-0", "expect": "empty", "trace": {}})
    cases.append({"id": "empty-trace-1", "expect": "empty", "trace": {"final": {"text": ""}}})

    for i in range(3):
        g = _smib_givens()
        cases.append(
            {
                "id": f"wrong-t2-solver-{i}",
                "expect": "wrong",
                "expect_fail_traps": ["T2"],
                "trace": {
                    "trap_ids": ["T2"],
                    "givens": g,
                    "final": {"solver_used": "ode45", "text": "Integrated with ode45 for clearing."},
                },
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"schema": "arc.trap_prm.eval.v1", "cases": cases}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"written": str(OUT), "cases": len(cases)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
