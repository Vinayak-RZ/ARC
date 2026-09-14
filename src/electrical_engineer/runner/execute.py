"""Run a named YAML recipe into an isolated run dir."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import electrical_engineer.nodes  # noqa: F401  register activities
from electrical_engineer.capabilities import DEFAULT_BIND, rebind_recipe
from electrical_engineer.catalog import load_recipe
from electrical_engineer.circuit.graph import default_graph_for, write_graph
from electrical_engineer.circuit.title import run_title
from electrical_engineer.nodes.registry import REGISTRY
from electrical_engineer.runner.fsm import Recipe, run_fsm
from electrical_engineer.runner.runs import create_run_dir, new_run_id, node_dir, project_root
from electrical_engineer.unchecked import UNCHECKED

_UNCHECKED_REASONS = (
    "no-provider",
    "sim-exhausted",
    "unmatched",
    "empty-retrieve",
    "gate-closed",
)
_REVERSE_BIND = {v: k for k, v in DEFAULT_BIND.items()}


def execute(
    recipe_id: str,
    *,
    cwd: Path | None = None,
    run_root: Path | None = None,
    problem: dict[str, Any] | None = None,
    allow_all: bool = False,
    recipe: Recipe | None = None,
) -> dict[str, Any]:
    del allow_all  # gates still apply inside nodes; EE_ALLOW_ALL is env-only
    root = project_root(cwd)
    loaded = recipe if recipe is not None else load_recipe(recipe_id, cwd)
    recipe = rebind_recipe(loaded)
    run_id = new_run_id()
    run_dir = create_run_dir(run_root or root, run_id)
    if problem:
        (run_dir / "problem.json").write_text(json.dumps(problem))
    elif (Path.cwd() / "problem.json").is_file():
        problem = json.loads((Path.cwd() / "problem.json").read_text())
        (run_dir / "problem.json").write_text(json.dumps(problem))

    def wrap(fn):
        def inner(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
            payload = {
                **spec,
                "run_dir": str(run_dir),
                "recipe_id": recipe.id,
                "problem": problem or {},
            }
            out = fn(payload, inputs)
            nd = node_dir(run_dir, spec["id"])
            (nd / "out.json").write_text(json.dumps(out, default=str))
            return out

        return inner

    completed = run_fsm(recipe, {name: wrap(fn) for name, fn in REGISTRY.items()})
    summary_node = completed.get("summary") or next(reversed(completed.values()))
    caps, provs, verifier = _ids(recipe, completed)
    payload = {
        "recipe_id": recipe.id,
        "run_id": run_id,
        "title": run_title(recipe.id, problem),
        "unchecked": bool(summary_node.get("unchecked")),
        "token": summary_node.get("token"),
        "value": summary_node.get("value"),
        "paths": summary_node.get("paths") or [],
        "citations": summary_node.get("citations") or [],
        "nodes": {
            k: {"unchecked": v.get("unchecked"), "ok": v.get("ok")} for k, v in completed.items()
        },
        "verifier": verifier,
        "values": {},
        "artifact_paths": list(summary_node.get("paths") or []),
    }
    if payload["unchecked"] and payload.get("token") is None:
        payload["token"] = UNCHECKED
    if not payload["unchecked"]:
        for v in completed.values():
            if isinstance(v, dict) and v.get("value") is not None:
                payload["value"] = v.get("value")
    payload["values"] = {
        "value": UNCHECKED if payload["unchecked"] else payload.get("value"),
    }
    reason = _unchecked_reason(recipe.id, completed, payload)
    observation = {
        "run_id": run_id,
        "capabilities": caps,
        "providers": provs,
        "nodes": payload["nodes"],
        "unchecked_reason": reason,
        "retrieve": _retrieve_seed(completed),
    }
    blob = json.dumps(payload, indent=2)
    (run_dir / "evidentiary.json").write_text(blob)
    (run_dir / "summary.json").write_text(blob)
    (run_dir / "observation.json").write_text(json.dumps(observation, indent=2))
    seed = default_graph_for(problem)
    if seed is not None and not (run_dir / "graph.json").is_file():
        write_graph(run_dir, seed)
    return {"run_id": run_id, "run_dir": str(run_dir), "summary": payload, "observation": observation}


def _ids(recipe, completed: dict[str, Any]) -> tuple[list[str], list[str], str]:
    caps: list[str] = []
    provs: list[str] = []
    for spec in recipe.nodes.values():
        provs.append(spec.activity)
        cap = spec.extras.get("capability") or _REVERSE_BIND.get(spec.activity)
        if cap:
            caps.append(str(cap))
    for v in completed.values():
        if isinstance(v, dict) and v.get("capability"):
            caps.append(str(v["capability"]))
    caps = sorted(set(caps))
    provs = sorted(set(provs))
    if not caps or not provs:
        verifier = "none"
    else:
        verifier = f"{caps[0]} via {provs[0]}"
    return caps, provs, verifier


def _retrieve_seed(completed: dict[str, Any]) -> dict[str, Any]:
    for v in completed.values():
        if isinstance(v, dict) and ("passages" in v or "empty" in v):
            return {
                "empty": bool(v.get("empty")),
                "filters": v.get("filters") or {},
                "citations": v.get("citations") or [],
            }
    return {"empty": True, "filters": {}, "citations": []}


def _unchecked_reason(recipe_id: str, completed: dict[str, Any], payload: dict[str, Any]) -> str | None:
    if not payload.get("unchecked"):
        return None
    for v in completed.values():
        if isinstance(v, dict) and v.get("cannot_do") == "CD-NO-PROVIDER":
            return "no-provider"
    for v in completed.values():
        if isinstance(v, dict) and v.get("exhausted"):
            return "sim-exhausted"
    if "unmatched" in recipe_id:
        return "unmatched"
    for v in completed.values():
        if isinstance(v, dict) and v.get("empty") is True:
            return "empty-retrieve"
    for v in completed.values():
        if isinstance(v, dict) and v.get("error") in {"unconfirmed", "gate"}:
            return "gate-closed"
    fallback = "unmatched"
    return fallback if fallback in _UNCHECKED_REASONS else None
