"""IEEE Std 80-2013 tolerable touch and step voltages (Eq. 32 / Eq. 35)."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record

_BODY_ID = {50: "IEEE80_BODY_50KG", 70: "IEEE80_BODY_70KG"}


def _resolve_body_id(*, body_mass_kg: int) -> str:
    if body_mass_kg not in _BODY_ID:
        raise ValueError("body_mass_kg must be 50 or 70")
    return _BODY_ID[body_mass_kg]


def tolerable_voltage(
    *,
    kind: str,
    body_mass_kg: int,
    rho_s_ohm_m: float,
    cs: float,
    t_s: float,
) -> dict:
    """One tolerable voltage; kind touch (Eq. 32) or step (Eq. 35)."""
    kind_l = str(kind).strip().lower()
    if kind_l not in ("touch", "step"):
        raise ValueError("kind must be 'touch' or 'step'")
    body_id = _resolve_body_id(body_mass_kg=body_mass_kg)
    rec = get_record(body_id)
    if rec is None:
        raise ValueError(f"unknown body constant id {body_id}")
    vals = rec["values"]
    k_touch = float(vals["k_touch"])
    k_step = float(vals["k_step"])
    if t_s <= 0:
        raise ValueError("t_s must be positive")
    denom = math.sqrt(t_s)
    if kind_l == "touch":
        factor = 1000.0 + 1.5 * cs * rho_s_ohm_m
        k = k_touch
        clause = "IEEE Std 80-2013 Eq. 32 (tolerable touch voltage)"
        equation = "(1000+1.5*Cs*rho_s)*k_touch/sqrt(t)"
    else:
        factor = 1000.0 + 6.0 * cs * rho_s_ohm_m
        k = k_step
        clause = "IEEE Std 80-2013 Eq. 35 (tolerable step voltage)"
        equation = "(1000+6*Cs*rho_s)*k_step/sqrt(t)"
    e_v = factor * k / denom
    inputs_used = {
        "kind": kind_l,
        "body_mass_kg": body_mass_kg,
        "rho_s_ohm_m": rho_s_ohm_m,
        "cs": cs,
        "t_s": t_s,
        "k": k,
    }
    return {
        "kind": kind_l,
        "body_mass_kg": body_mass_kg,
        "body_id": body_id,
        "e_v": e_v,
        "rho_s_ohm_m": rho_s_ohm_m,
        "cs": cs,
        "t_s": t_s,
        "k_used": k,
        "equation": equation,
        "standard_clause": clause,
        "inputs_used": inputs_used,
        "source_id": body_id,
    }


def tolerable_voltages(
    *,
    kind: str,
    body_mass_kg: int,
    rho_s_ohm_m: float,
    cs: float,
    t_s: float,
) -> dict:
    """Compute requested touch or step only (explicit kind and body mass required)."""
    return tolerable_voltage(
        kind=kind,
        body_mass_kg=body_mass_kg,
        rho_s_ohm_m=rho_s_ohm_m,
        cs=cs,
        t_s=t_s,
    )
