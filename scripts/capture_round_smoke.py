#!/usr/bin/env python3
"""CI smoke: collab-01 RLC headline, one rectifier lab shot, studio wires after resize."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8765
BASE = f"http://{HOST}:{PORT}"
CAPTURE_SUBDIR = os.environ.get("ARC_UX_CAPTURE_DIR", "round-smoke")
OUT = ROOT / "artifacts" / "ux-review" / CAPTURE_SUBDIR
W, H = 1440, 900


def _kill_port(port: int) -> None:
    try:
        subprocess.run(
            ["fuser", "-k", f"{port}/tcp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        pass
    time.sleep(0.3)


def _wait_health() -> None:
    for _ in range(80):
        try:
            with urllib.request.urlopen(f"{BASE}/api/health", timeout=2):
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError("UI not healthy")


def _api(method: str, path: str, data: dict | None = None) -> dict:
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())


def _run_series_rlc_collab() -> str:
    from electrical_engineer.engines.rlc_transient import series_rlc_step
    from electrical_engineer.runner.execute import execute

    meta = series_rlc_step(10, 0.01, 100e-6, 10.0)
    out = execute(
        "series-rlc-transient",
        cwd=ROOT,
        problem={
            "kind": "series_rlc",
            "vin": 10,
            "v_step": 10,
            "r_ohm": 10,
            "l_h": 0.01,
            "c_f": 100e-6,
            "analysis": "tran",
            "t_s": float(meta["t_Vc_peak_s"]),
            "probe": "v(3)",
            "tol": 0.02,
            "prompt": "Series RLC step",
        },
    )
    return out["run_id"]


def _assert_studio_wires(page, label: str) -> None:
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
    if info["n"] < 5 or info["empty"] or info["markers"] < info["n"]:
        raise RuntimeError(f"{label}: studio wires broken: {info}")


def _studio_wires_ready(page, minimum: int = 5, timeout_s: float = 60.0) -> None:
    deadline = time.time() + timeout_s
    paths = page.locator(".studio-canvas .react-flow__edge-path")
    while time.time() < deadline:
        if paths.count() >= minimum:
            return
        page.wait_for_timeout(250)
    raise RuntimeError(f"studio wires not ready (got {paths.count()})")


def main() -> int:
    global PORT, BASE
    sys.path.insert(0, str(ROOT / "scripts"))
    from capture_port import reserve_capture_port

    PORT = reserve_capture_port(int(os.environ.get("ARC_CAPTURE_PORT", PORT)))
    BASE = f"http://{HOST}:{PORT}"
    subprocess.check_call(["uv", "pip", "install", "-q", "-e", "."], cwd=ROOT)
    subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")
    OUT.mkdir(parents=True, exist_ok=True)

    env = {
        **os.environ,
        "EE_NO_BROWSER": "1",
        "EE_UI_PORT": str(PORT),
        "ARC_CAPTURE_PORT": str(PORT),
    }
    server = subprocess.Popen(
        [sys.executable, "-m", "electrical_engineer", "ui"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_health()
        from playwright.sync_api import sync_playwright

        # Studio after resize (matches UX capture assertion)
        req = urllib.request.Request(
            f"{BASE}/api/control-studio/sessions",
            method="POST",
            data=json.dumps({"title": "Smoke PID", "golden": "pid_dc_motor"}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            pid_sess = json.loads(resp.read().decode())["session_id"]

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": W, "height": H})
            page.goto(f"{BASE}/?view=studio&tab=control&session={pid_sess}", wait_until="domcontentloaded")
            _studio_wires_ready(page)
            page.set_viewport_size({"width": 1280, "height": 680})
            page.goto(f"{BASE}/?view=studio&tab=control&session={pid_sess}", wait_until="domcontentloaded")
            _studio_wires_ready(page, timeout_s=90.0)
            _assert_studio_wires(page, "studio-after-resize")
            page.screenshot(path=str(OUT / "studio-after-resize-smoke.png"))

            page.set_viewport_size({"width": W, "height": H})
            page.goto(f"{BASE}/?view=studio&tab=labs&lab=rectifier", wait_until="domcontentloaded")
            page.wait_for_selector(".lab-shell", timeout=30_000)
            page.get_by_role("radio", name="1φ half").check()
            page.get_by_role("radio", name="R", exact=True).check()
            page.locator('label:has-text("Line voltage")').locator('input[type="number"]').first.fill("230")
            page.locator('label:has-text("α (deg)")').locator('input[type="number"]').fill("30")
            page.wait_for_timeout(450)
            vo_txt = page.locator(".card").filter(has_text="Vo").locator("strong").inner_text()
            page.screenshot(path=str(OUT / "lab-rectifier-hw1-r-alpha30-smoke.png"))
            if float(vo_txt.split()[0]) < 1.0:
                raise RuntimeError(f"rectifier smoke: Vo readout too low: {vo_txt!r}")

            rlc_id = _run_series_rlc_collab()
            page.goto(f"{BASE}/?problem={rlc_id}", wait_until="domcontentloaded")
            page.wait_for_selector("#lab-verify-heading", timeout=120_000)
            page.get_by_text("Agrees (limit", exact=False).first.wait_for(state="visible", timeout=120_000)
            loc = page.locator(".answer-card .answer-line").first
            text = loc.inner_text(timeout=60_000)
            if not re.search(r"11\.630", text):
                raise RuntimeError(f"collab-01: expected Vc peak 11.630 V, got {text!r}")
            if not re.search(r"at\s+3\.628\s+ms", text):
                raise RuntimeError(f"collab-01: expected peak time 3.628 ms, got {text!r}")
            page.screenshot(path=str(OUT / "collab-01-run-sim-vs-derived-agrees-smoke.png"))
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=30)
    print("capture smoke ok", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())