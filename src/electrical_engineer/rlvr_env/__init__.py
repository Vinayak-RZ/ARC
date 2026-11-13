"""Open RLVR-style environment over Arc trap goldens (no weight training in v1)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.rlvr_env.env import ArcRlvrEnv, run_dummy_rollout
from electrical_engineer.rlvr_env.rewards import grade_trap, oracle_submission

MANIFEST = Path(__file__).resolve().parent / "manifest.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def list_trap_ids() -> list[str]:
    return [str(t["id"]) for t in load_manifest().get("traps", [])]


def contract_json() -> dict[str, Any]:
    """B7 contract output for frontier nodes."""
    m = load_manifest()
    return {
        "rlvr_env_manifest": {
            "version": str(m.get("version", "0.1")),
            "traps": len(m.get("traps", [])),
        }
    }


__all__ = [
    "ArcRlvrEnv",
    "contract_json",
    "grade_trap",
    "list_trap_ids",
    "load_manifest",
    "oracle_submission",
    "run_dummy_rollout",
]
