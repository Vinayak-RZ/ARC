from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import BIND_HOST, create_app, should_open_browser


def test_skip_link_and_no_wan() -> None:
    root = Path("ui/src/slots/root.jsx").read_text(encoding="utf-8")
    assert "Skip to workspace" in root
    assert "aria-live" in root
    assert "unchecked === true" in root
    assert 'String(summary).includes("unchecked")' not in root
    assert "run.result" in root
    assert "run.canvas" in root
    assert "Confirm topology" in root
    assert "Waiting for topology confirm" in root
    assert "waiting-human" in root
    assert 'alt="Arc"' in root
    assert "MATLAB · coming next" in root
    assert "No saved runs yet" in root
    assert "electrical-engineer run" in root
    assert "named runs · exact token unchecked" not in root
    assert "nav-toggle" in root
    assert BIND_HOST == "127.0.0.1"


def test_brand_icon_is_png() -> None:
    r = TestClient(create_app()).get("/arc-icon.png")
    assert r.status_code == 200
    assert r.content[:8] == b"\x89PNG\r\n\x1a\n"
    assert "png" in r.headers.get("content-type", "")


def test_ee_no_browser(monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_BROWSER", "1")
    assert should_open_browser() is False


def test_cli_ui_binds_loopback() -> None:
    text = Path("src/electrical_engineer/cli.py").read_text()
    assert "0.0.0.0" not in text
    assert "BIND_HOST" in text
    assert "should_open_browser" in text
    assert "ui_page_url" in text
