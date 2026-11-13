# Frontier scorecard (measured on `cursor/frontier-execution-7a2f`)

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| PSA eval CLI | 3/3 | **3/3 PASS** | done |
| `eval --pack power` | exit 0 | **6/6 PASS** | done |
| Full `electrical-engineer eval` | all runnable PASS | **20/20 PASS** | done |
| pytest | green | **283 passed** | done |
| Visual regression + sanity | image diff + size | **28 PASS** | done |
| `check_psa_evals.py` | green | **16+ passed** | done |
| Scripted pass^k (traps T1–T11) | ≥0.75 | **1.0** | done |
| LIVE A/B held-out (first Arc run) | ≥ bare | **21/25** (lost) | documented |
| LIVE A/B engine rerun | 25/25 | **25/25** | done |
| Visual Kit components | P0+P1 | **13** ids | done |
| Benchmark questions tarball | 82 tasks | `scripts/build_benchmark_v01.py` | done |
| Benchmark oracle grader | 82/82 | `scripts/grade_benchmark_v01.py` | done |
| Benchmark naive baseline | 0/82 | `grade_benchmark_v01.py --naive` | done |
| Bare agent (live) | pending | owner | pending |
| RLVR env import + rollout | 10/10 traps | `scripts/rlvr_dummy_rollout.py` | done |

Evidence: `artifacts/visual-goldens/`, `artifacts/frontier/pass_k_traps.json`, `artifacts/frontier-ab/live-run-2026-11-13/`.
