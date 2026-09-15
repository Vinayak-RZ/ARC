# RAG hybrid + hierarchical graph — Implementation Plan

> Execution contract for branch `cursor/rag-hybrid-pipeline-78c0`.  
> Profile: **project** · Commit budget: **20** · PRIORITY: QUALITY (retrieve p95 ≤ 7s)

## Objective

Ship local BYO textbook RAG: multimodal ingest (OCR + figures) into a typed hierarchy, hybrid BM25+dense retrieve with ≤2 graph hops, eval slice, dual architecture docs.

## Ontology (T0–T4)

| Tier | Kinds |
|------|--------|
| T0 | library → book → chapter → section |
| T1 | chunk (`prose` \| `equation` \| `caption` \| `solution_step` \| `table_cell`) |
| T2 | `worked_example` \| `section_parent` \| `figure_group` |
| T3 | `figure` (path, page, caption_text, ocr_text?) |
| T4 | `entity` \| `proposition` |

Edges: `belongs_to`, `part_of_example`, `illustrates`, `caption_of`, `mentions`, `states`, `prerequisite`.

## Pipelines

- **Ingest (offline):** gate → parse/OCR → structure → units/parents/figures → light T4 → BM25+dense+graph indexes
- **Query (online):** filters → BM25∥dense → RRF → parent hydrate → hops k≤2 → 3×1500, empty visible, `engine: hybrid-graph`

## Non-goals

MS GraphRAG communities; ColPali primary; commercial PDFs in git; forcing MinerU/RAG-Anything in CI; UI redesign.

## Commit matrix

See plan §9 (rows 1–20). Lead owns git. Subagents do not commit.

## Authority

`docs/ARCHITECTURE.md` §10, `docs/architecture/rag.md`, `docs/rag-byo.md`, `docs/CANNOT_DO.md`, ADR-0004.
