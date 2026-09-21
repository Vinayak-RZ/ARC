"""Compose run folders the way a host agent should (artifacts + evidentiary)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import write_graph
from electrical_engineer.control.diagram import write_control_diagram
from electrical_engineer.ui_diagrams.sidecars import attach_sidecar_artifacts

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = REPO_ROOT / "skills" / "ui-diagrams" / "examples"

DOMAIN_FILES: dict[str, tuple[str, str]] = {
    "rlc": ("rlc_graph.json", "graph"),
    "control": ("unity_feedback_control_diagram.json", "control"),
    "power": ("power_fault_control_diagram.json", "control"),
    "protection": ("protection_control_diagram.json", "control"),
    "drives": ("drives_control_diagram.json", "control"),
}

TITLES = {
    "rlc": "Agent trial — series RLC sheet",
    "control": "Agent trial — unity feedback system",
    "power": "Agent trial — LG fault SLD",
    "protection": "Agent trial — CT 50/51 feeder",
    "drives": "Agent trial — DC drive chain",
}


def trial_run_id(domain: str, stamp: str | None = None, suffix: str = "") -> str:
    """Unique run folder id per domain (second-level stamp is not enough alone)."""
    if domain not in DOMAIN_FILES:
        raise ValueError(f"unknown domain: {domain}")
    ts = stamp or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    tail = f"-{suffix}" if suffix else ""
    return f"trl-{domain}{tail}-{ts}"


def _load_example(filename: str) -> dict[str, Any]:
    path = EXAMPLES / filename
    return json.loads(path.read_text(encoding="utf-8"))


def write_agent_run(
    domain: str,
    runs_root: Path,
    payload: dict[str, Any],
    *,
    run_id: str,
    title: str,
    source_note: str,
    recipe_suffix: str = "",
) -> Path:
    if domain not in DOMAIN_FILES:
        raise ValueError(f"unknown domain: {domain}")
    _, kind = DOMAIN_FILES[domain]
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    if kind == "graph":
        write_graph(run_dir, payload)
    else:
        write_control_diagram(run_dir, payload)
        attach_sidecar_artifacts(domain, run_dir, payload)
    evid = {
        "title": title,
        "recipe_id": f"agent-ui-{domain}{recipe_suffix}",
        "unchecked": False,
        "value": "trial",
        "verifier": "agent-ui-diagram-trial",
    }
    (run_dir / "evidentiary.json").write_text(json.dumps(evid, indent=2), encoding="utf-8")
    (run_dir / "argument.md").write_text(source_note + "\n", encoding="utf-8")
    return run_dir


def compose_agent_trial_run(
    domain: str,
    runs_root: Path,
    *,
    run_id: str | None = None,
    payload: dict[str, Any] | None = None,
    title: str | None = None,
    source_note: str | None = None,
) -> Path:
    """Write a trial run using skill templates or an explicit payload."""
    filename, _ = DOMAIN_FILES[domain]
    body = payload if payload is not None else _load_example(filename)
    rid = run_id or trial_run_id(domain)
    note = source_note or f"Composed from `skills/ui-diagrams/examples/{filename}` per ui-diagrams skill."
    return write_agent_run(
        domain,
        runs_root,
        body,
        run_id=rid,
        title=title or TITLES[domain],
        source_note=note,
    )
