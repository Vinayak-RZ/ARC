# Simulink toolkit + host-spawned EE specialists — Master Execution Plan

> Nawab **lite** + **graph-engineering** §19.
> **The graph you run:** [`LOOP_GRAPH.md`](LOOP_GRAPH.md)
> **Node plans:** [`plans/simulink-agents-loops/`](plans/simulink-agents-loops/)
> Gate 0: [`docs/planning/GATE_0_SIMULINK_AGENTS.md`](docs/planning/GATE_0_SIMULINK_AGENTS.md)

XOR: not graphify. Archived skills-matlab graph: [`docs/planning/LOOP_GRAPH_SKILLS_MATLAB.md`](docs/planning/LOOP_GRAPH_SKILLS_MATLAB.md).

---

## §0 Plan metadata

| Field | Value |
|-------|-------|
| **Profile** | lite + §19 graph |
| **Mode** | feature |
| **Stack** | Python 3.11 kernel; host-native Cursor/Codex/Claude agents; optional MATLAB/Simulink MCP (kernel only) |
| **Base branch** | `main` (this branch continues unmerged skills-matlab work) |
| **Feature branch** | `cursor/ee-simulink-host-agents-37b3` |
| **User commit budget** | 12 |
| **Delivery** | repo IMPLEMENTATION_PLAN + LOOP_GRAPH + plans/simulink-agents-loops |
| **Supersedes** | live pointer; skills-matlab graph archived |
| **Authority** | Gate 0; PID; PRD; ARCHITECTURE §0.3; ADR-0015/0016 |
| **Lead** | git, gates, PR; subagents do not commit |

## §1 North star

The rented host can spawn named undergraduate EE specialists from files in this repo. Arc can call Simulink toolkit tools internally the same way it already calls MATLAB MCP. No second agent runtime. No host-attached Simulink MCP. No live MATLAB on CI.

## §9 Commit matrix

See [`LOOP_GRAPH.md`](LOOP_GRAPH.md) commit mapping. Budget 12.

## §16 Exit criteria

See Gate 0 P0 and LOOP_GRAPH lifecycle. `./scripts/validate.sh` must pass. Host `tools/list` has no MATLAB/Simulink names. README counts 12 spawnable specialists.

## §18 Execute

Follow [`LOOP_GRAPH.md`](LOOP_GRAPH.md) waves. Ponytail on every product-code write.

## §19

The graph is [`LOOP_GRAPH.md`](LOOP_GRAPH.md). Approving it started this execution.
