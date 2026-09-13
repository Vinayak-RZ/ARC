"""RAG inventory. Untrusted ingest; metadata owned by EE."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.rag.ingest import chunk_text, extract, write_index
from electrical_engineer.runner.runs import project_root


def rag_root(cwd: Path | None = None) -> Path:
    d = project_root(cwd) / ".electrical-engineer" / "rag"
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


def add_doc(path: str, *, tags: dict | None = None, cwd: Path | None = None) -> dict:
    items = load_inventory(cwd)
    src = Path(path)
    if not src.is_file():
        for cand in (project_root(cwd) / path, rag_root(cwd) / path):
            if cand.is_file():
                src = cand
                break
    text = extract(src)
    chunks = chunk_text(text)
    root = rag_root(cwd)
    chunk_dir = root / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    base = {
        "book_id": (tags or {}).get("book_id"),
        "chapter_id": (tags or {}).get("chapter_id"),
        "folder_tag": (tags or {}).get("folder_tag"),
        "domain_tag": (tags or {}).get("domain_tag"),
        "licence_tag": (tags or {}).get("licence_tag"),
        "untrusted": True,
        "source": path,
    }
    index_recs: list[dict] = []
    last: dict | None = None
    bodies = chunks or [text]
    for i, body in enumerate(bodies):
        dest = chunk_dir / f"{src.stem}-{i}.txt"
        dest.write_text(body)
        rec = {**base, "path": str(dest), "page": i + 1, "chunk_id": i}
        items.append(rec)
        index_recs.append({"path": str(dest), "page": i + 1, "source": path})
        last = rec
    save_inventory(items, cwd)
    write_index(root, index_recs)
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
