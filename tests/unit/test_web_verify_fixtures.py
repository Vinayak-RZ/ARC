"""Recorded web-verify fixtures must cite real URLs with unique citation ids."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from electrical_engineer.web_verify.source_evidence import validate_fixture_claim


def _fixture_paths() -> list[Path]:
    root = Path(__file__).resolve().parents[2] / "eval" / "fixtures" / "web_verify"
    return sorted(root.glob("*.json"))


def test_fixture_urls_are_not_placeholders():
    for path in _fixture_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        for claim in data.get("claims") or []:
            validate_fixture_claim(claim)
        for claim in data.get("claims") or []:
            for src in claim.get("sources") or []:
                url = str(src.get("url") or "").lower()
                if url:
                    assert "example" not in url, f"{path.name} contains placeholder URL {url}"
                    assert url.startswith("http"), f"{path.name} bad URL {url}"
                role = str(src.get("source_class") or "").lower()
                if role == "context_only":
                    assert src.get("extracted_value") is None, f"context_only must not carry extracted_value: {url}"


def test_fixture_snippet_value_misattribution_rejected():
    from electrical_engineer.web_verify.source_evidence import value_supported_by_snippet

    assert not value_supported_by_snippet("Overall diameter 28.62 mm", 0.01144, "m")
    bad_src = {
        "url": "https://upptcl.org/upptcl/en/article/table-14-i",
        "domain": "upptcl.org",
        "snippet": "Overall diameter 28.62 mm",
        "extracted_value": 0.01144,
        "unit": "m",
        "source_class": "primary",
    }
    claim = {
        "claim_id": "x",
        "sources": [
            {
                "url": "https://engineeringdevotion.com/page",
                "domain": "engineeringdevotion.com",
                "snippet": "GMR 1.144 cm",
                "extracted_value": 0.01144,
                "unit": "m",
                "source_class": "primary",
            },
            bad_src,
            {
                "domain": "arc.derived",
                "snippet": "11.44 mm",
                "extracted_value": 0.01144,
                "source_class": "derived",
                "derivation": "geometry",
            },
        ],
    }
    with pytest.raises(ValueError, match="not supported by snippet"):
        validate_fixture_claim(claim)
