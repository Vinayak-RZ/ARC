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


def get_component(component_id: str) -> dict[str, Any] | None:
    for c in load_manifest().get("components", []):
        if c.get("id") == component_id:
            return c
    return None
