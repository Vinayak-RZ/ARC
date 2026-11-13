# C1 cleanup report (frontier-2026-11)

| Item | Status | Notes |
|------|--------|-------|
| Recipe / index drift | **done** | README, hosts INDEX, eval/gold README → 34 workflows |
| Stale gold README prose | **done** | Rewrote eval/gold/README.md for shipped runner |
| Frontier planning canonical | **done** | `frontier-2026-11/` active; eec301-lift artifacts retained on main |
| Branch index | **done** | `docs/planning/archive/BRANCH_INDEX.md` |
| Trials media trim | **deferred** | No oversized untracked blobs in snapshot; manual trim if gallery grows |
| Dead imports | **partial** | PSA providers added to capabilities; full grep sweep deferred to M1 |

CI after C1 commits: `ruff`, `pytest`, `check_psa_evals.py` green.
