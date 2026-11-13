# Node plan: E1: evaluate gates

| Field | Value |
|-------|-------|
| **Node id** | `E1` |
| **Job** | Add `scripts/validate_frontier.sh` orchestrating fast+medium+slow tiers |
| **Wave** | 7 |
| **Depends on (data)** | `integrated_manifest` |
| **Write paths** | `scripts/validate_frontier.sh`, `.github/workflows/**` |
| **Model** | inherit |

## Objective

Single command reproduces frontier proof bar for reviewers.

## Contract

**Output:** `{ "validate_exit_code": 0 }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 36 | validate script | CI green |
