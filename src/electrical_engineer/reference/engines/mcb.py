"""IEC 60898 MCB magnetic trip band check."""

from __future__ import annotations

from electrical_engineer.reference.catalog import get_record


def magnetic_trip_in_band(*, mcb_type_id: str, i_a: float, rated_in_a: float) -> dict:
    rec = get_record(mcb_type_id)
    if rec is None:
        raise ValueError(f"unknown mcb type {mcb_type_id}")
    band_lo = float(rec["values"]["magnetic_multiple_min"])
    band_hi = float(rec["values"]["magnetic_multiple_max"])
    lo_a = band_lo * rated_in_a
    hi_a = band_hi * rated_in_a
    tripping = lo_a <= i_a <= hi_a
    return {
        "mcb_type_id": mcb_type_id,
        "i_a": i_a,
        "rated_in_a": rated_in_a,
        "magnetic_trip_lower_multiple": band_lo,
        "magnetic_trip_upper_multiple": band_hi,
        "magnetic_trip_lower_in_a": lo_a,
        "magnetic_trip_upper_in_a": hi_a,
        "band_multiple": [band_lo, band_hi],
        "band_a": [lo_a, hi_a],
        "in_magnetic_band": tripping,
        "source_id": mcb_type_id,
    }
