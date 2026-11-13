# Node plan: D0: docs-in sync

| Field | Value |
|-------|-------|
| **Node id** | `D0` |
| **Job** | Align README, gold README, agent INDEX, and catalog counts with tree truth |
| **Wave** | 1 |
| **Depends on (data)** | Gate 0 answers (optional for drift only) |
| **Write paths** | `README.md`, `hosts/agents/INDEX.md`, `eval/gold/README.md`, `docs/**/*.md` (planning only) |
| **subagent_type** | explore → lead |
| **Model** | inherit |

## Objective

Doc drift (27 vs 31 recipes, stale gold README) no longer undermines frontier proof story (audit #04).

## Contract

**Input:** `{ "repo_root": "...", "catalog_count": 31 }`

**Output:** `{ "doc_truth_manifest": { "recipe_count": 31, "files_updated": [] } }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 2 | `docs(frontier): sync recipe counts and eval readme` | `scripts/check_doc_drift.sh` |

## Do not

Commit product code beyond doc drift fixes.
