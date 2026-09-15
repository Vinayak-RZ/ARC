"""RAG inventory. Untrusted ingest; metadata owned by EE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from electrical_engineer.rag.graph_store import add_edge, load_graph, save_graph, upsert_node
from electrical_engineer.rag.ingest import (
    chunk_text,
    light_entities,
    split_worked_example,
    write_index,
)
from electrical_engineer.rag.parse import parse_document
from electrical_engineer.runner.runs import project_root


def rag_root(cwd: Path | None = None) -> Path:
    d = project_root(cwd) / ".electrical-engineer" / "rag"
    d.mkdir(parents=True, exist_ok=True)
    return d


def corpus_dir(cwd: Path | None = None) -> Path:
    env = os.environ.get("EE_CORPUS_DIR")
    if env:
        p = Path(env)
        if not p.is_absolute():
            p = project_root(cwd) / p
        p.mkdir(parents=True, exist_ok=True)
        return p
    d = project_root(cwd) / ".electrical-engineer" / "corpus"
    d.mkdir(parents=True, exist_ok=True)
    return d


def inventory_path(cwd: Path | None = None) -> Path:
    return rag_root(cwd) / "inventory.json"


def load_inventory(cwd: Path | None = None) -> list[dict]:
    path = inventory_path(cwd)
    if not path.is_file():
        return []
    return json.loads(path.read_text())


def seed_inventory(cwd: Path | None = None) -> list[dict]:
    man = project_root(cwd) / "eval" / "fixtures" / "oer" / "manifest.json"
    if not man.is_file():
        return []
    data = json.loads(man.read_text())
    return list(data.get("items") or [])


def listed_inventory(cwd: Path | None = None) -> list[dict]:
    return [*seed_inventory(cwd), *load_inventory(cwd)]


def save_inventory(items: list[dict], cwd: Path | None = None) -> None:
    inventory_path(cwd).write_text(json.dumps(items, indent=2))


def _stable_id(*parts: object) -> str:
    raw = "|".join(str(p) for p in parts)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def add_doc(path: str, *, tags: dict | None = None, cwd: Path | None = None) -> dict:
    items = load_inventory(cwd)
    src = Path(path)
    if not src.is_file():
        for cand in (project_root(cwd) / path, rag_root(cwd) / path, corpus_dir(cwd) / path):
            if cand.is_file():
                src = cand
                break
    parsed = parse_document(src)
    text = parsed.text
    chunks = chunk_text(text)
    root = rag_root(cwd)
    chunk_dir = root / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    tags = tags or {}
    book_id = tags.get("book_id") or "unknown"
    chapter_id = tags.get("chapter_id")
    base = {
        "book_id": book_id,
        "chapter_id": chapter_id,
        "folder_tag": tags.get("folder_tag"),
        "domain_tag": tags.get("domain_tag"),
        "licence_tag": tags.get("licence_tag"),
        "untrusted": True,
        "source": path,
        "low_confidence": parsed.low_confidence,
        "parse_provider": parsed.provider,
    }
    graph = load_graph(root)
    book_node = f"book:{book_id}"
    upsert_node(graph, book_node, "book", title=book_id)
    chapter_node = None
    if chapter_id:
        chapter_node = f"chapter:{book_id}:{chapter_id}"
        upsert_node(graph, chapter_node, "chapter", book_id=book_id, chapter_id=chapter_id)
        add_edge(graph, edge_type="belongs_to", src=chapter_node, dst=book_node)

    index_recs: list[dict] = []
    last: dict | None = None
    bodies = chunks or [text]
    chunk_ids: list[str] = []
    for i, body in enumerate(bodies):
        dest = chunk_dir / f"{src.stem}-{i}.txt"
        dest.write_text(body)
        cid = _stable_id(path, i, body[:64])
        node_id = f"chunk:{cid}"
        kind = "prose"
        q, sol = split_worked_example(body)
        if q and sol:
            kind = "question"
        rec = {
            **base,
            "path": str(dest),
            "page": i + 1,
            "chunk_id": i,
            "node_id": node_id,
            "chunk_kind": kind,
        }
        items.append(rec)
        index_recs.append({"path": str(dest), "page": i + 1, "source": path, "node_id": node_id})
        upsert_node(
            graph,
            node_id,
            kind if kind in {"question", "prose"} else "prose",
            path=str(dest),
            book_id=book_id,
            chapter_id=chapter_id,
            page=i + 1,
            text_preview=body[:240],
        )
        if chapter_node:
            add_edge(graph, edge_type="belongs_to", src=node_id, dst=chapter_node)
        else:
            add_edge(graph, edge_type="belongs_to", src=node_id, dst=book_node)
        chunk_ids.append(node_id)
        if q and sol:
            ex_id = f"example:{_stable_id(path, i)}"
            upsert_node(graph, ex_id, "worked_example", book_id=book_id, chapter_id=chapter_id)
            add_edge(graph, edge_type="part_of_example", src=node_id, dst=ex_id)
            sol_cid = _stable_id(path, i, "sol")
            sol_node = f"chunk:{sol_cid}"
            sol_dest = chunk_dir / f"{src.stem}-{i}-sol.txt"
            sol_dest.write_text(sol)
            upsert_node(
                graph,
                sol_node,
                "solution_step",
                path=str(sol_dest),
                book_id=book_id,
                chapter_id=chapter_id,
            )
            add_edge(graph, edge_type="part_of_example", src=sol_node, dst=ex_id)
            items.append(
                {
                    **base,
                    "path": str(sol_dest),
                    "page": i + 1,
                    "chunk_id": f"{i}-sol",
                    "node_id": sol_node,
                    "chunk_kind": "solution_step",
                }
            )
            index_recs.append(
                {"path": str(sol_dest), "page": i + 1, "source": path, "node_id": sol_node}
            )
        for ent in light_entities(body):
            eid = f"entity:{_stable_id(ent.lower())}"
            upsert_node(graph, eid, "entity", name=ent)
            add_edge(graph, edge_type="mentions", src=node_id, dst=eid)
            prop = f"prop:{_stable_id(ent.lower(), body[:40])}"
            upsert_node(graph, prop, "proposition", text=ent, source_chunk=node_id)
            add_edge(graph, edge_type="states", src=prop, dst=node_id)
            add_edge(graph, edge_type="mentions", src=prop, dst=eid)
        last = rec

    for fi, fig in enumerate(parsed.figures):
        fid = f"figure:{_stable_id(path, fi, fig.path)}"
        upsert_node(
            graph,
            fid,
            "figure",
            path=fig.path,
            caption=fig.caption,
            page=fig.page,
            ocr_text=fig.ocr_text,
            low_confidence=fig.low_confidence,
        )
        group = f"figure_group:{_stable_id(path, 'figs')}"
        upsert_node(graph, group, "figure_group", book_id=book_id)
        add_edge(graph, edge_type="belongs_to", src=fid, dst=group)
        if chunk_ids:
            add_edge(graph, edge_type="illustrates", src=fid, dst=chunk_ids[0])
        if fig.caption:
            cap_id = f"chunk:{_stable_id(path, 'cap', fi)}"
            cap_dest = chunk_dir / f"{src.stem}-cap-{fi}.txt"
            cap_dest.write_text(fig.caption)
            upsert_node(graph, cap_id, "caption", path=str(cap_dest), figure_id=fid)
            add_edge(graph, edge_type="caption_of", src=cap_id, dst=fid)
            items.append(
                {
                    **base,
                    "path": str(cap_dest),
                    "page": fig.page or 1,
                    "chunk_id": f"cap-{fi}",
                    "node_id": cap_id,
                    "chunk_kind": "caption",
                }
            )

    save_inventory(items, cwd)
    write_index(root, index_recs)
    save_graph(graph, root)
    assert last is not None
    return last


def tag_doc(path: str, tags: dict, cwd: Path | None = None) -> dict | None:
    items = load_inventory(cwd)
    hit = None
    for rec in items:
        if rec.get("path") == path or rec.get("source") == path:
            rec.update({k: v for k, v in tags.items() if v is not None})
            hit = rec
    if hit is not None:
        save_inventory(items, cwd)
    return hit
