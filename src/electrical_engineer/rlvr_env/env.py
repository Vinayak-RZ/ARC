"""Gym-style RLVR environment over Arc trap suite."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

import yaml

from electrical_engineer.rlvr_env.rewards import grade_trap, oracle_submission

_MANIFEST = Path(__file__).resolve().parent / "manifest.json"
_PROMPTS = Path(__file__).resolve().parents[3] / "proofs" / "ablation" / "trap_prompts.yaml"


class ArcRlvrEnv:
    """reset() samples a trap problem; step() grades a submission dict."""

    def __init__(self, *, manifest_path: Path | None = None) -> None:
        path = manifest_path or _MANIFEST
        self._manifest = json.loads(path.read_text(encoding="utf-8"))
        self._traps = [t["id"] for t in self._manifest["traps"]]
        self._prompts = self._load_prompts()
        self._rng = random.Random(0)
        self._episode_trap: str | None = None
        self._step_count = 0
        self._terminated = False

    @staticmethod
    def _load_prompts() -> dict[str, Any]:
        if not _PROMPTS.is_file():
            return {}
        return yaml.safe_load(_PROMPTS.read_text(encoding="utf-8")).get("traps") or {}

    def reset(self, *, seed: int | None = None) -> dict[str, Any]:
        if seed is not None:
            self._rng.seed(seed)
        self._episode_trap = self._rng.choice(self._traps)
        self._step_count = 0
        self._terminated = False
        meta = self._prompts.get(self._episode_trap) or {}
        return {
            "trap_id": self._episode_trap,
            "prompt": meta.get("prompt", f"Trap {self._episode_trap}"),
            "engine": next(
                (t["engine"] for t in self._manifest["traps"] if t["id"] == self._episode_trap),
                None,
            ),
        }

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool, dict[str, Any]]:
        if self._terminated or self._episode_trap is None:
            raise RuntimeError("call reset() before step()")
        self._step_count += 1
        trap_id = str(action.get("trap_id") or self._episode_trap)
        submission = dict(action.get("submission") or action)
        passed, reward = grade_trap(trap_id, submission)
        self._terminated = True
        info = {"trap_id": trap_id, "passed": passed, "steps": self._step_count}
        return {"trap_id": trap_id, "passed": passed}, reward, True, info

    def manifest_contract(self) -> dict[str, Any]:
        return {
            "rlvr_env_manifest": {
                "version": self._manifest.get("version", "0.1"),
                "traps": len(self._traps),
            }
        }


def run_dummy_rollout(*, seed: int = 42) -> dict[str, Any]:
    """One episode per trap with oracle submissions (CI smoke)."""
    env = ArcRlvrEnv()
    rows: list[dict[str, Any]] = []
    for i, trap_id in enumerate(env._traps):
        env.reset(seed=seed + i)
        env._episode_trap = trap_id
        sub = oracle_submission(trap_id)
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
