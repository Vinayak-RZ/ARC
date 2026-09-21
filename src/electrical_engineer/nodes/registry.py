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


def _nested_payloads(node: dict[str, Any]) -> list[Any]:
    inner = node.get("inputs")
    if isinstance(inner, dict):
        return list(inner.values())
    return []


def _walk_checked(inputs: Mapping[str, Any]) -> bool:
    """True when an upstream verifier (including through explain nodes) produced a checked value."""
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        if v.get("ok") is True and (v.get("value") is not None or v.get("tool")):
            return True
        if v.get("unchecked") is False and v.get("value") is not None:
            return True
        frontier.extend(_nested_payloads(v))
    return False


def _first_checked_value(inputs: Mapping[str, Any]) -> Any:
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        if v.get("ok") is True and v.get("value") is not None:
            return v.get("value")
        if v.get("unchecked") is False and v.get("value") is not None:
            return v.get("value")
        frontier.extend(_nested_payloads(v))
    return None


@register("label-unchecked")
def label_unchecked(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    extra = {}
    if _spec.get("cannot_do"):
        extra["cannot_do"] = _spec["cannot_do"]
    if _spec.get("capability"):
        extra["capability"] = _spec["capability"]
    if _walk_checked(inputs):
        value = _first_checked_value(inputs)
        return {"unchecked": False, "token": None, "value": value, "inputs": inputs, **extra}
    return {"unchecked": True, "token": UNCHECKED, "inputs": inputs, **extra}


@register("write-run-summary")
def write_run_summary(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    checked = _walk_checked(inputs)
    value = _first_checked_value(inputs) if checked else None
    paths: list[str] = []
    citations: list[Any] = []
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        paths.extend(v.get("paths") or [])
        citations.extend(v.get("citations") or [])
        frontier.extend(_nested_payloads(v))
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
