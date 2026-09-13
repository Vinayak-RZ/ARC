# D0 gaps — docs accepted

D19/D20 PID, PRD, and ARCHITECTURE are **docs accepted** for this graph (2026-09-13 Gate 0). Code waves close the gaps below. Do not rewrite README here (D1).

## As-built vs target

| Gap | As-built | Target loop |
|-----|----------|-------------|
| MCP verbs | `list_workflows`, `run_workflow` only | B_ACI |
| Capability bind | graphs name provider keys | B_KERNEL |
| FR9 mint | `_solve_value` can set checked ohms | B_KERNEL, B_EVAL |
| Two-band | `summary.json` only | B_KERNEL, B_UI |
| Observation | missing `observation.json` | B_KERNEL |
| CLI omitted-id | exits usage | B_ACI |
| RAG ingest | inventory-only (`CD-RAG-PARSE`) | B_RAG |
| Host-path `solve-explain` | mega YAML still catalogued | B_WF |
| Pack coverage test | recipes exist; no capability-path test | B_PACKS |
| UX two-band / empty / error | slots lack evidentiary/argument | U1, B_UI |

## speckit-analyze

`.specify/memory/constitution.md` and `specs/001-h3-cosolver/spec.md` exist (H1). No D19 `plan.md`/`tasks.md` under `.specify/` — this graph-of-loops **is** the task graph (`LOOP_GRAPH.md`). Constitution still matches: H3, `unchecked`, localhost, UG bound, Apache-2.0. Spec still scores `summary.json`; D1/B_EVAL must also mention `evidentiary.json` without forking a new spec-kit feature id. speckit-converge at E1 may append leftover **P0** tasks only; Later items stay Later.

## Honest holes already named

`docs/CANNOT_DO.md`: CD-NO-PROVIDER, CD-YAML-GAP, CD-RAG-PARSE, CD-HTTP-MCP, CD-BYOK, C5 sim later.
