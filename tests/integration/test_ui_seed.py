from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.ui_server import app as ui_app
from electrical_engineer.ui_server.app import clear_sample_runs, create_app, seed_sample_runs


def test_seed_marks_and_lists_samples(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    runs = tmp_path / "runs"
    runs.mkdir()

    def fake_execute(recipe_id, cwd=None, problem=None):
        rid = f"sample-{recipe_id.split('-')[0]}"
        folder = runs / rid
        folder.mkdir(exist_ok=True)
        (folder / "summary.json").write_text(
            f'{{"recipe_id":"{recipe_id}","unchecked":false,"title":"Sample {rid}"}}',
            encoding="utf-8",
        )
        return {"run_id": rid, "summary": {"unchecked": False}}

    monkeypatch.setattr("electrical_engineer.runner.execute.execute", fake_execute)
    n = seed_sample_runs(tmp_path, runs)
    assert n >= 1
    assert any((p / "sample.json").is_file() for p in runs.iterdir() if p.is_dir())

    client = TestClient(create_app(tmp_path))
    body = client.get("/api/runs").json()
    assert body["seeding"] is False
    samples = [r for r in body["runs"] if r.get("sample")]
    assert len(samples) >= 1

    removed = client.delete("/api/runs/samples").json()["removed"]
    assert removed >= 1
    assert clear_sample_runs(runs) == 0


def test_no_seed_when_env_set(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    called = {"n": 0}

    def boom(*_a, **_k):
        called["n"] += 1
        raise AssertionError("seed should not run")

    monkeypatch.setattr(ui_app, "seed_sample_runs", boom)
    TestClient(create_app(tmp_path))
    assert called["n"] == 0
