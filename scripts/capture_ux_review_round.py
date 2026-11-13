#!/usr/bin/env python3
"""Capture UX review screenshots at 1280x800 into artifacts/ux-review/round-<N>/."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
    dest = ROOT / "artifacts" / "ux-review" / "_runs_backup"
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


def _set_theme(page, mode: str) -> None:
    page.evaluate(
        """(mode) => {
        document.documentElement.dataset.theme = mode;
        localStorage.setItem('arc-theme', mode);
    }""",
        mode,
    )
    page.wait_for_timeout(200)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, default=1)
    args = parser.parse_args()
    out_dir = ROOT / "artifacts" / "ux-review" / f"round-{args.round}"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    if not (ROOT / "ui" / "dist" / "index.html").is_file():
        subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")

    env = {**os.environ, "EE_NO_BROWSER": "1"}
    server = subprocess.Popen(
        [sys.executable, "-m", "electrical_engineer", "ui"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    hashes: dict[str, str] = {}
    backup = None
    measurements: dict[str, object] = {}
    try:
        _wait_server(server)
        backup = _backup_runs()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": W, "height": H})

            def snap(name: str, target=None) -> None:
                shot = target or page
                path = out_dir / name
                shot.screenshot(path=str(path), full_page=False)
                digest = _md5(path)
                if digest in hashes.values():
                    dup = [k for k, v in hashes.items() if v == digest][0]
                    raise RuntimeError(f"duplicate screenshot: {name} matches {dup} (md5={digest})")
                hashes[name] = digest
                print(f"wrote {path} md5={digest}")

            def go(query: str = "") -> None:
                page.goto(f"http://{HOST}:{PORT}/{query}", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_selector(".product-shell", timeout=30000)
                page.wait_for_timeout(500)

            _clear_runs()
            go("?view=home")
            page.wait_for_selector(".composer-card", timeout=10000)
            if page.locator(".continue-section").count() > 0:
                raise RuntimeError("home-empty must not show Continue")
            if page.locator(".sidebar-recent-item").count() > 0:
                raise RuntimeError("home-empty must not show sidebar Recent rows")
            snap("home-empty.png")

            run_id = _run_example("divider")
            go("?view=home")
            page.wait_for_selector(".sidebar-recent-item", timeout=15000)
            page.wait_for_selector(".continue-section", timeout=15000)
            snap("home-with-recent.png")

            go("?view=problems")
            page.wait_for_selector(".problems-table", timeout=10000)
            snap("problems-list.png")

            go(f"?problem={run_id}")
            page.wait_for_selector(".answer-line", timeout=30000)
            if page.locator(".parameters-drawer").is_visible():
                page.click(".topbar-params-toggle")
            page.wait_for_selector(".parameters-drawer", state="hidden", timeout=5000)
            page.get_by_role("tab", name="Diagram").click()
            page.wait_for_selector('.tab-underline[aria-selected="true"]:has-text("Diagram")', timeout=5000)
            page.locator(".static-diagram, .diagram-shell svg").first.wait_for(state="visible", timeout=15000)
            snap("problem-answer.png")

            page.get_by_role("tab", name="Work").click()
            page.wait_for_selector('.tab-underline[aria-selected="true"]:has-text("Work")', timeout=5000)
            page.wait_for_selector(".step-timeline-row", timeout=10000)
            page.locator(".step-timeline").scroll_into_view_if_needed()
            if page.locator(".parameters-drawer").is_visible():
                page.click(".topbar-params-toggle")
            snap("problem-work-tab.png")

            page.click(".topbar-params-toggle")
            page.wait_for_selector(".param-field input", timeout=10000)
            snap("problem-parameters-drawer.png")

            page.locator("#param-r2").fill("2")
            page.wait_for_selector(".stale-banner", timeout=5000)
            snap("problem-parameters-stale.png")
            page.keyboard.press("Escape")

            go("?view=home")
            page.locator(".composer-input").focus()
            page.wait_for_timeout(100)
            snap("focus-composer.png")

            go("?view=studio")
            page.wait_for_timeout(800)
            snap("studio.png")

            page.locator(".studio-canvas .react-flow").wait_for(state="visible", timeout=15000)
            page.locator(".studio-palette").scroll_into_view_if_needed()
            chip = page.locator(".studio-palette-chip-compact").first
            if chip.count() > 0:
                chip.click(force=True)
                page.wait_for_timeout(600)
            nodes = page.locator(".react-flow__node")
            if nodes.count() > 0:
                box = nodes.last.bounding_box()
                if box:
                    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.wait_for_timeout(400)
            snap("studio-block-selected.png")
            sim = page.locator(".cs-simulate-btn")
            if sim.count() > 0:
                sim.click()
                page.wait_for_timeout(2000)
            snap("studio-after-simulate.png")

            go("?view=gallery")
            page.wait_for_selector(".gallery-card", timeout=10000)
            snap("gallery.png")

            go("?view=library")
            page.wait_for_selector(".library", timeout=10000)
            snap("library.png")

            go("?view=settings")
            page.wait_for_selector(".settings-page", timeout=10000)
            snap("settings.png")

            _clear_runs()
            go("?view=problems")
            page.wait_for_selector(".problems-empty", timeout=10000)
            snap("problems-empty.png")

            page.route("**/api/runs", lambda route: route.fulfill(status=500, body="{}"))
            page.reload(wait_until="domcontentloaded")
            page.wait_for_selector(".problems-error", timeout=15000)
            snap("problems-error.png")
            page.unroute("**/api/runs")

            loading_page = browser.new_page(viewport={"width": W, "height": H})
            held_runs: list = []

            def hold_runs(route) -> None:
                held_runs.append(route)

            loading_page.route("**/api/runs", hold_runs)
            loading_page.goto(f"http://{HOST}:{PORT}/?view=problems", wait_until="commit", timeout=60000)
            loading_page.wait_for_selector(".problems-loading", timeout=10000)
            loading_page.wait_for_timeout(150)
            snap("problems-loading.png", loading_page)
            if held_runs:
                held_runs[0].fulfill(status=200, body=json.dumps({"runs": []}), headers={"Content-Type": "application/json"})
            loading_page.close()

            run_id = _run_example("divider")

            go("?view=problems")
            page.wait_for_selector(".problems-table", timeout=15000)
            expanded_w = page.evaluate(
                """() => {
                const sb = document.querySelector('.product-sidebar');
                const shell = document.querySelector('.product-shell');
                return { sidebar: sb?.getBoundingClientRect().width ?? 0, shellCols: getComputedStyle(shell).gridTemplateColumns };
            }"""
            )
            measurements["sidebar_expanded"] = expanded_w

            page.keyboard.press("Control+b")
            page.wait_for_selector(".product-sidebar.is-collapsed", timeout=5000)
            page.wait_for_timeout(220)
            collapsed_w = page.evaluate(
                """() => {
                const sb = document.querySelector('.product-sidebar');
                const shell = document.querySelector('.product-shell');
                return { sidebar: sb?.getBoundingClientRect().width ?? 0, shellCols: getComputedStyle(shell).gridTemplateColumns };
            }"""
            )
            measurements["sidebar_collapsed"] = collapsed_w
            snap("sidebar-collapsed.png")

            page.keyboard.press("Control+b")
            page.wait_for_selector(".product-sidebar:not(.is-collapsed)", timeout=5000)
            page.keyboard.press("Control+k")
            page.wait_for_selector(".cmdk-root", timeout=5000)
            snap("cmdk-open.png")
            page.locator(".cmdk-root [cmdk-input]").fill("divider")
            page.wait_for_timeout(150)
            snap("cmdk-query.png")

            page.keyboard.press("Escape")
            _set_theme(page, "dark")
            go("?view=home")
            snap("dark-home.png")

            if not run_id:
                run_id = _run_example("divider")
            go(f"?problem={run_id}")
            page.wait_for_selector(".answer-line", timeout=30000)
            snap("dark-problem.png")

            go("?view=studio")
            page.wait_for_timeout(800)
            snap("dark-studio.png")

            browser.close()

        md5_lines = [f"{name}  {dig}" for name, dig in sorted(hashes.items())]
        (out_dir / "md5.txt").write_text("\n".join(md5_lines) + "\n", encoding="utf-8")
        (out_dir / "sidebar-measurements.json").write_text(
            json.dumps(measurements, indent=2) + "\n", encoding="utf-8"
        )
        print("md5.txt written", out_dir / "md5.txt")
        return 0
    finally:
        if backup is not None:
            _restore_runs(backup)
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    raise SystemExit(main())
