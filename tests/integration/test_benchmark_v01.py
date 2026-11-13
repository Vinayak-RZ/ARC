"""B10 benchmark: questions tarball, key separation, naive baseline."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from electrical_engineer.benchmark_v01.oracle_givens import oracle_eval, oracle_trap
from electrical_engineer.benchmark_v01.public_schema import values_close

ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = ROOT / "scripts" / "build_benchmark_v01.py"
GRADE_SCRIPT = ROOT / "scripts" / "grade_benchmark_v01.py"


@pytest.fixture(scope="session")
def benchmark_v01_build(tmp_path_factory: pytest.TempPathFactory) -> dict:
    out_dir = tmp_path_factory.mktemp("benchmark_v01")
    env = {**os.environ, "ARC_BENCHMARK_V01_DIR": str(out_dir)}
    proc = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    meta = json.loads(proc.stdout.strip())
    return {
        "out_dir": out_dir,
        "meta": meta,
        "key_path": out_dir / "_key" / "answer_key.json",
        "tarball": Path(meta["questions_tarball"]),
        "env": env,
    }


@pytest.fixture(scope="session")
def benchmark_tasks(benchmark_v01_build: dict) -> list[dict]:
    with tarfile.open(benchmark_v01_build["tarball"]) as tar:
        qname = next(m for m in tar.getnames() if m.endswith("questions.json"))
        data = json.loads(tar.extractfile(qname).read())
    return data["tasks"]


@pytest.fixture(scope="session")
def benchmark_answers(benchmark_v01_build: dict) -> dict:
    key = json.loads(benchmark_v01_build["key_path"].read_text())
    return key["answers"]


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


def test_build_at_least_sixty_unique_repro_sha(benchmark_v01_build: dict) -> None:
    meta = benchmark_v01_build["meta"]
    assert meta["tasks"] >= 60
    assert meta["unique_tasks"] == meta["tasks"]
    q_tar = benchmark_v01_build["tarball"]
    digest = hashlib.sha256(q_tar.read_bytes()).hexdigest()
    assert digest == meta["tarball_sha256"]
    proc = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=benchmark_v01_build["env"],
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    meta2 = json.loads(proc.stdout.strip())
    assert meta2["tarball_sha256"] == digest


def test_questions_tarball_has_no_answer_key_or_leaks(
    benchmark_tasks: list[dict], benchmark_answers: dict
) -> None:
    banned = {"expected", "tol", "pick_sigma", "value_key", "solver", "check_kind"}
    for task in benchmark_tasks:
        assert not any(b in task["givens"] for b in banned)
        ref = benchmark_answers[task["id"]]["reference"]
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


def test_rebuild_answers_from_givens_only(benchmark_answers: dict) -> None:
    for task_id, entry in benchmark_answers.items():
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


def test_trap_stems_and_rules_defuse_traps(benchmark_tasks: list[dict]) -> None:
    for task in benchmark_tasks:
        if task["domain"] != "trap":
            continue
        blob = task["question"] + (task.get("answer_schema") or {}).get("rule", "")
        assert not _TRAP_HINT_WORDS.search(blob), task["id"]


def test_schema_fields_match_reference_keys(
    benchmark_tasks: list[dict], benchmark_answers: dict
) -> None:
    tasks = {t["id"]: t for t in benchmark_tasks}
    for task_id, entry in benchmark_answers.items():
        ref = entry["reference"]
        schema_names = {f["name"] for f in tasks[task_id]["answer_schema"].get("fields", [])}
        for fname, val in ref.items():
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                assert fname in schema_names, f"{task_id} missing schema field {fname}"


def test_circuit_gold_provenance_and_independent_oracle(benchmark_answers: dict) -> None:
    for task_id, entry in benchmark_answers.items():
        if not task_id.startswith("circuits/rlc-natural"):
            continue
        prov = (entry.get("grading") or {}).get("gold_provenance") or {}
        assert prov.get("ok") is True, (task_id, prov)
        assert "convention" in prov
        indep = prov.get("independent_V")
        ref_v = float(entry["reference"]["value"])
        assert indep is not None and abs(float(indep) - ref_v) <= 1e-6, task_id
        if prov.get("ngspice_V") is not None:
            assert prov.get("ngspice_agree") is True, (task_id, prov)


S416_GIVENS = {
    "r": 212.0,
    "l": 0.106,
    "c": 1.06e-05,
    "vc0": 12.72,
    "i0": 0.053,
    "t": 0.00106,
}
S416_ORACLE_V = 0.09312035050446156


def test_rlc_natural_s416_ngspice_matches_oracle() -> None:
    from electrical_engineer.benchmark_v01.circuit_gold import (
        parallel_rlc_vc_independent,
        parallel_rlc_vc_ngspice,
    )
    from electrical_engineer.engines.spice_runner import spice_available

    if not spice_available():
        pytest.skip("ngspice/PySpice not installed")
    g = S416_GIVENS
    indep = parallel_rlc_vc_independent(**g)
    assert abs(indep - S416_ORACLE_V) <= 1e-6
    spice = parallel_rlc_vc_ngspice(**g)
    assert spice is not None
    assert values_close(
        S416_ORACLE_V,
        spice,
        {"tolerance_rel": 0.005, "tolerance_abs": 1e-3},
    ), spice


def test_oracle_full_naive_low(benchmark_v01_build: dict) -> None:
    env = benchmark_v01_build["env"]
    o = subprocess.run(
        [sys.executable, str(GRADE_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert o.returncode == 0, o.stdout + o.stderr
    n = subprocess.run(
        [sys.executable, str(GRADE_SCRIPT), "--naive"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert n.returncode == 0
    naive = json.loads(n.stdout)
    assert naive["passed"] < naive["total"] // 2
