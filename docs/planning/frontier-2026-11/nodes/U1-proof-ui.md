# Node plan: U1: proof surfaces UX

| Field | Value |
|-------|-------|
| **Node id** | `U1` |
| **Job** | Proof dashboard: eval scorecard, A/B replay, **Visual Kit gallery** with live registry previews |
| **Wave** | 3 |
| **Depends on (data)** | `capability_delta_spec`, `visual_manifest` from B11 |
| **Write paths** | `ui/src/**`, `src/electrical_engineer/ui_server/**` |
| **Model** | inherit |

## Objective

Demonstrate frontier **numbers and figures** together (owner 2026-11-13: visuals sell; gallery is P0).

## Contract

**Output:** `{ "ui_routes": ["/scorecard", "/ab", "/visuals"], "smoke_passed": true }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 25-26 | UI scorecard + AB viewer (may coalesce) | `curl` smoke 127.0.0.1:8765 |

## Non-goals

Full leaderboard product UI (P1).
