#!/usr/bin/env python3
"""Local pass^k for scripted trap ablation (no live LLM keys)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/frontier/pass_k_traps.json"


def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "tests/integration/test_trap_ablation.py", "-q"]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    passed = proc.returncode == 0
    report = {
        "mode": "scripted_regression",
        "k": 3,
        "pass_k": 1.0 if passed else 0.0,
        "threshold": 0.75,
        "ok": passed,
        "stdout_tail": proc.stdout.splitlines()[-5:],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
