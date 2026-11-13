"""Run lumped netlists via ngspice (CLI). PySpice import counts as installed for gates."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def _pyspice_installed() -> bool:
    try:
        import PySpice  # noqa: F401
    except ImportError:
        return False
    return True


def spice_available() -> bool:
    return shutil.which("ngspice") is not None and _pyspice_installed()


def simulator_status() -> dict[str, Any]:
    ng = shutil.which("ngspice")
    py = _pyspice_installed()
    if ng and py:
        return {"available": True, "backend": "ngspice", "reason": None}
    if ng and not py:
        return {"available": False, "backend": None, "reason": "PySpice not installed"}
    if py and not ng:
        return {"available": False, "backend": None, "reason": "ngspice binary not on PATH"}
    return {"available": False, "backend": None, "reason": "ngspice and PySpice unavailable"}


def _analysis_kind(cir: str, problem: dict[str, Any]) -> str:
    hint = str(problem.get("analysis") or "").lower()
    if hint in {"ac", "tran", "dc"}:
        return hint
    low = cir.lower()
    if ".ac" in low:
        return "ac"
    if ".tran" in low:
        return "tran"
    return "dc"


def _ensure_control_block(cir: str, probe: str = "v(2)", *, analysis: str = "dc") -> str:
    if ".control" in cir.lower():
        return cir
    text = cir.rstrip()
    if text.lower().endswith(".end"):
        text = text[:-4].rstrip()
    if analysis == "ac":
        cmd = f"run\nprint mag({probe})\n"
    else:
        cmd = f"run\nprint {probe}\n"
    return f"{text}\n.control\n{cmd}.endc\n.end\n"


def _probe_node(problem: dict[str, Any], cir: str) -> str:
    node = problem.get("probe_node") or problem.get("v_node")
    if node:
        return f"v({node})"
    if re.search(r"\b2\b", cir):
        return "v(2)"
    return "v(1)"


def _parse_print_voltage(stdout: str, probe: str) -> float | None:
    needle = probe.replace(" ", "").lower()
    mag_needle = f"mag({needle})" if not needle.startswith("mag(") else needle
    last: float | None = None
    in_table = False
    for line in stdout.splitlines():
        compact = line.lower().replace(" ", "")
        if "time" in compact and (needle in compact or mag_needle in compact):
            in_table = True
            continue
        if mag_needle in compact and "mag" in compact:
            in_table = True
            continue
        if in_table:
            if line.strip().startswith("Note:"):
                break
            parts = line.split()
            if len(parts) >= 2:
                try:
                    last = float(parts[-1])
                except ValueError:
                    continue
        else:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    last = float(parts[-1])
                except ValueError:
                    continue
    return last


def _write_wave_svg(run_dir: Path, value: float | None) -> str | None:
    if value is None:
        return None
    path = run_dir / "artifact.svg"
    text = (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='320' height='120'>"
        f"<rect width='100%' height='100%' fill='#f7f7f7'/>"
        f"<text x='16' y='40' font-family='Inter,sans-serif' font-size='14'>SPICE probe</text>"
        f"<text x='16' y='72' font-family='Inter,sans-serif' font-size='22' fill='#0052ff'>"
        f"{value:.6g} V</text></svg>"
    )
    path.write_text(text, encoding="utf-8")
    return str(path)


def run_spice_netlist(
    cir: str,
    run_dir: Path,
    problem: dict[str, Any],
) -> dict[str, Any]:
    probe = str(problem.get("probe") or _probe_node(problem, cir))
    analysis = _analysis_kind(cir, problem)
    body = _ensure_control_block(cir, probe=probe, analysis=analysis)
    net_path = run_dir / "netlist.cir"
    net_path.write_text(body, encoding="utf-8")
    if not spice_available():
        st = simulator_status()
        return {
            "ok": False,
            "error": st.get("reason") or "ngspice/PySpice not available",
            "unchecked": True,
            "tool": "ngspice",
            "simulator_skip": True,
        }
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / "run.cir"
        tmp_path.write_text(body, encoding="utf-8")
        try:
            proc = subprocess.run(
                ["ngspice", "-b", str(tmp_path)],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {
                "ok": False,
                "error": str(exc),
                "unchecked": True,
                "tool": "ngspice",
            }
    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    value = _parse_print_voltage(combined, probe)
    if value is None and proc.returncode != 0:
        return {
            "ok": False,
            "error": "ngspice failed",
            "detail": combined[-500:],
            "unchecked": True,
            "tool": "ngspice",
        }
    paths: list[str] = []
    svg = _write_wave_svg(run_dir, value)
    if svg:
        paths.append(svg)
    if value is None:
        return {
            "ok": False,
            "error": "no probe voltage parsed",
            "unchecked": True,
            "tool": "ngspice",
            "paths": paths,
        }
    return {
        "ok": True,
        "tool": "ngspice",
        "unchecked": False,
        "value": value,
        "probe": probe,
        "paths": paths,
    }
