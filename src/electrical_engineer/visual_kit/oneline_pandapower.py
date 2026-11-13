"""Pandapower-sourced one-line study network (default 3-bus)."""

from __future__ import annotations

from typing import Any


def load_flow_snapshot() -> dict[str, Any]:
    from electrical_engineer.engines.power_runner import _default_network, pandapower_available

    if not pandapower_available():
        return {
            "ok": False,
            "buses": [
                {"name": "slack", "vm_pu": 1.0, "va_deg": 0.0},
                {"name": "load", "vm_pu": 0.98, "va_deg": -1.2, "p_mw": 5.0, "q_mvar": 1.0},
                {"name": "fault", "vm_pu": 0.97, "va_deg": -1.5},
            ],
            "lines": [
                {"from": "slack", "to": "load", "p_mw": 5.0, "loading_pct": 32.0},
                {"from": "load", "to": "fault", "p_mw": 0.2, "loading_pct": 4.0},
            ],
            "fault_bus": "fault",
        }
    import pandapower as pp

    net = _default_network()
    pp.runpp(net)
    buses = []
    for i, row in net.bus.iterrows():
        buses.append(
            {
                "idx": int(i),
                "name": str(row["name"]),
                "vn_kv": float(row["vn_kv"]),
                "vm_pu": float(net.res_bus.vm_pu.at[i]),
                "va_deg": float(net.res_bus.va_degree.at[i]),
            }
        )
    lines = []
    for i, row in net.line.iterrows():
        fb = int(row["from_bus"])
        tb = int(row["to_bus"])
        lines.append(
            {
                "from": net.bus.name.at[fb],
                "to": net.bus.name.at[tb],
                "p_from_mw": float(net.res_line.p_from_mw.at[i]),
                "loading_pct": float(net.res_line.loading_percent.at[i]),
            }
        )
    load_p = float(net.load.p_mw.sum())
    return {
        "ok": True,
        "buses": buses,
        "lines": lines,
        "load_p_mw": load_p,
        "fault_bus": "fault",
        "sn_mva": float(net.sn_mva),
    }
