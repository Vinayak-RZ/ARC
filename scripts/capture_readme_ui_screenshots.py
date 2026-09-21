#!/usr/bin/env python3
"""Capture window-sized Arc UI screenshots for README (127.0.0.1:8765).

Rules: fixed viewport only (no full-page scroll), one run visible in the sidebar.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path

_RUN_ID = re.compile(r"^[a-z0-9]{4}-\d{8}T\d{6}Z$")
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 900
MAX_PNG_HEIGHT = 1000

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"
RUNS = ROOT / "runs"
PORT = 8765
HOST = "127.0.0.1"


def _png_height(path: Path) -> int:
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    offset = 8
    while offset < len(raw):
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        chunk = raw[offset + 4 : offset + 8]
        if chunk == b"IHDR":
            _, h = struct.unpack(">II", raw[offset + 8 : offset + 16])
            return int(h)
        offset += 12 + length
    raise ValueError("IHDR missing")


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


def _clear_runs() -> None:
    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)


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


def _diagram_has_ink(path: Path) -> None:
    if path.stat().st_size < 8000:
        raise RuntimeError(f"{path.name}: PNG suspiciously small")
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(path).convert("RGB")
    # Center band where static SVG diagrams render
    band = im.crop((240, 200, 1040, 520))
    dark = sum(1 for r, g, b in band.getdata() if r + g + b < 450)
    if dark / band.size[0] / band.size[1] < 0.002:
        raise RuntimeError(f"{path.name}: diagram band looks blank")


def _capture(page, run_id: str, dest: Path) -> None:
    url = f"http://{HOST}:{PORT}/?run={run_id}"
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector(".shell", timeout=20000)
    page.wait_for_selector(".lab-surface, .empty", timeout=20000)
    if page.locator(".static-diagram-wrap").count():
        page.wait_for_selector(".static-diagram rect, .static-diagram circle", timeout=20000)
        shapes = page.locator(".static-diagram rect, .static-diagram circle").count()
        if shapes < 2:
            raise RuntimeError(f"{dest.name}: expected diagram shapes, saw {shapes}")
    elif page.locator(".flow-wrap .part-node").count():
        page.wait_for_selector(".flow-wrap .part-node", timeout=20000)
    page.wait_for_timeout(1200)
    page.screenshot(
        path=str(dest),
        full_page=False,
        clip={"x": 0, "y": 0, "width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
    )
    height = _png_height(dest)
    if height > MAX_PNG_HEIGHT:
        raise RuntimeError(f"{dest.name} height {height}px exceeds {MAX_PNG_HEIGHT}px cap")
    _diagram_has_ink(dest)


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
                    "vin": 10,
                    "r_ohm": 1000,
                    "l_h": 1e-3,
                    "c_f": 1e-6,
                    "cir": "* series RLC\nV1 1 0 DC 10\nR1 1 2 1k\nL1 2 3 1m\nC1 3 0 1u\n.tran 1m 10m\n.end\n",
                },
                "ui-rlc-full.png",
            ),
            (
                "control-diagram-to-model",
                {
                    "blocks": [{"id": "G", "tf": "10/(s+1)"}, {"id": "H", "tf": "1"}],
                    "unity_feedback": {"forward": "G", "feedback": "H", "negative": True},
                },
                "ui-control-bode-full.png",
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
            (
                "solve-drives-problem",
                {"kind": "dc", "v_dc": 120, "ra_ohm": 1, "k_torque": 0.5, "t_load_nm": 5},
                "ui-drives-full.png",
            ),
        ]
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
            for recipe, problem, name in shots:
                _clear_runs()
                run_id = _run_recipe(recipe, problem)
                dest = MEDIA / name
                print(f"capture {name} run={run_id} viewport={VIEWPORT_WIDTH}x{VIEWPORT_HEIGHT}")
                _capture(page, run_id, dest)
                print(f"  -> {dest.name} height={_png_height(dest)}px")
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)
    print(f"Wrote PNGs under {MEDIA} (all heights <= {MAX_PNG_HEIGHT}px)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
