# Integration — Unagent × Arc

## Role

[Unagent](https://github.com/Vinayak-RZ/unagent) (`superdeterminism`) is a **design-time** determinism advisor. Arc remains the domain kernel; Unagent never owns the student loop.

## Export

```bash
uv run python -c "from pathlib import Path; from electrical_engineer.export import write_export, load_jsonl, to_unagent_events; \
print(write_export(Path('runs/<id>')))"
```

- `write_export` → span document (`adapter: custom`)
- `to_unagent_events` → `{events:[...]}` for `--adapter custom` (honest `unchecked` ≠ `error`)

## Recommend (offline)

```bash
uv pip install -e ../unagent   # sibling clone
uv run python -m superdeterminism recommend artifacts/kernel-harden/unagent_events_v2.json \
  --adapter custom --stdout md --n-min 1 --md artifacts/kernel-harden/unagent-report.md
```

## This graph’s result

ABSTAIN on FlipToDet for tool nodes — expected for Arc. Report: `artifacts/kernel-harden/unagent-report.md`.
