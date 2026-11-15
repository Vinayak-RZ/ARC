"""Evaluate Learn achievements from runs and progress."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from electrical_engineer.catalog import PACKS, pack_for_recipe
from electrical_engineer.learn import progress as progress_mod
from electrical_engineer.learn.curriculum import expand_topics, load_curriculum

_RULES_PATH = Path(__file__).with_name("achievements.yaml")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_rules() -> dict[str, Any]:
    return yaml.safe_load(_RULES_PATH.read_text(encoding="utf-8")) or {}


def _summaries(runs_dir: Path) -> list[dict[str, Any]]:
    if not runs_dir.is_dir():
        return []
    out: list[dict[str, Any]] = []
    for folder in runs_dir.iterdir():
        if not folder.is_dir():
            continue
        for name in ("summary.json", "evidentiary.json"):
            path = folder / name
            if path.is_file():
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                if isinstance(data, dict):
                    out.append(data)
                break
    return out


def _expand_templates(rules: list[dict[str, Any]], cwd: Path | None) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    curriculum = load_curriculum(cwd)
    for rule in rules:
        rtype = (rule.get("rule") or {}).get("type")
        if rtype == "first_in_pack":
            for pack in PACKS:
                expanded.append(
                    {
                        **rule,
                        "id": f"{rule['id']}:{pack.id}",
                        "title": str(rule["title"]).replace("{pack_label}", pack.label),
                        "_pack": pack.id,
                    }
                )
        elif rtype == "subject_complete":
            for sem in curriculum.get("semesters") or []:
                for subj in sem.get("subjects") or []:
                    topics = expand_topics(subj, cwd)
                    if not topics:
                        continue
                    expanded.append(
                        {
                            **rule,
                            "id": f"{rule['id']}:{subj['id']}",
                            "title": str(rule["title"]).replace(
                                "{subject_title}", str(subj.get("title") or subj["id"])
                            ),
                            "_subject_id": subj["id"],
                            "_topic_keys": [f"{subj['id']}/{t['id']}" for t in topics],
                        }
                    )
        elif rtype == "semester_complete":
            for sem in curriculum.get("semesters") or []:
                keys: list[str] = []
                for subj in sem.get("subjects") or []:
                    for t in expand_topics(subj, cwd):
                        keys.append(f"{subj['id']}/{t['id']}")
                if not keys:
                    continue
                expanded.append(
                    {
                        **rule,
                        "id": f"{rule['id']}:{sem['n']}",
                        "title": str(rule["title"]).replace("{n}", str(sem["n"])),
                        "_topic_keys": keys,
                    }
                )
        else:
            expanded.append(dict(rule))
    return expanded


def _eval_one(
    item: dict[str, Any],
    *,
    summaries: list[dict[str, Any]],
    progress: dict[str, Any],
    cwd: Path | None,
) -> tuple[bool, dict[str, int]]:
    rule = item.get("rule") or {}
    rtype = rule.get("type")
    topics_done = progress.get("topics_done") or {}
    labs_opened = progress.get("labs_opened") or {}
    if rtype == "run_count":
        min_n = int(rule.get("min") or 1)
        verified = bool(rule.get("verified"))
        count = 0
        for s in summaries:
            if verified and s.get("unchecked") is not False:
                continue
            count += 1
        return count >= min_n, {"value": count, "target": min_n}
    if rtype == "first_in_pack":
        pack = item.get("_pack")
        count = 0
        for s in summaries:
            rid = s.get("recipe_id")
            if rid and pack_for_recipe(str(rid), cwd) == pack:
                count += 1
        return count >= 1, {"value": min(count, 1), "target": 1}
    if rtype == "all_packs":
        touched: set[str] = set()
        for s in summaries:
            rid = s.get("recipe_id")
            if rid:
                p = pack_for_recipe(str(rid), cwd)
                if p:
                    touched.add(p)
        target = len(PACKS)
        return len(touched) >= target, {"value": len(touched), "target": target}
    if rtype == "topics_done":
        min_n = int(rule.get("min") or 1)
        n = len(topics_done)
        return n >= min_n, {"value": n, "target": min_n}
    if rtype == "labs_opened":
        min_n = int(rule.get("min") or 1)
        n = len(labs_opened)
        return n >= min_n, {"value": n, "target": min_n}
    if rtype == "subject_complete":
        keys = item.get("_topic_keys") or []
        n = sum(1 for k in keys if k in topics_done)
        return n >= len(keys) and len(keys) > 0, {"value": n, "target": len(keys)}
    if rtype == "semester_complete":
        keys = item.get("_topic_keys") or []
        n = sum(1 for k in keys if k in topics_done)
        return n >= len(keys) and len(keys) > 0, {"value": n, "target": len(keys)}
    return False, {"value": 0, "target": 1}


def evaluate(cwd: Path | None, runs_dir: Path) -> dict[str, Any]:
    rules = load_rules().get("achievements") or []
    items = _expand_templates(rules, cwd)
    summaries = _summaries(runs_dir)
    progress = progress_mod.load(cwd)
    unlocked = dict(progress.get("unlocked") or {})
    newly: list[str] = []
    achievements: list[dict[str, Any]] = []
    for item in items:
        met, prog = _eval_one(item, summaries=summaries, progress=progress, cwd=cwd)
        aid = str(item["id"])
        unlocked_at = unlocked.get(aid)
        if met and not unlocked_at:
            unlocked_at = _now()
            unlocked[aid] = unlocked_at
            newly.append(aid)
        achievements.append(
            {
                "id": aid,
                "title": item.get("title"),
                "icon": item.get("icon"),
                "unlocked_at": unlocked_at if met else None,
                "progress": prog,
            }
        )
    if newly:
        progress["unlocked"] = unlocked
        progress_mod.save(cwd, progress)
    return {"achievements": achievements, "newly_unlocked": newly}
