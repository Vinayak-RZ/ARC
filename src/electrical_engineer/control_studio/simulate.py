"""Time-domain simulation and Visual Kit plot export."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from electrical_engineer.control_studio.compose import compose_closed_loop
from electrical_engineer.engines.control_runner import control_available


def _plot_path(base: Path, theme: str) -> Path:
    if theme == "dark":
        return base.with_name(f"{base.stem}_dark{base.suffix}")
    return base


def _output_unit(diagram: dict[str, Any]) -> str:
    for b in diagram.get("blocks") or []:
        if b.get("type") == "plant_dc_motor":
            return "rad/s"
    return ""


def _round_window_nice(x: float) -> float:
    """Round up to 1, 2, or 5 × 10^n for Auto simulation windows."""
    if not math.isfinite(x) or x <= 0:
        return 10.0
    exp = math.floor(math.log10(x))
    mag = 10.0**exp
    norm = x / mag
    step = 1.0 if norm <= 1.0 else 2.0 if norm <= 2.0 else 5.0 if norm <= 5.0 else 10.0
    out = step * mag
    if out < x - 1e-12:
        if step == 1.0:
            step = 2.0
        elif step == 2.0:
            step = 5.0
        elif step == 5.0:
            step = 10.0
        else:
            step = 10.0
            mag *= 10.0
        out = step * mag
    return float(min(600.0, max(2.0, out)))


def _auto_t_final(margins: dict[str, Any] | None, *, t_settle: float | None = None) -> float:
    if t_settle is not None and math.isfinite(t_settle) and t_settle > 0:
        return _round_window_nice(8.0 * t_settle)
    wcg = (margins or {}).get("gain_crossover_rad_s")
    if wcg and math.isfinite(float(wcg)) and float(wcg) > 0:
        return _round_window_nice(max(10.0, 6.0 / float(wcg)))
    return 10.0


def _interpolate_settle_time(t, y, settle_idx: int, y_ss: float, band: float) -> float:
    """Linear crossing time when the response last enters the ±2% band."""
    if settle_idx >= len(y) - 1:
        return float(t[settle_idx])
    ti = float(t[settle_idx])
    tj = float(t[settle_idx + 1])
    yi = float(y[settle_idx])
    yj = float(y[settle_idx + 1])
    ai = abs(yi - y_ss)
    aj = abs(yj - y_ss)
    if ai <= band:
        return ti
    if aj > band:
        return ti
    if abs(ai - aj) < 1e-15:
        return ti
    frac = (ai - band) / (ai - aj)
    frac = max(0.0, min(1.0, frac))
    return ti + frac * (tj - ti)


def _step_metrics(t, y, setpoint: float, window_s: float) -> dict[str, Any]:
    import numpy as np

    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    sp = abs(setpoint or 1.0)
    if len(y) < 2:
        return {
            "status": "not_settled",
            "settled": False,
            "window_s": window_s,
            "value_at_end": float(y[-1]) if len(y) else None,
            "setpoint": setpoint,
        }
    # Flatness first: a response that has stopped moving has a final value y_ss.
    tail_n = max(3, int(len(y) * 0.1))
    tail = y[-tail_n:]
    y_ss = float(tail.mean())
    flat = float(tail.max() - tail.min()) <= 0.01 * max(abs(y_ss), 1e-9)
    # Textbook definitions (Ogata, Nise, Franklin and Powell): settling time and percent
    # overshoot are measured against the FINAL value, not the setpoint. The setpoint only
    # enters through the steady-state error e_ss = (setpoint - y_ss) / setpoint.
    sse_pct = abs(setpoint - y_ss) / sp * 100.0
    on_target = sse_pct <= 2.0
    if not flat:
        status = "not_settled"
    elif on_target:
        status = "settled"
    else:
        status = "settled_off_target"
    metrics: dict[str, Any] = {
        "status": status,
        "settled": status == "settled",
        "window_s": window_s,
        "final_value": y_ss if flat else float(y[-1]),
        "value_at_end": float(y[-1]),
        "setpoint": setpoint,
        "steady_state_error_pct": round(sse_pct, 1) if flat else None,
        "on_target": on_target if flat else None,
        "t_settle_s": None,
        "overshoot_pct": None,
        "band_pct": 2.0 if flat else None,
    }
    if flat:
        band = 0.02 * max(abs(y_ss), 1e-9)
        settle_idx = 0
        for i in range(len(y) - 1, -1, -1):
            if abs(float(y[i]) - y_ss) > band:
                settle_idx = i
                break
        peak = float(np.max(y)) if y_ss >= 0 else float(np.min(y))
        over = (peak - y_ss) / abs(y_ss) * 100.0 if y_ss >= 0 else (y_ss - peak) / abs(y_ss) * 100.0
        peak_idx = int(np.argmax(y)) if y_ss >= 0 else int(np.argmin(y))
        metrics["t_settle_s"] = _interpolate_settle_time(t, y, settle_idx, y_ss, band)
        metrics["overshoot_pct"] = round(max(0.0, over), 2)
        metrics["peak_t_s"] = float(t[peak_idx])
        metrics["peak_value"] = peak
    if status == "not_settled":
        slope = float((y[-1] - y[-tail_n]) / max(float(t[-1] - t[-tail_n]), 1e-9))
        metrics["tail_slope"] = slope
        metrics["aria_summary"] = (
            f"Closed-loop step response, not settled within {window_s:.0f} s, "
            f"at {y[-1]:.3g} toward setpoint {setpoint:g}"
        )
    elif status == "settled_off_target":
        direction = "below" if y_ss < setpoint else "above"
        metrics["direction"] = direction
        metrics["aria_summary"] = (
            f"Step response settles in {metrics['t_settle_s']:.2g} s at a final value of {y_ss:.3g}, "
            f"{sse_pct:.1f}% {direction} setpoint"
        )
    else:
        metrics["aria_summary"] = (
            f"Closed-loop step response settled in {metrics['t_settle_s']:.2g} s "
            f"at {y_ss:.3g} within {window_s:.0f} s"
        )
    return metrics


def simulate(
    diagram: dict[str, Any],
    *,
    run_dir: Path | None = None,
    t_final: float | str = 10.0,
    margins: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not control_available():
        return {"ok": False, "error": "python-control missing", "unchecked": True}
    import control
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from electrical_engineer.visual_kit.design_tokens import get_theme
    from electrical_engineer.visual_kit.mpl_theme import apply_theme

    sys, meta = compose_closed_loop(diagram)
    run_dir = run_dir or Path("runs") / "_control_studio_scratch"
    if t_final == "auto" or t_final is None:
        import numpy as np

        t_probe = np.linspace(0, 10.0, 500)
        t_p, y_p = control.step_response(sys, T=t_probe)
        probe = _step_metrics(t_p, y_p, 1.0, 10.0)
        t_final = _auto_t_final(margins, t_settle=probe.get("t_settle_s"))
    t_final = float(t_final)
    run_dir.mkdir(parents=True, exist_ok=True)
    step_png = run_dir / "studio_step.png"
    impulse_png = run_dir / "studio_impulse.png"
    t = __import__("numpy").linspace(0, t_final, max(500, int(t_final * 50)))
    t_step, y_step = control.step_response(sys, T=t)
    t_imp, y_imp = control.impulse_response(sys, T=t)

    setpoint = 1.0
    unit = _output_unit(diagram)
    metrics = _step_metrics(t_step, y_step, setpoint, t_final)
    step_series = {
        "t": [float(x) for x in t_step],
        "y": [float(x) for x in y_step],
        "setpoint": setpoint,
        "unit": unit,
        "metrics": metrics,
    }

    for theme_name in ("light", "dark"):
        theme = get_theme(theme_name)
        for base, tt, yy, title in (
            (step_png, t_step, y_step, "Closed-loop step response"),
            (impulse_png, t_imp, y_imp, "Impulse response"),
        ):
            path = _plot_path(base, theme_name)
            _, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h))
            apply_theme(ax, theme)
            ax.plot(tt, yy, color=theme.primary, linewidth=1.5)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Output" + (f" ({unit})" if unit else ""))
            ax.set_title(title)
            fig = ax.figure
            fig.patch.set_facecolor(theme.canvas)
            plt.tight_layout()
            plt.savefig(path, dpi=theme.dpi, facecolor=theme.canvas)
            plt.close()

    y_ss = float(y_step[-1]) if len(y_step) else None
    return {
        "ok": True,
        "unchecked": False,
        "tool": "python-control",
        "step_png": str(step_png),
        "impulse_png": str(impulse_png),
        "y_ss": y_ss,
        "step_series": step_series,
        "compose": meta,
    }
