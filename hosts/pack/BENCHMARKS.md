# Arc EE vertical pack — benchmark pointers

Published eval and lab goldens ship with the Arc checkout. After `hosts install`, cite these paths from the homework repo if you symlink or keep Arc as a sibling directory.

| Benchmark | Path | Command |
|-----------|------|---------|
| PSA lab goldens | `artifacts/eec301-lab-goldens/` | `uv run python scripts/check_psa_evals.py` |
| Control eval | `eval/gold/` | `uv run electrical-engineer eval --pack control` |
| Power eval | `eval/gold/` | `uv run electrical-engineer eval --pack power` |
| Trap pass^k | `knowledge/traps/` | `uv run python scripts/pass_k_traps.py` |
| Reference tables | `docs/reference/COVERAGE.md` | `uv run electrical-engineer reference search <query>` |

Do not copy held-out exam sets (`live-ab`, `exam-v4/v5/v6`, sealed `REFERENCE.json`) into homework trees.
