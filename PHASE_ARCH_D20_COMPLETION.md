# PHASE_ARCH_D20_COMPLETION — Harness persist, observe, spawn

## Completed work

Specified the undergraduate EE lab harness as Proposed docs: the rented host still owns the loop, compaction, and specialist spawn; the kernel owns runs, named memory files, BYO RAG ingest, observation, and deterministic hooks. No product Python.

## Files modified

- `docs/ARCHITECTURE.md` — §0.3 ownership; §2.5 kernel hooks; §10 ingest; §11 memory write law; observation
- `docs/PID.md`, `docs/PRD.md` — FR13/FR19 tighten; FR24 observation
- `docs/rag-byo.md`, `docs/CANNOT_DO.md` — pipeline + `CD-RAG-PARSE`
- `docs/hosts/*.md`, `hosts/adapters/` — spawn adapters (claude/codex/cursor)
- `skills/SKILL.md`, `skills/_cross/SKILL.md` — memory / retrieve / spawn law
- `DECISIONS.md` ADR-0011; critique loop 5; vision-lock D20
- `AGENTS.md`, `PROGRESS.md`

## Architectural changes

Control stays H3. Spawn is host-native (at most two pack specialists). CLI/MCP/UI never fan out agents. Memory improves this student only; `lessons.md` is explicit, not silent.

## Validation performed

`rg` gates from the D20 plan (ownership, FR24, pipeline, adapters, spawn/H5 wording). No `tests/*.py` in this overlay.

## Known issues

- D20 is Proposed, not owner-Accepted; README not rewritten
- As-built RAG `add` is inventory-only (`CD-RAG-PARSE`); observation file not yet written by the runner

## Next phase objectives

Owner Accept of D19/D20. Then a code plan: ingest extract/chunk, `observation.json` writer, `memory write` CLI.

## What you learned

- A complete lab harness can be specified without becoming a second agent product
- Persist/observe belong in the kernel; spawn belongs on the rented host
- “Improves with usage” is local files plus an explicit lesson write, not fleet learning
