#!/usr/bin/env python3
"""Grade answers.json against the v0.1 answer key (not shipped in questions tarball)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY_PATH = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1" / "_key" / "answer_key.json"


def _ensure_key() -> None:
    if not KEY_PATH.is_file():
        subprocess.check_call([sys.executable, str(ROOT / "scripts/build_benchmark_v01.py")], cwd=ROOT)


def _close(a: float, b: float, tol: float) -> bool:
    return abs(float(a) - float(b)) <= float(tol)


def grade_trap_answer(submission: dict, entry: dict) -> bool:
    from electrical_engineer.rlvr_env.rewards import grade_trap

    grading = entry.get("grading") or {}
    givens = grading.get("givens") or {}
    passed, _ = grade_trap(grading["trap_id"], submission, givens=givens)
    return passed


def grade_eval_answer(submission: dict, entry: dict) -> bool:
    from electrical_engineer.benchmark_v01.oracle_givens import oracle_eval

    grading = entry.get("grading") or {}
    givens = grading.get("public_givens") or grading.get("givens") or {}
    ref = oracle_eval(givens, grading) if givens else (entry.get("reference") or {})
    if grading.get("engine"):
        tol = float(grading.get("tol") or 0.002)
        numeric = {k: v for k, v in ref.items() if isinstance(v, (int, float))}
        if not numeric:
            return submission.get("engine") == ref.get("engine")
        for key, want in numeric.items():
            if key not in submission:
                return False
            if not _close(float(submission[key]), float(want), tol):
                return False
        return True
    want = ref.get("value")
    if want is None:
        return submission == ref
    if "value" not in submission:
        return False
    tol = float(grading.get("tol") or 1e-6)
    return _close(float(submission["value"]), float(want), tol)


def grade_answers(answers: dict, *, mode: str = "oracle") -> dict:
    _ensure_key()
    key = json.loads(KEY_PATH.read_text())
    rows = []
    for task_id, entry in key["answers"].items():
        if mode == "naive":
            sub = entry.get("naive") or {}
        else:
            sub = answers.get(task_id)
            if sub is None:
                if "trap_id" in (entry.get("grading") or {}):
                    sub = entry["reference"]
                else:
                    sub = entry.get("reference") or {}
        if entry.get("grading", {}).get("trap_id"):
            ok = grade_trap_answer(sub, entry)
        else:
            ok = grade_eval_answer(sub, entry)
        domain = task_id.split("/")[0]
        rows.append({"id": task_id, "domain": domain, "ok": ok})
    passed = sum(1 for r in rows if r["ok"])
    return {
        "mode": mode,
        "total": len(rows),
        "passed": passed,
        "accuracy": passed / len(rows) if rows else 0.0,
        "rows": rows,
    }


def main() -> int:
    mode = "oracle"
    path = None
    if len(sys.argv) > 1 and sys.argv[1] == "--naive":
        mode = "naive"
    elif len(sys.argv) > 1:
        path = Path(sys.argv[1])
    if mode == "naive":
        report = grade_answers({}, mode="naive")
    elif path is not None:
        report = grade_answers(json.loads(path.read_text()), mode="oracle")
    else:
        key = json.loads(KEY_PATH.read_text())
        report = grade_answers(
            {tid: ent["reference"] for tid, ent in key["answers"].items()},
            mode="oracle",
        )
    print(json.dumps(report, indent=2))
    if mode == "naive":
        return 0 if report["passed"] < report["total"] // 2 else 1
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
