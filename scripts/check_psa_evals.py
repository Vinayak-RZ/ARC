#!/usr/bin/env python3
"""CI gate: PSA golden eval fixtures and unit tests exist."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = [
    "eval/gold/power/smib-eec301-01/expect.json",
    "eval/gold/power/agc-eec301-01/expect.json",
    "eval/gold/power/ed-eec301-01/expect.json",
]


def main() -> int:
    missing = [p for p in GOLD if not (ROOT / p).is_file()]
    if missing:
        print("missing gold:", missing)
        return 1
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/unit/test_smib_swing.py",
        "tests/unit/test_agc_two_area.py",
        "tests/unit/test_ed_lambda.py",
        "tests/integration/test_trap_ablation.py",
        "-q",
    ]
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
