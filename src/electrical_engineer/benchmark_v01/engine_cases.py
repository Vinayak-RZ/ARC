"""Build engine case objects from public givens dicts."""

from __future__ import annotations

from typing import Any

from electrical_engineer.engines.agc_two_area import AreaParams, TwoAreaAgcCase
from electrical_engineer.engines.ed_lambda import EdCase, EdUnit


def agc_case_from_givens(g: dict[str, Any]) -> TwoAreaAgcCase:
    def area(obj: dict[str, float]) -> AreaParams:
        return AreaParams(
            tg=float(obj["tg"]),
            tt=float(obj["tt"]),
            m=float(obj["m"]),
            d=float(obj["d"]),
            r=float(obj["r"]),
            b=float(obj["b"]),
            k=float(obj.get("k", 0.0)),
        )

    return TwoAreaAgcCase(
        area1=area(g["area1"]),
        area2=area(g["area2"]),
        tie_sync_gain=float(g.get("tie_sync_gain", 2.0)),
        f0_hz=float(g.get("f0_hz", 60.0)),
        base_mva=float(g.get("base_mva", 1000.0)),
    )


def ed_case_from_givens(g: dict[str, Any]) -> EdCase:
    units = tuple(EdUnit(**u) for u in g["units"])
    return EdCase(units=units)
