"""Economic dispatch from catalog MATPOWER-style gencost rows (not pandapower poly_cost)."""

from __future__ import annotations

from typing import Any

from electrical_engineer.engines.ed_lambda import EdCase, EdUnit, solve_lambda_ed
from electrical_engineer.reference.catalog import get_record


def economic_dispatch(
    gencost_record_id: str,
    *,
    total_load_mw: float,
    out_of_service_buses: list[int] | None = None,
) -> dict[str, Any]:
    """gencost rows: bus, c2, c1, c0, pmin, pmax (MATPOWER quadratic cost)."""
    rec = get_record(gencost_record_id)
    if rec is None:
        raise ValueError(f"unknown gencost record {gencost_record_id}")
    oos = set(out_of_service_buses or [])
    units: list[EdUnit] = []
    rows: list[dict[str, Any]] = []
    for row in rec["values"]["generators"]:
        bus = int(row["bus"])
        if bus in oos:
            continue
        c2, c1, c0 = float(row["c2"]), float(row["c1"]), float(row["c0"])
        pmin, pmax = float(row["pmin_mw"]), float(row["pmax_mw"])
        # fuel_cost in ed_lambda: a + b*P + c*P^2  == c0 + c1*P + c2*P^2
        units.append(EdUnit(c0, c1, c2, pmin, pmax))
        rows.append({"bus": bus, "c2": c2, "c1": c1, "c0": c0, "pmin_mw": pmin, "pmax_mw": pmax})
    if not units:
        raise ValueError("no in-service generators")
    out = solve_lambda_ed(EdCase(units=tuple(units)), total_load_mw)
    dispatch = [
        {"bus": rows[i]["bus"], "p_mw": out["P"][i], "ic_mw_per_mw": out["IC"][i]}
        for i in range(len(rows))
    ]
    return {
        "gencost_record_id": gencost_record_id,
        "total_load_mw": total_load_mw,
        "out_of_service_buses": sorted(oos),
        "lambda_mw_per_mw": out["lam"],
        "generators": dispatch,
        "total_cost_per_h": out["total_cost"],
        "source_id": gencost_record_id,
        "note": "Costs from MATPOWER mpc.gencost row order, not pandapower poly_cost indexing",
    }
