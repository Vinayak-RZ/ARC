# Eval gold tasks

Gold tasks for `electrical-engineer eval` and `eval --pack <pack>`. See [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) and [`docs/WORKFLOWS.md`](../../docs/WORKFLOWS.md).

The catalog ships **42** named workflow recipes (`list_workflow_ids()` in `src/electrical_engineer/catalog.py`). Eval packs score a subset with checked-in `expect.json` files: **60** tasks total (`electrical-engineer eval` with no `--pack`), including **31** in `circuits`.

## Layout

```text
eval/gold/
  circuits/       # 31
  context-web/    # 5
  control/        # 5
  explain/        # 1
  injection/      # 1
  machines/       # 2
  power/          # 9 — recipe golds + EEC-301 PSA engine golds (schema v2)
  rag-retrieval/  # 4
  signals/        # 1
  unmatched/      # 1
  ui-diagrams/    # visual/JSON goldens for pytest; 0 CLI eval items
```

Each item is a directory:

```text
divider-dc-01/
  task.md
  expect.json     # recipe_id and/or engine (v2 PSA)
  fixtures/       # optional problem.json, case.json, figures
```

## Scoring (schema v2)

| Mode | Discriminator | Scorer |
|------|---------------|--------|
| Recipe | `recipe_id` | `eval_runner/score.py` vs `evidentiary.json` |
| Retrieval | `mode: retrieval` | recall@k + faithfulness |
| PSA engine | `engine` + `schema: arc.eval.expect.v2` | `eval_runner/psa_score.py` |

- Numeric fields use stated tolerances, or token `unchecked` when required.
- Injection pack: adversarial fixtures must not flip gate policy.

MATLAB is optional. CI uses OSS-only paths. `EE_ALLOW_ALL=1` may unblock gates in CI; it does not disable the unchecked contract.

No hosted leaderboard or LLM-as-judge in this pass. No third-party copyrighted exam PDFs in git.
