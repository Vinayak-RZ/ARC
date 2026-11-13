"""Study-level load flow and sequence-network fault currents."""

from __future__ import annotations

import cmath
import json
import math
import re
from pathlib import Path
from typing import Any


def _parse_complex(val: Any) -> complex:
    if isinstance(val, complex):
        return val
    if isinstance(val, (int, float)):
        return complex(float(val))
    s = str(val).strip().replace(" ", "")
    if not s:
        raise ValueError("empty complex")
    s = s.replace("J", "j")
    m = re.match(r"^([+-]?)j(.*)$", s)
    if m:
        sign, rest = m.group(1) or "+", m.group(2)
        coeff = rest if rest not in ("", "+", "-") else "1"
        s = f"{sign}{coeff}j"
    elif s in ("j", "+j", "-j"):
        s = s.replace("j", "1j")
    return complex(s)


def pandapower_available() -> bool:
    try:
        import pandapower  # noqa: F401
    except ImportError:
        return False
    return True


def _default_network():
    import pandapower as pp

    net = pp.create_empty_network(sn_mva=100.0)
    b0 = pp.create_bus(net, vn_kv=11.0, name="slack")
    b1 = pp.create_bus(net, vn_kv=11.0, name="load")
    b2 = pp.create_bus(net, vn_kv=11.0, name="fault")
    pp.create_ext_grid(net, b0, vm_pu=1.0)
    pp.create_line_from_parameters(
        net,
        from_bus=b0,
        to_bus=b1,
        length_km=5.0,
        r_ohm_per_km=0.4,
        x_ohm_per_km=0.35,
        c_nf_per_km=0.0,
        max_i_ka=1.0,
    )
    pp.create_line_from_parameters(
        net,
        from_bus=b1,
        to_bus=b2,
        length_km=2.0,
        r_ohm_per_km=0.4,
        x_ohm_per_km=0.35,
        c_nf_per_km=0.0,
        max_i_ka=1.0,
    )
    pp.create_load(net, b1, p_mw=5.0, q_mvar=1.0)
    pp.create_load(net, b2, p_mw=0.5, q_mvar=0.15, name="fault_shunt")
    return net


def _sequence_fault(
    fault_type: str,
    v_prefault: complex,
    z1: complex,
    z2: complex,
    z0: complex,
    zf: complex = 0j,
) -> complex:
    """Symmetrical-component bolted fault currents (per-unit on common base)."""
    ft = fault_type.upper().replace(" ", "")
    if ft in {"3PH", "LLL", "THREE_PHASE"}:
        return v_prefault / z1
    if ft in {"LG", "SLG", "1LG"}:
        return 3.0 * v_prefault / (z1 + z2 + z0 + 3.0 * zf)
    if ft in {"LL", "2LL"}:
        return cmath.sqrt(3) * v_prefault / (z1 + z2)
    if ft in {"LLG", "2LLG", "DLG"}:
        den = z1 + z2 * (z0 + 3.0 * zf) / (z2 + z0 + 3.0 * zf)
        return cmath.sqrt(3) * v_prefault / den
    raise ValueError(f"unsupported fault type {fault_type}")


def run_power_study(run_dir: Path, problem: dict[str, Any]) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    fault_type = str(problem.get("fault_type") or "LG")
    use_sequence = problem.get("sequence") is True or problem.get("mode") == "sequence"

    table: list[dict[str, Any]] = []
    vm_pu: float | None = None

    if pandapower_available() and not use_sequence and problem.get("skip_pp") is not True:
        import pandapower as pp

        net = _default_network()
        if problem.get("network_json"):
            net = pp.from_json(str(problem["network_json"]))
        try:
            pp.runpp(net)
            bus_idx = int(problem.get("bus", 1))
            vm_pu = float(net.res_bus.vm_pu.at[bus_idx])
            for i, row in net.bus.iterrows():
                table.append(
                    {
                        "bus": int(i),
                        "name": str(row.name),
                        "vm_pu": float(net.res_bus.vm_pu.at[i]),
                        "va_degree": float(net.res_bus.va_degree.at[i]),
                    }
                )
        except (RuntimeError, ValueError, OSError) as exc:
            return {
                "ok": False,
                "error": f"pandapower runpp failed: {exc}",
                "unchecked": True,
                "tool": "pandapower",
            }

    v_pre = _parse_complex(problem.get("v_prefault_pu", 1.0))
    z1 = _parse_complex(problem.get("z1_pu", 0.1))
    z2 = _parse_complex(problem.get("z2_pu", 0.1))
    z0 = _parse_complex(problem.get("z0_pu", 0.3))
    zf = _parse_complex(problem.get("zf_pu", 0.0))
    try:
        i_fault = _sequence_fault(fault_type, v_pre, z1, z2, z0, zf)
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "unchecked": True, "tool": "sequence"}

    fault_row = {
        "fault_type": fault_type,
        "i_fault_pu": float(abs(i_fault)),
        "i_fault_angle_deg": float(math.degrees(cmath.phase(i_fault))),
    }
    table.append({"fault": fault_row})

    out_path = run_dir / "power_tables.json"
    out_path.write_text(json.dumps({"buses": table, "fault": fault_row}, indent=2), encoding="utf-8")

    svg = run_dir / "artifact.svg"
    svg.write_text(
        (
            "<svg xmlns='http://www.w3.org/2000/svg' width='360' height='140'>"
            "<text x='12' y='28' font-size='14'>Power study</text>"
            f"<text x='12' y='56' font-size='13'>Fault {fault_type}: |I|={fault_row['i_fault_pu']:.4f} pu</text>"
            f"<text x='12' y='84' font-size='13'>V@bus1={vm_pu if vm_pu is not None else '—'} pu</text>"
            "</svg>"
        ),
        encoding="utf-8",
    )

    value = fault_row["i_fault_pu"] if fault_row else vm_pu
    return {
        "ok": True,
        "tool": "pandapower+sequence",
        "unchecked": False,
        "value": value,
        "vm_pu": vm_pu,
        "fault": fault_row,
        "paths": [str(out_path), str(svg)],
        "tables": table,
    }
