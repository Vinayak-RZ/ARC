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


def _auto_t_final(margins: dict[str, Any] | None, *, t_settle: float | None = None) -> float:
    if t_settle is not None and math.isfinite(t_settle) and t_settle > 0:
        return float(min(600.0, max(2.0, 8.0 * t_settle)))
    wcg = (margins or {}).get("gain_crossover_rad_s")
    if wcg and math.isfinite(float(wcg)) and float(wcg) > 0:
        return float(min(600.0, max(10.0, 6.0 / float(wcg))))
    return 10.0


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
    band = 0.02 * sp
    settle_idx = len(y) - 1
    for i in range(len(y) - 1, -1, -1):
        if abs(float(y[i]) - setpoint) > band:
            settle_idx = i
            break
    t_settle = float(t[settle_idx]) if settle_idx < len(t) else float(t[-1])
    peak = float(np.max(y)) if len(y) else setpoint
    overshoot_pct = max(0.0, (peak - setpoint) / sp * 100.0) if sp > 0 else None
    tail_n = max(3, int(len(y) * 0.1))
    tail = y[-tail_n:]
    flat = float(tail.max() - tail.min()) <= 0.01 * max(abs(float(tail.mean())), 1e-9)
    sse = abs(setpoint - float(y[-1])) / sp
    if not flat:
        status = "not_settled"
    elif sse <= 0.02:
        status = "settled"
    else:
        status = "settled_off_target"
    metrics: dict[str, Any] = {
        "status": status,
        "settled": status == "settled",
        "window_s": window_s,
        "final_value": float(y[-1]),
        "value_at_end": float(y[-1]),
        "setpoint": setpoint,
        "steady_state_error_pct": round(sse * 100.0, 1) if status == "settled_off_target" else None,
        "t_settle_s": t_settle if status == "settled" else None,
        "overshoot_pct": round(overshoot_pct, 2) if status == "settled" and overshoot_pct is not None else None,
    }
    if status == "not_settled":
        slope = float((y[-1] - y[-tail_n]) / max(float(t[-1] - t[-tail_n]), 1e-9))
        metrics["tail_slope"] = slope
        metrics["aria_summary"] = (
            f"Closed-loop step response, not settled within {window_s:.0f} s, "
            f"at {y[-1]:.3g} toward setpoint {setpoint:g}"
        )
    elif status == "settled_off_target":
        pct = metrics["steady_state_error_pct"]
        direction = "below" if float(y[-1]) < setpoint else "above"
        y_end = float(y[-1])
        metrics["aria_summary"] = (
            f"Step response settles at {y_end:.3g}, {pct:.1f}% {direction} setpoint"
        )
    else:
        metrics["aria_summary"] = f"Closed-loop step response settled near {setpoint:g} within {window_s:.0f} s"
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
