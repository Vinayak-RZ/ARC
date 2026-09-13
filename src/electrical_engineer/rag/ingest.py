"""BYO extract → chunk → index. Licence-clean text in CI; PDFs stay on the student machine."""

from __future__ import annotations

import json
from pathlib import Path

CHUNK_CHARS = 1500


def extract(path: Path) -> str:
    if not path.is_file():
        return ""
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            return path.read_text(errors="replace")
        pages = []
        for i, page in enumerate(PdfReader(str(path)).pages, start=1):
            pages.append(f"[page {i}]\n{page.extract_text() or ''}")
        return "\n".join(pages)
    return path.read_text(errors="replace")


def chunk_text(text: str, *, size: int = CHUNK_CHARS) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= size:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += size
    return chunks


def write_index(root: Path, records: list[dict]) -> None:
    path = root / "index.json"
    existing: list[dict] = []
    if path.is_file():
        existing = json.loads(path.read_text())
    path.write_text(json.dumps([*existing, *records], indent=2))
