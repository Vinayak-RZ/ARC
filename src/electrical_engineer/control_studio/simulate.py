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


def _auto_t_final(margins: dict[str, Any] | None) -> float:
    wcg = (margins or {}).get("gain_crossover_rad_s")
    if wcg and math.isfinite(float(wcg)) and float(wcg) > 0:
        return float(min(600.0, max(10.0, 6.0 / float(wcg))))
    return 10.0


def _step_metrics(t, y, setpoint: float, window_s: float) -> dict[str, Any]:
    import numpy as np

    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(y) < 2:
        return {"settled": False, "window_s": window_s, "rising_at_end": float(y[-1]) if len(y) else None}
    tail_n = max(3, int(len(y) * 0.1))
    band = 0.02 * abs(setpoint or 1.0)
    tail = y[-tail_n:]
    settled = bool(np.all(np.abs(tail - setpoint) <= band))
    metrics: dict[str, Any] = {
        "settled": settled,
        "window_s": window_s,
        "final_value": float(y[-1]),
        "setpoint": setpoint,
    }
    if not settled:
        metrics["rising_at_end"] = float(y[-1])
        metrics["aria_summary"] = (
            f"Closed-loop step response, not settled within {window_s:.0f} s, "
            f"still at {y[-1]:.3g} toward setpoint {setpoint:g}"
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

    if t_final == "auto" or t_final is None:
        t_final = _auto_t_final(margins)
    t_final = float(t_final)

    sys, meta = compose_closed_loop(diagram)
    run_dir = run_dir or Path("runs") / "_control_studio_scratch"
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
