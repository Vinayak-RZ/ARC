#!/usr/bin/env python3
"""Capture PRODUCT_SPEC section 5 screenshots at 1280x800."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path("/opt/cursor/artifacts")
PORT = 8765
HOST = "127.0.0.1"
W, H = 1280, 800


def _wait_server(proc: subprocess.Popen, timeout: float = 45.0) -> None:
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
    raise RuntimeError("ui server not healthy")


def _run_example(example_id: str) -> str:
    import urllib.request

    req = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/examples/{example_id}/run",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=b"{}",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode())
    rid = body.get("run_id")
    if not rid:
        raise RuntimeError(f"no run_id for {example_id}: {body}")
    return str(rid)


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    ui_dist = ROOT / "ui" / "dist" / "index.html"
    if not ui_dist.is_file():
        subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")

    OUT.mkdir(parents=True, exist_ok=True)
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
        run_id = _run_example("divider")
        shots: list[tuple[str, callable]] = []

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": W, "height": H})

            def snap(name: str) -> None:
                path = OUT / name
                page.screenshot(path=str(path), full_page=False)
                print(f"wrote {path}")

            def go(query: str = "") -> None:
                page.goto(f"http://{HOST}:{PORT}/{query}", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_selector(".product-shell", timeout=30000)
                page.wait_for_timeout(600)

            go("?view=home")
            snap("01-home-empty.png")
            go(f"?problem={run_id}")
            page.wait_for_selector(".answer-card", timeout=30000)
            go("?view=home")
            page.wait_for_selector(".continue-grid", timeout=10000)
            snap("01-home-with-continue.png")
            go(f"?problem={run_id}")
            page.wait_for_selector(".answer-card", timeout=30000)
            snap("05-problem-answer.png")
            if page.locator(".parameters-drawer").count() == 0:
                page.click("button.problem-params-toggle")
            page.wait_for_selector(".parameters-drawer", timeout=10000)
            snap("07-problem-parameters.png")
            page.click('button.problem-tab:has-text("Work")')
            page.wait_for_timeout(400)
            snap("06-problem-work-tab.png")
            go("?view=problems")
            snap("02-problems-list.png")
            go("?view=studio")
            snap("03-studio.png")
            go("?view=gallery")
            snap("04-gallery.png")
            go("?view=settings")
            snap("08-settings.png")
            page.keyboard.press("Control+b")
            page.wait_for_timeout(250)
            snap("09-sidebar-collapsed.png")
            go("?view=home")
            page.keyboard.press("Control+k")
            page.wait_for_selector(".cmdk-root", timeout=5000)
            snap("10-cmdk-open.png")
            page.keyboard.press("Escape")
            go("?view=home")
            page.evaluate(
                """() => {
                document.documentElement.dataset.theme = 'dark';
                localStorage.setItem('arc-theme', 'dark');
            }"""
            )
            page.wait_for_timeout(200)
            snap("11-dark-home.png")
            browser.close()
        return 0
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    raise SystemExit(main())
