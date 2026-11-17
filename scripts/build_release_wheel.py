#!/usr/bin/env python3
"""Build a release wheel with bundled workflows/hosts/ui. Fail if ui/dist is missing."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI_INDEX = ROOT / "ui" / "dist" / "index.html"
REQUIRED_PREFIXES = (
    "electrical_engineer/_bundle/workflows/",
    "electrical_engineer/_bundle/hosts/",
    "electrical_engineer/_bundle/ui/dist/",
)


def main() -> int:
    if not UI_INDEX.is_file():
        print(
            "ui/dist/index.html missing — run `npm run build` in ui/ before packaging",
            file=sys.stderr,
        )
        return 1
    subprocess.check_call([sys.executable, "-m", "build", "--wheel"], cwd=ROOT)
    dist = ROOT / "dist"
    wheels = sorted(dist.glob("electrical_engineer-*.whl"))
    if not wheels:
        print("no wheel produced in dist/", file=sys.stderr)
        return 1
    wheel = wheels[-1]
    with zipfile.ZipFile(wheel) as zf:
        names = zf.namelist()
    missing = [p for p in REQUIRED_PREFIXES if not any(n.startswith(p) for n in names)]
    if missing:
        print(f"wheel missing bundle paths: {missing}", file=sys.stderr)
        return 1
    print(f"ok {wheel.name} bundles workflows, hosts, ui/dist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
