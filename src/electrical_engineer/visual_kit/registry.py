"""Arc Visual Kit registry: engine-bound components only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def manifest_path() -> Path:
    return Path(__file__).resolve().parent / "manifest.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(manifest_path().read_text())


def list_component_ids() -> list[str]:
    return [str(c["id"]) for c in load_manifest().get("components", [])]


GOLDEN_MAP: dict[str, str] = {
    "power.swing_equal_area": "swing",
    "power.agc_trace": "agc",
    "power.dispatch_curve": "ed",
    "power.swing_animation": "swing",
    "power.oneline_bus": "oneline",
    "control.bode": "control",
    "control.step": "control",
    "control.root_locus": "control",
    "control.block_diagram": "control",
    "schematic.divider": "circuits",
    "waveform.phasor": "circuits",
}


def golden_path(component_id: str) -> Path | None:
    for c in load_manifest().get("components", []):
        if c.get("id") == component_id:
            rel = c.get("golden")
            if rel:
                return Path("artifacts/visual-goldens") / str(rel)
    return None


def get_component(component_id: str) -> dict[str, Any] | None:
    for c in load_manifest().get("components", []):
        if c.get("id") == component_id:
            return c
    return None
