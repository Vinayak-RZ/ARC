"""RLVR environment import, manifest, and oracle rollout."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from electrical_engineer.rlvr_env import (
    ArcRlvrEnv,
    contract_json,
    list_trap_ids,
    load_manifest,
    run_dummy_rollout,
)


def test_manifest_has_ten_traps() -> None:
    m = load_manifest()
    assert m["version"] == "0.1"
    assert len(m["traps"]) == 10
    assert list_trap_ids() == [f"T{i}" for i in range(1, 11)]


def test_contract_json_matches_manifest() -> None:
    c = contract_json()
    assert c["rlvr_env_manifest"]["version"] == "0.1"
    assert c["rlvr_env_manifest"]["traps"] == 10


def test_env_reset_step_oracle_reward() -> None:
    env = ArcRlvrEnv()
    obs = env.reset(seed=7)
    assert obs["trap_id"] in list_trap_ids()
    from electrical_engineer.rlvr_env import oracle_submission

    sub = oracle_submission(obs["trap_id"])
    _, reward, done, info = env.step({"trap_id": obs["trap_id"], "submission": sub})
    assert done is True
    assert reward == 1.0
    assert info["passed"] is True


def test_run_dummy_rollout_all_pass() -> None:
    report = run_dummy_rollout()
    assert report["episodes"] == 10
    assert report["passed"] == 10
    assert report["mean_reward"] == 1.0


def test_dummy_rollout_script_exit_zero() -> None:
    root = Path(__file__).resolve().parents[2]
    proc = subprocess.run(
        [sys.executable, str(root / "scripts/rlvr_dummy_rollout.py")],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_import_snippet() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from electrical_engineer.rlvr_env import ArcRlvrEnv, contract_json; "
                "print(contract_json())"
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "rlvr_env_manifest" in proc.stdout
