"""Per-unit base changes and symmetrical-fault bus impedance aggregation."""

from __future__ import annotations

from typing import Any

from electrical_engineer.engines.power_runner import _parse_complex


def impedance_pu_on_new_base(
    z_pu: complex,
    *,
    s_old_mva: float,
    s_new_mva: float,
    v_old_kv: float,
    v_new_kv: float,
) -> complex:
    if s_old_mva <= 0 or s_new_mva <= 0 or v_old_kv <= 0 or v_new_kv <= 0:
        raise ValueError("MVA and kV bases must be positive")
    return z_pu * (s_old_mva / s_new_mva) * (v_old_kv / v_new_kv) ** 2


def aggregate_fault_impedance(
    elements: list[dict[str, Any]],
    *,
    s_system_mva: float,
    v_system_kv: float,
) -> dict[str, Any]:
    """Convert each element to system base and return Z1/Z2/Z0 sum table."""
    rows: list[dict[str, Any]] = []
    z1 = 0j
    z2 = 0j
    z0 = 0j
    for el in elements:
        seq = str(el.get("sequence") or "1").strip()
        z_old = _parse_complex(el.get("z_pu"))
        z_new = impedance_pu_on_new_base(
            z_old,
            s_old_mva=float(el.get("s_base_mva") or s_system_mva),
            s_new_mva=s_system_mva,
            v_old_kv=float(el.get("v_base_kv") or v_system_kv),
            v_new_kv=v_system_kv,
        )
        rows.append(
            {
                "id": el.get("id"),
                "sequence": seq,
                "z_pu_old": f"{z_old.real:.6g}{z_old.imag:+.6g}j",
                "z_pu_system": f"{z_new.real:.6g}{z_new.imag:+.6g}j",
            }
        )
        if seq in {"1", "pos", "positive"}:
            z1 += z_new
        elif seq in {"2", "neg", "negative"}:
            z2 += z_new
        elif seq in {"0", "zero"}:
            z0 += z_new
        else:
            z1 += z_new
            z2 += z_new
            z0 += z_new
    return {
        "s_system_mva": s_system_mva,
        "v_system_kv": v_system_kv,
        "table": rows,
        "z1_pu": z1,
        "z2_pu": z2,
        "z0_pu": z0,
        "z1_pu_mag": float(abs(z1)),
    }
