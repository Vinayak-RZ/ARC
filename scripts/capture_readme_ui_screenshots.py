#!/usr/bin/env python3
"""Capture full-page Arc UI screenshots for README (127.0.0.1:8765).

Requires: ui built (`npm run build` in ui/), engines extra for checked runs, ngspice on PATH.
Install browser once: `pip install playwright && playwright install chromium`
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

_RUN_ID = re.compile(r"^[a-z0-9]{4}-\d{8}T\d{6}Z$")

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"
PORT = 8765
HOST = "127.0.0.1"


def _run_recipe(recipe: str, problem: dict) -> str:
    prob = ROOT / "problem.json"
    prob.write_text(json.dumps(problem), encoding="utf-8")
    out = subprocess.check_output(
        [sys.executable, "-m", "electrical_engineer", "run", recipe],
        cwd=ROOT,
        text=True,
    )
    for line in out.splitlines():
        candidate = line.strip()
        if _RUN_ID.match(candidate):
            return candidate
    raise RuntimeError(f"could not parse run_id from:\n{out}")


def _free_port() -> None:
    try:
        subprocess.run(["fuser", "-k", f"{PORT}/tcp"], check=False, capture_output=True)
        time.sleep(1.5)
    except FileNotFoundError:
        pass


def _wait_server(proc: subprocess.Popen, timeout: float = 30.0) -> None:
    import urllib.request

    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("ui server exited early")
        try:
            with urllib.request.urlopen(f"http://{HOST}:{PORT}/api/health", timeout=1) as resp:
                if resp.status == 200:
                    return
        except OSError:
            time.sleep(0.25)
    raise RuntimeError("ui server did not become healthy")


def _capture(page, run_id: str, dest: Path) -> None:
    url = f"http://{HOST}:{PORT}/?run={run_id}"
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector(".topbar", timeout=20000)
    page.wait_for_selector(".lab, .empty", timeout=20000)
    page.wait_for_timeout(1200)
    page.screenshot(path=str(dest), full_page=True)


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install playwright: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    ui_dist = ROOT / "ui" / "dist" / "index.html"
    if not ui_dist.is_file():
        subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")

    MEDIA.mkdir(parents=True, exist_ok=True)
    _free_port()
    env = {**os.environ, "EE_NO_BROWSER": "1"}
    server = subprocess.Popen(
        [sys.executable, "-m", "electrical_engineer", "ui"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_server(server)
        shots: list[tuple[str, dict, str]] = [
            (
                "simulate-circuit",
                {
                    "kind": "series_rlc",
                    "cir": "* series RLC\nV1 1 0 DC 10\nR1 1 2 1k\nL1 2 3 1m\nC1 3 0 1u\n.tran 1m 10m\n.end\n",
                },
                "ui-rlc-full.png",
            ),
            (
                "solve-control-problem",
                {"tf": "1/(s+1)"},
                "ui-control-bode-full.png",
            ),
            (
                "control-diagram-to-model",
                {
                    "blocks": [{"id": "G", "tf": "10/(s+1)"}, {"id": "H", "tf": "1"}],
                    "unity_feedback": {"forward": "G", "feedback": "H", "negative": True},
                },
                "ui-block-diagram-full.png",
            ),
            (
                "simulate-power-fault",
                {"fault_type": "LG", "z1_pu": 0.1, "z2_pu": 0.1, "z0_pu": 0.3},
                "ui-power-fault-full.png",
            ),
            (
                "study-protection-setting",
                {
                    "ct_primary_a": 300,
                    "ct_secondary_a": 5,
                    "relay_pickup_a": 2,
                    "fault_current_a": 800,
                },
                "ui-protection-full.png",
            ),
        ]
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            for recipe, problem, name in shots:
                run_id = _run_recipe(recipe, problem)
                dest = MEDIA / name
                print(f"capture {name} run={run_id}")
                _capture(page, run_id, dest)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)
    print(f"Wrote PNGs under {MEDIA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
