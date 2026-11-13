"""High-DPI schematic export (min width for Visual Kit goldens)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

EXPORT_DPI = 200
MIN_WIDTH_PX = 1200


def save_schematic_figure(draw_obj, path: Path, theme) -> None:
    """Save schemdraw Drawing at publication width."""
    path.parent.mkdir(parents=True, exist_ok=True)
    draw_obj.draw()
    fig = getattr(draw_obj, "fig", None)
    if fig is not None:
        if hasattr(fig, "set_facecolor"):
            fig.set_facecolor(theme.canvas)
        elif hasattr(fig, "patch"):
            fig.patch.set_facecolor(theme.canvas)
        for axis in getattr(fig, "axes", []):
            axis.set_facecolor(theme.surface)
    draw_obj.save(str(path), dpi=EXPORT_DPI)
    with Image.open(path) as img:
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            bg = Image.new("RGB", img.size, theme.surface)
            bg.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[-1])
            img = bg
        elif theme.name == "light" and img.mode != "RGB":
            img = img.convert("RGB")
        w, h = img.size
        if w < MIN_WIDTH_PX:
            scale = MIN_WIDTH_PX / w
            img = img.resize((MIN_WIDTH_PX, int(h * scale)), Image.Resampling.LANCZOS)
        img.save(path, dpi=(EXPORT_DPI, EXPORT_DPI))
