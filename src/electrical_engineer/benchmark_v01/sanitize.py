"""Strip grader-only fields from public benchmark givens."""

from __future__ import annotations

import re
from typing import Any

GRADER_ONLY_KEYS = frozenset(
    {
        "expected",
        "tol",
        "pick_sigma",
        "value_key",
        "solver",
        "check_kind",
        "recipe_id",
        "engine",
        "unchecked",
        "oracle",
        "reference",
        "golden_file",
        "schema",
        "margins",
    }
)

_RE_ARTIFACT = re.compile(r"(`[^`]*artifacts[^`]*`|artifacts/[^\s]+)", re.I)
_RE_ARC = re.compile(r"\b(Arc PSA|recipe_id|fixture case\.json|Run recipe)\b.*", re.I)


def strip_grader_fields(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {
            k: strip_grader_fields(v)
            for k, v in obj.items()
            if k not in GRADER_ONLY_KEYS
        }
    if isinstance(obj, list):
        return [strip_grader_fields(v) for v in obj]
    return obj


def materialize_preset_givens(givens: dict[str, Any]) -> dict[str, Any]:
    """Inline preset names so public dicts need no lookup tables."""
    from electrical_engineer.engines.ed_lambda import EdCase

    out = dict(givens)
    units = out.get("units")
    if units == "eec301":
        out["units"] = [
            {
                "a": u.a,
                "b": u.b,
                "c": u.c,
                "pmin": u.pmin,
                "pmax": u.pmax,
            }
            for u in EdCase.eec301_default().units
        ]
    return out


def flatten_public_givens(fixtures: dict[str, Any]) -> dict[str, Any]:
    """One flat dict for external solvers (no nested problem.json wrapper)."""
    prob = fixtures.get("problem.json") or {}
    case = fixtures.get("case.json") or {}
    graph = fixtures.get("graph.json") or {}
    merged = {**case, **prob, **graph}
    return materialize_preset_givens(strip_grader_fields(merged))


def clean_question_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if _RE_ARC.search(line):
            continue
        line = _RE_ARTIFACT.sub("", line)
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines).strip()


def grading_hints_from_fixtures(fixtures: dict[str, Any], expect: dict[str, Any]) -> dict[str, Any]:
    prob = fixtures.get("problem.json") or {}
    return {
        "solver": prob.get("solver") or prob.get("check_kind"),
        "tol": expect.get("tol", 1e-6),
        "engine": expect.get("engine"),
        "recipe_id": expect.get("recipe_id"),
        "expect": {k: v for k, v in expect.items() if k not in ("schema", "golden_file")},
    }
