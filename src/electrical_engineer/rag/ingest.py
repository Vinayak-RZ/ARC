"""BYO extract → chunk → index. Licence-clean text in CI; PDFs stay on the student machine."""

from __future__ import annotations

import json
import re
from pathlib import Path

from electrical_engineer.rag.parse import parse_document

CHUNK_CHARS = 1500

_EXAMPLE_HEAD = re.compile(
    r"(?im)^(#{2,3}\s*)?(worked\s+example|example|problem|exercise)\b.*"
)
_SOLUTION_HEAD = re.compile(r"(?im)^(#{2,3}\s*)?(solution|answer)\b.*")


def extract(path: Path) -> str:
    return parse_document(path).text


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


def split_worked_example(text: str) -> tuple[str | None, str | None]:
    """Return (question, solution) spans when headings look like a worked example."""
    lines = text.splitlines()
    q_start = s_start = None
    for i, line in enumerate(lines):
        if q_start is None and _EXAMPLE_HEAD.match(line.strip()):
            q_start = i
        elif q_start is not None and s_start is None and _SOLUTION_HEAD.match(line.strip()):
            s_start = i
            break
    if q_start is None:
        return None, None
    if s_start is None:
        return "\n".join(lines[q_start:]), None
    return "\n".join(lines[q_start:s_start]), "\n".join(lines[s_start:])


def light_entities(text: str) -> list[str]:
    """Heuristic EE symbols / law names — no LLM (COST)."""
    found: list[str] = []
    for pat in (
        r"\bOhm(?:'s)?\s+law\b",
        r"\bKVL\b",
        r"\bKCL\b",
        r"\bKirchhoff\w*\b",
        r"\bThevenin\w*\b",
        r"\bNorton\w*\b",
        r"\b[Vv]\s*=\s*[Ii]\s*[Rr]\b",
    ):
        for m in re.finditer(pat, text, flags=re.I):
            found.append(m.group(0))
    # de-dupe preserve order
    seen: set[str] = set()
    out: list[str] = []
    for f in found:
        key = f.lower()
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out
