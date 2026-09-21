"""Seed graph.json and control_diagram.json for the localhost UI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import default_graph_for, write_graph
from electrical_engineer.control.diagram import control_diagram_for_recipe, write_control_diagram


def seed_run_visuals(run_dir: Path, recipe_id: str, problem: dict[str, Any] | None) -> None:
    problem = problem or {}
    if not (run_dir / "graph.json").is_file():
        graph = default_graph_for(problem)
        if graph is None and recipe_id == "simulate-circuit":
            graph = default_graph_for({"kind": "series_rlc", **problem})
        if graph is not None:
            write_graph(run_dir, graph)
    if not (run_dir / "control_diagram.json").is_file():
        diagram = control_diagram_for_recipe(recipe_id, problem)
        if diagram is not None:
            write_control_diagram(run_dir, diagram)
