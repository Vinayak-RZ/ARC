#!/usr/bin/env python3
"""Capture PRODUCT_SPEC section 5 screenshots at 1280x800 (distinct states + MD5 guard)."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path("/opt/cursor/artifacts")
RUNS = ROOT / "runs"
PORT = 8765
HOST = "127.0.0.1"
W, H = 1280, 800


def _md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


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


def _backup_runs() -> Path | None:
    if not RUNS.is_dir() or not any(RUNS.iterdir()):
        return None
    dest = OUT / "_runs_backup"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(RUNS, dest)
    return dest


def _restore_runs(backup: Path | None) -> None:
    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    if backup and backup.is_dir():
        shutil.copytree(backup, RUNS)
    else:
        RUNS.mkdir(parents=True, exist_ok=True)


def _clear_runs() -> None:
    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)


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
    hashes: dict[str, str] = {}
    try:
        _wait_server(server)
        backup = _backup_runs()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": W, "height": H})

            def snap(name: str) -> None:
                path = OUT / name
                page.screenshot(path=str(path), full_page=False)
                digest = _md5(path)
                if digest in hashes.values():
                    dup = next(k for k, v in hashes.items() if v == digest)
                    raise RuntimeError(f"duplicate screenshot: {name} matches {dup} (md5={digest})")
                hashes[name] = digest
                print(f"wrote {path} md5={digest}")

            def go(query: str = "") -> None:
                page.goto(f"http://{HOST}:{PORT}/{query}", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_selector(".product-shell", timeout=30000)
                page.wait_for_timeout(400)

            # 01-home-empty: no Continue section
            _clear_runs()
            go("?view=home")
            page.wait_for_selector(".composer-card", timeout=10000)
            if page.locator(".continue-section").count() > 0:
                raise RuntimeError("home-empty must not show Continue")
            for img in page.locator("img.example-thumb").all():
                img.wait_for_element_state("visible", timeout=15000)
            snap("01-home-empty.png")

            run_id = _run_example("divider")
            if not (RUNS / run_id).is_dir():
                raise RuntimeError(f"run {run_id} missing after example")

            go("?view=home")
            page.wait_for_selector(".continue-section", timeout=15000)
            snap("01-home-with-continue.png")

            go(f"?problem={run_id}")
            page.wait_for_selector(".answer-line", timeout=30000)
            if page.locator(".parameters-drawer").is_visible():
                page.click(".topbar-params-toggle")
            page.wait_for_selector(".parameters-drawer", state="hidden", timeout=5000)
            snap("05-problem-answer.png")

            page.get_by_role("tab", name="Work").click()
            page.wait_for_selector(".work-trail-step", timeout=10000)
            if page.locator(".parameters-drawer").is_visible():
                page.click(".topbar-params-toggle")
            snap("06-problem-work-tab.png")

            page.click(".topbar-params-toggle")
            page.wait_for_selector(".param-field input", timeout=10000)
            snap("07-problem-parameters.png")

            go("?view=problems")
            page.wait_for_selector(".problems-table", timeout=10000)
            snap("02-problems-list.png")
            go("?view=studio")
            snap("03-studio.png")
            go("?view=gallery")
            page.wait_for_selector(".gallery-card", timeout=10000)
            snap("04-gallery.png")
            go("?view=settings")
            snap("08-settings.png")
            go("?view=home")
            page.keyboard.press("Control+b")
            page.wait_for_selector(".product-sidebar.is-collapsed", timeout=5000)
            snap("09-sidebar-collapsed.png")
            page.keyboard.press("Control+b")
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
            page.wait_for_timeout(250)
            snap("11-dark-home.png")
            browser.close()
        return 0
    finally:
        if "backup" in dir() and backup is not None:
            _restore_runs(backup)
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    raise SystemExit(main())
