# Node plan: B2: kernel PSA wire

| Field | Value |
|-------|-------|
| **Node id** | `B2` |
| **Job** | Register smib, agc, ed activities on YAML/MCP paths |
| **Wave** | 3 |
| **Depends on (data)** | `eval_schema_v2` |
| **Write paths** | `src/electrical_engineer/nodes/sim.py`, `workflows/power/**`, `engines/smib_*`, `eval/gold/power/**` |
| **Model** | inherit |

## Objective

Power pack eval 3/3 PASS; host can invoke PSA via same graph as CLI replay.

## Contract

**Output:** `{ "psa_dag_wiring": true, "eval_power_pass": "3/3" }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 7-10 | activities, YAML, gold CLI, MCP | `check_psa_evals.py` + eval pack |
