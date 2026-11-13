#!/usr/bin/env python3
"""Emit SCORECARD rows from real Arc engine/grader runs (B10)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
    build_meta = json.loads(build.stdout.strip().splitlines()[-1])
    sha = build_meta["sha256"]
    grade = subprocess.run(
        [sys.executable, str(ROOT / "scripts/grade_benchmark_v01.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    grade_report = json.loads(grade.stdout) if grade.stdout.strip() else {}
    rlvr = subprocess.run(
        [sys.executable, str(ROOT / "scripts/rlvr_dummy_rollout.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    rlvr_report = json.loads(rlvr.stdout) if rlvr.stdout.strip() else {}
    circuit = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_circuit_benchmark.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    circuit_report = json.loads(circuit.stdout) if circuit.stdout.strip() else {}
    psa = subprocess.run(
        ["uv", "run", "electrical-engineer", "eval", "--pack", "power"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    rows = [
        {
            "metric": "benchmark_tarball_sha256",
            "value": sha,
            "source": "scripts/build_benchmark_v01.py",
        },
        {
            "metric": "benchmark_oracle_grade",
            "value": f"{grade_report.get('passed', 0)}/{grade_report.get('total', 0)}",
            "source": "scripts/grade_benchmark_v01.py",
        },
        {
            "metric": "rlvr_dummy_rollout",
            "value": f"{rlvr_report.get('passed', 0)}/{rlvr_report.get('episodes', 0)}",
            "source": "scripts/rlvr_dummy_rollout.py",
        },
        {
            "metric": "circuit_subset",
            "value": f"{circuit_report.get('passed', 0)}/{circuit_report.get('total', 0)}",
            "source": "scripts/run_circuit_benchmark.py",
        },
        {
            "metric": "psa_power_pack_cli",
            "value": "PASS" if psa.returncode == 0 else f"FAIL({psa.returncode})",
            "source": "electrical-engineer eval --pack power",
        },
    ]
    contract = {"tarball_sha256": sha, "scorecard_rows": rows}
    print(json.dumps(contract, indent=2))
    out = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1" / "scorecard.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(contract, indent=2))
    return 0 if grade.returncode == 0 and rlvr.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
