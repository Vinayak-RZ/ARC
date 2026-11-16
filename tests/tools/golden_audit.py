"""Emit golden→derived contamination candidates for TEST_REPORT (read-only scan)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path("/opt/cursor/artifacts/golden-audit.json")
PATTERNS = (
    re.compile(r'"value"\s*:\s*[\d.]+', re.MULTILINE),
    re.compile(r"declared_gold", re.MULTILINE),
    re.compile(r"derived_value", re.MULTILINE),
    re.compile(r"expected\s*[:=]", re.MULTILINE),
)


def main() -> None:
    rows: list[dict] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT))
        if any(skip in rel for skip in (".git", "node_modules", ".venv", "ui/dist", "mutants")):
            continue
        if path.suffix not in {".py", ".yaml", ".json", ".js", ".ts"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if not any(p.search(text) for p in PATTERNS):
            continue
        if "golden" not in text.lower() and "derived" not in text.lower() and "declared_gold" not in text:
            continue
        rows.append({"path": rel, "bytes": len(text)})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"candidates": rows, "count": len(rows)}, indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({len(rows)} candidates)")


if __name__ == "__main__":
    main()