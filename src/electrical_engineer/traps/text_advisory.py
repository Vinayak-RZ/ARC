"""Negation-aware text advisories (never fail alone)."""

from __future__ import annotations

import re


def _negated_before(text: str, start: int) -> bool:
    window = text[max(0, start - 48) : start].lower()
    return bool(
        re.search(
            r"(?:did\s+not|don't|do\s+not|never|not|without|no)\s+(?:use\s+)?$",
            window,
        )
        or re.search(r"note:\s*agc\s+does\s+not", window)
    )


def find_advisory(text: str, pattern: re.Pattern[str]) -> str | None:
    for m in pattern.finditer(text):
        if not _negated_before(text, m.start()):
            return m.group(0)
    return None
