"""HTTP fetch helpers for the builtin web-verify provider."""

from __future__ import annotations

import re
from io import BytesIO
from typing import Any


def fetch_text(url: str, *, timeout_s: float = 30.0) -> tuple[int, str]:
    import httpx

    with httpx.Client(follow_redirects=True, timeout=timeout_s) as client:
        resp = client.get(url, headers={"User-Agent": "Arc-web-verify/1.0"})
        body = resp.text if "text" in (resp.headers.get("content-type") or "").lower() else ""
        if not body and resp.content:
            body = _pdf_text(resp.content) or ""
        return resp.status_code, body


def _pdf_text(data: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        reader = PdfReader(BytesIO(data))
        parts: list[str] = []
        for page in reader.pages[:8]:
            parts.append(page.extract_text() or "")
        return "\n".join(parts)
    except (OSError, ValueError, TypeError, AttributeError):
        return ""


def brave_search(query: str, api_key: str, *, count: int = 5) -> list[dict[str, Any]]:
    import httpx

    with httpx.Client(timeout=30.0) as client:
        resp = client.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "count": count},
            headers={"Accept": "application/json", "X-Subscription-Token": api_key},
        )
        resp.raise_for_status()
        data = resp.json()
    out: list[dict[str, Any]] = []
    for item in (data.get("web") or {}).get("results") or []:
        out.append(
            {
                "url": item.get("url"),
                "title": item.get("title"),
                "snippet": item.get("description") or "",
                "domain": _domain(item.get("url") or ""),
            }
        )
    return out


def tavily_search(query: str, api_key: str, *, max_results: int = 5) -> list[dict[str, Any]]:
    import httpx

    with httpx.Client(timeout=30.0) as client:
        resp = client.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "max_results": max_results},
        )
        resp.raise_for_status()
        data = resp.json()
    return [
        {
            "url": r.get("url"),
            "title": r.get("title"),
            "snippet": r.get("content") or "",
            "domain": _domain(r.get("url") or ""),
        }
        for r in data.get("results") or []
    ]


def _domain(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url)
    return (m.group(1) if m else "").lower().replace("www.", "")
