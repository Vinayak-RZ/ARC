"""Registered EE activity nodes. Bodies fail closed except label/summary."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from electrical_engineer.unchecked import UNCHECKED

Activity = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]

REGISTRY: dict[str, Activity] = {}


def register(name: str) -> Callable[[Activity], Activity]:
    def wrap(fn: Activity) -> Activity:
        REGISTRY[name] = fn
        return fn

    return wrap


def _walk_checked(inputs: Mapping[str, Any]) -> bool:
    """True when a direct child node verified a number. Do not recurse into echoed inputs."""
    for v in inputs.values():
        if not isinstance(v, dict):
            continue
        if v.get("unchecked"):
            continue
        if v.get("ok") is True or (v.get("unchecked") is False and v.get("value") is not None):
            return True
    return False


@register("label-unchecked")
def label_unchecked(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    extra = {}
    if _spec.get("cannot_do"):
        extra["cannot_do"] = _spec["cannot_do"]
    if _spec.get("capability"):
        extra["capability"] = _spec["capability"]
    if _walk_checked(inputs):
        value = None
        for v in inputs.values():
            if isinstance(v, dict) and v.get("value") is not None:
                value = v.get("value")
        return {"unchecked": False, "token": None, "value": value, "inputs": inputs, **extra}
    return {"unchecked": True, "token": UNCHECKED, "inputs": inputs, **extra}


@register("write-run-summary")
def write_run_summary(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    checked = _walk_checked(inputs)
    value = None
    paths: list[str] = []
    citations: list[Any] = []
    for v in inputs.values():
        if not isinstance(v, dict):
            continue
        if v.get("value") is not None:
            value = v.get("value")
        paths.extend(v.get("paths") or [])
        citations.extend(v.get("citations") or [])
    out = {
        "recipe_id": _spec.get("recipe_id", ""),
        "unchecked": not checked,
        "token": None if checked else UNCHECKED,
        "value": value,
        "paths": paths,
        "citations": citations,
    }
    run_dir = _spec.get("run_dir")
    if run_dir:
        Path(run_dir, "summary.json").write_text(json.dumps(out, indent=2))
        out["paths"] = [*paths, str(Path(run_dir) / "summary.json")]
    return out


def get(name: str) -> Activity:
    if name not in REGISTRY:
        raise KeyError(name)
    return REGISTRY[name]


def names() -> list[str]:
    return sorted(REGISTRY)
