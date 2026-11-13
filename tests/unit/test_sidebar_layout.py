from pathlib import Path


def test_product_shell_sidebar_grid() -> None:
    css = Path("ui/src/tokens.css").read_text(encoding="utf-8")
    assert "grid-template-columns: 240px 1fr" in css
    assert "grid-template-columns: 56px 1fr" in css
    assert "transition: grid-template-columns 180ms ease" in css
