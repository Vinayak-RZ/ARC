# Frontier scorecard (measured on branch `cursor/frontier-execution-7a2f`)

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| PSA eval CLI (smib/agc/ed) | 3/3 PASS | **3/3 PASS** | done |
| `eval --pack power` | exit 0 | **6/6 PASS** | done |
| Full `electrical-engineer eval` | all runnable PASS | **16/18** (control block-feedback, digital-pole **FAIL** pre-existing) | partial |
| pytest | green | **238 passed** | done |
| `check_psa_evals.py` | green | **16 passed** | done |
| LIVE A/B pass^8 | ≥0.75 | **blocked** (no API keys) | blocked |
| ControlEval subset | ≤50 items | not run | blocked |
| Visual Kit PSA components | 3 P0 | **3 rendered** + MCP list | partial |
| pass^k trials (T1) | ≥0.75 | not run (no held-out bundle) | blocked |

Evidence paths: `artifacts/visual-goldens/`, `artifacts/frontier-ab/live_ab_status.json`, `/opt/cursor/artifacts/visual-goldens/`.
