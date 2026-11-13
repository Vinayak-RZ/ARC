"""Open-loop margin export with stable names (python-control wcp/wcg are swapped vs textbook)."""

from __future__ import annotations

import math
from typing import Any


def loop_margins(sys) -> dict[str, float]:
    """Map python-control margin() to textbook crossover names.

    python-control returns (gm, pm, wg, wp) where wg is phase crossover (phase=-180°)
    and wp is gain crossover (|L|=1). gm is a linear gain ratio, not dB.
    """
    import control

    gm_lin, pm, w_phase_crossover, w_gain_crossover = control.margin(sys)
    if gm_lin is None or math.isnan(float(gm_lin)):
        gm_db = float("nan")
    else:
        gm_db = 20.0 * math.log10(float(gm_lin))
    return {
        "gain_crossover_rad_s": float(w_gain_crossover),
        "phase_crossover_rad_s": float(w_phase_crossover),
        "phase_margin_deg": float(pm),
        "gain_margin_dB": gm_db,
        "gain_margin_linear": float(gm_lin),
    }


def margins_from_problem(problem: dict[str, Any]) -> dict[str, float]:
    from electrical_engineer.engines.control_runner import _tf_from_problem

    return loop_margins(_tf_from_problem(problem))
