"""Circuit Visual Kit."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme


def render_schematic_divider(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    """Voltage divider (R1=1k, R2=1k, Vin=10V) with engine-sourced Vout=5V."""
    v_in = 10.0
    r1, r2 = 1000.0, 1000.0
    v_out = v_in * r2 / (r1 + r2)
    try:
        import schemdraw
        import schemdraw.elements as elm

        theme = get_theme(theme_name)
        d = schemdraw.Drawing()
        d.config(color=theme.ink, bgcolor=theme.bg, font="sans-serif", fontsize=10)
        d += (elm.SourceV().up().label(f"{v_in:.0f} V"))
        d += (elm.Resistor().right().label(f"{r1/1000:.0f} kΩ"))
        d += (elm.Resistor().down().label(f"{r2/1000:.0f} kΩ"))
        d += (elm.Ground())
        d += (elm.Line().left())
        out_dir.mkdir(parents=True, exist_ok=True)
        png = out_dir / "schematic.divider.png"
        d.save(str(png))
        return {
            "png": str(png),
            "meta": {"component_id": "schematic.divider", "Vout": v_out, "backend": "schemdraw"},
        }
    except ImportError:
        import matplotlib.pyplot as plt

        theme = get_theme(theme_name)
        fig, ax = plt.subplots(figsize=(theme.fig_w * 0.9, theme.fig_h * 0.7))
        apply_theme(ax, theme)
        ax.axis("off")
        ax.annotate(
            f"Divider: $V_{{out}}={v_out:.2f}$ V (schemdraw not installed)",
            (0.5, 0.5),
            ha="center",
            fontsize=theme.label_size,
            color=theme.ink,
        )
        png = out_dir / "schematic.divider.png"
        fig.savefig(png, dpi=theme.dpi, bbox_inches="tight")
        plt.close(fig)
        return {"png": str(png), "meta": {"component_id": "schematic.divider", "Vout": v_out, "backend": "fallback"}}


def render_phasor_diagram(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:

    import matplotlib.pyplot as plt

    v = complex(120.0, 0.0)
    i = complex(2.0, -0.4)
    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(theme.fig_w * 0.75, theme.fig_h * 0.75))
    apply_theme(ax, theme)
    ax.axhline(0, color=theme.hairline, linewidth=0.8)
    ax.axvline(0, color=theme.hairline, linewidth=0.8)
    ax.arrow(0, 0, v.real, v.imag, head_width=4, head_length=6, color=theme.primary, length_includes_head=True)
    ax.arrow(0, 0, i.real * 30, i.imag * 30, head_width=4, head_length=6, color=theme.accent, length_includes_head=True)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Real")
    ax.set_ylabel("Imaginary")
    ax.set_title(f"Phasor diagram ($|V|={abs(v):.0f}$ V, $|I|={abs(i):.2f}$ A)")
    png = out_dir / "waveform.phasor.png"
    fig.tight_layout()
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight")
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "waveform.phasor", "V_mag": abs(v), "I_mag": abs(i)}}
