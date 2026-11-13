#!/usr/bin/env python3
"""Emit B5 contract JSON: automated traps, hook path, ablation scores."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from electrical_engineer.traps.ablation import contract_payload


def main() -> int:
    payload = contract_payload()
    out = ROOT / "artifacts/frontier/b5_trap_prm_contract.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
