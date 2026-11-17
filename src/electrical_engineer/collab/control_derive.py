"""Hand-derived unity-feedback metrics for verify (not golden simulation)."""

from __future__ import annotations

import math
import re
from typing import Any


def _plant_first_order(problem: dict[str, Any]) -> tuple[float, float] | None:
    """Open-loop G(s) = K / (τ s + 1) from problem only."""
    if problem.get("num") is not None and problem.get("den") is not None:
        num = problem["num"]
        den = problem["den"]
        if isinstance(num, list) and isinstance(den, list) and len(num) == 1 and len(den) == 2:
            try:
                k = float(num[0])
                tau = float(den[0])
                if abs(float(den[1]) - 1.0) > 1e-9:
                    return None
                return k, tau
            except (TypeError, ValueError):
                return None
    tf = str(problem.get("tf") or "").replace(" ", "")
    m = re.match(r"^(\d+(?:\.\d+)?)/\(s\+(\d+(?:\.\d+)?)\)$", tf)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.match(r"^(\d+(?:\.\d+)?)/\(τs\+(\d+(?:\.\d+)?)\)$", tf, re.IGNORECASE)
    if m:
        return float(m.group(1)), float(m.group(2))
    if problem.get("k") is not None and problem.get("tau") is not None:
        return float(problem["k"]), float(problem["tau"])
    return None


def derive_unity_feedback(problem: dict[str, Any]) -> dict[str, Any] | None:
    """
    Unity negative feedback around G = K/(τs+1), H = 1.

    y(∞) = K/(K+1), 2% settling time of final: t_s = ln(50)/(K+1).
    """
    plant = _plant_first_order(problem)
    if plant is None:
        return None
    k, _tau = plant
    if k <= 0:
        return None
    y_ss = k / (k + 1.0)
    t_settle = math.log(50.0) / (k + 1.0)
    return {
        "y_ss": y_ss,
        "t_settle_s": t_settle,
        "value": y_ss,
        "unit": "",
        "engine": "hand_derivation",
        "kind": "unity_feedback",
    }


def derive_control_metrics(problem: dict[str, Any]) -> dict[str, Any] | None:
    kind = str(problem.get("kind") or "").lower()
    golden = str(problem.get("golden") or "")
    if kind == "unity_feedback" or golden == "unity_first_order" or _plant_first_order(problem):
        return derive_unity_feedback(problem)
    return None