#!/usr/bin/env python3
"""CI gate: circuit property tests and engine gold count."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_ENGINE_GOLDS = 30


def main() -> int:
    pack = ROOT / "eval" / "gold" / "circuits"
    engine = 0
    for item in pack.iterdir():
        if not item.is_dir():
            continue
        expect = item / "expect.json"
        if not expect.is_file():
            continue
        data = json.loads(expect.read_text())
        if data.get("engine") in {"circuit_unit", "circuit_verify"}:
            engine += 1
    if engine < MIN_ENGINE_GOLDS:
        print(f"circuit engine golds {engine} < {MIN_ENGINE_GOLDS}")
        return 1
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/unit/test_circuit_properties.py",
        "tests/integration/test_circuit_kernel.py",
        "-q",
    ]
    code = subprocess.call(cmd, cwd=ROOT)
    if code != 0:
        return code
    from electrical_engineer.engines.spice_runner import simulator_status

    st = simulator_status()
    if not st.get("available"):
        print(f"circuit_eval: ngspice required in CI: {st.get('reason')}", file=sys.stderr)
        return 1
    print(f"circuit_eval: {engine} engine golds ok (ngspice present)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
