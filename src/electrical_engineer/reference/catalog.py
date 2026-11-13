"""Load, search, and fetch curated EE reference records."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from electrical_engineer.reference.schema import SchemaError, validate_record

DATA_DIR = Path(__file__).resolve().parent / "data"
_TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?", re.IGNORECASE)


def _data_files() -> list[Path]:
    return sorted(DATA_DIR.glob("*.yaml"))


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN.findall(text)]


def _record_blob(rec: dict[str, Any]) -> str:
    parts = [
        rec["id"],
        rec["title"],
        rec["domain"],
        " ".join(str(a) for a in rec.get("aliases") or []),
    ]
    vals = rec.get("values") or {}
    for k, v in vals.items():
        parts.append(str(k))
        if isinstance(v, (str, int, float, bool)):
            parts.append(str(v))
    src = rec.get("source") or {}
    for k in ("title", "edition", "clause"):
        parts.append(str(src.get(k, "")))
    return " ".join(parts).lower()


def _condition_summary(rec: dict[str, Any]) -> dict[str, str]:
    vals = rec.get("values") or {}
    cond = dict(rec.get("value_conditions") or {})
    for key in vals:
        if key not in cond:
            cond[key] = "see source clause; check units in key name"
    return cond


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for path in _data_files():
        raw = yaml.safe_load(path.read_text()) or []
        if not isinstance(raw, list):
            raise SchemaError(f"{path.name}: expected top-level list")
        for i, rec in enumerate(raw):
            validate_record(rec, path=f"{path.name}[{i}]")
            rid = str(rec["id"])
            if rid in by_id:
                raise SchemaError(f"duplicate id {rid}")
            by_id[rid] = rec
    return by_id


def list_domains() -> dict[str, int]:
    counts: dict[str, int] = {}
    for rec in load_catalog().values():
        d = str(rec["domain"])
        counts[d] = counts.get(d, 0) + 1
    return counts


def get_record(record_id: str) -> dict[str, Any] | None:
    rec = load_catalog().get(record_id)
    if rec is None:
        return None
    return _presentation(rec)


def _presentation(rec: dict[str, Any]) -> dict[str, Any]:
    src = rec["source"]
    src2 = rec.get("source_secondary") or {}
    return {
        "id": rec["id"],
        "domain": rec["domain"],
        "title": rec["title"],
        "aliases": list(rec.get("aliases") or []),
        "values": rec["values"],
        "value_conditions": _condition_summary(rec),
        "source": {
            "title": src["title"],
            "edition": src["edition"],
            "clause": src["clause"],
        },
        "source_secondary": {
            "title": src2["title"],
            "edition": src2["edition"],
            "clause": src2["clause"],
            "url": src2.get("url", ""),
        },
        "url": rec["url"],
        "license": rec["license"],
        "verification": rec["verification"],
        "confidence": rec["confidence"],
    }


def search_records(query: str, *, limit: int = 20) -> list[dict[str, Any]]:
    q = (query or "").strip()
    if not q:
        return []
    tokens = _tokenize(q)
    if not tokens:
        return []
    scored: list[tuple[int, str]] = []
    for rid, rec in load_catalog().items():
        blob = _record_blob(rec)
        rid_l = rid.lower()
        score = 0
        for t in tokens:
            if t == rid_l or t.replace("_", "") == rid_l.replace("_", ""):
                score += 50
            elif t in rid_l:
                score += 30
            elif t in blob:
                score += 10 + blob.count(t)
        if score:
            scored.append((score, rid))
    scored.sort(key=lambda x: (-x[0], x[1]))
    out: list[dict[str, Any]] = []
    for score, rid in scored[:limit]:
        item = _presentation(load_catalog()[rid])
        item["score"] = score
        out.append(item)
    return out


def clear_catalog_cache() -> None:
    load_catalog.cache_clear()
