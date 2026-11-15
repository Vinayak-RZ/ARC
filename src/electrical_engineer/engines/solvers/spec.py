"""Table-driven SolverSpec for new ee_v2 solvers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

REQUIRED = object()


@dataclass(frozen=True)
class Param:
    name: str
    kind: Literal["num", "str", "list", "matrix"] = "num"
    default: Any = REQUIRED
    choices: tuple[str, ...] = ()


@dataclass(frozen=True)
class SolverSpec:
    fn: Callable[..., dict[str, Any]]
    params: tuple[Param, ...]
    value_key: str
    unit: str


def build_kwargs(spec: SolverSpec, problem: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for p in spec.params:
        if p.name not in problem:
            if p.default is REQUIRED:
                raise KeyError(f"missing {p.name}")
            out[p.name] = p.default
            continue
        raw = problem[p.name]
        if p.kind == "num":
            if isinstance(raw, dict) and "value" in raw:
                raw = raw["value"]
            out[p.name] = float(raw)
        elif p.kind == "str":
            val = str(raw)
            if p.choices and val not in p.choices:
                raise ValueError(f"{p.name} must be one of {p.choices}, got {val!r}")
            out[p.name] = val
        elif p.kind == "list":
            out[p.name] = list(raw)
        elif p.kind == "matrix":
            out[p.name] = raw
        else:  # pragma: no cover
            raise ValueError(p.kind)
    return out
