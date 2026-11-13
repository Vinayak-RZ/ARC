"""RLVR environment import, observations, anti-gaming, and rollouts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from electrical_engineer.rlvr_env import (
    ArcRlvrEnv,
    contract_json,
    list_trap_ids,
    load_manifest,
    oracle_submission,
    run_dummy_rollout,
    run_naive_rollout,
)
from electrical_engineer.rlvr_env.rewards import grade_trap


def test_manifest_has_ten_traps() -> None:
    m = load_manifest()
    assert m["version"] == "0.1"
    assert len(m["traps"]) == 10


def test_reset_includes_question_givens_schema() -> None:
    env = ArcRlvrEnv()
    obs = env.reset(seed=17, trap_id="T6")
    assert obs["trap_id"] == "T6"
    assert "PD_MW" in obs["givens"]
    assert obs["question"]
    assert obs["answer_schema"]["fields"]
    assert obs["givens_units"]


def test_oracle_rollout_all_pass() -> None:
    report = run_dummy_rollout()
    assert report["episodes"] == 10
    assert report["passed"] == 10


def test_naive_rollout_low_score() -> None:
    report = run_naive_rollout()
    assert report["passed"] <= 2


def test_reward_hacking_empty_zero() -> None:
    givens = {"PD_MW": 500.0, "unit1_MW": 120.0}
    ok, reward = grade_trap("T6", {}, givens=givens)
    assert ok is False and reward == 0.0


def test_reward_hacking_constants_zero() -> None:
    givens = {"PD_MW": 500.0, "unit1_MW": 120.0}
    _ok, reward = grade_trap("T6", {"unit2_MW": 1.0, "unit2_IC": 1.0, "lambda": 1.0}, givens=givens)
    assert reward == 0.0


def test_reward_hacking_flags_only_zero() -> None:
    env = ArcRlvrEnv()
    obs = env.reset(seed=99, trap_id="T9")
    ok, reward = grade_trap("T9", {"integrator": "rk4", "forbidden_solver_used": False}, givens=obs["givens"])
    assert ok is False and reward == 0.0


def test_reward_hacking_copied_givens_zero() -> None:
    env = ArcRlvrEnv()
    obs = env.reset(seed=88, trap_id="T10")
    sub = {k: v for k, v in obs["givens"].items()}
    ok, reward = grade_trap("T10", sub, givens=obs["givens"])
    assert ok is False and reward == 0.0


def test_oracle_beats_naive_per_trap() -> None:
    env = ArcRlvrEnv()
    for i, tid in enumerate(list_trap_ids()):
        obs = env.reset(seed=1000 + i, trap_id=tid)
        _, r_oracle = grade_trap(tid, oracle_submission(tid, obs["givens"]), givens=obs["givens"])
        _, r_naive = grade_trap(tid, __import__(
            "electrical_engineer.rlvr_env.rewards", fromlist=["naive_submission"]
        ).naive_submission(tid, obs["givens"]), givens=obs["givens"])
        assert r_oracle >= r_naive


def test_import_and_rollout_script() -> None:
    root = Path(__file__).resolve().parents[2]
    proc = subprocess.run(
        [sys.executable, str(root / "scripts/rlvr_dummy_rollout.py")],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "rlvr_env_manifest" in proc.stdout


def test_contract_json() -> None:
    c = contract_json()
    assert c["rlvr_env_manifest"]["traps"] == 10
    assert c["rlvr_env_manifest"]["held_out_seed_min"] == 9000
