"""Pluggable web search backends for context verification."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from electrical_engineer.web_verify.config import WebVerifyConfig


def _now() -> str:
    return datetime.now(UTC).isoformat()


class WebSearchProvider(ABC):
    @abstractmethod
    def verify_claims(
        self, claims: list[dict[str, Any]], *, problem: dict[str, Any], run_dir: Path | None
    ) -> dict[str, Any]:
        """Return enriched claims with sources and reconciled web_value."""

    @abstractmethod
    def find_similar_problems(
        self, problem: dict[str, Any], *, arc_result: Any, run_dir: Path | None
    ) -> dict[str, Any]:
        """Return similar_problems bundle."""


class OfflineProvider(WebSearchProvider):
    def __init__(self, fixtures_root: Path) -> None:
        self._root = fixtures_root

    def _load(self, fixture_id: str) -> dict[str, Any]:
        path = self._root / f"{fixture_id}.json"
        if not path.is_file():
            raise FileNotFoundError(fixture_id)
        return json.loads(path.read_text(encoding="utf-8"))

    def verify_claims(
        self, claims: list[dict[str, Any]], *, problem: dict[str, Any], run_dir: Path | None
    ) -> dict[str, Any]:
        fix_id = str(problem.get("web_verify_fixture") or problem.get("fixture_id") or "")
        if not fix_id:
            fix_id = str(claims[0].get("claim_id")) if claims else ""
        data = self._load(fix_id)
        enriched: list[dict[str, Any]] = []
        citation_id = 1
        all_citations: list[dict[str, Any]] = []
        for row in data.get("claims", []):
            sources = []
            for src in row.get("sources", []):
                rec = {**src, "citation_id": citation_id, "retrieved_at": src.get("retrieved_at") or _now()}
                sources.append(rec)
                all_citations.append(rec)
                citation_id += 1
            enriched.append(
                {
                    **row,
                    "queries": row.get("queries") or data.get("queries") or [],
                    "sources": sources,
                    "web_value": row.get("authoritative_value"),
                    "status": row.get("status") or "verified",
                }
            )
        return {
            "provider": "offline",
            "status": data.get("status") or "pass",
            "claims": enriched,
            "citations": all_citations,
        }

    def find_similar_problems(
        self, problem: dict[str, Any], *, arc_result: Any, run_dir: Path | None
    ) -> dict[str, Any]:
        fix_id = str(problem.get("web_verify_fixture") or problem.get("fixture_id") or "")
        data = self._load(fix_id)
        matches = []
        cid = 0
        for row in data.get("claims") or []:
            cid += len(row.get("sources") or [])
        cid = max(cid, 0) + 1
        for m in data.get("similar_problems", []):
            matches.append({**m, "citation_id": m.get("citation_id") or cid})
            cid += 1
        return {
            "provider": "offline",
            "topic": data.get("topic") or problem.get("topic") or "",
            "matches": matches,
        }


class HostProvider(WebSearchProvider):
    """Defer search to the coding agent via MCP submit files in the run directory."""

    def verify_claims(
        self, claims: list[dict[str, Any]], *, problem: dict[str, Any], run_dir: Path | None
    ) -> dict[str, Any]:
        if run_dir is None:
            return {"provider": "host", "status": "pending_host", "claims": claims, "citations": []}
        submit = run_dir / "evidence" / "host_submit.json"
        request = run_dir / "evidence" / "host_request.json"
        if submit.is_file():
            data = json.loads(submit.read_text(encoding="utf-8"))
            from electrical_engineer.web_verify.validate import validate_host_submit

            validate_host_submit(data)
            return data.get("web_sources") or data
        request.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "kind": "arc_web_evidence_request",
            "requested_at": _now(),
            "claims": claims,
            "queries_per_claim": 3,
            "min_sources": 2,
            "min_domains": 2,
            "problem_excerpt": {k: problem.get(k) for k in ("topic", "given", "find") if problem.get(k)},
        }
        request.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return {"provider": "host", "status": "pending_host", "claims": claims, "citations": []}

    def find_similar_problems(
        self, problem: dict[str, Any], *, arc_result: Any, run_dir: Path | None
    ) -> dict[str, Any]:
        if run_dir and (run_dir / "evidence" / "host_submit.json").is_file():
            data = json.loads((run_dir / "evidence" / "host_submit.json").read_text(encoding="utf-8"))
            return data.get("similar_problems") or {"provider": "host", "topic": "", "matches": []}
        return {"provider": "host", "topic": problem.get("topic") or "", "matches": []}


class BuiltinProvider(WebSearchProvider):
    """HTTP fetch + optional search API (minimal; falls back to offline when no key)."""

    def verify_claims(
        self, claims: list[dict[str, Any]], *, problem: dict[str, Any], run_dir: Path | None
    ) -> dict[str, Any]:
        # Without configured search URL, fail closed to pending.
        return {"provider": "builtin", "status": "unsupported", "claims": claims, "citations": []}

    def find_similar_problems(
        self, problem: dict[str, Any], *, arc_result: Any, run_dir: Path | None
    ) -> dict[str, Any]:
        return {"provider": "builtin", "topic": problem.get("topic") or "", "matches": []}


def get_provider(cfg: WebVerifyConfig) -> WebSearchProvider:
    if cfg.provider == "offline":
        root = cfg.offline_fixtures_root or Path(__file__).resolve().parents[3] / "eval" / "fixtures" / "web_verify"
        return OfflineProvider(root)
    if cfg.provider == "builtin":
        return BuiltinProvider()
    return HostProvider()
