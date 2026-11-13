#!/usr/bin/env python3
"""Grade a frontier A/B answers dict against REFERENCE.json."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "artifacts/frontier-ab/live-run-2026-11-13/grading/REFERENCE.json"


def _flatten_answers(raw: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for pk, block in raw.items():
        if not pk.startswith("P"):
            continue
        if "answers" in block:
            out[pk] = block["answers"]
        else:
            out[pk] = block
    return out


def _qty_map() -> dict[str, dict[str, str]]:
    return {
        "P1": {
            "delta0_deg": "delta0_deg",
            "delta_cr_deg": "delta_cr_deg",
            "t_cr_s": "t_cr_s",
        },
        "P2": {
            "stable": "stable",
            "max_rotor_angle_deg": "max_rotor_angle_deg",
        },
        "P3": {
            "P1_MW": "P1_MW",
            "P2_MW": "P2_MW",
            "P3_MW": "P3_MW",
            "lambda_Rs_per_MWh": "lambda_Rs_per_MWh",
        },
        "P4": {
            "steady_state_frequency_deviation_Hz": "steady_state_frequency_deviation_Hz",
            "Delta_P12_MW": "Delta_P12_MW",
        },
        "P5": {
            "gain_crossover_rad_s": "gain_crossover_rad_per_s",
            "phase_margin_deg": "phase_margin_deg",
            "phase_crossover_rad_s": "phase_crossover_rad_per_s",
            "gain_margin_dB": "gain_margin_dB",
        },
        "P6": {
            "damping_type": "damping_type",
            "Vc_peak_V": "Vc_peak_V",
            "t_Vc_peak_s": "t_Vc_peak_s",
            "settling_time_2pct_s": "settling_time_2pct_s",
        },
        "P7": {
            "I_fault_pu": "I_fault_pu",
            "I_fault_kA": "I_fault_kA",
        },
        "P8": {
            "rotor_speed_rpm": "rotor_speed_rpm",
            "stator_current_A": "stator_current_A",
            "developed_torque_Nm": "developed_torque_Nm",
            "slip_at_max_torque": "slip_at_max_torque",
        },
    }


def _aliases(sub: dict[str, Any]) -> dict[str, Any]:
    s = dict(sub)
    if "fault_current_pu" in s:
        s["I_fault_pu"] = s["fault_current_pu"]
    if "fault_current_kA" in s:
        s["I_fault_kA"] = s["fault_current_kA"]
    if "damping" in s and "damping_type" not in s:
        s["damping_type"] = s["damping"]
    if "max_delta_deg" in s:
        s["max_rotor_angle_deg"] = s["max_delta_deg"]
    if "df_hz" in s:
        s["steady_state_frequency_deviation_Hz"] = s["df_hz"]
    if "dP12_MW" in s:
        s["Delta_P12_MW"] = s["dP12_MW"]
    return s


def _close(a: Any, b: Any, *, rtol: float = 0.002, atol: float = 0.02) -> bool:
    if a is None or b is None:
        return False
    if isinstance(b, bool):
        return bool(a) == b
    if isinstance(b, str):
        return str(a).lower() == str(b).lower()
    return abs(float(a) - float(b)) <= max(atol, rtol * abs(float(b)))


def grade(submission: dict[str, Any], ref: dict[str, Any]) -> dict[str, Any]:
    flat = {k: _aliases(v) for k, v in _flatten_answers(submission).items()}
    problems: dict[str, Any] = {}
    qty_pass = 0
    qty_total = 0
    for pk, keys in _qty_map().items():
        ref_q = ref[pk]["reference"]
        sub_q = flat.get(pk, {})
        row: dict[str, Any] = {}
        passed = 0
        total = 0
        for out_key, ref_key in keys.items():
            total += 1
            qty_total += 1
            rv = ref_q[ref_key]
            sv = sub_q.get(out_key, sub_q.get(ref_key))
            ok = _close(sv, rv)
            if ok:
                passed += 1
                qty_pass += 1
            row[ref_key] = {"pass": ok, "submitted": sv, "reference": rv}
        problems[pk] = {**row, "fraction": passed / total if total else 0, "full_credit": passed == total}
    return {
        "quantity_pass": qty_pass,
        "quantity_total": qty_total,
        "total_fraction": qty_pass / qty_total if qty_total else 0,
        "problems": problems,
    }


def main() -> int:
    ref = json.loads(REF.read_text())
    sub_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "artifacts/frontier-ab/live-run-2026-11-13/arc-rerun/answers.json"
    submission = json.loads(sub_path.read_text())
    out = grade(submission, ref)
    out["submission"] = sub_path.stem
    print(json.dumps(out, indent=2))
    out_path = sub_path.parent / "SCORES.json"
    out_path.write_text(json.dumps(out, indent=2))
    return 0 if out["quantity_pass"] == out["quantity_total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
