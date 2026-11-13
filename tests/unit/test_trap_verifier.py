"""Unit tests for trap PRM detectors and grader split."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.traps.ablation import contract_payload, run_ablation
from electrical_engineer.traps.index import automated_trap_ids
from electrical_engineer.traps.schema import SolutionTrace
from electrical_engineer.traps.verify import (
    grade_outcome_only,
    grade_with_verifier,
    verify_trace_payload,
)


def test_automated_trap_ids_includes_contract_set() -> None:
    auto = set(automated_trap_ids())
    assert {"T1", "T2", "T4", "T5", "T6"}.issubset(auto)


def test_t1_bare_fails_process_arc_passes() -> None:
    cases = json.loads(Path("eval/fixtures/trap_prm/traces.json").read_text())["cases"]
    bare = SolutionTrace.from_mapping(next(c for c in cases if c["id"] == "t1-bare-bad")["trace"])
    arc = SolutionTrace.from_mapping(next(c for c in cases if c["id"] == "t1-arc-good")["trace"])
    assert not grade_with_verifier(bare).process_pass
    assert grade_with_verifier(arc).process_pass


def test_outcome_only_can_pass_when_process_fails() -> None:
    cases = json.loads(Path("eval/fixtures/trap_prm/traces.json").read_text())["cases"]
    t2 = SolutionTrace.from_mapping(next(c for c in cases if c["id"] == "t2-ode45-bad")["trace"])
    outcome = grade_outcome_only(t2)
    full = grade_with_verifier(t2)
    assert outcome.outcome_pass
    assert not full.process_pass


def test_verify_trace_payload_shape() -> None:
    payload = verify_trace_payload(
        {
            "trap_ids": ["T6"],
            "steps": [{"id": "x", "text": "λ-ED with limits", "P2_mw": 150.0}],
            "final": {"P2_mw": 150.0, "expected": {"P2_mw": 150.0}},
        }
    )
    assert payload["tool"] == "trap-verify"
    assert payload["process_pass"] is True
    assert payload["ok"] is True


def test_ablation_produces_real_rates() -> None:
    report = run_ablation()
    assert report["cases"] >= 6
    assert 0.0 <= report["outcome_only_pass_rate"] <= 1.0
    assert 0.0 <= report["with_verifier_pass_rate"] <= 1.0
    assert report["with_verifier_pass_rate"] < report["outcome_only_pass_rate"]


def test_contract_payload_fields() -> None:
    c = contract_payload()
    assert c["hook_contract_path"] == "docs/hosts/trap_hooks.md"
    assert "T1" in c["traps_automated"]
    assert "ablation" in c
