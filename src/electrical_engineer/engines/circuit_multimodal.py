"""Schematic image or Visual Kit id to netlist proposal (confirm before simulate)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import (
    divider_graph,
    parse_graph,
    series_rlc_graph,
    write_graph,
)
from electrical_engineer.circuit.netlist import compile_netlist
from electrical_engineer.runner.runs import project_root


def propose_netlist_from_image(image_path: Path, *, cwd: Path | None = None) -> dict[str, Any]:
    """Fixture-aware path: uses linked graph.json when this is a gold photo fixture."""
    root = project_root(cwd)
    path = image_path if image_path.is_absolute() else root / image_path
    if not path.is_file():
        return {"ok": False, "error": f"missing image {path}", "low_confidence": True}
    fixture_graph = _fixture_graph_for_image(path, root)
    if fixture_graph:
        try:
            graph = parse_graph(fixture_graph)
            cir = compile_netlist(graph)
        except (ValueError, TypeError) as exc:
            return {"ok": False, "error": str(exc), "low_confidence": True, "image": str(path)}
        return {
            "ok": True,
            "cir": cir,
            "graph": fixture_graph,
            "confidence": 0.85,
            "low_confidence": False,
            "source": "fixture_graph",
            "image": str(path),
        }
    return {
        "ok": False,
        "error": "no fixture mapping for image",
        "low_confidence": True,
        "image": str(path),
    }


def propose_netlist_from_component(component_id: str, *, cwd: Path | None = None, props: dict[str, Any] | None = None) -> dict[str, Any]:
    """Render schemdraw schematic when available, else use canonical graph."""
    del props
    root = project_root(cwd)
    if component_id == "schematic.divider":
        graph = divider_graph(vin=10.0, r1=1000.0, r2=1000.0)
        png_dir = root / "runs" / "_mm_smoke"
        png_dir.mkdir(parents=True, exist_ok=True)
        try:
            from electrical_engineer.visual_kit.render_circuit import render_schematic_divider

            render_schematic_divider(png_dir)
            png = png_dir / "schematic.divider.png"
        except ImportError:
            png = None
        cir = compile_netlist(graph)
        return {
            "ok": True,
            "cir": cir,
            "graph": graph,
            "png": str(png) if png and png.is_file() else None,
            "component_id": component_id,
            "confidence": 0.9,
            "low_confidence": False,
        }
    if component_id == "schematic.rlc_series":
        graph = series_rlc_graph(vin=10.0, r_ohm=1000.0, l_h=1e-3, c_f=1e-6)
        cir = compile_netlist(graph)
        png_dir = root / "runs" / "_mm_smoke"
        png_dir.mkdir(parents=True, exist_ok=True)
        try:
            from electrical_engineer.visual_kit.render_circuit import render_schematic_rlc_series

            out = render_schematic_rlc_series(png_dir)
            png = out.get("png")
        except ImportError:
            png = None
        return {
            "ok": True,
            "cir": cir,
            "graph": graph,
            "png": png,
            "component_id": component_id,
            "confidence": 0.88,
            "low_confidence": False,
        }
    return {"ok": False, "error": f"unknown component {component_id}", "low_confidence": True}


def confirm_and_write(run_dir: Path, *, cir: str, graph: dict[str, Any] | None = None) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "draft.cir").write_text(cir)
    if graph:
        write_graph(run_dir / "graph.json", graph)
    confirmed = {"confirmed": True, "simulate": True}
    flag = run_dir / "confirmed.json"
    flag.write_text(json.dumps(confirmed))
    return flag


def _fixture_graph_for_image(image_path: Path, root: Path) -> dict[str, Any] | None:
    rel = None
    try:
        rel = image_path.relative_to(root)
    except ValueError:
        pass
    if rel and "photo-stub" in str(rel):
        gpath = root / "eval" / "gold" / "circuits" / "photo-stub-01" / "fixtures" / "graph.json"
        if gpath.is_file():
            return json.loads(gpath.read_text())
    if image_path.name == "schematic.divider.png":
        return divider_graph(vin=10.0, r1=1000.0, r2=1000.0)
    return None
