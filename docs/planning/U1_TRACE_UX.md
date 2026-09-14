# U1 — Trace / observation UX (kernel harden)

Design IA only — no brand rewrite. Tokens: DESIGN-coinbase / existing `ui` tokens.

## Placement

- Keep single-page `?run=<id>` shell.
- Surface in existing **run.more** / disclosure region (today: Observation `<pre>`).
- Do not invent a second app chrome or hero cards.

## Human-readable observation excerpt

Show above or instead of full dump (dump remains behind nested `<details>`):

- `unchecked` boolean + exact token when set
- `unchecked_reason` when present
- `capabilities[]` and `providers[]` as compact lists
- `retrieve.empty` hint when true

## trace.jsonl panel

- API: run detail includes `trace_excerpt` (last N lines or summarized spans: name, duration_ms, node_id, ok/unchecked).
- UI: timeline-ish list (simple stacked rows; no chart lib).
- Truncate large files; never block paint on full corpus.

## unchecked_reason

- Must be visible without opening raw JSON.
- Copy stays plain: reason code as monospace; no euphemism for `unchecked`.

## A11y

- Use `<details>`/`<summary>` with visible focus.
- Do not rely on color alone for ok vs unchecked.

## Non-goals

- New router, dashboard home, marketing polish pass beyond run inspector density.
- Binding UI off localhost.
