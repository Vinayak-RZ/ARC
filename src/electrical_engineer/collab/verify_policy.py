"""Lab verify tolerance (single policy for derive vs simulate)."""

from __future__ import annotations

DEFAULT_REL_TOL = 0.02  # 2% relative on |derived|

DOCS = (
    "Arc compares |derived − simulated| / max(|derived|, ε) to a fixed relative limit "
    f"(default {DEFAULT_REL_TOL * 100:.0f}%). Difference column shows the measured relative error; "
    "status badges state Agrees or Differs against that same limit."
)


def status_label(*, agrees: bool, rel_err_pct: float, limit_pct: float = DEFAULT_REL_TOL * 100) -> str:
    if agrees:
        return f"Agrees (limit {limit_pct:.0f}%)"
    return f"Differs by {rel_err_pct:.1f}% (limit {limit_pct:.0f}%)"


def format_rel_err_pct(rel_err_pct: float) -> float:
    """Round for display without hiding small nonzero errors."""
    if rel_err_pct < 0.05:
        return rel_err_pct
    return round(rel_err_pct, 1)