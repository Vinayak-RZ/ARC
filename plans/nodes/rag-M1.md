# Node plan — M1 / E1 / R1 / T1 / D1

## M1 Integrate

Wire `pyproject` extras (`rag`, `rag-ocr`), `EE_CORPUS_DIR`, exports. Commits 16.

## E1 Evaluate

`pytest tests/unit/test_rag_*.py` + `electrical-engineer eval --pack rag-retrieval` + latency script. Commit 17.

## R1 Boot

`rag add` fixture → `rag query` smoke.

## T1 Trials

Happy / empty / hop / figure / OCR-skip notes. Commit 18.

## D1 Docs-out

Sync ARCHITECTURE, architecture/rag.md, rag-byo, CANNOT_DO, ADR. Commits 19–20.
