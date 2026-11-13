# UX review round 2

## Form border tokens (critique item 8)

| Token | Light | vs `#FFFFFF` | vs canvas `#FAFAF9` |
|-------|-------|--------------|---------------------|
| `--ee-border-input` | `#8C8C87` | **3.38:1** | **3.23:1** |
| `--ee-border-input-hover` | `#7A7A75` | **4.31:1** | **4.13:1** |

Dark theme:

| Token | Dark | vs surface `#1A1A18` | vs canvas `#121211` |
|-------|------|------------------------|---------------------|
| `--ee-border-input` | `#757570` | **3.76:1** | **4.05:1** |
| `--ee-border-input-hover` | `#8A8A85` | **5.03:1** | **5.40:1** |

Dark hover is lighter than base (fixes the inverted `#6A6A65` regression). Focus: `outline: 2px solid #2F6FEB; outline-offset: 2px`. Dark primary label ink: `--ee-color-on-primary: #0B1222`.

## Sidebar measurement (`sidebar-measurements.json`)

Expanded: **240px** sidebar, grid `240px 1040px`. Collapsed: **56px** sidebar, grid `56px 1224px` at 1280×800.

## Critique items (file · action · self-score /5)

| # | Capture / artifact | Action | Score |
|---|-------------------|--------|-------|
| 1 | `problem-parameters-drawer.png`, `problem-parameters-stale.png` | kΩ-aligned parameter fields, stale Run again | 4 |
| 2 | `problem-work-tab.png` | StepTimeline rows, collapsed diagnostics in Activity | 4 |
| 3 | `studio.png`, `studio-block-selected.png`, `studio-after-simulate.png`, `dark-studio.png` | 44px toolbar, 220/280 grid, no SSE banner; selection + Simulate | 3 |
| 4 | `problem-answer.png` | Full-width diagram container, IEEE-style divider SVG | 3 |
| 5 | `sidebar-measurements.json`, `sidebar-collapsed.png` | `100dvh` shell, 240/56 grid, 180ms transition, unit test | 5 |
| 6 | `home-empty.png`, `home-with-recent.png` | Six unique example thumbs, 3×2 grid, Continue, no spurious Recent when empty | 4 |
| 7 | `problem-answer.png`, `problem-work-tab.png` | ProblemHeader, answer line, verification strip, top bar actions | 4 |
| 8 | `focus-composer.png` | Muted/faint tokens, border-input ratios above, focus ring | 5 |
| 9 | `cmdk-open.png`, `cmdk-query.png` | Grouped Cmd+K, shortcuts, footer | 4 |
| 10 | `problems-list.png`, `problems-loading.png`, `problems-empty.png`, `problems-error.png` | Table columns, filters with counts, hover Open, load/error states | 4 |
| 11 | `gallery.png`, `library.png`, `settings.png` | Nav titles, settings tabs | 3 |
| 12 | `problem-answer.png`, `gallery.png` | Golden thumbs deduped; SVG uses token colors | 3 |

**Round 2 self-total: 46/60** (12 items × 5 max).

## Capture index

All PNGs under this folder; dedup enforced via `md5.txt`.
