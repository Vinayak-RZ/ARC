"""Forward-path blocks share one port rail (horizontal wires)."""

from __future__ import annotations

from electrical_engineer.control_studio.goldens import pid_dc_motor
from electrical_engineer.control_studio.layout import BLOCK_H, layout_chain


def _port_center_y(block: dict) -> float:
    return float(block["y"]) + BLOCK_H / 2


def test_forward_wires_share_port_center_y() -> None:
    diagram = layout_chain(pid_dc_motor())
    by_id = {b["id"]: b for b in diagram["blocks"]}
    centers = [_port_center_y(b) for b in diagram["blocks"] if b["type"] not in ("scope",)]
    assert centers, "expected blocks on diagram"
    rail = centers[0]
    for y in centers:
        assert abs(y - rail) < 1e-6, f"port rail mismatch: {y} vs {rail}"

    for wire in diagram.get("wires") or []:
        to = wire["to"]
        fr = wire["from"]
        if to.endswith(":feedback") or fr.endswith(":tap"):
            continue
        src_id = fr.split(":", 1)[0]
        tgt_id = to.split(":", 1)[0]
        sy = _port_center_y(by_id[src_id])
        ty = _port_center_y(by_id[tgt_id])
        assert abs(sy - ty) < 1e-6, f"forward wire {wire['id']} source y {sy} != target y {ty}"
