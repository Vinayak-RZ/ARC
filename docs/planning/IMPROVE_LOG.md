# Improve log — Kernel harden

## I1 — Honest `unchecked_reason`

- **Class:** F1 mislabel fallback
- **Change:** `_unchecked_reason` no longer defaults to `unmatched`; emits `labeled` when the run is unchecked via label/explain path. `unmatched` reserved for unmatched recipes / router miss.
- **Docs:** ARCHITECTURE observation enum includes `labeled`.
- **Tests:** `tests/unit/test_unchecked_reason.py`
- **Validate:** required after commit

## I2 — Unagent export hygiene + advisor reports

- **Class:** advisor false “failure_rate” from treating `unchecked` as tool error
- **Change:** `to_unagent_events()` — only `ok is False` sets `error`; Unagent run ABSTAINs on FlipToDet (tool-shaped kernel)
- **Artifacts:** `artifacts/kernel-harden/unagent-report.md`, `improveness-notes.md`
- **Improveness:** frozen physics / held-out / grader≠improver documented; no DeepSeek Harness mount

