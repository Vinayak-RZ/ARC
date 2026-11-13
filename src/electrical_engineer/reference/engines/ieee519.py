"""IEEE 519 TDD limit lookup by I_SC / I_L ratio."""

from __future__ import annotations

from electrical_engineer.reference.catalog import get_record, load_catalog

# IEEE Std 519-2022 Table 2 band order (stiff → weak supply).
_TDD_BAND_IDS = (
    "IEEE519_TDD_BAND_LT20",
    "IEEE519_TDD_BAND_20_50",
    "IEEE519_TDD_BAND_50_100",
    "IEEE519_TDD_BAND_100_1000",
    "IEEE519_TDD_BAND_GT1000",
)

# Table 2 rows are Isc/IL <20, 20–50, 50–100, 100–1000, >1000 (519-2022 Table 2).
# Lookup uses half-open [lo, hi): interior breakpoints 20, 50, 100, 1000 map to the
# next row (e.g. ratio 20 -> 8% band, ratio 1000 -> >1000 / 20% band).
BOUNDARY_POLICY = "half_open_lo_inclusive_hi_exclusive"
BOUNDARY_POLICY_CITATION = (
    "IEEE Std 519-2022 Table 2 (120 V–69 kV TDD limits); "
    "interval endpoints assigned to weaker-supply row per half-open [lo, hi) lookup"
)


def _band_row_label(rec: dict) -> str:
    src = rec.get("source") or {}
    clause = src.get("clause") or rec.get("id")
    vals = rec.get("values") or {}
    lo = vals.get("isc_il_min")
    hi = vals.get("isc_il_max")
    if hi is None:
        return f"IEEE 519-2022 Table 2: Isc/IL > {lo} ({clause})"
    return f"IEEE 519-2022 Table 2: {lo} <= Isc/IL < {hi} ({clause})"


def tdd_limit_percent(*, ratio_id: str | None = None, isc_il_ratio: float | None = None) -> dict:
    if ratio_id:
        rec = get_record(ratio_id)
        if rec is None:
            raise ValueError(f"unknown ratio band id {ratio_id}")
        raw = load_catalog()[ratio_id]
        return {
            "ratio_id": ratio_id,
            "tdd_limit_percent": float(rec["values"]["tdd_percent"]),
            "isc_il_min": rec["values"].get("isc_il_min"),
            "isc_il_max": rec["values"].get("isc_il_max"),
            "table_row_label": _band_row_label(raw),
            "standard_clause": "IEEE Std 519-2022 Table 2",
            "boundary_policy": BOUNDARY_POLICY,
            "boundary_policy_citation": BOUNDARY_POLICY_CITATION,
            "inputs_used": {"isc_il_ratio": None, "ratio_id": ratio_id},
            "source_id": ratio_id,
        }
    if isc_il_ratio is None or isc_il_ratio <= 0:
        raise ValueError("provide ratio_id or positive isc_il_ratio")
    for rid in _TDD_BAND_IDS:
        rec = load_catalog()[rid]
        lo = rec["values"].get("isc_il_min")
        hi = rec["values"].get("isc_il_max")
        lo_f = float(lo) if lo is not None else 0.0
        hi_f = float(hi) if hi is not None else float("inf")
        if lo_f <= isc_il_ratio < hi_f:
            out = tdd_limit_percent(ratio_id=rid)
            out["inputs_used"] = {"isc_il_ratio": isc_il_ratio, "ratio_id": rid}
            return out
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
        "table_row_label": limit["table_row_label"],
        "standard_clause": limit["standard_clause"],
        "boundary_policy": limit["boundary_policy"],
        "boundary_policy_citation": limit["boundary_policy_citation"],
        "inputs_used": {
            "isc_il_ratio": isc_il_ratio,
            "measured_tdd_percent": measured_tdd_percent,
        },
        "compliant": compliant,
        "margin_percent": float(limit["tdd_limit_percent"]) - measured_tdd_percent,
        "source_id": limit["ratio_id"],
    }
