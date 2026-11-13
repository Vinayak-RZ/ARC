"""B10 benchmark build, checksum, and grader."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1"


def _run(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_build_benchmark_produces_checksum() -> None:
    proc = _run("build_benchmark_v01.py")
    assert proc.returncode == 0, proc.stderr
    meta = json.loads(proc.stdout.strip())
    tarball = Path(meta["tarball"])
    assert tarball.is_file()
    digest = hashlib.sha256(tarball.read_bytes()).hexdigest()
    assert digest == meta["sha256"]
    manifest = json.loads((BENCH_DIR / "manifest.json").read_text())
    assert manifest["sha256"] == digest
    assert meta["tasks"] >= 16


def test_grade_oracle_answers_full_pass() -> None:
    proc = _run("grade_benchmark_v01.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = json.loads(proc.stdout)
    assert report["passed"] == report["total"]


def test_benchmark_excludes_sealed_paths() -> None:
    _run("build_benchmark_v01.py")
    key = json.loads((BENCH_DIR / "_stage" / "answer_key.json").read_text())
    blob = json.dumps(key)
    assert "live-ab" not in blob
    assert "exam-v" not in blob
    assert "REFERENCE.json" not in blob
