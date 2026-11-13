from pathlib import Path


def test_css_vars_match_design() -> None:
    css = Path("ui/src/tokens.css").read_text(encoding="utf-8")
    assert "--ee-color-canvas: #fafaf9" in css
    assert "--ee-color-ink: #202020" in css
    assert "--ee-color-primary: #2f6feb" in css
    assert "--ee-color-surface-strong: #efefed" in css
    assert "--ee-color-surface-dark: #202020" in css
    assert "--ee-color-primary-disabled: #b9cdfb" in css
    assert "--ee-semantic-up: #2f9e6a" in css
    assert "--ee-semantic-down: #d0312d" in css
    assert "Geist" in css
    assert "JetBrains Mono" in css
    assert "--ee-border-input: #8c8c87" in css
    assert "--ee-border-input-hover: #8a8a85" in css
    assert "--ee-color-hairline" in css
    assert ".status-badge" in css
    assert "var(--ee-color-surface-strong)" in css
    assert "outline: none" not in css
    assert ".asset-row:focus-visible" in css
