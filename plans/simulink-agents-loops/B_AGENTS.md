# Node plan — `B_AGENTS` — `catalog`

> Collapsed feature-mode plan. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_AGENTS` |
| **Job** | 12 committed cards + INDEX. Install copies homework dirs. Tests in temp dir. No product .cursor/agents. |
| **Wave** | 3 |
| **Depends on (data)** | A1 |
| **Write paths** | `hosts/agents/**, src/electrical_engineer/hosts_install.py, hosts/adapters/specialist-body.md, tests/unit/test_host_adapters.py` |
| **subagent_type** | lead |
| **Model** | inherit |

---

## Objective

12 committed cards + INDEX. Install copies homework dirs. Tests in temp dir. No product .cursor/agents.

## Non-goals

- Live MATLAB/Simulink on this VM
- Product `.cursor/agents/`
- H5 Python fan-out
- Inventing capability ids

## Contract

**Output:** files_touched + gate command result. **Do NOT commit.**

## Gate

```text
uv run pytest tests/unit/test_host_adapters.py -q
```

## Do not

- Commit, push, or open a PR
- Write outside write paths
- Expand into another graph
