"""Regression: false web-verified labels without session evidence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from electrical_engineer.web_verify.provenance import (
    audit_text_provenance,
    sanitize_verification_markers,
)
from electrical_engineer.web_verify.validate import audit_markdown_provenance


def test_audit_fails_on_web_verify_note_without_evidence(tmp_path: Path) -> None:
    notes = "Answer: 70 A\nWeb-verify: NFPA NEC 310.16 / 310.15(B)(1)\n"
    with pytest.raises(ValueError, match="provenance audit"):
        audit_markdown_provenance(notes, run_dir=tmp_path)


def test_audit_passes_when_session_evidence_present(tmp_path: Path) -> None:
    evid = tmp_path / "evidence"
    evid.mkdir()
    bundle = {
        "claims": [
            {
                "claim_id": "nec_adj",
                "sources": [
                    {
                        "url": "https://conduit.site/tables/table-310.15-b-1.php",
                        "snippet": "41-45 ... 0.87",
                        "retrieved_at": "2026-11-13T12:00:00Z",
                    },
                    {
                        "url": "https://up.codes/s/correction-factor-for-ambient-temperatures",
                        "snippet": "41—45 | 0.87",
                        "retrieved_at": "2026-11-13T12:01:00Z",
                    },
                ],
            }
        ]
    }
    (evid / "web_sources.json").write_text(json.dumps(bundle), encoding="utf-8")
    text = "Derated ampacity 70 A\nWeb-verify: NEC 310.15(B)(1) ambient row\n"
    audit_markdown_provenance(text, run_dir=tmp_path)


def test_sanitize_rewrites_web_verify_lines() -> None:
    text = "- Web-verify: NFPA NEC 310.16\n"
    cleaned, notes = sanitize_verification_markers(text)
    assert "unverified (from memory)" in cleaned
    assert notes
    assert audit_text_provenance(cleaned) == []


def test_cli_provenance_audit_rejects_bad_notes(tmp_path: Path) -> None:
    bad = tmp_path / "notes.md"
    bad.write_text("Web-verify: made up\n", encoding="utf-8")
    from electrical_engineer.web_verify.validate import audit_markdown_provenance

    with pytest.raises(ValueError):
        audit_markdown_provenance(bad.read_text(), run_dir=tmp_path)
