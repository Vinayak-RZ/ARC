"""Neutral public answer_schema text (no verifier or product names)."""

from __future__ import annotations

from typing import Any

DEFAULT_REL_TOL = 0.005
DEFAULT_ABS_FLOOR = 1e-4


def field_tolerance(absolute: float | None = None) -> dict[str, float]:
    return {
        "tolerance_rel": DEFAULT_REL_TOL,
        "tolerance_abs": max(DEFAULT_ABS_FLOOR, float(absolute or DEFAULT_ABS_FLOOR)),
    }


def neutral_grading_rule(fields: list[dict[str, Any]]) -> str:
    bits: list[str] = []
    for f in fields:
        name = f.get("name", "value")
        unit = f.get("unit") or "1"
        rel = float(f.get("tolerance_rel", DEFAULT_REL_TOL))
        ab = float(f.get("tolerance_abs", DEFAULT_ABS_FLOOR))
        bits.append(f"{name} [{unit}] within ±{rel*100:.2g}% or ±{ab:g}")
    return "Numeric submission (match givens precision); " + "; ".join(bits)


def public_answer_schema(fields: list[dict[str, Any]], *, rule: str | None = None) -> dict[str, Any]:
    norm = []
    for f in fields:
        row = dict(f)
        if "tolerance_rel" not in row and row.get("name") != "cases":
            row.update(field_tolerance(row.get("tolerance")))
        norm.append(row)
    return {"fields": norm, "rule": rule or neutral_grading_rule(norm)}


def values_close(a: float, b: float, field: dict[str, Any]) -> bool:
    rel = float(field.get("tolerance_rel", DEFAULT_REL_TOL))
    ab = float(field.get("tolerance_abs", DEFAULT_ABS_FLOOR))
    scale = max(ab, rel * max(abs(a), abs(b), 1.0))
    return abs(float(a) - float(b)) <= scale
