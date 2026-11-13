#!/usr/bin/env python3
"""Grade answers.json against the v0.1 benchmark answer key."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY_PATH = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1" / "_stage" / "answer_key.json"


def _ensure_key() -> None:
    if not KEY_PATH.is_file():
        subprocess.check_call([sys.executable, str(ROOT / "scripts/build_benchmark_v01.py")], cwd=ROOT)


def _close(a: float, b: float, tol: float) -> bool:
    return abs(float(a) - float(b)) <= float(tol)


def grade_item(item_id: str, submission: dict, entry: dict) -> bool:
    domain = entry.get("domain")
    if domain == "trap":
        from electrical_engineer.rlvr_env.rewards import grade_trap

        tid = entry["grading"]["trap_id"]
        passed, _ = grade_trap(tid, submission)
        return passed
    ref = entry.get("reference") or {}
    grading = entry.get("grading") or {}
    if grading.get("engine") == "smib_swing":
        tol_t = float(grading.get("tol") or 0.002)
        tol_deg = 0.01
        checks = []
        for key, tol in (
            ("delta0_deg", tol_deg),
            ("delta_cr_deg", tol_deg),
            ("tcr_s", tol_t),
            ("t_to_delta_cr_s", tol_t),
        ):
            if key in ref and key in submission:
                checks.append(_close(float(submission[key]), float(ref[key]), tol))
        return bool(checks) and all(checks)
    if grading.get("engine") in ("agc_two_area", "ed_lambda"):
        return submission.get("engine_ok") is True or ref == submission
    want = ref.get("value")
    if want is None:
        want = ref.get("recomputed", {}).get("value")
    if want is not None and "value" in submission:
        tol = float(grading.get("tol") or 1e-6)
        return _close(float(submission["value"]), float(want), tol)
    if "value" in ref and "value" not in submission:
        return False
    return submission.get("ok") is True or submission == ref


def grade_answers(answers: dict) -> dict:
    _ensure_key()
    key = json.loads(KEY_PATH.read_text())
    rows = []
    for item_id, entry in key["answers"].items():
        sub = answers.get(item_id)
        if sub is None:
            if item_id.startswith("trap/"):
                from electrical_engineer.rlvr_env.rewards import oracle_submission

                sub = oracle_submission(entry["grading"]["trap_id"])
            else:
                sub = entry.get("reference") or {}
        ok = grade_item(item_id, sub, entry)
        rows.append({"id": item_id, "domain": entry["domain"], "ok": ok})
    passed = sum(1 for r in rows if r["ok"])
    return {
        "total": len(rows),
        "passed": passed,
        "accuracy": passed / len(rows) if rows else 0.0,
        "rows": rows,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if path is not None:
        answers = json.loads(path.read_text())
    else:
        _ensure_key()
        key = json.loads(KEY_PATH.read_text())
        answers = {}
        for item_id, entry in key["answers"].items():
            if item_id.startswith("trap/"):
                from electrical_engineer.rlvr_env.rewards import oracle_submission

                answers[item_id] = oracle_submission(entry["grading"]["trap_id"])
            else:
                ref = entry.get("reference") or {}
                if "value" in ref:
                    answers[item_id] = {"value": ref["value"]}
                else:
                    answers[item_id] = {**ref, "engine_ok": entry.get("oracle_ok")}
    report = grade_answers(answers)
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
