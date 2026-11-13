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

Produce via:

```bash
uv run python -c "from electrical_engineer.rlvr_env import contract_json; print(contract_json())"
uv run python scripts/rlvr_dummy_rollout.py
```

Package: `src/electrical_engineer/rlvr_env/` (`ArcRlvrEnv`, `rewards.py`, `ENVIRONMENT_CARD.md`, `seeds.json`).

## Commits

| # | Commit | Gate |
|---|--------|------|
| 30-31 | package + card | `python -c import` + `scripts/rlvr_dummy_rollout.py` |
