from pathlib import Path


def test_css_vars_match_design() -> None:
    css = Path("ui/src/tokens.css").read_text(encoding="utf-8")
    assert "--ee-color-canvas: #ffffff" in css
    assert "--ee-color-ink: #0a0b0d" in css
    assert "--ee-color-primary: #0052ff" in css
    assert "--ee-color-surface-strong: #eef0f3" in css
    assert "--ee-color-surface-dark: #0a0b0d" in css
    assert "--ee-color-primary-disabled: #a8b8cc" in css
    assert "--ee-semantic-up: #05b169" in css
    assert "--ee-semantic-down: #cf202f" in css
    assert "Inter" in css
    assert "JetBrains Mono" in css
    assert "--ee-color-hairline" in css
    assert ".badge-pill" in css
    assert "var(--ee-color-surface-strong)" in css
    assert "outline: none" not in css
    assert ".asset-row:focus-visible" in css
