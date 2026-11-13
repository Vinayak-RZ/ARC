"""B10 benchmark: questions tarball, key separation, naive baseline."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

from electrical_engineer.benchmark_v01.oracle_givens import oracle_eval, oracle_trap
from electrical_engineer.benchmark_v01.public_schema import values_close

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
        assert not any(b in task["givens"] for b in banned)
        ref = key[task["id"]]["reference"]
        schema = task.get("answer_schema") or {}
        key_fields = [f["name"] for f in schema.get("fields", []) if f.get("name") in ref]
        if not key_fields:
            key_fields = list(ref.keys())
        for fname in key_fields:
            val = ref.get(fname)
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                continue
            fval = float(val)
            if abs(fval) < 1e-4 or fval in (0.0, 1.0):
                continue
            field = {"tolerance_rel": 0.001, "tolerance_abs": 1e-6}
            for gval in _floats_in_obj(task["givens"]):
                if values_close(gval, fval, field):
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
        schema = (grading.get("answer_schema") or {}).get("fields") or []
        fields_by = {f["name"]: f for f in schema}

        for k, v in entry["reference"].items():
            if isinstance(v, (int, float)):
                spec = fields_by.get(k) or {"tolerance_rel": 1e-5, "tolerance_abs": 1e-5}
                assert values_close(float(rebuilt[k]), float(v), spec), task_id


_TRAP_HINT_WORDS = re.compile(
    r"ode45|RK4|handwritten|Arc\b|smib_swing|bind unit|must be zero|not b \+ c\*P|python-control|engine",
    re.IGNORECASE,
)


def test_trap_stems_and_rules_defuse_traps() -> None:
    tasks = _load_questions()
    for task in tasks:
        if task["domain"] != "trap":
            continue
        blob = task["question"] + (task.get("answer_schema") or {}).get("rule", "")
        assert not _TRAP_HINT_WORDS.search(blob), task["id"]


def test_schema_fields_match_reference_keys() -> None:
    tasks = {t["id"]: t for t in _load_questions()}
    key = _load_key()
    for task_id, entry in key.items():
        ref = entry["reference"]
        schema_names = {f["name"] for f in tasks[task_id]["answer_schema"].get("fields", [])}
        for fname, val in ref.items():
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                assert fname in schema_names, f"{task_id} missing schema field {fname}"


def test_circuit_gold_provenance_and_independent_oracle() -> None:
    key = _load_key()
    for task_id, entry in key.items():
        if not task_id.startswith("circuits/rlc-natural"):
            continue
        prov = (entry.get("grading") or {}).get("gold_provenance") or {}
        assert prov.get("ok") is True, (task_id, prov)
        assert "convention" in prov
        indep = prov.get("independent_V")
        ref_v = float(entry["reference"]["value"])
        assert indep is not None and abs(float(indep) - ref_v) <= 1e-6, task_id


def test_oracle_full_naive_low() -> None:
    o = _run("grade_benchmark_v01.py")
    assert o.returncode == 0, o.stdout + o.stderr
    n = _run("grade_benchmark_v01.py", "--naive")
    assert n.returncode == 0
    naive = json.loads(n.stdout)
    assert naive["passed"] < naive["total"] // 2
