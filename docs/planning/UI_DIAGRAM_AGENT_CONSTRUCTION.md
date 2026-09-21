# Agent UI diagram construction (planning note)

**Status:** Accepted for PR #42 workstream.

## Decision

Host agents (Cursor / Claude / Codex) construct Arc localhost figures by writing **allowlisted artifacts** into `runs/<id>/`, not by drawing in chat or generating bitmaps.

| Surface | Artifact | Enforced by |
|---------|----------|-------------|
| RLC sheet / editable canvas | `graph.json` (`arc.circuit.v1`) | `parse_graph`, UI caps |
| Study diagrams | `control_diagram.json` (`arc.control_diagram.v1`, `diagramKind`) | Static renderer + checker |

Kernel recipes may seed the same JSON via `seed_run_visuals`; agents may copy **`skills/ui-diagrams/examples/`** and edit numbers, then validate with `scripts/check_ui_diagram_artifacts.py`.

## Rationale

README-quality IITR figures require shared **visual law** (orthogonal SLDs, unity-feedback topology). Teaching hosts only via one-line pack mentions failed; skill + gold JSON + trials closes the loop.

## Consequences

- New skill `skills/ui-diagrams/SKILL.md` is the single method reference.
- `scripts/trial_agent_ui_diagrams.py` proves agent-compose paths render non-blank UI.
- UI React code remains the renderer of record; agents do not fork SVG by hand in production runs unless maintaining examples.
