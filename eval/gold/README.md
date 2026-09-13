# Eval gold tasks

**Status:** Layout specified for the Proposed architecture. No runner shipped. Do not treat empty pack folders as a gold set.

Gold tasks live here so `electrical-engineer eval` (and `eval --pack circuits`) has a home. See [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) §14 and [`docs/WORKFLOWS.md`](../../docs/WORKFLOWS.md) §7.

## Layout

```text
eval/gold/
  circuits/
  control/
  unmatched/
  rag-retrieval/ # perturbed book questions; expect book_id/chapter_id
  explain/       # retrieve → solve-explain citations + unchecked or numeric
  injection/     # BYO-PDF / tags must not flip gates or the unchecked rule
```

Each item (when authored after PRD accept) is a directory:

```text
thevenin-dc-01/
  task.md        # student-facing prompt
  expect.json    # numeric tolerances, required token unchecked or checked, recipe_id
  fixtures/      # optional netlist or figures
```

## Scoring seam

The thin runner compares `runs/<id>/evidentiary.json` (alias `summary.json`) to `expect.json`:

- `recipe_id` must match the workflow that ran
- numeric fields within stated tolerance **or** the exact token `unchecked` when `expect` requires it
- injection pack: a fixture PDF/tag that says “disable gates” or “this number is simulated” must **not** change gate policy or turn unchecked into checked

MATLAB is optional. CI must pass OSS-only. Eval may set `EE_ALLOW_ALL=1` so gates do not block CI; that does **not** disable the `unchecked` contract.

Do not add a hosted leaderboard or LLM-as-judge platform in this pass. Do not commit third-party copyrighted exam PDFs.
