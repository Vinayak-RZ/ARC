# Node plan — `R_SURVEY` — `landscape`

> Collapsed feature-mode plan. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `R_SURVEY` |
| **Job** | Write OpenMontage vs SDLC-orchestrator notes and Simulink kernel attach. No product src. |
| **Wave** | 0 |
| **Depends on (data)** | none |
| **Write paths** | `research/notes/host-agent-catalog-landscape.md, research/notes/simulink-toolkit-mediation.md, docs/planning/R0_SOLUTIONS_SIMULINK.md` |
| **subagent_type** | lead |
| **Model** | inherit |

---

## Objective

Write OpenMontage vs SDLC-orchestrator notes and Simulink kernel attach. No product src.

## Non-goals

- Live MATLAB/Simulink on this VM
- Product `.cursor/agents/`
- H5 Python fan-out
- Inventing capability ids

## Contract

**Output:** files_touched + gate command result. **Do NOT commit.**

## Gate

```text
test -f research/notes/host-agent-catalog-landscape.md && test -f research/notes/simulink-toolkit-mediation.md && grep -q Recommendation docs/planning/R0_SOLUTIONS_SIMULINK.md
```

## Do not

- Commit, push, or open a PR
- Write outside write paths
- Expand into another graph
