"""Time-domain simulation and Visual Kit plot export."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.control_studio.compose import compose_closed_loop
from electrical_engineer.engines.control_runner import control_available


def _plot_path(base: Path, theme: str) -> Path:
    if theme == "dark":
        return base.with_name(f"{base.stem}_dark{base.suffix}")
    return base


def simulate(diagram: dict[str, Any], *, run_dir: Path | None = None, t_final: float = 10.0) -> dict[str, Any]:
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
    run_dir.mkdir(parents=True, exist_ok=True)
    step_png = run_dir / "studio_step.png"
    impulse_png = run_dir / "studio_impulse.png"
    t = __import__("numpy").linspace(0, t_final, 500)
    t_step, y_step = control.step_response(sys, T=t)
    t_imp, y_imp = control.impulse_response(sys, T=t)

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
            ax.set_ylabel("Output")
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
        "compose": meta,
    }
