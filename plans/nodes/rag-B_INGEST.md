# Node plan — B_INGEST

| Field | Value |
|-------|-------|
| **Node id** | `B_INGEST` |
| **Job** | Parse/OCR providers, figure links, inventory writes chunks+graph |
| **Wave** | 1 |
| **Depends on** | A1 |
| **Write paths** | `src/electrical_engineer/rag/ingest.py`, `src/electrical_engineer/rag/parse.py`, `src/electrical_engineer/rag/inventory.py`, fixtures |
| **subagent_type** | generalPurpose |
| **Model** | inherit |

## Objective

`rag add` extracts text/PDF/OCR, emits T1–T3, optional multimodal adapter (import-skip).

## Commits

§9 rows 3–7.
