"""Local Learn progress store under .electrical-engineer/learn/."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from electrical_engineer.learn.curriculum import expand_topics, load_curriculum
from electrical_engineer.runner.runs import project_root

logger = logging.getLogger(__name__)

_LAB_IDS = frozenset({"rectifier", "converter", "idmt", "lead"})
_SCHEMA = "arc.learn_progress.v1"


class ProgressError(ValueError):
    pass


def progress_dir(cwd: Path | None = None) -> Path:
    return project_root(cwd) / ".electrical-engineer" / "learn"


def progress_path(cwd: Path | None = None) -> Path:
    return progress_dir(cwd) / "progress.json"


def _empty() -> dict[str, Any]:
    return {
        "schema": _SCHEMA,
        "topics_done": {},
        "labs_opened": {},
        "unlocked": {},
    }


def load(cwd: Path | None = None) -> dict[str, Any]:
    path = progress_path(cwd)
    if not path.is_file():
        return _empty()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("corrupt learn progress at %s: %s", path, exc)
        return _empty()
    if not isinstance(data, dict):
        logger.warning("corrupt learn progress (not object) at %s", path)
        return _empty()
    out = _empty()
    out["topics_done"] = dict(data.get("topics_done") or {})
    out["labs_opened"] = dict(data.get("labs_opened") or {})
    out["unlocked"] = dict(data.get("unlocked") or {})
    return out


def save(cwd: Path | None, data: dict[str, Any]) -> None:
    folder = progress_dir(cwd)
    folder.mkdir(parents=True, exist_ok=True)
    path = progress_path(cwd)
    payload = json.dumps(data, indent=2, sort_keys=True)
    fd, tmp_name = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(payload)
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _known_topic_keys(cwd: Path | None) -> set[str]:
    data = load_curriculum(cwd)
    keys: set[str] = set()
    for sem in data.get("semesters") or []:
        for subj in sem.get("subjects") or []:
            for t in expand_topics(subj, cwd):
                keys.add(f"{subj['id']}/{t['id']}")
    return keys


def set_topic(cwd: Path | None, key: str, done: bool) -> dict[str, Any]:
    if key not in _known_topic_keys(cwd):
        raise ProgressError(f"unknown topic {key}")
    data = load(cwd)
    if done:
        data["topics_done"][key] = _now()
    else:
        data["topics_done"].pop(key, None)
    save(cwd, data)
    return data


def mark_lab(cwd: Path | None, lab: str) -> dict[str, Any]:
    if lab not in _LAB_IDS:
        raise ProgressError(f"unknown lab {lab}")
    data = load(cwd)
    data["labs_opened"].setdefault(lab, _now())
    save(cwd, data)
    return data


def apply(cwd: Path | None, body: dict[str, Any]) -> dict[str, Any]:
    keys = set(body.keys())
    if keys == {"topic", "done"}:
        topic = body["topic"]
        done = body["done"]
        if not isinstance(topic, str) or not isinstance(done, bool):
            raise ProgressError("topic must be str and done must be bool")
        return set_topic(cwd, topic, done)
    if keys == {"lab"}:
        lab = body["lab"]
        if not isinstance(lab, str):
            raise ProgressError("lab must be str")
        return mark_lab(cwd, lab)
    raise ProgressError("body must be {topic, done} or {lab}")
