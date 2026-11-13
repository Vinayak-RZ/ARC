# Node plan: B12 Arc Control Studio

| Field | Value |
|-------|-------|
| **Node id** | `B12` |
| **Job** | Control block-diagram editor + simulator (human and agent shared model) |
| **Wave** | 4 |
| **Depends on (data)** | B11 Visual Kit, B3 kernel control |
| **Write paths** | `src/electrical_engineer/control_studio/`, `ui/src/slots/control_studio/`, `docs/research/frontier-2026-11/06-control-studio-survey.md` |
| **Model** | inherit |

## Objective

Ship Arc Control Studio: JSON diagram schema, python-control backend, React Flow UI, MCP/CLI tools, goldens, and demo artifacts.

## Contract

**Output:** `{ "control_studio_goldens": 4, "mcp_tools": 10, "ui_view": "control-studio" }`

## Research

Survey: [06-control-studio-survey.md](../../research/frontier-2026-11/06-control-studio-survey.md) recommends python-control + xyflow.

## Verification

- Four reference diagrams simulate/analyze vs independent python-control
- MCP agent can build PID DC motor loop; UI edits Kp; margins re-analyze
- CI: `tests/unit/test_control_studio_*`, `tests/integration/test_control_studio_api.py`

## Docs-out

Listed in D2 final README refresh.
