"""Open RLVR-style environment over Arc trap goldens (no weight training in v1)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.rlvr_env.env import ArcRlvrEnv, run_dummy_rollout, run_naive_rollout
from electrical_engineer.rlvr_env.rewards import grade_trap, naive_submission, oracle_submission
from electrical_engineer.rlvr_env.schema import HELD_OUT_SEED_MIN, is_held_out_seed

MANIFEST = Path(__file__).resolve().parent / "manifest.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def list_trap_ids() -> list[str]:
    return [str(t["id"]) for t in load_manifest().get("traps", [])]


def contract_json() -> dict[str, Any]:
    m = load_manifest()
    return {
        "rlvr_env_manifest": {
            "version": str(m.get("version", "0.1")),
            "traps": len(m.get("traps", [])),
            "held_out_seed_min": HELD_OUT_SEED_MIN,
        }
    }


__all__ = [
    "ArcRlvrEnv",
    "contract_json",
    "grade_trap",
    "is_held_out_seed",
    "list_trap_ids",
    "load_manifest",
    "naive_submission",
    "oracle_submission",
    "run_dummy_rollout",
    "run_naive_rollout",
]
