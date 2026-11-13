"""Default unity-feedback spec (matches eval gold block-feedback-01)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.engines.block_diagram import plant_problem_dict

_DEFAULT: dict[str, Any] = {
    "blocks": [
        {"id": "G", "tf": "10/(s+1)"},
        {"id": "H", "tf": "1"},
    ],
    "unity_feedback": {"forward": "G", "feedback": "H", "negative": True},
}


def unity_feedback_problem(props: dict[str, Any] | None = None) -> dict[str, Any]:
    if props and props.get("blocks"):
        return props
    gold = Path(__file__).resolve().parents[3] / "eval/gold/control/block-feedback-01/fixtures/problem.json"
    if gold.is_file():
        return json.loads(gold.read_text(encoding="utf-8"))
    return dict(_DEFAULT)


def plant_meta(problem: dict[str, Any]) -> dict[str, Any]:
    plant = plant_problem_dict(problem)
    blocks = {str(b["id"]): b for b in problem.get("blocks") or []}
    g = blocks.get(str(problem.get("unity_feedback", {}).get("forward") or "G"), {})
    h_id = str(problem.get("unity_feedback", {}).get("feedback") or "")
    h = blocks.get(h_id, {}) if h_id else {}
    return {
        "G_tf": str(g.get("tf") or g.get("transfer_function") or "G(s)"),
        "H_tf": str(h.get("tf") or "1"),
        "negative": bool(problem.get("unity_feedback", {}).get("negative", True)),
        "num": plant["num"],
        "den": plant["den"],
    }
