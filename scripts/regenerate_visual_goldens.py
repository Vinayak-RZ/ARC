#!/usr/bin/env python3
"""Regenerate Visual Kit golden PNGs under artifacts/visual-goldens/."""

from __future__ import annotations

from pathlib import Path

from electrical_engineer.visual_kit.registry import GOLDEN_MAP, list_component_ids
from electrical_engineer.visual_kit.render import render_component

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "artifacts" / "visual-goldens"


def main() -> int:
    ids = list_component_ids()
    for cid in ids:
        sub = GOLDEN_MAP.get(cid, cid.split(".")[-1])
        out_dir = GOLD / sub
        out_dir.mkdir(parents=True, exist_ok=True)
        out = render_component(cid, out_dir)
        path = out.get("png") or out.get("gif")
        print(cid, "->", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
