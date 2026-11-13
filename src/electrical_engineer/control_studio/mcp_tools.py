"""MCP tool defs and handlers for Control Studio."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.control_studio import analyze as analyze_mod
from electrical_engineer.control_studio import session as session_mod
from electrical_engineer.control_studio import simulate as simulate_mod
from electrical_engineer.control_studio.library import PALETTE
from electrical_engineer.control_studio.schema import StudioError, empty_diagram, parse_diagram
from electrical_engineer.control_studio.validate import validate
from electrical_engineer.runner.runs import project_root

TOOL_DEFS: list[dict[str, Any]] = [
    {
        "name": "control_studio_create_diagram",
        "description": "Create a Control Studio session and optional seed diagram.",
        "inputSchema": {
            "type": "object",
            "properties": {"title": {"type": "string"}, "session_id": {"type": "string"}},
        },
    },
    {
        "name": "control_studio_add_block",
        "description": "Add a block to a studio session diagram.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "block_id": {"type": "string"},
                "type": {"type": "string"},
                "params": {"type": "object"},
                "x": {"type": "number"},
                "y": {"type": "number"},
            },
            "required": ["session_id", "block_id", "type"],
        },
    },
    {
        "name": "control_studio_connect",
        "description": "Wire two ports in a studio session.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "wire_id": {"type": "string"},
                "from": {"type": "string"},
                "to": {"type": "string"},
            },
            "required": ["session_id", "from", "to"],
        },
    },
    {
        "name": "control_studio_set_param",
        "description": "Merge parameters on a block (e.g. PID Kp).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "block_id": {"type": "string"},
                "params": {"type": "object"},
            },
            "required": ["session_id", "block_id", "params"],
        },
    },
    {
        "name": "control_studio_remove",
        "description": "Remove a block or wire by id.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "block_id": {"type": "string"},
                "wire_id": {"type": "string"},
            },
            "required": ["session_id"],
        },
    },
    {
        "name": "control_studio_auto_layout",
        "description": "Apply grid auto-layout to blocks.",
        "inputSchema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    {
        "name": "control_studio_validate",
        "description": "Validate wiring, loops, and Arc traps.",
        "inputSchema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    {
        "name": "control_studio_simulate",
        "description": "Time-domain step/impulse via python-control.",
        "inputSchema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    {
        "name": "control_studio_analyze",
        "description": "Bode, Nyquist, root locus, margins for assembled diagram.",
        "inputSchema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    {
        "name": "control_studio_export",
        "description": "Export diagram JSON and revision metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}, "path": {"type": "string"}},
            "required": ["session_id"],
        },
    },
]


def _load_diagram(session_id: str) -> tuple[str, dict[str, Any]]:
    payload = session_mod.load_session(session_id)
    return session_id, payload["diagram"]


def _save(session_id: str, diagram: dict[str, Any], op: str) -> dict[str, Any]:
    return session_mod.apply_diagram(session_id, diagram, author="agent", op=op)


def handle_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.ui_server.app import ui_page_url

    try:
        if name == "control_studio_create_diagram":
            title = str(args.get("title") or "Control Studio")
            if args.get("session_id"):
                sid = str(args["session_id"])
                payload = session_mod.load_session(sid)
            else:
                payload = session_mod.create_session(title)
                sid = payload["session_id"]
            if args.get("seed_diagram"):
                payload = session_mod.apply_diagram(sid, args["seed_diagram"], author="agent", op="seed")
            return {
                "session_id": sid,
                "ui_url": f"{ui_page_url()}?view=control-studio&session={sid}",
                "palette": PALETTE,
                "diagram": payload.get("diagram") or empty_diagram(title),
                "waits": False,
            }
        if name == "control_studio_add_block":
            sid = str(args["session_id"])
            _, diagram = _load_diagram(sid)
            block = {
                "id": str(args["block_id"]),
                "type": str(args["type"]),
                "params": dict(args.get("params") or {}),
                "x": float(args.get("x") or 120),
                "y": float(args.get("y") or 120),
            }
            diagram = session_mod.add_block(diagram, block)
            out = _save(sid, diagram, "add_block")
            return {**out, "waits": False}
        if name == "control_studio_connect":
            sid = str(args["session_id"])
            _, diagram = _load_diagram(sid)
            wire = {
                "id": str(args.get("wire_id") or f"w-{len(diagram.get('wires') or [])+1}"),
                "from": str(args["from"]),
                "to": str(args["to"]),
            }
            diagram = session_mod.connect(diagram, wire)
            out = _save(sid, diagram, "connect")
            return {**out, "waits": False}
        if name == "control_studio_set_param":
            sid = str(args["session_id"])
            _, diagram = _load_diagram(sid)
            diagram = session_mod.set_param(diagram, str(args["block_id"]), dict(args.get("params") or {}))
            out = _save(sid, diagram, "set_param")
            return {**out, "waits": False}
        if name == "control_studio_remove":
            sid = str(args["session_id"])
            payload = session_mod.load_session(sid)
            diagram = payload["diagram"]
            if args.get("block_id"):
                bid = str(args["block_id"])
                diagram["blocks"] = [b for b in diagram["blocks"] if b["id"] != bid]
                diagram["wires"] = [
                    w for w in diagram["wires"] if not w["from"].startswith(f"{bid}:") and not w["to"].startswith(f"{bid}:")
                ]
            if args.get("wire_id"):
                wid = str(args["wire_id"])
                diagram["wires"] = [w for w in diagram["wires"] if w["id"] != wid]
            diagram = parse_diagram(diagram)
            out = _save(sid, diagram, "remove")
            return {**out, "waits": False}
        if name == "control_studio_auto_layout":
            sid = str(args["session_id"])
            _, diagram = _load_diagram(sid)
            diagram = session_mod.auto_layout(diagram)
            out = _save(sid, diagram, "auto_layout")
            return {**out, "waits": False}
        if name == "control_studio_validate":
            sid = str(args["session_id"])
            _, diagram = _load_diagram(sid)
            return {**validate(diagram), "session_id": sid, "waits": False}
        if name == "control_studio_simulate":
            sid = str(args["session_id"])
            _, diagram = _load_diagram(sid)
            run_dir = project_root() / "runs" / sid
            return {**simulate_mod.simulate(diagram, run_dir=run_dir), "session_id": sid, "waits": False}
        if name == "control_studio_analyze":
            sid = str(args["session_id"])
            _, diagram = _load_diagram(sid)
            run_dir = project_root() / "runs" / sid
            return {**analyze_mod.analyze(diagram, run_dir=run_dir), "session_id": sid, "waits": False}
        if name == "control_studio_export":
            sid = str(args["session_id"])
            payload = session_mod.load_session(sid)
            path = args.get("path")
            if path:
                dest = Path(path)
                dest.write_text(json.dumps(payload["diagram"], indent=2), encoding="utf-8")
            return {
                "session_id": sid,
                "diagram": payload["diagram"],
                "revision": payload.get("revision"),
                "op_log": payload.get("op_log"),
                "waits": False,
            }
    except StudioError as exc:
        return {"error": str(exc), "waits": False}
    return {"error": f"unknown control studio tool {name}", "waits": False}
