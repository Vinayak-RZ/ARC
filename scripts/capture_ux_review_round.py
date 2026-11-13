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

            def shot_name(name: str) -> str:
                if args.round < 4:
                    return name
                stem = name.replace(".png", "")
                if stem.endswith("-light") or stem.endswith("-dark"):
                    return name
                if stem.startswith("dark-"):
                    return f"{stem[5:]}-dark.png"
                return f"{stem}-light.png"

            def snap(name: str, target=None) -> None:
                name = shot_name(name)
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

            import urllib.request

            req = urllib.request.Request(
                f"http://{HOST}:{PORT}/api/control-studio/sessions",
                method="POST",
                data=json.dumps({"title": "PID DC motor", "golden": "pid_dc_motor"}).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                pid_sess = json.loads(resp.read().decode())["session_id"]
            go(f"?view=studio&session={pid_sess}")
            page.wait_for_timeout(800)
            snap("studio-layout-before-simulate.png")

            page.locator(".studio-canvas .react-flow").wait_for(state="visible", timeout=15000)
            pid = page.locator(".react-flow__node[data-id='pid1']")
            if pid.count() == 0:
                pid = page.locator(".react-flow__node-pid, .react-flow__node", has_text="PID")
            box = pid.first.bounding_box()
            if box:
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            else:
                pid.first.locator(".studio-block").click(force=True)
            page.wait_for_function(
                "() => document.querySelector('.studio.has-selection')",
                timeout=15000,
            )
            page.wait_for_timeout(300)
            page.wait_for_timeout(400)
            snap("studio-block-selected.png")
            sim = page.locator(".cs-simulate-btn")
            if sim.count() > 0:
                sim.click()
                page.wait_for_selector(".studio-results-stage img", timeout=120000)
                page.wait_for_timeout(800)
            snap("studio-layout-after-simulate.png")
            if args.round >= 4:
                wide_studio = browser.new_page(viewport={"width": 1440, "height": 900})
                wide_studio.goto(
                    f"http://{HOST}:{PORT}/?view=studio&session={pid_sess}",
                    wait_until="domcontentloaded",
                )
                wide_studio.wait_for_selector(".studio-canvas", timeout=15000)
                wide_studio.wait_for_timeout(500)
                snap("studio-layout-before-simulate-1440.png", wide_studio)
                wide_studio.locator(".cs-simulate-btn").click()
                wide_studio.wait_for_selector(".studio-results-stage img", timeout=120000)
                wide_studio.wait_for_timeout(400)
                snap("studio-layout-after-simulate-1440.png", wide_studio)
                wide_studio.close()

            if args.round >= 3:
                req = urllib.request.Request(
                    f"http://{HOST}:{PORT}/api/control-studio/sessions",
                    method="POST",
                    data=json.dumps({"title": "Low gain", "golden": "open_loop_low_gain"}).encode(),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    low = json.loads(resp.read().decode())
                sid = low["session_id"]
                go(f"?view=studio&session={sid}")
                page.wait_for_selector(".cs-simulate-btn", timeout=15000)
                page.click(".cs-simulate-btn")
                page.wait_for_selector(".studio-margin-table", timeout=60000)
                page.wait_for_timeout(400)
                snap("studio-margins-no-crossover.png")

            if args.round >= 4:
                req = urllib.request.Request(
                    f"http://{HOST}:{PORT}/api/control-studio/sessions",
                    method="POST",
                    data=json.dumps({"title": "Finite crossover", "golden": "unity_first_order"}).encode(),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    fin = json.loads(resp.read().decode())["session_id"]
                go(f"?view=studio&session={fin}")
                page.wait_for_selector(".cs-simulate-btn", timeout=15000)
                page.click(".cs-simulate-btn")
                page.wait_for_selector(".studio-margin-table", timeout=120000)
                page.wait_for_timeout(400)
                snap("studio-margins-finite.png")

            go("?view=gallery")
            page.wait_for_selector(".gallery-card", timeout=10000)
            snap("gallery.png")

            go("?view=library")
            page.wait_for_selector(".library", timeout=10000)
            snap("library.png")

            go("?view=settings")
            page.wait_for_selector(".settings-page", timeout=10000)
            if args.round >= 3:
                snap("settings-agents.png")
                for tab, name in [
                    ("Engines", "settings-engines.png"),
                    ("Appearance", "settings-appearance.png"),
                    ("Data", "settings-data.png"),
                    ("About", "settings-about.png"),
                ]:
                    page.get_by_role("tab", name=tab).click()
                    page.wait_for_timeout(200)
                    snap(name)
            else:
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
            page.wait_for_function(
                """() => {
                const shell = document.querySelector('.product-shell');
                const cols = getComputedStyle(shell).gridTemplateColumns || '';
                return cols.startsWith('240px');
            }""",
                timeout=5000,
            )
            page.wait_for_timeout(220)
            page.keyboard.press("Control+k")
            page.wait_for_selector(".cmdk-root", timeout=5000)
            snap("cmdk-open.png")
            cmdk_w = page.evaluate("() => document.querySelector('.product-sidebar')?.getBoundingClientRect().width")
            measurements["sidebar_cmdk_open"] = {"sidebar": cmdk_w}
            page.locator(".cmdk-root [cmdk-input]").fill("divider")
            page.wait_for_timeout(150)
            snap("cmdk-query.png")

            page.keyboard.press("Escape")
            _set_theme(page, "dark")
            go("?view=home")
            snap("dark-home.png")

            if args.round >= 3:
                run_id = _run_example("divider")
                go("?view=home")
                page.evaluate("() => document.querySelector('.agent-card')?.scrollIntoView({block: 'end'})")
                page.wait_for_timeout(300)
                snap("home-scrolled-1280.png")
                wide = browser.new_page(viewport={"width": 1440, "height": H})
                wide.goto(f"http://{HOST}:{PORT}/?view=home", wait_until="domcontentloaded")
                wide.wait_for_selector(".example-grid-six", timeout=15000)
                wide.evaluate("() => document.querySelector('.agent-card')?.scrollIntoView({block: 'end'})")
                wide.wait_for_timeout(300)
                snap("home-scrolled-1440.png", wide)
                wide.close()

                go("?view=problems")
                page.wait_for_selector(".problems-row", timeout=15000)
                page.locator(".problems-row").first.hover()
                page.wait_for_timeout(150)
                snap("problems-row-hover.png")

                go(f"?problem={run_id}")
                page.get_by_role("tab", name="Work").click()
                for _ in range(6):
                    page.keyboard.press("Tab")
                    page.wait_for_timeout(80)
                snap("focus-tab.png")
                go("?view=home")
                page.locator(".example-card").first.click()
                page.keyboard.press("Tab")
                page.wait_for_timeout(150)
                snap("focus-tile.png")
                go("?view=problems")
                page.locator(".problems-row").first.click()
                for _ in range(4):
                    page.keyboard.press("Tab")
                    page.wait_for_timeout(80)
                snap("focus-table-row.png")
                page.locator(".problems-row").first.click()
                for _ in range(3):
                    page.keyboard.press("Tab")
                    page.wait_for_timeout(80)
                snap("focus-button.png")

            if not run_id:
                run_id = _run_example("divider")
            go(f"?problem={run_id}")
            page.wait_for_selector(".answer-line", timeout=30000)
            page.get_by_role("tab", name="Diagram").click()
            page.wait_for_selector(".static-diagram", timeout=15000)
            snap("dark-problem.png")

            req = urllib.request.Request(
                f"http://{HOST}:{PORT}/api/control-studio/sessions",
                method="POST",
                data=json.dumps({"golden": "pid_dc_motor"}).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                dark_sid = json.loads(resp.read().decode())["session_id"]
            go(f"?view=studio&session={dark_sid}")
            page.wait_for_timeout(800)
            snap("dark-studio-before-simulate.png")
            page.locator(".cs-simulate-btn").click()
            page.wait_for_selector(".studio-results-stage img", timeout=120000)
            page.wait_for_timeout(400)
            snap("dark-studio-after-simulate.png")

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
