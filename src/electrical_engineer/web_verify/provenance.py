"""Session evidence requirements for web-verified labels and citations."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_VERIFICATION_PHRASE = re.compile(
    r"(?i)\b(web[- ]?verif(?:y|ied)|verified\s+via\s+web|verified\s+online|web\s+citation)\b"
)
_WEB_VERIFY_LINE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:web[- ]?verify|web[- ]?verified)\s*:\s*.+$"
)


@dataclass(frozen=True)
class ProvenanceViolation:
    kind: str
    message: str
    line_no: int | None = None


def source_timestamp(src: dict[str, Any]) -> str | None:
    for key in ("fetched_at", "retrieved_at", "timestamp"):
        val = src.get(key)
        if val:
            return str(val)
    return None


def evidence_record_valid(src: dict[str, Any]) -> bool:
    url = (src.get("url") or "").strip()
    snippet = (src.get("snippet") or "").strip()
    ts = source_timestamp(src)
    if not snippet:
        return False
    if not ts:
        return False
    role = str(src.get("source_class") or "").lower()
    if role == "derived":
        return bool(src.get("derivation") or snippet)
    return bool(url or (src.get("domain") or "").strip())


def claim_has_session_evidence(claim: dict[str, Any]) -> bool:
    sources = claim.get("sources") or []
    valid = [s for s in sources if evidence_record_valid(s)]
    return len(valid) >= 2


def claim_may_use_verified_label(claim: dict[str, Any]) -> bool:
    if not claim_has_session_evidence(claim):
        return False
    status = str(claim.get("status") or "").lower()
    return status in ("verified", "pass")


def downgrade_claim_provenance(claim: dict[str, Any]) -> dict[str, Any]:
    out = dict(claim)
    if claim_may_use_verified_label(claim):
        return out
    status = str(claim.get("status") or "").lower()
    if status in ("needs_review", "mismatch_library", "mismatch_solver", "pending_host", "unsupported"):
        return out
    if status in ("verified", "pass"):
        out["status"] = "unverified_from_memory"
        out["provenance_note"] = "unverified (from memory) — no session evidence record"
    elif status in ("", "unverified", "unverified_from_memory"):
        out["status"] = "unverified_from_memory"
        out["provenance_note"] = "unverified (from memory) — no session evidence record"
    return out


def find_verification_language_violations(text: str) -> list[ProvenanceViolation]:
    violations: list[ProvenanceViolation] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if _VERIFICATION_PHRASE.search(line) or _WEB_VERIFY_LINE.match(line):
            violations.append(
                ProvenanceViolation(
                    kind="verification_language",
                    message=line.strip()[:200],
                    line_no=i,
                )
            )
    return violations


def load_session_evidence_from_run(run_dir: Path | None) -> list[dict[str, Any]]:
    if run_dir is None:
        return []
    paths = (
        run_dir / "evidence" / "web_sources.json",
        run_dir / "evidence" / "host_submit.json",
    )
    claims: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        bundle = data.get("web_sources") if isinstance(data.get("web_sources"), dict) else data
        for row in bundle.get("claims") or []:
            if claim_has_session_evidence(row):
                claims.append(row)
    return claims


def audit_text_provenance(
    text: str,
    *,
    run_dir: Path | None = None,
    session_claims: list[dict[str, Any]] | None = None,
) -> list[ProvenanceViolation]:
    """Fail when verification language appears without matching session evidence."""
    language_hits = find_verification_language_violations(text)
    if not language_hits:
        return []
    claims = session_claims if session_claims is not None else load_session_evidence_from_run(run_dir)
    if claims:
        return []
    return language_hits


def sanitize_verification_markers(text: str) -> tuple[str, list[str]]:
    """Replace false web-verify notes with honest unverified labels."""
    notes: list[str] = []
    lines_out: list[str] = []
    for line in text.splitlines():
        if _WEB_VERIFY_LINE.match(line) or _VERIFICATION_PHRASE.search(line):
            stripped = line.strip().lstrip("-*").strip()
            if stripped.lower().startswith("web"):
                payload = stripped.split(":", 1)[-1].strip() if ":" in stripped else stripped
                repl = f"unverified (from memory): {payload}"
            else:
                repl = f"unverified (from memory): {stripped}"
            notes.append(repl)
            if line.strip().startswith(("-", "*")):
                indent = line[: len(line) - len(line.lstrip())]
                lines_out.append(f"{indent}- {repl}")
            else:
                lines_out.append(repl)
        else:
            lines_out.append(line)
    return "\n".join(lines_out), notes


def apply_claim_provenance_honesty(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [downgrade_claim_provenance(c) for c in claims]


def audit_file(path: Path, *, run_dir: Path | None = None) -> list[ProvenanceViolation]:
    text = path.read_text(encoding="utf-8")
    parent_run = run_dir
    if parent_run is None and (path.parent / "web_sources.json").is_file():
        parent_run = path.parent
    elif parent_run is None and (path.parent.name == "evidence"):
        parent_run = path.parent.parent
    return audit_text_provenance(text, run_dir=parent_run)
