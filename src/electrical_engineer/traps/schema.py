"""Solution trace schema for deterministic trap PRM checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

CheckStatus = Literal["pass", "fail", "unchecked"]
ProcessStatus = Literal["pass", "fail", "unchecked"]


@dataclass(frozen=True)
class TraceStep:
    id: str
    text: str = ""
    kind: str = "step"
    values: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SolutionTrace:
    trap_ids: tuple[str, ...] = ()
    givens: dict[str, Any] = field(default_factory=dict)
    steps: tuple[TraceStep, ...] = ()
    final: dict[str, Any] = field(default_factory=dict)
    topic: str = ""

    @classmethod
    def from_mapping(cls, raw: dict[str, Any] | None) -> SolutionTrace:
        if not raw:
            return cls()
        steps_in = raw.get("steps") or []
        steps: list[TraceStep] = []
        for i, s in enumerate(steps_in):
            if not isinstance(s, dict):
                continue
            steps.append(
                TraceStep(
                    id=str(s.get("id") or f"step-{i + 1}"),
                    text=str(s.get("text") or ""),
                    kind=str(s.get("kind") or "step"),
                    values={k: v for k, v in s.items() if k not in ("id", "text", "kind")},
                )
            )
        tids = raw.get("trap_ids") or raw.get("traps") or ()
        givens = dict(raw.get("givens") or {})
        return cls(
            trap_ids=tuple(str(t) for t in tids),
            givens=givens,
            steps=tuple(steps),
            final=dict(raw.get("final") or {}),
            topic=str(raw.get("topic") or ""),
        )


@dataclass(frozen=True)
class TrapCheck:
    trap_id: str
    status: CheckStatus
    passed: bool
    offending_step: str | None = None
    message: str = ""
    advisory: str | None = None


@dataclass(frozen=True)
class GradeScores:
    outcome_pass: bool
    process_pass: bool
    process_status: ProcessStatus
    outcome_score: float
    process_score: float
    checks: tuple[TrapCheck, ...]
    advisories: tuple[str, ...] = ()
