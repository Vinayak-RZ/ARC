"""Keyword scores for omitted-id CLI classify. Router never invents ids."""

from __future__ import annotations

KEYWORDS: dict[str, tuple[str, ...]] = {
    "simulate-circuit": ("spice", "netlist", "simulate", "transient"),
    "derive-circuit": ("derive", "kvl", "kcl", "thevenin"),
    "photo-to-netlist": ("photo", "handwritten", "schematic image"),
    "solve-circuit-problem": ("ohm", "divider", "mesh", "nodal"),
}


def scores_from_text(text: str) -> list[tuple[str, float]]:
    blob = text.lower()
    out: list[tuple[str, float]] = []
    for wid, words in KEYWORDS.items():
        hits = sum(1 for w in words if w in blob)
        if hits:
            out.append((wid, hits / len(words)))
    return out
