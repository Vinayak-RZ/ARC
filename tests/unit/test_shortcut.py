from pathlib import Path


def test_shortcut_platform_logic_in_source() -> None:
    src = Path("ui/src/components/Shortcut.jsx").read_text(encoding="utf-8")
    assert "navigator.platform" in src
    assert "Mac|iPhone|iPad|iPod" in src
    assert "MAC ?" in src and "Ctrl" in src and "⌘" in src
