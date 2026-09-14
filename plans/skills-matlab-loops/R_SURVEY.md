# Loop plan — `R_SURVEY` — solution landscape

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `R_SURVEY` |
| **Job** | Survey spawn and MATLAB mediation solution families; write landscape notes and R0_SOLUTIONS synthesis. |
| **Wave** | 0 |
| **Depends on (data)** | none |
| **Write paths** | `research/notes/pack-specialist-spawn-landscape.md`, `research/notes/matlab-mcp-mediation-landscape.md`, `docs/planning/R0_SOLUTIONS.md` |
| **Read paths** | `research/notes/matlab-simulink-surface.md`, `research/notes/host-first-class-attach.md`, `docs/PID.md`, `docs/PRD.md` |
| **Maker type** | lead |
| **Maker model** | inherit |
| **Checker type** | explore |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [R_SURVEY.state.json](R_SURVEY.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | agentic-system-design |

---

## Stop (required)

**Command:**

```text
test -f research/notes/pack-specialist-spawn-landscape.md && test -f research/notes/matlab-mcp-mediation-landscape.md && grep -q '## Recommendation' docs/planning/R0_SOLUTIONS.md && grep -q '## ADR impact' docs/planning/R0_SOLUTIONS.md && grep -q 'http' research/notes/pack-specialist-spawn-landscape.md && grep -q 'http' research/notes/matlab-mcp-mediation-landscape.md
```

---

## Objective

A1 can cite R0_SOLUTIONS.md. No product code.

## Non-goals

- Product src/, skills rewrites, ADRs
- Implementing retrieval
- Storing MathWorks passwords

---

## Contract

**Input:** `docs/planning/GATE_0_SKILLS_MATLAB.md` plus upstream artifacts.

**Maker output:** files_touched + notes. **Do NOT commit.**

**Checker output:** `{ pass, command, exit_code, findings }`. Readonly.

---

## Escalate

After 3 failed rounds, status `escalated`; wait for the human.

---

## Commits (this node only)

2–4: research notes + R0_SOLUTIONS — lead commits after **passed**.

---

## Do not

- Commit, push, or open a PR
- Write outside write paths
- Checker: write product files or be the maker
- Expand into another graph
- Use Cursor `/loop` timers
