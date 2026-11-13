# Arc round 7 critique

Built from `53d8a46` on the draft PR #58 (`cursor/arc-ui-round7`). All 69 PNGs, `NOTES.md`, `md5.txt`, `preflight.json` and `sidebar-measurements.json` were read. I also built `53d8a46` in a scratch copy (`/tmp/r7w`, from `git archive`, nothing in their repo touched), ran their server on it and ran all the Playwright specs.

**Score: 39 / 50** (trend 25, 30, 32, 33, 32, 35, **39**). Gate G1 to G9: **7 pass, 2 fail (G5, G9).**

**Ready to show Vinayak: NO by the gate I wrote in round 6, but only just.** The score clears 38 and no criterion is below 3, but two of the nine must-pass items failed, and one of them (the Studio margin captions at 3.47:1 and 11px) is a visible defect. Every remaining blocker is small and mechanical. This is a half-round (round 8), not a full one. If Vinayak has to see something today, Studio, Problem and Home are showable; do not walk him through Library, Gallery in dark, or the Work tab in dark.

---

## 1. Gates G1 to G9

| Gate | Result | Evidence |
|---|---|---|
| **G1** Wires, arrowheads, labels at 1280 and 1440, before and after Simulate, light and dark | **PASS** | All eight captures show 5 wires with heads and `r, e, u, y` labels: `studio-layout-{before,after}-simulate-light.png`, `...-1440-light.png`, `...-1440-dark.png` (new), `studio-before-simulate-dark.png`, `studio-after-simulate-dark.png`. Also selected and unsettled states. Edge count 5 at both viewports in my probe. `edge paths keep non-empty d` ran 20 times per viewport at `retries=0`: 40/40 green, no flake |
| **G2** Dark arrowheads visible | **PASS** | `studio-after-simulate-dark.png`: heads and wires `#E8E8E6` on `#1A1A18`, **14.2:1** (sampled). Code: `markerEnd.color = "currentColor"` (`ControlStudio.jsx:494`), `.studio-canvas { color: var(--cs-wire) }`. `useWireStroke` is gone |
| **G3** Step chart: ticks, size, Auto, one header row, annotations, dark window buttons | **PASS, with a gap** | Tick numbers on both axes at 12px, axis titles "Time (s), 3 s window" and "Speed (rad/s)", plot about 740 x 150 px at 1280, tabs and window control on one 32px row, Auto picks 3 s for a 0.43 s settle and 600 s for the slow loop. Dark window buttons measure **7.4:1**. "Settled at 0.43 s · Overshoot 1.6%" is in the header. **Gap:** the 2% band and a settling marker are not drawn on the plot, so the annotation lives in text only (playbook 4.1 wants it on the plot). Not a gate failure, but the next polish item |
| **G4** "Not settled" captured, off-target pill | **PASS** | `studio-step-unsettled-light/dark.png`: pill "Not settled within 600 s", curve at 0.7 after 600 s. `studio-step-extended-light.png`: 30 s window, x axis 0 to 30, pill "Not settled within 30 s", a genuinely different picture. `studio-step-offtarget-light.png`: "Settles at 0.909, 9.1% below the setpoint". Pill is `#B45309` on `#FFF4E0`, **4.61:1** |
| **G5** Low gain "Not defined", settle precision, caption 4.5:1 | **FAIL** | Low gain now reads Phase margin **"Not defined"** with "No gain crossover in range." (NaN fix landed, `margins.py:69-80`). Settle text keeps precision ("0.00100"). **But the margin captions render `#8A8A86` at 11px: 3.47:1 on white.** Computed style confirmed in a live page. Root cause below (section 3). The `studio-r7.spec.ts` caption test fails on this commit, light and dark |
| **G6** PID to motor gap at least 48px, one block name, no overflow | **PASS** | Measured in a live page: gap **48.0px**, PID **168.0px**, at both 1280 (zoom 0.96) and 1440 (zoom 1.16). Plant reads "First-order plant" in all captures and sits inside its block. Block text 12.5px at 1280, 15.1px at 1440 on screen (at 85% zoom with the inspector open it is about 11px, the floor) |
| **G7** Inspector never clipped, Pin usable, selected dark captured | **PASS** | `studio-block-selected-after-simulate-light.png`, `studio-block-selected-dark.png` (new): inspector spans the full right column, Kp, Ki, Kd, "Pin comment" and "Pin" all visible, 2px cobalt outline on the PID block, margins and chart stay beside it |
| **G8** Home thumbnails read | **PASS** | `home-with-recent-light.png`, `home-dark.png`, `home-scrolled-*`: divider with Vin, resistors, ground and a Vout dot; `1 − e^(−t)` line with dashed final value; SMIB arc with two tinted areas; unit circle with `x` poles; stems. No blobs. Weak spot: "DC drive speed" and "First-order step" are almost the same curve (see 6.2) |
| **G9** Focus captures right, one dark, `NOTES.md` self-score | **FAIL** | A dark focus pair exists, but the elements are wrong in both themes. `focus-tab-*.png` shows the **Skip to workspace link**, not a Work tab. `focus-button-*.png` shows the **Diagram tab**, not a button. `focus-table-row-light.png` shows the **Activity tab** on a Problem page, not a Problems row. `focus-tile-light.png` shows the **Home nav item** focused, with the tile only hovered. `NOTES.md` is four lines and still has no per-item self-score. The ring is black, not `--accent-500` |

---

## 2. Preflight and md5

**`preflight.json`: clean, verified.** `git_sha` is `53d8a46aca2e...` and matches the commit; `git_dirty_lines` 0; `package_path` is under `src/` (editable); `dist_index_mtime` 1794595822 is 00:20:22 IST, 12 seconds after the commit at 00:20:10 IST, so `dist` was rebuilt for this tree; `kp` 50; `step_series` true; `gain_margin_caption` correct; `low_gain_pm_deg` "Not defined" (the probe now covers the Low gain golden, which was my round 6 ask). It does not yet probe the Finite crossover golden. Round 7 is the first round where the preflight is evidence rather than a label.

**md5 against round 6:** 0 of 69 identical; 60 same name and changed; 9 new (`focus-button-dark`, `focus-tab-dark`, `studio-block-selected-dark`, `studio-layout-{before,after}-simulate-1440-dark`, `studio-step-extended-dark`, `studio-step-settled-light`, `studio-step-unsettled-{light,dark}`); 0 dropped. All 69 match `md5.txt`; no two files are identical. Pixel diff against round 6: every page differs by 0.7 to 7.8% of pixels, which is the sidebar Recent list and the new Ctrl and Enter chips, plus Studio. `NOTES.md` says "All captures differ from round-4 md5 where compared": wrong baseline, it should be round 6.

---

## 3. EE Project's claims, verified

| Claim | Verdict | Evidence |
|---|---|---|
| Wires persist after Simulate (root cause: session loop replacing nodes) | **True** | Loop fix confirmed: `opening a session loads it once` allows at most 3 validate calls in 3 s and passed 20 of 20. Wires present in every after-Simulate capture. The extra "re-measure handles after node replacement" commit (`bd0d25f`) closes the 1-in-40 case; I saw 0 in 40 |
| Arrowheads use `currentColor` | **True** | Code and pixels, 14.2:1 dark |
| Step chart: axes, single header, Auto | **True** | G3 |
| Unsettled state shown | **True** | G4 |
| New captures: dark 1440, selected-dark, focus-dark | **Three of three exist; focus-dark shows the wrong elements** | G9 |
| Home thumbnails redrawn per 6.6, CSS fill override was the cause | **True** | `ExampleThumb.jsx` now sets a class per shape. The old `.example-thumb-accent` rule (`fill: var(--ee-color-primary)`, `tokens.css:1453`) is still in the stylesheet and will blob again if anyone reuses it. Delete it |
| kbd chips in, CLI line removed | **True** | "Press [Ctrl] [Enter] to solve" as two chips in `home-with-recent-light.png`; `Shortcut.jsx` now renders one `kbd` per key; Cmd+K chips match. The `electrical-engineer mcp` command remains under "Agent", which is fine |
| Studio empty-state hint shows once | **True** | One "Run Simulate to see the step response and margins." in the drawer, none in the inspector |

**Why the caption stays grey (G5 root cause).** `control-studio/tokens.css:12` sets `--cs-text-muted: #70706c`, but `src/tokens.css:1808` (the product-workspace scope) remaps it: `--cs-text-muted: var(--ee-color-faint)` which is `#8a8a86`. The remap wins, so every Studio caption, light and dark, is the faint grey. Light is 3.47:1. A second `.studio-margin-meta` block at `studio.css:535` also forces `font-size: 11px` and `max-width: 14rem` over the 12px, two-line-clamp block at line 159.
**Fix:** `src/tokens.css:1808` becomes `--cs-text-muted: var(--ee-color-muted);` (`#70706C` light, `#A3A39E` dark). Delete the duplicate block at `studio.css:535-541`.

---

## 4. Round 6 open items

| Item | Status | Evidence |
|---|---|---|
| `useWireStroke` read `--cs-wire` from the wrong element | **Fixed** | Hook deleted, `currentColor` plus canvas `color`. Dark heads visible |
| `PID_W` 144 vs 168 | **Fixed** | `layout.py:8` `PID_W = 168`, `GAP = 48`; new `tests/unit/test_studio_layout_css.py` compares CSS widths to the Python constants. Live gap 48.0px |
| Phase margin "Infinite" from NaN | **Fixed** | `_fmt_pm` treats non-finite gain crossover as "Not defined". Low gain capture and `low gain: phase margin is not defined` both pass |
| Two specs that pass without checking | **Partial** | `studio-r5` dark arrowhead test was rewritten to count `marker-end` attributes only, so it still passes with invisible heads (the real colour check is now in `studio-r6`, which is sound). `studio-wire-selection` now skips any element that is invisible or times out and still has no count assertion, so zero drawn wires would pass. `playwright.config.ts` also gained `retries: 2`, which hides the very flake they fixed. Run at `retries=0`, all 23 pass |
| Playbook and critiques on `main` | **Not on `main`; on the PR branch** | `origin/main` is `7b2a9aa`. It has `studio-layout`, `studio-r5`, `studio-wire-selection` specs and `docs/design/{DESIGN,cobalt-ui-design-system}`. PR #58 adds `docs/design/DESIGN_PLAYBOOK.md` (byte-identical to mine, 672 lines), `docs/design/round6-critique.md` (identical to my round 6) and `ui/e2e/studio-r6.spec.ts`. Not on the branch: round 3, 4, 5 and 7 critiques. Merging #58 carries everything else |

**Specs I ran** on `53d8a46` in the scratch build, `retries=0`: **23 of 23 pass** (layout 3, r5 5, r6 13, wire-selection 2). Then `--repeat-each=20` on the edge-path and session-loop tests: 60 of 60. I wrote `round7/studio-fix/studio-r7.spec.ts` (caption 12px and 4.5:1 in both themes; Home thumbnail well 1.05 to 1.25:1 in both themes). On `53d8a46`, **3 of 4 fail by design**: caption light, caption dark (11px), thumbnail well dark (1.00:1). They pass once fixes 1 and 4 below land.

---

## 5. Status of round 6's 12 fixes

| # | Fix | Status | Evidence |
|---|---|---|---|
| 1 | Wires at 1440 | **Done** | G1 |
| 2 | Dark arrowheads | **Done** | G2 |
| 3 | Step chart | **Done, 2% band missing** | G3 |
| 4 | Unsettled and extended captures | **Done** | G4 |
| 5 | Margins semantics and tokens | **Partial** | NaN and precision done; caption colour and size not (section 3) |
| 6 | Layout constants and label | **Done** | G6 |
| 7 | Inspector spans both rows | **Done** | G7 |
| 8 | Home thumbnails, kbd chips, CLI line | **Done** | G8 |
| 9 | Problems and Cmd+K finish | **Partial** | Hover row now runs the rule full width with three icons (`problems-row-hover-light.png`), but the resting row rule still stops at about 920px while the header bar runs to 1004px (`problems-list-light.png`). Subject and Made by still native selects, tags still 11px caps, "Details" still 4px under "Try again" |
| 10 | Gallery and Library finish | **Not done** | Gallery ids (`power.swing_equal_area`) still shown, mixed image heights, white PNGs on dark cards. Library unchanged: wrapping "Add a source", inline form, native file input and selects |
| 11 | Focus and dark capture set | **Partial** | Selected-dark and breadcrumb title done. Focus elements still wrong (G9) |
| 12 | Process | **Partial** | Clean preflight and Low gain probe done. Playbook and round 6 critique on the PR branch. No `NOTES.md` self-score. Config `retries: 2` added |

---

## 6. Scores

| # | Criterion | R5 | R6 | **R7** | One-line reason |
|---|---|---|---|---|---|
| 1 | Answer-first hierarchy | 4 | 4 | **4** | Unchanged and still the best part. Answer, Checked strip, stale strip all hold in both themes |
| 2 | Layout, spacing, alignment | 3 | 4 | **4** | Studio is now a real workspace at 1280 and 1440. Held back by a 240px empty drawer before Simulate, a half-clipped palette, a short Problems rule and the Library column |
| 3 | Typography | 3 | 3 | **3** | Chart ticks and titles fixed. Margin captions 11px at 3.47:1, 11px caps tags, unlabelled chevron |
| 4 | Colour and accent discipline | 3 | 3 | **4** | Dark window buttons 7.4:1, arrowheads 14.2:1, pill 4.61:1. Light amber pill in dark mode is loud; caption token leak is counted under Typography |
| 5 | Surfaces, borders, elevation | 4 | 4 | **4** | Flat hairlines, no shadows. Native selects and file input remain; thumbnail well is light-only |
| 6 | States and interaction | 4 | 4 | **4** | Selected state (dark too), settled, off-target, unsettled, extended, stale, empty and error all exist. Dark Work chevron is an unstyled native button; focus captures wrong |
| 7 | Plots | 2 | 3 | **4** | Themed SVG with ticks, units, setpoint, Auto window and honest pills; Home thumbnails now read. No band or marker on the plot, Gallery still raw white PNGs |
| 8 | Schematics and block diagrams | 3 | 3 | **4** | Orthogonal wires with heads in both themes and viewports, 48px gaps, labels inside blocks. A loose unused port ring under "First-order plant" |
| 9 | Trust and copy | 2 | 3 | **4** | Margins are physically right (Finite crossover: PM 95.7° and crossover 9.95 rad/s match 10/(s+1)·feedback exactly; Low gain: PM "Not defined"). "Settles at 0.909" has no unit and clashes with "Settled at 0.43 s" |
| 10 | Shell, navigation, consistency | 4 | 4 | **4** | 240 and 56 exact, Cmd+K chips, no duplicates. Black focus ring instead of cobalt; Recent shows test scenario names in some captures |
| | **Total** | 32 | 35 | **39 / 50** | Clears 38 |

Margin for error: Typography is the one 3. A reviewer who marks Plots 3 for the Gallery would land on 38, still at the gate.

### 6.1 Thumbnail well decision: **show it in both themes**

The playbook already decides this: section 3.2 puts every Home thumbnail on `--surface-subtle` at the same 160 x 96 frame, and round 6 fix 8 said "same frame in both themes". The well has no border and no shadow, so it does not break the hairline and no-shadow rules, and it is one nesting level (tile, then well), inside the playbook's limit of two. Removing it instead would drop the shared frame that keeps six different-shaped drawings visually equal, and the line art would float on the tile. Dark mode is a token bug, not a design choice: measured, the dark tile and the dark well are both `rgb(26,26,24)`, 1.00:1, while light is 1.09:1.
**Fix:** `.example-thumb-bg { fill: var(--ee-color-surface-soft); }` resolves to the same colour as the tile in dark. In the dark scope set `--ee-color-surface-soft: #121211` (the canvas colour, **1.075:1** against the tile, matching light's 1.09). No border added. Test: `studio-r7.spec.ts`, well ratio between 1.05 and 1.25 in both themes.

### 6.2 Smaller thumbnail point
Tile 2 "First-order step" and tile 4 "DC drive speed" are the same rising exponential with a dashed asymptote. Give DC drive a different read: add a faint second line for the load-torque dip (a small step down at 60% of the width), or draw a motor-and-shaft glyph.

---

## 7. Per-screen issues

### Studio (`studio-layout-*`, `studio-block-selected-*`, `studio-step-*`, `studio-margins-*`, `studio-after-resize-light.png`)
- Margin captions under the four values (`studio-layout-after-simulate-light.png`, margins strip): 11px `#8A8A86`, see section 3.
- Chart header (`studio-margins-no-crossover-light.png`, right of the window control): "Settles at 0.00100, 99.9% below the setpoint" has no unit, and "Settles at" reads like a time next to "Settled at 0.43 s" in the PID capture. Use "Steady state 0.00100, 99.9% below setpoint" and "Steady state 0.909, 9.1% below setpoint".
- Before Simulate (`studio-layout-before-simulate-light.png`, bottom drawer): an empty 240px white box with one grey line takes 40% of the screen and leaves the canvas only about 250px. The height is reserved on purpose so the canvas does not re-fit, which is right, but fill it: skeleton of the margins strip (four 16px grey bars) and an empty axis frame with ticks, or the same height with a "Simulate" primary button inside.
- Palette (`studio-layout-before-simulate-light.png`, left column): 8 of 16 blocks visible and a half-clipped glyph under "Integrator". Add a 16px bottom fade and a visible scrollbar thumb, or show 6 and a "More" row.
- `studio-after-resize-light.png` (1280 x 680): the drawer's bottom border is cut off by the viewport, the page scrolls. Acceptable at this height, but the minimum should be stated (min-height 560 on the grid is why).
- Plant block (`studio-margins-finite-light.png`): an unused blue port ring under "First-order plant". Hide unconnected optional ports until hover.
- `studio-step-unsettled-dark.png`: a "HUMAN" badge appears inside the PID block, 8px caps. Fine as a feature, but it is under 11px; move it to the inspector title or make it 11px.
- Chart: add the 2% band (`--cs-accent` at 8% opacity) and a vertical dotted line at the settle time with the label "0.43 s". Overshoot gets a small cobalt dot at the peak with "1.6%".
- Dark: the amber pill is a bright light patch. Use `--warning-tint` dark (`#2A2210`) with `--warning-ink` `#F5B35A` (check 4.5:1).

### Home (`home-empty-light`, `home-with-recent-light`, `home-dark`, `home-scrolled-*`, `focus-tile-light`)
- Thumbnails fixed; well missing in dark (6.1); tiles 2 and 4 near-identical (6.2).
- "Continue" cards duplicate the sidebar Recent list in function; fine, but the sidebar Recent in some captures shows test scenario names ("Finite crossover", "Low gain"). Clear `runs/` and create sessions with real titles before capture.

### Problem (`problem-*`, `focus-*-dark`, `sidebar-collapsed-dark`)
- **Dark Work tab (`problem-work-dark.png`, step 2, under "Vout from Vin, R1, R2"):** the expand control is a near-white native button on a near-black page. It is `.step-expand` in `StepTimeline.jsx:81` and **has no CSS at all**, so it is the browser default in both themes (a grey boxed chevron in light). It also has no accessible name. Fix: 28 x 28, transparent, `color: var(--text-secondary)`, hover `--surface-subtle`, `border-radius: 4px`, `aria-label="Show working"`, rotate the chevron 180 degrees when open.
- Step 2 has a hidden body but the page never shows the working (the divider equation) unless clicked. The answer-first rule is met; the "show the work" rule is better met with step 2 expanded by default.
- Parameters drawer (`problem-parameters-stale-light.png`): the stale message appears twice (banner and drawer) and the drawer's "Run again" wraps to two lines. Drop the drawer copy, keep one 28px "Run again".

### Problems, Cmd+K, rail (`problems-*`, `cmdk-*`, `sidebar-collapsed-*`)
- Resting row rule stops at about 920px while the header bar reaches 1004px (`problems-list-light.png`, `problems-list-dark.png`). Make the actions column always occupy its width.
- Native selects for Subject and Made by (`problems-list-light.png`, top right). Style them: 32px, 6px radius, `--border-input`, chevron icon.
- "Details" is 4px under "Try again" (`problems-error-dark.png`). Use 12px.
- Cmd+K (`cmdk-open-light.png`) is good: grouped, chips, footer hints. Leave it.
- 240px and 56px are exact in `sidebar-measurements.json` (`240px 1040px`, `56px 1224px`, 240 with the palette open).

### Gallery, Library, Settings
- Gallery (`gallery-light.png`, `gallery-dark.png`): ids still printed under titles, image heights vary per card, white PNGs sit directly on dark cards. Add a 16:10 `--surface-subtle` mat, hide ids, one SMIB card with a GIF toggle.
- Library (`library-light.png`, `library-dark.png`): "Add a source" wraps to two lines, the "Add a book" form is inline below the table, the native file input and selects are unstyled, the "Used in 2, 6" column is meaningless. Move the form into a dialog.
- Settings (`settings-engines-dark.png`): heavy table header and a second rule line under the table. Minor.

### Focus (`focus-*`)
See G9. Use real Tab presses and name the element in the filename.

---

## 8. Ready to show Vinayak?

**No, not yet. Round 8 should be the one to show him; it is a half-round.**

| Gate | Round 7 | Pass? |
|---|---|---|
| Total at or above about 38 | 39 | Yes |
| No criterion below 3 | Lowest is 3 (Typography) | Yes |
| No visible correctness errors | Margins and settling text are right. A visible miss: 11px captions at 3.47:1, an unstyled button in dark, a unit-less "Settles at" | **No** (cosmetic and accessibility, not wrong numbers) |
| All nine G items pass | 7 of 9 | **No** (G5, G9) |

**Exact blockers for round 8** (all mechanical, none needs design thinking):
1. Caption token: `src/tokens.css:1808` and the duplicate `.studio-margin-meta` block (G5).
2. Focus captures on the right elements, plus a per-item `NOTES.md` self-score (G9).
3. Work step chevron styled and named (dark mode defect).
4. Thumbnail well in both themes.
5. Merge #58 so the playbook, round 6 critique and `studio-r6.spec.ts` reach `main`, and tighten the two weak specs.

**Estimate:** one half-round. If those five pass, the projected score is **41 to 42** and the verdict flips to yes. Fixes 6 to 12 are polish that would take it to 43 but are not gating.

---

## 9. Ranked fix list (12, ordered by what moves "ready"; paste into the round 8 prompt)

1. **Margin captions** (G5). `src/tokens.css:1808` set `--cs-text-muted: var(--ee-color-muted);`. Delete `.studio-margin-meta` at `studio.css:535-541`, keep the block at line 159 (12px, 16px line, two-line clamp, `max-width: none`). Add `studio-r7.spec.ts` caption test (12px, at least 4.5:1, both themes).
2. **Focus captures** (G9, `capture_ux_review_round.py`). Reach elements by Tab presses and assert `document.activeElement` before the shot: `focus-tab` on the Work tab (first Tab after the skip link, then `Tab` into the tab list), `focus-table-row` on a Problems row (on `/problems`), `focus-button` on "Run again", `focus-tile` on an example tile, `focus-composer` on the textarea. One dark of each. Ring `outline: 2px solid var(--accent-500); outline-offset: 2px` on all (4.57:1 on white; in dark use `--accent-400`). `NOTES.md`: a table, one row per fix number with done, partial or not done and the file that proves it.
3. **Work step expander** (`StepTimeline.jsx:81`, `tokens.css`). `.step-expand { width: 28px; height: 28px; display: inline-grid; place-items: center; border: 0; border-radius: 4px; background: transparent; color: var(--ee-color-muted); cursor: pointer; }`, hover `background: var(--ee-color-surface-soft)`, `:focus-visible` ring, `aria-label="Show working"`, `aria-expanded` already there. Chevron rotates 180 degrees on open. Expand step 2 by default on a Checked problem.
4. **Thumbnail well in both themes** (6.1). Dark `--ee-color-surface-soft: #121211`; keep `.example-thumb-bg { fill: var(--ee-color-surface-soft) }`; delete `.example-thumb-accent` at `tokens.css:1453`. DC drive speed gets a distinct drawing (6.2).
5. **Merge #58 and fix the specs.** Merge the playbook and `round6-critique.md`; add `artifacts/ux-review/round-{3,4,5,7}/CRITIQUE.md`. `studio-r5` dark test: delete it (the r6 one covers it) or assert marker fill contrast at least 3:1 and at least four markers. `studio-wire-selection.spec.ts`: add `expect(n).toBeGreaterThanOrEqual(10)` on the measured set and remove the `continue` on timeout. `playwright.config.ts`: `retries: 0`. Add `studio-r7.spec.ts` (provided in `round7/studio-fix/`).
6. **Settle wording** (`ResultsDock.jsx`). "Steady state 0.909 (9.1% below setpoint)"; use units when the plant has them ("0.909 rad/s"). Keep "Settled at 0.43 s" for time.
7. **Plot annotations** (`StepChart.jsx`). 2% band, settle-time dotted line with a label, overshoot peak dot with its percentage.
8. **Before-Simulate drawer.** Fill the reserved 240px with a skeleton (four margin bars, an empty axis frame) or a primary "Simulate" button; keep the height so nothing re-fits.
9. **Palette scroll affordance.** 16px bottom fade, visible scrollbar, no half-clipped row.
10. **Problems list finish.** Resting rule to the full width, 32px styled selects, tags 12px sentence case, 12px gap above "Details".
11. **Gallery and Library finish.** Gallery: hide ids, 16:10 equal frames on `--surface-subtle`, one SMIB card with a GIF toggle. Library: "Add a source" on one line, form in a dialog with a drop zone, 36px styled selects.
12. **Capture hygiene.** Clear `runs/` per theme and create sessions with real titles so Recent never shows "Finite crossover" or "Low gain"; preflight also probes the Finite crossover golden; `NOTES.md` md5 comparison against round 7, not round 4; unused ports hidden until hover; "HUMAN" badge at 11px; dark pill tinted not bright.

---

## 10. Round 8 checklist

Every capture: theme in the filename, `data-theme` reset first, 1280 x 800 unless stated, unedited `preflight.json` with the dirty flag, `runs/` cleared per theme, md5 diff against round 7.

**Studio (light and dark, 1280 and 1440, before and after Simulate):** wires, heads, labels, 48px gap, ticks, margins strip with 12px captions at 4.5:1.
- `studio-block-selected-{light,dark}.png` and `studio-block-selected-after-simulate-{light,dark}.png`.
- `studio-step-{settled,unsettled,extended}-{light,dark}.png`, `studio-step-offtarget-light.png` with the band and settle marker visible.
- `studio-margins-{finite,no-crossover}-{light,dark}.png`, `studio-after-resize-light.png`, a before-Simulate capture showing the new empty-drawer skeleton.

**Home:** the three light captures, `home-dark.png` and the two scrolled shots, with a visible thumbnail well in both themes.

**Problem:** `problem-work-dark.png` showing the styled expander, step 2 open; light twin.

**Focus, by real Tab presses, with `activeElement` asserted:** tab, table row, button, tile, composer, light and dark.

**Pages changed:** `problems-list`, `problems-row-hover`, `gallery`, `library` (plus the Add dialog open), the five Settings tabs, light and dark.

**Logs to attach:** `preflight.json`, `sidebar-measurements.json`, Playwright output for all five spec files at `retries=0`, the md5 diff, a contrast table for captions, pills, arrowheads and window buttons.

Files reviewed: all 69 PNGs in `round7/` (the Settings tabs, Home variants and Problems states not named above I read through their light or dark twins), `NOTES.md`, `md5.txt`, `preflight.json`, `sidebar-measurements.json`. Source read from `53d8a46` (a `git archive` copy built and run in `/tmp/r7w`) and `origin/main` at `7b2a9aa`, read-only. Nothing was pushed, merged or commented on.
