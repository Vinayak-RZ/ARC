# Node plan: M1: integrate barrier

| Field | Value |
|-------|-------|
| **Node id** | `M1` |
| **Job** | Merge parallel kernel slices; resolve conflicts; single pytest green |
| **Wave** | 5 |
| **Depends on (data)** | All B* outputs |
| **Write paths** | lead-only integration |
| **Model** | inherit |

## Objective

One runnable tree after fan-out (TOPOLOGIES diamond merge).

## Contract

**Output:** `{ "integrated_manifest": { "pytest_passed": true } }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 32-33 | merge + CI job | full pytest |
