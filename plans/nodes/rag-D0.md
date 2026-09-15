# Node plan — D0 — Docs-in

| Field | Value |
|-------|-------|
| **Node id** | `D0` |
| **Job** | Confirm ARCH §10 + architecture/rag.md authority; list as-built gaps |
| **Wave** | 0 |
| **Depends on** | none |
| **Write paths** | `docs/planning/RAG_GATE0_NOTES.md` (optional) |
| **Read paths** | `docs/ARCHITECTURE.md`, `docs/architecture/rag.md`, `research/notes/rag-ingest-query-architecture.md` |
| **subagent_type** | explore |
| **Model** | inherit |

## Objective

Authority docs are accurate enough to build hybrid-graph RAG; gaps named (CD-RAG-PARSE, inventory-only drift).

## Contract

**Output:** `{ "gaps": ["…"], "authority_ok": true }`

## Commits

None alone — feeds commit 1.
