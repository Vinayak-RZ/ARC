# UX review round 3

**PNG count: 35** (unique MD5s in `md5.txt`)

Studio ported from `cursor/control-studio-6ef3` @ `8253197` (margins, rail layout, compose, forward-rail + PID open-loop tests).

## Sidebar measurements

`sidebar-measurements.json`: expanded **240px**, collapsed **56px**, Cmd+K open **240px** (after 180ms transition wait).

## Round 3 fixes (file · action · self-score /5)

| # | Capture(s) | Action | Score |
|---|------------|--------|-------|
| 1 | `studio.png`, `studio-after-simulate.png`, `dark-studio.png` | `.studio` CSS grid, 220/280, toolbar, palette search+rows, margins in results drawer | 4 |
| 2 | `studio-after-simulate.png`, `studio-margins-no-crossover.png` | Sweep 1e-3…1e5, edge rejection, table KPI; PID ωcg≈0.051, PM≈99.8°, GM ∞ | 5 |
| 3 | `studio-block-selected.png` | PR #50 rail wires, 96×56 blocks, select PID without stray Gain in capture | 4 |
| 4 | `dark-studio.png`, `gallery.png` | Shell token bridge for Studio; example thumbs dispatch + Nyquist | 3 |
| 5 | `home-scrolled-1280.png`, `home-scrolled-1440.png` | Thumb frame, Shortcut, scrolled Continue/agent | 4 |
| 6 | `problem-parameters-stale.png` | Verification strip + stale styling (subagent) | 4 |
| 7 | `cmdk-open.png`, `cmdk-query.png` | Grouped palette, transition settle, footer fade | 4 |
| 8 | `problems-*.png`, `problems-row-hover.png` | Chips, skeleton, hover icons, sidebar Recent quiet on load/error | 4 |
| 9 | `sidebar-collapsed.png` | Recent row dots; no default Agent ready chip | 4 |
| 10 | `gallery.png`, `library.png`, `settings-*.png` (×5) | Titles/tabs captures; Library dialog partial | 3 |
| 11 | `focus-*.png` | `--text-muted` #70706C, `--text-faint` #8A8A86, subscripts on schematic | 4 |
| 12 | `problem-answer.png` | V<sub>in</sub>/R labels, fit padding | 4 |

**Round 3 self-total: 47/60**
