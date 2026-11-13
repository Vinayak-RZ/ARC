"""Trap ablation: outcome-only vs process verifier on fixture traces."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.traps.index import automated_trap_ids
from electrical_engineer.traps.schema import SolutionTrace
from electrical_engineer.traps.verify import grade_outcome_only, grade_with_verifier

FIXTURES = Path(__file__).resolve().parents[3] / "eval/fixtures/trap_prm/traces.json"


def load_ablation_cases() -> list[dict[str, Any]]:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return list(data.get("cases") or [])


def run_ablation() -> dict[str, Any]:
    cases = load_ablation_cases()
    without_pass = 0
    with_pass = 0
    caught = 0
    bare_process_fail = 0
    rows: list[dict[str, Any]] = []
    for case in cases:
        trace = SolutionTrace.from_mapping(case.get("trace") or {})
        outcome = grade_outcome_only(trace)
        full = grade_with_verifier(trace)
        if outcome.outcome_pass:
            without_pass += 1
        if full.outcome_pass and full.process_pass:
            with_pass += 1
        if not full.process_pass and outcome.outcome_pass:
            caught += 1
        if case.get("label") == "bare_trap" and not full.process_pass:
            bare_process_fail += 1
        rows.append(
            {
                "case_id": case.get("id"),
                "label": case.get("label"),
                "outcome_only_pass": outcome.outcome_pass,
                "with_verifier_pass": full.outcome_pass and full.process_pass,
                "failed_traps": [c.trap_id for c in full.checks if not c.passed],
            }
        )
    n = len(cases) or 1
    return {
        "cases": n,
        "outcome_only_pass_rate": round(without_pass / n, 4),
        "with_verifier_pass_rate": round(with_pass / n, 4),
        "traps_caught_with_good_outcome": caught,
        "bare_labeled_process_failures": bare_process_fail,
        "rows": rows,
    }


def contract_payload() -> dict[str, Any]:
    ablation = run_ablation()
    return {
        "traps_automated": automated_trap_ids(),
        "hook_contract_path": "docs/hosts/trap_hooks.md",
        "ablation": ablation,
    }
