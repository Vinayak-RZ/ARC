# Loop plan — `B_MATLAB` — MATLAB MCP client

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_MATLAB` |
| **Job** | Stdio JSON-RPC client behind run-matlab-if-present; stub + missing fail-closed. |
| **Wave** | 2 |
| **Depends on (data)** | A1 |
| **Write paths** | `src/electrical_engineer/matlab_mcp.py`, `src/electrical_engineer/nodes/sim.py`, `tests/unit/test_matlab_mcp.py` |
| **Read paths** | `docs/planning/R0_SOLUTIONS.md`, `research/notes/matlab-mcp-mediation-landscape.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_MATLAB.state.json](B_MATLAB.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail |

---

## Stop (required)

**Command:**

```text
python -m pytest tests/unit/test_matlab_mcp.py tests/unit/test_sim_seams.py -q
```

---

## Objective

Missing MATLAB still _missing; stub can return ok evidentiary.

## Non-goals

- Simulink toolkit
- matlab.engine as P0
- New host MCP verb

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

15–16 feat+test matlab — lead commits after **passed**.

---

## Do not

- Commit, push, or open a PR
- Write outside write paths
- Checker: write product files or be the maker
- Expand into another graph
- Use Cursor `/loop` timers
