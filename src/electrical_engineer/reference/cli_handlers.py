"""CLI handlers for reference search/get/engine."""

from __future__ import annotations

import json
import sys
from typing import Any

from electrical_engineer.reference import catalog
from electrical_engineer.reference import engines as ref_engines


def cmd_search(query: str) -> int:
    hits = catalog.search_records(query)
    print(json.dumps({"query": query, "count": len(hits), "results": hits}, indent=2))
    return 0 if hits else 1


def cmd_get(record_id: str) -> int:
    rec = catalog.get_record(record_id)
    if rec is None:
        print(json.dumps({"error": "not_found", "id": record_id}), file=sys.stderr)
        return 2
    print(json.dumps(rec, indent=2))
    return 0


def cmd_engine(name: str, payload: dict[str, Any]) -> int:
    name = name.lower().replace("-", "_")
    try:
        if name == "idmt":
            out = ref_engines.idmt_operating_time_s(
                str(payload["curve_id"]),
                tms=float(payload.get("tms", 1.0)),
                i_ratio=float(payload["i_ratio"]),
            )
        elif name == "iec60909":
            z = payload.get("z_ohm")
            if isinstance(z, dict):
                zc = complex(float(z["re"]), float(z.get("im", 0)))
            else:
                zc = complex(z)
            out = ref_engines.initial_symmetrical_ka(
                voltage_kv=float(payload["voltage_kv"]),
                z_ohm=zc,
                c_factor_id=str(payload.get("c_factor_id", "IEC60909_CMAX_LV")),
                kt=float(payload.get("kt", 1.0)),
            )
        elif name == "line_params":
            out = ref_engines.line_sequence_per_km(
                str(payload["conductor_id"]),
                length_km=float(payload["length_km"]),
                spacing_m=float(payload["spacing_m"]) if payload.get("spacing_m") is not None else None,
                n_bundled=int(payload.get("n_bundled", 1)),
                freq_hz=float(payload.get("freq_hz", 50.0)),
                temp_c=float(payload["temp_c"]) if payload.get("temp_c") is not None else None,
            )
        elif name == "load_flow":
            out = ref_engines.run_case_load_flow(str(payload["case_id"]))
        elif name == "economic_dispatch":
            oos = payload.get("out_of_service_buses") or []
            out = ref_engines.economic_dispatch(
                str(payload["gencost_record_id"]),
                total_load_mw=float(payload["total_load_mw"]),
                out_of_service_buses=[int(b) for b in oos],
            )
        elif name == "iec60909_peak":
            z = payload.get("z_ohm")
            if isinstance(z, dict):
                zc = complex(float(z["re"]), float(z.get("im", 0)))
            else:
                zc = complex(z)
            out = ref_engines.peak_short_circuit_ka(
                voltage_kv=float(payload["voltage_kv"]),
                z_ohm=zc,
                c_factor_id=str(payload.get("c_factor_id", "IEC60909_CMAX_LV")),
                kt=float(payload.get("kt", 1.0)),
                kappa_id=str(payload.get("kappa_id", "IEC60909_KAPPA_XR10")),
            )
        elif name == "nema_locked_rotor":
            out = ref_engines.locked_rotor_current_a(
                code_id=str(payload["code_id"]),
                hp=float(payload["hp"]),
                line_voltage_v=float(payload["line_voltage_v"]),
                use=str(payload.get("use", "mid")),
            )
        elif name == "ieee80":
            if payload.get("kind") is None or payload.get("body_mass_kg") is None:
                raise ValueError("ieee80 requires kind (touch|step) and body_mass_kg (50|70)")
            if payload.get("rho_s_ohm_m") is None or payload.get("cs") is None or payload.get("t_s") is None:
                raise ValueError("ieee80 requires rho_s_ohm_m, cs, and t_s")
            out = ref_engines.tolerable_voltages(
                kind=str(payload["kind"]),
                body_mass_kg=int(payload["body_mass_kg"]),
                rho_s_ohm_m=float(payload["rho_s_ohm_m"]),
                cs=float(payload["cs"]),
                t_s=float(payload["t_s"]),
            )
        elif name == "ieee519":
            if payload.get("measured_tdd_percent") is not None:
                out = ref_engines.tdd_compliance(
                    isc_il_ratio=float(payload["isc_il_ratio"]),
                    measured_tdd_percent=float(payload["measured_tdd_percent"]),
                )
            elif payload.get("ratio_id"):
                out = ref_engines.tdd_limit_percent(ratio_id=str(payload["ratio_id"]))
            else:
                out = ref_engines.tdd_limit_percent(isc_il_ratio=float(payload["isc_il_ratio"]))
        elif name == "mcb":
            out = ref_engines.magnetic_trip_in_band(
                mcb_type_id=str(payload["mcb_type_id"]),
                i_a=float(payload["i_a"]),
                rated_in_a=float(payload["rated_in_a"]),
            )
        elif name == "vector_group":
            out = ref_engines.phase_shift_deg(group_id=str(payload["group_id"]))
        else:
            print(json.dumps({"error": "unknown_engine", "name": name}), file=sys.stderr)
            return 2
    except (KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "engine": name}), file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2))
    return 0
