"""Offline web-verify: citations, similar problems, stale-context gate."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from electrical_engineer.eval_runner.score import run_item
from electrical_engineer.runner.execute import execute
from electrical_engineer.web_verify.engine import run_web_verify
from electrical_engineer.web_verify.validate import validate_host_submit


@pytest.fixture(autouse=True)
def _offline_provider(monkeypatch):
    monkeypatch.setenv("EE_WEB_VERIFY_PROVIDER", "offline")


def test_offline_catches_stale_library_value():
    problem = {
        "web_verify_fixture": "zebra_gmr",
        "context_claims": [
            {
                "claim_id": "zebra_gmr",
                "name": "ACSR Zebra GMR",
                "library_value": 0.01058,
                "unit": "m",
                "tolerance": 0.01,
            }
        ],
        "recompute": {"kind": "zebra_inductance_p04", "gmd_m": 5.961},
    }
    out = run_web_verify(problem=problem, solver_outputs={}, summary_lines=[], run_dir=None)
    assert out["needs_review"] is True
    md = out["answer_markdown"]
    assert "[1]" in md
    assert "Similar solved problems" in md
    claims = out["web_sources"]["claims"]
    assert claims[0]["status"] == "needs_review"
    assert abs(out["recomputed"]["L_mH_per_km"] - 1.2525) < 0.01


def test_host_submit_validation():
    payload = {
        "web_sources": {
            "claims": [
                {
                    "claim_id": "x",
                    "queries": ["a", "b", "c"],
                    "sources": [
                        {"domain": "a.example", "snippet": "one"},
                        {"domain": "b.example", "snippet": "two"},
                    ],
                }
            ]
        }
    }
    validate_host_submit(payload)


def test_context_web_gold_pack(tmp_path):
    root = Path(__file__).resolve().parents[2]
    item = root / "eval/gold/context-web/zebra_gmr-01"
    result = run_item(item, run_root=tmp_path)
    assert result["ok"] is True


def test_solve_recipe_includes_web_verify(tmp_path):
    problem = json.loads(
        (Path(__file__).resolve().parents[2] / "eval/gold/circuits/rc-step-01/fixtures/problem.json").read_text()
    )
    result = execute("solve-circuit-problem", run_root=tmp_path, problem=problem)
    summary = json.loads((Path(result["run_dir"]) / "evidentiary.json").read_text())
    assert summary.get("web_verification") is not None or any(
        n.get("ok") is not None for n in (summary.get("nodes") or {}).values()
    )
    nodes = (Path(result["run_dir"]) / "nodes").iterdir() if (Path(result["run_dir"]) / "nodes").is_dir() else []
    assert any(p.name == "web" for p in nodes)
