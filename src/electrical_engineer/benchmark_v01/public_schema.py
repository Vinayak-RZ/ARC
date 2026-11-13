"""Neutral public answer_schema text (no verifier or product names)."""

from __future__ import annotations

from typing import Any


def neutral_grading_rule(fields: list[dict[str, Any]]) -> str:
    bits: list[str] = []
    for f in fields:
        name = f.get("name", "value")
        unit = f.get("unit") or "1"
        tol = f.get("tolerance", 1e-6)
        bits.append(f"{name} [{unit}] within ±{tol}")
    return "Numeric submission; " + "; ".join(bits)


def public_answer_schema(fields: list[dict[str, Any]], *, rule: str | None = None) -> dict[str, Any]:
    return {"fields": fields, "rule": rule or neutral_grading_rule(fields)}
