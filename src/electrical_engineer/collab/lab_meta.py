"""lab_meta.json on runs: links problems to circuit or control studio artifacts."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def lab_meta_path(run_dir: Path) -> Path:
    return run_dir / "lab_meta.json"


def load_lab_meta(run_dir: Path) -> dict[str, Any]:
    path = lab_meta_path(run_dir)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def save_lab_meta(run_dir: Path, data: dict[str, Any]) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    data.setdefault("updated_at_ms", int(time.time() * 1000))
    lab_meta_path(run_dir).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def ensure_lab_meta(
    run_dir: Path,
    *,
    kind: str,
    control_session_id: str | None = None,
) -> dict[str, Any]:
    meta = load_lab_meta(run_dir)
    meta.setdefault("kind", kind)
    meta.setdefault("revision", 0)
    meta.setdefault("op_log", [])
    if control_session_id:
        meta["control_session_id"] = control_session_id
    if kind == "circuit":
        meta.setdefault("workspace", "circuits")
    elif kind == "control":
        meta.setdefault("workspace", "control")
        meta.setdefault("control_session_id", control_session_id or meta.get("control_session_id"))
    return save_lab_meta(run_dir, meta)


def ui_lab_url(run_id: str, meta: dict[str, Any], base: str = "http://127.0.0.1:8765/") -> str:
    kind = str(meta.get("kind") or "circuit")
    if kind == "control" and meta.get("control_session_id"):
        return f"{base}?view=control-studio&session={meta['control_session_id']}"
    return f"{base}?view=studio&tab=circuits&run={run_id}"