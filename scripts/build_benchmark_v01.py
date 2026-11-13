#!/usr/bin/env python3
"""Package EEE-Coursework-Trap v0.1 (license-clean reconstructions only)."""

from __future__ import annotations

import hashlib
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "artifacts" / "frontier"
OUT_DIR = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    members = [
        ROOT / "artifacts/frontier/trap_suite_index.json",
        ROOT / "proofs/ablation/trap_prompts.yaml",
        ROOT / "eval/gold/power/smib-eec301-01/expect.json",
    ]
    tarball = OUT_DIR / "eee-coursework-trap-v0.1.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        for path in members:
            if path.is_file():
                tar.add(path, arcname=path.relative_to(ROOT).as_posix())
    digest = hashlib.sha256(tarball.read_bytes()).hexdigest()
    manifest = {"version": "v0.1", "sha256": digest, "files": [p.relative_to(ROOT).as_posix() for p in members]}
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(tarball, digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
