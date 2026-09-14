# UG EE knowledge corpus — Master Execution Plan

> Nawab **project** profile + **graph-of-loops** §19.
> **The graph you run:** [`LOOP_GRAPH.md`](LOOP_GRAPH.md)
> **Loop plans:** [`plans/knowledge-loops/`](plans/knowledge-loops/)
> Gate 0: [`docs/planning/GATE_0_UG_EE_KNOWLEDGE.md`](docs/planning/GATE_0_UG_EE_KNOWLEDGE.md)
> D19 archive: [`docs/planning/LOOP_GRAPH_D19.md`](docs/planning/LOOP_GRAPH_D19.md), [`docs/planning/IMPLEMENTATION_PLAN_D19.md`](docs/planning/IMPLEMENTATION_PLAN_D19.md)

XOR: `graph-engineering` is not loaded. [`EXECUTION_GRAPH.md`](EXECUTION_GRAPH.md) is historical.

---

## §0 Plan metadata

| Field | Value |
|-------|-------|
| **Profile** | project |
| **Mode** | project |
| **Stack** | markdown + stdlib Python checker |
| **Base branch** | `main` |
| **Feature branch** | `cursor/ug-ee-knowledge-corpus-0daa` |
| **User commit budget** | no cap (coalesce ~17) |
| **Delivery** | repo IMPLEMENTATION_PLAN + LOOP_GRAPH + plans/knowledge-loops |
| **Supersedes** | none for product; replaces **live execution pointer** (D19 archived) |
| **Authority** | Gate 0 knowledge; curriculum-map; constitution V |
| **Lead** | git, gates, PR; subagents do not commit |

---

## §1 North star & scope boundary

### Objective

Licence-clean encyclopedic UG EE markdown corpus in `knowledge/`, proven by checker + inventory boot + trials + README.

### Deliverables

- Nested tree `knowledge/ug-ee/**` (10 packs + listed electives)
- `scripts/check_knowledge_tree.py` + pytest
- ADR-0014, Gate 0, R1/T1 logs, `knowledge/README.md`

### Non-goals

- RAG ingest, MCP, CLI, UI, product `src/`
- Commercial textbooks, GATE/university exam PDFs, NC-licensed OER in git
- PG, civil/mechanical, live PLC, inventing capability ids

### Priority

| Priority | Items |
|----------|-------|
| **P0** | Full encyclopedic tree; SPDX on `oer/`; original worked sets; inventory test |
| **P1** | Retrieval, chunking, gold promotion, Hindi, video |

---

## §2 Prerequisites & blockers

| Item | Status | Blocks | Resolution |
|------|--------|--------|------------|
| D19 graph complete | done | overwrite risk | archive first commit |
| Licence matrix | done | illegal copies | reuse ee-corpus-and-licensing |
| OER fetch | optional | `oer/` files | original notes still required |

---

## §3 Authority & artifact map

| Document | Path | Role |
|----------|------|------|
| Gate 0 | `docs/planning/GATE_0_UG_EE_KNOWLEDGE.md` | owner answers |
| Corpus product lock | `knowledge/PRODUCT.md` | P0 for this graph |
| Coverage | `knowledge/COVERAGE.yaml` | checker truth |
| ADR | `DECISIONS.md` ADR-0014 | layout/trust |
| This plan | `IMPLEMENTATION_PLAN.md` | nawab §0–§18 |
| Loop graph | `LOOP_GRAPH.md` | execute |

---

## §4 Architecture & system map

See mermaid in `LOOP_GRAPH.md`. Truth is git markdown. Checker is stdlib Python. Not wired to RAG.

### Target layout

```text
knowledge/ug-ee/{pack}/{unit}/{notes,questions,sources}.md
knowledge/ug-ee/{pack}/{unit}/oer/   # SPDX only
scripts/check_knowledge_tree.py
```

### Trust boundaries

No auth. Git may hold original pedagogical text and SPDX-clean OER only. `oer/` without SPDX fails the checker.

---

## §5 Workstreams

| ID | Name | Owns paths | Depends on | Lead / subagent |
|----|------|------------|------------|-----------------|
| WS-SCAFFOLD | schema + checker | `knowledge/SCHEMA.md`, `COVERAGE.yaml`, `scripts/check_knowledge_tree.py` | P0 D0 A1 | lead |
| WS-PACKS | encyclopedic units | `knowledge/ug-ee/<pack>/**` | scaffold | makers, cap 4 |
| WS-TAIL | index, tests, boot, docs | glossary, tests, planning logs, README | all packs | lead |

---

## §6 Agent orchestration & subagent spawn map

Makers: `generalPurpose`, inherit, disjoint pack write paths, **Do NOT commit**.
Checkers: different Task, readonly, `composer-2.5-fast` else `inherit`.
Parallel limit: 4 writers.

---

## §7 Phase map & dependencies

Wave 0 serial P0→D0→A1→B_SCAFFOLD. Waves 1–3 pack fan-out. Wave 4 M1 barrier. Wave 5 E1→R1→T1→D1.

---

## §8 Todo registry

See Cursor todos: archive-d19-gate0, p0-d0-a1-scaffold, wave1–3 packs, m1-e1-r1-t1-d1.

---

## §9 Commit matrix

User budget: **no cap**, coalesce **17**. One row = one commit. See `LOOP_GRAPH.md` commit mapping.

---

## §10 Test & CI strategy

| Tier | Purpose | Command |
|------|---------|---------|
| Fast | tree contract | `python scripts/check_knowledge_tree.py` |
| Fast | pytest | `pytest tests/unit/test_knowledge_tree.py` |
| Validate | include pytest in `scripts/validate.sh` | `./scripts/validate.sh` |

---

## §11 Research log & decisions

| Topic | Choice | Record in |
|-------|--------|-----------|
| Source model | original + CC BY/SA copies | Gate 0, ADR-0014 |
| Depth | encyclopedic including electives | Gate 0 |
| Location | `knowledge/` | ADR-0014 |
| FBS / DSP Guide | link only | Gate 0 |

---

## §12 Documentation & artifact sync

Gate 0, PRODUCT, ADR, PROGRESS, R1/T1 knowledge logs, `knowledge/README.md`.

---

## §13 Quality gates & checkpoints

Checker exit 0. T1 ≥5 rows. No human freeze except licence escalate.

---

## §14 Validation & hardening

`scripts/check_knowledge_tree.py` then pytest. Ponytail: no product-code drive-bys.

---

## §15 Rollout & cutover

N/A — documentation tree, no deploy.

---

## §16 Exit criteria

- Checker exit 0 on full tree
- T1 log ≥5 pass rows
- `knowledge/README.md` names inventory command
- Product `src/` diff empty
- Thin root README pointer

---

## §17 Risks & contingencies

| Risk | Mitigation |
|------|------------|
| Volume vs quality | checker floors; escalate pack |
| Copyright slip | original reconstructions; SPDX on oer |
| OER fetch fail | original notes still ship |
| Overwrite D19 | archive first commit |

---

## §18 Execution protocol

If **§19 is filled**, do not run this linear protocol as the primary loop.
On approval: the graph is the plan you read. Execute [`.cursor/skills/graph-of-loops/EXECUTE.md`](.cursor/skills/graph-of-loops/EXECUTE.md). Keep §9 commits, gates, and lead-owned git.

---

## §19 Execution graph

Filled as **graph-of-loops**: [`LOOP_GRAPH.md`](LOOP_GRAPH.md). Loop plans in [`plans/knowledge-loops/`](plans/knowledge-loops/). Approving started execution immediately.

---

## Open questions

None blocking. Gate 0 closed.

---

## Approval

**Mode:** project.
Approving this plan started graph execution. Lead follows graph-of-loops EXECUTE, not linear §18.
