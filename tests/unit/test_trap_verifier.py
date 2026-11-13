"""Unit tests for engine-backed trap PRM."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from electrical_engineer.traps.ablation import contract_payload
from electrical_engineer.traps.index import automated_trap_ids
from electrical_engineer.traps.metrics import compute_eval_metrics
from electrical_engineer.traps.schema import SolutionTrace
from electrical_engineer.traps.text_advisory import find_advisory
from electrical_engineer.traps.verify import grade_trace, verify_trace_payload

EVAL = Path("eval/fixtures/trap_prm/eval_traces.json")


def test_automated_trap_ids_includes_contract_set() -> None:
    auto = set(automated_trap_ids())
    assert {"T1", "T2", "T4", "T5", "T6"}.issubset(auto)


def test_negation_does_not_advisory_ode45() -> None:
    pat = re.compile(r"\bode45\b", re.IGNORECASE)
    assert find_advisory("We did not use ode45 here.", pat) is None
    assert find_advisory("Solved with ode45.", pat) is not None


def test_empty_trace_process_unchecked() -> None:
    g = grade_trace(SolutionTrace.from_mapping({}))
    assert g.process_status == "unchecked"
    assert g.process_pass is False


def test_correct_smib_varied_givens_passes_t1() -> None:
    cases = json.loads(EVAL.read_text())["cases"]
    row = next(c for c in cases if c["id"] == "correct-smib-0")
    g = grade_trace(SolutionTrace.from_mapping(row["trace"]))
    t1 = next(c for c in g.checks if c.trap_id == "T1")
    assert t1.status == "pass"


def test_wrong_t1_fails_not_lab_constant() -> None:
    cases = json.loads(EVAL.read_text())["cases"]
    row = next(c for c in cases if c["id"].startswith("wrong-t1-smib"))
    g = grade_trace(SolutionTrace.from_mapping(row["trace"]))
    assert any(c.trap_id == "T1" and c.status == "fail" for c in g.checks)


def test_eval_metrics_zero_fp_on_correct() -> None:
    m = compute_eval_metrics()
    assert m["eval_cases"] >= 30
    assert m["false_positives_on_correct"] == 0
    assert m["false_positive_rate_on_correct"] == 0.0


def test_contract_includes_eval_metrics() -> None:
    c = contract_payload()
    assert c["hook_contract_path"] == "docs/hosts/trap_hooks.md"
    assert c["eval_metrics"]["eval_cases"] >= 30


def test_contract_script_runs() -> None:
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        [sys.executable, "scripts/trap_prm_contract.py"],
        cwd=Path.cwd(),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["eval_metrics"]["false_positives_on_correct"] == 0


def test_verify_payload_process_status() -> None:
    payload = verify_trace_payload(
        {
            "trap_ids": ["T9"],
            "givens": {"domain": "integration"},
            "final": {"solver_used": "rk4"},
        }
    )
    assert payload["process_status"] in ("pass", "unchecked")
