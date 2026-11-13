#!/usr/bin/env python3
"""CIRCUIT subset v0.1: run circuit eval golds with ngspice oracle."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "frontier" / "circuit_benchmark.json"


def main() -> int:
    from electrical_engineer.eval_runner.score import run_item

    pack = ROOT / "eval" / "gold" / "circuits"
    rows = []
    for item in sorted(pack.iterdir()):
        if not item.is_dir() or item.name.startswith(".") or not (item / "expect.json").is_file():
            continue
        row = run_item(item, run_root=ROOT / "runs" / "_circuit_bench")
        rows.append({"id": item.name, "ok": bool(row.get("ok"))})
    passed = sum(1 for r in rows if r["ok"])
    report = {"subset": "circuits", "total": len(rows), "passed": passed, "items": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
