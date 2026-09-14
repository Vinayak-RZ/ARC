# UG EE knowledge corpus

## User

Arc maintainers (and a later retrieval layer). Not a student-facing UI this graph.

## Job

Persist a licence-clean undergraduate electrical-engineering teaching corpus so later retrieval can ground co-solving.

## Done looks like

`python scripts/check_knowledge_tree.py` exits 0 and prints pack/unit/question counts. `knowledge/README.md` explains how to browse the tree. Five T1 spot-checks are logged in `docs/planning/T1_TRIALS_KNOWLEDGE.md`.

## P0 (this graph)

- Encyclopedic unit handbooks for every curriculum-map pack (circuits including BES and network theory, signals, electronics, machines, power, control, power electronics, measurements, EM, maths-for-EE)
- Listed electives: microprocessors, protection and switchgear, high voltage, utilization, electric drives, DSP, communication (EEE), PLC/industrial, renewables intro
- Original worked questions (≥5 per unit) with method, never third-party exam PDFs
- SPDX on every `oer/` file (CC BY / CC BY-SA / CC0 only)
- Inventory test in pytest

## Later (not this graph)

- Retrieval, chunking, RAG wiring
- Gold-eval promotion of worked items
- BYO textbook ingest into this tree
- Hindi, video, extra electives

## Non-goals

- Product `src/`, `ui/`, `workflows/`, MCP, CLI verbs
- Overwriting `docs/PRODUCT.md` / PID / PRD / ARCHITECTURE
- Commercial textbooks or GATE/university exam papers in git
- NC-licensed OER (MIT OCW, Fiore, Adams) copied into git
- PG, civil, mechanical, live PLC writes

## Honest holes

- Machines, power, and power electronics have no SPDX-clean full OER at retrieve date — original notes plus links only
- Åström/Murray *Feedback Systems* and Smith DSP Guide are **link only** until SPDX is recorded
- Encyclopedic means syllabus-complete teaching handbooks, not reprints of Chapman/Hayt/Ogata
- Numeric examples are pedagogical; they are not `eval/gold/` items until a later graph
