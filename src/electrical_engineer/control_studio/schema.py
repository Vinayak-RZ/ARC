"""Parse and normalize arc.control_studio.v1 diagrams."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_CONTRACT = json.loads(
    Path(__file__).with_name("arc.control_studio.v1.json").read_text(encoding="utf-8")
)
SCHEMA = str(_CONTRACT["properties"]["schema"]["const"])
BLOCK_TYPES = frozenset(_CONTRACT["$defs"]["blockType"]["enum"])
MAX_BLOCKS = int(_CONTRACT["properties"]["blocks"]["maxItems"])
MAX_WIRES = int(_CONTRACT["properties"]["wires"]["maxItems"])


class StudioError(ValueError):
    pass


def parse_diagram(data: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise StudioError("diagram must be an object")
    if data.get("schema") and data.get("schema") != SCHEMA:
        raise StudioError(f"unsupported schema {data.get('schema')}")
    blocks = data.get("blocks") or []
    wires = data.get("wires") or []
    if not isinstance(blocks, list) or not isinstance(wires, list):
        raise StudioError("blocks and wires must be lists")
    if len(blocks) > MAX_BLOCKS:
        raise StudioError(f"at most {MAX_BLOCKS} blocks")
    if len(wires) > MAX_WIRES:
        raise StudioError(f"at most {MAX_WIRES} wires")
    seen: set[str] = set()
    norm_blocks: list[dict[str, Any]] = []
    for b in blocks:
        if not isinstance(b, dict):
            raise StudioError("block must be an object")
        bid = str(b.get("id") or "").strip()
        if not bid or bid in seen:
            raise StudioError("block id required and unique")
        seen.add(bid)
        btype = str(b.get("type") or "")
        if btype not in BLOCK_TYPES:
            raise StudioError(f"unsupported block type {btype}")
        norm_blocks.append({**b, "id": bid, "type": btype, "params": dict(b.get("params") or {})})
    norm_wires: list[dict[str, Any]] = []
    wseen: set[str] = set()
    by_id = {b["id"]: b for b in norm_blocks}
    for w in wires:
        if not isinstance(w, dict):
            raise StudioError("wire must be an object")
        wid = str(w.get("id") or "")
        if not wid or wid in wseen:
            raise StudioError("wire id required and unique")
        wseen.add(wid)
        fr = str(w.get("from") or "")
        to = str(w.get("to") or "")
        if ":" not in fr or ":" not in to:
            raise StudioError("wire endpoints use block:port")
        f_bid = fr.split(":", 1)[0]
        t_bid = to.split(":", 1)[0]
        if f_bid not in by_id or t_bid not in by_id:
            raise StudioError(f"wire references unknown block: {wid}")
        norm_wires.append({"id": wid, "from": fr, "to": to})
    out: dict[str, Any] = {
        "schema": SCHEMA,
        "id": str(data.get("id") or "diagram"),
        "title": str(data.get("title") or "Control diagram"),
        "blocks": norm_blocks,
        "wires": norm_wires,
        "notes": list(data.get("notes") or []),
        "meta": dict(data.get("meta") or {}),
    }
    return out


def empty_diagram(title: str = "New control diagram") -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "id": "new",
        "title": title,
        "blocks": [],
        "wires": [],
        "notes": [],
        "meta": {},
    }
