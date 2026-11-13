# Node plan: A1: architecture freeze

| Field | Value |
|-------|-------|
| **Node id** | `A1` |
| **Job** | Record Gate 0 decisions as ADRs and capability delta spec |
| **Wave** | 1 |
| **Depends on (data)** | `gate0_answers.json` |
| **Write paths** | `docs/planning/frontier-2026-11/DECISIONS.md`, `docs/ARCHITECTURE.md` (appendix only if owner approves) |
| **Model** | inherit |

## Objective

Architecture boundaries for multimodal, MATLAB provider, benchmark scope, and tutoring are **written**, not assumed.

## Contract

**Output:** `{ "capability_delta_spec": { "p0_capabilities": [], "deferred": [] } }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 3 | `docs(frontier): record gate0 ADRs` | Owner ack in PR |

## Do not

Invent tenancy, HTTP MCP, or H5 loop without Gate 0 override.
