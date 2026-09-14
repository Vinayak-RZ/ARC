# Integration — Unagent × Arc

## Role

[Unagent](https://github.com/Vinayak-RZ/unagent) (`superdeterminism`) is a **design-time** determinism advisor. Arc remains the domain kernel; Unagent never owns the student loop.

## Export

```bash
uv run python scripts/kernel_harden/export_unagent.py
# writes artifacts/kernel-harden/unagent_events.json
```

- `write_export` → span document (`adapter: custom`) for one run dir
- `to_unagent_events` → `{events:[...]}` for `--adapter custom`
- Honest `unchecked` is **not** `error`. A node that never reports `ok` is not a crash (`ok: null`).

## Recommend (offline)

```bash
uv pip install -e ../unagent   # sibling clone
uv run python -m superdeterminism recommend artifacts/kernel-harden/unagent_events.json \
  --adapter custom --stdout md --n-min 1 --md artifacts/kernel-harden/unagent-report.md
```

## This graph’s result

ABSTAIN on FlipToDet for tool nodes — expected for Arc. Report: `artifacts/kernel-harden/unagent-report.md`.
The first export overstated `failure_rate` because missing `ok` was coerced to `False` (I3).
