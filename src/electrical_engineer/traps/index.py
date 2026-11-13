"""Trap catalog index (T1–T10) for automated PRM routing."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_INDEX = Path(__file__).resolve().parents[3] / "artifacts/frontier/trap_suite_index.json"


@lru_cache(maxsize=1)
def load_trap_index() -> dict[str, Any]:
    return json.loads(_INDEX.read_text(encoding="utf-8"))


def automated_trap_ids() -> list[str]:
    """Traps with deterministic detectors in this pass."""
    catalog = {str(t["id"]) for t in load_trap_index().get("traps") or []}
    wired = {
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
        "T7",
        "T9",
        "T10",
    }
    return sorted(catalog & wired)


def trap_topics() -> dict[str, str]:
    out: dict[str, str] = {}
    for row in load_trap_index().get("traps") or []:
        out[str(row["id"])] = str(row.get("topic") or "")
    return out
