#!/usr/bin/env python3
"""DEPRECATED: golds come from ngspice/hand oracle (capture_circuit_oracle.py), not derive()."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    script = Path(__file__).resolve().parent / "capture_circuit_oracle.py"
    print("seed_circuit_golds: delegating to capture_circuit_oracle (independent golds)")
    return subprocess.call([sys.executable, str(script)], cwd=Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    raise SystemExit(main())
