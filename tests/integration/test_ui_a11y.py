from pathlib import Path

from electrical_engineer.ui_server.app import BIND_HOST, should_open_browser


def test_skip_link_and_no_wan() -> None:
    root = Path("ui/src/slots/root.jsx").read_text()
    assert "Skip to workspace" in root
    assert "aria-live" in root
    assert "obj.unchecked === true" in root
    assert 'String(summary).includes("unchecked")' not in root
    assert "run.evidentiary" in root
    assert "waiting-human" in root
    assert 'alt="Arc"' in root
    assert BIND_HOST == "127.0.0.1"


def test_ee_no_browser(monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_BROWSER", "1")
    assert should_open_browser() is False


def test_cli_ui_binds_loopback() -> None:
    text = Path("src/electrical_engineer/cli.py").read_text()
    assert "0.0.0.0" not in text
    assert "BIND_HOST" in text
    assert "should_open_browser" in text
    assert "ui_page_url" in text
