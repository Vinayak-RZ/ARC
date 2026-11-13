"""Circuit Visual Kit."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme
from electrical_engineer.visual_kit.schematic_export import EXPORT_DPI, save_schematic_figure


def render_schematic_divider(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
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
        d = schemdraw.Drawing(show=False, unit=4.0, inches_per_unit=0.55)
        d.config(color=theme.ink, bgcolor=theme.bg, font="DejaVu Sans", fontsize=13, lw=2.2)
        d += elm.SourceV().up().label(f"$V_{{in}}={v_in:.1f}$ V", loc="top")
        d += elm.Resistor().right().label(f"$R_1={int(r1)}\\,\\Omega$")
        d += elm.Dot().label(f"$V_{{out}}={v_out:.3f}$ V\n$I={i_a*1e3:.2f}$ mA", loc="right")
        d += elm.Resistor().down().label(f"$R_2={int(r2)}\\,\\Omega$")
        d += elm.Ground()
        d += elm.Line().left()
        save_schematic_figure(d, png, theme)
        return {
            "png": str(png),
            "meta": {"component_id": "schematic.divider", "backend": "schemdraw", "dpi": EXPORT_DPI, **solved},
        }
    except ImportError:
        return _fallback_divider(out_dir, theme_name, v_out)


def render_schematic_rlc_series(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    """Series RLC step (10 V, 1 kΩ, 1 mH, 1 µF) with engine-style parameter labels."""
    v_in = 10.0
    r_ohm, l_h, c_f = 1000.0, 1e-3, 1e-6
    omega0 = 1.0 / (c_f**0.5 * l_h**0.5)
    try:
        import schemdraw
        import schemdraw.elements as elm

        theme = get_theme(theme_name)
        out_dir.mkdir(parents=True, exist_ok=True)
        png = out_dir / "schematic.rlc_series.png"
        d = schemdraw.Drawing(show=False, unit=3.5, inches_per_unit=0.5)
        d.config(color=theme.ink, bgcolor=theme.bg, font="DejaVu Sans", fontsize=12, lw=2.2)
        d += elm.SourceV().up().label(f"$V_s={v_in:.0f}$ V", loc="top")
        d += elm.Resistor().right().label(f"$R={int(r_ohm)}\\,\\Omega$")
        d += elm.Inductor().right().label("$L=1$ mH")
        d += elm.Capacitor().down().label("$C=1$ µF")
        d += elm.Ground()
        d += elm.Line().left().length(3.2)
        d += elm.Line().up()
        d += elm.Label().label(rf"$\omega_0 \approx {omega0:.0f}$ rad/s", ofst=(0, -0.6))
        save_schematic_figure(d, png, theme)
        return {
            "png": str(png),
            "meta": {"component_id": "schematic.rlc_series", "V_s": v_in, "omega0_rad_s": omega0},
        }
    except ImportError:
        return _fallback_divider(out_dir, theme_name, v_in, name="schematic.rlc_series")


def _fallback_divider(out_dir: Path, theme_name: ThemeName, val: float, name: str = "schematic.divider") -> dict[str, Any]:
    import matplotlib.pyplot as plt

    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    apply_theme(ax, theme)
    ax.axis("off")
    ax.annotate(f"{name} fallback", (0.5, 0.5), ha="center", color=theme.ink)
    png = out_dir / f"{name}.png"
    fig.savefig(png, dpi=EXPORT_DPI, bbox_inches="tight")
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": name, "Vout": val, "backend": "fallback"}}


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
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "waveform.phasor.png"
    fig.tight_layout()
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight")
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "waveform.phasor", "V_mag": abs(v), "I_mag": abs(i)}}
