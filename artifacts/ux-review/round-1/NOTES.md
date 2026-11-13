# UX review round 1

## Shell and layout

- Product composer card (auto-growing textarea, subject chip popover, compact Solve button, Cmd+Enter).
- DESIGN.md button sizing (32px height, 4–6px radius); top bar actions use compact buttons.
- Page content column max-width ~1080px.
- Sidebar Recent: single-row layout (status dot, truncated title, subject chip).

## Problem detail

- Display-type answer line with muted units (no monospace answer).
- Plain-language circuit verifier line when checked.
- Underline tabs; Parameters only via top bar toggle and right drawer.
- Work tab shows input/equation/trace steps; diagram inspector only on Diagram tab.
- Parameters drawer with Vin/R1/R2 unit fields and stale banner.

## Titles and assets

- Human run titles from problem prompt, recipe map, and measured values (server + list API).
- Schematic divider golden uses matplotlib fallback figure when schemdraw is absent (no placeholder text).

## Capture

- `scripts/capture_ux_review_round.py` clears runs for empty home, asserts distinct MD5 per PNG, writes `md5.txt`.
