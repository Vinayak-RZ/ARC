# Frontier scorecard (measured on `cursor/frontier-execution-7a2f`)

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| PSA eval CLI | 3/3 | **3/3 PASS** | done |
| `eval --pack power` | exit 0 | **6/6 PASS** | done |
| Full `electrical-engineer eval` | all runnable PASS | **18/18 PASS** | done |
| pytest | green | **251 passed** | done |
| Visual regression | image diff | **10/10 PNG** (`tests/visual`) | done |
| `check_psa_evals.py` | green | **16 passed** | done |
| Scripted pass^k (traps) | ≥0.75 | **1.0** (`scripts/pass_k_traps.py`) | done |
| LIVE A/B pass^8 | ≥0.75 | **blocked** (no API keys) | blocked |
| Visual Kit components | P0+P1 slice | **11** registry ids | partial |
| Benchmark v0.1 | tarball | **built** (`scripts/build_benchmark_v01.py`) | partial |

Evidence: `artifacts/visual-goldens/`, `artifacts/frontier/pass_k_traps.json`, `docs/planning/frontier-2026-11/LIVE_AB.md`.
