from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import BIND_HOST, create_app, should_open_browser

UI_SRC = Path("ui/src")


def _read(*parts: str) -> str:
    return (UI_SRC.joinpath(*parts)).read_text(encoding="utf-8")


def test_skip_link_and_no_wan() -> None:
    shell = _read("shell", "AppShell.jsx")
    root = _read("slots", "root.jsx")
    assert "Skip to workspace" in shell
    assert "aria-live" in root
    assert "unchecked === true" in root
    assert 'String(summary).includes("unchecked")' not in root
    assert "run.result" in root
    assert "run.canvas" in root
    canvas = _read("slots", "canvas", "Canvas.jsx")
    inspector = _read("slots", "canvas", "Inspector.jsx")
    assert "Confirm topology" in canvas
    assert "Save graph" in canvas
    assert ">Refdes<" in inspector.replace(" ", "") or "Refdes" in inspector
    assert "palette-btn" in _read("slots", "canvas", "Palette.jsx")
    assert "Waiting for topology confirm" in root
    assert "waiting-human" in root
    assert 'alt="Arc"' in _read("shell", "Sidebar.jsx")
    home = _read("pages", "HomePage.jsx")
    assert "Try an example" in home
    assert "/api/examples" in home
    assert "electrical-engineer mcp" in home
    assert "named runs · exact token unchecked" not in shell
    assert 'register("rag.inventory"' in root
    library = _read("slots", "library.jsx")
    assert "Add a PDF you have rights to; it stays on this machine." in library
    assert 'aria-label="Book"' in library
    assert "I have rights to this file." in library
    assert "Search tagged books" in library
    assert "No passages for that query." in library
    problems = _read("pages", "ProblemsPage.jsx")
    assert "No problems yet" in problems
    assert "product-sidebar" in _read("tokens.css")
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
