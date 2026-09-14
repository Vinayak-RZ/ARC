# T1 trials — Kernel harden final

| # | Trial | Result | Evidence |
|---|-------|--------|----------|
| 1 | Happy CLI `solve-circuit-problem` divider | PASS | corpus checked rows; unit observation |
| 2 | `explain-circuits` → reason `labeled` | PASS | `tests/unit/test_unchecked_reason.py` + T_RETEST |
| 3 | `unmatched-cosolver` → `unmatched` | PASS | unit + T_RETEST |
| 4 | `simulate-after-confirm` → `gate-closed` | PASS | T_RETEST |
| 5 | Host corpus ≥100 with `trace.jsonl` | PASS | CORPUS_INDEX 120/120 |
| 6 | Unagent recommend ABSTAIN (no FlipToDet) | PASS | unagent-report.md |
| 7 | Held-out ids file present (24) | PASS | HELD_OUT_IDS.txt |
| 8 | validate.sh | PASS | Wave 6/7 gate |
| 9 | Graded corpus 120/120 | PASS | `trial_driver` expect-match; Wave 8 |
| 10 | `solve-control-problem` → `no-provider` | PASS | `test_unchecked_reason.py` |
| 11 | `photo-to-netlist` → `gate-closed` | PASS | `test_unchecked_reason.py` |

Held-out scenario ids were not used as improver prompts (Improveness Self-Harness).
