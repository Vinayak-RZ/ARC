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

## I3 — Self-audit of the harden graph (2026-09-14)

- **Class:** F6 labeled masking provider-absent; F7 labeled masking awaiting-confirm; F8 `bool(ok)` poisoning traces; F9 ungraded corpus
- **Change:**
  - `nodes.sim._missing` stamps `cannot_do: CD-NO-PROVIDER` so recipes that name a provider id (`run-python-control`) report `no-provider` the same way capability-bound ones do.
  - `_unchecked_reason` treats `confirmed is False` as `gate-closed`; `labeled` is only the residual after those detectors.
  - Trace `ok` is tri-state (`True` / `False` / `None`); a node that never reports `ok` is not a tool crash.
  - Corpus scenarios carry an `expect` block derived from the recipe YAML; `trial_driver` grades PASS/FAIL.
- **Tests:** `tests/unit/test_unchecked_reason.py`, `tests/unit/test_scenario_bank.py`, `tests/unit/test_unagent_export.py`, `tests/integration/test_ui_artifacts.py`
- **Validate:** `./scripts/validate.sh` after commit

