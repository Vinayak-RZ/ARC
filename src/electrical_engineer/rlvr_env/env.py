"""Gym-style RLVR environment over Arc trap suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.rlvr_env import problems as trap_problems
from electrical_engineer.rlvr_env.rewards import grade_trap, naive_submission, oracle_submission
from electrical_engineer.rlvr_env.schema import HELD_OUT_SEED_MIN, is_held_out_seed

_MANIFEST = Path(__file__).resolve().parent / "manifest.json"


class ArcRlvrEnv:
    """reset() returns full problem + givens; step() grades numeric submission only."""

    def __init__(self, *, manifest_path: Path | None = None) -> None:
        path = manifest_path or _MANIFEST
        self._manifest = json.loads(path.read_text(encoding="utf-8"))
        self._traps = [t["id"] for t in self._manifest["traps"]]
        self._episode_trap: str | None = None
        self._givens: dict[str, Any] | None = None
        self._seed: int | None = None
        self._step_count = 0
        self._terminated = False

    def reset(self, *, seed: int | None = None, trap_id: str | None = None) -> dict[str, Any]:
        if seed is None:
            seed = 0
        self._seed = int(seed)
        self._episode_trap = trap_id or trap_problems.default_trap_for_seed(self._seed)
        if self._episode_trap not in self._traps:
            raise ValueError(f"unknown trap_id {self._episode_trap!r}")
        self._step_count = 0
        self._terminated = False
        obs = trap_problems.build_observation(self._episode_trap, self._seed)
        self._givens = obs["givens"]
        obs["held_out_eval"] = is_held_out_seed(self._seed)
        obs["eval_seed_range"] = {"min": HELD_OUT_SEED_MIN, "max": 9999}
        return obs

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool, dict[str, Any]]:
        if self._terminated or self._episode_trap is None or self._givens is None:
            raise RuntimeError("call reset() before step()")
        self._step_count += 1
        trap_id = str(action.get("trap_id") or self._episode_trap)
        submission = dict(action.get("submission") or action)
        passed, reward = grade_trap(trap_id, submission, givens=self._givens)
        self._terminated = True
        info = {
            "trap_id": trap_id,
            "passed": passed,
            "steps": self._step_count,
            "seed": self._seed,
        }
        return {"trap_id": trap_id, "passed": passed}, reward, True, info

    def manifest_contract(self) -> dict[str, Any]:
        return {
            "rlvr_env_manifest": {
                "version": self._manifest.get("version", "0.1"),
                "traps": len(self._traps),
                "held_out_seed_min": HELD_OUT_SEED_MIN,
            }
        }


def run_dummy_rollout(*, seed: int = 42) -> dict[str, Any]:
    env = ArcRlvrEnv()
    rows: list[dict[str, Any]] = []
    for i, trap_id in enumerate(env._traps):
        obs = env.reset(seed=seed + i, trap_id=trap_id)
        sub = oracle_submission(trap_id, obs["givens"])
        _, reward, _, info = env.step({"trap_id": trap_id, "submission": sub})
        rows.append({"trap_id": trap_id, "reward": reward, "passed": info["passed"]})
    passed = sum(1 for r in rows if r["passed"])
    return {
        "episodes": len(rows),
        "passed": passed,
        "mean_reward": sum(r["reward"] for r in rows) / len(rows),
        "rows": rows,
        "contract": env.manifest_contract(),
    }


def run_naive_rollout(*, seed: int = 42) -> dict[str, Any]:
    env = ArcRlvrEnv()
    rows: list[dict[str, Any]] = []
    for i, trap_id in enumerate(env._traps):
        obs = env.reset(seed=seed + i, trap_id=trap_id)
        sub = naive_submission(trap_id, obs["givens"])
        _, reward, _, info = env.step({"trap_id": trap_id, "submission": sub})
        rows.append({"trap_id": trap_id, "reward": reward, "passed": info["passed"]})
    passed = sum(1 for r in rows if r["passed"])
    return {
        "episodes": len(rows),
        "passed": passed,
        "mean_reward": sum(r["reward"] for r in rows) / max(len(rows), 1),
        "rows": rows,
    }
