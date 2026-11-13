# Node plan: U1: proof surfaces UX

| Field | Value |
|-------|-------|
| **Node id** | `U1` |
| **Job** | Localhost panels for eval scorecard and A/B transcript replay |
| **Wave** | 3 |
| **Depends on (data)** | `capability_delta_spec`, Gate 0 T4 (UI depth) |
| **Write paths** | `ui/src/**`, `src/electrical_engineer/ui_server/**` |
| **Model** | inherit |

## Objective

Demonstrate frontier metrics without requiring engineers to read JSON only (default minimal per Gate 0 T4).

## Contract

**Output:** `{ "ui_routes": ["/scorecard", "/ab"], "smoke_passed": true }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 25-26 | UI scorecard + AB viewer (may coalesce) | `curl` smoke 127.0.0.1:8765 |

## Non-goals

Full leaderboard product UI (P1).
