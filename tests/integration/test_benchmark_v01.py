"""B10 benchmark: questions tarball, key separation, naive baseline."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path

from electrical_engineer.benchmark_v01.oracle_givens import oracle_eval, oracle_trap

ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1"
KEY_PATH = BENCH_DIR / "_key" / "answer_key.json"


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _ensure_built() -> dict:
    proc = _run("build_benchmark_v01.py")
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip())


def _load_questions() -> list[dict]:
    _ensure_built()
    with tarfile.open(BENCH_DIR / "eee-coursework-trap-v0.1-questions.tar.gz") as tar:
        data = json.loads(tar.extractfile(next(m for m in tar.getnames() if m.endswith("questions.json"))).read())
    return data["tasks"]


def _load_key() -> dict:
    return json.loads(KEY_PATH.read_text())["answers"]


def _floats_in_obj(obj, parent_key: str | None = None) -> list[float]:
    out: list[float] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in {"pmin", "pmax", "expected", "tol"}:
                continue
            out.extend(_floats_in_obj(v, k))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_floats_in_obj(v, parent_key))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out.append(float(obj))
    return out


def test_build_at_least_sixty_unique_repro_sha() -> None:
    meta = _ensure_built()
    assert meta["tasks"] >= 60
    assert meta["unique_tasks"] == meta["tasks"]
    q_tar = Path(meta["questions_tarball"])
    digest = hashlib.sha256(q_tar.read_bytes()).hexdigest()
    assert digest == meta["tarball_sha256"]
    meta2 = _ensure_built()
    assert meta2["tarball_sha256"] == digest


def test_questions_tarball_has_no_answer_key_or_leaks() -> None:
    tasks = _load_questions()
    key = _load_key()
    banned = {"expected", "tol", "pick_sigma", "value_key", "solver", "check_kind"}
    for task in tasks:
        blob = json.dumps({"q": task["question"], "g": task["givens"]})
        assert not any(b in task["givens"] for b in banned)
        ref = key[task["id"]]["reference"]
        schema = task.get("answer_schema") or {}
        key_fields = [f["name"] for f in schema.get("fields", []) if f.get("name") in ref]
        if not key_fields:
            key_fields = list(ref.keys())
        tol_by = {f["name"]: float(f.get("tolerance", 1e-3)) for f in schema.get("fields", [])}
        public_blob = (task["question"] + json.dumps(task["givens"], sort_keys=True)).lower()
        for fname in key_fields:
            val = ref.get(fname)
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                continue
            fval = float(val)
            if abs(fval) < 1e-4 or fval in (0.0, 1.0):
                continue
            tol = tol_by.get(fname, 1e-3)
            for gval in _floats_in_obj(task["givens"]):
                if abs(gval - fval) <= max(tol, 1e-6 * max(1.0, abs(fval))):
                    raise AssertionError(
                        f"answer leak field {fname}={val} in givens for {task['id']}"
                    )
        assert task.get("question")
        assert "reference" not in task


def test_rebuild_answers_from_givens_only() -> None:
    key = _load_key()
    for task_id, entry in key.items():
        grading = entry["grading"]
        givens = grading.get("public_givens") or grading.get("givens") or {}
        if grading.get("trap_id"):
            rebuilt = oracle_trap(grading["trap_id"], givens)
        else:
            rebuilt = oracle_eval(givens, grading)
        for k, v in entry["reference"].items():
            if isinstance(v, (int, float)):
                assert abs(float(rebuilt[k]) - float(v)) < 1e-5, task_id


def test_oracle_full_naive_low() -> None:
    o = _run("grade_benchmark_v01.py")
    assert o.returncode == 0, o.stdout + o.stderr
    n = _run("grade_benchmark_v01.py", "--naive")
    assert n.returncode == 0
    naive = json.loads(n.stdout)
    assert naive["passed"] < naive["total"] // 2
