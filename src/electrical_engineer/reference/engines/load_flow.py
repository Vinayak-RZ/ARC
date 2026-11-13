"""IEEE test-system load flow via pandapower case loaders."""

from __future__ import annotations

from typing import Any

from electrical_engineer.engines.power_runner import pandapower_available
from electrical_engineer.reference.catalog import get_record


def run_case_load_flow(case_id: str) -> dict[str, Any]:
    rec = get_record(case_id)
    if rec is None:
        raise ValueError(f"unknown case id {case_id}")
    loader = str(rec["values"].get("pandapower_loader", ""))
    if not loader:
        raise ValueError(f"case {case_id} has no pandapower_loader")
    if not pandapower_available():
        return {
            "case_id": case_id,
            "unchecked": True,
            "reason": "pandapower not installed (extra power)",
            "source_id": case_id,
        }
    import pandapower as pp
    import pandapower.networks as pn

    net = getattr(pn, loader)()
    pp.runpp(net)
    buses = []
    for idx, row in net.bus.iterrows():
        vm = float(net.res_bus.vm_pu.at[idx])
        buses.append({"bus": int(idx), "name": str(row.get("name", "")), "vm_pu": vm})
    worst = min(buses, key=lambda b: b["vm_pu"])
    return {
        "case_id": case_id,
        "loader": loader,
        "sn_mva": float(net.sn_mva),
        "bus_count": len(net.bus),
        "min_vm_pu": worst["vm_pu"],
        "min_vm_bus": worst["bus"],
        "converged": bool(net.converged),
        "source_id": case_id,
    }
