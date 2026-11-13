#!/usr/bin/env python3
"""Oracle-policy rollout through ArcRlvrEnv (B7 CI gate)."""

from __future__ import annotations

import json

from electrical_engineer.rlvr_env import run_dummy_rollout


def main() -> int:
    report = run_dummy_rollout()
    print(json.dumps(report, indent=2))
    if report["passed"] != report["episodes"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
