#!/usr/bin/env python3
"""Regenerate Visual Kit golden PNGs under artifacts/visual-goldens/."""

from __future__ import annotations

from pathlib import Path

from electrical_engineer.visual_kit.registry import GOLDEN_MAP, list_component_ids, load_manifest
from electrical_engineer.visual_kit.render import render_component

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "artifacts" / "visual-goldens"


def main() -> int:
    for c in load_manifest().get("components", []):
        cid = str(c["id"])
        sub = GOLDEN_MAP.get(cid, cid.split(".")[-1])
        out_dir = GOLD / sub
        out_dir.mkdir(parents=True, exist_ok=True)
        out = render_component(cid, out_dir, {"theme": "light"})
        path = out.get("png") or out.get("gif")
        print(cid, "light ->", path)
        if c.get("golden_dark"):
            dark_dir = GOLD / Path(str(c["golden_dark"])).parent
            dark_dir.mkdir(parents=True, exist_ok=True)
            dout = render_component(cid, dark_dir, {"theme": "dark"})
            print(cid, "dark ->", dout.get("png") or dout.get("gif"))
    # ensure list matches manifest only
    for cid in list_component_ids():
        if cid not in {str(x["id"]) for x in load_manifest().get("components", [])}:
            sub = GOLDEN_MAP.get(cid, cid.split(".")[-1])
            render_component(cid, GOLD / sub)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
