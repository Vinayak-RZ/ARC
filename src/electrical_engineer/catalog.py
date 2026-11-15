"""Discover checked-in YAML recipes."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from electrical_engineer.paths import workflows_dir
from electrical_engineer.runner.fsm import Recipe, parse_recipe


@dataclass(frozen=True)
class PackMeta:
    id: str
    label: str
    blurb: str


PACKS: tuple[PackMeta, ...] = (
    PackMeta("circuits", "Circuits", "Dividers, RLC, and SPICE checks"),
    PackMeta("signals", "Signals", "FFT, convolution, and frequency-domain homework"),
    PackMeta("electronics", "Electronics", "Bias, op-amps, and digital minimisation"),
    PackMeta("machines", "Machines", "Transformers, induction, and DC drives"),
    PackMeta("power", "Power", "Faults, swing, AGC, economic dispatch"),
    PackMeta("control", "Control", "Bode, step response, block diagrams"),
    PackMeta("power_electronics", "Power electronics", "Rectifiers, converters, and inverters"),
    PackMeta("measurements", "Measurements", "Bridges, meters, and error budgets"),
    PackMeta("em", "EM fields", "Line parameters and electrostatics"),
    PackMeta("maths", "Maths for EE", "Complex analysis and transforms for EE"),
)

KNOWLEDGE_DIR: dict[str, str] = {
    "power_electronics": "power-electronics",
}

_PACK_IDS = frozenset(p.id for p in PACKS)


def workflows_root(cwd: Path | None = None) -> Path:
    return workflows_dir(cwd)


def list_workflow_ids(cwd: Path | None = None) -> list[str]:
    root = workflows_root(cwd)
    if not root.is_dir():
        return []
    ids: list[str] = []
    for path in sorted(root.glob("**/*.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        ids.append(str(data.get("id") or path.stem))
    return ids


def load_recipe(recipe_id: str, cwd: Path | None = None) -> Recipe:
    root = workflows_root(cwd)
    for path in root.glob("**/*.yaml"):
        data = yaml.safe_load(path.read_text()) or {}
        if str(data.get("id") or path.stem) == recipe_id:
            return parse_recipe(data)
    raise FileNotFoundError(recipe_id)


def load_recipe_meta(recipe_id: str, cwd: Path | None = None) -> dict[str, Any]:
    """Return title/pack/sample_problem from the YAML (unknown keys preserved)."""
    root = workflows_root(cwd)
    for path in root.glob("**/*.yaml"):
        data = yaml.safe_load(path.read_text()) or {}
        if str(data.get("id") or path.stem) == recipe_id:
            pack = path.parent.name if path.parent.name in _PACK_IDS else None
            return {
                "id": recipe_id,
                "title": data.get("title"),
                "pack": data.get("pack") or pack,
                "sample_problem": data.get("sample_problem"),
            }
    raise FileNotFoundError(recipe_id)


@lru_cache(maxsize=8)
def _id_to_pack(root_s: str) -> dict[str, str]:
    root = Path(root_s)
    out: dict[str, str] = {}
    if not root.is_dir():
        return out
    for path in root.glob("**/*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        rid = str(data.get("id") or path.stem)
        folder = path.parent.name
        if folder in _PACK_IDS:
            out[rid] = folder
    return out


def pack_for_recipe(recipe_id: str, cwd: Path | None = None) -> str | None:
    root = workflows_root(cwd)
    return _id_to_pack(str(root.resolve())).get(recipe_id)


def pack_recipe_counts(cwd: Path | None = None) -> list[dict[str, Any]]:
    root = workflows_root(cwd)
    ids = list_workflow_ids(cwd)
    out: list[dict[str, Any]] = []
    for pack in PACKS:
        folder = root / pack.id
        count = len(list(folder.glob("**/*.yaml"))) if folder.is_dir() else 0
        if count == 0:
            count = sum(1 for i in ids if pack.id in i.replace("_", "-") or pack.id in i)
        out.append(
            {
                "id": pack.id,
                "label": pack.label,
                "blurb": pack.blurb,
                "recipe_count": count,
            }
        )
    return out
