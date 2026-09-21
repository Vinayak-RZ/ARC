"""Agent-style UI diagram trials: compose from skill templates, capture, ink gate."""

from __future__ import annotations

import os
import shutil
import struct
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from electrical_engineer.ui_diagrams.check import check_run_dir
from electrical_engineer.ui_diagrams.compose import compose_agent_trial_run

RUNS = ROOT / "runs"
MEDIA = ROOT / "docs" / "media" / "trials"
REPORT = ROOT / "docs" / "planning" / "UI_DIAGRAM_AGENT_TRIALS.md"
PORT = 8765
HOST = "127.0.0.1"
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 900
DOMAINS = ("rlc", "control", "power", "protection", "drives")


def _png_height(path: Path) -> int:
    raw = path.read_bytes()
    offset = 8
    while offset < len(raw):
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        chunk = raw[offset + 4 : offset + 8]
        if chunk == b"IHDR":
            _, h = struct.unpack(">II", raw[offset + 8 : offset + 16])
            return int(h)
        offset += 12 + length
    raise ValueError("IHDR missing")


def _require_pillow():
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("pip install Pillow") from exc
    return Image


def _diagram_has_ink(path: Path, *, circuit: bool) -> float:
    Image = _require_pillow()
    im = Image.open(path).convert("RGB")
    band = im.crop((180, 160, 1100, 560) if circuit else (240, 200, 1040, 520))
    pixels = band.size[0] * band.size[1]
    dark = sum(1 for r, g, b in band.getdata() if r + g + b < 450)
    frac = dark / pixels if pixels else 0.0
    if frac < 0.002:
        raise RuntimeError(f"{path.name}: blank band dark_frac={frac:.5f}")
    return frac


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


def _capture(page, run_id: str, dest: Path) -> tuple[int, float, bool]:
    url = f"http://{HOST}:{PORT}/?run={run_id}"
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector(".shell", timeout=20000)
    page.wait_for_selector(".lab-surface, .empty", timeout=20000)
    is_circuit = False
    if page.locator(".series-rlc-schematic").count():
        is_circuit = True
        page.wait_for_selector(".series-rlc-schematic", state="attached", timeout=20000)
        shapes = page.locator(".series-rlc-schematic line, .series-rlc-schematic path").count()
    elif page.locator(".static-diagram-wrap").count():
        page.wait_for_selector(".static-diagram", state="attached", timeout=20000)
        shapes = page.locator(
            ".static-diagram line, .static-diagram path, .static-diagram rect, .static-diagram circle"
        ).count()
    else:
        is_circuit = True
        shapes = page.locator(".flow-wrap .part-node").count()
    if shapes < 2:
        raise RuntimeError(f"expected >=2 shapes, saw {shapes}")
    page.wait_for_timeout(800)
    page.screenshot(
        path=str(dest),
        full_page=False,
        clip={"x": 0, "y": 0, "width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
    )
    frac = _diagram_has_ink(dest, circuit=is_circuit)
    return shapes, frac, is_circuit


def main() -> int:
    ui_dist = ROOT / "ui" / "dist" / "index.html"
    if not ui_dist.is_file():
        subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")

    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "check_ui_diagram_artifacts.py"), "--examples"])

    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    run_ids: dict[str, str] = {}

    for domain in DOMAINS:
        run_dir = compose_agent_trial_run(domain, RUNS)
        errs = check_run_dir(run_dir)
        if errs:
            raise RuntimeError(f"{domain} compose failed check: {errs}")
        run_ids[domain] = run_dir.name

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
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
            for domain in DOMAINS:
                rid = run_ids[domain]
                dest = MEDIA / f"trial-{domain}.png"
                try:
                    shapes, frac, _ = _capture(page, rid, dest)
                    status = "PASS"
                    note = ""
                except (RuntimeError, OSError, ValueError) as exc:
                    status = "FAIL"
                    note = str(exc)
                    shapes = 0
                    frac = 0.0
                rows.append(
                    {
                        "domain": domain,
                        "run_id": rid,
                        "status": status,
                        "shapes": shapes,
                        "dark_frac": frac,
                        "png": str(dest.relative_to(ROOT)),
                        "note": note,
                    }
                )
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)

    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# UI diagram agent trials",
        "",
        f"Generated: {stamp}",
        "",
        "Method: compose from `skills/ui-diagrams/examples/` (agent copy path), not README recipe seeds.",
        "",
        "| Domain | Status | Shapes | dark_frac | PNG | Run id |",
        "|--------|--------|--------|-----------|-----|--------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['domain']} | {r['status']} | {r['shapes']} | {r['dark_frac']:.4f} | `{r['png']}` | `{r['run_id']}` |"
        )
        if r["note"]:
            lines.append(f"\n_{r['domain']}: {r['note']}_\n")
    lines.append("")
    lines.append("Skill: `skills/ui-diagrams/SKILL.md`. Checker: `scripts/check_ui_diagram_artifacts.py --examples`.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    failed = [r for r in rows if r["status"] != "PASS"]
    if failed:
        print(f"{len(failed)} trial(s) failed", file=sys.stderr)
        return 1
    print(f"Wrote report {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
