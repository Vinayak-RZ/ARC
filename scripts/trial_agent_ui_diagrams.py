"""Agent-style UI diagram trials: compose from skill templates, capture, ink gate."""

from __future__ import annotations

import hashlib
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
from electrical_engineer.ui_diagrams.compose import compose_agent_trial_run, trial_run_id

RUNS = ROOT / "runs"
MEDIA = ROOT / "docs" / "media" / "trials"
REPORT = ROOT / "docs" / "planning" / "UI_DIAGRAM_AGENT_TRIALS.md"
PORT = 8765
HOST = "127.0.0.1"
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 900
DOMAINS = ("rlc", "control", "power", "protection", "drives")

# Per-domain UI waits (must match composed evidentiary titles / renderers).
DOMAIN_EXPECT: dict[str, dict] = {
    "rlc": {
        "title": "series RLC",
        "selector": ".series-rlc-schematic",
        "shape_sel": ".series-rlc-schematic line, .series-rlc-schematic path",
        "circuit": True,
        "min_shapes": 8,
    },
    "control": {
        "title": "unity feedback",
        "selector": ".static-diagram",
        "shape_sel": ".static-diagram line, .static-diagram path, .static-diagram rect, .static-diagram circle",
        "hint": "Unity feedback system",
        "circuit": False,
        "min_shapes": 8,
    },
    "power": {
        "title": "LG fault",
        "selector": ".static-diagram",
        "shape_sel": ".static-diagram line, .static-diagram path, .static-diagram rect, .static-diagram circle",
        "hint": "single-line",
        "circuit": False,
        "min_shapes": 8,
    },
    "protection": {
        "title": "50/51",
        "selector": ".static-diagram",
        "shape_sel": ".static-diagram line, .static-diagram path, .static-diagram rect, .static-diagram circle",
        "hint": "Feeder protection",
        "circuit": False,
        "min_shapes": 8,
    },
    "drives": {
        "title": "DC drive",
        "selector": ".static-diagram",
        "shape_sel": ".static-diagram line, .static-diagram path, .static-diagram rect, .static-diagram circle",
        "hint": "armature",
        "circuit": False,
        "min_shapes": 6,
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def _capture(page, domain: str, run_id: str, dest: Path) -> tuple[int, float]:
    spec = DOMAIN_EXPECT[domain]
    url = f"http://{HOST}:{PORT}/?run={run_id}"
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector(".shell", timeout=20000)
    page.wait_for_selector(".lab-surface", timeout=20000)
    page.get_by_text(spec["title"], exact=False).first.wait_for(timeout=20000)
    if spec.get("hint"):
        page.get_by_text(spec["hint"], exact=False).first.wait_for(timeout=20000)
    page.wait_for_selector(spec["selector"], state="attached", timeout=20000)
    shapes = page.locator(spec["shape_sel"]).count()
    if shapes < spec["min_shapes"]:
        raise RuntimeError(f"{domain}: expected >={spec['min_shapes']} shapes, saw {shapes}")
    page.wait_for_timeout(600)
    page.screenshot(
        path=str(dest),
        full_page=False,
        clip={"x": 0, "y": 0, "width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
    )
    frac = _diagram_has_ink(dest, circuit=bool(spec["circuit"]))
    return shapes, frac


def _assert_distinct_pngs(paths: list[Path]) -> None:
    digests = [_sha256(p) for p in paths]
    if len(set(digests)) != len(digests):
        dup = {d: [] for d in digests}
        for p, d in zip(paths, digests, strict=True):
            dup[d].append(p.name)
        clashes = {d: names for d, names in dup.items() if len(names) > 1}
        raise RuntimeError(f"duplicate trial PNG SHA-256: {clashes}")


def main() -> int:
    ui_dist = ROOT / "ui" / "dist" / "index.html"
    if not ui_dist.is_file():
        subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")

    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "check_ui_diagram_artifacts.py"), "--examples"])

    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    rows: list[dict] = []
    run_ids: dict[str, str] = {}
    png_paths: list[Path] = []

    for domain in DOMAINS:
        rid = trial_run_id(domain, stamp)
        run_dir = compose_agent_trial_run(domain, RUNS, run_id=rid)
        errs = check_run_dir(run_dir)
        if errs:
            raise RuntimeError(f"{domain} compose failed check: {errs}")
        run_ids[domain] = rid

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
                    shapes, frac = _capture(page, domain, rid, dest)
                    digest = _sha256(dest)
                    status = "PASS"
                    note = ""
                except (RuntimeError, OSError, ValueError) as exc:
                    status = "FAIL"
                    note = str(exc)
                    shapes = 0
                    frac = 0.0
                    digest = ""
                rows.append(
                    {
                        "domain": domain,
                        "run_id": rid,
                        "status": status,
                        "shapes": shapes,
                        "dark_frac": frac,
                        "sha256": digest,
                        "png": str(dest.relative_to(ROOT)),
                        "note": note,
                    }
                )
                if dest.is_file():
                    png_paths.append(dest)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)

    failed = [r for r in rows if r["status"] != "PASS"]
    if not failed:
        try:
            _assert_distinct_pngs([MEDIA / f"trial-{d}.png" for d in DOMAINS])
        except RuntimeError as exc:
            for r in rows:
                r["status"] = "FAIL"
                r["note"] = str(exc)
            failed = rows

    stamp_report = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# UI diagram agent trials",
        "",
        f"Generated: {stamp_report}",
        "",
        "Method: compose from `skills/ui-diagrams/examples/` (agent copy path), not README recipe seeds.",
        "Each domain uses a **distinct** run id `trl-<domain>-<stamp>` and must produce a **distinct** PNG SHA-256.",
        "",
        "| Domain | Status | Shapes | dark_frac | SHA-256 (prefix) | PNG | Run id |",
        "|--------|--------|--------|-----------|------------------|-----|--------|",
    ]
    for r in rows:
        pref = (r["sha256"][:16] + "…") if r.get("sha256") else "—"
        lines.append(
            f"| {r['domain']} | {r['status']} | {r['shapes']} | {r['dark_frac']:.4f} | `{pref}` | `{r['png']}` | `{r['run_id']}` |"
        )
        if r.get("note"):
            lines.append(f"\n_{r['domain']}: {r['note']}_\n")
    if rows and all(r.get("sha256") for r in rows if r["status"] == "PASS"):
        lines.append("")
        lines.append("## Full SHA-256")
        for r in rows:
            if r.get("sha256"):
                lines.append(f"- `{r['domain']}`: `{r['sha256']}`")
    lines.append("")
    lines.append("Skill: `skills/ui-diagrams/SKILL.md`. Checker: `scripts/check_ui_diagram_artifacts.py --examples`.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if failed:
        print(f"{len(failed)} trial(s) failed", file=sys.stderr)
        return 1
    print(f"Wrote report {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
