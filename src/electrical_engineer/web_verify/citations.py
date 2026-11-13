"""Build answer markdown with inline numeric citations."""

from __future__ import annotations

from typing import Any


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


def render_answer_section(
    summary_lines: list[str],
    web_bundle: dict[str, Any],
    similar_bundle: dict[str, Any],
    citations: list[dict[str, Any]],
) -> str:
    """Return markdown with [n] refs and trailing reference list."""
    lines = list(summary_lines)
    claim_ids = citation_map_for_claims(web_bundle.get("claims") or [])
    if claim_ids:
        lines.append("")
        lines.append("### Verified context")
        for claim in web_bundle.get("claims") or []:
            cid = claim.get("claim_id") or claim.get("name")
            refs = claim_ids.get(cid, [])
            ref_str = "".join(f" [{i}]" for i in refs)
            val = claim.get("web_value")
            unit = claim.get("unit") or ""
            lines.append(f"- **{claim.get('name', cid)}**: {val} {unit}{ref_str}".strip())
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
