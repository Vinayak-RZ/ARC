"""Orchestrate web verification for a workflow run."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.web_verify.citations import index_citations, render_answer_section
from electrical_engineer.web_verify.config import load_web_verify_config
from electrical_engineer.web_verify.providers import get_provider
from electrical_engineer.web_verify.reconcile import overall_status, reconcile_claim, reconcile_similar_match


def extract_context_claims(problem: dict[str, Any], solver_outputs: dict[str, Any]) -> list[dict[str, Any]]:
    raw = problem.get("context_claims")
    if isinstance(raw, list) and raw:
        claims = []
        for row in raw:
            if not isinstance(row, dict):
                continue
            c = dict(row)
            sid = c.get("solver_key")
            if sid and sid in solver_outputs:
                c["solver_value"] = solver_outputs[sid]
            claims.append(c)
        return claims
    # Auto: single external constant on problem
    if problem.get("external_constant"):
        ec = problem["external_constant"]
        if isinstance(ec, dict):
            return [ec]
    return []


def run_web_verify(
    *,
    problem: dict[str, Any],
    solver_outputs: dict[str, Any],
    summary_lines: list[str] | None,
    run_dir: Path | None,
    arc_primary_result: Any = None,
) -> dict[str, Any]:
    cfg = load_web_verify_config(run_dir)
    claims = extract_context_claims(problem, solver_outputs)
    if not claims and not problem.get("web_verify_fixture"):
        bundle = {"provider": cfg.provider, "status": "no_claims", "claims": [], "citations": []}
        similar_bundle = {"provider": cfg.provider, "topic": problem.get("topic") or "", "matches": []}
        return {
            "status": "pass",
            "provider": cfg.provider,
            "web_sources": bundle,
            "similar_problems": similar_bundle,
            "citations": [],
            "answer_markdown": "\n".join(summary_lines or []),
            "needs_review": False,
            "offline_unverified": False,
        }
    provider = get_provider(cfg)
    web_raw = provider.verify_claims(claims, problem=problem, run_dir=run_dir)
    claims_out = [reconcile_claim(c) for c in web_raw.get("claims") or []]
    web_bundle = {**web_raw, "claims": claims_out}
    similar_raw = provider.find_similar_problems(
        problem, arc_result=arc_primary_result, run_dir=run_dir
    )
    similar_matches = [
        reconcile_similar_match(m, arc_result=arc_primary_result)
        for m in similar_raw.get("matches") or []
    ]
    similar_bundle = {**similar_raw, "matches": similar_matches}
    citations = index_citations(web_bundle, similar_bundle)
    web_bundle["citations"] = citations
    status = overall_status(claims_out, similar_matches, str(web_raw.get("status") or ""))
    answer_md = render_answer_section(summary_lines or [], web_bundle, similar_bundle, citations)

    evidence_dir = (run_dir / "evidence") if run_dir else None
    if evidence_dir:
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / "web_sources.json").write_text(
            json.dumps(web_bundle, indent=2), encoding="utf-8"
        )
        (evidence_dir / "similar_problems.json").write_text(
            json.dumps(similar_bundle, indent=2), encoding="utf-8"
        )
        (evidence_dir / "answer_cited.md").write_text(answer_md, encoding="utf-8")

    return {
        "status": status,
        "provider": cfg.provider,
        "web_sources": web_bundle,
        "similar_problems": similar_bundle,
        "citations": citations,
        "answer_markdown": answer_md,
        "needs_review": status == "needs_review",
        "offline_unverified": status == "offline_pass" and cfg.provider == "offline",
    }
