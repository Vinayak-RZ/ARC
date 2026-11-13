"""Build answer markdown with inline numeric citations."""

from __future__ import annotations

from typing import Any

from electrical_engineer.web_verify.provenance import (
    claim_may_use_verified_label,
    sanitize_verification_markers,
)


def index_citations(web_bundle: dict[str, Any], similar_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    citations: list[dict[str, Any]] = list(web_bundle.get("citations") or [])
    next_id = max((c.get("citation_id", 0) for c in citations), default=0) + 1
    for m in similar_bundle.get("matches") or []:
        if m.get("url"):
            if not m.get("citation_id"):
                m["citation_id"] = next_id
                next_id += 1
            citations.append(
                {
                    "citation_id": m["citation_id"],
                    "url": m["url"],
                    "title": m.get("title"),
                    "domain": m.get("domain"),
                    "snippet": m.get("snippet"),
                    "source_class": "similar_problem",
                }
            )
    return citations


def citation_map_for_claims(claims: list[dict[str, Any]]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for c in claims:
        ids = [s.get("citation_id") for s in (c.get("sources") or []) if s.get("citation_id")]
        if ids:
            out[c.get("claim_id") or c.get("name") or "claim"] = ids
    return out


def append_standard_formula_lines(lines: list[str], recomputed: dict[str, Any]) -> None:
    """Show clause + inputs when a recompute used a standard formula/table."""
    clause = recomputed.get("standard_clause")
    inputs = recomputed.get("inputs_used")
    if not clause and not inputs:
        return
    lines.append("")
    lines.append("### Standard formula check")
    if clause:
        lines.append(f"- **Clause**: {clause}")
    if inputs:
        parts = [f"{k}={v}" for k, v in sorted(inputs.items()) if v is not None]
        if parts:
            lines.append(f"- **Inputs**: {', '.join(parts)}")
    if recomputed.get("table_row_label"):
        lines.append(f"- **Table row**: {recomputed['table_row_label']}")
    for key in ("e_v", "V_touch_V", "tdd_limit_percent", "limit_tdd_percent"):
        if key in recomputed and recomputed[key] is not None:
            lines.append(f"- **Result ({key})**: {recomputed[key]}")


def render_answer_section(
    summary_lines: list[str],
    web_bundle: dict[str, Any],
    similar_bundle: dict[str, Any],
    citations: list[dict[str, Any]],
    *,
    recomputed: dict[str, Any] | None = None,
) -> str:
    """Return markdown with [n] refs and trailing reference list."""
    raw = "\n".join(summary_lines or [])
    sanitized, _ = sanitize_verification_markers(raw)
    lines = sanitized.splitlines() if sanitized else []
    if recomputed:
        append_standard_formula_lines(lines, recomputed)
    claim_ids = citation_map_for_claims(web_bundle.get("claims") or [])
    verified_claims = [c for c in (web_bundle.get("claims") or []) if claim_may_use_verified_label(c)]
    if verified_claims:
        lines.append("")
        lines.append("### Verified context (session evidence)")
        for claim in verified_claims:
            cid = claim.get("claim_id") or claim.get("name")
            refs = claim_ids.get(cid, [])
            ref_str = "".join(f" [{i}]" for i in refs)
            val = claim.get("web_value")
            unit = claim.get("unit") or ""
            lines.append(f"- **{claim.get('name', cid)}**: {val} {unit}{ref_str}".strip())
    memory_claims = [
        c
        for c in (web_bundle.get("claims") or [])
        if not claim_may_use_verified_label(c) and (c.get("library_value") is not None or c.get("web_value") is not None)
    ]
    if memory_claims:
        lines.append("")
        lines.append("### unverified (from memory)")
        for claim in memory_claims:
            cid = claim.get("claim_id") or claim.get("name")
            val = claim.get("web_value") if claim.get("web_value") is not None else claim.get("library_value")
            unit = claim.get("unit") or ""
            lines.append(f"- **{claim.get('name', cid)}**: {val} {unit} — session evidence required for verified label".strip())
    matches = similar_bundle.get("matches") or []
    if matches:
        lines.append("")
        lines.append("### Similar solved problems")
        for m in matches:
            ref = f" [{m['citation_id']}]" if m.get("citation_id") else ""
            agree = m.get("agrees_after_adjustment")
            flag = " (disagrees, needs review)" if agree is False else ""
            title = m.get("title") or m.get("url")
            lines.append(f"- [{title}]({m.get('url')}){ref}: {m.get('diff_note', '')}{flag}")
    if citations:
        lines.append("")
        lines.append("### References")
        for c in sorted(citations, key=lambda x: int(x.get("citation_id") or 0)):
            cid = c.get("citation_id")
            url = c.get("url") or ""
            title = c.get("title") or url
            lines.append(f"[{cid}] {title} - {url}")
    return "\n".join(lines)


def attach_inline_citations(text: str, claim_refs: dict[str, list[int]], key: str) -> str:
    ids = claim_refs.get(key)
    if not ids:
        return text
    suffix = "".join(f" [{i}]" for i in ids)
    if suffix in text:
        return text
    return text.rstrip() + suffix
