#!/usr/bin/env python3
"""Orchestrate round-12 UX capture (main pass + collab + postflight)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
CONTROL_STUDIO = ROOT / ".electrical-engineer" / "control_studio"
HOST = "127.0.0.1"
PORT = 8765


def _wait_health() -> None:
    for _ in range(120):
        try:
            with urllib.request.urlopen(f"http://{HOST}:{PORT}/api/health", timeout=2):
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError("UI not healthy")


def main() -> int:
    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)
    if CONTROL_STUDIO.is_dir():
        shutil.rmtree(CONTROL_STUDIO)
    subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")
    env = {**os.environ, "EE_NO_BROWSER": "1"}
    server = subprocess.Popen(
        [sys.executable, "-m", "electrical_engineer", "ui"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_health()
        for script in (
            [sys.executable, str(ROOT / "scripts" / "capture_ux_review_round.py"), "--round", "12"],
            [sys.executable, str(ROOT / "scripts" / "capture_round_12_collab.py")],
        ):
            print(">>>", " ".join(script))
            subprocess.check_call(script, cwd=ROOT)
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "round_12_postflight.py")], cwd=ROOT)
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())