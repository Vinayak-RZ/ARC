#!/usr/bin/env python3
"""LIVE host A/B harness. Blocked without API keys (Gate 0 models)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/frontier-ab/live_ab_status.json"


def main() -> int:
    keys = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY")
    missing = [k for k in keys if not os.environ.get(k)]
    payload = {
        "status": "blocked",
        "reason": "missing_api_keys" if missing else "not_implemented",
        "missing_env": missing,
        "pass_k_threshold": 0.75,
        "bare_threshold": 0.15,
        "held_out_sheets": 8,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload))
    return 0 if missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
