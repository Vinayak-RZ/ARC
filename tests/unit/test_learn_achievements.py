"""Achievements evaluator."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.learn import achievements as achievements_mod
from electrical_engineer.learn import progress as progress_mod
from electrical_engineer.ui_server.app import create_app


def _write_run(runs: Path, rid: str, *, recipe_id: str, unchecked: bool) -> None:
    folder = runs / rid
    folder.mkdir(parents=True)
    (folder / "summary.json").write_text(
        json.dumps({"recipe_id": recipe_id, "unchecked": unchecked}),
        encoding="utf-8",
    )


def test_run_count_and_newly_unlocked(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(progress_mod, "progress_dir", lambda cwd=None: tmp_path / "learn")
    monkeypatch.setattr(progress_mod, "progress_path", lambda cwd=None: tmp_path / "learn" / "progress.json")
    runs = tmp_path / "runs"
    _write_run(runs, "r1", recipe_id="solve-circuit-problem", unchecked=False)
    first = achievements_mod.evaluate(None, runs)
    assert "first-solve" in first["newly_unlocked"]
    second = achievements_mod.evaluate(None, runs)
    assert "first-solve" not in second["newly_unlocked"]
    badge = next(a for a in second["achievements"] if a["id"] == "first-solve")
    assert badge["unlocked_at"] is not None


def test_pack_first_and_topics(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(progress_mod, "progress_dir", lambda cwd=None: tmp_path / "learn")
    monkeypatch.setattr(progress_mod, "progress_path", lambda cwd=None: tmp_path / "learn" / "progress.json")
    runs = tmp_path / "runs"
    _write_run(runs, "r1", recipe_id="smib-swing-study", unchecked=False)
    out = achievements_mod.evaluate(None, runs)
    ids = {a["id"] for a in out["achievements"] if a["unlocked_at"]}
    assert "pack-first:power" in ids
    # mark topics
    data = progress_mod.load(None)
    for i in range(10):
        data["topics_done"][f"fake/{i}"] = "2026-01-01T00:00:00Z"
    progress_mod.save(None, data)
    out2 = achievements_mod.evaluate(None, runs)
    assert any(a["id"] == "topics-10" and a["unlocked_at"] for a in out2["achievements"])


def test_labs_and_api(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(progress_mod, "progress_dir", lambda cwd=None: tmp_path / "learn")
    monkeypatch.setattr(progress_mod, "progress_path", lambda cwd=None: tmp_path / "learn" / "progress.json")
    data = progress_mod._empty()
    for lab in ("rectifier", "converter", "idmt", "lead"):
        data["labs_opened"][lab] = "2026-01-01T00:00:00Z"
    progress_mod.save(None, data)
    out = achievements_mod.evaluate(None, tmp_path / "runs")
    assert any(a["id"] == "lab-explorer" and a["unlocked_at"] for a in out["achievements"])
    client = TestClient(create_app())
    body = client.get("/api/learn/achievements").json()
    assert "achievements" in body
    assert "newly_unlocked" in body
