# U_POLISH critique — product register, DESIGN-coinbase

Register: **product** (task UI, not a marketing landing). Visual authority remains [`docs/design/DESIGN-coinbase.md`](../design/DESIGN-coinbase.md). **Did not** run `impeccable teach`. Loader: `docs/PRODUCT.md` via impeccable fallback `docs/`; no `DESIGN.md` (DESIGN-coinbase is the locked equivalent).

Live: `EE_NO_BROWSER=1 electrical-engineer ui` → `GET http://127.0.0.1:8765/api/health` `{"bind":"127.0.0.1","ok":true}`; SPA `GET /` 200.

## Issues

1. MATLAB chip still read as a future promise in older copy ("coming next") after mediation shipped.
2. Empty workspace ("Select a run from the list") did not teach the CLI path when the sidebar is collapsed under 640px.
3. Engines chip had a title tooltip but no accessible name besides the visible text.

Out of scope (DESIGN-coinbase lock): new palette, display fonts, in-window chat, Coinbase wordmark.

## what we changed

- Chip copy: `MATLAB · via Arc` plus title that Arc mediates MATLAB MCP; missing stays `unchecked`.
- Empty workspace teaches `electrical-engineer run simulate-circuit`.
- `aria-label="MATLAB optional via Arc"` on the chip.
- `docs/ui-ia.md` matches the chip.

No `impeccable teach`. No second visual system.
