"""Append-safe graph.json under the RAG root."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.rag.ontology import valid_edge, valid_node


def graph_path(root: Path) -> Path:
    return root / "graph.json"


def load_graph(root: Path) -> dict:
    path = graph_path(root)
    if not path.is_file():
        return {"nodes": {}, "edges": []}
    return json.loads(path.read_text())


def save_graph(graph: dict, root: Path) -> None:
    graph_path(root).write_text(json.dumps(graph, indent=2))


def upsert_node(graph: dict, node_id: str, kind: str, **meta: object) -> None:
    if not valid_node(kind):
        raise ValueError(f"unknown node kind: {kind}")
    nodes = graph.setdefault("nodes", {})
    prev = dict(nodes.get(node_id) or {})
    prev.update(meta)
    prev["id"] = node_id
    prev["kind"] = kind
    nodes[node_id] = prev


def add_edge(
    graph: dict,
    *,
    edge_type: str,
    src: str,
    dst: str,
) -> None:
    if not valid_edge(edge_type):
        raise ValueError(f"unknown edge type: {edge_type}")
    edges = graph.setdefault("edges", [])
    rec = {"type": edge_type, "src": src, "dst": dst}
    if rec not in edges:
        edges.append(rec)


def neighbors(
    graph: dict,
    node_id: str,
    *,
    edge_types: set[str] | frozenset[str] | None = None,
    undirected: bool = True,
) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for e in graph.get("edges") or []:
        et = str(e.get("type") or "")
        if edge_types is not None and et not in edge_types:
            continue
        if e.get("src") == node_id:
            out.append((et, str(e["dst"])))
        elif undirected and e.get("dst") == node_id:
            out.append((et, str(e["src"])))
    return out
