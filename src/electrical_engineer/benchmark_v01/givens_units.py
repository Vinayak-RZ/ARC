"""Units for every scalar key present in public givens."""

from __future__ import annotations

from typing import Any

_SCALAR_UNITS: dict[str, str] = {
    "h_mj_mva": "MJ/MVA",
    "f0_hz": "Hz",
    "pm_pu": "pu",
    "pmax_pre_pu": "pu",
    "pmax_fault_pu": "pu",
    "pmax_post_pu": "pu",
    "h_integrator_s": "s",
    "tc_s": "s",
    "t_query_s": "s",
    "dpl1_pu": "pu",
    "dpl2_pu": "pu",
    "step_time_s": "s",
    "t_end_s": "s",
    "agc_t_end_s": "s",
    "K_agc": "pu",
    "h_s": "s",
    "tie_sync_gain": "pu",
    "base_mva": "MVA",
    "PD_MW": "MW",
    "unit1_MW": "MW",
    "pd_mw": "MW",
    "vin": "V",
    "vin_V": "V",
    "r1": "ohm",
    "r2": "ohm",
    "r1_ohm": "ohm",
    "r2_ohm": "ohm",
    "v": "V",
    "c": "F",
    "l": "H",
    "t": "s",
    "vc0": "V",
    "i0": "A",
    "gain": "1",
    "system_type": "1",
    "ts": "s",
    "ct_primary_a": "A",
    "ct_secondary_a": "A",
    "relay_pickup_a": "A",
    "fault_current_a": "A",
    "v_prefault_pu": "pu",
    "z1_pu": "pu",
    "z2_pu": "pu",
    "z0_pu": "pu",
    "zf_pu": "pu",
    "s_system_mva": "MVA",
    "v_system_kv": "kV",
    "a": "Rs/MWh",
    "b": "Rs/MWh",
    "pmin": "MW",
    "pmax": "MW",
}

_AREA_KEY_UNITS = {"tg": "s", "tt": "s", "m": "s", "d": "pu", "r": "pu", "b": "pu", "k": "pu"}
_UNIT_COST_C = "Rs/MWh/MW^2"


def _unit_for(path: str, key: str) -> str | None:
    if path.startswith("area") and key in _AREA_KEY_UNITS:
        return _AREA_KEY_UNITS[key]
    if key == "r" and "area" not in path:
        return "ohm"
    if key == "r" and path.startswith("area"):
        return "pu"
    if key == "c" and path.startswith("units"):
        return _UNIT_COST_C
    return _SCALAR_UNITS.get(key)


def givens_units_map(givens: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}

    def walk(obj: Any, prefix: str) -> None:
        if isinstance(obj, dict):
            for key, val in obj.items():
                path = f"{prefix}.{key}" if prefix else key
                if isinstance(val, dict):
                    walk(val, path)
                elif isinstance(val, list) and val and isinstance(val[0], dict):
                    for i, row in enumerate(val):
                        walk(row, f"{path}[{i}]")
                else:
                    unit = _unit_for(path, key)
                    if unit:
                        out[path] = unit
                    elif key == "num" or key == "den":
                        out[path] = "s-domain coeff"
                    elif key == "units" and isinstance(val, list):
                        out[path] = "generator cost tables"
                    elif key == "B":
                        out[path] = "loss coeff matrix"
                    elif key == "elements":
                        out[path] = "network elements"
                    elif key == "blocks":
                        out[path] = "block diagram"
        elif isinstance(obj, list):
            for i, row in enumerate(obj):
                walk(row, f"{prefix}[{i}]")

    walk(givens, "")
    return out
