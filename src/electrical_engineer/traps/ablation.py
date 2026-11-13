"""Trap ablation and B5 contract metrics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.traps.index import automated_trap_ids
from electrical_engineer.traps.metrics import compute_eval_metrics, load_eval_cases
from electrical_engineer.traps.schema import SolutionTrace
from electrical_engineer.traps.verify import grade_outcome_only, grade_with_verifier

LEGACY = Path(__file__).resolve().parents[3] / "eval/fixtures/trap_prm/traces.json"


def load_ablation_cases() -> list[dict[str, Any]]:
    if not LEGACY.is_file():
        return []
    return list(json.loads(LEGACY.read_text(encoding="utf-8")).get("cases") or [])


def run_ablation() -> dict[str, Any]:
    cases = load_ablation_cases()
    if not cases:
        return {"cases": 0, "note": "legacy fixtures removed; use eval_metrics"}
    without_pass = 0
    with_pass = 0
    for case in cases:
        trace = SolutionTrace.from_mapping(case.get("trace") or {})
        outcome = grade_outcome_only(trace)
        full = grade_with_verifier(trace)
        if outcome.outcome_pass:
            without_pass += 1
        if full.outcome_pass and full.process_pass:
            with_pass += 1
    n = len(cases) or 1
    return {
        "cases": n,
        "outcome_only_pass_rate": round(without_pass / n, 4),
        "with_verifier_pass_rate": round(with_pass / n, 4),
    }


def contract_payload() -> dict[str, Any]:
    eval_cases = len(load_eval_cases())
    return {
        "traps_automated": automated_trap_ids(),
        "hook_contract_path": "docs/hosts/trap_hooks.md",
        "eval_cases": eval_cases,
        "eval_metrics": compute_eval_metrics(),
        "legacy_ablation": run_ablation(),
    }
