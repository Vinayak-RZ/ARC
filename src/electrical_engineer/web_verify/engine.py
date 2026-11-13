"""Orchestrate web verification for a workflow run."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.web_verify.citations import index_citations, render_answer_section
from electrical_engineer.web_verify.config import load_web_verify_config
from electrical_engineer.web_verify.providers import get_provider
from electrical_engineer.web_verify.recompute import recompute
from electrical_engineer.web_verify.reconcile import (
    overall_status,
    reconcile_claim,
    reconcile_similar_match,
)


def enrich_claims_from_reference_library(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach library_value from curated reference records when claim cites a record."""
    from electrical_engineer.reference.catalog import get_record

    enriched: list[dict[str, Any]] = []
    for row in claims:
        claim = dict(row)
        rid = claim.get("reference_record_id") or claim.get("reference_id")
        vkey = claim.get("record_value_key") or claim.get("library_value_key")
        if rid and vkey:
            rec = get_record(str(rid))
            if rec is None:
                claim.setdefault("reference_error", f"unknown record {rid}")
            else:
                vals = rec.get("values") or {}
                if vkey not in vals:
                    claim.setdefault("reference_error", f"value key {vkey} missing on {rid}")
                else:
                    claim.setdefault("reference_record_id", str(rid))
                    claim.setdefault("reference_title", rec.get("title"))
                    if claim.get("library_value") is None:
                        claim["library_value"] = vals[vkey]
                    cond = (rec.get("value_conditions") or {}).get(vkey)
                    if cond and not claim.get("conditions"):
                        claim["conditions"] = cond
                    if not claim.get("name"):
                        claim["name"] = rec.get("title")
        enriched.append(claim)
    return enriched


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
    claims = enrich_claims_from_reference_library(extract_context_claims(problem, solver_outputs))
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
    incoming = {str(c.get("claim_id")): c for c in claims if c.get("claim_id")}
    claims_out = []
    for c in web_raw.get("claims") or []:
        cid = str(c.get("claim_id") or "")
        if cid in incoming:
            inc = incoming[cid]
            if inc.get("library_value") is not None:
                c["library_value"] = inc["library_value"]
            if inc.get("tolerance") is not None:
                c["tolerance"] = inc["tolerance"]
            for key in ("reference_record_id", "reference_title", "record_value_key"):
                if inc.get(key) is not None:
                    c[key] = inc[key]
        row = reconcile_claim(c)
        if row.get("web_value") is not None:
            row["substituted_value"] = row.get("web_value")
        claims_out.append(row)
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
    recomputed: dict[str, Any] = {}
    try:
        if problem.get("recompute"):
            recomputed = recompute(problem, claims_out)
    except (ValueError, KeyError, TypeError):
        recomputed = {"error": "recompute_failed"}
    answer_md = render_answer_section(
        summary_lines or [],
        web_bundle,
        similar_bundle,
        citations,
        recomputed=recomputed if recomputed and "error" not in recomputed else None,
    )

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
        if recomputed:
            (evidence_dir / "recomputed.json").write_text(json.dumps(recomputed, indent=2), encoding="utf-8")

    return {
        "status": status,
        "provider": cfg.provider,
        "web_sources": web_bundle,
        "similar_problems": similar_bundle,
        "citations": citations,
        "answer_markdown": answer_md,
        "needs_review": status == "needs_review",
        "offline_unverified": status == "offline_pass" and cfg.provider == "offline",
        "recomputed": recomputed,
    }
