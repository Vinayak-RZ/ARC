#!/usr/bin/env python3
"""Count completed corpus rows that include a trace_path."""

from __future__ import annotations

import json
from pathlib import Path

INDEX = Path(__file__).resolve().parents[2] / "artifacts" / "kernel-harden" / "CORPUS_INDEX.jsonl"


def main() -> None:
    completed = 0
    if INDEX.is_file():
        for line in INDEX.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("trace_path"):
                completed += 1
    print(f"completed: {completed}")


if __name__ == "__main__":
    main()
