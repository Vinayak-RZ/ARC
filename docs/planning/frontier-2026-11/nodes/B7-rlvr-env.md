# Node plan: B7: RLVR environment pack

| Field | Value |
|-------|-------|
| **Node id** | `B7` |
| **Job** | Package goldens+traps as importable RLVR-style environment (no weight training) |
| **Wave** | 4 |
| **Depends on (data)** | `eval_schema_v2` |
| **Write paths** | `src/electrical_engineer/rlvr_env/**` or `packages/arc_rlvr/**`, docs |
| **Model** | composer-2.5-fast for scaffold, inherit for merge |

## Objective

External researchers can train routers against Arc oracle (report #03 RLVR, #02 white space #10).

## Contract

**Output:** `{ "rlvr_env_manifest": { "version": "0.1", "traps": 10 } }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 30-31 | package + card | `python -c import` |
