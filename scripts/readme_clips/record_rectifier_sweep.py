"""Record the rectifier firing-angle sweep: 3-phase full bridge, R load, 415 V, alpha 0 -> 120 deg."""

import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("BASE", "http://127.0.0.1:8765")
THEME = os.environ.get("THEME", "light")
OUT = Path(os.environ.get("OUT", "build/readme-clips/raw-rect"))
OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(
        viewport={"width": 1440, "height": 1000},
        record_video_dir=str(OUT),
        record_video_size={"width": 1440, "height": 1000},
    )
    ctx.add_init_script(f'localStorage.setItem("arc-theme", "{THEME}")')
    page = ctx.new_page()
    t0 = time.time()
    page.goto(f"{BASE}/?view=studio&tab=labs&lab=rectifier&ymax=600", wait_until="networkidle")
    page.wait_for_selector(".lab-shell")
    page.get_by_role("radio", name="3φ full").check()
    page.get_by_role("radio", name="R", exact=True).check()
    page.locator('label:has-text("Line voltage")').locator('input[type="number"]').first.fill("415")
    a_num = page.locator('label:has-text("α (deg)")').locator('input[type="number"]')
    a_num.fill("0")
    page.wait_for_timeout(600)
    print("sweep_start", round(time.time() - t0, 2), flush=True)
    rng = page.locator('label:has-text("α (deg)")').locator('input[type="range"]')
    rng.focus()
    for a in range(1, 121):
        rng.press("ArrowRight")
        page.wait_for_timeout(110 if a not in (30, 60, 75, 90) else 700)
    page.wait_for_timeout(1500)
    print("sweep_end", round(time.time() - t0, 2), flush=True)
    vo = page.locator(".card", has_text="Vo").first.inner_text()
    print("readout at 120:", vo.replace("\n", " "))
    ctx.close()
    b.close()
print(max(OUT.glob("*.webm")))
