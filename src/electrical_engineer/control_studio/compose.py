"""Reduce studio diagrams to LTI models via python-control (BSD)."""

from __future__ import annotations

from typing import Any

from electrical_engineer.control_studio.library import dc_motor_tf, first_order_tf, pid_tf
from electrical_engineer.control_studio.schema import StudioError, parse_diagram
from electrical_engineer.engines.block_diagram import _parse_tf, compose_plant, plant_problem_dict


def _wire_index(diagram: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    """Map block_id -> list of {port, peer_block, peer_port, direction in|out}."""
    ins: dict[str, list[dict[str, str]]] = {}
    outs: dict[str, list[dict[str, str]]] = {}
    for w in diagram.get("wires") or []:
        fb, fp = w["from"].split(":", 1)
        tb, tp = w["to"].split(":", 1)
        outs.setdefault(fb, []).append({"port": fp, "peer": tb, "peer_port": tp})
        ins.setdefault(tb, []).append({"port": tp, "peer": fb, "peer_port": fp})
    return {"in": ins, "out": outs}


def _block_tf(block: dict[str, Any]):
    import control

    btype = block["type"]
    p = block.get("params") or {}
    if btype in ("step", "ramp", "sine", "scope"):
        return control.tf([1.0], [1.0])
    if btype == "gain":
        k = float(p.get("k") or p.get("gain") or 1.0)
        return control.tf([k], [1.0])
    if btype == "transfer_function":
        return _parse_tf({"tf": p.get("tf"), "num": p.get("num"), "den": p.get("den")})
    if btype == "plant_first_order":
        return first_order_tf(p)
    if btype == "plant_dc_motor":
        return dc_motor_tf(p)
    if btype == "pid":
        return pid_tf(p)
    if btype == "integrator":
        return control.tf([1.0], [1.0, 0.0])
    if btype == "derivative":
        return control.tf([1.0, 0.0], [1.0])
    if btype == "delay":
        tau = float(p.get("tau_s") or p.get("tau") or 0.1)
        # first-order Pade approx
        return control.pade(tau, 1)
    if btype == "state_space" and "A" in p and "B" in p and "C" in p and "D" in p:
        return control.ss(p["A"], p["B"], p["C"], p["D"])
    if btype == "sum":
        raise StudioError("sum is a junction, not a transfer block")
    return control.tf([1.0], [1.0])


def _find_blocks(diagram: dict[str, Any], btype: str) -> list[dict[str, Any]]:
    return [b for b in diagram.get("blocks") or [] if b.get("type") == btype]


def as_legacy_problem(diagram: dict[str, Any]) -> dict[str, Any]:
    """Map simple unity-feedback studio layouts to existing compose_plant format."""
    meta = diagram.get("meta") or {}
    if meta.get("unity_feedback"):
        return meta["unity_feedback"]
    blocks = diagram.get("blocks") or []
    by_id = {b["id"]: b for b in blocks}
    wires = _wire_index(diagram)
    sums = [b for b in blocks if b["type"] == "sum"]
    plants = [b for b in blocks if b["type"] in ("plant_first_order", "transfer_function", "plant_dc_motor")]
    if len(sums) == 1 and plants:
        s = sums[0]
        sid = s["id"]
        forward = None
        feedback = None
        for link in wires["in"].get(sid, []):
            peer = by_id.get(link["peer"])
            if peer and peer["type"] in ("step", "ramp", "sine"):
                continue
            if link["port"] in ("feedback", "in2", "neg"):
                feedback = link["peer"]
            else:
                forward = _forward_plant_id(link["peer"], by_id, wires)
        if forward and not feedback:
            for w in diagram.get("wires") or []:
                if w["to"].startswith(f"{sid}:") and "plant" in w["from"]:
                    feedback = w["from"].split(":", 1)[0]
        neg = str((s.get("params") or {}).get("signs") or "+-").startswith("+-")
        g_block = by_id.get(forward or plants[0]["id"], plants[0])
        h_block = by_id.get(feedback) if feedback else {"tf": "1"}
        g_tf = _tf_str(g_block)
        h_tf = _tf_str(h_block)
        return {
            "blocks": [
                {"id": "G", "tf": g_tf},
                {"id": "H", "tf": h_tf},
            ],
            "unity_feedback": {"forward": "G", "feedback": "H", "negative": neg},
        }
    raise StudioError("diagram is not reducible to unity feedback; set meta.unity_feedback")


def _tf_str(block: dict[str, Any]) -> str:
    p = block.get("params") or {}
    if p.get("tf"):
        return str(p["tf"])
    if block["type"] == "plant_first_order":
        k = p.get("k", 1)
        tau = p.get("tau", 1)
        return f"{k}/(s+{1/tau})" if tau else f"{k}/(s+1)"
    if block["type"] == "pid":
        return f"pid kp={p.get('kp',1)}"
    return "1"


def _forward_plant_id(start: str, by_id: dict[str, dict], wires: dict) -> str | None:
    cur = start
    seen: set[str] = set()
    while cur and cur not in seen:
        seen.add(cur)
        b = by_id.get(cur)
        if not b:
            return None
        if b["type"] in ("plant_first_order", "transfer_function", "plant_dc_motor"):
            return cur
        nxt = None
        for link in wires["out"].get(cur, []):
            if link["port"] == "out":
                nxt = link["peer"]
                break
        cur = nxt
    return None


def _unity_from_wired(diagram: dict[str, Any]):
    import control

    by_id = {b["id"]: b for b in diagram["blocks"]}
    wires = _wire_index(diagram)
    sums = [b for b in diagram["blocks"] if b["type"] == "sum"]
    if not sums:
        raise StudioError("no sum block")
    s = sums[0]
    sid = s["id"]
    neg = str((s.get("params") or {}).get("signs") or "+-").startswith("+-")
    sign = -1 if neg else 1
    forward_start = None
    feedback_id = None
    for link in wires["in"].get(sid, []):
        peer = link["peer"]
        if by_id.get(peer, {}).get("type") in ("step", "ramp", "sine"):
            continue
        if link["port"] in ("feedback", "in2"):
            feedback_id = peer
        else:
            forward_start = peer
    if not forward_start:
        for link in wires["out"].get(sid, []):
            if link["port"] in ("out", "y"):
                forward_start = link["peer"]
                break
    if not forward_start:
        raise StudioError("sum has no forward path")
    chain = _collect_series_from(forward_start, by_id, wires)
    g = control.tf([1.0], [1.0])
    for bid in chain:
        g = control.series(g, _block_tf(by_id[bid]))
    if feedback_id and feedback_id in by_id:
        h = _block_tf(by_id[feedback_id])
    else:
        h = control.tf([1.0], [1.0])
    sys = control.feedback(g, h, sign=sign)
    return sys, {"mode": "wired_unity", "forward_chain": chain, "feedback": feedback_id}


def _collect_series_from(start: str, by_id: dict[str, dict], wires: dict) -> list[str]:
    out: list[str] = []
    cur: str | None = start
    seen: set[str] = set()
    while cur and cur not in seen:
        seen.add(cur)
        b = by_id.get(cur)
        if not b:
            break
        if b["type"] == "scope":
            break
        if b["type"] not in ("step", "ramp", "sine", "sum"):
            out.append(cur)
        nxt = None
        for link in wires["out"].get(cur, []):
            if link["port"] in ("out", "y"):
                nxt = link["peer"]
        if not nxt:
            break
        if by_id.get(nxt, {}).get("type") == "scope":
            break
        cur = nxt
    return out


def compose_closed_loop(diagram: dict[str, Any]):
    """Return (lti_sys, summary dict)."""
    import control

    diagram = parse_diagram(diagram)
    meta = diagram.get("meta") or {}
    if isinstance(meta.get("unity_feedback"), dict):
        legacy = meta["unity_feedback"]
        sys, meta_c = compose_plant(legacy)
        return sys, {"mode": "unity_feedback_meta", **meta_c, **plant_problem_dict(legacy)}
    try:
        return _unity_from_wired(diagram)
    except StudioError:
        pass
    try:
        legacy = as_legacy_problem(diagram)
        sys, meta = compose_plant(legacy)
        return sys, {"mode": "unity_feedback", **meta, **plant_problem_dict(legacy)}
    except StudioError:
        pass
    meta = diagram.get("meta") or {}
    if isinstance(meta.get("num"), list) and isinstance(meta.get("den"), list):
        return control.tf(meta["num"], meta["den"]), {"mode": "explicit_tf", "num": meta["num"], "den": meta["den"]}
    raise StudioError("cannot compose diagram: add unity-feedback wiring or meta.num/den")


def series_blocks_from_diagram(diagram: dict[str, Any]):
    """Open-loop product along forward path (controller * plant) when wired step->sum->...->scope."""
    import control

    diagram = parse_diagram(diagram)
    by_id = {b["id"]: b for b in diagram["blocks"]}
    wires = _wire_index(diagram)
    scopes = _find_blocks(diagram, "scope")
    if not scopes:
        raise StudioError("scope block required")
    scope_id = scopes[0]["id"]
    preds = wires["in"].get(scope_id, [])
    if not preds:
        raise StudioError("scope input unwired")
    chain = _collect_series(preds[0]["peer"], by_id, wires)
    sys = control.tf([1.0], [1.0])
    for bid in chain:
        sys = control.series(sys, _block_tf(by_id[bid]))
    return sys, {"chain": chain}


def _collect_series(start: str, by_id: dict[str, dict], wires: dict) -> list[str]:
    out: list[str] = []
    cur: str | None = start
    seen: set[str] = set()
    while cur and cur not in seen:
        seen.add(cur)
        b = by_id.get(cur)
        if not b:
            break
        if b["type"] == "sum":
            break
        if b["type"] not in ("step", "ramp", "sine", "scope"):
            out.append(cur)
        nxt = None
        for link in wires["out"].get(cur, []):
            if link["port"] in ("out", "y"):
                nxt = link["peer"]
        cur = nxt
    return list(reversed(out))


def open_loop_with_controller(diagram: dict[str, Any]):
    """Controller times plant for loop shaping goldens."""
    ol, meta = series_blocks_from_diagram(diagram)
    return ol, meta
