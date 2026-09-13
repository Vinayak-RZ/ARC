from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app


def test_artifact_svg() -> None:
    client = TestClient(create_app())
    r = client.get("/api/runs/x/artifact.svg")
    assert r.status_code == 200
    assert "svg" in r.headers.get("content-type", "")


def test_artifact_falls_back_to_first_svg(tmp_path) -> None:
    d = tmp_path / "runs" / "c1"
    d.mkdir(parents=True)
    (d / "bode.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>")
    r = TestClient(create_app(tmp_path)).get("/api/runs/c1/artifact.svg")
    assert r.status_code == 200
    assert "svg" in r.text.lower()


def test_two_band_payload(tmp_path) -> None:
    d = tmp_path / "runs" / "band-1"
    d.mkdir(parents=True)
    (d / "evidentiary.json").write_text('{"recipe_id":"x","unchecked":true,"token":"unchecked"}')
    (d / "argument.md").write_text("method only; any extra numeral is unchecked")
    (d / "plan.md").write_text("# Job plan\n")
    (d / "observation.json").write_text('{"unchecked_reason":"unmatched"}')
    client = TestClient(create_app(tmp_path))
    detail = client.get("/api/runs/band-1").json()
    assert detail["state"] == "done"
    assert "unchecked" in detail["evidentiary"]
    assert "method only" in detail["argument"]
    assert "Job plan" in detail["plan"]
    assert "unmatched" in detail["observation"]
