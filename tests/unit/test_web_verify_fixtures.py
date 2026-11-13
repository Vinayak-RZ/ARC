"""Recorded web-verify fixtures must cite real URLs with unique citation ids."""

from __future__ import annotations

import json
from pathlib import Path


def _fixture_paths() -> list[Path]:
    root = Path(__file__).resolve().parents[2] / "eval" / "fixtures" / "web_verify"
    return sorted(root.glob("*.json"))


def test_fixture_urls_are_not_placeholders():
    for path in _fixture_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        ids: list[int] = []
        for claim in data.get("claims") or []:
            for src in claim.get("sources") or []:
                url = str(src.get("url") or "").lower()
                assert "example" not in url, f"{path.name} contains placeholder URL {url}"
                assert url.startswith("http"), f"{path.name} bad URL {url}"
                cid = int(src.get("citation_id") or 0)
                if cid:
                    ids.append(cid)
        for m in data.get("similar_problems") or []:
            url = str(m.get("url") or "").lower()
            if url:
                assert "example" not in url
            if m.get("citation_id"):
                ids.append(int(m["citation_id"]))
        assert len(ids) == len(set(ids)), f"{path.name} duplicate citation ids"
