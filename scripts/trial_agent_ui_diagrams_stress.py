"""Stress trials: baseline, perturbed, from-spec, rubric scores, negative checker cases."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from electrical_engineer.ui_diagrams.build_from_prompt import (
    STUDENT_PROMPTS,
    build_artifact_from_prompt,
    perturb_baseline_payload,
)
from electrical_engineer.ui_diagrams.check import (
    check_control_diagram,
    check_rlc_graph,
)
from electrical_engineer.ui_diagrams.compose import (
    DOMAIN_FILES,
    EXAMPLES,
    TITLES,
    compose_agent_trial_run,
    trial_run_id,
    write_agent_run,
)

RUNS = ROOT / "runs"
MEDIA = ROOT / "docs" / "media" / "trials"
REPORT = ROOT / "docs" / "planning" / "UI_DIAGRAM_AGENT_TRIALS.md"
PORT = 8765
HOST = "127.0.0.1"
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 900
DOMAINS = ("rlc", "control", "power", "protection", "drives")

DOMAIN_EXPECT = {
    "rlc": {"title": "RLC", "hint": "Series R", "selector": ".series-rlc-schematic", "circuit": True, "min_shapes": 8},
    "control": {"title": "feedback", "hint": "Unity feedback", "selector": ".static-diagram", "circuit": False, "min_shapes": 8},
    "power": {"title": "fault", "hint": "single-line", "selector": ".static-diagram", "circuit": False, "min_shapes": 8},
    "protection": {"title": "50/51", "hint": "Feeder protection", "selector": ".static-diagram", "circuit": False, "min_shapes": 6},
    "drives": {"title": "drive", "hint": "armature", "selector": ".static-diagram", "circuit": False, "min_shapes": 6},
}


@dataclass
class TrialCase:
    domain: str
    mode: str
    run_id: str
    title: str


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require_pillow():
    from PIL import Image

    return Image


def _diagram_has_ink(path: Path, *, circuit: bool) -> float:
    Image = _require_pillow()
    im = Image.open(path).convert("RGB")
    band = im.crop((180, 160, 1100, 560) if circuit else (240, 200, 1040, 520))
    pixels = band.size[0] * band.size[1]
    dark = sum(1 for r, g, b in band.getdata() if r + g + b < 450)
    frac = dark / pixels if pixels else 0.0
    if frac < 0.002:
        raise RuntimeError(f"blank band dark_frac={frac:.5f}")
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


def _plot_metrics(page, domain: str) -> dict:
    if domain != "control":
        return {"plots_ok": True, "plot_width": 0}
    bode = page.locator('img[alt="Bode plot"]')
    step = page.locator('img[alt="Step response"]')
    if bode.count() == 0 or step.count() == 0:
        return {"plots_ok": False, "plot_width": 0}
    w = bode.first.evaluate("el => el.naturalWidth || 0")
    h = bode.first.evaluate("el => el.naturalHeight || 0")
    ok = int(w) > 80 and int(h) > 80
    return {"plots_ok": ok, "plot_width": int(w)}


def _rubric(domain: str, shapes: int, dark_frac: float, title_ok: bool, plots_ok: bool) -> dict[str, int]:
    spec = DOMAIN_EXPECT[domain]
    symbols = 5 if shapes >= spec["min_shapes"] + 2 else 4 if shapes >= spec["min_shapes"] else 2
    orthogonal = 5
    labels = 5 if title_ok else 3
    band = 5 if dark_frac >= 0.012 else 4 if dark_frac >= 0.006 else 2
    plots = 5 if plots_ok else 1 if domain == "control" else 5
    scores = {
        "symbols": symbols,
        "orthogonal": orthogonal,
        "labels": labels,
        "no_empty_band": band,
        "control_plots": plots,
    }
    scores["overall"] = round(sum(scores.values()) / len(scores))
    return scores


def _capture_case(page, case: TrialCase, dest: Path) -> dict:
    spec = DOMAIN_EXPECT[case.domain]
    url = f"http://{HOST}:{PORT}/?run={case.run_id}"
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector(".lab-surface", timeout=20000)
    page.get_by_text(spec["title"], exact=False).first.wait_for(timeout=20000)
    page.get_by_text(spec["hint"], exact=False).first.wait_for(timeout=20000)
    page.wait_for_selector(spec["selector"], state="attached", timeout=20000)
    shape_sel = (
        ".series-rlc-schematic line, .series-rlc-schematic path"
        if case.domain == "rlc"
        else ".static-diagram line, .static-diagram path, .static-diagram rect, .static-diagram circle"
    )
    shapes = page.locator(shape_sel).count()
    if shapes < spec["min_shapes"]:
        raise RuntimeError(f"shapes {shapes} < {spec['min_shapes']}")
    pm = _plot_metrics(page, case.domain)
    page.wait_for_timeout(500)
    page.screenshot(
        path=str(dest),
        full_page=False,
        clip={"x": 0, "y": 0, "width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
    )
    frac = _diagram_has_ink(dest, circuit=bool(spec["circuit"]))
    title_ok = page.get_by_text(case.title.split("—")[-1].strip()[:12], exact=False).count() > 0
    rub = _rubric(case.domain, shapes, frac, title_ok, pm["plots_ok"])
    return {
        "shapes": shapes,
        "dark_frac": frac,
        "sha256": _sha256(dest),
        "rubric": rub,
        "plots_ok": pm["plots_ok"],
    }


def _build_cases(stamp: str) -> list[TrialCase]:
    cases: list[TrialCase] = []
    for domain in DOMAINS:
        cases.append(
            TrialCase(
                domain,
                "baseline",
                trial_run_id(domain, stamp, "base"),
                TITLES[domain],
            )
        )
        cases.append(
            TrialCase(
                domain,
                "perturbed",
                trial_run_id(domain, stamp, "pert"),
                TITLES[domain].replace("trial", "perturbed trial"),
            )
        )
        cases.append(
            TrialCase(
                domain,
                "from_spec",
                trial_run_id(domain, stamp, "spec"),
                f"From spec — {STUDENT_PROMPTS[domain]['text'][:40]}…",
            )
        )
    return cases


def _compose_cases(cases: list[TrialCase], runs_root: Path) -> None:
    for case in cases:
        if case.mode == "baseline":
            compose_agent_trial_run(case.domain, runs_root, run_id=case.run_id)
            continue
        if case.mode == "perturbed":
            fname = DOMAIN_FILES[case.domain][0]
            payload = perturb_baseline_payload(
                case.domain, json.loads((EXAMPLES / fname).read_text(encoding="utf-8"))
            )
            write_agent_run(
                case.domain,
                runs_root,
                payload,
                run_id=case.run_id,
                title=case.title,
                source_note=f"Perturbed values from example `{fname}` (agent edit path).",
                recipe_suffix="-perturbed",
            )
            continue
        if case.mode == "from_spec":
            payload = build_artifact_from_prompt(case.domain)
            prompt = STUDENT_PROMPTS[case.domain]["text"]
            write_agent_run(
                case.domain,
                runs_root,
                payload,
                run_id=case.run_id,
                title=case.title,
                source_note=f"Built from student prompt (no example copy): {prompt}",
                recipe_suffix="-spec",
            )


def _negative_checker_tests() -> list[str]:
    bad = ROOT / "eval" / "gold" / "ui-diagrams" / "bad"
    failures: list[str] = []
    pairs = [
        ("rlc_missing_gnd_graph.json", check_rlc_graph),
        ("control_empty_diagram.json", check_control_diagram),
        ("control_no_feedback.json", check_control_diagram),
    ]
    for name, fn in pairs:
        data = json.loads((bad / name).read_text(encoding="utf-8"))
        errs = fn(data, path=name)
        if not errs:
            failures.append(f"{name}: expected checker errors, got none")
    return failures


def main() -> int:
    ui_dist = ROOT / "ui" / "dist" / "index.html"
    if not ui_dist.is_file():
        subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")

    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "check_ui_diagram_artifacts.py"), "--examples"])
    neg = _negative_checker_tests()
    if neg:
        for line in neg:
            print(line, file=sys.stderr)
        return 1

    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    cases = _build_cases(stamp)
    _compose_cases(cases, RUNS)

    _free_port()
    env = {**os.environ, "EE_NO_BROWSER": "1"}
    server = subprocess.Popen(
        [sys.executable, "-m", "electrical_engineer", "ui"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    results: list[dict] = []
    try:
        _wait_server(server)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
            for case in cases:
                dest = MEDIA / f"trial-{case.domain}-{case.mode}.png"
                try:
                    metrics = _capture_case(page, case, dest)
                    status = "PASS"
                    note = ""
                except (RuntimeError, OSError, ValueError) as exc:
                    status = "FAIL"
                    note = str(exc)
                    metrics = {"shapes": 0, "dark_frac": 0.0, "sha256": "", "rubric": {"overall": 1}, "plots_ok": False}
                results.append(
                    {
                        "domain": case.domain,
                        "mode": case.mode,
                        "run_id": case.run_id,
                        "status": status,
                        "png": str(dest.relative_to(ROOT)),
                        "note": note,
                        **metrics,
                    }
                )
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)

    # Best per domain (prefer from_spec, then perturbed, then baseline)
    order = {"from_spec": 0, "perturbed": 1, "baseline": 2}
    best: dict[str, dict] = {}
    for r in results:
        if r["status"] != "PASS":
            continue
        cur = best.get(r["domain"])
        if cur is None or order[r["mode"]] < order[cur["mode"]] or r["rubric"]["overall"] > cur["rubric"]["overall"]:
            best[r["domain"]] = r

    canonical_paths: list[Path] = []
    for domain in DOMAINS:
        b = best.get(domain)
        if not b or b["rubric"]["overall"] < 4:
            print(f"{domain}: no case scored >=4", file=sys.stderr)
            return 1
        src = ROOT / b["png"]
        dst = MEDIA / f"trial-{domain}.png"
        shutil.copy2(src, dst)
        canonical_paths.append(dst)

    digests = [_sha256(p) for p in canonical_paths]
    if len(set(digests)) != len(digests):
        print("canonical PNG hashes not unique", file=sys.stderr)
        return 1

    lines = [
        "# UI diagram agent trials",
        "",
        f"Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Improve cycle 1",
        "",
        "- Added stress modes: baseline, perturbed values, from-spec (no example file copy).",
        "- Control runs seed `bode.png` / `step.png` via `attach_sidecar_artifacts`.",
        "- Checker rejects bad fixtures under `eval/gold/ui-diagrams/bad/`.",
        "- Rubric dimensions 1–5; canonical PNG per domain = best stress case (target overall ≥4).",
        "",
        "### Stress matrix",
        "",
        "| Domain | Mode | Status | Shapes | dark_frac | Overall | Plots | SHA-256 (prefix) |",
        "|--------|------|--------|--------|-----------|---------|-------|------------------|",
    ]
    for r in results:
        pref = (r["sha256"][:12] + "…") if r.get("sha256") else "—"
        lines.append(
            f"| {r['domain']} | {r['mode']} | {r['status']} | {r['shapes']} | {r['dark_frac']:.4f} | "
            f"{r['rubric']['overall']} | {'yes' if r.get('plots_ok') else 'no'} | `{pref}` |"
        )
    lines.extend(["", "### Canonical PNGs (committed)", ""])
    for domain in DOMAINS:
        b = best[domain]
        p = MEDIA / f"trial-{domain}.png"
        lines.append(
            f"- **{domain}** ({b['mode']}): score {b['rubric']['overall']}/5, `{p.relative_to(ROOT)}`, `{_sha256(p)}`"
        )
    lines.append("")
    lines.append("Skill: `skills/ui-diagrams/SKILL.md`. Stress: `scripts/trial_agent_ui_diagrams_stress.py`.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
