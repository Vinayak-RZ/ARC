"""NEC Table 310.16 ampacity with 310.15(B)(1) and 310.15(C)(1) adjustments."""

from __future__ import annotations

import math
import re
from typing import Any

from electrical_engineer.reference.catalog import get_record

_INSULATION_KEYS = {"60": "factor_60", "75": "factor_75", "90": "factor_90"}
_AWG_RE = re.compile(r"^\s*(\d+(?:/\d+)?)\s*(?:awg|kcmil)?\s*$", re.IGNORECASE)


def _normalize_size_awg(size: str) -> str:
    raw = str(size).strip().upper().replace("AWG", "").replace("KCMIL", "").strip()
    m = _AWG_RE.match(raw) or _AWG_RE.match(str(size))
    if m:
        return m.group(1)
    return raw


def _band_factor(
    bands: list[dict[str, Any]],
    *,
    value: int,
    factor_key: str,
    label_key: str = "label",
) -> tuple[float, str]:
    for row in bands:
        lo = row.get("ambient_c_min")
        if lo is None:
            lo = row.get("n_min")
        hi = row.get("ambient_c_max")
        if hi is None:
            hi = row.get("n_max")
        in_band = True
        if lo is not None and value < int(lo):
            in_band = False
        if hi is not None and value > int(hi):
            in_band = False
        if not in_band:
            continue
        factor = row.get(factor_key) if factor_key in row else row.get("factor")
        if factor is None:
            raise ValueError(f"NEC band {row.get(label_key)} has no factor for {factor_key}")
        return float(factor), str(row.get(label_key) or "")
    raise ValueError(f"no NEC band for value {value}")


def ambient_correction_factor(*, ambient_c: int, insulation_column: str) -> dict[str, Any]:
    col = str(insulation_column).strip()
    if col not in _INSULATION_KEYS:
        raise ValueError(f"insulation_column must be one of {sorted(_INSULATION_KEYS)}")
    rec = get_record("NEC_TABLE_310_15B1_AMBIENT")
    if rec is None:
        raise ValueError("NEC_TABLE_310_15B1_AMBIENT missing from catalog")
    fkey = _INSULATION_KEYS[col]
    bands = rec["values"]["ambient_bands"]
    factor, label = _band_factor(bands, value=int(ambient_c), factor_key=fkey)
    return {
        "ambient_c": ambient_c,
        "insulation_column_c": int(col),
        "ambient_factor": factor,
        "ambient_band_label": label,
        "record_id": "NEC_TABLE_310_15B1_AMBIENT",
        "standard_clause": "NEC Table 310.15(B)(1)(1)",
        "boundary_policy": rec["values"].get("boundary_policy"),
    }


def conductor_count_factor(*, n_current_carrying: int) -> dict[str, Any]:
    if n_current_carrying < 4:
        return {
            "n_current_carrying": n_current_carrying,
            "adjustment_factor": 1.0,
            "conductor_band_label": "1-3 (no adjustment)",
            "record_id": "NEC_TABLE_310_15C1_ADJUSTMENT",
            "standard_clause": "NEC Table 310.15(C)(1) not applied",
        }
    rec = get_record("NEC_TABLE_310_15C1_ADJUSTMENT")
    if rec is None:
        raise ValueError("NEC_TABLE_310_15C1_ADJUSTMENT missing from catalog")
    bands = rec["values"]["conductor_bands"]
    factor, label = _band_factor(bands, value=int(n_current_carrying), factor_key="factor")
    return {
        "n_current_carrying": n_current_carrying,
        "adjustment_factor": factor,
        "conductor_band_label": label,
        "record_id": "NEC_TABLE_310_15C1_ADJUSTMENT",
        "standard_clause": "NEC Table 310.15(C)(1)",
        "boundary_policy": rec["values"].get("boundary_policy"),
    }


def table31016_ampacity_a(*, size_awg: str, material: str, insulation_column: str) -> dict[str, Any]:
    mat = str(material).strip().lower()
    col = str(insulation_column).strip()
    if mat not in ("cu", "copper"):
        raise ValueError("this pass catalog covers copper only (material=cu)")
    if col != "90":
        raise ValueError("this pass lookup uses NEC_TABLE_310_16_CU_90C (insulation_column=90)")
    size_key = _normalize_size_awg(size_awg)
    rec = get_record("NEC_TABLE_310_16_CU_90C")
    if rec is None:
        raise ValueError("NEC_TABLE_310_16_CU_90C missing from catalog")
    table = rec["values"]["ampacity_by_size"]
    if size_key not in table:
        raise ValueError(f"size {size_awg!r} not in NEC copper 90 C table")
    return {
        "size_awg": size_key,
        "material": "copper",
        "insulation_column_c": 90,
        "base_ampacity_a": float(table[size_key]),
        "record_id": "NEC_TABLE_310_16_CU_90C",
        "standard_clause": "NEC Table 310.16",
    }


def allowable_ampacity(
    *,
    size_awg: str,
    material: str,
    insulation_column: str,
    ambient_c: int,
    n_current_carrying: int,
) -> dict[str, Any]:
    """Corrected allowable ampacity with NEC round-down (fractional ampere dropped)."""
    base = table31016_ampacity_a(
        size_awg=size_awg, material=material, insulation_column=insulation_column
    )
    amb = ambient_correction_factor(ambient_c=ambient_c, insulation_column=insulation_column)
    adj = conductor_count_factor(n_current_carrying=n_current_carrying)
    corrected = (
        base["base_ampacity_a"] * amb["ambient_factor"] * adj["adjustment_factor"]
    )
    allowable = float(math.floor(corrected))
    return {
        **base,
        **amb,
        **adj,
        "ambient_boundary_policy": amb.get("boundary_policy"),
        "conductor_boundary_policy": adj.get("boundary_policy"),
        "corrected_ampacity_a": corrected,
        "allowable_ampacity_a": allowable,
        "round_down_rule": "NEC 310.15(B) / 310.15(C) — drop fractional amperes",
        "inputs_used": {
            "size_awg": base["size_awg"],
            "material": material,
            "insulation_column": insulation_column,
            "ambient_c": ambient_c,
            "n_current_carrying": n_current_carrying,
        },
    }
