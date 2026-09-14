# Gate 0 — UG EE knowledge corpus

**Status:** Closed 2026-09-14. Do not re-ask on resume.

Skill: `.cursor/skills/graph-of-loops/QUESTIONS.md`. XOR: `graph-engineering` not loaded.
This graph does **not** reopen D19. D19 archive: [`LOOP_GRAPH_D19.md`](LOOP_GRAPH_D19.md), [`IMPLEMENTATION_PLAN_D19.md`](IMPLEMENTATION_PLAN_D19.md).

## Research (5–10 lines)

Arc’s UG bound is [`docs/curriculum-map.md`](../curriculum-map.md). Constitution V and PID: no commercial textbooks or third-party exam PDFs in git. ADR-0002 is BYO RAG; this tree is **not** the RAG index. Research notes cover licensing and taxonomy only — there is no teaching corpus. Gold eval is a handful of path fixtures. Safe OER to copy: Kuphaldt Lessons in Electric Circuits + ModEL (CC BY), Ellingson Electromagnetics Vol 1 (CC BY-SA), Don Johnson Fundamentals of EE I (CC BY). Link-only: MIT OCW (typically NC), NPTEL, Fiore/Adams (NC), Åström/Murray FBS and DSP Guide until SPDX is recorded.

## Locked from PID/PRD (cited, not re-asked)

- Primary *product* user remains UG EE students — [`docs/PID.md`](../PID.md) §3
- No commercial books / exam PDFs in git — PID §8, constitution V
- GATE is eval overlay, not the syllabus — [`docs/curriculum-map.md`](../curriculum-map.md)
- Surfaces / harness / `unchecked` — not this graph

## Owner answers (2026-09-14)

1. **Who uses this artifact:** Arc maintainers and a later retrieval layer. Not a student UI this graph.
2. **Job:** Persist a licence-clean UG EE teaching corpus (concepts, methods, original worked questions) so later retrieval can ground co-solving.
3. **Done looks like:** nested markdown under `knowledge/`; `python scripts/check_knowledge_tree.py` exits 0; five T1 spot-checks logged.
4. **Out of scope:** RAG ingest, MCP, CLI verbs, product `src/`/`ui/`/`workflows/`, overwriting `docs/PRODUCT.md`.
5. **P0 vs later:** encyclopedic handbooks for all curriculum-map packs **and** listed electives this graph. Retrieval, Hindi, video, gold promotion = later.
6. **How we know:** checker floors (headings, ≥1500 words `notes.md`, ≥5 worked Qs); inventory boot log; T1 log.
7. **Extend this repo.** Off-limits: `src/`, `ui/`, `workflows/`, `eval/gold/`, PID/PRD/ARCHITECTURE/`docs/PRODUCT.md`.
8. **Stack:** markdown + stdlib Python checker. No new dependency.
9. **Truth:** git files under `knowledge/`. Must not lose SPDX on `oer/` or original worked solutions.
10. **Auth / tenancy:** none. Secrets: none.
11. **UI:** none this graph.
12. **Run target:** local git tree only.
13. **Commit budget:** no cap; coalesce ~17 conventional commits.

## Trade-offs (answered)

### Knowledge source
**Option A:** original notes + links only.
**Option B:** original notes + verified CC BY / CC BY-SA / public-domain copies with SPDX.
**Option C:** links-only syllabus map.
**Choice:** B.
**PRIORITY:** QUALITY (licence-clean encyclopedic corpus).

### Done bar
**Choice:** encyclopedic textbook-length for every curriculum-map pack **including common electives**. Checkable as unit handbooks (not reprints of commercial texts): 1500-word `notes.md`, ≥5 original worked problems per unit.

## Optional defaults (accepted)

- Hosting: local this graph
- Language: English
- Location: `knowledge/` (not `research/`, not RAG corpus)
- Åström/Murray FBS and DSP Guide: link only until SPDX recorded
- MIT OCW / NPTEL: cite URL only
- Extra packs beyond listed electives: P1, not this graph
