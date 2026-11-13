from pathlib import Path


def test_product_shell_sidebar_grid() -> None:
    css = Path("ui/src/tokens.css").read_text(encoding="utf-8")
    assert "grid-template-columns: 240px 1fr" in css
    assert "grid-template-columns: 56px 1fr" in css
    assert "transition: grid-template-columns 180ms ease" in css
    assert "sidebarLastToggledAt" in Path("ui/src/store.js").read_text(encoding="utf-8")
    assert "SIDEBAR_TRANSITION_MS" in Path("ui/src/shell/CommandPalette.jsx").read_text(encoding="utf-8")


def test_shortcut_component_source() -> None:
    src = Path("ui/src/components/Shortcut.jsx").read_text(encoding="utf-8")
    assert "navigator.platform" in src
    assert "⌘" in src
