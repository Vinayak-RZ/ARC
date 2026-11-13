"""IEEE Std 80-2013 tolerable touch and step voltages (Eq. 32 / step form)."""

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
    """Touch uses k_touch (Eq. 32 fibrillation path); step uses k_step (70 kg uses 0.313)."""
    rec = get_record(body_id)
    if rec is None:
        raise ValueError(f"unknown body constant id {body_id}")
    vals = rec["values"]
    k_touch = float(vals["k_touch"])
    k_step = float(vals["k_step"])
    if t_s <= 0:
        raise ValueError("t_s must be positive")
    factor = 1000.0 + 1.5 * cs * rho_s_ohm_m
    denom = math.sqrt(t_s)
    e_touch = factor * k_touch / denom
    e_step = factor * k_step / denom
    return {
        "body_id": body_id,
        "e_touch_v": e_touch,
        "e_step_v": e_step,
        "rho_s_ohm_m": rho_s_ohm_m,
        "cs": cs,
        "t_s": t_s,
        "k_touch": k_touch,
        "k_step": k_step,
        "equation_touch": "IEEE 80 Eq. 32 style: (1000+1.5*Cs*rho_s)*k_touch/sqrt(t)",
        "equation_step": "(1000+1.5*Cs*rho_s)*k_step/sqrt(t)",
        "source_id": body_id,
    }
