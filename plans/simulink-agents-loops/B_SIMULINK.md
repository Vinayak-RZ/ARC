# Node plan — `B_SIMULINK` — `kernel`

> Collapsed feature-mode plan. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_SIMULINK` |
| **Job** | extension-file when EE_SIMULINK_TOOLS_JSON set. run-simulink-if-present fail-closed to CD-SIMULINK-PLANT. Stub must not mint checked plants. |
| **Wave** | 3 |
| **Depends on (data)** | A1 |
| **Write paths** | `src/electrical_engineer/matlab_mcp.py, src/electrical_engineer/nodes/sim.py, src/electrical_engineer/capabilities.py, tests/fixtures/fake_matlab_mcp.py, tests/unit/test_matlab_mcp.py, tests/fixtures/fake_simulink_tools.json` |
| **subagent_type** | lead |
| **Model** | inherit |

---

## Objective

extension-file when EE_SIMULINK_TOOLS_JSON set. run-simulink-if-present fail-closed to CD-SIMULINK-PLANT. Stub must not mint checked plants.

## Non-goals

- Live MATLAB/Simulink on this VM
- Product `.cursor/agents/`
- H5 Python fan-out
- Inventing capability ids

## Contract

**Output:** files_touched + gate command result. **Do NOT commit.**

## Gate

```text
uv run pytest tests/unit/test_matlab_mcp.py tests/unit/test_sim_seams.py -q
```

## Do not

- Commit, push, or open a PR
- Write outside write paths
- Expand into another graph
