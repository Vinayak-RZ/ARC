"""Forward-path grid layout for studio diagrams (ponytail: one chain heuristic)."""

from __future__ import annotations

from typing import Any

BLOCK_W = 96
PID_W = 144
BLOCK_H = 56
GAP = 32
GRID = 8
ORIGIN_X = 56
ORIGIN_Y = 96
PORT_RAIL_CENTER_Y = ORIGIN_Y + BLOCK_H / 2
SUM_W = 56


def _snap(value: float) -> float:
    return round(value / GRID) * GRID


def _block_height(_btype: str) -> float:
    return float(BLOCK_H)


def _block_width(btype: str) -> float:
    if btype == "sum":
        return float(SUM_W)
    if btype == "pid":
        return float(PID_W)
    return float(BLOCK_W)


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
    placed: set[str] = set()
    for bid in order:
        b = by_id.get(bid)
        if not b:
            continue
        btype = b.get("type")
        h = _block_height(btype)
        b["x"] = _snap(float(x))
        b["y"] = _snap(float(PORT_RAIL_CENTER_Y - h / 2))
        placed.add(bid)
        span = _block_width(btype)
        x += int(span) + GAP
    for b in blocks:
        if b["id"] not in placed:
            b["x"] = _snap(float(x))
            b["y"] = _snap(float(PORT_RAIL_CENTER_Y - BLOCK_H / 2))
            x += BLOCK_W + GAP
    out = dict(diagram)
    out["blocks"] = blocks
    return out
