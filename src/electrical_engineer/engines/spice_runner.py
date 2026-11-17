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
    return shutil.which("ngspice") is not None


def simulator_status() -> dict[str, Any]:
    ng = shutil.which("ngspice")
    py = _pyspice_installed()
    if ng:
        return {
            "available": True,
            "backend": "ngspice",
            "reason": None,
            "pyspice": py,
        }
    if py:
        return {"available": False, "backend": None, "reason": "ngspice binary not on PATH"}
    return {"available": False, "backend": None, "reason": "ngspice not on PATH"}


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


def _ensure_control_block(
    cir: str,
    probe: str = "v(2)",
    *,
    analysis: str = "dc",
    f_hz: float | None = None,
    t_s: float | None = None,
    t_stop: float | None = None,
    derive_metric: str | None = None,
) -> str:
    if ".control" in cir.lower():
        return cir
    text = cir.rstrip()
    if text.lower().endswith(".end"):
        text = text[:-4].rstrip()
    low = text.lower()
    if analysis == "ac" and ".ac" not in low:
        f = float(f_hz or 1000.0)
        text += f"\n.ac lin 1 {f} {f}\n"
    if analysis == "tran" and ".tran" not in low:
        metric = str(derive_metric or "").lower()
        if metric in {"vc_peak", "peak", "max", "vc_final", "final"} and t_s is not None:
            if metric in {"vc_final", "final"}:
                stop = float(t_stop) if t_stop is not None else max(float(t_s) * 2.5, 0.015)
            else:
                stop = float(t_stop) if t_stop is not None else max(float(t_s) * 2.5, 1e-3)
            step = min(stop / 4000.0, 50e-6)
            m = re.search(r"v\((\d+)\)", probe)
            if m and ".ic" not in low:
                text += f"\n.ic v({m.group(1)})=0"
            text += f"\n.tran {step:g} {stop:g} uic\n"
        else:
            text += "\n.tran 1m 0.1\n"
    if analysis == "ac":
        probe_inner = probe
        if not probe.lower().startswith("mag("):
            probe_inner = f"mag({probe})"
        cmd = f"run\nprint {probe_inner}\n"
    elif analysis == "tran":
        metric = str(derive_metric or "").lower()
        if metric in {"vc_peak", "peak", "max"} or (
            metric in {"vc_final", "final"} and t_s is not None
        ):
            text += f"\n.measure tran _arc_out max {probe}\n"
            cmd = f"run\nprint all {probe}\nprint _arc_out\n"
        elif t_s is not None:
            text += f"\n.measure tran _arc_out find {probe} at={float(t_s)}\n"
            cmd = "run\nprint _arc_out\n"
        else:
            cmd = f"run\nprint {probe}\n"
    else:
        cmd = f"op\nprint {probe}\n"
    return f"{text}\n.control\n{cmd}.endc\n.end\n"


def _probe_node(problem: dict[str, Any], cir: str) -> str:
    node = problem.get("probe_node") or problem.get("v_node")
    if node:
        return f"v({node})"
    if re.search(r"\b2\b", cir):
        return "v(2)"
    return "v(1)"


def _parse_tran_series(stdout: str, probe: str) -> list[tuple[float, float]]:
    """Parse ngspice `print` tran tables as (time_s, probe_value) rows.

    `print all v(n)` prints every node vector, so the table header looks like
    ``Index time V(1) V(2) V(3)``. Column positions come from the header; the
    probe is not assumed to be the last column, nor time the second to last.
    """
    needle = probe.replace(" ", "").lower()
    rows: list[tuple[float, float]] = []
    t_col: int | None = None
    v_col: int | None = None
    for line in stdout.splitlines():
        parts = line.split()
        if not parts:
            continue
        lowered = [p.lower() for p in parts]
        if "time" in lowered and needle in lowered:
            t_col = lowered.index("time")
            v_col = lowered.index(needle)
            # Header with an Index column has data rows with one leading integer too.
            continue
        if t_col is None or v_col is None:
            continue
        if line.strip().startswith(("Note:", "---")):
            continue
        if len(parts) <= max(t_col, v_col):
            continue
        if lowered[0] != "index" and not parts[0].lstrip("-").isdigit() and t_col > 0:
            continue
        try:
            rows.append((float(parts[t_col]), float(parts[v_col])))
        except ValueError:
            continue
    seen: set[float] = set()
    unique: list[tuple[float, float]] = []
    for t, v in rows:
        if t in seen:
            continue
        seen.add(t)
        unique.append((t, v))
    return unique


def _refine_peak_time(series: list[tuple[float, float]], idx: int) -> float:
    """Peak time from a parabola through the sampled max and its neighbours.

    ngspice samples on its own time grid, so the raw argmax time is quantised to
    the step size; a three-point vertex fit recovers the time between samples.
    """
    t1, v1 = series[idx]
    if idx <= 0 or idx >= len(series) - 1:
        return t1
    t0, v0 = series[idx - 1]
    t2, v2 = series[idx + 1]
    denom = (t0 - t1) * (t0 - t2) * (t1 - t2)
    if denom == 0:
        return t1
    a = (t2 * (v1 - v0) + t1 * (v0 - v2) + t0 * (v2 - v1)) / denom
    b = (t2 * t2 * (v0 - v1) + t1 * t1 * (v2 - v0) + t0 * t0 * (v1 - v2)) / denom
    if a >= 0:
        return t1
    tv = -b / (2 * a)
    return tv if t0 <= tv <= t2 else t1


def _interp_crossing(
    t0: float, v0: float, t1: float, v1: float, *, target: float, rising: bool
) -> float:
    if abs(v1 - v0) <= 1e-18:
        return t1
    frac = (target - v0) / (v1 - v0)
    frac = max(0.0, min(1.0, frac))
    return t0 + frac * (t1 - t0)


def _settling_2pct_last_entry(
    rows: list[tuple[float, float]], target: float, *, frac: float = 0.02
) -> float | None:
    """Last time Vc enters the ±frac band of target (linear interpolation at boundary)."""
    if not rows or target == 0:
        return None
    tol = abs(target) * frac
    lo, hi = target - tol, target + tol
    entry: float | None = None
    dwell_s = max((rows[-1][0] - rows[0][0]) * 0.02, 1e-6)
    in_band_at: float | None = None
    for i, (t, v) in enumerate(rows):
        if lo <= v <= hi:
            if in_band_at is None:
                if i == 0:
                    in_band_at = t
                else:
                    t0, v0 = rows[i - 1]
                    if v0 < lo:
                        in_band_at = _interp_crossing(t0, v0, t, v, target=lo, rising=True)
                    elif v0 > hi:
                        in_band_at = _interp_crossing(t0, v0, t, v, target=hi, rising=False)
                    else:
                        in_band_at = t
            elif entry is None and t - in_band_at >= dwell_s:
                entry = in_band_at
        else:
            # Leaving the band voids any earlier entry: settling is the LAST entry.
            in_band_at = None
            entry = None
    return entry


def _interp_series_at_t(rows: list[tuple[float, float]], t_query: float) -> float | None:
    if not rows:
        return None
    if t_query <= rows[0][0]:
        return rows[0][1]
    for i in range(1, len(rows)):
        t0, v0 = rows[i - 1]
        t1, v1 = rows[i]
        if t_query <= t1:
            if abs(t1 - t0) <= 0.0:
                return v1
            frac = (t_query - t0) / (t1 - t0)
            return v0 + frac * (v1 - v0)
    t0, v0 = rows[-2] if len(rows) >= 2 else rows[-1]
    t1, v1 = rows[-1]
    if abs(t1 - t0) <= 0.0:
        return v1
    frac = (t_query - t0) / (t1 - t0)
    return v0 + frac * (v1 - v0)


def _parse_print_voltage(stdout: str, probe: str) -> float | None:
    needle = probe.replace(" ", "").lower()
    mag_needle = f"mag({needle})" if not needle.startswith("mag(") else needle
    for line in stdout.splitlines():
        low = line.lower().replace(" ", "")
        if "_arc_out" in low and "=" in line:
            rhs = line.split("=", 1)[-1].strip()
            try:
                return float(rhs.split()[0])
            except ValueError:
                continue
        if "=" in line and (needle in low or mag_needle.replace(" ", "") in low):
            rhs = line.split("=", 1)[-1].strip()
            try:
                return float(rhs.split()[0])
            except ValueError:
                continue
    last: float | None = None
    in_table = False
    for line in stdout.splitlines():
        compact = line.lower().replace(" ", "")
        if "time" in compact and (needle in compact or mag_needle in compact):
            in_table = True
            continue
        if mag_needle.replace("mag(", "").replace(")", "") in compact and "mag" in compact:
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
    f_hz = problem.get("f_hz")
    cir_body = cir.strip()
    if not cir_body.startswith("*"):
        cir_body = "* arc netlist\n" + cir_body
    t_s = problem.get("t_s")
    t_stop = problem.get("t_stop")
    derive_metric = problem.get("derive_metric")
    body = _ensure_control_block(
        cir_body,
        probe=probe,
        analysis=analysis,
        f_hz=float(f_hz) if f_hz else None,
        t_s=float(t_s) if t_s is not None else None,
        t_stop=float(t_stop) if t_stop is not None else None,
        derive_metric=str(derive_metric) if derive_metric else None,
    )
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
    derive_metric = str(problem.get("derive_metric") or "").lower()
    series: list[tuple[float, float]] = []
    t_peak_s: float | None = None
    settling_s: float | None = None
    if analysis == "tran" and derive_metric in {"vc_peak", "peak", "max", "vc_final", "final"}:
        value = _parse_print_voltage(combined, "_arc_out")
        series = _parse_tran_series(combined, probe)
        if value is None:
            if series:
                peak_idx = max(range(len(series)), key=lambda i: series[i][1])
                value = series[peak_idx][1]
                t_peak_s = _refine_peak_time(series, peak_idx)
            else:
                value = _parse_print_voltage(combined, probe)
        elif series:
            peak_idx = max(range(len(series)), key=lambda i: series[i][1])
            t_peak_s = _refine_peak_time(series, peak_idx)
        v_step = problem.get("v_step") or problem.get("vin")
        if series and v_step is not None:
            settling_s = _settling_2pct_last_entry(series, float(v_step))
    else:
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
    out: dict[str, Any] = {
        "ok": True,
        "tool": "ngspice",
        "unchecked": False,
        "value": value,
        "probe": probe,
        "paths": paths,
    }
    if t_peak_s is not None:
        out["t_peak_s"] = float(t_peak_s)
    if settling_s is not None:
        out["settling_2pct_entry_s"] = float(settling_s)
    if series:
        trace: dict[str, Any] = {
            "vc_trace_ms": [[t * 1000.0, v] for t, v in series],
            "t_Vc_peak_s": t_peak_s,
            "Vc_peak_V": value,
        }
        if settling_s is not None:
            trace["settling_2pct_entry_s"] = float(settling_s)
        out["trace"] = trace
    return out
