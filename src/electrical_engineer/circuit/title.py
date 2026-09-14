"""Human titles for saved runs. Recipe + kind + find."""

from __future__ import annotations

from typing import Any

KIND_HEAD = {
    "voltage_divider": "Voltage divider",
    "ohms_law": "Ohm's law",
}

KIND_FIND = {
    "voltage_divider": "Vout",
    "ohms_law": "I",
}


def run_title(recipe_id: str, problem: dict[str, Any] | None = None) -> str:
    problem = problem or {}
    kind = str(problem.get("kind") or "")
    head = KIND_HEAD.get(kind) or recipe_id.replace("-", " ")
    find = str(problem.get("find") or KIND_FIND.get(kind) or "")
    if find:
        return f"{head} · {find}"
    return head
