"""Load EEC-301 lab-pack golden JSON shipped under artifacts/."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


def _golden_dir() -> Path:
    root = Path(__file__).resolve().parents[3]
    return root / "artifacts" / "eec301-lab-goldens"


@lru_cache(maxsize=1)
def load_exp06_golden() -> dict[str, Any]:
    path = _golden_dir() / "exp06.json"
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_exp07_golden() -> dict[str, Any]:
    path = _golden_dir() / "exp07.json"
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_exp08_golden() -> dict[str, Any]:
    path = _golden_dir() / "exp08.json"
    return json.loads(path.read_text(encoding="utf-8"))
