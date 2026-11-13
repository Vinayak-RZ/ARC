"""Render Visual Kit components; numeric props must come from engines."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.engines.smib_swing import SmibCase
from electrical_engineer.visual_kit.animation import render_swing_fault_animation
from electrical_engineer.visual_kit.design_tokens import ThemeName
from electrical_engineer.visual_kit.render_circuit import (
    render_phasor_diagram,
    render_schematic_divider,
)
from electrical_engineer.visual_kit.render_control import (
    render_control_bode,
    render_control_nyquist,
    render_control_root_locus,
    render_control_step,
)
from electrical_engineer.visual_kit.render_misc import (
    render_control_block_diagram,
    render_power_oneline,
)
from electrical_engineer.visual_kit.render_power import (
    render_agc_trace,
    render_dispatch_curve,
    render_swing_equal_area,
)


def _smib_case(props: dict[str, Any]) -> SmibCase | None:
    fields = set(SmibCase.__dataclass_fields__)
    data = {k: v for k, v in props.items() if k in fields}
    return SmibCase(**data) if data else None


def _theme(props: dict[str, Any]) -> ThemeName:
    t = str(props.get("theme", "light"))
    return "dark" if t == "dark" else "light"


_COMPONENTS = {
    "power.swing_equal_area": lambda out, props: render_swing_equal_area(
        out, _smib_case(props), theme_name=_theme(props)
    ),
    "power.agc_trace": lambda out, props: render_agc_trace(out, theme_name=_theme(props)),
    "power.dispatch_curve": lambda out, props: render_dispatch_curve(
        out, float(props.get("PD", 500.0)), theme_name=_theme(props)
    ),
    "power.swing_animation": lambda out, props: render_swing_fault_animation(out),
    "control.bode": lambda out, props: render_control_bode(out, theme_name=_theme(props)),
    "control.step": lambda out, props: render_control_step(out, theme_name=_theme(props)),
    "control.root_locus": lambda out, props: render_control_root_locus(out, theme_name=_theme(props)),
    "control.nyquist": lambda out, props: render_control_nyquist(out, theme_name=_theme(props)),
    "schematic.divider": lambda out, props: render_schematic_divider(out, theme_name=_theme(props)),
    "waveform.phasor": lambda out, props: render_phasor_diagram(out, theme_name=_theme(props)),
    "control.block_diagram": lambda out, props: render_control_block_diagram(
        out, theme_name=_theme(props), props=props
    ),
    "power.oneline_bus": lambda out, props: render_power_oneline(out, theme_name=_theme(props)),
}


def render_component(component_id: str, out_dir: Path, props: dict[str, Any] | None = None) -> dict[str, Any]:
    props = props or {}
    fn = _COMPONENTS.get(component_id)
    if fn is None:
        raise ValueError(f"unknown visual component: {component_id}")
    return fn(out_dir, props)
