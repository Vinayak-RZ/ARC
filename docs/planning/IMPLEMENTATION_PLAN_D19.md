# Arc — D19/D20 Master Execution Plan (archive)

> **Historical.** Live execution is [`../../LOOP_GRAPH.md`](../../LOOP_GRAPH.md) (UG EE knowledge corpus).
>
> Nawab **project** profile + **graph-of-loops** §19.  
> **This archived graph:** [`LOOP_GRAPH_D19.md`](LOOP_GRAPH_D19.md)  
> **Loop plans:** [`plans/loops/`](../../plans/loops/) · index [`plans/README.md`](../../plans/README.md)  
> Gate 0: [`GATE_0.md`](GATE_0.md)  
> H1 archive: [`IMPLEMENTATION_PLAN_H1.md`](IMPLEMENTATION_PLAN_H1.md)

XOR: `graph-engineering` is not loaded. [`EXECUTION_GRAPH.md`](EXECUTION_GRAPH.md) is historical.

---

## §0 Plan metadata

| Field | Value |
|-------|-------|
| **Profile** | project |
| **Mode** | project |
| **Stack** | Python 3.11+ `uv`/hatchling; FastAPI + Vite/React + Zustand + DESIGN-coinbase; stdio MCP; RAG facade |
| **Base branch** | `main` |
| **Feature branch** | `cursor/d19-loop-graph-572f` |
| **User commit budget** | no cap (coalesce; ~44) |
| **Delivery** | repo IMPLEMENTATION_PLAN + LOOP_GRAPH + plans/loops |
| **Supersedes** | H1 EXECUTION_GRAPH **for execution** |
| **Authority** | PID / PRD / ARCHITECTURE (accepted for this graph at D0) |
| **Lead** | git, gates, PR; subagents do not commit |

---

## §1 North star

**Objective:** Any in-bound UG EE question has a complete co-solver path (capability check or exact `unchecked`), visible in a two-band localhost UI, driveable via 5–7 MCP verbs — proven by boot, queued trials, and a README that names the boot command.

**P0:** capability bind; 5–7 ACI including `propose_composition`; two-band + observation; FR9 no mint; CLI classifier without host; every pack path (not gold depth); RAG ingest; ChatGPT desktop contract; C4 stub kept; UX empty/error/a11y.

**Later:** HTTP MCP, BYOK, C5 sim, large gold, PyPI.

**Non-goals:** H4/H5, Python specialist fan-out, Python composition chat, faculty LMS, PG, civil/mech, ChatGPT web, `0.0.0.0`, Cordis, copyrighted books in git, inventing capability ids, visual rebrand.

---

## §2 Prerequisites

Gate 0 closed. H1 on `main`. `graph-of-loops` vendored (V0). `.specify/` exists (analyze/converge only). MATLAB optional.

---

## §3 Authority

PID, PRD, ARCHITECTURE, WORKFLOWS, curriculum-map, CANNOT_DO, `docs/PRODUCT.md`, `docs/planning/FR_TRACE.md`, `DECISIONS.md`, this file (§0–§18), `LOOP_GRAPH.md` (execute).

---

## §4–§8

Architecture, workstreams, spawns, waves, and todos: **[`LOOP_GRAPH_D19.md`](LOOP_GRAPH_D19.md)**. File ownership is per loop write paths. Parallel makers 2–4, disjoint.

---

## §9 Commit matrix

One conventional commit per passed loop slice (tests in the same commit). See loop plans’ Commits tables. Coalesce inside a loop; do not nest a second graph.

---

## §10–§17

Fast CI: `uv run ruff check . && uv run pytest -q`. Stops in loop plans. Orchestrator: `./scripts/validate.sh`. Rollout N/A (local). Exit: LOOP_GRAPH lifecycle + FR_TRACE + T1 queue. Risks: scope creep via speckit-converge (escalate); write-path overlap; impeccable teach vs DESIGN-coinbase.

---

## §18 Execution protocol

Do **not** run linear nawab §18. Run `.cursor/skills/graph-of-loops/EXECUTE.md`. Resume from `LOOP_GRAPH.md` wave status + `plans/loops/<id>.state.json`. Never re-ask Gate 0. Never redo `passed`.

---

## §19 Execution graph

**Filled:** [`LOOP_GRAPH_D19.md`](LOOP_GRAPH_D19.md) (graph-of-loops). Graph-engineering `EXECUTION_GRAPH.md` is not live.
