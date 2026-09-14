#!/usr/bin/env python3
"""Host-style trial driver: load scenario JSON → execute → index row."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from electrical_engineer.runner.execute import execute  # noqa: E402


def load_scenario(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_one(scenario: dict, run_root: Path) -> dict:
    recipe_id = scenario["recipe_id"]
    problem = scenario.get("problem") or {}
    out = execute(recipe_id, run_root=run_root, problem=problem)
    run_dir = Path(out["run_dir"])
    trace = run_dir / "trace.jsonl"
    obs = json.loads((run_dir / "observation.json").read_text(encoding="utf-8"))
    summary = out["summary"]
    return {
        "scenario_id": scenario.get("id"),
        "pack": scenario.get("pack"),
        "recipe_id": recipe_id,
        "run_id": out["run_id"],
        "run_dir": str(run_dir),
        "trace_path": str(trace) if trace.is_file() else None,
        "unchecked": bool(summary.get("unchecked")),
        "unchecked_reason": obs.get("unchecked_reason"),
        "ok": summary.get("unchecked") is False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path, help="Path to scenario JSON")
    parser.add_argument("--run-root", type=Path, default=ROOT / "artifacts" / "kernel-harden" / "raw")
    parser.add_argument("--index", type=Path, default=ROOT / "artifacts" / "kernel-harden" / "CORPUS_INDEX.jsonl")
    args = parser.parse_args()
    scenario = load_scenario(args.scenario)
    args.run_root.mkdir(parents=True, exist_ok=True)
    args.index.parent.mkdir(parents=True, exist_ok=True)
    row = run_one(scenario, args.run_root)
    with args.index.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
    print(json.dumps(row))
    return 0 if row.get("trace_path") else 2


if __name__ == "__main__":
    raise SystemExit(main())
