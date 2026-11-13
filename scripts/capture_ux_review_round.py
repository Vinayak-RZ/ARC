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


def _kill_port(port: int) -> None:
    try:
        subprocess.run(
            ["fuser", "-k", f"{port}/tcp"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        pass
    time.sleep(0.3)


def _prepare_capture_env() -> None:
    subprocess.check_call(["uv", "pip", "install", "-q", "-e", "."], cwd=ROOT)
    subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")


def _preflight(out_dir: Path) -> dict:
    import urllib.request

    import electrical_engineer

    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    sha_short = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    dist = ROOT / "ui" / "dist" / "index.html"
    dist_mtime = dist.stat().st_mtime if dist.is_file() else None
    pkg_path = str(Path(electrical_engineer.__file__).resolve())
    if "/src/" not in pkg_path.replace("\\", "/"):
        raise RuntimeError(f"electrical_engineer not editable from src: {pkg_path}")
    req = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/control-studio/sessions",
        method="POST",
        data=json.dumps({"title": "Lab 4 · DC motor PID", "golden": "pid_dc_motor"}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        sess = json.loads(resp.read().decode())
    sid = sess["session_id"]
    with urllib.request.urlopen(f"http://{HOST}:{PORT}/api/control-studio/sessions/{sid}", timeout=60) as resp:
        payload = json.loads(resp.read().decode())
    pid = next((b for b in payload.get("diagram", {}).get("blocks", []) if b.get("id") == "pid1"), {})
    kp = float((pid.get("params") or {}).get("kp", 0))
    sim_req = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/control-studio/sessions/{sid}/simulate",
        method="POST",
        data=b"{}",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(sim_req, timeout=180) as resp:
        sim = json.loads(resp.read().decode())
    gm_tip = str((sim.get("analyze") or {}).get("margin_tooltips", {}).get("gm_db", ""))
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
    diff = subprocess.check_output(["git", "diff", "HEAD"], cwd=ROOT)
    req_low = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/control-studio/sessions",
        method="POST",
        data=json.dumps({"title": "HW 3 · Open-loop gain", "golden": "open_loop_low_gain"}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req_low, timeout=60) as resp:
        low_sid = json.loads(resp.read().decode())["session_id"]
    low_sim = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/control-studio/sessions/{low_sid}/simulate",
        method="POST",
        data=b"{}",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(low_sim, timeout=180) as resp:
        low_payload = json.loads(resp.read().decode())
    low_pm = str(((low_payload.get("analyze") or {}).get("display") or {}).get("pm_deg", ""))
    req_fin = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/control-studio/sessions",
        method="POST",
        data=json.dumps({"title": "HW 3 · Unity feedback, K = 10", "golden": "unity_first_order"}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req_fin, timeout=60) as resp:
        fin_sid = json.loads(resp.read().decode())["session_id"]
    fin_req = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/control-studio/sessions/{fin_sid}/simulate",
        method="POST",
        data=b"{}",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(fin_req, timeout=180) as resp:
        fin_payload = json.loads(resp.read().decode())
    fin_m = (fin_payload.get("step_series") or {}).get("metrics") or {}
    data = {
        "git_sha": sha,
        "git_sha_short": sha_short,
        "git_dirty_lines": len(dirty.splitlines()) if dirty else 0,
        "git_diff_sha256": hashlib.sha256(diff).hexdigest()[:16] if diff else None,
        "package_path": pkg_path,
        "dist_index_mtime": dist_mtime,
        "kp": kp,
        "step_series": bool(sim.get("step_series")),
        "gain_margin_caption": gm_tip,
        "low_gain_pm_deg": low_pm,
        "finite_crossover": {
            "status": fin_m.get("status"),
            "final_value": fin_m.get("final_value"),
            "t_settle_s": fin_m.get("t_settle_s"),
            "overshoot_pct": fin_m.get("overshoot_pct"),
            "steady_state_error_pct": fin_m.get("steady_state_error_pct"),
        },
    }
    if kp != 50:
        raise RuntimeError(f"preflight kp={kp}, expected 50 (stale backend?)")
    if not sim.get("step_series"):
        raise RuntimeError("preflight: simulate response missing step_series")
    if "180" not in gm_tip and "−180" not in gm_tip:
        raise RuntimeError(f"preflight: gain margin caption missing −180: {gm_tip!r}")
    if low_pm != "Not defined":
        raise RuntimeError(f"preflight low_gain pm_deg={low_pm!r}, expected Not defined")
    if fin_m.get("status") != "settled_off_target" or fin_m.get("t_settle_s") is None:
        raise RuntimeError(f"preflight finite crossover: {fin_m}")
    if abs(float(fin_m.get("final_value", 0)) - 10 / 11) > 5e-3:
        raise RuntimeError(f"preflight finite crossover final value {fin_m.get('final_value')}")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "preflight.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("preflight.json", data)
    return data


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


def _studio_wires_ready(page, minimum: int = 5, timeout_s: float = 60.0) -> None:
    deadline = time.time() + timeout_s
    paths = page.locator(".studio-canvas .react-flow__edge-path")
    while time.time() < deadline:
        if paths.count() >= minimum:
            return
        page.wait_for_timeout(250)
    raise RuntimeError(f"studio wires not ready after {timeout_s:.0f}s (got {paths.count()})")


def _studio_x_axis(page) -> dict:
    """Axis title and last x tick of the step chart (proves a window change moved the axis)."""
    return page.evaluate(
        """() => {
        const svg = document.querySelector('.studio-step-svg');
        if (!svg) return null;
        const title = [...svg.querySelectorAll('.studio-step-axis')].find((n) => /Time/.test(n.textContent || ''));
        const ticks = [...svg.querySelectorAll('text.studio-step-tick')]
          .map((n) => ({ x: n.getBoundingClientRect().x, t: (n.textContent || '').trim() }))
          .filter((n) => /^-?\\d+(\\.\\d+)?$/.test(n.t))
          .sort((a, b) => a.x - b.x);
        return { title: title ? title.textContent : '', last_tick: ticks.length ? ticks[ticks.length - 1].t : '' };
    }"""
    )


def _click_window(page, label: str) -> None:
    before = _studio_x_axis(page)
    page.locator(".studio-window-segment button", has_text=label).click(force=True)
    deadline = time.time() + 30
    while time.time() < deadline:
        page.wait_for_timeout(250)
        after = _studio_x_axis(page)
        if after and before and after != before:
            return
    raise RuntimeError(f"x axis did not change after choosing {label}: {before} -> {after}")


def _assert_studio_wires(page, name: str) -> None:
    """Every Studio capture must show wires with real geometry and arrowheads."""
    if page.locator(".studio-canvas").count() == 0:
        return
    info = page.evaluate(
        """() => {
        const paths = [...document.querySelectorAll('.studio-canvas .react-flow__edge-path')];
        return {
          n: paths.length,
          empty: paths.filter((p) => (p.getAttribute('d') || '').trim().length < 5).length,
          markers: paths.filter((p) => p.getAttribute('marker-end')).length,
        };
    }"""
    )
    if info["n"] < 1 or info["empty"] or info["markers"] < info["n"]:
        raise RuntimeError(f"{name}: studio wires broken: {info}")


FOCUS_LOG: dict[str, dict] = {}

_ACTIVE_DESC_JS = """() => {
  const e = document.activeElement;
  if (!e || e === document.body) return null;
  return {
    tag: e.tagName.toLowerCase(),
    role: e.getAttribute('role'),
    aria_label: e.getAttribute('aria-label'),
    cls: e.className && e.className.baseVal === undefined ? String(e.className) : '',
    text: (e.textContent || '').trim().slice(0, 40),
    outline: getComputedStyle(e).outlineStyle + ' ' + getComputedStyle(e).outlineWidth + ' ' + getComputedStyle(e).outlineColor,
  };
}"""


def _tab_to(page, name: str, start_selector: str, match_js: str, max_tabs: int = 60) -> dict:
    """Click a non-focusable start point, then press real Tab keys until activeElement matches.

    match_js is a JS arrow function taking the active element. Raises if it is never reached.
    """
    page.locator(start_selector).first.click()
    for presses in range(1, max_tabs + 1):
        page.keyboard.press("Tab")
        page.wait_for_timeout(40)
        if page.evaluate(f"({match_js})(document.activeElement)"):
            desc = page.evaluate(_ACTIVE_DESC_JS)
            desc["tab_presses"] = presses
            FOCUS_LOG[name] = desc
            return desc
    raise RuntimeError(f"{name}: activeElement never matched after {max_tabs} Tab presses")


def _assert_still_active(page, name: str, match_js: str) -> None:
    if not page.evaluate(f"({match_js})(document.activeElement)"):
        raise RuntimeError(f"{name}: focus moved before the screenshot was taken")


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

    _kill_port(PORT)
    _prepare_capture_env()

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
        if args.round >= 6:
            _preflight(out_dir)
        backup = _backup_runs()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": W, "height": H})

            def shot_name(name: str) -> str:
                if args.round < 4:
                    return name
                stem = name.replace(".png", "")
                if stem.endswith(("-light", "-dark")):
                    return name
                if stem.startswith("dark-"):
                    return f"{stem[5:]}-dark.png"
                return f"{stem}-light.png"

            def snap(name: str, target=None, *, theme: str | None = None) -> None:
                name = shot_name(name)
                shot = target or page
                if args.round >= 5:
                    use_theme = theme or ("dark" if name.endswith("-dark.png") else "light")
                    _set_theme(shot, use_theme)
                    shot.wait_for_timeout(250)
                path = out_dir / name
                _assert_studio_wires(shot, name)
                shot.screenshot(path=str(path), full_page=False)
                digest = _md5(path)
                if digest in hashes.values():
                    dup = next(k for k, v in hashes.items() if v == digest)
                    raise RuntimeError(f"duplicate screenshot: {name} matches {dup} (md5={digest})")
                hashes[name] = digest
                print(f"wrote {path} md5={digest}")

            def go(query: str = "") -> None:
                page.goto(f"http://{HOST}:{PORT}/{query}", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_selector(".product-shell", timeout=30000)
                page.wait_for_timeout(500)

            def focus_shot(name: str, start: str, match_js: str, query: str, prep=None) -> None:
                """Tab to the intended element, assert it is active, then screenshot (theme from name)."""
                go(query)
                if prep:
                    prep()
                _tab_to(page, name, start, match_js)
                snap(name)
                _assert_still_active(page, name, match_js)

            def focus_set(theme: str, run_id: str) -> None:
                _set_theme(page, theme)
                sfx = f"-{theme}.png"

                def stale_params() -> None:
                    page.click(".topbar-params-toggle")
                    page.wait_for_selector(".param-field input", timeout=10000)
                    page.locator("#param-r2").fill("2")
                    page.wait_for_selector(".stale-banner", timeout=5000)
                    page.keyboard.press("Escape")

                focus_shot(
                    "focus-composer" + sfx, "h1", "e => e.classList.contains('composer-input')", "?view=home"
                )
                focus_shot(
                    "focus-tile" + sfx, "h1", "e => e.classList.contains('example-card')", "?view=home"
                )
                focus_shot(
                    "focus-table-row" + sfx,
                    "h1",
                    "e => e.getAttribute('aria-label') === 'Open problem'",
                    "?view=problems",
                )
                focus_shot(
                    "focus-tab" + sfx,
                    "h1, .answer-line, .problem-meta",
                    "e => e.getAttribute('role') === 'tab' && e.textContent.trim() === 'Work'",
                    f"?problem={run_id}",
                    prep=lambda: page.get_by_role("tab", name="Work").click(),
                )
                focus_shot(
                    "focus-button" + sfx,
                    "h1, .answer-line, .problem-meta",
                    "e => e.tagName === 'BUTTON' && /Run again/.test(e.textContent)",
                    f"?problem={run_id}",
                    prep=stale_params,
                )

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

            if args.round < 8:
                go("?view=home")
                page.locator(".composer-input").focus()
                page.wait_for_timeout(100)
                snap("focus-composer.png")

            import urllib.request

            req = urllib.request.Request(
                f"http://{HOST}:{PORT}/api/control-studio/sessions",
                method="POST",
                data=json.dumps({"title": "Lab 4 · DC motor PID", "golden": "pid_dc_motor"}).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                pid_sess = json.loads(resp.read().decode())["session_id"]
            go(f"?view=studio&session={pid_sess}")
            _studio_wires_ready(page)
            page.wait_for_timeout(400)
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
            page.wait_for_timeout(400)
            snap("studio-block-selected.png")
            page.locator(".studio-canvas .react-flow__pane").click(position={"x": 40, "y": 40}, force=True)
            page.wait_for_timeout(200)

            sim = page.locator(".cs-simulate-btn")
            if sim.count() > 0:
                sim.click()
                page.wait_for_selector(
                    ".studio-results-stage .studio-step-svg, .studio-results-stage img",
                    timeout=120000,
                )
                _studio_wires_ready(page)
            snap("studio-layout-after-simulate.png")

            if args.round >= 6:
                box = pid.first.bounding_box()
                if box:
                    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                else:
                    pid.first.locator(".studio-block").click(force=True)
                page.wait_for_timeout(400)
                snap("studio-block-selected-after-simulate.png")
                if args.round < 7:
                    page.locator(".studio-canvas .react-flow__pane").click(position={"x": 40, "y": 40}, force=True)
                    page.wait_for_timeout(200)
                    page.locator(".studio-window-segment button", has_text="30 s").click(force=True)
                    page.wait_for_timeout(1200)
                    snap("studio-step-extended.png")
                req_u = urllib.request.Request(
                    f"http://{HOST}:{PORT}/api/control-studio/sessions",
                    method="POST",
                    data=json.dumps({"golden": "unity_first_order"}).encode(),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req_u, timeout=60) as resp:
                    u_sid = json.loads(resp.read().decode())["session_id"]
                go(f"?view=studio&session={u_sid}")
                page.locator(".cs-simulate-btn").click()
                page.wait_for_selector(".studio-step-svg", timeout=120000)
                page.wait_for_timeout(400)
                snap("studio-step-offtarget.png")
                page.set_viewport_size({"width": 1280, "height": 680})
                go(f"?view=studio&session={pid_sess}")
                page.wait_for_timeout(800)
                snap("studio-after-resize.png")
                page.set_viewport_size({"width": W, "height": H})
            if args.round >= 7:
                go(f"?view=studio&session={pid_sess}")
                page.locator(".cs-simulate-btn").click()
                page.wait_for_selector(".studio-settled-pill", timeout=120000)
                snap("studio-step-settled.png")
                if args.round >= 8:
                    snap("studio-step-settled-dark.png")
                page.locator(".react-flow__node", has_text="PID").click(force=True)
                for label, val in [("Kp", "0.08"), ("Ki", "0.02"), ("Kd", "0")]:
                    field = page.get_by_label(label)
                    if field.count():
                        field.fill(val)
                page.locator(".cs-simulate-btn").click()
                page.wait_for_selector(".studio-unsettled-pill", timeout=120000)
                snap("studio-step-unsettled.png")
                _click_window(page, "30 s")
                page.wait_for_timeout(300)
                snap("studio-step-extended.png")
            if args.round >= 4:
                wide_studio = browser.new_page(viewport={"width": 1440, "height": 900})
                req1440 = urllib.request.Request(
                    f"http://{HOST}:{PORT}/api/control-studio/sessions",
                    method="POST",
                    data=json.dumps({"title": "Lab 4 · DC motor PID", "golden": "pid_dc_motor"}).encode(),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req1440, timeout=60) as resp:
                    wide_sid = json.loads(resp.read().decode())["session_id"]
                wide_studio.goto(
                    f"http://{HOST}:{PORT}/?view=studio&session={wide_sid}",
                    wait_until="domcontentloaded",
                )
                wide_studio.wait_for_selector(".studio-canvas", timeout=15000)
                wide_studio.wait_for_selector(".studio-canvas .react-flow__node", timeout=60000)
                _studio_wires_ready(wide_studio, timeout_s=120.0)
                wide_studio.wait_for_timeout(400)
                snap("studio-layout-before-simulate-1440.png", wide_studio)
                if args.round >= 7:
                    snap("studio-layout-before-simulate-1440-dark.png", wide_studio)
                wide_studio.locator(".cs-simulate-btn").click()
                wide_studio.wait_for_selector(
                    ".studio-results-stage .studio-step-svg, .studio-results-stage img",
                    timeout=120000,
                )
                wide_studio.wait_for_selector(".studio-canvas .react-flow__node", timeout=60000)
                _studio_wires_ready(wide_studio, timeout_s=120.0)
                snap("studio-layout-after-simulate-1440.png", wide_studio)
                if args.round >= 7:
                    snap("studio-layout-after-simulate-1440-dark.png", wide_studio)
                wide_studio.close()

            if args.round >= 3:
                req = urllib.request.Request(
                    f"http://{HOST}:{PORT}/api/control-studio/sessions",
                    method="POST",
                    data=json.dumps({"title": "HW 3 · Open-loop gain", "golden": "open_loop_low_gain"}).encode(),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    low = json.loads(resp.read().decode())
                sid = low["session_id"]
                go(f"?view=studio&session={sid}")
                page.wait_for_selector(".cs-simulate-btn", timeout=15000)
                page.click(".cs-simulate-btn")
                page.wait_for_selector(".studio-margins .studio-margin", timeout=60000)
                page.wait_for_timeout(400)
                snap("studio-margins-no-crossover.png")
                if args.round >= 8:
                    snap("studio-margins-no-crossover-dark.png")

            if args.round >= 4:
                req = urllib.request.Request(
                    f"http://{HOST}:{PORT}/api/control-studio/sessions",
                    method="POST",
                    data=json.dumps({"title": "HW 3 · Unity feedback, K = 10", "golden": "unity_first_order"}).encode(),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    fin = json.loads(resp.read().decode())["session_id"]
                go(f"?view=studio&session={fin}")
                page.wait_for_selector(".cs-simulate-btn", timeout=15000)
                page.click(".cs-simulate-btn")
                page.wait_for_selector(".studio-margins .studio-margin", timeout=120000)
                page.wait_for_timeout(400)
                snap("studio-margins-finite.png")
                if args.round >= 8:
                    snap("studio-margins-finite-dark.png")

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
            _set_theme(page, "light")

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

                if args.round >= 8:
                    focus_set("light", run_id)
                else:
                    go(f"?problem={run_id}")
                    page.get_by_role("tab", name="Work").click()
                    for _ in range(6):
                        page.keyboard.press("Tab")
                        page.wait_for_timeout(80)
                    snap("focus-tab.png")
                    go("?view=home")
                    page.locator(".composer-input").click()
                    for _ in range(12):
                        page.keyboard.press("Tab")
                        page.wait_for_timeout(60)
                    snap("focus-tile.png")
                    go("?view=problems")
                    page.locator("tr.problems-row").first.click()
                    for _ in range(4):
                        page.keyboard.press("Tab")
                        page.wait_for_timeout(80)
                    snap("focus-table-row.png")
                    go("?view=problems")
                    page.wait_for_selector("tr.problems-row", timeout=15000)
                    page.locator("tr.problems-row").first.click()
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
                data=json.dumps({"title": "Lab 4 · DC motor PID", "golden": "pid_dc_motor"}).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                dark_sid = json.loads(resp.read().decode())["session_id"]
            go(f"?view=studio&session={dark_sid}")
            _studio_wires_ready(page)
            page.wait_for_timeout(800)
            snap("studio-before-simulate-dark.png")
            if args.round >= 7:
                page.locator(".react-flow__node", has_text="PID").click(force=True)
                page.wait_for_function("() => document.querySelector('.studio.has-selection')", timeout=15000)
                page.wait_for_timeout(500)
                snap("studio-block-selected-dark.png")
                page.locator(".studio-canvas .react-flow__pane").click(position={"x": 40, "y": 40}, force=True)
                page.wait_for_timeout(200)
            page.locator(".cs-simulate-btn").click()
            page.wait_for_selector(
                ".studio-results-stage .studio-step-svg, .studio-results-stage img",
                timeout=120000,
            )
            _studio_wires_ready(page)
            page.wait_for_timeout(400)
            snap("studio-after-simulate-dark.png")
            if args.round >= 7:
                page.locator(".react-flow__node", has_text="PID").click(force=True)
                for label, val in [("Kp", "0.08"), ("Ki", "0.02"), ("Kd", "0")]:
                    field = page.get_by_label(label)
                    if field.count():
                        field.fill(val)
                page.locator(".cs-simulate-btn").click()
                try:
                    page.wait_for_selector(".studio-unsettled-pill", timeout=60000)
                except Exception:
                    page.screenshot(path="/tmp/capture-debug-unsettled-dark.png")
                    raise
                page.wait_for_timeout(400)
                snap("studio-step-unsettled-dark.png")
                _click_window(page, "30 s")
                page.wait_for_timeout(300)
                snap("studio-step-extended-dark.png")

            if args.round >= 5:
                _set_theme(page, "dark")
                go("?view=home")
                snap("home-dark.png")
                go("?view=home")
                page.evaluate("() => document.querySelector('.agent-card')?.scrollIntoView({block: 'end'})")
                page.wait_for_timeout(300)
                snap("home-scrolled-dark.png")
                _clear_runs()
                go("?view=problems")
                page.wait_for_selector(".problems-empty", timeout=10000)
                snap("problems-empty-dark.png")
                page.route("**/api/runs", lambda route: route.fulfill(status=500, body="{}"))
                page.reload(wait_until="domcontentloaded")
                page.wait_for_selector(".problems-error", timeout=15000)
                snap("problems-error-dark.png")
                page.unroute("**/api/runs")
                run_id = _run_example("divider")
                go("?view=problems")
                page.wait_for_selector(".problems-table", timeout=15000)
                snap("problems-list-dark.png")
                page.locator(".problems-row").first.hover()
                page.wait_for_timeout(150)
                snap("problems-row-hover-dark.png")
                if args.round >= 8:
                    focus_set("dark", run_id)
                elif args.round >= 7:
                        _set_theme(page, "dark")
                        go(f"?problem={run_id}")
                        page.get_by_role("tab", name="Work").click()
                        for _ in range(6):
                            page.keyboard.press("Tab")
                            page.wait_for_timeout(80)
                        snap("focus-tab-dark.png")
                        go("?view=problems")
                        page.wait_for_selector("tr.problems-row", timeout=15000)
                        page.locator("tr.problems-row").first.click()
                        for _ in range(3):
                            page.keyboard.press("Tab")
                            page.wait_for_timeout(80)
                        snap("focus-button-dark.png")
                if args.round >= 9:
                    # Fresh page and route per capture: no leftover drawer, focus ring or filter.
                    go(f"?problem={run_id}")
                    page.wait_for_selector(".answer-line", timeout=30000)
                    page.evaluate("() => document.activeElement && document.activeElement.blur()")
                page.keyboard.press("Control+b")
                page.wait_for_selector(".product-sidebar.is-collapsed", timeout=5000)
                page.wait_for_timeout(200)
                snap("sidebar-collapsed-dark.png")
                page.keyboard.press("Control+b")
                page.wait_for_timeout(200)
                if args.round >= 9:
                    go("?view=problems")
                    page.wait_for_selector("tr.problems-row", timeout=15000)
                    page.evaluate("() => document.activeElement && document.activeElement.blur()")
                page.keyboard.press("Control+k")
                page.wait_for_selector(".cmdk-root", timeout=5000)
                snap("cmdk-open-dark.png")
                go("?view=gallery")
                page.wait_for_selector(".gallery-card", timeout=10000)
                snap("gallery-dark.png")
                go("?view=library")
                page.wait_for_selector(".library", timeout=10000)
                snap("library-dark.png")
                go("?view=settings")
                page.wait_for_selector(".settings-page", timeout=10000)
                for tab, stem in [
                    ("Agents", "settings-agents"),
                    ("Engines", "settings-engines"),
                    ("Appearance", "settings-appearance"),
                    ("Data", "settings-data"),
                    ("About", "settings-about"),
                ]:
                    page.get_by_role("tab", name=tab).click()
                    page.wait_for_timeout(200)
                    snap(f"{stem}-dark.png")
                go(f"?problem={run_id}")
                page.get_by_role("tab", name="Diagram").click()
                page.wait_for_selector(".static-diagram", timeout=15000)
                snap("problem-answer-dark.png")
                page.get_by_role("tab", name="Work").click()
                page.wait_for_selector(".step-timeline-row", timeout=10000)
                snap("problem-work-dark.png")
                page.click(".topbar-params-toggle")
                page.locator("#param-r2").fill("2")
                page.wait_for_selector(".stale-banner", timeout=5000)
                snap("problem-stale-dark.png")

            browser.close()

        md5_lines = [f"{name}  {dig}" for name, dig in sorted(hashes.items())]
        (out_dir / "md5.txt").write_text("\n".join(md5_lines) + "\n", encoding="utf-8")
        if args.round >= 5:
            prev = ROOT / "artifacts" / "ux-review" / f"round-{args.round - 1}" / "md5.txt"
            changed = []
            if prev.is_file():
                prev_map = {}
                for line in prev.read_text(encoding="utf-8").splitlines():
                    if "  " in line:
                        n, d = line.split("  ", 1)
                        prev_map[n] = d.strip()
                for n, d in hashes.items():
                    old = prev_map.get(n.replace("-light", "-light").replace("-dark", "-dark"))
                    # map round-4 names without theme suffix
                    legacy = n.replace("-light.png", ".png").replace("-dark.png", ".png")
                    if prev_map.get(legacy) == d or old == d:
                        changed.append(f"{n} unchanged from round {args.round - 1}")
            (out_dir / "NOTES.md").write_text(
                f"# Round {args.round} captures\n\n"
                f"PNG count: {len(hashes)}\n\n"
                + ("\n".join(changed) if changed else f"All captures differ from round-{args.round - 1} md5 where compared.\n"),
                encoding="utf-8",
            )
        if FOCUS_LOG:
            (out_dir / "focus-log.json").write_text(json.dumps(FOCUS_LOG, indent=2) + "\n", encoding="utf-8")
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
