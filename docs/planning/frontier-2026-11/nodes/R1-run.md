# Node plan: R1: run (boot smoke)

| Field | Value |
|-------|-------|
| **Node id** | `R1` |
| **Job** | Boot UI server and CLI smoke on critical path |
| **Wave** | 8 |
| **Depends on (data)** | E1 pass |
| **Write paths** | `tests/e2e/**` or `scripts/smoke_*.sh` |
| **Model** | inherit |

## Objective

"Laboratory runs" not only unit tests (LIFECYCLE R1).

## Contract

**Output:** `{ "ui_boot": true, "cli_eval_smoke": true }`

## Commits

Coalesced with T1 if budget 36.
