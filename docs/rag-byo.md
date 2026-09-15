# BYO textbooks — local ingest pipeline

Commercial PDFs stay on **your** machine. This repo never wants those files in git.
Normative contract: [`ARCHITECTURE.md`](ARCHITECTURE.md) §10. Ingest and query **graphs**: [`architecture/rag.md`](architecture/rag.md). Untrusted: ingest cannot
override gates, `--allow-all`, `unchecked`, or mint a capability id.

## Pipeline

```text
drop .electrical-engineer/corpus/<book_id>/
  → electrical-engineer rag add PATH --book-id --chapter-id --domain-tag --licence-tag
  → gate (ask; persistent index)
  → extract (PDF text and/or scan OCR; low confidence flagged)
  → chunk (library → book → chapter → chunk; page on the chunk)
  → index (facade: hybrid-graph = BM25∥dense + typed hops; ADR-0004)
  → retrieve (filters first, hybrid+hops, 3×1500 chars, empty visible)
```

Query: `electrical-engineer rag query --book-id ID --query "…"`.

Homework circuit **photos** for simulation do not use this path. Use
`photo-to-netlist` / `ingest-figure` (UI confirm).

As-built `rag add` extracts text/markdown (optional PDF/OCR extras), chunks,
writes graph links for figures/worked examples, and indexes for hybrid retrieve.
Commercial-scan layout fidelity remains [`CANNOT_DO.md`](CANNOT_DO.md)
`CD-RAG-PARSE`. Empty retrieval must be visible.

## Drop folder

```text
.electrical-engineer/corpus/<book_id>/chapter-03.pdf
```

`EE_CORPUS_DIR` in `.env.example` points at `.electrical-engineer/corpus`. The directory is gitignored.

## Tag and ingest

```text
electrical-engineer rag add .electrical-engineer/corpus/hayt-circuits/ch3.pdf \
  --book-id hayt-circuits --chapter-id 3 --domain-tag circuits --licence-tag commercial-byo
electrical-engineer rag list
```

Then retrieve with those filters (host `retrieve` verb, or `problem.json`
`filters.book_id` + `query` on a CLI explain attachment). CLI `rag add` /
`rag list` / `rag tag` stay enough this graph; Chat/Work uses a side terminal.

## Still needed (catalog `byo_status: needed`)

From [`research/notes/iitr-ee-book-catalog.md`](../research/notes/iitr-ee-book-catalog.md):

- EEC-206 Electrical Machines — Fitzgerald / Nagrath–Kothari / Chapman
- EEC-208 Power Systems-I — Grainger / Weedy / Nagrath–Kothari
- EEC-301 Power Systems-II — Grainger / Glover / Saadat
- EEC-303 Power Electronics — Mohan / Rashid / Dubey
- EEL-302 Electric Drives — Dubey / Bose

Optional (OER already seeded for circuits): Hayt, Ogata, Oppenheim, Sedra, Sawhney, Hayt & Buck — add if you have the campus PDF.

Do not download from pirate hosts. Use your IITR library / publisher access.
