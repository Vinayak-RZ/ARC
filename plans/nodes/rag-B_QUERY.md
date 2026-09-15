# Node plan — B_QUERY

| Field | Value |
|-------|-------|
| **Node id** | `B_QUERY` |
| **Job** | Hybrid RRF + parent hydrate + typed hops k≤2 + CLI query |
| **Wave** | 1 |
| **Depends on** | A1 |
| **Write paths** | `src/electrical_engineer/rag/retrieve.py`, `src/electrical_engineer/rag/hybrid.py`, `src/electrical_engineer/cli.py` |
| **subagent_type** | generalPurpose |
| **Model** | inherit |

## Objective

Filter → BM25∥dense → RRF → hydrate → hops → 3×1500; `engine: hybrid-graph`; empty visible; p95≤7s guard.

## Commits

§9 rows 8–11.
