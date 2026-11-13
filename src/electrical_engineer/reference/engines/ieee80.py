"""IEEE 80 tolerable touch and step voltages (simplified body-weight constants)."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record


def tolerable_voltages(
    *,
    body_id: str = "IEEE80_BODY_50KG",
    rho_s_ohm_m: float = 100.0,
    cs: float = 1.0,
    t_s: float = 1.0,
) -> dict:
    rec = get_record(body_id)
    if rec is None:
        raise ValueError(f"unknown body constant id {body_id}")
    k = float(rec["values"]["k_factor"])
    if t_s <= 0:
        raise ValueError("t_s must be positive")
    base = (1000.0 + 1.5 * cs * rho_s_ohm_m) * k / math.sqrt(t_s)
    return {
        "body_id": body_id,
        "e_step_v": base,
        "e_touch_v": base,
        "rho_s_ohm_m": rho_s_ohm_m,
        "cs": cs,
        "t_s": t_s,
        "source_id": body_id,
        "note": "touch and step use same simplified limit in this engine",
    }
