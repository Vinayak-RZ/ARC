# Arc ship graph (W1–W7) — Master Execution Plan

> Nawab **standard** profile. Supersedes: none (orthogonal to H1/D19 plans).  
> Delivery: `docs/planning/IMPLEMENTATION_PLAN_SHIP.md` + `LOOP_GRAPH_SHIP.md`.

## §0 Plan metadata

| Field | Value |
|-------|-------|
| **Profile** | standard |
| **Mode** | feature |
| **Stack** | Python 3.11+ / FastAPI / Vite React UI |
| **Base branch** | `main` |
| **Feature branch** | `cursor/graph-ship-waves-79c5` |
| **User commit budget** | coalesce (~8–12) |
| **Delivery** | repo |
| **Supersedes** | none |
| **Authority** | `docs/PID.md`, `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/curriculum-map.md` |
| **Estimated commits** | 8–12 |
| **Lead agent** | cloud agent (graph-of-loops) |

## §1 North star & scope boundary

### Objective

UG EE student can run **real** RLC (ngspice), control Bode/step (python-control), and power fault/load-flow demos in CLI and localhost UI, with IITR Y1–Y3 gaps closed or documented, and README domain screenshots.

### Deliverables

- Engine backends under `src/electrical_engineer/engines/`
- Optional deps: `pyproject.toml` extras `sim`, `control`, `power`, `engines`
- Control/power UI panels + artifact API routes
- Fault gold `eval/gold/power/*`, recipe `simulate-power-fault`
- `docs/planning/IITR_GAP_MATRIX.md`, QA artifacts, `docs/media/*` wired in README

### Non-goals

PG-only EE, MATLAB licence path, PyPI, marketing site, KiCad (per Gate 0).

### Priority

**P0:** W1–W7 table in `LOOP_GRAPH_SHIP.md`. **P1:** numba speed for pandapower.

## §2 Prerequisites & blockers

| Item | Status | Blocks | Resolution |
|------|--------|--------|------------|
| ngspice + libngspice | done in cloud image | W1 | apt packages |
| PyPI `control` package | done | W1 | extra name `control` not `python-control` |
| UI `npm ci` | done | W2 | `ui/package-lock.json` |

## §3 Authority & artifact map

| Document | Path | Role |
|----------|------|------|
| Gate 0 | `docs/planning/GATE_0.md` | Locked answers |
| Loop graph | `docs/planning/LOOP_GRAPH_SHIP.md` | Wave stops |
| IITR gaps | `docs/planning/IITR_GAP_MATRIX.md` | Gap matrix |
| QA | `docs/planning/QA_CHECKLIST_SHIP.md` | W5 checklist |

## §4 Architecture & system map

Providers remain registry activities; new **engines** package implements bodies for `run-spice`, `run-python-control`, `run-load-flow`. UI reads `/api/runs/{id}/file/*`.

## §5 Workstreams

| ID | Owns | Depends |
|----|------|---------|
| WS-E | `src/electrical_engineer/engines/**`, `nodes/sim.py` | ngspice |
| WS-U | `ui/**`, `ui_server/app.py` | WS-E |
| WS-G | `eval/gold/power`, tests | WS-E |
| WS-D | planning + README media | WS-U, WS-G |

## §6 Agent orchestration

§6 N/A — lead executes sequentially (single cloud agent).

## §7 Phase map

| Phase | Waves | Exit gate |
|-------|-------|-----------|
| A | W1 engines | CLI demos checked when extras installed |
| B | W2–W4 UI | `npm run build`, manual visual pass |
| C | W3 faults | `pytest tests/integration/test_power_faults.py` |
| D | W5 QA | `validate.sh` |
| E | W6 IITR | matrix rows shipped |
| F | W7 README | `docs/media` + README links |

## §8 Todo registry

N/A — tracked in `LOOP_GRAPH_SHIP.md` wave status.

## §9 Commit matrix (coalesced)

| # | Commit | Contents |
|---|--------|----------|
| 1 | `docs(planning): gate-0 and ship loop graph` | GATE_0, LOOP_GRAPH, IMPLEMENTATION_PLAN |
| 2 | `feat(engines): ngspice control pandapower backends` | engines/*, sim.py, pyproject extras |
| 3 | `fix(kernel): pass verified engine values through explain` | registry.py, photo.py, sim check |
| 4 | `feat(ui): control and power engine panels` | UI + app routes |
| 5 | `feat(power): fault recipe and gold fixtures` | workflow, eval, tests |
| 6 | `docs(planning): IITR gap matrix and QA` | matrix, QA checklist |
| 7 | `docs(readme): domain screenshots and engine install` | README, docs/media |
| 8 | `test: scenario bank annotate for installed engines` | kernel_harden bank json |

## §10 Test & CI strategy

| Tier | Command |
|------|---------|
| Fast | `uv run pytest -q` |
| Validate | `./scripts/validate.sh` |

## §11 Research log

| Topic | Choice | Record |
|-------|--------|--------|
| SPICE | ngspice CLI + PySpice import gate | engines/spice_runner.py |
| Control PyPI | package `control` | pyproject `control` extra |
| Faults | sequence + pandapower LF | power_runner.py |

## §12 Documentation sync

Update README, `docs/planning/*`, scenario bank when provider contract changes.

## §13 Quality gates

W5 checklist + pytest 199+ green before W7.

## §14 Validation

`./scripts/validate.sh` orchestrator.

## §15 Rollout

N/A — local-only OSS; no production cutover.

## §16 Exit criteria (P0)

- [ ] W1–W7 stop commands in `LOOP_GRAPH_SHIP.md` satisfied
- [ ] `uv run pytest -q` green
- [ ] Demos documented in `docs/planning/R1_BOOT_SHIP.md`

## §17 Risks

| Risk | Mitigation |
|------|------------|
| ngspice not on student laptop | honest `unchecked` + extras docs |
| PySpice/ngspice version skew | CLI path primary |

## §18 Execution protocol

Execute `LOOP_GRAPH_SHIP.md` waves in order; ponytail on code; coalesce commits per §9.

## §19 Execution graph

Filled as `docs/planning/LOOP_GRAPH_SHIP.md` (graph-of-loops, not graph-engineering).

## Open questions

None.
