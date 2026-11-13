"""Voltage divider DC solve (ngspice if available, else KCL)."""

from __future__ import annotations

import tempfile
from pathlib import Path


def solve_divider(r1_ohm: float = 1000.0, r2_ohm: float = 1000.0, v_in: float = 10.0) -> dict[str, float]:
    v_out = v_in * r2_ohm / (r1_ohm + r2_ohm)
    i_a = v_in / (r1_ohm + r2_ohm)
    try:
        from electrical_engineer.engines.spice_runner import run_spice_netlist, spice_available

        if spice_available():
            cir = (
                f"* divider\nV1 1 0 DC {v_in}\nR1 1 2 {r1_ohm}\nR2 2 0 {r2_ohm}\n"
                ".control\nop\nprint v(2) i(v1)\n.endc\n.end\n"
            )
            with tempfile.TemporaryDirectory() as td:
                out = run_spice_netlist(cir, Path(td), {"probe_node": 2})
                if out.get("ok") and out.get("value") is not None:
                    v_out = float(out["value"])
    except (ImportError, OSError, ValueError, TypeError):
        pass
    v_analytic = v_in * r2_ohm / (r1_ohm + r2_ohm)
    return {
        "V_in": v_in,
        "V_out": v_analytic,
        "V_out_spice": v_out,
        "I": i_a,
        "R1": r1_ohm,
        "R2": r2_ohm,
        "spice_used": abs(v_out - v_analytic) > 1e-6,
    }
