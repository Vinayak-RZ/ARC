"""IEEE 519 TDD limit lookup by I_SC / I_L ratio."""

from __future__ import annotations

from electrical_engineer.reference.catalog import get_record


def tdd_limit_percent(*, ratio_id: str | None = None, isc_il_ratio: float | None = None) -> dict:
    if ratio_id:
        rec = get_record(ratio_id)
        if rec is None:
            raise ValueError(f"unknown ratio band id {ratio_id}")
        return {
            "ratio_id": ratio_id,
            "tdd_limit_percent": float(rec["values"]["tdd_percent"]),
            "isc_il_min": rec["values"].get("isc_il_min"),
            "isc_il_max": rec["values"].get("isc_il_max"),
            "source_id": ratio_id,
        }
    if isc_il_ratio is None or isc_il_ratio <= 0:
        raise ValueError("provide ratio_id or positive isc_il_ratio")
    from electrical_engineer.reference.catalog import load_catalog

    for rid in sorted(load_catalog()):
        if not rid.startswith("IEEE519_TDD"):
            continue
        rec = get_record(rid)
        if not rec:
            continue
        lo = rec["values"].get("isc_il_min")
        hi = rec["values"].get("isc_il_max")
        lo_f = float(lo) if lo is not None else 0.0
        hi_f = float(hi) if hi is not None else float("inf")
        if lo_f <= isc_il_ratio < hi_f:
            return tdd_limit_percent(ratio_id=rid)
    raise ValueError("isc_il_ratio out of tabulated bands")


def tdd_compliance(*, isc_il_ratio: float, measured_tdd_percent: float) -> dict:
    """Compare measured TDD against IEEE 519-2022 Table 2 limits by Isc/IL ratio."""
    limit = tdd_limit_percent(isc_il_ratio=isc_il_ratio)
    compliant = measured_tdd_percent <= float(limit["tdd_limit_percent"])
    return {
        "edition_label": "IEEE Std 519-2022 Table 2 (TDD limits)",
        "isc_il_ratio": isc_il_ratio,
        "measured_tdd_percent": measured_tdd_percent,
        "limit_tdd_percent": limit["tdd_limit_percent"],
        "ratio_band_id": limit["ratio_id"],
        "compliant": compliant,
        "margin_percent": float(limit["tdd_limit_percent"]) - measured_tdd_percent,
        "source_id": limit["ratio_id"],
    }
