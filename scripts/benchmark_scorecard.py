#!/usr/bin/env python3
"""Emit SCORECARD rows from real Arc engine/grader runs (B10)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_json(stdout: str) -> dict:
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(text.splitlines()[-1])


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_benchmark_v01.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if build.returncode != 0:
        print(build.stderr or build.stdout, file=sys.stderr)
        return build.returncode
    build_meta = _load_json(build.stdout)
    oracle = subprocess.run(
        [sys.executable, str(ROOT / "scripts/grade_benchmark_v01.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    naive = subprocess.run(
        [sys.executable, str(ROOT / "scripts/grade_benchmark_v01.py"), "--naive"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    rlvr = subprocess.run(
        [sys.executable, str(ROOT / "scripts/rlvr_dummy_rollout.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    oracle_report = _load_json(oracle.stdout)
    naive_report = _load_json(naive.stdout)
    rlvr_report = _load_json(rlvr.stdout)
    rows = [
        {
            "metric": "benchmark_questions_sha256",
            "value": build_meta.get("tarball_sha256"),
            "source": "scripts/build_benchmark_v01.py",
        },
        {
            "metric": "benchmark_task_count",
            "value": str(build_meta.get("tasks")),
            "source": "scripts/build_benchmark_v01.py",
        },
        {
            "metric": "benchmark_oracle_grade",
            "value": f"{oracle_report.get('passed', 0)}/{oracle_report.get('total', 0)}",
            "source": "scripts/grade_benchmark_v01.py",
        },
        {
            "metric": "benchmark_naive_trap_baseline",
            "value": f"{naive_report.get('passed', 0)}/{naive_report.get('total', 0)}",
            "source": "scripts/grade_benchmark_v01.py --naive",
        },
        {
            "metric": "bare_agent",
            "value": "pending live run",
            "source": "owner",
        },
        {
            "metric": "rlvr_dummy_rollout",
            "value": f"{rlvr_report.get('passed', 0)}/{rlvr_report.get('episodes', 0)}",
            "source": "scripts/rlvr_dummy_rollout.py",
        },
    ]
    contract = {
        "tarball_sha256": build_meta.get("tarball_sha256"),
        "scorecard_rows": rows,
    }
    print(json.dumps(contract, indent=2))
    out = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1" / "scorecard.json"
    out.write_text(json.dumps(contract, indent=2))
    return 0 if oracle.returncode == 0 and rlvr.returncode == 0 and naive.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
