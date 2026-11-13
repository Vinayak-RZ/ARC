"""Builtin web search (Brave or Tavily) plus direct URL fetch."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.web_verify.config import WebVerifyConfig
from electrical_engineer.web_verify.fetch import brave_search, fetch_text, tavily_search


class BuiltinProviderImpl:
    def __init__(self, cfg: WebVerifyConfig) -> None:
        self._cfg = cfg

    def verify_claims(
        self, claims: list[dict[str, Any]], *, problem: dict[str, Any], run_dir: Path | None
    ) -> dict[str, Any]:
        brave = self._cfg.search_api_key if self._cfg.search_url is None else None
        tavily = self._cfg.search_api_key if "/tavily" in (self._cfg.search_url or "") else None
        if not brave and not tavily and not self._cfg.search_api_key:
            return {"provider": "builtin", "status": "unsupported", "claims": claims, "citations": []}
        api_key = self._cfg.search_api_key or ""
        enriched: list[dict[str, Any]] = []
        citations: list[dict[str, Any]] = []
        cid = 1
        for claim in claims:
            qs = claim.get("queries") or [
                f"{claim.get('name')} datasheet",
                f"{claim.get('name')} standard value",
                f"{claim.get('claim_id')} engineering",
            ]
            sources: list[dict[str, Any]] = []
            for q in qs[:3]:
                hits = (
                    tavily_search(q, api_key, max_results=3)
                    if "tavily" in (self._cfg.search_url or "")
                    else brave_search(q, api_key, count=3)
                )
                for h in hits:
                    if h.get("url") and "example" not in str(h.get("url")).lower():
                        status, _ = fetch_text(str(h["url"]))
                        if status < 400:
                            sources.append(
                                {
                                    **h,
                                    "http_status": status,
                                    "citation_id": cid,
                                    "snippet": (h.get("snippet") or "")[:280],
                                }
                            )
                            citations.append(sources[-1])
                            cid += 1
                            if len(sources) >= 2:
                                break
                if len(sources) >= 2:
                    break
            enriched.append({**claim, "queries": qs[:3], "sources": sources, "status": "host_pending"})
        return {
            "provider": "builtin",
            "status": "pass" if enriched else "unsupported",
            "claims": enriched,
            "citations": citations,
        }

    def find_similar_problems(
        self, problem: dict[str, Any], *, arc_result: Any, run_dir: Path | None
    ) -> dict[str, Any]:
        return {"provider": "builtin", "topic": problem.get("topic") or "", "matches": []}
