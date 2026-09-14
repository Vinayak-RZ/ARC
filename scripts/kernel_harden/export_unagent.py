#!/usr/bin/env python3
"""Export corpus traces to one Unagent ``--adapter custom`` payload.

Reads run dirs from ``CORPUS_INDEX.jsonl`` (or ``--run-dir`` repeats) so the
committed advisor input under ``artifacts/kernel-harden/`` is reproducible
instead of hand-assembled.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from electrical_engineer.export.unagent_adapter import load_jsonl, to_unagent_events

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts" / "kernel-harden"


def index_run_dirs(index: Path, limit: int | None) -> list[Path]:
    dirs: list[Path] = []
    for line in index.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        run_dir = row.get("run_dir")
        if run_dir:
            dirs.append(Path(run_dir))
    return dirs[:limit] if limit else dirs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=ARTIFACTS / "CORPUS_INDEX.jsonl")
    parser.add_argument("--run-dir", type=Path, action="append", default=[])
    parser.add_argument("--limit", type=int, default=None, help="first N indexed runs")
    parser.add_argument("--out", type=Path, default=ARTIFACTS / "unagent_events.json")
    args = parser.parse_args()

    run_dirs = list(args.run_dir) or index_run_dirs(args.index, args.limit)
    events: list[dict] = []
    used = 0
    for run_dir in run_dirs:
        trace = load_jsonl(Path(run_dir) / "trace.jsonl")
        if trace:
            events.extend(trace)
            used += 1
    payload = to_unagent_events(events)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    errors = sum(1 for e in payload["events"] if e["error"])
    print(f"runs: {used} events: {len(payload['events'])} hard_errors: {errors} -> {args.out}")
    return 0 if used else 2


if __name__ == "__main__":
    raise SystemExit(main())
