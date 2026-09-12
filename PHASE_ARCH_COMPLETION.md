# PHASE_ARCH_COMPLETION — technical architecture (historical)

> **Historical.** Live architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (Accepted).

## Completed work

Phase A research notes, owner Q&A recorded, Proposed `docs/ARCHITECTURE.md` and `docs/WORKFLOWS.md`, ADR-0007, eval gold layout, doc sync.

## Files modified

- `research/notes/architecture-qa-gate.md` — owner answer list
- `docs/ARCHITECTURE.md`, `docs/WORKFLOWS.md` — Proposed
- `DECISIONS.md` — ADR-0007 proposed
- `eval/gold/` — layout + README
- Sync: `PROGRESS.md`, `IMPLEMENTATION_PLAN.md`, `PROJECT_OVERVIEW.md`, `docs/EXTENSIVE.md`, `README.md`, registers, `.gitignore` (`runs/`)

## Architectural changes

Specified (not shipped): Python 3.11+ YAML DAG runner, hybrid router that never invents DAGs, `run-recipe` depth 3, persistent localhost UI as a critical surface, tagged RAG + markdown memory, `eval/gold/`.

## Validation performed

`./scripts/research/validate-research.sh --full`

## Known issues

- Architecture and PRD are both **Proposed/draft** until owner accept
- No product code; empty gold packs
- agent-patterns MCP unreachable (MCP-PENDING)

## Next phase objectives

Owner reviews architecture (accept or list edits). After **PRD accept**, a new implementation nawab plan.

## What you learned

- Named EE workflows are for **answer quality** (RAG, citations, verified numbers), not for running a graph for its own sake
- A persistent local UI can stay H3 glue if it is a viewer/workspace and not a second agent loop
- Nested recipes need hard caps (depth, cycles, interrupt budget) or composition becomes a fork bomb
