"""Validate host-submitted evidence bundles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.web_verify.provenance import source_timestamp
from electrical_engineer.web_verify.source_evidence import validate_claim_sources


def _domains(sources: list[dict[str, Any]]) -> set[str]:
    out: set[str] = set()
    for s in sources:
        d = s.get("domain") or ""
        if d:
            out.add(d.lower())
    return out


def validate_host_submit(payload: dict[str, Any]) -> None:
    web = payload.get("web_sources") or {}
    claims = web.get("claims") or []
    if not claims:
        raise ValueError("host submit must include web_sources.claims")
    all_sources: list[dict[str, Any]] = []
    for c in claims:
        validate_claim_sources(c, min_sources=2)
        srcs = c.get("sources") or []
        qs = c.get("queries") or []
        if len(qs) < 3:
            raise ValueError(f"claim {c.get('claim_id')}: need at least 3 queries recorded")
        all_sources.extend(srcs)
    if len(_domains(all_sources)) < 2:
        raise ValueError("host submit must cite at least 2 independent domains")
    for s in all_sources:
        snip = (s.get("snippet") or "").strip()
        if not snip:
            raise ValueError("each source requires a quoted snippet")
        if len(snip) > 280:
            raise ValueError("snippet too long (max 280 chars)")
        if not source_timestamp(s):
            raise ValueError("each source requires fetched_at or retrieved_at timestamp")


def audit_markdown_provenance(text: str, *, run_dir: Path | None = None) -> None:
    """Raise when answer/notes text claims web verification without session evidence."""
    from electrical_engineer.web_verify.provenance import audit_text_provenance

    violations = audit_text_provenance(text, run_dir=run_dir)
    if violations:
        first = violations[0]
        loc = f"line {first.line_no}" if first.line_no else "text"
        raise ValueError(
            f"provenance audit failed at {loc}: verification language without session evidence — {first.message}"
        )


def validate_similar_matches(matches: list[dict[str, Any]]) -> None:
    for m in matches:
        snip = (m.get("snippet") or "").strip()
        if snip and len(snip) > 280:
            raise ValueError("similar-problem snippet too long")
