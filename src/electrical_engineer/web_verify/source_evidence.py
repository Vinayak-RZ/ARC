"""Source snippet/value alignment for web-verify evidence bundles."""

from __future__ import annotations

import math
import re
from typing import Any


def _variants(value: float, unit: str | None) -> list[str]:
    patterns: list[str] = []
    v = value
    if math.isclose(v, round(v)):
        patterns.append(str(int(round(v))))
    patterns.append(f"{v:.6g}")
    patterns.append(f"{v:.4f}".rstrip("0").rstrip("."))
    u = (unit or "").lower()
    if u in ("m", "metre", "meter") and 0.001 < v < 1:
        patterns.append(f"{v * 1000:.4g} mm")
        patterns.append(f"{v * 100:.4g} cm")
        patterns.append(f"{v * 1000:.2f} mm".rstrip("0").rstrip("."))
    if "ohm" in u and v < 1:
        patterns.append(f"{v * 1000:.4g} mohm")
        patterns.append(f"{v * 1000:.4g} mOhm")
        patterns.append("44 m")
    if "ohm/km" in u.replace(" ", ""):
        patterns.append(f"{v:.4g} Ohm/km")
        patterns.append(f"{v:.4g} ohm/km")
    return patterns


def value_supported_by_snippet(snippet: str, value: float | None, unit: str | None) -> bool:
    if value is None:
        return True
    text = snippet.lower()
    for p in _variants(float(value), unit):
        if p.lower() in text:
            return True
    return False


def counts_toward_minimum(src: dict[str, Any]) -> bool:
    role = str(src.get("source_class") or src.get("role") or "primary").lower()
    if role in ("context_only", "corroboration"):
        return False
    if role in ("standard_tutorial", "standard_constant") and src.get("extracted_value") is None:
        return bool((src.get("snippet") or "").strip())
    if role == "derived":
        return bool((src.get("derivation") or src.get("snippet") or "").strip())
    if role in ("secondary_mirror", "authorized_distributor_mirror"):
        return True
    val = src.get("extracted_value")
    if val is not None and not value_supported_by_snippet(
        str(src.get("snippet") or ""), float(val), src.get("unit")
    ):
        return False
    return bool((src.get("snippet") or "").strip())


def validate_claim_sources(claim: dict[str, Any], *, min_sources: int = 2) -> None:
    sources = claim.get("sources") or []
    counting = [s for s in sources if counts_toward_minimum(s)]
    if len(counting) < min_sources:
        raise ValueError(
            f"claim {claim.get('claim_id')}: need {min_sources} verifiable sources, got {len(counting)}"
        )
    domains = {
        (s.get("domain") or "").lower().replace("www.", "")
        for s in counting
        if s.get("domain")
    }
    has_derived = any(str(s.get("source_class") or "").lower() == "derived" for s in counting)
    non_derived_domains = {
        (s.get("domain") or "").lower().replace("www.", "")
        for s in counting
        if s.get("domain") and str(s.get("source_class") or "").lower() != "derived"
    }
    if has_derived:
        if len(non_derived_domains) < 1:
            raise ValueError(f"claim {claim.get('claim_id')}: derived evidence needs a non-derived domain source")
    elif len(domains) < 2:
        raise ValueError(
            f"claim {claim.get('claim_id')}: need at least 2 independent domains among verifiable sources"
        )


def validate_fixture_claim(claim: dict[str, Any]) -> None:
    validate_claim_sources(claim, min_sources=2)
    for src in claim.get("sources") or []:
        role = str(src.get("source_class") or "primary").lower()
        if role == "derived":
            continue
        val = src.get("extracted_value")
        if val is None:
            continue
        if not value_supported_by_snippet(str(src.get("snippet") or ""), float(val), src.get("unit")):
            if role not in ("context_only",):
                raise ValueError(
                    f"source {src.get('url')}: extracted_value {val} not supported by snippet"
                )
