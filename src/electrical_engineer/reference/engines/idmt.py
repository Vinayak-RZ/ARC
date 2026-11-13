"""IDMT relay operating time from catalog curve ids (IEC 60255 / IEEE C37.112)."""

from __future__ import annotations

from electrical_engineer.reference.catalog import get_record


def _curve_record(curve_id: str) -> dict:
    rec = get_record(curve_id)
    if rec is None:
        raise ValueError(f"unknown curve id {curve_id}")
    return rec


def idmt_operating_time_s(
    curve_id: str,
    *,
    tms: float = 1.0,
    i_ratio: float,
) -> dict:
    """i_ratio = I / I_pickup (both same side of CT). Returns operating time in seconds."""
    if i_ratio <= 1.0:
        raise ValueError("i_ratio must be > 1 for definite minimum region")
    if tms <= 0:
        raise ValueError("tms must be positive")
    rec = _curve_record(curve_id)
    vals = rec["values"]
    std = str(vals.get("standard", "")).upper()
    if std == "IEC":
        k = float(vals["k"])
        alpha = float(vals["alpha"])
        t = (k * tms) / (i_ratio**alpha - 1.0)
    elif std == "IEEE":
        a = float(vals["A"])
        b = float(vals["B"])
        p = float(vals["p"])
        td = tms
        t = td * (a / (i_ratio**p - 1.0) + b)
    else:
        raise ValueError(f"unsupported curve standard for {curve_id}")
    return {
        "curve_id": curve_id,
        "tms": tms,
        "i_ratio": i_ratio,
        "time_s": t,
        "source_id": curve_id,
        "formula": vals.get("formula_note", std),
    }


def coordination_margin_s(t_upstream_s: float, t_downstream_s: float, *, ctibm_s: float = 0.3) -> dict:
    """Coordination check: upstream must be slower by CTI (norm from catalog CTI_NORM)."""
    margin = t_upstream_s - t_downstream_s
    return {
        "margin_s": margin,
        "cti_required_s": ctibm_s,
        "coordinated": margin >= ctibm_s,
    }
