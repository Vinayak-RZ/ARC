"""Load and validate Learn curriculum YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from electrical_engineer.catalog import PACKS, list_workflow_ids
from electrical_engineer.runner.runs import project_root

_LAB_IDS = frozenset({"rectifier", "converter", "idmt", "lead"})
_PACK_IDS = frozenset(p.id for p in PACKS) | {None}
_CURRICULUM_PATH = Path(__file__).with_name("curriculum.yaml")


def curriculum_path() -> Path:
    return _CURRICULUM_PATH


def load_curriculum(root: Path | None = None) -> dict[str, Any]:
    del root  # packaged YAML; root reserved for future checkout overlays
    data = yaml.safe_load(_CURRICULUM_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("curriculum.yaml must be a mapping")
    return data


def _coverage_path(cwd: Path | None = None) -> Path:
    return project_root(cwd) / "knowledge" / "COVERAGE.yaml"


def _load_coverage_units(cwd: Path | None = None) -> dict[str, list[dict[str, str]]]:
    path = _coverage_path(cwd)
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    packs = data.get("packs") or {}
    out: dict[str, list[dict[str, str]]] = {}
    for key, pack in packs.items():
        units = []
        for u in pack.get("units") or []:
            units.append({"id": str(u["id"]), "title": str(u.get("title") or u["id"])})
        out[str(key)] = units
    # electives live under knowledge/ug-ee/electives — COVERAGE may not list them;
    # fall back to directory chapter folders when units_from starts with electives/
    return out


def _elective_units(cwd: Path | None, rel: str) -> list[dict[str, str]]:
    """List chapter folders under knowledge/ug-ee/<rel>."""
    base = project_root(cwd) / "knowledge" / "ug-ee" / Path(rel)
    if not base.is_dir():
        return []
    units: list[dict[str, str]] = []
    for child in sorted(base.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            title = child.name.replace("-", " ")
            units.append({"id": child.name, "title": title})
    return units


def expand_topics(subject: dict[str, Any], cwd: Path | None = None) -> list[dict[str, Any]]:
    """Return explicit topics, or expand from COVERAGE / elective folders."""
    if subject.get("topics") is not None and "units_from" not in subject:
        return list(subject.get("topics") or [])
    units_from = subject.get("units_from")
    if not units_from:
        return list(subject.get("topics") or [])
    recipe_map = subject.get("topic_recipes") or {}
    slice_ids = subject.get("units")
    if str(units_from).startswith("electives/"):
        units = _elective_units(cwd, str(units_from))
    else:
        cov = _load_coverage_units(cwd)
        units = list(cov.get(str(units_from), []))
    if slice_ids:
        allow = set(slice_ids)
        units = [u for u in units if u["id"] in allow]
    topics: list[dict[str, Any]] = []
    for u in units:
        topics.append(
            {
                "id": u["id"],
                "title": u["title"],
                "anchor": "",
                "recipes": list(recipe_map.get(u["id"]) or []),
                "labs": [],
            }
        )
    return topics


def validate(
    data: dict[str, Any] | None = None,
    *,
    cwd: Path | None = None,
) -> list[str]:
    """Return a list of validation errors (empty = ok)."""
    errors: list[str] = []
    raw = data if data is not None else load_curriculum(cwd)
    if raw.get("schema") != "arc.curriculum.v1":
        errors.append("schema must be arc.curriculum.v1")
    known = set(list_workflow_ids(cwd))
    subject_ids: set[str] = set()
    for sem in raw.get("semesters") or []:
        n = sem.get("n")
        if not isinstance(n, int) or not 1 <= n <= 8:
            errors.append(f"invalid semester n={n!r}")
        for subj in sem.get("subjects") or []:
            sid = subj.get("id")
            if not sid:
                errors.append(f"semester {n}: subject missing id")
                continue
            if sid in subject_ids:
                errors.append(f"duplicate subject id {sid}")
            subject_ids.add(sid)
            src = subj.get("source")
            if src not in {"provided", "inferred"}:
                errors.append(f"{sid}: source must be provided|inferred")
            pack = subj.get("pack")
            if pack is not None and pack not in _PACK_IDS:
                errors.append(f"{sid}: unknown pack {pack!r}")
            topic_ids: set[str] = set()
            for topic in expand_topics(subj, cwd):
                tid = topic.get("id")
                if not tid:
                    errors.append(f"{sid}: topic missing id")
                    continue
                if tid in topic_ids:
                    errors.append(f"{sid}: duplicate topic {tid}")
                topic_ids.add(tid)
                for rid in topic.get("recipes") or []:
                    if rid not in known:
                        errors.append(f"{sid}/{tid}: unknown recipe {rid}")
                for lab in topic.get("labs") or []:
                    if lab not in _LAB_IDS:
                        errors.append(f"{sid}/{tid}: unknown lab {lab}")
    return errors
