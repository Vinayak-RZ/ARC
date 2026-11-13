"""Precision / recall / abstain metrics on labeled eval traces."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from electrical_engineer.traps.schema import SolutionTrace
from electrical_engineer.traps.verify import grade_trace, trace_has_substance

EVAL_PATH = Path(__file__).resolve().parents[3] / "eval/fixtures/trap_prm/eval_traces.json"


def load_eval_cases() -> list[dict[str, Any]]:
    return list(json.loads(EVAL_PATH.read_text(encoding="utf-8")).get("cases") or [])


def compute_eval_metrics() -> dict[str, Any]:
    cases = load_eval_cases()
    per_trap: dict[str, dict[str, int]] = defaultdict(
        lambda: {"tp": 0, "fp": 0, "fn": 0, "abstain": 0, "scored": 0}
    )
    n_correct = 0
    fp_on_correct = 0
    total_checks = 0
    abstain_checks = 0
    empty_unchecked = 0

    for case in cases:
        trace = SolutionTrace.from_mapping(case.get("trace") or {})
        expect = str(case.get("expect") or "correct")
        fail_traps = set(case.get("expect_fail_traps") or [])
        grades = grade_trace(trace)
        by_id = {c.trap_id: c for c in grades.checks}

        if expect == "empty" and grades.process_status != "unchecked":
            empty_unchecked += 1
        if expect == "correct":
            n_correct += 1

        for tid, check in by_id.items():
            total_checks += 1
            if check.status == "unchecked":
                abstain_checks += 1
                per_trap[tid]["abstain"] += 1
                continue
            per_trap[tid]["scored"] += 1
            failed = check.status == "fail"
            if expect == "correct":
                if failed:
                    per_trap[tid]["fp"] += 1
                    fp_on_correct += 1
                else:
                    per_trap[tid]["tp"] += 0  # tn counted implicitly
            elif expect == "wrong" and tid in fail_traps:
                if failed:
                    per_trap[tid]["tp"] += 1
                else:
                    per_trap[tid]["fn"] += 1

    trap_rows: dict[str, Any] = {}
    for tid, row in sorted(per_trap.items()):
        tp, fp, fn = row["tp"], row["fp"], row["fn"]
        prec = tp / (tp + fp) if (tp + fp) else None
        rec = tp / (tp + fn) if (tp + fn) else None
        trap_rows[tid] = {
            **row,
            "precision": round(prec, 4) if prec is not None else None,
            "recall": round(rec, 4) if rec is not None else None,
            "false_positive_rate_on_correct": round(fp / n_correct, 4) if n_correct else None,
        }

    return {
        "eval_cases": len(cases),
        "correct_cases": n_correct,
        "false_positives_on_correct": fp_on_correct,
        "false_positive_rate_on_correct": round(fp_on_correct / n_correct, 4) if n_correct else None,
        "abstain_rate": round(abstain_checks / total_checks, 4) if total_checks else None,
        "empty_not_unchecked": empty_unchecked,
        "per_trap": trap_rows,
        "substance_empty_count": sum(1 for c in cases if not trace_has_substance(SolutionTrace.from_mapping(c.get("trace") or {}))),
    }
