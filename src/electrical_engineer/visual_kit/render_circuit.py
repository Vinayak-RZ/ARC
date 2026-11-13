"""Circuit Visual Kit."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme


def render_schematic_divider(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    """Voltage divider with ngspice or DC solver annotations."""
    from electrical_engineer.visual_kit.divider_solve import solve_divider

    solved = solve_divider()
    v_in, v_out, i_a = solved["V_in"], solved["V_out"], solved["I"]
    r1, r2 = solved["R1"], solved["R2"]
    try:
        import schemdraw
        import schemdraw.elements as elm

        theme = get_theme(theme_name)
        out_dir.mkdir(parents=True, exist_ok=True)
        png = out_dir / "schematic.divider.png"
        with schemdraw.Drawing(show=False, unit=3.0, inches_per_unit=0.45) as d:
            d.config(
                color=theme.ink,
                bgcolor=theme.bg,
                font="DejaVu Sans",
                fontsize=11,
                lw=2.0,
            )
            d += elm.SourceV().up().label(f"{v_in:.1f} V", loc="top")
            d += elm.Resistor().right().label(f"$R_1={r1/1000:.0f}$ kΩ")
            d += elm.Dot().label(f"$V_{{out}}={v_out:.3f}$ V\n$I={i_a*1e3:.2f}$ mA", loc="right")
            d += elm.Resistor().down().label(f"$R_2={r2/1000:.0f}$ kΩ")
            d += elm.Ground()
            d += elm.Line().left()
            d.save(str(png), dpi=theme.dpi)
        return {
            "png": str(png),
            "meta": {
                "component_id": "schematic.divider",
                "backend": "schemdraw",
                "solver": "ngspice" if solved.get("spice_used") else "dc",
            "V_out_spice": solved.get("V_out_spice"),
                **solved,
            },
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
