# State of Arc

Last updated: 2026-11-16 (commit `a437f4e` on `main`, plus collaboration-loop work on branch `cursor/collab-loop-f29f`).

This report is based on repository layout, source inspection, and commands run in the Cloud Agent environment (`uv sync --extra dev --extra engines --extra control`, `find`, `uv run pytest`).

## Product snapshot

Arc is a local EE co-solver: named YAML workflows, deterministic engine nodes (ngspice, python-control, MNA derive, reference library), MCP and CLI for coding agents, and a localhost Learning Lab UI (`electrical-engineer ui` on `127.0.0.1:8765`).

Headline on `main` (PR #61): Learn curriculum, Studio workspaces, 80 workflow recipes, circuit canvas with junctions.

## What works end to end

| Path | Evidence |
|------|----------|
| CLI `electrical-engineer run <recipe>` | `src/electrical_engineer/cli.py`, `runner/execute.py`; integration tests under `tests/integration/test_circuits_wf.py`, `test_derive_circuit.py` |
| Workflow catalog | `find workflows -name '*.yaml' \| wc -l` → **80** recipes |
| Derive + SPICE verify (circuits) | `workflows/circuits/derive-circuit.yaml`, nodes `run-circuit-derive`, `verify-circuit-spice` |
| Control Studio (UI + MCP + CLI) | `control_studio/*`, `ui_server/studio_routes.py`, `control_studio/mcp_tools.py`, SSE via `studio_events.py` |
| Circuit graph on runs (problem Diagram tab) | `arc.circuit.v1` in `circuit/graph.py`, `PUT /api/runs/{id}/graph` in `ui_server/app.py`, React Flow in `ui/src/slots/canvas/` |
| Studio circuit sandbox (local) | `ui/src/studio-engine/CircuitSandbox.jsx` |
| Teaching sim labs | Rectifier, converter, IDMT, lead in `ui/src/studio-engine/labs/` |
| Learn page | `learn/curriculum.yaml`, `ui_server/learn_routes.py`, Playwright `learn.spec.ts` |
| MCP core verbs | `mcp/server.py`: `list_workflows`, `retrieve`, `open_ui`, `simulate_attachment`, `propose_composition`, `label`, `run_workflow`, reference and trap tools |
| Circuit MCP | `arc_circuit_derive_verify`, image-to-netlist (confirm path), unit benchmark |
| Reference library | `reference/data/`, CLI `reference search|get|engine`, MCP `arc_reference_*` |
| Eval / benchmark | `eval/gold/` (48 `task.md` files on disk per `find eval/gold -name task.md \| wc -l`), `scripts/check_circuit_evals.py`, `benchmark_v01/` |

## Stubbed or partial

| Area | Status |
|------|--------|
| `photo-to-netlist` | Fixture/stub vision path; confirm without silent sim (`workflows/_cross/photo-to-netlist.yaml`, `nodes/photo.py`) |
| `control-diagram-to-model` | Documented stub-class; compose path exists but not full host photo loop |
| MATLAB / Simulink plant | Optional `matlab_mcp.py`; OSS providers remain primary |
| RAG multimodal | `rag/parse.py` stub adapter |
| ngspice in this VM | `simulator_status()` may report unavailable when `ngspice` is not on `PATH` (verify marks unchecked, not a fake pass) |

## Tests and CI

| Item | Count / note |
|------|----------------|
| Pytest modules | `find tests -name 'test_*.py' \| wc -l` → **173** (before new collab tests) |
| CI job | `.github/workflows/ci.yml`: `ruff`, `pytest -q`, hosts smoke, PSA/circuit eval scripts, RLVR smoke, visual tests, UI build + Playwright against live `electrical-engineer ui` |
| Local pytest (2026-11-16 VM, `main` + ui/dist) | **575 passed**, **18 failed**, **2 skipped** (failures included visual regression goldens, `test_ui_runs`, `test_studio_layout_css`, `test_t1_trials`) |
| New collaboration tests | `tests/integration/test_collab_loop.py`, `tests/unit/test_collab_lab_meta.py`, `ui/e2e/collab-lab.spec.ts` |

## How pieces connect today

```text
Agent (MCP/CLI) → mcp/server.py / cli.py
       → runner/execute.py → nodes/* (derive, spice, control, …)
       → runs/<id>/* artifacts (graph.json, evidentiary.json, plots)
       → ui_server/app.py REST → React UI (problem page, Studio, Learn)

Control Studio: MCP/CLI/UI → session JSON under .electrical-engineer/control_studio/
                → simulate/analyze → python-control → plots in runs/<session_id>/
```

## Gaps vs human–agent shared lab direction (before this branch)

1. No unified **lab artifact + provenance** on workflow runs for circuits (only `graph.json` without revision/op_log).
2. Derive workflow did **not** require seeding a Studio-visible circuit or control diagram tied to the run.
3. Problem page **Open in lab** pointed at teaching labs (`openExample.js`), not the agent-built model on the run.
4. Circuit side had **no MCP CRUD + simulate** parity with Control Studio.
5. **Live co-edit**: Control Studio had SSE; run graph edits did not publish events to the UI.
6. No **five-example** collab integration suite with verify-after-derive on the shared graph.

## Collaboration loop delivered on `cursor/collab-loop-f29f`

| Piece | Location |
|-------|----------|
| `lab_meta.json` + op_log on runs | `collab/lab_meta.py`, `circuit/run_session.py` |
| Verify-after-derive (flag mismatch only when sim runs) | `collab/workflow.py`, node `seed-circuit-lab`, `derive-circuit.yaml` |
| Circuit MCP lab tools | `arc_circuit_lab_*` in `circuit/mcp_lab.py` |
| Control finish on run | MCP `arc_lab_finish_control` |
| CLI | `electrical-engineer lab get|finish|simulate|open` |
| API | `GET /api/runs/{id}/lab`, `GET /api/runs/{id}/events` (SSE), enriched run detail `lab` |
| UI | Problem **Open in lab**; Studio `circuits` with `?run=` shared save + SSE; Diagram tab SSE refresh |

## Remaining gaps

- AC/tran probes on **compiled graphs** need tolerant golds when ngspice node numbering differs from hand templates.
- Control problems on the generic `solve-control-problem` path do not yet auto-call `arc_lab_finish_control` in the YAML DAG (MCP/CLI only).
- Full activity-feed UI for per-op human vs agent provenance (data is in `lab_meta.op_log`; minimal UI surfacing only).
- Visual regression failures on `main` in this VM (unrelated fonts/assets); CI on GitHub may differ.

## Commands reference

```bash
uv sync --extra dev --extra engines --extra control
uv run ruff check .
uv run pytest -q
cd ui && npm ci && npm run build
EE_NO_BROWSER=1 uv run electrical-engineer ui &
cd ui && STUDIO_URL=http://127.0.0.1:8765 npm run test:e2e
```