"""Forward-path grid layout for studio diagrams (ponytail: one chain heuristic)."""

from __future__ import annotations

from typing import Any

BLOCK_W = 132
BLOCK_H = 64
GAP = 44
ORIGIN_X = 56
ORIGIN_Y = 96


def _forward_order(diagram: dict[str, Any]) -> list[str]:
    blocks = {b["id"]: b for b in diagram.get("blocks") or []}
    wires = diagram.get("wires") or []
    outs: dict[str, list[str]] = {}
    ins_count: dict[str, int] = {bid: 0 for bid in blocks}
    for w in wires:
        if str(w.get("to", "")).endswith(":feedback"):
            continue
        fb = w["from"].split(":", 1)[0]
        tb = w["to"].split(":", 1)[0]
        outs.setdefault(fb, []).append(tb)
        ins_count[tb] = ins_count.get(tb, 0) + 1
    starts = [bid for bid, b in blocks.items() if b.get("type") in ("step", "ramp", "sine") and ins_count.get(bid, 0) == 0]
    if not starts:
        starts = [bid for bid, n in ins_count.items() if n == 0]
    order: list[str] = []
    seen: set[str] = set()

    def walk(bid: str) -> None:
        if bid in seen or bid not in blocks:
            return
        seen.add(bid)
        order.append(bid)
        for nxt in outs.get(bid, []):
            walk(nxt)

    for s in starts:
        walk(s)
    for bid in blocks:
        if bid not in seen:
            order.append(bid)
    return order


def layout_chain(diagram: dict[str, Any]) -> dict[str, Any]:
    """Place blocks on a horizontal grid with GAP between BOXes."""
    blocks = list(diagram.get("blocks") or [])
    by_id = {b["id"]: b for b in blocks}
    order = _forward_order(diagram)
    x = ORIGIN_X
    y_stack = ORIGIN_Y
    placed: set[str] = set()
    for bid in order:
        b = by_id.get(bid)
        if not b:
            continue
        btype = b.get("type")
        b["x"] = float(x)
        if btype == "sum":
            b["y"] = float(y_stack)
        else:
            b["y"] = float(y_stack)
        placed.add(bid)
        span = 56 if btype == "sum" else BLOCK_W
        x += span + GAP
    for b in blocks:
        if b["id"] not in placed:
            b["x"] = float(x)
            b["y"] = float(y_stack + 48)
            x += BLOCK_W + GAP
    out = dict(diagram)
    out["blocks"] = blocks
    return out
