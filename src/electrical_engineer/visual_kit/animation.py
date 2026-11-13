"""Short engine-driven animations for Visual Kit."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from electrical_engineer.engines.smib_swing import SmibCase, simulate_clearing
from electrical_engineer.visual_kit.design_tokens import get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme


def render_swing_fault_animation(out_dir: Path) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    case = SmibCase()
    theme = get_theme("light")
    cleared = simulate_clearing(case, 0.15, 0.005, 1.5, "rk4")
    uncleared = simulate_clearing(case, 0.32, 0.005, 1.5, "rk4")
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h * 0.85))
    apply_theme(ax, theme)
    (line1,) = ax.plot([], [], color=theme.primary, linewidth=2, label="Cleared 0.15 s")
    (line2,) = ax.plot([], [], color=theme.fault, linewidth=1.6, linestyle="--", label="Uncleared 0.32 s")
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, math.degrees(math.pi) * 1.05)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"$\delta$ (deg)")
    ax.set_title("Rotor angle after fault clearing")
    ax.legend(loc="upper right", fontsize=8, frameon=True, facecolor=theme.surface)

    t1 = [p[0] for p in cleared["trail"]]
    d1 = [math.degrees(p[1]) for p in cleared["trail"]]
    t2 = [p[0] for p in uncleared["trail"]]
    d2 = [math.degrees(p[1]) for p in uncleared["trail"]]
    n = max(len(t1), len(t2))

    def update(frame: int):
        i = min(frame, len(t1) - 1)
        j = min(frame, len(t2) - 1)
        line1.set_data(t1[: i + 1], d1[: i + 1])
        line2.set_data(t2[: j + 1], d2[: j + 1])
        return line1, line2

    out_dir.mkdir(parents=True, exist_ok=True)
    gif = out_dir / "power.swing_animation.gif"
    anim = FuncAnimation(fig, update, frames=n, interval=40, blit=True)
    try:
        anim.save(gif, writer=matplotlib.animation.PillowWriter(fps=25))
    except (OSError, RuntimeError, ValueError):
        plt.close(fig)
        return {"gif": None, "meta": {"component_id": "power.swing_animation", "error": "pillow writer missing"}}
    plt.close(fig)
    return {"gif": str(gif), "meta": {"component_id": "power.swing_animation", "frames": n}}
