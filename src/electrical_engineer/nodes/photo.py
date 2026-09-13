"""Photo-to-netlist stages. Confirm does not simulate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.nodes.registry import register
from electrical_engineer.unchecked import UNCHECKED


def _problem(spec: dict[str, Any]) -> dict[str, Any]:
    p = spec.get("problem")
    if isinstance(p, dict) and p:
        return p
    run_dir = spec.get("run_dir")
    if run_dir:
        path = Path(run_dir) / "problem.json"
        if path.is_file():
            return json.loads(path.read_text())
    return {}


@register("detect-components")
def detect_components(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    return {"components": [], "confidence": 0.0, "low_confidence": True, **inputs}


@register("connect-wires")
def connect_wires(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    return {"wires": [], **inputs}


@register("ocr-labels")
def ocr_labels(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    return {"labels": [], "low_confidence": True, **inputs}


@register("draft-netlist")
def draft_netlist(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    cir = "* draft\n"
    graph = {"nodes": [], "edges": []}
    run_dir = spec.get("run_dir")
    if run_dir:
        Path(run_dir, "draft.cir").write_text(cir)
        Path(run_dir, "graph.json").write_text(json.dumps(graph))
    return {"cir": cir, "graph": graph, **inputs}


@register("confirm-topology")
def confirm_topology(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    run_dir = spec.get("run_dir")
    confirmed = False
    if run_dir and Path(run_dir, "confirmed.json").is_file():
        confirmed = True
    return {"confirmed": confirmed, "simulate": False, **inputs}


@register("retrieve-passage")
def retrieve_passage(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    try:
        from electrical_engineer.rag.retrieve import retrieve
    except ImportError:
        return {"passages": [], "empty": True}
    problem = _problem(spec)
    filters = problem.get("filters") or spec.get("filters") or {}
    query = str(problem.get("query") or problem.get("task") or "")
    out = retrieve(filters, query=query)
    citations = [
        {
            "book_id": p.get("book_id"),
            "chapter_id": p.get("chapter_id"),
            "page": p.get("page"),
        }
        for p in out.get("passages") or []
    ]
    return {**out, "citations": citations}


@register("solve-explain")
def solve_explain(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    problem = _problem(spec)
    passages = []
    citations = []
    for v in inputs.values():
        if isinstance(v, dict):
            passages.extend(v.get("passages") or [])
            citations.extend(v.get("citations") or [])
    value = _solve_value(problem)
    bits = [p.get("text", "")[:400] for p in passages[:3]]
    cited = " ".join(bits)
    if value is not None:
        # FR9: argument-band fallback must never mint unchecked: false.
        return {
            "text": f"value={value}\n{cited}",
            "value": value,
            "unchecked": True,
            "token": UNCHECKED,
            "law": problem.get("kind") or "numeric",
            "citations": citations,
        }
    from electrical_engineer.local_llm.client import complete

    prompt = f"Explain using only these passages:\n{cited}\n\nQuestion: {problem.get('query') or problem}"
    llm = complete(prompt)
    llm_text = None if llm.get("skipped") else llm.get("text")
    return {
        "text": llm_text or UNCHECKED,
        "unchecked": True,
        "token": UNCHECKED,
        "citations": citations,
    }


def _solve_value(problem: dict[str, Any]) -> float | None:
    kind = str(problem.get("kind") or "")
    if kind == "ohms_law" and "v" in problem and "r" in problem:
        r = float(problem["r"])
        if r == 0:
            return None
        return float(problem["v"]) / r
    if {"vin", "r1", "r2"} <= set(problem) or kind == "voltage_divider":
        r1, r2 = float(problem["r1"]), float(problem["r2"])
        if r1 + r2 == 0:
            return None
        return float(problem["vin"]) * r2 / (r1 + r2)
    if kind == "symbolic":
        try:
            import sympy as sp
        except ImportError:
            return None
        try:
            return float(sp.sympify(str(problem.get("expr", "0"))))
        except (TypeError, ValueError, SyntaxError, AttributeError):
            return None
    return None


@register("ask-human")
def ask_human(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    return {"asked": True, "waiting": True}


@register("run-recipe")
def run_recipe(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    return {"child": inputs.get("recipe_id") or _spec.get("child"), "paths": []}
