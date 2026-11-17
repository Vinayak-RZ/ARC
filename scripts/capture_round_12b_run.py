#!/usr/bin/env python3
"""Orchestrate round-12b UX capture (main pass + collab + postflight)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
CONTROL_STUDIO = ROOT / ".electrical-engineer" / "control_studio"
OUT = ROOT / "artifacts" / "ux-review" / "round-12b"
CAPTURE_ENV = {**os.environ, "ARC_UX_CAPTURE_DIR": "round-12b"}


def main() -> int:
    if OUT.is_dir():
        shutil.rmtree(OUT)
    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)
    if CONTROL_STUDIO.is_dir():
        shutil.rmtree(CONTROL_STUDIO)
    subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")
    collab_env = {**CAPTURE_ENV, "ROUND12_START_UI": "1"}
    for script, env in (
        (
            [
                sys.executable,
                str(ROOT / "scripts" / "capture_ux_review_round.py"),
                "--round",
                "12",
                "--subdir",
                "round-12b",
            ],
            CAPTURE_ENV,
        ),
        ([sys.executable, str(ROOT / "scripts" / "capture_round_12_collab.py")], collab_env),
    ):
        print(">>>", " ".join(script))
        subprocess.check_call(script, cwd=ROOT, env=env)
    env_pf = {
        **CAPTURE_ENV,
        "ROUND12_CI_RUN_ID": os.environ.get("ROUND12_CI_RUN_ID", ""),
        "ROUND12_CI_STATUS": os.environ.get("ROUND12_CI_STATUS", "success"),
    }
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "round_12_postflight.py")],
        cwd=ROOT,
        env=env_pf,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())