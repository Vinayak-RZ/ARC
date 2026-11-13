"""Token contrast sanity for light/dark verification UI."""

from __future__ import annotations


def _rel_lum(hex_rgb: str) -> float:
    h = hex_rgb.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

    def chan(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = chan(r), chan(g), chan(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    l1, l2 = _rel_lum(fg), _rel_lum(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def test_checked_tag_light_contrast() -> None:
    ratio = contrast("#1a6b45", "#e8f5ee")
    assert ratio >= 4.5


def test_dark_verification_link_contrast() -> None:
    ratio = contrast("#8fb0f5", "#12261c")
    assert ratio >= 4.5
