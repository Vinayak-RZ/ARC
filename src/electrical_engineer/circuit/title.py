"""Human titles for saved runs. Recipe + kind + find."""

from __future__ import annotations

from typing import Any

KIND_HEAD = {
    "voltage_divider": "Voltage divider",
    "ohms_law": "Ohm's law",
    "series_rlc": "Series RLC",
    "dc": "DC drive",
}

KIND_FIND = {
    "voltage_divider": "Vout",
    "ohms_law": "I",
    "series_rlc": "Vc",
    "dc": "rpm",
}

RECIPE_HEAD = {
    "solve-circuit-problem": "Circuit problem",
    "simulate-circuit": "Circuit simulation",
    "simulate-after-confirm": "Confirmed simulation",
    "solve-control-problem": "Control step",
    "smib-swing-study": "SMIB swing",
    "solve-drives-problem": "Drive speed",
    "solve-digital-control-problem": "Digital loop",
    "solve-signals-problem": "Signals problem",
    "unmatched-cosolver": "Open question",
    "explain-circuits": "Circuits explanation",
    "explain-control": "Control explanation",
    "explain-signals": "Signals explanation",
    "explain-power": "Power explanation",
    "photo-to-netlist": "Photo to netlist",
}


def _format_qty(val: Any, recipe_id: str) -> str:
    try:
        n = float(val)
    except (TypeError, ValueError):
        return str(val)
    if "control" in recipe_id or "signal" in recipe_id:
        return f"{n:.3f}"
    if abs(n) >= 100:
        return f"{n:.2f}"
    if abs(n) < 0.01:
        return f"{n:.4f}"
    return f"{n:.2f}"


def run_title(recipe_id: str, problem: dict[str, Any] | None = None) -> str:
    problem = problem or {}
    prompt = str(problem.get("prompt") or "").strip()
    if prompt:
        one = " ".join(prompt.split())
        if len(one) > 56:
            return one[:53] + "…"
        return one
    kind = str(problem.get("kind") or "")
    head = KIND_HEAD.get(kind) or RECIPE_HEAD.get(recipe_id) or recipe_id.replace("-", " ").title()
    find = str(problem.get("find") or KIND_FIND.get(kind) or "")
    if find:
        return f"{head} · {find}"
    return head


def title_with_value(recipe_id: str, problem: dict[str, Any] | None, value: Any, unchecked: bool) -> str:
    base = run_title(recipe_id, problem)
    if unchecked or value is None or value == "unchecked":
        return base
    qty = _format_qty(value, recipe_id)
    if "·" in base:
        return base
    find = KIND_FIND.get(str((problem or {}).get("kind") or "")) or "Result"
    return f"{base} · {find} = {qty}"
