# Node plan: D1: docs-out

| Field | Value |
|-------|-------|
| **Node id** | `D1` |
| **Job** | README frontier section + DOMAIN_KERNEL metrics update |
| **Wave** | 9 |
| **Depends on (data)** | `proof_artifacts_bundle` |
| **Write paths** | `README.md`, `docs/DOMAIN_KERNEL_CAPABILITIES.md` |
| **Model** | inherit |

## Objective

Shipped product documented with numbers, not intentions (LIFECYCLE D1).

## Contract

**Output:** `{ "readme_updated": true, "metrics_table": true }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 39-40 | README + DOMAIN_KERNEL (may coalesce) | review |
