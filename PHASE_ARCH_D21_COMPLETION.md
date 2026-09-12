# PHASE_ARCH_D21_COMPLETION — Student-facing lab UI

> **Historical completion log.** Student IA is now Accepted in [`docs/UI.md`](docs/UI.md). As-built `ui/` still dumps JSON.

## Completed work

Specified the localhost UI as a UG EE lab workbook (docs only). Named four pages and two overlays. Locked: no raw Markdown/JSON as the product; no in-DAG reasoning-mode node. No React or Python.

## Files modified

- `docs/UI.md` — pages, presentation law, copy dictionary, visual bar
- `docs/ARCHITECTURE.md` §9; no reasoning-mode node under `propose_composition`
- `docs/PRD.md` FR11; `docs/PID.md`; `docs/design/DESIGN-coinbase.md` pointer
- `DECISIONS.md` ADR-0012; critique loop 6; vision-lock D21
- `AGENTS.md`, `PROGRESS.md`

## Architectural changes

Layer 3 is a lab workbook, not a file browser. Kernel files stay the contract; the UI maps them. Host still reasons between kernel verbs.

## Validation performed

`rg` for UI.md, FR11, reasoning-mode, D21. No `ui/` code in the diff.

## Known issues

- D21 is Proposed, not owner-Accepted; README not rewritten
- As-built `ui/` still dumps `summary.json`

## Next phase objectives

Owner Accept. Then a UI **code** plan that implements This problem / Past work / Books / Notes.

## What you learned

- EE students need netlists and plots; they do not need our filenames
- Four pages cover D20 slots without exposing observation.json
- Rejecting a reasoning node and specifying UI are the same Layer 0/3 split: host thinks, workbook shows
