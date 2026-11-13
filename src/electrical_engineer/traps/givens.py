"""Extract problem givens from a solution trace for engine-backed checks."""

from __future__ import annotations

from typing import Any

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase
from electrical_engineer.engines.ed_lambda import EdCase, EdUnit
from electrical_engineer.engines.smib_swing import SmibCase
from electrical_engineer.traps.schema import SolutionTrace

_SMIB_KEYS = (
    "h_mj_mva",
    "f0_hz",
    "pm_pu",
    "pmax_pre_pu",
    "pmax_fault_pu",
    "pmax_post_pu",
)


def merged_givens(trace: SolutionTrace) -> dict[str, Any]:
    base = dict(trace.givens or {})
    if isinstance(trace.final.get("givens"), dict):
        base = {**base, **trace.final["givens"]}
    for step in trace.steps:
        g = step.values.get("givens")
        if isinstance(g, dict):
            base = {**base, **g}
    return base


def smib_case_from_givens(givens: dict[str, Any]) -> SmibCase | None:
    if not all(k in givens for k in _SMIB_KEYS):
        return None
    try:
        return SmibCase(
            h_mj_mva=float(givens["h_mj_mva"]),
            f0_hz=float(givens["f0_hz"]),
            pm_pu=float(givens["pm_pu"]),
            pmax_pre_pu=float(givens["pmax_pre_pu"]),
            pmax_fault_pu=float(givens["pmax_fault_pu"]),
            pmax_post_pu=float(givens["pmax_post_pu"]),
        )
    except (TypeError, ValueError):
        return None


def ed_case_from_givens(givens: dict[str, Any]) -> EdCase | None:
    units_in = givens.get("units")
    if not isinstance(units_in, list) or not units_in:
        return None
    try:
        units = []
        for row in units_in:
            units.append(
                EdUnit(
                    a=float(row["a"]),
                    b=float(row["b"]),
                    c=float(row["c"]),
                    pmin=float(row["pmin"]),
                    pmax=float(row["pmax"]),
                )
            )
        return EdCase(units=tuple(units))
    except (KeyError, TypeError, ValueError):
        return None


def agc_case_from_givens(givens: dict[str, Any]) -> TwoAreaAgcCase | None:
    preset = str(givens.get("agc_preset") or "")
    if preset == "eec301":
        k = float(givens["k"]) if "k" in givens else 0.0
        return TwoAreaAgcCase.eec301_default().with_k(k)
    return None


def pd_mw_from_givens(givens: dict[str, Any]) -> float | None:
    if "pd_mw" in givens:
        return float(givens["pd_mw"])
    return None
