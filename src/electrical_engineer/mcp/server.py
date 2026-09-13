"""JSON-RPC MCP stdio. Never waits on humans. 5–7 always-on verbs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from electrical_engineer.capabilities import CapabilityError, bind
from electrical_engineer.catalog import list_workflow_ids
from electrical_engineer.compose.graph import ComposeError, compose
from electrical_engineer.rag.retrieve import retrieve
from electrical_engineer.runner.fsm import parse_recipe
from electrical_engineer.runner.runs import create_run_dir, new_run_id, project_root
from electrical_engineer.unchecked import UNCHECKED

ASK_ON_MCP = {"photo-to-netlist", "compose-from-parts", "control-diagram-to-model"}
HOST_ATTACHMENTS = frozenset(
    {
        "simulate-circuit",
        "unmatched-cosolver",
        "derive-circuit",
    }
)

TOOLS = [
    {
        "name": "list_workflows",
        "description": "List named workflow ids",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "retrieve",
        "description": "Retrieve cited passages; empty is visible",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "book_id": {"type": "string"},
                "chapter_id": {"type": "string"},
                "domain_tag": {"type": "string"},
            },
        },
    },
    {
        "name": "open_ui",
        "description": "Return localhost UI URL. clarify alias. Never waits.",
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}, "prompt": {"type": "string"}},
        },
    },
    {
        "name": "simulate_attachment",
        "description": "Run a short host-path attachment id. Never waits.",
        "inputSchema": {
            "type": "object",
            "properties": {"attachment_id": {"type": "string"}, "workflow_id": {"type": "string"}},
            "required": ["attachment_id"],
        },
    },
    {
        "name": "propose_composition",
        "description": "Validate capability graph; apply false records plan.md. Returns run_id+paths.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nodes": {"type": "object"},
                "edges": {"type": "array"},
                "id": {"type": "string"},
                "apply": {"type": "boolean"},
            },
        },
    },
    {
        "name": "label",
        "description": "Read evidentiary summary for a run. summary alias.",
        "inputSchema": {
            "type": "object",
            "properties": {"run_id": {"type": "string"}},
            "required": ["run_id"],
        },
    },
    {
        "name": "run_workflow",
        "description": "Eval/CLI rollback for a named YAML id. Never waits.",
        "inputSchema": {
            "type": "object",
            "properties": {"workflow_id": {"type": "string"}},
            "required": ["workflow_id"],
        },
    },
]


def fail_closed(run_id: str | None = None) -> dict[str, Any]:
    from electrical_engineer.ui_server.app import ui_page_url

    hint = "electrical-engineer ui" + (f" --run {run_id}" if run_id else "")
    return {
        "error": "gate_would_wait",
        "ui_url": ui_page_url(run_id),
        "cli_hint": hint,
        "waits": False,
    }


def _ok(payload: dict[str, Any], *, error: bool = False) -> dict[str, Any]:
    body: dict[str, Any] = {
        "content": [{"type": "text", "text": json.dumps(payload)}],
    }
    if error:
        body["isError"] = True
    return body


def _plan_md(data: dict[str, Any]) -> str:
    nodes = data.get("nodes") or {}
    ids = [
        str(body.get("capability") or body.get("activity") or body.get("uses") or "")
        for body in nodes.values()
        if isinstance(body, dict)
    ]
    listed = ", ".join(x for x in ids if x) or "(none)"
    return (
        "# Job plan\n"
        "Given / Find: host composition\n"
        f"Packs: (at most two)\n"
        f"Attachments or capability ids: {listed}\n"
        "What stays unchecked: missing providers or unmatched ports\n"
    )


def _graph_recipe(data: dict[str, Any]):
    compose(data)
    edges = data.get("edges") or []
    recipe_nodes: dict[str, Any] = {}
    for nid, body in (data.get("nodes") or {}).items():
        needs = [e["from"] for e in edges if e.get("to") == nid]
        raw = body.get("activity") or body.get("uses") or body.get("capability")
        bound = bind(str(raw))
        node = {"activity": bound.provider, "needs": needs}
        if bound.capability:
            node["capability"] = bound.capability
        if bound.no_provider:
            node["cannot_do"] = bound.cannot_do
        recipe_nodes[nid] = node
    return parse_recipe({"id": data.get("id", "composed"), "nodes": recipe_nodes})


def handle(method: str, params: dict[str, Any] | None) -> Any:
    params = params or {}
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "electrical-engineer", "version": "0.1.0"},
            "capabilities": {"tools": {}},
        }
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        if name == "list_workflows":
            return _ok({"workflows": list_workflow_ids(), "waits": False})
        if name == "retrieve":
            filters = {
                k: args[k]
                for k in ("book_id", "chapter_id", "domain_tag", "folder_tag")
                if args.get(k)
            }
            out = retrieve(filters, query=str(args.get("query") or ""))
            out["waits"] = False
            return _ok(out)
        if name in {"open_ui", "clarify"}:
            from electrical_engineer.ui_server.app import ui_page_url

            rid = args.get("run_id")
            return _ok(
                {
                    "ui_url": ui_page_url(str(rid) if rid else None),
                    "waits": False,
                    "prompt": args.get("prompt") or "",
                }
            )
        if name == "simulate_attachment":
            wid = str(args.get("attachment_id") or args.get("workflow_id") or "")
            if wid in ASK_ON_MCP:
                return _ok(fail_closed(), error=True)
            if wid not in HOST_ATTACHMENTS:
                return _ok(
                    {
                        "error": "not_a_short_attachment",
                        "waits": False,
                        "cli_hint": "electrical-engineer run <id>",
                    },
                    error=True,
                )
            from electrical_engineer.runner.execute import execute

            result = execute(wid)
            return _ok(
                {
                    "run_id": result["run_id"],
                    "paths": [
                        str(Path(result["run_dir"]) / "evidentiary.json"),
                        str(Path(result["run_dir"]) / "observation.json"),
                    ],
                    "waits": False,
                    "status": "started",
                }
            )
        if name == "propose_composition":
            apply = bool(args.get("apply"))
            graph = {
                "id": args.get("id") or "composed",
                "nodes": args.get("nodes") or {},
                "edges": args.get("edges") or [],
            }
            try:
                compose(graph)
            except (ComposeError, CapabilityError) as exc:
                return _ok({"error": str(exc), "waits": False}, error=True)
            if not apply:
                run_id = new_run_id()
                run_dir = create_run_dir(project_root(), run_id)
                plan_path = run_dir / "plan.md"
                plan_path.write_text(_plan_md(graph))
                return _ok(
                    {
                        "run_id": run_id,
                        "paths": [str(plan_path)],
                        "applied": False,
                        "waits": False,
                    }
                )
            from electrical_engineer.runner.execute import execute

            result = execute(str(graph.get("id") or "composed"), recipe=_graph_recipe(graph))
            plan_path = Path(result["run_dir"]) / "plan.md"
            plan_path.write_text(_plan_md(graph))
            evid = Path(result["run_dir"]) / "evidentiary.json"
            return _ok(
                {
                    "run_id": result["run_id"],
                    "paths": [str(evid), str(Path(result["run_dir"]) / "observation.json"), str(plan_path)],
                    "applied": True,
                    "waits": False,
                }
            )
        if name in {"label", "summary"}:
            rid = str(args.get("run_id") or "")
            path = project_root() / "runs" / rid / "evidentiary.json"
            alias = project_root() / "runs" / rid / "summary.json"
            target = path if path.is_file() else alias
            if not target.is_file():
                return _ok({"error": "missing", "token": UNCHECKED, "waits": False}, error=True)
            data = json.loads(target.read_text())
            data["waits"] = False
            return _ok(data)
        if name == "run_workflow":
            wid = str(args.get("workflow_id") or "")
            if wid in ASK_ON_MCP:
                return _ok(fail_closed(), error=True)
            from electrical_engineer.runner.execute import execute

            result = execute(wid)
            return _ok(
                {
                    "workflow_id": wid,
                    "waits": False,
                    "status": "started",
                    "run_id": result["run_id"],
                    "paths": [str(Path(result["run_dir"]) / "evidentiary.json")],
                }
            )
        return _ok({"error": f"unknown tool {name}", "waits": False}, error=True)
    if method == "notifications/initialized":
        return None
    raise ValueError(method)


def serve(stdin=None, stdout=None) -> None:
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        result = handle(msg.get("method", ""), msg.get("params"))
        if "id" in msg:
            stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": result}) + "\n")
            stdout.flush()
