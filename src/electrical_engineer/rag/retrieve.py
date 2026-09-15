"""Hybrid BM25+dense retrieve with parent hydrate and typed graph hops."""

from __future__ import annotations

import time
from pathlib import Path

from electrical_engineer.rag.graph_store import load_graph, neighbors
from electrical_engineer.rag.hybrid import bm25_scores, dense_scores, rrf_fuse
from electrical_engineer.rag.inventory import listed_inventory, rag_root
from electrical_engineer.rag.ontology import (
    ENGINE_ID,
    HOP_EDGES,
    MAX_HOPS,
    MAX_PASSAGES,
    PASSAGE_CHARS,
    RETRIEVE_BUDGET_S,
    T1_KINDS,
    T2_KINDS,
)
from electrical_engineer.runner.runs import project_root


def _read_text(rec: dict, cwd: Path | None) -> str:
    raw = rec.get("path") or ""
    p = Path(raw)
    if not p.is_absolute():
        root = project_root(cwd)
        for cand in (root / raw, rag_root(cwd) / raw):
            if cand.is_file():
                p = cand
                break
    if p.is_file():
        return p.read_text(errors="replace")
    return ""


def _inventory_index(cwd: Path | None) -> list[dict]:
    return listed_inventory(cwd)


def _passage_from_node(
    graph: dict,
    node_id: str,
    inventory_by_node: dict[str, dict],
    cwd: Path | None,
) -> dict | None:
    node = (graph.get("nodes") or {}).get(node_id) or {}
    kind = node.get("kind")
    if kind in T2_KINDS:
        return None
    rec = inventory_by_node.get(node_id)
    if rec:
        text = _read_text(rec, cwd)
        return {
            **rec,
            "text": text[:PASSAGE_CHARS],
            "node_id": node_id,
            "graph_kind": kind,
        }
    preview = str(node.get("text_preview") or node.get("caption") or node.get("name") or "")
    if not preview and kind == "figure":
        preview = f"[figure] {node.get('path') or node_id} {node.get('caption') or ''}"
    if not preview:
        return None
    return {
        "node_id": node_id,
        "text": preview[:PASSAGE_CHARS],
        "book_id": node.get("book_id"),
        "chapter_id": node.get("chapter_id"),
        "page": node.get("page"),
        "graph_kind": kind,
        "path": node.get("path"),
    }


def _hydrate_and_hop(
    graph: dict,
    seed_ids: list[str],
    inventory_by_node: dict[str, dict],
    cwd: Path | None,
    *,
    hops: int,
    deadline: float,
) -> list[dict]:
    hops = max(0, min(int(hops), MAX_HOPS))
    seen: set[str] = set()
    frontier = list(seed_ids)
    passages: list[dict] = []

    for seed in seed_ids:
        # attach worked_example / figure_group siblings at hop 0 hydrate
        for et, other in neighbors(graph, seed, edge_types=HOP_EDGES):
            if et == "part_of_example":
                frontier.append(other)
            node = (graph.get("nodes") or {}).get(other) or {}
            if node.get("kind") in T2_KINDS:
                for et2, child in neighbors(graph, other, edge_types=HOP_EDGES):
                    if et2 in {"part_of_example", "illustrates", "caption_of", "belongs_to"}:
                        frontier.append(child)

    depth = 0
    while frontier and depth <= hops:
        if time.monotonic() > deadline:
            break
        nxt: list[str] = []
        for nid in frontier:
            if nid in seen:
                continue
            seen.add(nid)
            node = (graph.get("nodes") or {}).get(nid) or {}
            kind = node.get("kind")
            if kind in T1_KINDS or kind == "figure" or nid in inventory_by_node:
                pas = _passage_from_node(graph, nid, inventory_by_node, cwd)
                if pas:
                    passages.append(pas)
            if depth < hops:
                for _et, other in neighbors(graph, nid, edge_types=HOP_EDGES):
                    if other not in seen:
                        nxt.append(other)
        frontier = nxt
        depth += 1
    return passages


def retrieve(
    filters: dict | None = None,
    *,
    query: str = "",
    cwd: Path | None = None,
    hops: int = 1,
) -> dict:
    t0 = time.monotonic()
    deadline = t0 + RETRIEVE_BUDGET_S
    filters = {k: v for k, v in (filters or {}).items() if v}
    records = []
    for rec in _inventory_index(cwd):
        if any(rec.get(k) != v for k, v in filters.items()):
            continue
        records.append(rec)

    texts = [_read_text(r, cwd) for r in records]
    seed_indices: list[int] = []
    if query and records:
        bm = bm25_scores(query, texts)
        dens = dense_scores(query, texts)
        bm_rank = sorted(range(len(records)), key=lambda i: -bm[i])
        dens_rank = sorted(range(len(records)), key=lambda i: -dens[i])
        fused = rrf_fuse([bm_rank, dens_rank])
        # drop zero-ish lexical+dense misses when query present
        seed_indices = [
            idx
            for idx, _score in fused
            if bm[idx] > 0 or dens[idx] > 0.05
        ][:12]
        if not seed_indices:
            # fall back to top fused even if weak — empty handled later
            seed_indices = [idx for idx, _ in fused[:3]]
    else:
        seed_indices = list(range(min(3, len(records))))

    inventory_by_node = {
        str(r["node_id"]): r for r in records if r.get("node_id")
    }
    # Seed inventory rows without node_id still participate
    seed_ids: list[str] = []
    for idx in seed_indices:
        rec = records[idx]
        nid = rec.get("node_id")
        if nid:
            seed_ids.append(str(nid))
        else:
            # synthetic id so hydrate can still emit passage
            seed_ids.append(f"inv:{idx}")
            inventory_by_node[f"inv:{idx}"] = rec

    root = rag_root(cwd)
    graph = load_graph(root)
    # Ensure seed inventory rows without graph nodes still return passages
    for sid in seed_ids:
        if sid.startswith("inv:") and sid not in (graph.get("nodes") or {}):
            rec = inventory_by_node[sid]
            passages_direct = {
                **rec,
                "text": _read_text(rec, cwd)[:PASSAGE_CHARS],
                "node_id": sid,
                "score": 1,
            }
            inventory_by_node[sid] = passages_direct

    hopped = _hydrate_and_hop(
        graph,
        seed_ids,
        inventory_by_node,
        cwd,
        hops=hops,
        deadline=deadline,
    )

    # Always include direct seed passages first (stable for OER tests)
    hits: list[dict] = []
    seen_paths: set[str] = set()
    for idx in seed_indices[:MAX_PASSAGES]:
        rec = records[idx]
        text = _read_text(rec, cwd)[:PASSAGE_CHARS]
        key = str(rec.get("path") or rec.get("node_id") or idx)
        if key in seen_paths:
            continue
        seen_paths.add(key)
        hits.append({**rec, "text": text, "score": len(seed_indices) - len(hits)})
    for pas in hopped:
        key = str(pas.get("path") or pas.get("node_id"))
        if key in seen_paths:
            continue
        if filters and any(
            pas.get(k) not in (None, v) and pas.get(k) != v for k, v in filters.items()
        ):
            # allow figure/entity expansions without chapter sometimes — keep if book matches
            if filters.get("book_id") and pas.get("book_id") not in (None, filters["book_id"]):
                continue
            if filters.get("chapter_id") and pas.get("chapter_id") not in (
                None,
                filters["chapter_id"],
            ) and pas.get("graph_kind") not in {"figure", "entity", "proposition"}:
                continue
        seen_paths.add(key)
        hits.append({**pas, "score": pas.get("score", 0)})
        if len(hits) >= MAX_PASSAGES + 2:
            break
    hits = hits[:MAX_PASSAGES]
    elapsed_ms = int((time.monotonic() - t0) * 1000)
    truncated = time.monotonic() > deadline
    return {
        "passages": hits,
        "empty": len(hits) == 0,
        "filters": filters,
        "engine": ENGINE_ID,
        "elapsed_ms": elapsed_ms,
        "truncated": truncated,
        "hops": hops,
    }
