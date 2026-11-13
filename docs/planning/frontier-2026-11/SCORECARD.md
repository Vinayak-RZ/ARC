# Frontier scorecard (measured on `cursor/frontier-execution-7a2f`)

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| PSA eval CLI | 3/3 | **3/3 PASS** | done |
| `eval --pack power` | exit 0 | **6/6 PASS** | done |
| Full `electrical-engineer eval` | all runnable PASS | **18/18 PASS** | done |
| pytest | green | **255 passed** | done |
| Visual regression (light) | image diff | **11/11 PNG** | done |
| Visual regression (dark) | image diff | **3/3** (swing, agc, nyquist) | done |
| `check_psa_evals.py` | green | **16 passed** | done |
| Scripted pass^k (traps) | ≥0.75 | **1.0** | done |
| Circuit benchmark subset | runnable golds | **divider-dc-01** | partial |
| LIVE A/B pass^8 | ≥0.75 | **blocked** | blocked |
| Visual Kit components | P0+P1 | **12** ids | done |
| Benchmark v0.1 tarball | built | `scripts/build_benchmark_v01.py` | partial |

Evidence: `artifacts/visual-goldens/`, `artifacts/frontier/pass_k_traps.json`, `artifacts/frontier/boot_smoke.json`.
