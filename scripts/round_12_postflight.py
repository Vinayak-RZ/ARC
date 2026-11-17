#!/usr/bin/env python3
"""Scan round-12 PNGs, enrich preflight.json, write INDEX.md for Design critique."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_CAPTURE_SUBDIR = os.environ.get("ARC_UX_CAPTURE_DIR", "round-12")
OUT = ROOT / "artifacts" / "ux-review" / _CAPTURE_SUBDIR
BAD_RE = re.compile(r"\b(NaN|undefined)\b", re.IGNORECASE)


def _png_mean_luminance(path: Path) -> float:
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        return 255.0
    pos = 8
    data = b""
    width = height = 0
    color_type = 2
    while pos < len(raw):
        ln = struct.unpack(">I", raw[pos : pos + 4])[0]
        kind = raw[pos + 4 : pos + 8]
        chunk = raw[pos + 8 : pos + 8 + ln]
        pos += 12 + ln
        if kind == b"IHDR":
            width, height = struct.unpack(">II", chunk[:8])
            color_type = chunk[9] if len(chunk) > 9 else 2
        elif kind == b"IDAT":
            data += chunk
        elif kind == b"IEND":
            break
    if not data or not width:
        return 128.0
    bpp = 4 if color_type in (4, 6) else 3
    stream = zlib.decompress(data)
    row_bytes = width * bpp
    total = 0.0
    count = 0
    y = 0
    off = 0
    while y < height and off < len(stream):
        off += 1
        row = stream[off : off + row_bytes]
        off += row_bytes
        for i in range(0, len(row) - 2, bpp):
            r, g, b = row[i : i + 3]
            total += 0.2126 * r + 0.7152 * g + 0.0722 * b
            count += 1
        y += 1
        if count > 120_000:
            break
    return total / max(count, 1)


def _git_ci_status() -> dict:
    try:
        out = subprocess.check_output(
            ["gh", "pr", "view", "--json", "statusCheckRollup,commits", "-q", ".statusCheckRollup"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        checks = json.loads(out or "[]")
        return {
            "checks": [
                {
                    "name": c.get("name"),
                    "state": c.get("state") or c.get("conclusion"),
                    "url": c.get("detailsUrl"),
                }
                for c in checks
            ]
        }
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return {"checks": [], "note": "CI status unavailable from gh"}


def _describe_file(name: str) -> tuple[str, str, str, str]:
    """screen, theme, viewport, look_at"""
    theme = "dark" if "-dark.png" in name or name.endswith("-dark.png") else "light"
    if "-1024-" in name:
        vp = "1024×900"
    else:
        vp = "1440×900"
    stem = name.replace(".png", "")
    if stem.startswith("collab-01"):
        return (
            "Collaboration 1 · RLC run",
            theme,
            vp,
            "Simulated vs derived card shows Agrees (limit 2%).",
        )
    if stem.startswith("collab-02"):
        return (
            "Collaboration 2 · Circuit lab",
            theme,
            vp,
            "Provenance bar, Vc waveform, Activity drawer after agent build.",
        )
    if stem.startswith("collab-03-out-of-date"):
        return (
            "Collaboration 3 · Out of date",
            theme,
            vp,
            "Human R1→20 Ω; derived out of date; Ask agent to re-derive CTA.",
        )
    if stem.startswith("collab-03b"):
        return (
            "Collaboration 3b · After re-derive",
            theme,
            vp,
            "Agrees after agent re-derive; R1 = 20 Ω; no overshoot; t_s ≈ 5.83 ms.",
        )
    if stem.startswith("collab-04-changes"):
        return (
            "Collaboration 4 · Changes chip",
            theme,
            vp,
            "Changes view with R1: 10 → 20 Ω chip.",
        )
    if stem.startswith("collab-04b"):
        return (
            "Collaboration 4b · Restore",
            theme,
            vp,
            "After Restore agent version on circuit lab.",
        )
    if stem.startswith("collab-05"):
        return (
            "Collaboration 5 · Forward Euler mismatch",
            theme,
            vp,
            "Real rlc-bad-derive example: forward-Euler derivation vs ngspice.",
        )
    if stem.startswith("lab-rectifier-full3"):
        return (
            "Lab · Rectifier",
            theme,
            vp,
            "3φ full, RL load, α = 75°; Vo readout ≈ 145.1 V.",
        )
    if re.match(r"lab-rectifier-(hw1|semi1|full1|hw3|semi3|full3)-r-alpha\d+", stem):
        return (
            "Lab · Rectifier",
            theme,
            vp,
            "Rectifier topology sweep — R load, α as in filename (no RL except full3-rl-alpha75).",
        )
    if "collab-06-control-unity-run" in stem:
        return (
            "Collaboration 6 · Control run",
            theme,
            vp,
            "Unity-feedback run page agreement card.",
        )
    if stem.startswith("problem-control-checked-lab-agreement"):
        return (
            "Control-step studio lab",
            theme,
            vp,
            "First-order step gallery run: simulated vs derived in lab drawer after Simulate.",
        )
    if stem.startswith("problem-control-checked-work"):
        return ("Control-step run", theme, vp, "Gallery first-order step, Work tab checked.")
    if stem.startswith("problem-control-checked"):
        return ("Control-step run", theme, vp, "Gallery first-order step with agreement card.")
    if "collab-06-control-unity-lab" in stem:
        return (
            "Collaboration 6 · Control lab",
            theme,
            vp,
            "Step metrics: y_ss≈0.909, t_s≈0.36 s on unity lab session.",
        )
    if stem.startswith("run-rectifier"):
        return ("Rectifier example run", theme, vp, "Checked three-phase rectifier run summary.")
    if stem.startswith("run-idmt"):
        return ("IDMT example run", theme, vp, "IDMT relay coordination run summary.")
    hints = {
        "home-empty": ("Home", "Empty composer, six example tiles."),
        "home-with-recent": ("Home", "Recent run strip after divider."),
        "problems-list": ("Problems", "Runs table."),
        "studio-layout-after-simulate": ("Studio · Control", "PID golden after Simulate."),
        "studio-circuit-series-rlc": ("Studio · Circuits", "Series RLC preset on sandbox."),
        "gallery": ("Gallery", "Workflow cards."),
        "library": ("Library", "Reference corpus."),
        "learn-landing": ("Learn", "Semester rail landing."),
        "settings-agents": ("Settings", "Agents tab."),
        "problem-answer": ("Run page", "Divider diagram tab."),
        "problem-circuit-checked": ("Run page", "RLC example checked."),
        "lab-idmt": ("Lab · IDMT", "IDMT coordination workspace."),
        "lab-rectifier": ("Lab · Rectifier", "Rectifier study workspace."),
    }
    base = stem.replace("-light", "").replace("-dark", "").replace("-1024-light", "").replace("-1024-dark", "")
    for key, (screen, look) in hints.items():
        if base == key or base.startswith(key):
            return (screen, theme, vp, look)
    return (stem.replace("-", " "), theme, vp, "Main product surface.")


def main() -> int:
    if not OUT.is_dir():
        raise SystemExit(f"missing {OUT}")

    pf_path = OUT / "preflight.json"
    pf = json.loads(pf_path.read_text(encoding="utf-8")) if pf_path.is_file() else {}

    pngs = sorted(OUT.glob("*.png"))
    scan = {"files": [], "dark_integrity_failures": [], "nan_text_hits": []}
    light_lums: dict[str, float] = {}
    for path in pngs:
        lum = _png_mean_luminance(path)
        entry = {"file": path.name, "mean_luminance": round(lum, 2)}
        if path.name.endswith("-dark.png") or "-dark." in path.name:
            light_name = path.name.replace("-dark.png", "-light.png").replace("-dark.", "-light.")
            light_path = OUT / light_name
            if light_path.is_file() and abs(
                lum - light_lums.get(light_name, _png_mean_luminance(light_path))
            ) < 4:
                scan["dark_integrity_failures"].append(
                    {"dark": path.name, "light": light_name, "reason": "mean luminance too close to light"}
                )
            if lum > 95:
                scan["dark_integrity_failures"].append({"dark": path.name, "reason": f"mean luminance {lum:.1f} too bright"})
        else:
            light_lums[path.name] = lum
        scan["files"].append(entry)

    pf["capture_scan"] = scan
    pf["ci_status_rollup"] = _git_ci_status()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    pf["git_sha"] = head
    pf["git_sha_short"] = head[:7]
    if os.environ.get("ROUND12_CI_RUN_ID"):
        pf["ci_workflow_run_id"] = os.environ["ROUND12_CI_RUN_ID"]
    if os.environ.get("ROUND12_CI_STATUS"):
        pf["ci_workflow_status"] = os.environ["ROUND12_CI_STATUS"]
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
    dirty_lines = [ln for ln in dirty.splitlines() if ln and not ln.startswith("??")]
    pf["git_dirty_lines"] = len(dirty_lines)
    diff = subprocess.check_output(["git", "diff", "HEAD"], cwd=ROOT, text=True)
    pf["git_diff_sha256"] = hashlib.sha256(diff.encode()).hexdigest()[:16] if diff.strip() else None
    ci_run = os.environ.get("ROUND12_CI_RUN_ID") or pf.get("ci_workflow_run_id")
    pf_ci_status = os.environ.get("ROUND12_CI_STATUS") or pf.get("ci_workflow_status") or ""
    product_sha = os.environ.get("CAPTURE_PRODUCT_SHA") or pf.get("capture_product_git_sha") or head
    pf["ci_reference"] = {
        "head_sha": product_sha,
        "head_sha_short": product_sha[:7],
        "workflow_run_id": str(ci_run) if ci_run else "",
        "status": pf_ci_status,
    }
    if os.environ.get("CAPTURE_PRODUCT_SHA"):
        pf["capture_product_git_sha"] = os.environ["CAPTURE_PRODUCT_SHA"]
    pf["png_count"] = len(pngs)
    ngspice_txt = OUT / ".ngspice_version"
    ng_cached = ngspice_txt.read_text(encoding="utf-8").strip() if ngspice_txt.is_file() else ""
    if ng_cached and not ng_cached.startswith("*"):
        pf["ngspice_version"] = ng_cached
    elif shutil.which("ngspice"):
        proc = subprocess.run(["ngspice", "-v"], capture_output=True, text=True, check=False)
        banner = (proc.stdout + proc.stderr).strip().splitlines()
        ver = next((ln.strip().strip("*").strip() for ln in banner if "ngspice" in ln.lower()), banner[-1] if banner else "")
        pf["ngspice_version"] = ver
        ngspice_txt.write_text(ver + "\n", encoding="utf-8")
    pf_path.write_text(json.dumps(pf, indent=2) + "\n", encoding="utf-8")

    known: list[str] = []
    if scan["dark_integrity_failures"]:
        known.append(
            "Automated dark vs light luminance pairs flagged (spot-check): "
            + "; ".join(f"{f.get('dark')}" for f in scan["dark_integrity_failures"][:8])
        )

    round_title = _CAPTURE_SUBDIR.replace("-", " ").title()
    notes = [
        f"# {round_title} captures",
        "",
        f"PNG count: {len(pngs)}",
        "",
        (
            "Includes round-11 coverage, 1280×800 home scroll companions (incl. `home-scrolled-1280-dark.png`), "
            "collab-03–05 (live forward-Euler mismatch), rectifier topology sweep (two α per topology), "
            "and `lab-rectifier-full3-rl-alpha75` (Vo ≈ 145.1 V)."
        ),
        "",
        f"Capture HEAD: `{pf.get('git_sha_short')}` · CI run `{pf.get('ci_workflow_run_id', '—')}` · `git_dirty_lines`: {pf.get('git_dirty_lines')}.",
        "",
    ]
    if known:
        notes.extend(["## Known issues", ""] + [f"- {x}" for x in known] + [""])
    (OUT / "NOTES.md").write_text("\n".join(notes), encoding="utf-8")

    md5_lines = []
    for path in pngs:
        md5_lines.append(f"{path.name}  {hashlib.md5(path.read_bytes()).hexdigest()}")
    (OUT / "md5.txt").write_text("\n".join(md5_lines) + "\n", encoding="utf-8")

    fixture_stems: set[str] = set()

    lines = [
        "# Round 12 — UX capture index",
        "",
        f"Git HEAD: `{pf.get('git_sha', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())}`",
        f"Short SHA: `{pf.get('git_sha_short', '?')}`",
        f"CI workflow run: `{pf.get('ci_workflow_run_id', '—')}`",
        f"`git_dirty_lines`: {pf.get('git_dirty_lines', '?')}",
        f"PNG count: {len(pngs)}",
        "",
        "## How to read",
        "",
        "| File | Screen | Theme | Viewport | Staged | What to look at |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for path in pngs:
        screen, theme, vp, look = _describe_file(path.name)
        stem = path.name.replace(".png", "").replace("-light", "").replace("-dark", "")
        staged = "fixture" if any(stem.startswith(f) for f in fixture_stems) else ""
        lines.append(f"| `{path.name}` | {screen} | {theme} | {vp} | {staged} | {look} |")

    lines.extend(
        [
            "",
            "## Collaboration loop (numbered)",
            "",
            "1. `collab-01-run-sim-vs-derived-agrees-*.png` — agent RLC solve with Agrees.",
            "2. `collab-02-lab-provenance-vc-activity-*.png` — Studio lab with provenance, Vc plot, Activity.",
            "3. `collab-03-out-of-date-ask-rederive-*.png` — Out of date + Ask agent to re-derive.",
            "3b. `collab-03b-after-rederive-agrees-*.png` — Agrees after re-derive; R1 = 20 Ω; t_s ≈ 5.83 ms.",
            "4. `collab-04-changes-r1-chip-*.png` — Changes tab with R1: 10 → 20 Ω chip.",
            "4b. `collab-04b-after-restore-*.png` — After Restore agent version.",
            "5. `collab-05-forward-euler-mismatch-*.png` — live forward-Euler derive vs ngspice (not a JSON fixture).",
            "6. `collab-06-control-unity-run-agrees-*.png` + `collab-06-control-unity-lab-agreement-*.png` — unity control run + lab.",
            "",
            "Rectifier: `lab-rectifier-full3-rl-alpha75-*.png` — 3φ full, RL, α = 75°, Vo ≈ 145.1 V.",
            "",
            "## Known issues",
            "",
        ]
    )
    if known:
        lines.extend(f"- {item}" for item in known)
    else:
        lines.append("- None noted during automated scan; spot-check clipped labels during critique.")
    lines.append("")
    (OUT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT / "INDEX.md", "preflight updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())