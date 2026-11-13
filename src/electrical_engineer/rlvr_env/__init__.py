"""Open RLVR-style environment over PSA goldens (no weight training in v1)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MANIFEST = Path(__file__).resolve().parent / "manifest.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text())


def list_trap_ids() -> list[str]:
    return [str(t["id"]) for t in load_manifest().get("traps", [])]
