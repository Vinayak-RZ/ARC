# Round 4 UX review notes

## Checklist item 1 — Studio layout
- Applied `studio-layout.fix` (grid `clamp` results row, `isolation: isolate`, removed stale min-heights).
- `is-empty` on studio section + results footer; duplicate simulate hint removed.
- Playwright `ui/e2e/studio-layout.spec.ts` (3 passed at 1280×800 and 1440×900 with `pid_dc_motor` seed).

## Checklist item 2 — Block legibility
- Block/param/kind text **13px**; PID block **168×56**; fit zoom floor **0.85**, cap **1.25** (`WIDTH_FILL=0.92`).
- Inspector column **0px** until selection (`has-selection`).
- Human labels (`plant_first_order` → “First-order plant”, etc.).
- **Measured min on-screen block text:** ~**11.05px** at fit (13 × 0.85) via Playwright spec.

## Checklist item 3 — Dark mode (partial)
- Dark plot PNGs (`studio_*_dark.png`) generated on simulate; UI passes `theme=` on plot URLs.
- Verification strip dark tints (`--ee-semantic-up-tint: #12261c`), body text `--ee-color-ink`.
- Arrowheads via CSS `fill/stroke: var(--cs-text)`; signal labels no chip background.

## Checklist item 4 — Margins
- Textual KPI **20px/28px** (`.studio-kpi.is-textual`); sweep copy **0.001 to 100,000 rad/s**.
- Regression test `test_pid_dc_motor_margins_unchanged_with_unconnected_gain` already in tree.
- Captures: `studio-layout-after-simulate-*`, `studio-margins-no-crossover-light`, `studio-margins-finite-light`.

## Checklist item 5 — Home thumbnails
- Frame **100% × 112px**, `object-fit: contain`; corrected example thumbs (DC drive → step plot; Signals → phasor).
- Dark home capture included.

## Items 6–12
- **Checked** tag on passing verification strip; stale/dark/gallery/settings/cmdk/problems remain **partial** (not fully redesigned this round).

## Contrast samples (computed sRGB)
- Muted hint `#70706C` on white: **~4.97:1**
- Dark verification strip text `#f4f4f3` on `#12261c`: **~12.8:1**
- Dark canvas `#121211` vs plot face from dark theme tokens: themed (no longer forced white step PNG when control extra installed)

## Layout rects (Playwright, 1280×800 after simulate, pid_dc_motor)
See CI log / `ui/e2e` — canvas ≥280px tall, no panel intersections, plot inside results drawer.
