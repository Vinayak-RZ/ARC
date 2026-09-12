# PHASE_ARCH_D19_COMPLETION — Capability-first architecture overlay

## Completed work

Refined Proposed architecture so the kernel is a UG EE co-solver, not an ngspice/YAML/FastAPI product. Added coverage law, capability registry, pack method skills, ADR-0010, D19 lock-sheet row.

## Files modified

- `docs/ARCHITECTURE.md` — §0 domain contract; providers vs identity
- `docs/ARCHITECTURE_CRITIQUE.md` — loop 4
- `docs/PID.md`, `docs/PRD.md`, `docs/WORKFLOWS.md`, `docs/CANNOT_DO.md`, `docs/curriculum-map.md`, `docs/EXTENSIVE.md`
- `skills/**/SKILL.md` — method + capability ids for every curriculum pack
- `DECISIONS.md` ADR-0010; `research/synthesis/vision-lock-sheet.md` D19; `research/DECISION_REGISTER.md`
- `AGENTS.md`, `PROGRESS.md`
- `tests/unit/test_capability_docs.py`

## Architectural changes

Capabilities are the stable physics contract. This-pass providers (ngspice, python-control, pandapower, sympy, MATLAB-if-present) and encodings (YAML, Python CLI, FastAPI+React, LightRAG facade) stay as freezes. Every in-bound pack × genre has a complete path: check or `unchecked`.

## Validation performed

`uv run pytest tests/unit/test_capability_docs.py tests/integration/test_review_explain.py -q` plus `./scripts/validate.sh` (planned in this phase).

## Known issues

- Runner still keys on provider ids (`run-spice`, …); capability→provider bind is a later code plan
- D19 is Proposed, not owner-Accepted; README not rewritten
- As-built MCP remains `list_workflows` + `run_workflow`

## Next phase objectives

Owner Accept of D19. Then a code plan: validator accepts capability ids; gold depth per pack remains circuits-first.

## What you learned

- “Solve any UG question” is a **path guarantee** (method + check or `unchecked`), not a claim that every numeral is simulated
- Naming providers as the architecture made signals/EM look like missing SPICE recipes
- Pack skills can be domain-specific without locking a simulator if they request capability ids
