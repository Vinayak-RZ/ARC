"""Score circuit engine-mode gold items (verify-after-derive). Schema v2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.engines.circuit_verify import verify_after_derive


def _fixture(problem: dict[str, Any], item: Path) -> dict[str, Any]:
    merged = dict(problem)
    for name in ("problem.json", "case.json"):
        path = item / "fixtures" / name
        if path.is_file():
            merged.update(json.loads(path.read_text()))
    return merged


def run_circuit_item(item: Path, expect: dict[str, Any], *, run_root: Path | None = None) -> dict[str, Any]:
    problem = _fixture({}, item)
    run_dir = None
    if run_root is not None:
        run_dir = run_root / item.name
        run_dir.mkdir(parents=True, exist_ok=True)
    out = verify_after_derive(problem, run_dir=run_dir, rel_tol=float(expect.get("rel_tol", 1e-3)))
    want = expect.get("value")
    tol = float(expect.get("tol", problem.get("tol", 1e-4)))
    ok = bool(out.get("ok"))
    if want is not None:
        got = out.get("value")
        ok = got is not None and abs(float(got) - float(want)) <= tol
    if expect.get("require_spice_match") and out.get("mismatch"):
        ok = False
    if expect.get("require_spice") and (out.get("spice") or {}).get("skipped"):
        ok = False
    summary = {
        "engine": expect.get("engine", "circuit_unit"),
        "schema": expect.get("schema", "arc.eval.expect.v2"),
        "kind": out.get("kind"),
        "value": out.get("value"),
        "simulated": out.get("simulated"),
        "mismatch": out.get("mismatch"),
        "spice_skipped": (out.get("spice") or {}).get("skipped"),
        "spice_reason": (out.get("spice") or {}).get("reason"),
    }
    return {"ok": bool(ok), "summary": summary, "expect": expect, "item": str(item), "run_id": None}
