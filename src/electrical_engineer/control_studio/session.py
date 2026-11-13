"""Persistent studio sessions with operation log and undo."""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from electrical_engineer.control_studio.schema import StudioError, empty_diagram, parse_diagram
from electrical_engineer.runner.runs import project_root


def _studio_dir(root: Path | None = None) -> Path:
    d = (root or project_root()) / ".electrical-engineer" / "control_studio"
    d.mkdir(parents=True, exist_ok=True)
    return d


def new_session_id() -> str:
    return f"cs-{uuid.uuid4().hex[:12]}"


def session_path(session_id: str, root: Path | None = None) -> Path:
    sid = "".join(c for c in session_id if c.isalnum() or c in "-_")
    return _studio_dir(root) / f"{sid}.json"


def load_session(session_id: str, root: Path | None = None) -> dict[str, Any]:
    path = session_path(session_id, root)
    if not path.is_file():
        raise StudioError(f"unknown session {session_id}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise StudioError("corrupt session file")
    return data


def save_session(session_id: str, payload: dict[str, Any], root: Path | None = None) -> None:
    path = session_path(session_id, root)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    try:
        from electrical_engineer.ui_server.studio_events import publish

        publish(
            session_id,
            {
                "type": "session",
                "revision": payload.get("revision"),
                "presence": payload.get("presence"),
                "last_op": (payload.get("op_log") or [])[-1:] if payload.get("op_log") else [],
            },
        )
    except ImportError:
        pass


def create_session(
    title: str = "Control Studio",
    root: Path | None = None,
    *,
    golden: str | None = None,
) -> dict[str, Any]:
    from electrical_engineer.control_studio.goldens import GOLDENS

    sid = new_session_id()
    diagram = empty_diagram(title)
    if golden and golden in GOLDENS:
        diagram = parse_diagram(GOLDENS[golden]())
        diagram["title"] = title
        if golden not in ("pid_dc_motor", "unity_first_order"):
            diagram = auto_layout(diagram)
    payload = {
        "session_id": sid,
        "revision": 0,
        "diagram": diagram,
        "op_log": [],
        "undo_stack": [],
        "redo_stack": [],
        "presence": {"agent_editing": False, "last_author": "system", "highlight_until_ms": 0},
        "updated_at_ms": int(time.time() * 1000),
    }
    if diagram.get("blocks"):
        payload["undo_stack"] = [json.loads(json.dumps(diagram))]
    _append_op(
        payload,
        {"op": "create", "target": golden or "blank", "detail": {"title": title}},
        "agent" if golden else "human",
    )
    save_session(sid, payload, root)
    return payload


def list_sessions(root: Path | None = None, *, limit: int = 12) -> list[dict[str, Any]]:
    d = _studio_dir(root)
    items: list[dict[str, Any]] = []
    if not d.is_dir():
        return items
    for path in sorted(d.glob("cs-*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        diagram = data.get("diagram") or {}
        title = str(diagram.get("title") or data.get("session_id"))
        if title.startswith("unmatched") or "scratch" in title.lower():
            continue
        items.append(
            {
                "session_id": data.get("session_id") or path.stem,
                "title": title,
                "revision": data.get("revision") or 0,
                "updated_at_ms": data.get("updated_at_ms") or 0,
            }
        )
        if len(items) >= limit:
            break
    return items


def _append_op(payload: dict[str, Any], op: dict[str, Any], author: str) -> dict[str, Any]:
    entry = {
        "id": f"op-{len(payload.get('op_log') or []) + 1}",
        "ts_ms": int(time.time() * 1000),
        "author": author if author in ("human", "agent") else "agent",
        **op,
    }
    payload.setdefault("op_log", []).append(entry)
    payload["revision"] = int(payload.get("revision") or 0) + 1
    payload["updated_at_ms"] = entry["ts_ms"]
    snapshot = json.loads(json.dumps(payload.get("diagram")))
    payload.setdefault("undo_stack", []).append(snapshot)
    payload["redo_stack"] = []
    if len(payload["undo_stack"]) > 64:
        payload["undo_stack"] = payload["undo_stack"][-64:]
    return entry


def apply_diagram(
    session_id: str,
    diagram: dict[str, Any],
    *,
    author: str,
    op: str,
    target: str | None = None,
    detail: dict[str, Any] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    payload = load_session(session_id, root)
    parsed = parse_diagram(diagram)
    payload["diagram"] = parsed
    body: dict[str, Any] = {"op": op, "target": target}
    if detail:
        body["detail"] = detail
    entry = _append_op(payload, body, author)
    presence = payload.setdefault(
        "presence",
        {"agent_editing": False, "last_author": author, "highlight_until_ms": 0},
    )
    presence["last_author"] = author
    presence["agent_editing"] = author == "agent"
    presence["highlight_until_ms"] = int(time.time() * 1000) + (4000 if author == "agent" else 1500)
    if author == "agent":
        presence["agent_editing_until_ms"] = int(time.time() * 1000) + 8000
    else:
        presence["agent_editing"] = False
    save_session(session_id, payload, root)
    return {
        "session_id": session_id,
        "revision": payload["revision"],
        "diagram": parsed,
        "last_op": entry,
        "presence": presence,
    }


def add_note(
    session_id: str,
    block_id: str,
    text: str,
    *,
    author: str = "human",
    root: Path | None = None,
) -> dict[str, Any]:
    payload = load_session(session_id, root)
    diagram = payload["diagram"]
    note = {
        "id": f"note-{len(diagram.get('notes') or []) + 1}",
        "block_id": block_id,
        "text": text,
        "author": author if author in ("human", "agent") else "human",
        "ts_ms": int(time.time() * 1000),
    }
    diagram.setdefault("notes", []).append(note)
    return apply_diagram(session_id, diagram, author=author, op="add_note", root=root)


def undo(session_id: str, *, author: str = "human", root: Path | None = None) -> dict[str, Any]:
    payload = load_session(session_id, root)
    stack = payload.get("undo_stack") or []
    if len(stack) < 2:
        raise StudioError("nothing to undo")
    current = stack.pop()
    payload.setdefault("redo_stack", []).append(current)
    payload["diagram"] = stack[-1]
    payload["revision"] = int(payload.get("revision") or 0) + 1
    _append_op(payload, {"op": "undo"}, author)
    save_session(session_id, payload, root)
    return {"session_id": session_id, "diagram": payload["diagram"], "revision": payload["revision"]}


def redo(session_id: str, *, author: str = "human", root: Path | None = None) -> dict[str, Any]:
    payload = load_session(session_id, root)
    rstack = payload.get("redo_stack") or []
    if not rstack:
        raise StudioError("nothing to redo")
    restored = rstack.pop()
    payload["diagram"] = restored
    payload.setdefault("undo_stack", []).append(restored)
    payload["revision"] = int(payload.get("revision") or 0) + 1
    _append_op(payload, {"op": "redo"}, author)
    save_session(session_id, payload, root)
    return {"session_id": session_id, "diagram": payload["diagram"], "revision": payload["revision"]}


def auto_layout(diagram: dict[str, Any]) -> dict[str, Any]:
    d = parse_diagram(diagram)
    x0, y0 = 80, 120
    dx = 180
    row = 0
    for i, b in enumerate(d["blocks"]):
        b["x"] = x0 + (i % 4) * dx
        b["y"] = y0 + row * 120
        if (i + 1) % 4 == 0:
            row += 1
    d["blocks"] = d["blocks"]
    return d


def add_block(diagram: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
    d = parse_diagram(diagram)
    d["blocks"].append(block)
    return parse_diagram(d)


def connect(diagram: dict[str, Any], wire: dict[str, Any]) -> dict[str, Any]:
    d = parse_diagram(diagram)
    d["wires"].append(wire)
    return parse_diagram(d)


def set_param(diagram: dict[str, Any], block_id: str, params: dict[str, Any]) -> dict[str, Any]:
    d = parse_diagram(diagram)
    for b in d["blocks"]:
        if b["id"] == block_id:
            b["params"] = {**(b.get("params") or {}), **params}
            break
    else:
        raise StudioError(f"block {block_id} missing")
    return parse_diagram(d)
