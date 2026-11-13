"""Unity-feedback block layout + wire-graph validation (Simulink contract)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from electrical_engineer.visual_kit.block_diagram_spec import plant_meta, unity_feedback_problem

GRID = 0.2
TAKEOFF_GRIDS = 1.5
_PORT_TOL = 0.08


def snap(x: float) -> float:
    return round(round(x / GRID) * GRID, 6)


@dataclass
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float

    def contains_interior(self, x: float, y: float, *, pad: float = 0.02) -> bool:
        return (self.x0 + pad) < x < (self.x1 - pad) and (self.y0 + pad) < y < (self.y1 - pad)


@dataclass
class WireDef:
    name: str
    points: list[tuple[float, float]]
    arrow_end: bool = False


@dataclass
class UnityFeedbackLayout:
    ports: dict[str, tuple[float, float]]
    takeoff: tuple[float, float]
    bus_junction: tuple[float, float]
    block_rects: dict[str, Rect]
    summer: tuple[float, float, float]
    ref: tuple[float, float]
    y_end: tuple[float, float]
    wires: list[WireDef] = field(default_factory=list)

    def anchor_points(self) -> set[tuple[float, float]]:
        nodes = {self.ref, self.y_end, self.takeoff, self.bus_junction}
        nodes.update(self.ports.values())
        return nodes


def build_unity_feedback_layout(props: dict[str, Any] | None = None) -> UnityFeedbackLayout:
    problem = unity_feedback_problem(props)
    _meta = plant_meta(problem)

    y = snap(3.2)
    y_fb = snap(1.0)
    x_ref = snap(0.4)
    cx = snap(2.4)
    r_sum = snap(0.34)
    bw, bh = snap(2.0), snap(0.8)
    x_g = snap(4.0)
    y_end_pt = (snap(9.2), y)

    port_r = (snap(cx - r_sum), y)
    port_sum_out = (snap(cx + r_sum), y)
    port_minus = (cx, snap(y - r_sum))
    port_g_in = (x_g, y)
    port_g_out = (snap(x_g + bw), y)
    port_h_in = (port_g_out[0], y_fb)
    port_h_out = (x_g, y_fb)
    takeoff = (snap(port_g_out[0]) + TAKEOFF_GRIDS * GRID, y)
    bus_junction = (port_minus[0], y_fb)

    ports = {
        "summer_plus": port_r,
        "summer_minus": port_minus,
        "summer_out": port_sum_out,
        "g_in": port_g_in,
        "g_out": port_g_out,
        "h_in": port_h_in,
        "h_out": port_h_out,
    }

    wires = [
        WireDef("R", [(x_ref, y), port_r], arrow_end=True),
        WireDef("E", [port_sum_out, port_g_in], arrow_end=True),
        WireDef("Y_to_tap", [port_g_out, takeoff], arrow_end=False),
        WireDef("Y_from_tap", [takeoff, y_end_pt], arrow_end=True),
        WireDef(
            "fb",
            [takeoff, (takeoff[0], y_fb), port_h_in],
            arrow_end=True,
        ),
        WireDef("B_bus", [port_h_out, bus_junction], arrow_end=False),
        WireDef("B_up", [bus_junction, port_minus], arrow_end=True),
    ]

    return UnityFeedbackLayout(
        ports=ports,
        takeoff=takeoff,
        bus_junction=bus_junction,
        block_rects={
            "G": Rect(x_g, y - bh / 2, x_g + bw, y + bh / 2),
            "H": Rect(x_g, y_fb - bh / 2, x_g + bw, y_fb + bh / 2),
        },
        summer=(cx, y, r_sum),
        ref=(x_ref, y),
        y_end=y_end_pt,
        wires=wires,
    )


def _expand_axis_segments(points: list[tuple[float, float]]) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        if abs(a[0] - b[0]) < 1e-9:
            y0, y1 = sorted((a[1], b[1]))
            segs.append(((a[0], y0), (a[0], y1)))
        elif abs(a[1] - b[1]) < 1e-9:
            x0, x1 = sorted((a[0], b[0]))
            segs.append(((x0, a[1]), (x1, a[1])))
        else:
            elbow = (b[0], a[1])
            segs.append((a, elbow))
            segs.append((elbow, b))
    return segs


def _near(p: tuple[float, float], q: tuple[float, float], tol: float = _PORT_TOL) -> bool:
    return abs(p[0] - q[0]) <= tol and abs(p[1] - q[1]) <= tol


def _on_anchor(p: tuple[float, float], layout: UnityFeedbackLayout) -> bool:
    for pt in layout.anchor_points():
        if _near(p, pt):
            return True
    return False


def _h_crosses_rect(y: float, xa: float, xb: float, rect: Rect) -> bool:
    x0, x1 = sorted((xa, xb))
    if y <= rect.y0 or y >= rect.y1:
        return False
    overlap = not (x1 <= rect.x0 or x0 >= rect.x1)
    if not overlap:
        return False
    inner_x0 = max(x0, rect.x0)
    inner_x1 = min(x1, rect.x1)
    return inner_x1 - inner_x0 > 2 * _PORT_TOL


def _v_crosses_rect(x: float, ya: float, yb: float, rect: Rect) -> bool:
    y0, y1 = sorted((ya, yb))
    if x <= rect.x0 or x >= rect.x1:
        return False
    overlap = not (y1 <= rect.y0 or y0 >= rect.y1)
    if not overlap:
        return False
    inner_y0 = max(y0, rect.y0)
    inner_y1 = min(y1, rect.y1)
    return inner_y1 - inner_y0 > 2 * _PORT_TOL


def _segment_hits_rect(
    a: tuple[float, float],
    b: tuple[float, float],
    rect: Rect,
) -> bool:
    if abs(a[0] - b[0]) < 1e-9:
        return _v_crosses_rect(a[0], a[1], b[1], rect)
    if abs(a[1] - b[1]) < 1e-9:
        return _h_crosses_rect(a[1], a[0], b[0], rect)
    return False


def _summer_interior_hit(a: tuple[float, float], b: tuple[float, float], layout: UnityFeedbackLayout) -> bool:
    cx, cy, r = layout.summer
    rect = Rect(cx - r, cy - r, cx + r, cy + r)
    return _segment_hits_rect(a, b, rect)


def _adjacency(layout: UnityFeedbackLayout) -> dict[tuple[float, float], set[tuple[float, float]]]:
    adj: dict[tuple[float, float], set[tuple[float, float]]] = {}
    for w in layout.wires:
        for i in range(len(w.points) - 1):
            a, b = w.points[i], w.points[i + 1]
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
    summer_nodes = (
        layout.ports["summer_plus"],
        layout.ports["summer_out"],
        layout.ports["summer_minus"],
    )
    for a in summer_nodes:
        for b in summer_nodes:
            if a != b:
                adj.setdefault(a, set()).add(b)
    g_in, g_out = layout.ports["g_in"], layout.ports["g_out"]
    adj.setdefault(g_in, set()).add(g_out)
    adj.setdefault(g_out, set()).add(g_in)
    h_in, h_out = layout.ports["h_in"], layout.ports["h_out"]
    adj.setdefault(h_in, set()).add(h_out)
    adj.setdefault(h_out, set()).add(h_in)
    return adj


def _reachable(adj: dict[tuple[float, float], set[tuple[float, float]]], start: tuple[float, float]) -> set[tuple[float, float]]:
    seen = {start}
    stack = [start]
    while stack:
        cur = stack.pop()
        for nxt in adj.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def validate_unity_feedback_layout(layout: UnityFeedbackLayout) -> None:
    g_out = layout.ports["g_out"]
    h_in = layout.ports["h_in"]
    if layout.takeoff[1] != g_out[1]:
        raise ValueError("takeoff must sit on forward wire height")
    min_tap = g_out[0] + (TAKEOFF_GRIDS - 0.25) * GRID
    if layout.takeoff[0] < min_tap:
        raise ValueError("takeoff must be to the right of G output port")
    if layout.takeoff[0] <= h_in[0]:
        raise ValueError("feedback vertical must sit right of H right edge")

    for w in layout.wires:
        if len(w.points) < 2:
            raise ValueError(f"wire {w.name} too short")
        if not _on_anchor(w.points[0], layout):
            raise ValueError(f"wire {w.name} start {w.points[0]} not on anchor")
        end = w.points[-1]
        if not _on_anchor(end, layout):
            raise ValueError(f"wire {w.name} end {end} not on anchor")
        if w.arrow_end and not (
            _near(end, layout.y_end) or any(_near(end, pt) for pt in layout.ports.values())
        ):
            raise ValueError(f"wire {w.name} arrow end {end} must land on port or Y")

    for w in layout.wires:
        for a, b in _expand_axis_segments(w.points):
            for rect in layout.block_rects.values():
                if _segment_hits_rect(a, b, rect):
                    raise ValueError(f"wire {w.name} crosses block interior")
            if _summer_interior_hit(a, b, layout) and w.name not in ("B_up", "E", "R"):
                raise ValueError(f"wire {w.name} crosses summer interior")

    adj = _adjacency(layout)
    reach = _reachable(adj, layout.ref)
    if layout.y_end not in reach and not any(
        abs(layout.y_end[0] - p[0]) < 1e-6 and abs(layout.y_end[1] - p[1]) < 1e-6 for p in reach
    ):
        raise ValueError("forward path R to Y not connected")
    if layout.ports["summer_minus"] not in _reachable(adj, layout.takeoff):
        raise ValueError("feedback loop not connected from takeoff to summer minus")
    if layout.ports["h_in"] not in _reachable(adj, layout.takeoff):
        raise ValueError("feedback path must reach H input from takeoff")
