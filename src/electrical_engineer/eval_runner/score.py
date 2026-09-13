"""Gold eval: compare evidentiary band to expect.json. No LLM-as-judge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.runner.execute import execute
from electrical_engineer.runner.runs import project_root
from electrical_engineer.unchecked import UNCHECKED


def gold_root(cwd: Path | None = None) -> Path:
    return project_root(cwd) / "eval" / "gold"


def iter_items(pack: str | None = None, cwd: Path | None = None) -> list[Path]:
    root = gold_root(cwd)
    names = [pack] if pack else sorted(p.name for p in root.iterdir() if p.is_dir())
    items: list[Path] = []
    for name in names:
        folder = root / name
        if not folder.is_dir():
            continue
        for item in sorted(folder.iterdir()):
            if item.is_dir() and (item / "expect.json").is_file():
                items.append(item)
    return items


def score(summary: dict[str, Any], expect: dict[str, Any]) -> dict[str, Any]:
    ok = summary.get("recipe_id") == expect.get("recipe_id")
    if expect.get("token") == UNCHECKED or expect.get("unchecked") is True:
        ok = ok and summary.get("token") == UNCHECKED
    if expect.get("unchecked") is False:
        ok = ok and not summary.get("unchecked")
        if "value" in expect:
            tol = float(expect.get("tol", 1e-6))
            ok = ok and abs(float(summary.get("value")) - float(expect["value"])) <= tol
    if expect.get("citations"):
        got = summary.get("citations") or []
        for want in expect["citations"]:
            ok = ok and any(
                str(g.get("book_id")) == str(want.get("book_id"))
                and str(g.get("chapter_id")) == str(want.get("chapter_id"))
                for g in got
            )
    return {"ok": bool(ok), "summary": summary, "expect": expect}


def run_item(item: Path, *, run_root: Path | None = None) -> dict[str, Any]:
    expect = json.loads((item / "expect.json").read_text())
    problem: dict[str, Any] = {}
    for name in ("problem.json", "payload.json"):
        path = item / "fixtures" / name
        if path.is_file():
            problem.update(json.loads(path.read_text()))
    result = execute(expect["recipe_id"], run_root=run_root, problem=problem or None)
    evid_path = Path(result["run_dir"]) / "evidentiary.json"
    summary = json.loads(evid_path.read_text()) if evid_path.is_file() else result["summary"]
    scored = score(summary, expect)
    scored["item"] = str(item)
    scored["run_id"] = result["run_id"]
    return scored


def run_pack(pack: str | None = None, *, cwd: Path | None = None, run_root: Path | None = None) -> int:
    items = iter_items(pack, cwd)
    failed = 0
    for item in items:
        row = run_item(item, run_root=run_root)
        mark = "PASS" if row["ok"] else "FAIL"
        print(f"{mark} {item.name} recipe={row['expect'].get('recipe_id')}")
        if not row["ok"]:
            failed += 1
    print(f"{len(items) - failed}/{len(items)} passed")
    return 0 if failed == 0 and items else 1
