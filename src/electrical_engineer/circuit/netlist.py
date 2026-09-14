"""Compile an allowlisted circuit graph to a SPICE netlist. Does not simulate."""

from __future__ import annotations

from typing import Any


class CompileError(ValueError):
    pass


def compile_netlist(graph: dict[str, Any]) -> str:
    nodes = list(graph.get("nodes") or [])
    edges = list(graph.get("edges") or [])
    if not any(n.get("type") == "ground" for n in nodes):
        raise CompileError("missing ground")
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        parent[ra] = rb

    for edge in edges:
        union(str(edge["from"]), str(edge["to"]))

    ground_roots = set()
    for node in nodes:
        if node.get("type") == "ground":
            ground_roots.add(find(f"{node['id']}.n1"))

    spice_of: dict[str, int] = {}
    next_id = 1

    def spice(port: str) -> int:
        nonlocal next_id
        root = find(port)
        if root in ground_roots:
            return 0
        if root not in spice_of:
            spice_of[root] = next_id
            next_id += 1
        return spice_of[root]

    lines = ["* arc.circuit.v1"]
    for node in nodes:
        kind = node.get("type")
        if kind == "ground":
            continue
        n1 = spice(f"{node['id']}.n1")
        n2 = spice(f"{node['id']}.n2")
        ref = str(node.get("refdes") or node["id"])
        val = node.get("value")
        if val is None:
            raise CompileError(f"missing value for {ref}")
        if kind == "source_v":
            lines.append(f"{ref} {n1} {n2} DC {val}")
        elif kind in {"resistor", "capacitor", "inductor"}:
            lines.append(f"{ref} {n1} {n2} {val}")
        else:
            raise CompileError(f"unknown type {kind}")
    lines.append(".end")
    return "\n".join(lines) + "\n"
