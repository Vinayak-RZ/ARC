# Arc round 9 critique

Code `2297a66`, PR #58 head `605b445`. I read all 75 PNGs, `NOTES.md`, `focus-log.json`, `md5.txt`, `preflight.json` and `sidebar-measurements.json`. I built `2297a66` from `git archive` in a scratch copy (`/tmp/r9w`), ran their server on it, and ran all 32 e2e specs, the three step-metric, caption and layout unit-test files, and my own probes. Their repo was not touched.

**Score: 41 / 50** (trend 25, 30, 32, 33, 32, 35, 39, 40, **41**). Gates G1 to G9: **all pass.** Round 8 gates: **all three pass.**

**Ready to show Vinayak: YES, with the curated pack in `SHOW_PACK.md`.** The score clears 38, nothing is below 3, and I found no wrong number or clipped value in the captures I would show. Two things to know before he clicks around live, both listed in section 5: the settling time shifts by up to 4% when he changes the window button (a sampling effect, easy fix), and the Low gain chart has overprinted labels, so it is not in the pack.

---

## 1. Gates

### G1 to G9

| Gate | Result | Evidence |
|---|---|---|
| **G1** Wires, heads, labels, both widths, both themes | **Pass** | Every Studio capture, including `studio-layout-after-simulate-1440-dark.png`: 5 wires with heads and `r, e, u, y`. `studio-wire-selection` and `studio-r6` green at `retries: 0` |
| **G2** Dark arrowheads | **Pass** | White heads on the dark canvas; `studio-r5` checks head paint equals wire colour |
| **G3** Step chart, band, settle marker, overshoot dot | **Pass, with label clutter** | `studio-step-settled-{light,dark}.png`: "Settling time 0.43 s · Overshoot 1.6%", dotted marker with "0.43 s", dot at the peak, "Setpoint 1.00", "±2% of final value". The "1.6%" label is struck through by the setpoint line (5.3) |
| **G4** Not settled, off target, extended | **Pass** | `studio-step-unsettled-*`: pill "Not settled within 600 s", **no band, no marker**, only "Setpoint 1.00". `studio-step-extended-*`: 30 s window, pill "within 30 s". `studio-step-offtarget-light.png`: see R9-B |
| **G5** Caption 4.5:1, 12px, complete | **Pass** | `studio-r7` green (4.97:1 light, 6.88:1 dark, 12px). Captions now read "No −180° crossing in 0.001 to 100,000 rad/s." and "Phase above −180° over 0.001 to 100,000 rad/s." and are whole in every inspector-open capture |
| **G6** Gap and labels | **Pass** | 48px gap, 168px PID, unchanged and green |
| **G7** Inspector never clipped | **Pass** | `studio-block-selected-after-simulate-light.png`: Kp, Ki, Kd, "Pin comment", "Pin" all visible, margins and chart beside it |
| **G8** Thumbnails, well in both themes | **Pass** | Unchanged from round 8 (1.075:1 dark, 1.09:1 light); `studio-r7` well test green |
| **G9** Focus captures | **Pass** | Five light and five dark focus captures byte-identical to round 8 and still correct; `focus-log.json` unchanged |

### Round 8 gates

| Gate | Result | Evidence |
|---|---|---|
| **R9-A** Captions never truncated | **Pass** | Five previously clipped captures (`studio-block-selected-after-simulate-light`, `studio-step-unsettled-*`, `studio-step-extended-*`) now show whole sentences. Copy shortened, clamp is 3 lines. `studio-r8` truncation tests green in both themes, and `studio-r5` has a new vertical-overflow check |
| **R9-B** Settling against the final value | **Pass** | See section 2. Setpoint line, final-value label, e_ss label, band, marker and overshoot dot are all present and consistent with each other. Unsettled shows no band |
| **R9-C** Capture state | **Pass** | `cmdk-open-dark.png` is on the Problems list, `sidebar-collapsed-dark.png` on the Checked problem, both clean. Recent shows "Lab 4 · DC motor PID", "HW 3 · Unity feedback, K = 10", "HW 3 · Open-loop gain". No "Control Studio", "Low gain" or "Finite crossover" |

---

## 2. R9-B in the pixels and the code

**Is 0.3556 confirmed? Yes. I was wrong to write 0.34, and `round8/CRITIQUE.md` is corrected.** The closed loop is `10/(s+11)`, so the step is `0.9091 (1 − e^(−11t))`. It is within 2% of the final value when `e^(−11t) ≤ 0.02`, which gives `t = ln(50)/11 = 0.35564 s`. My 0.341 s came from running the metric on a 0.02 s grid and reading the last sample outside the band (0.3407 s), which is the grid, not the answer. I should have checked it against the closed form, as I asked EE Project to do. In `round8/CRITIQUE.md` I replaced 0.34 with 0.356 (table), 0.36 (display copy) and 0.356 ± 0.01 (the spec I proposed for the unit test).

**`studio-step-offtarget-light.png` (K = 10), left to right:** header "Settling time 0.36 s · Final value 0.909 · 9.1% below setpoint"; dashed "Setpoint 1.00" at 1.0; the curve flattens at 0.909 (the dotted final-value line sits under it); right-end labels "Final value 0.909" and "e_ss = 9.1%"; "±2% of final value" label; band drawn around 0.909, not 1.0; dotted marker with "0.36 s". Band and pill no longer contradict each other. Correct: the 0.36 is ln 50 / 11.

**Metric check (I recomputed, not from their numbers).**
- `final_value` 0.90909, `t_settle_s` 0.3550, `overshoot_pct` 0.0, `steady_state_error_pct` 9.1 on Auto. On a 100 s window the reported value is 0.340.
- K = 39 (2.5% off target) and K = 60 (1.6%) now both report a settling time, and the `on_target` flag alone follows the 2% rule. The discontinuity from round 8 is gone.
- Under-damped test (ζ = 0.3, ωn = 5): overshoot 37.23% against the textbook 37.23%.
- A still-rising loop (Kp 0.08, Ki 0.02) stays `not_settled` with no `t_settle_s`.
- 15 unit tests pass (`test_step_metrics`, `test_margin_captions`, `test_studio_layout_css`).

**Their claim "t_s 0.355 s" is true only for the Auto window.** It is the fine-grid value (3 s window, 0.006 s step). On any fixed window the app reads about 4% low:

| Loop | Auto | 10 s | 30 s | 100 s | Theory |
|---|---|---|---|---|---|
| K = 10 | 0.355 s | 0.341 s | 0.340 s | 0.340 s | 0.3556 s |
| PID DC motor | 0.425 s | 0.421 s | 0.420 s | 0.420 s | n/a |

The header shows "0.36 s" on Auto and "0.34 s" after pressing 10 s, for the same loop. The unit test hides this on purpose ("the last sample outside the band sits at most one step before the true time", tolerance 1.5 steps) and the 1% test runs on a 50,001-point grid. It is a sampling artefact, not a wrong definition, and fast loops get worse: K = 200 returns **0.0 s** (true 0.019 s) because the first sample after t = 0 is already inside the band. **Fix:** after finding the last sample outside the band, linearly interpolate the band crossing between that sample and the next. That makes the result window-independent to better than 0.1%. `studio-fix/studio-r9.spec.ts` encodes it; on `2297a66` it fails (10 s window 4.0% off Auto, theory test off by 0.015 s).

---

## 3. Claims

| Claim | Verdict | Evidence |
|---|---|---|
| 32/32 e2e at retries 0, including `studio-r8` | **True** | I ran all 32: passed in 1.5 minutes, `retries: 0`. The `studio-r8.spec.ts` in the repo is byte-identical to mine |
| K = 10: final 0.9091, t_s 0.355 s | **True for Auto only** | Section 2 |
| 3-line clamp with overflow test | **True** | Plus shortened copy. Clipping gone in all five captures |
| Captures start from reset, student titles | **True** | R9-C |
| Expander toggles Show/Hide working | **True, and better than asked** | `problem-work-dark.png`, `problem-work-tab-light.png`: step 2 is open by default and shows "Vout = Vin R2 / (R1 + R2)" in real subscript type, chevron points up. `problem-r9.spec.ts` green |
| Preflight clean, now with Finite crossover | **True** | `git_sha` `2297a66`, 0 dirty lines, `dist` built 01:22:57 IST, 7 seconds after the commit at 01:22:50 IST, and the new `finite_crossover` block reads `settled_off_target`, 0.9091, 0.355 s, 0.0, 9.1 |
| CI green | Not checked; I do not have CI access. All specs and unit tests pass locally | |
| 75 captures, md5 | **Matches** | 45 changed, 30 byte-identical (the unchanged light pages and focus shots), 0 new, 0 dropped, no duplicates, all match `md5.txt` |

**PR #58 contents:** playbook, round 3 to 7 critiques, specs and code. The round 8 and round 9 critiques are not in `design-critiques/` yet. Nothing is on `main`.

---

## 4. Their self-flagged items: gate or polish

| Item | Decision | Reason |
|---|---|---|
| "1.6%" label crowds the setpoint line | **Polish, do it next round (10 minutes)** | Confirmed in `studio-step-settled-*`, `studio-block-selected-after-simulate-light.png`, `studio-layout-after-simulate-1440-dark.png`: the text is struck through by the dashed line. It is legible but untidy on the hero chart. Fix: place the label 10px above the dot, `paint-order: stroke`, 3px `--surface` halo, and skip it if the peak is under 0.5% |
| Long Recent title truncates | **Polish** | Truncation with an ellipsis (`HW 3 · Unity feedback, …`) is correct behaviour. Add a `title` tooltip and the full name in the Cmd+K list |
| Gain crossover 8.735 vs 9.95 | **Polish** | Cause: `margins.py:27` uses `f"{x:.4g}"`, which strips trailing zeros, so 9.950 prints as 9.95. Not wrong. Rule: 4 significant figures with trailing zeros kept ("9.950 rad/s"); `0.001998` is already 4. One format helper for all margins |
| Round 7 items 8 to 11 open | **Polish for the pack, gating if he browses** | Before-Simulate drawer, palette fade, Problems list, Gallery and Library: none changes a number or breaks the Studio and Problem story. The pack leaves those screens out. If Vinayak will click through Library and Gallery himself, do items 10 and 11 first |

---

## 5. Other findings

### 5.1 Settling time depends on the window
Section 2. Not a gate for the pack (every captured chart uses Auto), but it is the top fix before a live demo, because the app's promise is checked numbers.

### 5.2 Low gain chart (`studio-margins-no-crossover-light.png`, `-dark.png`)
- Header says "Settling time 3.90 s · Final value 0.00100 · 99.9% below setpoint". The 3.90 s is correct against the final value (ln 50 times a 1 s lag), but a response that stays 99.9% below its target has no useful settling time; it is the less important fact.
- "±2% of final value" and "Final value 0.00100 / e_ss = 99.9%" are drawn over the x-axis tick numbers "20" and "30", because the final line sits on the axis.
- Auto window reads "31 s window", not a round number.
**Fix:** when `|e_ss| > 50%`, lead with "Final value 0.00100 · 99.9% below setpoint" and drop the settling time to the marker label only; when the final line is within 12% of the axis, place its labels above the line and the band label at the left; round the Auto window up to 1, 2 or 5 times a power of ten (30 s).

### 5.3 Overshoot label
See section 4. `studio-r9.spec.ts` asserts that no `%` label intersects the setpoint line or a tick number.

### 5.4 Band is almost invisible after settling
At ±2% on a 0 to 1.05 axis the band is 2.7px tall, the same as the curve, so after the curve enters it the band is hidden. This is faithful to the data. Optional: draw the two band edges as 1px dotted lines in `--text-muted` so they stay visible beside the curve.

### 5.5 Still open from earlier rounds
Unchanged and listed in the fix list: before-Simulate drawer is an empty 240px box; palette has a half-clipped row; Problems resting rule stops at about 920px, native selects; Gallery ids and white PNGs on dark; Library inline form; duplicate stale message in the Parameters drawer. All byte-identical captures show them unchanged where relevant (`problems-list-light.png`, `library-dark.png`, `gallery-dark.png`).

---

## 6. Scores

| # | Criterion | R7 | R8 | **R9** | One-line reason |
|---|---|---|---|---|---|
| 1 | Answer-first hierarchy | 4 | 4 | **5** | Answer with units is the largest thing, Checked and engine stated beside it, and the working is now open by default with the equation in real subscript type. One primary action |
| 2 | Layout, spacing, alignment | 4 | 4 | **4** | Captions whole, Studio stable. Empty drawer, palette clip, Problems rule, Library pending |
| 3 | Typography | 3 | 4 | **4** | 12px captions at 4.97:1, subscripts, tabular numbers. Tags still 11px caps; margin precision inconsistent (9.95 vs 8.735) |
| 4 | Colour and accent discipline | 4 | 4 | **4** | Clean contrast table, cobalt used sparingly. Light amber pill in dark still loud |
| 5 | Surfaces, borders, elevation | 4 | 4 | **4** | Flat hairlines, well in both themes. Native selects and file input remain |
| 6 | States and interaction | 4 | 4 | **4** | Selected, unsettled, extended, stale, focus, toggling expander all real. No drawer skeleton |
| 7 | Plots | 4 | 4 | **4** | Setpoint, final value, e_ss, band, marker, peak dot and honest unsettled state. Label clutter (1.6%, Low gain), band hidden under the curve, Gallery still raw PNGs |
| 8 | Schematics and block diagrams | 4 | 4 | **4** | Stable, strictly tested, both themes and widths. Unused port ring under the plant |
| 9 | Trust and copy | 4 | 4 | **4** | Numbers right in the pack. Window-dependent 4% shift in settling time and "Settling time 3.90 s" on a flat output keep it from 5 |
| 10 | Shell, navigation, consistency | 4 | 4 | **4** | Clean captures, student titles, focus system correct |
| | **Total** | 39 | 40 | **41 / 50** | Clears 38 |

---

## 7. Ready to show Vinayak?

**YES.**

| Gate | Round 9 | Pass? |
|---|---|---|
| Total at or above about 38 | 41 | Yes |
| No criterion below 3 | Lowest is 4 | Yes |
| No visible correctness errors (wrong captions, clipped values, duplicates, band against metric) | None in the pack. Labels clash on Low gain (not in pack) and the 1.6% label is overstruck (cosmetic) | Yes |
| All nine G items and all three round 8 gates | 12 of 12 | Yes |

**Before a live click-through (not before the pack), do these three, about an hour:**
1. Interpolate the band crossing in `_step_metrics` so settling time does not move with the window (5.1). Otherwise pressing 10 s changes K = 10 from 0.36 s to 0.34 s on screen.
2. Move the "1.6%" label off the setpoint line.
3. Keep him off Low gain, Library, Gallery and the Problems list until round 10.

**Estimate:** the pack is ready now. One more small round (round 10) takes it to about 43.

---

## 8. Ranked remaining fixes (paste into the round 10 prompt)

1. **Interpolate the settling time** (`simulate.py:_step_metrics`). After `settle_idx`, set `t_settle = t[i] + (t[i+1] − t[i]) × (|y[i] − y_ss| − band) / (|y[i] − y[i+1]|)` (linear crossing). Test `test_k10_golden_through_simulate` at 0.5% of 0.3556 s on the 10 s window; K = 200 gives 0.019 s, not 0. Add `studio-r9.spec.ts` (window independence within 1%, theory within 0.005 s).
2. **Overshoot label** (`StepChart.jsx`). 10px above the dot, `paint-order: stroke` halo, hidden under 0.5%.
3. **Low gain chart labels** (5.2). Suppress the settling time when `|e_ss| > 50%`; labels clear of tick numbers; Auto window on 1, 2, 5 steps.
4. **Number format** (`margins.py`). One helper, 4 significant figures, trailing zeros kept, unit after. "9.950 rad/s", "8.735 rad/s", "0.001998 rad/s".
5. **Recent titles.** `title` attribute on truncated rows, full name in Cmd+K.
6. **Before-Simulate drawer** (round 7 fix 8). Four-bar margins skeleton and an empty axis frame in the reserved 240px.
7. **Palette** (fix 9). 16px bottom fade, no half-clipped row.
8. **Problems list** (fix 10). Resting rule full width, 32px styled selects, tags 12px sentence case.
9. **Gallery and Library** (fix 11). Hide ids, 16:10 mats, dialog for "Add a book".
10. **Parameters drawer.** Drop the duplicate stale message in the drawer.
11. **Band edges.** 1px dotted lines in `--text-muted` so the band stays visible beside the curve.
12. **Process.** Merge #58; add round 8 and round 9 critiques to `design-critiques/`; keep `studio-r9.spec.ts` in `testMatch`.

---

## 9. Round 10 checklist
Every capture: fresh page and route, theme in the filename, 1280 x 800 unless stated, unedited `preflight.json`, md5 diff against round 9.
- `studio-step-settled-{light,dark}.png` with the label clear of the setpoint line; `studio-step-offtarget-{light,dark}.png` showing 0.36 s after a click on **10 s** as well as Auto.
- `studio-margins-no-crossover-{light,dark}.png` with the new Low gain header and clear labels.
- Every Studio chart with margins formatted to 4 significant figures.
- Problems list, Gallery and Library after fixes 8 and 9, both themes.
- Logs: all spec files at `retries: 0`, pytest output for `test_step_metrics.py`, preflight, md5 diff.

Files reviewed: all 75 PNGs in `round9/` (byte-identical ones checked by md5 against round 8, the rest read directly or through contact sheets), `NOTES.md`, `focus-log.json`, `md5.txt`, `preflight.json`, `sidebar-measurements.json`. Source read from a `git archive` of `2297a66` and `origin/pr58`. Nothing was pushed, merged or commented on.
