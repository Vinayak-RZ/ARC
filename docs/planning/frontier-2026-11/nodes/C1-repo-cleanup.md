# Node plan: C1: repo cleanup

| Field | Value |
|-------|-------|
| **Node id** | `C1` |
| **Job** | Prune dead paths, fix doc drift, archive stale planning, tidy layout without breaking CI or users |
| **Wave** | 2 (immediately after B1; may overlap late B1 if eval paths untouched) |
| **Depends on (data)** | B1 `eval_schema_v2` recommended so gold README matches scorer |
| **Write paths** | `README.md`, `docs/**`, `hosts/**`, `eval/gold/README.md`, `docs/media/trials/` (trim only), `docs/planning/**` archives; **no** `src/**` engine logic except dead imports |
| **Model** | inherit |

## Objective

Reduce maintenance drag called out in audit #04 before kernel fan-out: duplicate host narrative, recipe count drift (27 vs 31), stale `eval/gold/README.md`, oversized `docs/media/trials/` galleries, confusing `origin/cursor/*` branch story. **Do not** delete git history on remote branches; **archive** stale planning markdown under `docs/planning/archive/` with pointer from PROGRESS.

## Safety rule (non-negotiable)

Before **every** commit in this node and before exit:

```text
uv run ruff check .
uv run pytest -q
uv run python scripts/check_psa_evals.py
```

All three must pass. No user-facing behavior change to CLI, MCP verbs, or default workflows. If a cleanup item risks behavior, defer to DECISIONS and skip.

## Scope from audit #04

| Item | Action |
|------|--------|
| Recipe / agent index drift | Sync README, `hosts/agents/INDEX.md`, `eval/gold/README.md` to `catalog.py` (31) |
| Remote-only `cursor/*` branches | Document in `docs/planning/archive/BRANCH_INDEX.md`; no force-delete remotes in automation |
| Stale planning on unmerged branches | Archive superseded planning copies; keep `frontier-2026-11` and `eec301-lift` canonical |
| `docs/media/trials/` | Keep README-linked subset; move excess to `docs/media/trials/archive/` or delete untracked-only assets |
| Dead code | Remove unused modules only when grep + pytest prove zero imports |
| Folder layout | Normalize `visual-kit` target path with A1 ADR; no drive-by renames in `engines/` |

## Non-goals

- Deleting merged git history
- Removing PSA engines or trap knowledge
- Changing eval gold expectations
- PyPI or packaging restructure

## Contract

**Input:** `{ "doc_truth_manifest": from D0 optional }`

**Output:** `{ "cleanup_report_path": "docs/planning/frontier-2026-11/CLEANUP_REPORT.md", "ci_green": true }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 1 | `chore(repo): sync recipe and gold readme counts` | pytest + PSA |
| 2 | `chore(repo): trim trials media and archive stale planning` | pytest |
| 3 | `chore(repo): remove dead imports and duplicate host copy` | ruff + pytest |

Coalesce into 2 rows if commit budget tight.

## Kill criteria

If pytest or PSA regresses and cannot fix in-node, **revert** the offending commit; do not proceed to wave 3 until green.
