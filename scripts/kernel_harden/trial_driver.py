#!/usr/bin/env python3
"""Host-style trial driver: load scenario JSON → execute → graded index row.

A row is PASS only if the run's ``unchecked`` flag and ``unchecked_reason``
match the scenario's ``expect`` block. Scenarios whose expectation assumes an
absent optional provider are SKIP when that provider is installed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from electrical_engineer.capabilities import provider_installed
from electrical_engineer.runner.execute import execute

ROOT = Path(__file__).resolve().parents[2]


def load_scenario(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def grade(expect: dict, unchecked: bool, reason: str | None) -> str:
    for provider in expect.get("requires") or []:
        if provider_installed(provider):
            return "skip"
    if bool(expect.get("unchecked")) != unchecked:
        return "fail"
    return "pass" if expect.get("reason") == reason else "fail"


def run_one(scenario: dict, run_root: Path) -> dict:
    recipe_id = scenario["recipe_id"]
    out = execute(recipe_id, run_root=run_root, problem=scenario.get("problem") or {})
    run_dir = Path(out["run_dir"])
    trace = run_dir / "trace.jsonl"
    obs = json.loads((run_dir / "observation.json").read_text(encoding="utf-8"))
    unchecked = bool(out["summary"].get("unchecked"))
    reason = obs.get("unchecked_reason")
    expect = scenario.get("expect") or {}
    return {
        "scenario_id": scenario.get("id"),
        "pack": scenario.get("pack"),
        "recipe_id": recipe_id,
        "run_id": out["run_id"],
        "run_dir": str(run_dir),
        "trace_path": str(trace) if trace.is_file() else None,
        "unchecked": unchecked,
        "unchecked_reason": reason,
        "expected_unchecked": expect.get("unchecked"),
        "expected_reason": expect.get("reason"),
        "grade": grade(expect, unchecked, reason) if expect else "ungraded",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path, nargs="+", help="scenario JSON path(s)")
    parser.add_argument("--run-root", type=Path, default=ROOT / "artifacts" / "kernel-harden" / "raw")
    parser.add_argument("--index", type=Path, default=ROOT / "artifacts" / "kernel-harden" / "CORPUS_INDEX.jsonl")
    parser.add_argument("--truncate", action="store_true", help="start a fresh index")
    args = parser.parse_args()
    args.run_root.mkdir(parents=True, exist_ok=True)
    args.index.parent.mkdir(parents=True, exist_ok=True)
    if args.truncate:
        args.index.write_text("", encoding="utf-8")
    failures = 0
    for path in args.scenario:
        row = run_one(load_scenario(path), args.run_root)
        with args.index.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        print(json.dumps(row))
        if row["grade"] == "fail" or not row["trace_path"]:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
