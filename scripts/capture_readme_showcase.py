#!/usr/bin/env python3
"""Capture README showcase images at 2x scale into docs/assets/readme/."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "readme"
HOST = "http://127.0.0.1:8765"
VP = {"width": 1280, "height": 800}

SHOTS = [
    ("home-light.png", f"{HOST}/?view=home", "Load"),
    ("studio-hero-light.png", None, "studio_simulate"),
    ("problem-checked-light.png", None, "problem_divider"),
    ("gallery-light.png", f"{HOST}/?view=gallery", "Load"),
    ("library-light.png", f"{HOST}/?view=library", "Load"),
    ("studio-dark.png", None, "studio_simulate_dark"),
]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pip install playwright && playwright install chromium", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, url, kind in SHOTS:
            ctx = browser.new_context(viewport=VP, device_scale_factor=2)
            page = ctx.new_page()
            if kind == "studio_simulate" or kind == "studio_simulate_dark":
                if kind.endswith("_dark"):
                    page.add_init_script('localStorage.setItem("arc-theme", "dark")')
                page.goto(f"{HOST}/?view=studio")
                r = page.request.post(
                    f"{HOST}/api/control-studio/sessions",
                    data={"title": "HW 3 · Unity feedback, K = 10", "golden": "unity_first_order"},
                )
                sid = r.json()["session_id"]
                page.goto(f"{HOST}/?view=studio&session={sid}")
                page.get_by_role("button", name="Simulate").click()
                page.wait_for_selector(".studio-step-svg", timeout=120000)
            elif kind == "problem_divider":
                (ROOT / "problem.json").write_text(
                    '{"kind":"voltage_divider","vin":10,"r1":1000,"r2":1000}\n',
                    encoding="utf-8",
                )
                out = subprocess.check_output(
                    [sys.executable, "-m", "electrical_engineer", "run", "solve-circuit-problem"],
                    cwd=ROOT,
                    text=True,
                )
                run_id = next((ln.strip() for ln in out.splitlines() if ln.strip()), "")
                page.goto(f"{HOST}/?run={run_id}")
                page.wait_for_selector(".verification-ok", timeout=60000)
            else:
                page.goto(url)
                page.wait_for_load_state("networkidle")
            page.screenshot(path=str(OUT / name), full_page=False)
            ctx.close()
            print(name, (OUT / name).stat().st_size)
        browser.close()
    for png in OUT.glob("*.png"):
        if png.stat().st_size > 400_000:
            subprocess.check_call(["pngquant", "--force", "--quality=65-90", "-o", str(png), str(png)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
