# Node plan: B5: verifier + trap PRM

| Field | Value |
|-------|-------|
| **Node id** | `B5` |
| **Job** | Host hook contract + automate T4/T5 + split process vs outcome graders |
| **Wave** | 3 |
| **Depends on (data)** | PSA wiring recommended |
| **Write paths** | `knowledge/traps/**`, `hosts/**`, `tests/integration/test_trap_*`, `docs/hosts/**` |
| **Model** | inherit |

## Objective

Traps act as deterministic PRM (report #03); extend ablation beyond T1/T2/T6.

## Contract

**Output:** `{ "traps_automated": ["T1","T2","T4","T5","T6"], "hook_contract_path": "docs/hosts/trap_hooks.md" }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 20-22 | hook doc, T4/T5 tests, grader split | trap ablation green |
