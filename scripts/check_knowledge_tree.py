#!/usr/bin/env python3
"""Contract checker for knowledge/ug-ee (stdlib + PyYAML already in the project)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
COVERAGE = KNOWLEDGE / "COVERAGE.yaml"
MIN_WORDS = 1500
MIN_QUESTIONS = 5
NOTE_HEADINGS = ("## Concepts", "## Equations", "## Methods", "## Mistakes")
Q_HEADINGS = ("### Given", "### Find", "### Solution", "### Answer")
SPDX_OK = ("CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0")
SPDX_RE = re.compile(r"SPDX-License-Identifier:\s*(CC-BY-4\.0|CC-BY-SA-4\.0|CC0-1\.0)")
FORBIDDEN = (
    "CC-BY-NC",
    "SPDX-License-Identifier: CC-BY-NC",
    "BEGIN COMMERCIAL TEXTBOOK DUMP",
    "GATE EE previous year paper verbatim",
)
Q_RE = re.compile(r"^## Q(\d+)\s*$", re.M)


def load_coverage() -> dict:
    return yaml.safe_load(COVERAGE.read_text())


def select_packs(data: dict, pack: str | None) -> dict[str, dict]:
    packs = data["packs"]
    if pack is None:
        return packs
    if pack in packs:
        return {pack: packs[pack]}
    grouped = {k: v for k, v in packs.items() if v.get("group") == pack}
    if grouped:
        return grouped
    raise SystemExit(f"unknown pack {pack!r}")


def word_count(text: str) -> int:
    return len(text.split())


def check_floors(data: dict) -> list[str]:
    errs: list[str] = []
    mins = data.get("min_units") or {}
    packs = data["packs"]
    for key, n in mins.items():
        if key not in packs:
            errs.append(f"min_units: missing pack {key}")
            continue
        got = len(packs[key]["units"])
        if got < n:
            errs.append(f"{key}: {got} units < min {n}")
    if len(packs) < 10:
        errs.append(f"expected >=10 packs, got {len(packs)}")
    return errs


def check_unit(unit_dir: Path, allow_empty: bool) -> list[str]:
    errs: list[str] = []
    for name in ("notes.md", "questions.md", "sources.md"):
        p = unit_dir / name
        if not p.is_file():
            errs.append(f"missing {p.relative_to(ROOT)}")
    if errs:
        return errs
    notes = (unit_dir / "notes.md").read_text()
    questions = (unit_dir / "questions.md").read_text()
    if not allow_empty:
        wc = word_count(notes)
        if wc < MIN_WORDS:
            errs.append(f"{unit_dir.relative_to(ROOT)}/notes.md words {wc} < {MIN_WORDS}")
        for h in NOTE_HEADINGS:
            if h not in notes:
                errs.append(f"{unit_dir.relative_to(ROOT)}/notes.md missing {h}")
        ids = [int(m.group(1)) for m in Q_RE.finditer(questions)]
        if len(ids) < MIN_QUESTIONS:
            errs.append(
                f"{unit_dir.relative_to(ROOT)}/questions.md has {len(ids)} Q headings < {MIN_QUESTIONS}"
            )
        for m in Q_RE.finditer(questions):
            start = m.start()
            nxt = Q_RE.search(questions, m.end())
            block = questions[start : nxt.start() if nxt else None]
            for h in Q_HEADINGS:
                if h not in block:
                    errs.append(
                        f"{unit_dir.relative_to(ROOT)}/questions.md {m.group(0)} missing {h}"
                    )
                    break
    oer = unit_dir / "oer"
    if oer.is_dir():
        files = [p for p in oer.rglob("*") if p.is_file()]
        if files and not allow_empty:
            pass
        for p in files:
            head = p.read_text(errors="replace")[:4000]
            for tok in FORBIDDEN:
                if tok in head or tok in p.read_text(errors="replace"):
                    errs.append(f"{p.relative_to(ROOT)} forbidden token {tok!r}")
            if not SPDX_RE.search(head):
                errs.append(f"{p.relative_to(ROOT)} missing SPDX CC-BY/SA or CC0")
    return errs


def inventory(data: dict, packs: dict) -> dict[str, int]:
    units = questions = 0
    for spec in packs.values():
        units += len(spec["units"])
        base = KNOWLEDGE / spec["path"]
        for u in spec["units"]:
            qpath = base / u["id"] / "questions.md"
            if qpath.is_file():
                questions += len(Q_RE.findall(qpath.read_text()))
    return {"packs": len(packs), "units": units, "questions": questions}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow-empty", action="store_true")
    ap.add_argument("--pack", default=None)
    ap.add_argument("--floors-only", action="store_true")
    args = ap.parse_args(argv)
    data = load_coverage()
    errs = check_floors(data)
    if args.floors_only:
        if errs:
            print("\n".join(errs), file=sys.stderr)
            return 1
        print("coverage floors OK")
        return 0
    packs = select_packs(data, args.pack)
    for spec in packs.values():
        base = KNOWLEDGE / spec["path"]
        if not (base / "INDEX.md").is_file():
            errs.append(f"missing {base.relative_to(ROOT)}/INDEX.md")
        if not (base / "SYLLABUS.md").is_file():
            errs.append(f"missing {base.relative_to(ROOT)}/SYLLABUS.md")
        for u in spec["units"]:
            errs.extend(check_unit(base / u["id"], args.allow_empty))
    inv = inventory(data, packs)
    print(
        f"packs={inv['packs']} units={inv['units']} questions={inv['questions']} "
        f"allow_empty={args.allow_empty}"
    )
    if errs:
        print(f"{len(errs)} error(s):", file=sys.stderr)
        print("\n".join(errs[:80]), file=sys.stderr)
        if len(errs) > 80:
            print(f"... {len(errs) - 80} more", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
