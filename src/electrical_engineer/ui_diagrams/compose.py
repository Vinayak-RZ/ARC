"""Compose run folders the way a host agent should (artifacts + evidentiary)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import write_graph
from electrical_engineer.control.diagram import write_control_diagram

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = REPO_ROOT / "skills" / "ui-diagrams" / "examples"

DOMAIN_FILES: dict[str, tuple[str, str]] = {
    "rlc": ("rlc_graph.json", "graph"),
    "control": ("unity_feedback_control_diagram.json", "control"),
    "power": ("power_fault_control_diagram.json", "control"),
    "protection": ("protection_control_diagram.json", "control"),
    "drives": ("drives_control_diagram.json", "control"),
}


def trial_run_id(domain: str, stamp: str | None = None) -> str:
    """Unique run folder id per domain (second-level stamp is not enough alone)."""
    if domain not in DOMAIN_FILES:
        raise ValueError(f"unknown domain: {domain}")
    ts = stamp or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"trl-{domain}-{ts}"


def _load_example(filename: str) -> dict[str, Any]:
    path = EXAMPLES / filename
    return json.loads(path.read_text(encoding="utf-8"))


def compose_agent_trial_run(
    domain: str,
    runs_root: Path,
    *,
    run_id: str | None = None,
) -> Path:
    """Write a trial run using skill templates (agent copy-edit path, not README recipe seed)."""
    if domain not in DOMAIN_FILES:
        raise ValueError(f"unknown domain: {domain}")
    filename, kind = DOMAIN_FILES[domain]
    payload = _load_example(filename)
    rid = run_id or trial_run_id(domain)
    run_dir = runs_root / rid
    run_dir.mkdir(parents=True, exist_ok=True)
    if kind == "graph":
        write_graph(run_dir, payload)
    else:
        write_control_diagram(run_dir, payload)
    title = {
        "rlc": "Agent trial — series RLC sheet",
        "control": "Agent trial — unity feedback system",
        "power": "Agent trial — LG fault SLD",
        "protection": "Agent trial — CT 50/51 feeder",
        "drives": "Agent trial — DC drive chain",
    }[domain]
    evid = {
        "title": title,
        "recipe_id": f"agent-ui-{domain}",
        "unchecked": False,
        "value": "trial",
        "verifier": "agent-ui-diagram-trial",
    }
    (run_dir / "evidentiary.json").write_text(json.dumps(evid, indent=2), encoding="utf-8")
    (run_dir / "argument.md").write_text(
        f"Composed from `skills/ui-diagrams/examples/{filename}` per ui-diagrams skill.\n",
        encoding="utf-8",
    )
    return run_dir
