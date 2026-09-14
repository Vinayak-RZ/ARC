# Improve log — Kernel harden

## I1 — Honest `unchecked_reason`

- **Class:** F1 mislabel fallback
- **Change:** `_unchecked_reason` no longer defaults to `unmatched`; emits `labeled` when the run is unchecked via label/explain path. `unmatched` reserved for unmatched recipes / router miss.
- **Docs:** ARCHITECTURE observation enum includes `labeled`.
- **Tests:** `tests/unit/test_unchecked_reason.py`
- **Validate:** required after commit

## I2 — (pending advisors)

- Placeholder for Unagent FlipToDet / Improveness notes.
