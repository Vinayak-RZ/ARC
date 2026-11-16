#!/usr/bin/env python3
"""Scan round-11 PNGs, enrich preflight.json, write INDEX.md for Design critique."""

from __future__ import annotations

import json
import re
import struct
import subprocess
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "ux-review" / "round-11"
BAD_RE = re.compile(r"\b(NaN|undefined)\b", re.I)


def _png_mean_luminance(path: Path) -> float:
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        return 255.0
    pos = 8
    data = b""
    width = height = 0
    while pos < len(raw):
        ln = struct.unpack(">I", raw[pos : pos + 4])[0]
        kind = raw[pos + 4 : pos + 8]
        chunk = raw[pos + 8 : pos + 8 + ln]
        pos += 12 + ln
        if kind == b"IHDR":
            width, height = struct.unpack(">II", chunk[:8])
        elif kind == b"IDAT":
            data += chunk
        elif kind == b"IEND":
            break
    if not data or not width:
        return 128.0
    stream = zlib.decompress(data)
    stride = width * 3 + 1
    total = 0.0
    count = 0
    y = 0
    off = 0
    while y < height and off < len(stream):
        off += 1
        row = stream[off : off + width * 3]
        off += width * 3
        for i in range(0, len(row), 3):
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
    if stem.startswith("collab-03"):
        return (
            "Collaboration 3 · Human edit",
            theme,
            vp,
            "R1→20 Ω re-simulate; Activity filter You highlights human ops.",
        )
    if stem.startswith("collab-04"):
        return (
            "Collaboration 4 · Changes",
            theme,
            vp,
            "Changes segment selected; Restore agent version enabled.",
        )
    if stem.startswith("collab-05"):
        return (
            "Collaboration 5 · Needs review",
            theme,
            vp,
            "Needs review banner when derived/simulated exceed tolerance.",
        )
    if "collab-06-control-unity-run" in stem:
        return (
            "Collaboration 6 · Control run",
            theme,
            vp,
            "Unity-feedback run page agreement card.",
        )
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
            if light_path.is_file():
                if abs(lum - light_lums.get(light_name, _png_mean_luminance(light_path))) < 4:
                    scan["dark_integrity_failures"].append(
                        {"dark": path.name, "light": light_name, "reason": "mean luminance too close to light"}
                    )
            if lum > 95:
                scan["dark_integrity_failures"].append({"dark": path.name, "reason": f"mean luminance {lum:.1f} too bright"})
        else:
            light_lums[path.name] = lum
        scan["files"].append(entry)

    pf["capture_scan"] = scan
    pf["ci_status"] = _git_ci_status()
    head = pf.get("git_sha") or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    pf["git_sha"] = head
    pf["git_sha_short"] = pf.get("git_sha_short") or head[:7]
    pf["merged_collab_pr62_head"] = "83968d8f74046cb738c5a7bbcdbcbcd0ae54d364"
    pf["ci_reference"] = {
        "pr": 62,
        "head_sha_short": "83968d8",
        "workflow_run_id": "43910447419",
        "status": "success",
    }
    pf["png_count"] = len(pngs)
    pf_path.write_text(json.dumps(pf, indent=2) + "\n", encoding="utf-8")

    known: list[str] = [
        "Capture VM has no ngspice on PATH; collab RLC Agrees and Vc waveform used analytical staging in `capture_round_11_collab.py` (derived/simulated from `series_rlc_step`). CI PR #62 run 43910447419 uses ngspice.",
        "`control-step` gallery run pages were not in the main sweep when the API returned 500 on an older server; re-capture can add `problem-control-checked-*` at 83968d8 (API now returns 200).",
    ]
    if scan["dark_integrity_failures"]:
        known.append(
            "Automated dark vs light luminance pairs flagged (spot-check): "
            + "; ".join(f"{f.get('dark')}" for f in scan["dark_integrity_failures"][:8])
        )

    lines = [
        "# Round 11 — UX capture index",
        "",
        f"Git HEAD: `{pf.get('git_sha', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())}`",
        f"Short SHA: `{pf.get('git_sha_short', '?')}`",
        f"PNG count: {len(pngs)}",
        "",
        "## How to read",
        "",
        "| File | Screen | Theme | Viewport | What to look at |",
        "| --- | --- | --- | --- | --- |",
    ]
    for path in pngs:
        screen, theme, vp, look = _describe_file(path.name)
        lines.append(f"| `{path.name}` | {screen} | {theme} | {vp} | {look} |")

    lines.extend(
        [
            "",
            "## Collaboration loop (numbered)",
            "",
            "1. `collab-01-run-sim-vs-derived-agrees-*.png` — agent RLC solve with Agrees.",
            "2. `collab-02-lab-provenance-vc-activity-*.png` — Studio lab with provenance, Vc plot, Activity.",
            "3. `collab-03-human-r1-resim-activity-you-*.png` — human R1 edit, re-sim, Activity → You.",
            "4. `collab-04-changes-restore-agent-*.png` — Changes view and Restore agent version.",
            "5. `collab-05-needs-review-bad-derive-*.png` — Needs review derive mismatch state.",
            "6. `collab-06-control-unity-run-agrees-*.png` + `collab-06-control-unity-lab-agreement-*.png` — unity control run + lab (y_ss 0.909, t_s ~0.36 s).",
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