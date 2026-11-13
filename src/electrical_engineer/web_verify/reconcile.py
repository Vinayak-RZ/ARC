"""Compare library, solver, and web-sourced values."""

from __future__ import annotations

import math
from typing import Any


def _as_float(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip().replace(",", ""))
        except ValueError:
            return None
    return None


def reconcile_claim(claim: dict[str, Any]) -> dict[str, Any]:
    tol = float(claim.get("tolerance") or 0.05)
    lib = _as_float(claim.get("library_value"))
    sol = _as_float(claim.get("solver_value"))
    web = _as_float(claim.get("web_value"))
    status = claim.get("status") or "verified"
    disagreement: dict[str, Any] = {}

    def rel_diff(a: float, b: float) -> float:
        denom = max(abs(a), abs(b), 1e-12)
        return abs(a - b) / denom

    lib_raw = claim.get("library_value")
    web_raw = claim.get("web_value")
    if lib is None and web is None and lib_raw is not None and web_raw is not None:
        if str(lib_raw).strip().lower() != str(web_raw).strip().lower():
            status = "mismatch_library"
            disagreement["library_vs_web"] = {"library": lib_raw, "web": web_raw}
    if web is not None and lib is not None and rel_diff(web, lib) > tol:
        status = "mismatch_library"
        disagreement["library_vs_web"] = {"library": lib, "web": web}
    if web is not None and sol is not None and rel_diff(web, sol) > tol:
        if status == "verified":
            status = "mismatch_solver"
        disagreement["solver_vs_web"] = {"solver": sol, "web": web}
    if status not in ("verified", "pass"):
        status = "needs_review"
    out = {**claim, "status": status}
    if disagreement:
        out["disagreement"] = disagreement
    return out


def reconcile_similar_match(match: dict[str, Any], *, arc_result: Any) -> dict[str, Any]:
    m = dict(match)
    if m.get("agrees_after_adjustment") is False:
        m["status"] = "needs_review"
    return m


def overall_status(
    claims: list[dict[str, Any]], similar: list[dict[str, Any]], provider_status: str
) -> str:
    if provider_status in ("pending_host", "unsupported"):
        return provider_status
    if any(c.get("status") == "needs_review" for c in claims):
        return "needs_review"
    if any(s.get("status") == "needs_review" or s.get("agrees_after_adjustment") is False for s in similar):
        return "needs_review"
    if provider_status == "offline":
        return "offline_pass"
    return "pass"
