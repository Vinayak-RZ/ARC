"""JSON shapes for web evidence and similar-problem matches."""

from __future__ import annotations

from typing import Any, TypedDict


class SourceRecord(TypedDict, total=False):
    citation_id: int
    query: str
    url: str
    domain: str
    retrieved_at: str
    snippet: str
    extracted_value: float | str
    unit: str
    conditions: str
    source_class: str


class ClaimRecord(TypedDict, total=False):
    claim_id: str
    name: str
    description: str
    library_value: float | str
    solver_value: float | str
    web_value: float | str
    unit: str
    conditions: str
    tolerance: float
    queries: list[str]
    sources: list[SourceRecord]
    status: str
    disagreement: dict[str, Any]


class SimilarProblem(TypedDict, total=False):
    url: str
    title: str
    domain: str
    similarity_score: float
    diff_note: str
    their_result: float | str
    their_unit: str
    arc_result: float | str
    agrees_after_adjustment: bool | None
    snippet: str
    citation_id: int


class WebSourcesBundle(TypedDict, total=False):
    provider: str
    status: str
    claims: list[ClaimRecord]
    citations: list[SourceRecord]


class SimilarProblemsBundle(TypedDict, total=False):
    provider: str
    topic: str
    matches: list[SimilarProblem]
