"""MCP tools for shared circuit lab on workflow runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import GraphError, default_graph_for
from electrical_engineer.circuit.run_session import add_part, apply_graph, connect_ports, load_graph
from electrical_engineer.circuit.simulate_graph import simulate_graph
from electrical_engineer.collab import lab_meta
from electrical_engineer.collab.workflow import finish_circuit_lab
from electrical_engineer.runner.runs import create_run_dir, new_run_id, project_root

TOOL_DEFS: list[dict[str, Any]] = [
    {
        "name": "arc_circuit_lab_open",
        "description": "Open or create a circuit lab artifact on a run (seeds graph from problem when provided).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string"},
                "problem": {"type": "object"},
            },
        },
    },
    {
        "name": "arc_circuit_lab_set_graph",
        "description": "Replace the full arc.circuit.v1 graph on a run.",
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}, "graph": {"type": "object"}},
            "required": ["run_id", "graph"],
        },
    },
    {
        "name": "arc_circuit_lab_add_part",
        "description": "Add one part to the run circuit graph.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string"},
                "id": {"type": "string"},
                "type": {"type": "string"},
                "value": {},
                "unit": {"type": "string"},
                "x": {"type": "number"},
                "y": {"type": "number"},
            },
            "required": ["run_id", "id", "type"],
        },
    },
    {
        "name": "arc_circuit_lab_connect",
        "description": "Connect two ports on the run circuit graph.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string"},
                "edge_id": {"type": "string"},
                "from": {"type": "string"},
                "to": {"type": "string"},
            },
            "required": ["run_id", "from", "to"],
        },
    },
    {
        "name": "arc_circuit_lab_simulate",
        "description": "Compile graph to SPICE and simulate (ngspice when available).",
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}, "problem": {"type": "object"}},
            "required": ["run_id"],
        },
    },
    {
        "name": "arc_circuit_lab_finish_solve",
        "description": "Seed lab from problem, simulate, verify-after-derive.",
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}, "problem": {"type": "object"}},
            "required": ["run_id", "problem"],
        },
    },
    {
        "name": "arc_circuit_lab_re_derive",
        "description": "Re-run agent derivation for the current lab graph and refresh verify.",
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}},
            "required": ["run_id"],
        },
    },
    {
        "name": "arc_circuit_lab_get",
        "description": "Read graph, lab_meta, and last simulation on a run.",
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}},
            "required": ["run_id"],
        },
    },
]


def _run_dir(run_id: str | None, root: Path) -> Path:
    rid = str(run_id or new_run_id())
    d = root / "runs" / rid
    if not d.is_dir():
        create_run_dir(root, rid)
    return d


def handle_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    root = project_root()
    try:
        if name == "arc_circuit_lab_open":
            run_dir = _run_dir(args.get("run_id"), root)
            problem = dict(args.get("problem") or {})
            lab_meta.ensure_lab_meta(run_dir, kind="circuit")
            graph = default_graph_for(problem)
            if graph:
                apply_graph(run_dir, graph, author="agent", op="open", detail=problem.get("kind"))
            meta = lab_meta.load_lab_meta(run_dir)
            return {
                "run_id": run_dir.name,
                "ui_url": lab_meta.ui_lab_url(run_dir.name, meta),
                "graph": load_graph(run_dir),
                "lab_meta": meta,
                "waits": False,
            }
        if name == "arc_circuit_lab_set_graph":
            run_dir = _run_dir(args["run_id"], root)
            out = apply_graph(run_dir, args["graph"], author="agent", op="set_graph")
            return {**out, "waits": False}
        if name == "arc_circuit_lab_add_part":
            run_dir = _run_dir(args["run_id"], root)
            part = {
                "id": args["id"],
                "type": args["type"],
                "value": args.get("value"),
                "unit": args.get("unit"),
                "x": args.get("x"),
                "y": args.get("y"),
            }
            out = add_part(run_dir, part, author="agent")
            return {**out, "waits": False}
        if name == "arc_circuit_lab_connect":
            run_dir = _run_dir(args["run_id"], root)
            edge = {"id": args.get("edge_id"), "from": args["from"], "to": args["to"]}
            out = connect_ports(run_dir, edge, author="agent")
            return {**out, "waits": False}
        if name == "arc_circuit_lab_simulate":
            run_dir = _run_dir(args["run_id"], root)
            problem = dict(args.get("problem") or {})
            graph = load_graph(run_dir)
            sim = simulate_graph(graph, problem, run_dir=run_dir)
            return {"run_id": run_dir.name, **sim, "waits": False}
        if name == "arc_circuit_lab_finish_solve":
            run_dir = _run_dir(args.get("run_id"), root)
            verify = finish_circuit_lab(run_dir, dict(args["problem"]))
            meta = lab_meta.load_lab_meta(run_dir)
            return {
                "run_id": run_dir.name,
                "ui_url": meta.get("ui_url"),
                "verify": verify,
                "mismatch": verify.get("mismatch"),
                "waits": False,
            }
        if name == "arc_circuit_lab_re_derive":
            run_dir = _run_dir(args["run_id"], root)
            from electrical_engineer.collab.lab_verify import agent_rederive_circuit_lab

            verify = agent_rederive_circuit_lab(run_dir)
            meta = lab_meta.load_lab_meta(run_dir)
            return {"run_id": run_dir.name, "verify": verify, "lab_meta": meta, "waits": False}
        if name == "arc_circuit_lab_get":
            run_dir = _run_dir(args["run_id"], root)
            meta = lab_meta.load_lab_meta(run_dir)
            sim_path = run_dir / "lab_simulate.json"
            verify_path = run_dir / "lab_verify.json"
            payload: dict[str, Any] = {
                "run_id": run_dir.name,
                "graph": load_graph(run_dir),
                "lab_meta": meta,
                "waits": False,
            }
            if sim_path.is_file():
                payload["lab_simulate"] = json.loads(sim_path.read_text(encoding="utf-8"))
            if verify_path.is_file():
                payload["lab_verify"] = json.loads(verify_path.read_text(encoding="utf-8"))
            return payload
    except GraphError as exc:
        return {"error": str(exc), "waits": False}
    return {"error": f"unknown lab tool {name}", "waits": False}