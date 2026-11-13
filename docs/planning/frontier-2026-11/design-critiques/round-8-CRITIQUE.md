# Arc round 8 critique

Code `25c1070`, PR #58 head `96855e6` (the head only adds captures and notes; no `ui`, `src`, `scripts` or `tests` change after `25c1070`). I read all 75 PNGs, `NOTES.md`, `focus-log.json`, `md5.txt`, `preflight.json` and `sidebar-measurements.json`. I built `25c1070` from `git archive` in a scratch copy (`/tmp/r8w`), ran their server on it, and ran every spec plus my own probes. Their repo was not touched.

**Score: 40 / 50** (trend 25, 30, 32, 33, 32, 35, 39, **40**). Gates G1 to G9: **all nine pass.**

**Ready to show Vinayak: NO, one small round away.** The score clears 38 and nothing is below 3, but the third test fails: there are visible defects. The margin captions are now **cut off mid-sentence in five Studio captures** whenever the inspector is open (a regression caused by the round 8 caption fix), and the **settling band and metric are referenced to the setpoint, not the final value**, so an off-target loop gets no settling time at all. Both are small. Round 9 should be a quarter-round, and it should be the one to show him.

---

## 1. Gates G1 to G9

| Gate | Result | Evidence |
|---|---|---|
| **G1** Wires, heads, labels, both widths, both themes | **Pass** | Every Studio capture shows 5 wires with heads and `r, e, u, y`. `studio-wire-selection` now asserts exactly 5 wires and at least 10 measured elements, and fails on any element with no bounding box (round 7 skipped them). Green at `retries: 0` |
| **G2** Dark arrowheads | **Pass** | `studio-r5` now resolves each wire's `marker-end` to its `<marker>` and requires the head paint to equal the wire colour. A real check where round 7's only counted attributes |
| **G3** Step chart, band, settle marker | **Pass, with the band defect in section 3** | `studio-step-settled-{light,dark}.png`: dotted line at 0.43 s with a "0.43 s" label, "±2% band" label and two edge lines. Band is 2.75px tall on screen (thin but visible). **Not drawn:** overshoot peak dot. **Wrong reference:** band is centred on the setpoint (section 3) |
| **G4** Not settled, off-target | **Pass** | `studio-step-unsettled-*`, `studio-step-extended-*` (30 s window), `studio-step-offtarget-light.png`. Unchanged and still correct |
| **G5** Low gain, precision, caption 4.5:1 | **Pass** | Computed in a live page: light `rgb(112,112,108)` on white **4.97:1**, dark `rgb(163,163,158)` on `rgb(26,26,24)` **6.88:1**, both **12px**. Their numbers are right. Root cause fixed (`--cs-text-muted` now `var(--ee-color-muted)`, duplicate 11px block deleted). `studio-margins-no-crossover-*`: Phase margin "Not defined". **But see 3.2: with the inspector open the captions are clipped** |
| **G6** Gap and labels | **Pass** | Unchanged: 48.0px gap, 168px PID |
| **G7** Inspector never clipped | **Pass** | `studio-block-selected-*`: docked, Kp, Ki, Kd, "Pin comment" and "Pin" visible |
| **G8** Thumbnails | **Pass** | Dark well now `rgb(18,18,17)` on a `rgb(26,26,24)` tile, **1.075:1**, light 1.09:1 (`home-dark.png`, `home-empty-light.png`). "DC drive speed" is now an under-damped response with a load dip, clearly different from "First-order step". `.example-thumb-accent` rule is gone |
| **G9** Focus captures | **Pass** | Verified in the pixels, not only the log. Composer ring on the card, example tile, "Open problem" action in the Problems row, **Work tab**, **"Run again"** (the stale banner button in the open Parameters drawer). All ten (five light, five dark) show a 2px cobalt ring (`rgb(47,111,235)` light, `rgb(107,147,245)` dark). `focus-log.json` records tag, class, outline and Tab count for each. `NOTES.md` has a per-gate and per-fix self-score table |

I agree with the builder's nine passes, with the two caveats in G3 and G5. Their self-score on fixes 6, 8, 9, 10, 11 as "not done" is accurate.

---

## 2. Verification of their claims

| Claim | Verdict | Evidence |
|---|---|---|
| 27/27 e2e at `retries: 0`, including my 4 `studio-r7` tests | **True** | I ran all 27: 27 passed, 1.3 minutes, `retries: 0` in `playwright.config.ts`. `studio-r7.spec.ts` on the branch is byte-identical to the file I wrote |
| Caption contrast 4.97:1 light and 6.88:1 dark | **True** | Section 1, G5 |
| Focus captures from real Tab presses, `activeElement` asserted | **True** | G9. Also an honest note in `NOTES.md` that Problems rows are not focusable, so the target is the row action, which now appears on `:focus-within` |
| `NOTES.md` has self-scores | **True** | Gate table, fix table, focus table. md5 line is also right: 13 identical (all light pages that did not change), 56 changed, 6 new, 0 dropped. All 75 match `md5.txt`, no two files are identical |
| Preflight clean | **True** | `git_sha` `25c1070`, `git_dirty_lines` 0, package under `src/`, `dist` built at 00:56:28 IST, 11 seconds after the commit at 00:56:17 IST. Still does not probe the Finite crossover golden |

**Round 7 secondary items**

| Item | Status | Evidence |
|---|---|---|
| `.step-expand` styling and label | **Done, two small gaps** | 28 x 28, transparent, 4px radius, `--ee-color-muted`, hover fill, 120ms chevron rotation, `aria-label="Show working"` (`tokens.css:1867-1882`, `StepTimeline.jsx:81`). Dark capture is now a quiet chevron, not a white box. Gaps: the label is static (stays "Show working" when open; `aria-expanded` covers it for screen readers, but the visible tooltip should flip to "Hide working"), and step 2 is still collapsed by default, so the working is hidden on the page that should show it |
| Thumbnail well in dark | **Done** | G8. Side effect: dark `--ee-color-surface-soft` is global, so other dark `surface-soft` users (headers, subtle fills) also went darker. I scanned the dark Problems, Library, Gallery, Settings and cmdk captures and see no regression |
| Weak specs | **Fixed** | `studio-r5` dark test, `studio-wire-selection` and `retries: 0`, see G1 and G2 |
| Critiques 3 to 7 on the PR branch | **Yes** | `docs/planning/frontier-2026-11/design-critiques/round-{3,4,5,6,7}-CRITIQUE.md`, all five byte-identical to mine. With `docs/design/DESIGN_PLAYBOOK.md` and `docs/design/round6-critique.md` from earlier. **None of it is on `main` (`7b2a9aa`) until #58 merges**; this round 8 critique is not in the repo yet |

---

## 3. Findings

### 3.1 The band question: reference the final value

**Yes. The band, the settle marker and the settling time should all be referenced to the final value, and the chart should show the setpoint as a separate line.**

Why: the standard definition, in Ogata, Nise and Franklin and Powell, is the time after which the response stays within ±2% of the **final (steady-state) value**. Percent overshoot is also relative to the final value: (peak − y_ss) / y_ss. The setpoint only enters through steady-state error, e_ss = (setpoint − y_ss) / setpoint. A type-0 loop settling at 0.909 is a well-defined, fully settled response with a settling time of ln 50 / 11 = 0.356 s (the closed loop is 10/(s+11)), and it should say so.

**What `_step_metrics` actually computes** (`simulate.py:35-97`):
- `band = 0.02 * sp`, and `settle_idx` is the last sample where `|y − setpoint| > band`. Setpoint-referenced.
- `t_settle_s` and `overshoot_pct` are set **only if** `status == "settled"`, which requires `|setpoint − y_end| / sp <= 2%`. So any loop with more than 2% steady-state error returns `t_settle_s: null` and `overshoot_pct: null`.
- Overshoot is `(peak − setpoint) / sp`, again setpoint-referenced.

**What the chart draws** (`StepChart.jsx:68-73, 140-160`): `bandLo = setpoint × 0.98`, `bandHi = setpoint × 1.02`, always, for every status. The settle marker only appears when `status === "settled"`.

I ran the metric on unity-feedback first-order loops `K/(s+1)`:

| K | y_ss | Status now | t_settle now | t_settle on final value | e_ss |
|---|---|---|---|---|---|
| 10 (the Finite crossover capture) | 0.9091 | settled_off_target | **null** | **0.356 s** (ln 50 / 11; my first run read 0.341 s, the last sample outside the band on a 0.02 s grid, which is the grid's rounding, not the answer) | 9.1% |
| 39 | 0.9750 | settled_off_target | **null** | 0.080 s | 2.5% |
| 60 | 0.9836 | settled | 0.080 s | 0.060 s | 1.6% |
| 200 | 0.9950 | settled | 0.020 s | 0.000 s | 0.5% |

Two real problems follow:
1. **A discontinuity.** K = 39 and K = 60 have almost the same response, but one gets a settling time and a marker and the other gets nothing, because 2.5% crosses an arbitrary line. And for K = 10 the student, who knows ts is about 4 / (K + 1), sees no number.
2. **The drawn band can contradict the label.** In `studio-margins-finite-light.png` and `studio-step-offtarget-light.png` the ±2% band sits at 1.0, the curve flattens at 0.909 well below it and never enters it, and the header says "Settles at 0.909". The band says "this response does not settle". The metric reports no time, so there is no *numeric* contradiction on screen today, but the picture and the pill disagree, and the moment someone fixes the metric to the textbook definition the band would contradict the reported time. I rate it a **visible correctness defect and a round 9 gate item**. For the PID capture (final value equals the setpoint) the band is correct.

**Spec (backend and chart):**
- `_step_metrics`: decide flatness first (tail range at most 1% of the tail mean, as now). If flat, `y_ss = tail mean`; `band = 0.02 × |y_ss|` (floor at `1e-9`); `t_settle_s` = time of the last sample with `|y − y_ss| > band`; `overshoot_pct = max(0, (peak − y_ss) / |y_ss|) × 100`; `steady_state_error_pct = (setpoint − y_ss) / setpoint × 100`. Return all of them for **both** `settled` and `settled_off_target`. Keep `on_target = |e_ss| ≤ 2%` as a separate flag. Not flat: `not_settled`, as now, with no band.
- Chart: always draw the setpoint as the dashed line with a right-end label "Setpoint 1.00". If `|e_ss| > 2%`, also draw a dotted final-value line labelled "Final 0.909" and a thin bracket between the two lines labelled "e_ss 9.1%". The ±2% band is centred on the **final** value, edge lines 1px, fill 14% cobalt, minimum drawn height 4px, label "±2% of final". The settle marker is a dotted vertical at `t_settle_s` with "0.36 s". For `not_settled` draw no band and no marker, only the setpoint line and the "Not settled within N s" pill.
- Header text: settled on target "Settled at 0.43 s · Overshoot 1.6%"; off target "Settled at 0.36 s · Final 0.909 · 9.1% below setpoint". This also replaces "Settles at 0.00100, 99.9% below the setpoint" (no unit, and "Settles at" reads like a time), which is fix 6 from round 7.
- Also draw the overshoot peak: a 4px cobalt dot at the peak with "1.6%".

`round8/studio-fix/studio-r8.spec.ts` encodes this: recomputes the settling time from the series and compares it with `t_settle_s`, requires non-null time and about 0 overshoot for K = 10, requires a `.studio-step-final` line and a `.studio-step-sse` label, and requires the band centre to match the final line to within 1.5px. On `25c1070` those fail, which is the intent.

### 3.2 Captions are cut off when the inspector is open (new, caused by round 8)

Five captures are affected (the two `studio-block-selected-{light,dark}.png` are taken before Simulate and show no captions): `studio-block-selected-after-simulate-light.png`, `studio-step-unsettled-light.png`, `studio-step-unsettled-dark.png`, `studio-step-extended-light.png`, `studio-step-extended-dark.png`. Under "Gain margin" and "Phase crossover" the caption ends mid-sentence: "Phase never reaches −180° from 0.001 to…" and "Phase stays above −180° from 0.001 to 100,000…". The caption box is 142px wide, the new 12px text no longer fits in the two-line clamp, and `-webkit-line-clamp: 2` cuts the sentence that gives the *reason* for the Infinite margin. `scrollHeight > clientHeight` is true on both captions in both themes. The existing `margins never collide or clip` test checks horizontal overflow only, so it passes.
**Fix:** raise the clamp to 3 lines and give the caption `min-height: 48px`, or better, shorten the copy so it fits two lines in 142px: "No −180° crossing in 0.001 to 100,000 rad/s." and "Gain stays below 0 dB over 0.001 to 100,000 rad/s." The `title` already holds the long form. Add the truncation test in `studio-r8.spec.ts`.

### 3.3 Dark capture state leaks (new)
`cmdk-open-dark.png` and `sidebar-collapsed-dark.png` are now taken on the stale Problem page with the Parameters drawer open and the "Run again" focus ring present. Their light twins are on the Problems list (cmdk) and the Checked Problem. The dark set inherits state from the new `focus-button-dark` capture. Reset the route, drawer and focus before each capture (a fresh page per capture, or `goto` plus `blur()`).

### 3.4 Recent still lists scenario sessions
"Control Studio", "PID DC motor", "Low gain" and "Finite crossover" show in the Recent list of Studio and Gallery captures. Use fresh runs directories per capture, or name sessions as a student would.

---

## 4. Status of round 7's 12 fixes

| # | Fix | Status | Evidence |
|---|---|---|---|
| 1 | Margin captions | **Done, with a regression** | 4.97:1 and 12px, but truncated with the inspector open (3.2) |
| 2 | Focus captures and self-score table | **Done** | G9 |
| 3 | Work step expander | **Done** | Section 2. Static label; step 2 not open by default |
| 4 | Thumbnail well, both themes | **Done** | G8 |
| 5 | Merge and specs | **Done, merge not** | Specs strengthened, `retries: 0`, critiques 3 to 7 and playbook on the branch |
| 6 | Settle wording | **Not done** | "Settles at 0.00100, 99.9% below the setpoint" unchanged (`studio-margins-no-crossover-*`) |
| 7 | Plot annotations | **Partial** | Band and settle marker drawn; band reference wrong (3.1); no overshoot dot |
| 8 | Before-Simulate drawer skeleton | **Not done** | 240px empty box in `studio-layout-before-simulate-*` |
| 9 | Palette scroll affordance | **Not done** | Half-clipped row under "Integrator" |
| 10 | Problems list finish | **Not done** | `problems-list-light.png` byte-identical to round 7: resting rule stops at about 920px, native selects |
| 11 | Gallery and Library finish | **Not done** | `library-light.png` byte-identical; Gallery ids and white PNGs on dark remain |
| 12 | Capture hygiene | **Partial** | md5 baseline fixed; Recent still lists scenarios; preflight skips Finite crossover; dark state leak (3.3) |

---

## 5. Scores

| # | Criterion | R6 | R7 | **R8** | One-line reason |
|---|---|---|---|---|---|
| 1 | Answer-first hierarchy | 4 | 4 | **4** | Unchanged and still strong |
| 2 | Layout, spacing, alignment | 4 | 4 | **4** | Captions cut off with the inspector open offsets the gain from the settle marker. Empty drawer, palette clip, Problems rule and Library still pending |
| 3 | Typography | 3 | 3 | **4** | Captions now 12px at 4.97:1, chart ticks and titles fine. Tags still 11px caps, unit-less pill |
| 4 | Colour and accent discipline | 3 | 4 | **4** | Contrast table is clean. Light amber pill in dark still loud |
| 5 | Surfaces, borders, elevation | 4 | 4 | **4** | Thumbnail well now in both themes, flat hairlines. Native selects and file input remain |
| 6 | States and interaction | 4 | 4 | **4** | Real, visible focus rings in both themes, styled expander. No skeleton, duplicate stale messages, static expander label |
| 7 | Plots | 3 | 4 | **4** | Band, settle marker and setpoint line exist, but the band reference is wrong for off-target loops and there is no peak dot. Gallery still raw PNGs |
| 8 | Schematics and block diagrams | 3 | 4 | **4** | Stable and strict-tested. Loose unused port ring under the plant |
| 9 | Trust and copy | 3 | 4 | **4** | Margins and statuses are right; a missing settling time for K = 10 and the band and pill mismatch keep it from 5 |
| 10 | Shell, navigation, consistency | 4 | 4 | **4** | Focus system now correct. Dark capture state leaks |
| | **Total** | 35 | 39 | **40 / 50** | Clears 38 |

If the band and clipped captions are judged to lower Plots and Layout to 3, the total is 38, still at the gate. The verdict does not rest on the number.

---

## 6. Ready to show Vinayak?

**No. Round 9 should be the one to show him, and it is a quarter-round: three gating items, all small.**

| Gate | Round 8 | Pass? |
|---|---|---|
| Total at or above about 38 | 40 | Yes |
| No criterion below 3 | Lowest is 4 | Yes |
| No visible correctness errors (wrong captions, clipped values, duplicates) | Captions clipped in five captures; band and metric disagree on off-target loops | **No** |
| All nine G items | 9 of 9 | Yes |

**Gating items for round 9** (all must pass; none deferred):

| # | Item | Proof |
|---|---|---|
| R9-A | Captions never truncated, inspector open or closed | The five captures above, plus `studio-r8` truncation tests (light and dark) |
| R9-B | Settling time, overshoot, band and marker reference the final value; setpoint and final value drawn separately; e_ss labelled | `studio-margins-finite-light.png`, `studio-step-offtarget-light.png`, `studio-step-settled-light.png`, plus the `studio-r8` metric and chart tests |
| R9-C | Dark captures start from a clean state | `cmdk-open-dark.png` on the Problems list, `sidebar-collapsed-dark.png` on the Checked problem |

**Estimate:** one quarter-round, hours not days. If these pass, the projected score is **41 to 42**. Fixes 6, 8 to 11 from round 7 are polish and do not gate.

If Vinayak must see something today: Studio with the inspector closed, Home, the Problem page and Cmd+K are showable. Do not open the inspector on the PID loop, do not show the Finite crossover chart, and do not show Library or Gallery in dark.

---

## 7. Ranked fix list (paste into the round 9 prompt)

1. **Settling on the final value** (R9-B; `simulate.py:_step_metrics`, `StepChart.jsx`, `ResultsDock.jsx`). Exact spec in 3.1. Add unit tests in `test_step_metrics.py`: K = 10 gives `t_settle_s` 0.356 ± 0.01 (ln 50 / 11) and overshoot 0; K = 39 and K = 60 both settled; an under-damped loop has overshoot relative to y_ss; a still-rising loop stays `not_settled`. Keep `studio-r8.spec.ts`.
2. **Captions** (R9-A; `studio.css`, `margins.py`). Shorter copy that fits two lines at 142px, or 3-line clamp with `min-height: 48px`. Test with the inspector open in both themes.
3. **Dark capture hygiene** (R9-C; `capture_ux_review_round.py`). A fresh page and route per capture, close drawers, `document.activeElement.blur()`. Fresh `runs/` per theme with student-style session titles. Preflight also probes Finite crossover (expects `status: settled_off_target`, `t_settle_s` not null).
4. **Settle wording** (round 7 fix 6). "Settled at 0.36 s · Final 0.909 · 9.1% below setpoint"; units when the plant has them ("0.909 rad/s"); "Final 0.00100, 99.9% below setpoint" for Low gain.
5. **Overshoot peak dot and label** (`StepChart.jsx`). 4px cobalt dot at the peak, "1.6%" in 12px `--text-secondary`.
6. **Expander** (`StepTimeline.jsx`). Visible label flips to "Hide working" when open; step 2 open by default on a Checked problem so the equation is on the page.
7. **Before-Simulate drawer.** Four-bar margins skeleton and an empty axis frame in the reserved 240px.
8. **Palette.** 16px bottom fade and a visible scrollbar thumb; no half-clipped row.
9. **Problems list.** Rule to full width at rest, 32px styled selects, tags 12px sentence case, 12px above "Details".
10. **Gallery and Library.** Hide ids, 16:10 `--surface-subtle` mats, GIF toggle on one SMIB card. Library form into a dialog, "Add a source" on one line, styled selects and file drop zone.
11. **Parameters drawer.** Drop the duplicate stale message in the drawer (the banner already says it); keep one "Run again".
12. **Process.** Merge #58. Keep `studio-r8.spec.ts` in `testMatch`. Put this critique in `design-critiques/round-8-CRITIQUE.md`.

---

## 8. Round 9 checklist

Every capture: theme in the filename, fresh page and route per capture, `data-theme` reset, 1280 x 800 unless stated, unedited `preflight.json` with the dirty flag, md5 diff against round 8, `focus-log.json` for any focus capture.

- **Studio, with the inspector closed and open:** `studio-block-selected-{light,dark}.png`, `studio-block-selected-after-simulate-{light,dark}.png`: captions complete, no ellipsis.
- **Settling:** `studio-step-settled-{light,dark}.png` (PID, final equals setpoint, band at 1.0, marker 0.43 s, overshoot dot); `studio-step-offtarget-{light,dark}.png` and `studio-margins-finite-{light,dark}.png` (Finite crossover: setpoint line, dotted final line at 0.909, e_ss 9.1% label, band around the final line, marker near 0.36 s); `studio-step-unsettled-{light,dark}.png` (no band, no marker); `studio-step-extended-{light,dark}.png`.
- **Dark set clean:** `cmdk-open-dark.png` on the Problems list, `sidebar-collapsed-dark.png` on the Checked problem.
- **Problem:** `problem-work-{light,dark}.png` with step 2 open.
- **Logs to attach:** Playwright output for all six spec files at `retries: 0`, the `test_step_metrics.py` output, `preflight.json` (with Finite crossover), the md5 diff, a contrast table.

Files reviewed: all 75 PNGs in `round8/` (secondary Settings, Home and Problems states read through their twins, byte-identical ones checked by md5), `NOTES.md`, `focus-log.json`, `md5.txt`, `preflight.json`, `sidebar-measurements.json` (240px and 56px unchanged). Source read from a `git archive` of `25c1070` and `origin/pr58`, plus `origin/main` at `7b2a9aa`. Nothing was pushed, merged or commented on.
