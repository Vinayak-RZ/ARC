"""B10 benchmark: questions tarball, key separation, naive baseline."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1"


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_build_at_least_sixty_tasks_repro_sha() -> None:
    proc = _run("build_benchmark_v01.py")
    assert proc.returncode == 0, proc.stderr
    meta = json.loads(proc.stdout.strip())
    assert meta["tasks"] >= 60
    q_tar = Path(meta["questions_tarball"])
    digest = hashlib.sha256(q_tar.read_bytes()).hexdigest()
    assert digest == meta["tarball_sha256"]
    proc2 = _run("build_benchmark_v01.py")
    meta2 = json.loads(proc2.stdout.strip())
    assert meta2["tarball_sha256"] == digest


def test_questions_tarball_has_no_answer_key() -> None:
    _run("build_benchmark_v01.py")
    q_tar = BENCH_DIR / "eee-coursework-trap-v0.1-questions.tar.gz"
    with tarfile.open(q_tar) as tar:
        names = tar.getnames()
    assert not any("answer_key" in n for n in names)
    with tarfile.open(q_tar) as tar:
        data = json.loads(tar.extractfile(next(n for n in names if n.endswith("questions.json"))).read())
    task = data["tasks"][0]
    assert task.get("question")
    assert "givens" in task
    assert "answer_schema" in task
    assert "reference" not in task and "oracle" not in json.dumps(task)


def test_oracle_full_naive_low() -> None:
    o = _run("grade_benchmark_v01.py")
    assert o.returncode == 0, o.stdout + o.stderr
    oracle = json.loads(o.stdout)
    n = _run("grade_benchmark_v01.py", "--naive")
    assert n.returncode == 0
    naive = json.loads(n.stdout)
    assert naive["total"] >= 60
    assert oracle["passed"] == oracle["total"]
    assert naive["passed"] < naive["total"] // 2


def test_benchmark_excludes_sealed_paths() -> None:
    _run("build_benchmark_v01.py")
    key = json.loads((BENCH_DIR / "_key" / "answer_key.json").read_text())
    blob = json.dumps(key)
    assert "REFERENCE.json" not in blob
    assert "exam-v" not in blob
