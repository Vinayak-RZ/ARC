"""Validate arc.diagram.v1 payloads (mirrors ui/src/studio-engine/spec.js)."""

from __future__ import annotations

from typing import Any

SCHEMA = "arc.diagram.v1"
MAX_POINTS = 4000
COMPONENT_PINS = {
    "resistor",
    "inductor",
    "capacitor",
    "switch",
    "vsource",
    "isource",
    "acsource",
    "diode",
    "scr",
    "igbt",
    "ground",
    "transformer",
    "motor",
    "opamp",
    "bjt",
    "junction",
    "terminal",
}
PANEL_KINDS = {"schematic", "block", "oneline", "waveform"}
ROTS = {0, 90, 180, 270}
WAVE_STYLES = {"primary", "secondary", "positive", "muted-dashed"}
SCALES = {"linear", "log"}


def validate_diagram(d: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(d, dict):
        return ["diagram must be object"]
    if d.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    panels = d.get("panels")
    if not isinstance(panels, list):
        errors.append("panels must be array")
        return errors
    for i, panel in enumerate(panels):
        pfx = f"panels[{i}]"
        if not isinstance(panel, dict):
            errors.append(f"{pfx}: must be object")
            continue
        kind = panel.get("kind")
        if kind not in PANEL_KINDS:
            errors.append(f"{pfx}: unknown kind")
        if kind == "schematic":
            for c in panel.get("components") or []:
                if c.get("type") not in COMPONENT_PINS:
                    errors.append(f"{pfx}: unknown component {c.get('type')}")
                if c.get("rot") is not None and c.get("rot") not in ROTS:
                    errors.append(f"{pfx}: bad rot")
        if kind == "waveform":
            for s in panel.get("series") or []:
                style = s.get("style") or "primary"
                if style not in WAVE_STYLES:
                    errors.append(f"{pfx}: bad series style")
                n = len(s.get("points") or [])
                if n > MAX_POINTS:
                    errors.append(f"{pfx}: series {s.get('id')} exceeds {MAX_POINTS} points")
            x = panel.get("x") or {}
            y = panel.get("y") or {}
            if x.get("scale") and x.get("scale") not in SCALES:
                errors.append(f"{pfx}: bad x scale")
            if y.get("scale") and y.get("scale") not in SCALES:
                errors.append(f"{pfx}: bad y scale")
    return errors
