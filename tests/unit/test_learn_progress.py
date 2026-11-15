"""Learn progress store and API."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.learn import progress as progress_mod
from electrical_engineer.ui_server.app import create_app


def test_round_trip(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    # need workflows + knowledge for project_root and curriculum
    (tmp_path / "workflows").mkdir()
    (tmp_path / ".electrical-engineer").mkdir()
    # use real curriculum keys via cwd=None — point progress dir via monkeypatch
    monkeypatch.setattr(progress_mod, "progress_dir", lambda cwd=None: tmp_path / "learn")
    monkeypatch.setattr(progress_mod, "progress_path", lambda cwd=None: tmp_path / "learn" / "progress.json")
    monkeypatch.setattr(
        progress_mod,
        "_known_topic_keys",
        lambda cwd=None: {"eec-303/rectifiers-control-laws"},
    )
    data = progress_mod.set_topic(None, "eec-303/rectifiers-control-laws", True)
    assert "eec-303/rectifiers-control-laws" in data["topics_done"]
    loaded = progress_mod.load(None)
    assert "eec-303/rectifiers-control-laws" in loaded["topics_done"]
    progress_mod.set_topic(None, "eec-303/rectifiers-control-laws", False)
    assert "eec-303/rectifiers-control-laws" not in progress_mod.load(None)["topics_done"]
    progress_mod.mark_lab(None, "rectifier")
    assert "rectifier" in progress_mod.load(None)["labs_opened"]


def test_corrupt_file(tmp_path: Path, monkeypatch) -> None:
    folder = tmp_path / "learn"
    folder.mkdir()
    path = folder / "progress.json"
    path.write_text("not-json", encoding="utf-8")
    monkeypatch.setattr(progress_mod, "progress_path", lambda cwd=None: path)
    monkeypatch.setattr(progress_mod, "progress_dir", lambda cwd=None: folder)
    data = progress_mod.load(None)
    assert data["topics_done"] == {}


def test_api_422_and_ok(tmp_path: Path, monkeypatch) -> None:
    # isolate progress writes
    monkeypatch.setattr(progress_mod, "progress_dir", lambda cwd=None: tmp_path / "learn")
    monkeypatch.setattr(progress_mod, "progress_path", lambda cwd=None: tmp_path / "learn" / "progress.json")
    monkeypatch.setattr(
        progress_mod,
        "_known_topic_keys",
        lambda cwd=None: {"eec-303/rectifiers-control-laws"},
    )
    client = TestClient(create_app())
    bad = client.post("/api/learn/progress", json={"topic": "nope", "done": True})
    assert bad.status_code == 422
    weird = client.post("/api/learn/progress", json={"foo": 1})
    assert weird.status_code == 422
    ok = client.post(
        "/api/learn/progress",
        json={"topic": "eec-303/rectifiers-control-laws", "done": True},
    )
    assert ok.status_code == 200
    body = ok.json()
    assert "eec-303/rectifiers-control-laws" in body["topics_done"]
    got = client.get("/api/learn/progress").json()
    assert "unlocked" not in got
    assert "eec-303/rectifiers-control-laws" in got["topics_done"]
