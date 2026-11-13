"""IEEE Std 80-2013 tolerable touch and step voltages (clause 8.4, Eq. 29–33)."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record

_BODY_ID = {50: "IEEE80_BODY_50KG", 70: "IEEE80_BODY_70KG"}

# Touch Eq. 29–30; step Eq. 32–33 (IEEE Std 80-2013 clause 8.4).
_CLAUSE: dict[tuple[str, int], tuple[str, str]] = {
    ("touch", 50): (
        "IEEE Std 80-2013 Eq. 29 (tolerable touch voltage, 50 kg)",
        "(1000+1.5*Cs*rho_s)*k/sqrt(t)",
    ),
    ("touch", 70): (
        "IEEE Std 80-2013 Eq. 30 (tolerable touch voltage, 70 kg)",
        "(1000+1.5*Cs*rho_s)*k/sqrt(t)",
    ),
    ("step", 50): (
        "IEEE Std 80-2013 Eq. 32 (tolerable step voltage, 50 kg)",
        "(1000+6*Cs*rho_s)*k/sqrt(t)",
    ),
    ("step", 70): (
        "IEEE Std 80-2013 Eq. 33 (tolerable step voltage, 70 kg)",
        "(1000+6*Cs*rho_s)*k/sqrt(t)",
    ),
}

_CLAUSE_CITATIONS = (
    "IEEE Std 80-2013 clause 8.4 (Eq. 29–33); "
    "secondary: ieccalc.com/standards/ieee-80, windfarmbop.com IEEE 80 worked example"
)


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
    """One tolerable voltage; k depends on body mass only (0.116 kg50, 0.157 kg70)."""
    kind_l = str(kind).strip().lower()
    if kind_l not in ("touch", "step"):
        raise ValueError("kind must be 'touch' or 'step'")
    body_id = _resolve_body_id(body_mass_kg=body_mass_kg)
    rec = get_record(body_id)
    if rec is None:
        raise ValueError(f"unknown body constant id {body_id}")
    vals = rec["values"]
    k = float(vals["k"])
    if t_s <= 0:
        raise ValueError("t_s must be positive")
    clause, equation = _CLAUSE[(kind_l, body_mass_kg)]
    rs_coeff = 1.5 if kind_l == "touch" else 6.0
    factor = 1000.0 + rs_coeff * cs * rho_s_ohm_m
    e_v = factor * k / math.sqrt(t_s)
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
        "standard_clause_citations": _CLAUSE_CITATIONS,
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
