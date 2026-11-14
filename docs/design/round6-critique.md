# Round 6 critique (Design lead, 13 Nov 2026)

Build: captured from the working tree on top of `2ba9b3e`, committed as `5095779` on `cursor/arc-ui-polish-ad61`, now merged to `main` (merge `8d181a8`). I opened all 60 PNGs in `round6/` (the folder holds 65 files, not 58: 60 PNGs plus `NOTES.md`, `MY_NOTES.md`, `md5.txt`, `preflight.json` and `sidebar-measurements.json`). I compared every md5 with round 5, sampled native pixels (PNGs are 1280 wide, so coordinates are native unless I say "scaled"), and read `origin/main` read-only with `git show` in my own clone. I did not edit, commit or push anything in their repo.

**Total: 35 / 50 (round 1: 25, round 2: 30, round 3: 32, round 4: 33, round 5: 32, so +3).** The biggest jump since round 2. The stale-backend problem is gone, the margins strip, docked inspector, three-state settling, token thumbnails and Cmd+K all landed and are visible. What is left is narrower and mostly mechanical, but three items are visible correctness failures (wires missing at 1440, no dark arrowheads, a plot with no tick numbers).

**Ready to show Vinayak: NO today. Round 7 should be the one to show him, if the nine gate items in section 9 all pass in the captures.** Estimated 2 rounds worst case.

---

## 1. Preflight, verified

EE Project says it passes. I checked each field against the captures and the source.

| Field | Value | Check | Verdict |
|---|---|---|---|
| `package_path` | `/agent/repos/ARC/src/electrical_engineer/__init__.py` | Under `src/`, so an editable install, which was the round 5 root cause | Pass |
| `kp` | 50.0 | PID block reads `Kp 50 · Ki 100 · Kd 5` in every Studio capture | Pass |
| `step_series` | true | The SVG chart renders (round 5 showed the PNG fallback) | Pass |
| `gain_margin_caption` | "Phase never reaches −180° ..." | Same text on screen in `studio-layout-after-simulate-light.png` | Pass |
| `dist_index_mtime` | 1794576121 = 18:52 IST | Two minutes before the commit (18:53:55 IST), so `dist` was rebuilt for this tree | Pass |
| `git_sha` | `5095779` | **Hand-edited.** The script wrote `2ba9b3e` (HEAD at capture, because the work was uncommitted); commit `a5b0944` "align round-6 preflight git sha" rewrote it afterwards | Label only, not proof |

So the backend and UI are now consistent with the source, and the captures can be trusted for what they show. Two weaknesses to fix in round 7: (1) the sha is not evidence, so record `git rev-parse HEAD` **plus** `git status --porcelain | wc -l` and a hash of `git diff HEAD`, or capture after committing; (2) the preflight probes one throw-away PID session, not the sessions that are photographed, so it could not see the Low gain Phase margin bug below. The capture script on `main` now kills port 8765, always runs `npm run build`, clears `runs/` per theme and raises on a bad preflight. All good.

---

## 2. Byte-identical check against round 5 (md5)

| Result | Count | Files |
|---|---|---|
| Identical to round 5 | **4** | `problem-work-tab-light`, `problems-empty-light`, `problems-error-light`, `sidebar-collapsed-light` |
| Same name, changed | 50 | everything else from round 5 |
| New in round 6 | 6 | `problems-empty-dark`, `problems-error-dark`, `studio-after-resize-light`, `studio-block-selected-after-simulate-light`, `studio-step-extended-light`, `studio-step-offtarget-light` |
| Dropped from round 5 | 0 | |

`NOTES.md` declares the same four with a reason ("empty/error/sidebar unchanged pixels"), which is acceptable. `problem-work-tab-light` is not named in the reason but nothing in it changed (the boxed chevron under step 2 is still there). All 60 files match `md5.txt`, and no two images in the folder are identical. `NOTES.md` has no per-item self-score this round, so I could not compare against the builder's own tally. Please add one.

**Measurements**
- Sidebar: expanded **240**, collapsed **56**, Cmd+K open **240**. **Pass.** Studio widths at 1280 and 1440 were still not recorded.
- Input borders `#8C8C87`, 3.38:1. **Pass.**
- Dark, measured: schematic labels `#F4F4F3` on `#1A1A18`, **15.8:1** (was 1.2:1, fixed). Parameters values now white (was 1.2:1, fixed). Home thumbnails `#939AA9` on `#1A1A18`, 6.2:1. **Step window buttons "10 s 30 s 100 s Auto": `#353532` on `#121211`, 1.52:1, fail.** Light-mode margin captions "Phase never reaches ..." are `#8A8A86` on white, **3.47:1, fail** (the playbook token is `--text-muted` `#70706C`).
- No panels overlap at 1280, 1440 or 1280 x 680 (`studio-after-resize-light.png`).

---

## 3. EE Project's notes, verified

| Point | Verdict | Evidence |
|---|---|---|
| Step plot has no tick labels, plot area small inside the card, settling and overshoot metrics not visible | **Agree** | `StepChart.jsx` has no tick code at all (no `tick` anywhere in the file). The SVG has a fixed 640 x 220 viewBox drawn into a container about 740 x 120px, so it letterboxes to about 400 x 90px of plot. Settling is shown only as a pill when off target; no "Settled at" or "Overshoot" label for the good case |
| Dark: step window buttons nearly invisible | **Agree** | 1.52:1. `.studio-window-segment button` sets no `color`, so the native button text colour shows on a dark surface |
| Dark: forward wires lost arrowheads | **Agree, and I found the exact cause** | Section 6.2 |
| Dark: inspector missing, palette shown instead | **Partly agree** | `studio-after-simulate-dark.png` and `...before...` show the palette because nothing is selected, which is correct. The gap is that there is **no dark selected capture**, so the dark inspector is unverified |
| Breadcrumb "PID DC motor" in light, "Control Studio" in dark | **Agree** | The dark capture session is created without a title (`{"golden": "pid_dc_motor"}`), and the same happens for the Finite crossover capture (`studio-step-offtarget-light.png` says "Control Studio"). A capture-script issue, but the UI also shows the golden's generic name; fine to leave once the script passes a title |
| Inspector "Pin comment" is monospace and clipped | **Agree** | `.studio-comments textarea` has `height: 36px` and no `font: inherit`, while `rows={2}`. After Simulate it is also cut by the results drawer (below) |
| Home thumbnails token-drawn but First-order step reads as a wedge | **Agree, and four of six read badly** | Section 6.6 |
| Third row cut by the fold | **Disagree, minor** | The grid is three rows of two; the third is below the fold at 800px by design and `home-scrolled-*` shows it whole |

I found three more that the notes do not mention:
1. **`studio-layout-before-simulate-1440-light.png` and `studio-layout-after-simulate-1440-light.png` have no wires at all.** No signal wires, no arrowheads, no `r`, `e`, `u`, `y` labels, no feedback path. Only the blocks and ports. This is a regression (round 5 had wires at 1440).
2. **Low gain, Phase margin reads "Infinite" next to Gain crossover "No crossover in range"** (`studio-margins-no-crossover-light.png`). A phase margin is measured at the gain crossover, so with none it must read "Not defined". Round 4 fix 5 asked for this and `_fmt_pm` was changed, but it is only reached when `w_gain_cross is None`, and `control.margin` returns NaN, not None, so the branch is skipped. I confirmed the same "Infinite" by running the code in round 5.
3. **The PID to DC motor gap is still 8px** (PID right edge 585 scaled, motor left edge 592). Round 5 claimed the golden had a 72px gap. I was wrong: `layout_chain()` re-places every block and uses `PID_W = 144` while the CSS draws the PID at 168px, so the 32px `GAP` becomes 8px. Root cause below.

---

## 4. Status of round 5's 12 fixes (verified in the captures)

| # | Round 5 fix | Status | Evidence |
|---|---|---|---|
| 1 | Captures prove the build | **Done** | Preflight, editable path, forced build, port kill, runs cleared. Sha is hand-edited (section 1) |
| 2 | Margins strip | **Done** | One full-width row of four cells, 24px value with a 12px unit beside it ("8.735 rad/s"), captions clamped to two lines, nothing collides. Residual: caption colour 3.47:1, the "°" unit is tiny and detached |
| 3 | Fix "not settled" | **Done** (code and captures), one gap | `studio-step-offtarget-light.png`: "Settles at 0.91, 9% below the setpoint". Gap: the amber "Not settled within 10 s" state and the "Auto" window are never captured, and Low gain says "Settles at 0.00, 100% below the setpoint" (precision: it is 0.001, 99.9%) |
| 4 | Dock the inspector | **Done at 1280, two defects** | Docked 264px right column, palette collapses to a 48px rail, loop at 101% and untouched. Defects: after Simulate the inspector is cut by the results drawer ("Pin comment" half visible, "Pin" button gone), and the rail icons have no labels (tooltip not shown) and are clipped after Simulate with no scroll cue |
| 5 | Engine capture defects | **Partial** | Done: distinct icons for most blocks (Saturation and DC motor still share the gauge, Transfer Fcn is a funnel). Not done: "1st-order plant" still overflows its block with a port dot over the second line (`studio-margins-*`, `studio-step-offtarget`), PID to motor gap still 8px, "1st-order plant" still named differently from "First-order plant" in the title |
| 6 | Dark correctness | **Partial** | Done: schematic labels 15.8:1, Parameters values, Home thumbnails themed. Not done: **arrowheads in dark**, Gallery figures still white mats, native white Copy button in Settings > Agents (dark). New: window buttons 1.52:1 |
| 7 | Home example cards | **Partial** | Six distinct token SVGs, no embedded titles, Continue cards differ, Agent line reworded. But the drawings do not read (6.6), "Press Ctrl Enter to solve" is still plain text, and the Agent line still ends with a clipped "CLI" |
| 8 | Disambiguate duplicates | **Done** | One Recent entry, Library merged to one row ("Used in 2, 6"), Continue cards differ, `test_run_list_dedupe.py` added. UI-level disambiguation ("Today 17:12") is not visible because the data was cleaned, so the rule is untested in the pictures |
| 9 | Cmd+K polish | **Done, one residual** | Left-aligned rows, 16px icons, `G` `H` as two chips, Actions group, no fade. Residual: the query input keeps a 2px near-black ring inside the bordered palette (`cmdk-query-light.png`) |
| 10 | Problems table and filters | **Not done** | Row rules still end 106px short of the header (`problems-list-light.png`), Subject and Made by are still native selects, tags unchanged. Only the hovered row shows a full-width rule |
| 11 | Gallery and Library finish | **Not done** | Gallery still prints `power.swing_equal_area` ids, uneven card heights, white mats in dark. Library still has the inline "Add a book" form, native file input and selects, "Add a source" wraps |
| 12 | Capture discipline v3 | **Partial** | New: `studio-block-selected-after-simulate`, `studio-after-resize`, `studio-step-offtarget`, `studio-step-extended`, `problems-empty/error-dark`. Still wrong: `focus-tab-light` is the skip link, `focus-table-row-light` is the Activity tab on a Problem page, `focus-button-light` is the Diagram tab. No dark focus captures, no dark selected capture, `studio-step-extended-light.png` is the same picture as the 10 s one with "Auto" shaded, so it proves nothing |

Tally: **done 1, 2, 3, 4 (with defects), 8, 9; partial 5, 6, 7, 12; not done 10, 11.** That is 6 done, 4 partial, 2 not done, against 3 done, 5 partial, 4 not done last round.

---

## 5. Scores

| # | Criterion | R1 | R2 | R3 | R4 | R5 | R6 | One-line reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Answer-first hierarchy | 3 | 4 | 4 | 4 | 4 | 4 | Answer card, Checked strip and amber stale strip all coherent in both themes. Unchanged, still the best part of the app |
| 2 | Layout, spacing, alignment | 2 | 3 | 3 | 4 | 3 | **4** | Margins strip and docked inspector fixed the Studio drawer. Chart is squeezed to about 90px, inspector clipped after Simulate, Problems rules short, Library a pinned column |
| 3 | Typography | 3 | 3 | 3 | 3 | 3 | 3 | Chart has no tick numbers and 10px axis titles, captions at 3.47:1, tags still 11px uppercase |
| 4 | Colour and accent discipline | 3 | 3 | 3 | 3 | 3 | 3 | Dark inputs and schematic labels fixed. Dark window buttons 1.52:1, no dark arrowheads, light captions 3.47:1 |
| 5 | Surfaces, borders, elevation | 3 | 3 | 3 | 4 | 4 | 4 | Flat hairline panels, no stray shadows. Native selects and file input remain |
| 6 | States and interaction | 3 | 4 | 4 | 3 | 4 | **4** | Selection docks and persists, three-state settling shows, stale and dark empty and error states exist. Focus captures still show the wrong elements, no dark selected state |
| 7 | Plots | 2 | 2 | 2 | 2 | 2 | **3** | Themed SVG with axis titles, units, setpoint and window control, but no ticks and a tiny plot area. Gallery still raw PNGs, Home thumbnails weak |
| 8 | Schematics and block diagrams | 2 | 3 | 3 | 3 | 3 | 3 | 1280 loop is clean, selected block is clear. But **no wires at all at 1440**, no dark arrowheads, 8px PID to motor gap, label overflow. Would be 2 if the 1440 result is not a capture race |
| 9 | Trust and copy | 2 | 3 | 3 | 3 | 2 | **3** | Captions now correct and the off-target pill is honest. Low gain "Phase margin Infinite" beside "No gain crossover" contradicts itself, "Settles at 0.00" loses precision |
| 10 | Shell, navigation, consistency | 3 | 4 | 4 | 4 | 4 | 4 | 240 and 56 exact, Cmd+K fixed, theme labels right, duplicates gone. Breadcrumb says "Control Studio" in dark for the PID loop |
| | **Total** | **25** | **30** | **32** | **33** | **32** | **35 / 50** | Below 38 |

**What the gates need:** 38 means +3, which is Plots 3 to 4 (ticks, bigger chart, Home thumbnails that read), Schematics 3 to 4 (wires at 1440, arrowheads, gap), and one of Typography or Colour 3 to 4 (tick text, the two contrast fixes). All are in the list below.

---

## 6. Findings that need exact detail

### 6.1 Wires missing at 1440 (`studio-layout-before-simulate-1440-light.png`, `...after...`)
Not a timing race: the after-Simulate capture is taken seconds later and still has no wires. The 1280 captures from the same script have them. The difference in the script is that 1440 uses a **fresh `browser.new_page()` viewport 1440 x 900** instead of the long-lived page. I could not run the UI, so this is unproven, but the existing `studio-wire-selection.spec.ts` cannot catch it either: it loops over `.react-flow__edge-path` and skips any element whose `boundingBox()` is null, so with zero edges it passes vacuously (verified in the source). Required: reproduce in Playwright at 1440 x 900 on a freshly loaded page with `page.on('console')` and `pageerror` logging, find the cause, and add the assertion in 6.4.

### 6.2 Dark arrowheads: exact cause
`ControlStudio.jsx` line 27, `useWireStroke()`, reads `getComputedStyle(document.documentElement).getPropertyValue("--cs-wire")`. But `--cs-wire` is defined on **`.cs-app`** (`tokens.css` line 10, `#1a1a18`) and on `[data-theme="dark"] .cs-app.control-studio` (`studio.css` line 13, `#e8e8e6`), never on `:root`. So the read returns `""` and the hook falls back to `"#1A1A18"` in both themes. The wires themselves use `var(--cs-wire)` in CSS and turn white in dark; the arrowheads get a hard-coded near-black and vanish on `#1A1A18`. Fix, either one:
- Pass `color: "currentColor"` in `markerEnd`, and set `.studio-canvas { color: var(--cs-wire); }` so the marker inherits the themed colour with no JS; delete `useWireStroke`. Or
- Read from the app element: `getComputedStyle(document.querySelector(".cs-app.control-studio"))`.

Take the first. Also fix the vacuous test: React Flow arrowheads are `polyline` elements, but the dark spec selects `marker polygon, marker path`, so it matches nothing and passes while the arrowheads are invisible. Selector must be `.studio-canvas marker polyline, .studio-canvas marker polygon, .studio-canvas marker path`, and the test must first assert the count is at least 4.

### 6.3 PID to DC motor gap and label overflow
`layout.py` has `PID_W = 144` and `GAP = 32`, while `studio.css` line 847 draws `.studio-pid.studio-block` at **168px**, so the visual gap is 32 − 24 = 8px and the `u` label has no wire. Fix: `PID_W = 168`, `GAP = 48`, and a unit test that parses the `width:` of `.studio-pid.studio-block`, `.studio-sum.studio-block` and `.studio-block` from `studio.css` and asserts they equal `PID_W`, `SUM_W`, `BLOCK_W`, so the two can never drift again. "1st-order plant" needs one name ("First-order plant"), at most two lines of 13px/16px, and the block `min-height: 64px` with `overflow: hidden` only on the label, not the port.

### 6.4 Step chart spec
The SVG is the right choice and the pill is honest. What is missing:
- **Responsive, not letterboxed.** Measure the container with a `ResizeObserver` and draw at its real width and height (no fixed viewBox, no `height={220}`). Minimum 560 x 160px at 1280.
- **Ticks, numbers on both axes.** 11px, `font-variant-numeric: tabular-nums`, `--text-secondary`. Use a "nice ticks" helper (target 5 x ticks, 4 y ticks), x labels `0, 2, 4 ... 10`, y labels `0, 0.5, 1.0` (or the unit scale, e.g. `0 ... 12 rad/s`). Gridlines `--border`.
```js
function niceTicks(min, max, n = 5) {
  const step0 = (max - min) / (n - 1), mag = 10 ** Math.floor(Math.log10(step0)), norm = step0 / mag;
  const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag, out = [];
  for (let v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) out.push(+v.toFixed(10));
  return out;
}
```
- **Auto window actually automatic.** Default to Auto: window = `clamp(8 × t_settle, 2, 600)` seconds, where `t_settle` is the last time the response leaves the 2% band (fall back to `6/ωcg`). With the PID golden the response settles in about 0.5 s, so a 10 s window shows a vertical line followed by a flat one; Auto would give about 4 s and show the shape. The x axis label states the window ("Time (s), 4 s window").
- **Annotations when they exist:** a 2% band (light cobalt tint), "Settled at 0.4 s" with a tick, "Overshoot 1.6%" at the peak with a dot. None when absent.
- **Header on one row.** Today the "Step / Bode / Root locus" tabs sit on their own row above the chart's own header, costing 36px. Put the tabs on the left and the window control and pill on the right of one 32px row.
- **Window buttons in dark:** `.studio-window-segment button { color: var(--cs-text-secondary); font: inherit; }` and `.is-active { color: var(--cs-text); background: var(--cs-surface-subtle); }`. At least 4.5:1.
- **Not-settled state captured:** a loop that really does not settle (for example `pid_dc_motor` with Kp 0.5 and Ki 0.1, or a lightly damped second-order plant) so "Not settled within 10 s" and "Still rising ..." appear once, plus the extended window.

### 6.5 Margin cell fixes
- Caption colour `--text-muted` `#70706C` (not `#8A8A86`), 12px.
- Unit "°" and "dB" sit on the baseline at 12px with the same colour as `rad/s`.
- `_fmt_pm`: treat NaN and `None` gain crossover the same: `if w_gain_cross is None or not math.isfinite(w_gain_cross): return "Not defined", "No gain crossover in range."`. Add to `test_margin_captions.py`: `open_loop_low_gain` gives `pm_deg == "Not defined"`.
- Settle text uses significant figures: "Settles at 0.001, 99.9% below the setpoint" (format `.3g`, percent `.1f`, and never "0.00").

### 6.6 Home thumbnails
Six distinct token SVGs landed, which is real progress, but at thumbnail scale four do not read:
| Tile | Shows now | Should show |
|---|---|---|
| Voltage divider | A horizontal line with a dot between two end ticks | Vin on the left, two zigzag resistors in series, a ground, the Vout tap as a cobalt dot |
| First-order step | A filled wedge | A line curve `1 − e^(−t)` with axis lines and a dashed final value. No fill |
| SMIB swing | A filled blob | A sine arc with the two equal areas lightly tinted, a dashed Pm line |
| DC drive speed | A straight diagonal with a stray "ω" | A rising exponential to a dashed final speed, axes, no glyph |
| Digital loop | Unit circle with two dots | Acceptable. Add the real axis and `x` marks instead of dots |
| Signals workout | Histogram bars | Acceptable. Make them stems on a baseline for a spectrum look |
Stroke 1.5px `--accent-500`, axes 1px `--border-strong`, canvas 16:10, no fills except the 12% cobalt tint in SMIB. Dark uses the same tokens, and the grey well should appear in both themes or neither (light has one, dark does not).

### 6.7 Inspector after Simulate
The grid row for the inspector is the canvas row only, so the 264px panel is cut by the results drawer. Make the right column span both rows (`grid-template-areas: "bar bar bar" "palette canvas inspector" "palette results inspector"`, drawer under canvas only), or make the inspector `max-height: calc(100% - 0)` with `overflow: auto` and a visible scrollbar gutter. Prefer the first: it keeps Kp, Ki, Kd, "Pin comment" and "Pin" always visible. `textarea { font: inherit; height: auto; min-height: 56px }`. Ports on a selected block 12px filled cobalt.

---

## 7. Per-screen issues

### Studio (`studio-layout-before-simulate-light.png`, `studio-layout-after-simulate-light.png`, `studio-block-selected-light.png`, `studio-block-selected-after-simulate-light.png`, `studio-step-offtarget-light.png`, `studio-step-extended-light.png`, `studio-after-resize-light.png`, `studio-margins-finite-light.png`, `studio-margins-no-crossover-light.png`, both dark captures, the two 1440 captures)
- **Canvas, between PID and DC motor:** 8px gap, `u` label on the PID corner, no wire (6.3).
- **Canvas, 1440 pair:** no wires, arrowheads or signal labels (6.1).
- **Canvas, dark pair:** no arrowheads on `r`, `e`, `y` or the feedback entry into the sum (6.2). Everything else is legible, sum ring is faint.
- **Canvas, plant block (finite and low gain captures):** "1st-order plant" cut off with a port dot over the text.
- **Palette rail (selected captures):** ten icons with no tooltip shown and no scroll cue after Simulate (cut at the gauge). Before Simulate the full 16-row palette is clean and the icons are distinct apart from Saturation and DC motor.
- **Inspector, right column, after Simulate:** cut by the drawer, "Pin comment" monospace and half hidden, "Pin" missing (6.7).
- **Results strip:** the best-looking part of the app now. Values 24px, units beside, captions two lines. Caption contrast 3.47:1.
- **Chart:** tiny, no ticks, two header rows (6.4). In `studio-step-extended-light.png` the Auto window looks identical to 10 s because the response settles in half a second.
- **Low gain capture:** "Phase margin Infinite" next to "Gain crossover No crossover in range", no caption under Phase margin (6.5). Step pill "Settles at 0.00, 100% below the setpoint".
- **Toolbar:** one filled button, zoom 101% when the inspector is open and 119% when it is not, which is correct. Breadcrumb "Control Studio" in the dark and Finite crossover captures.

### Home (`home-empty-light.png`, `home-with-recent-light.png`, `home-scrolled-1280-light.png`, `home-scrolled-1440-light.png`, `home-dark.png`, `home-scrolled-dark.png`)
- **Example cards:** thumbnails per 6.6. Dark has no frame, light has a grey well.
- **Continue:** distinct cards ("Control Studio", "Voltage divider · Vout") with "just now" and a Checked tag. Good.
- **Composer hint:** "Press Ctrl Enter to solve". Render `Ctrl` `↵` as two `kbd` chips.
- **Agent section:** "Connect your coding agent." then "electrical-engineer mcp — then connect Cursor or Claude Code. CLI" with the trailing "CLI" clipped by a following line. Remove "CLI", and put the one command in the `kbd` block.

### Problem (`problem-answer-light/dark.png`, `problem-work-tab-light.png`, `problem-work-dark.png`, `problem-parameters-drawer-light.png`, `problem-parameters-stale-light.png`, `problem-stale-dark.png`, `problem-dark.png`)
- **Answer card:** still the strongest screen. Dark Parameters values and schematic labels now readable.
- **Stale (right column, first card):** the banner repeats the strip's message and "Run again" still wraps to two lines at 76px wide. Make the banner action a text link on one line, or drop the banner.
- **Work tab, step 2:** boxed chevron still 36px below the text. Put it at the row end.

### Problems, Cmd+K, rail (`problems-*-light/dark.png`, `cmdk-*`, `sidebar-collapsed-*`)
- **Table:** rules end 106px short of the header band in every non-hover capture; selects native; tags 11px uppercase. Tooltips on the three hover icons are still not shown.
- **Cmd+K:** fixed except the 2px dark ring on the query input.
- **Dark empty and error:** consistent with light, "Try again" and "Details" 4px apart, give 12px.

### Gallery, Library, Settings (`gallery-light/dark.png`, `library-light/dark.png`, `settings-*`)
- **Gallery:** `power.swing_equal_area` ids, uneven card heights, white mats in dark, the SMIB figure twice.
- **Library:** one source row now. Inline "Add a book" form, native controls, "Add a source" two lines.
- **Settings:** About, Engines, Appearance good in both themes. "SPICE when installed | conditional | ok" still reads oddly. The Agents Copy button is a native white button in dark.

### Focus (`focus-*-light.png`)
- Composer and tile correct (tile on "Digital loop" with a cobalt ring). Tab, table-row and button captures focus the wrong elements, and the ring on them is black not cobalt.

---

## 8. Carry-over: what is and is not on `main`

All Arc PRs are merged, so the builder's code is on `main`. I read `origin/main` (read-only) to see what my earlier material became.

| Item | On `main`? | Notes |
|---|---|---|
| `studio-layout.spec.ts` (round 3) | **Yes**, `ui/e2e/studio-layout.spec.ts` | Builder's version of my spec: no-overlap before and after Simulate at two viewports, 11px block text and the 0.85 fit floor. The round 3 CSS patch is also in `studio.css` (`isolation: isolate`, `contain: layout paint` at lines 418 to 419, `--studio-results-h: clamp(300px, 42vh, 400px)`). Nothing to carry |
| `studio-wire-selection.spec.ts` (round 4) | **Yes**, `ui/e2e/studio-wire-selection.spec.ts` | **Weak**: it iterates over drawn edges and skips any with a null bounding box, so a diagram with zero wires passes. The 1440 captures prove it. Needs the edge-count assertion in the list |
| `studio-r5.spec.ts` (round 5) | **Yes**, `ui/e2e/studio-r5.spec.ts`, wired in `playwright.config.ts` `testMatch` and CI (`npm run test:e2e` in `.github/workflows/ci.yml`) | **Dark arrowhead test is vacuous**: selector `marker polygon, marker path` misses React Flow's `polyline`, so it passes with invisible arrowheads. The margins and inspector tests are sound. The inspector test selects `.studio-inspector:not(.studio-inspector-float)` which is right for the docked panel |
| Preflight in `scripts/capture_ux_review_round.py` | **Yes** | See section 1 for the sha weakness |
| `DESIGN_PLAYBOOK.md` | **No** | Lives only in `/workspace/arc-frontier/design-loop/`. The fresh branch will not contain it. **Copy it into the repo** (`docs/design/DESIGN_PLAYBOOK.md`) and paste the rubric into the round 7 prompt |
| Critiques for rounds 3 to 6 | **No** | Historical note: UX dump rounds lived under `artifacts/ux-review/` (removed; regenerate via `scripts/capture_ux_review_round.py` if needed) |
| `round3/studio-fix/` repro files (`repro.spec.js`, before and after HTML) | **No, not needed** | Debug scaffolding, superseded by the layout spec |
| `round6/studio-fix/studio-r6.spec.ts` (new, this round) | **No** | Saved next to this file. Merge into `studio-wire-selection.spec.ts` and `studio-r5.spec.ts` on the new branch |

New spec assertions (all in `round6/studio-fix/studio-r6.spec.ts`):
1. Edge count equals wire count (`.react-flow__edge` count equals the diagram's `wires.length`, `.react-flow__edge-path` each has non-zero width or height) at 1280 x 800 and 1440 x 900, on a freshly loaded page, before and after Simulate.
2. Every marker shape under `.studio-canvas` has a computed fill with at least 3:1 against the canvas background in light and dark, and there are at least four.
3. Gap between every pair of adjacent forward-path blocks is at least 40px, and no block's text overflows its box (`scrollHeight <= clientHeight` on the label).
4. Step chart: at least 3 x tick labels and 3 y tick labels exist, plot box at least 560 x 160px, and the Step header is one row.
5. Inspector is fully inside the viewport and not clipped by the drawer: `bottom <= drawer.top` is **not** required, but its Kp, Ki, Kd inputs and the "Pin" button must be `isVisible()` and inside the canvas row or the spanning column.
6. Low gain golden: `pm` text is "Not defined".
7. Window buttons contrast at least 4.5:1 in both themes.

---

## 9. Ready to show Vinayak?

**No, not today (35/50). Round 7 should be the one to show him, provided every gate item below passes in the round 7 captures.** Nothing here needs new design thinking; it is mostly mechanical, and the root causes for four of the nine are already identified.

| Gate | Round 6 | Pass? |
|---|---|---|
| Total at or above about 38 | 35 | No |
| No criterion below 3 | Lowest is 3 | Yes (but Schematics would be 2 if the 1440 result is real) |
| No wrong captions | Corrected captions on screen; Low gain "Phase margin Infinite" contradicts its neighbour | No |
| No clipped or colliding values | None in the margins strip | Yes |
| No duplicates | Clean | Yes |
| No broken diagram or invisible element | No wires at 1440, no dark arrowheads, 1.5:1 dark window buttons | No |

**Exact must-fix list that gates round 7** (each is verified by a named capture or a Playwright assertion; all nine must pass, none can be "deferred"):

| # | Gate item | Proof in the round 7 folder |
|---|---|---|
| G1 | Wires, arrowheads and signal labels present at 1280 and 1440, before and after Simulate, light and dark | The four 1440 and four dark captures, plus spec assertion 1 |
| G2 | Dark arrowheads visible (`currentColor`, 6.2) | `studio-*-dark.png`, assertion 2 |
| G3 | Step chart: tick numbers, responsive size, Auto window, one header row, settled and overshoot annotations, dark window buttons at 4.5:1 | `studio-layout-after-simulate-{light,dark}.png`, `studio-step-extended-light.png` showing a different window, assertions 4 and 7 |
| G4 | "Not settled within N s" actually captured once, plus the off-target pill | `studio-step-unsettled-{light,dark}.png` |
| G5 | Low gain Phase margin "Not defined"; settle text keeps precision; caption colour 4.5:1 | `studio-margins-no-crossover-light.png`, assertion 6 |
| G6 | PID to motor gap at least 48px, one block name, no label overflow | Every Studio capture, assertion 3 |
| G7 | Inspector never clipped, Pin comment usable, selected state captured in dark | `studio-block-selected-{light,dark}.png`, `studio-block-selected-after-simulate-light.png`, assertion 5 |
| G8 | Home thumbnails that read as the thing they name (6.6) | `home-empty-light.png`, `home-dark.png` |
| G9 | Focus captures show the right element (Work tab, Problems row, a button), one dark focus capture, `NOTES.md` with a per-item self-score | `focus-*.png` |

**Not gating, but needed to hold the total at or above 38:** Problems table rules and styled selects (fix 8), Gallery ids and card heights (fix 9), Library dialog (fix 9). These lift Surfaces and Shell from 4 and keep them there; if they slip, round 7 still lands at about 37 to 38 and the verdict rests on the G-list.

**Projection:** G1 to G7 move Schematics 3 to 4, Plots 3 to 4, Colour 3 to 4, Typography 3 to 4, Trust 3 to 4. G8 and the polish keep Plots at 4 and Layout at 4. That gives **38 to 40** in round 7.

**If round 7 does not pass:** a round 8 would carry only the failed gate items and is a half-round of work. The risk is G1 (the 1440 cause is not yet known) and G8 (Home thumbnails have been skipped or botched four rounds in a row, so draw them from the table in 6.6). My estimate, from the pattern of the last three rounds, is that round 7 passes about two times in three; I would not promise Vinayak a date before the round 7 captures are in.

---

## 10. Ranked fix list (12, ordered by what moves the "ready" verdict; paste into the round 7 prompt)

1. **Find and fix the missing wires at 1440** (`studio-layout-*-1440-light.png`). Reproduce with Playwright on a fresh `page.goto` at 1440 x 900, log `console` and `pageerror`, fix the cause. Add spec assertion 1 (edge count equals wire count, each edge path has non-zero size) at both viewports, before and after Simulate. Gates G1.
2. **Dark arrowheads** (`studio-*-dark.png`). Delete `useWireStroke`; `markerEnd: { type: MarkerType.ArrowClosed, color: "currentColor" }` and `.studio-canvas { color: var(--cs-wire); }`. Fix the vacuous test selector (`marker polyline`) and assert at least four markers with fill contrast of at least 3:1 in both themes. Gates G2.
3. **Step chart** (`StepChart.jsx`, `ResultsDock.jsx`). Spec 6.4: container-measured SVG at least 560 x 160px, `niceTicks` on both axes at 11px tabular, Auto window default (`clamp(8 × t_settle, 2, 600)`), 2% band, "Settled at" and "Overshoot" labels, tabs and window control on one 32px row, window buttons `color: var(--cs-text-secondary)` (4.5:1 in dark). Gates G3.
4. **Capture the unsettled and extended states** (`capture_ux_review_round.py`). A loop that genuinely does not settle (Kp 0.5, Ki 0.1 on the DC motor, or a lightly damped plant) for `studio-step-unsettled-{light,dark}`, and `studio-step-extended-light` taken after choosing 30 s or Auto, showing a different x axis from the 10 s picture. Gates G4.
5. **Margins semantics and tokens** (`margins.py`, `studio.css`). `_fmt_pm`: non-finite gain crossover gives "Not defined" with "No gain crossover in range." Settle text with `.3g` and `.1f` ("Settles at 0.001, 99.9% below the setpoint"). Caption `color: var(--cs-text-muted)` set to `#70706C`, 12px. Unit "°" and "dB" on the baseline. Test in `test_margin_captions.py`. Gates G5.
6. **Layout constants and block label** (`layout.py`, `studio.css`). `PID_W = 168`, `GAP = 48`, a unit test comparing the CSS widths to the Python constants, "First-order plant" everywhere, label at most two lines at 13px/16px inside a 64px block, port dots outside the text. Gates G6.
7. **Inspector spans both rows** (`studio.css`, `Inspector.jsx`). `grid-template-areas: "bar bar bar" "palette canvas inspector" "palette results inspector"` so Kp, Ki, Kd, "Pin comment" and "Pin" are never cut; `textarea { font: inherit; min-height: 56px; height: auto }`; selected ports 12px filled cobalt; rail icons get `title` tooltips and a scroll fade. Capture the dark selected state. Gates G7.
8. **Home thumbnails that read** (`ExampleThumb.jsx`). Redraw per table 6.6: divider with Vin, two resistors, ground and a Vout dot; `1 − e^(−t)` line with a dashed final value (no fill); SMIB arc with two tinted equal areas; DC speed rising exponential (remove the stray "ω"); unit circle with axes and `x` poles; spectrum stems. 16:10, 1.5px stroke, same frame in both themes. "Press `Ctrl` `↵` to solve" as `kbd` chips; remove the trailing "CLI". Gates G8.
9. **Problems and Cmd+K finish** (`ProblemsPage.jsx`, `CommandPalette.jsx`). Row rules full width to the actions column, hover icons with tooltips, Subject and Made by as 32px styled selects, tags 12px sentence case, 12px between "Try again" and "Details"; Cmd+K query input a bottom border with no ring. Keeps Surfaces and Shell at 4.
10. **Gallery and Library finish** (`gallery.jsx`, `library.jsx`). Drop the `power.swing_equal_area` ids, 16:10 equal-height frames with a `--surface-subtle` mat in dark, one SMIB card with a "GIF" toggle. Library: "Add a source" on one line, the inline form moves into a dialog with a drop zone and styled 36px selects, subtitle 12px under the H1. Keeps Layout at 4.
11. **Focus and dark capture set** (`capture_ux_review_round.py`). `focus-tab` lands on a Work tab, `focus-table-row` on a Problems row, `focus-button` on a button, by Tab presses; ring `2px solid var(--accent-500)` on all; one dark focus capture; the breadcrumb title passed when creating every session; `studio-block-selected-dark.png`. Gates G9.
12. **Process, so round 8 is not needed.** `NOTES.md` lists each fix by number with done, partial or not done and the capture that proves it. Record `git rev-parse HEAD`, a dirty-tree flag and a diff hash in `preflight.json`; do not edit it afterwards. Preflight also probes the Low gain and Finite crossover goldens. Copy `DESIGN_PLAYBOOK.md` and the round 3 to 6 critiques into the repo. Merge `round6/studio-fix/studio-r6.spec.ts` into the existing specs.

---

## 11. Round 7 checklist

Every capture: theme in the filename, `data-theme` reset first, 1280 x 800 unless stated, `preflight.json` (unedited, with dirty flag) attached, runs cleared per theme.

**Studio (light and dark, 1280 and 1440, each before and after Simulate):** wires, arrowheads and signal labels visible in all eight; PID gap at least 48px; chart with tick numbers; margins strip on one line.
- `studio-block-selected-{light,dark}.png` and `studio-block-selected-after-simulate-{light,dark}.png`: inspector never clipped, Pin comment and "Pin" visible.
- `studio-step-settled-{light,dark}.png` (PID golden with "Settled at" and "Overshoot"), `studio-step-offtarget-light.png`, `studio-step-unsettled-{light,dark}.png`, `studio-step-extended-light.png` (a different x axis from the 10 s one).
- `studio-margins-finite-light.png`, `studio-margins-no-crossover-light.png` (Phase margin "Not defined"), and a dark of each.
- `studio-after-resize-light.png`.

**Home:** `home-empty-light`, `home-with-recent-light`, `home-dark`, `home-scrolled-{1280,1440}-light`, `home-scrolled-dark` with the redrawn thumbnails.

**Light and dark pages that changed:** `problems-list`, `problems-row-hover` (with tooltips visible), `cmdk-open`, `cmdk-query`, `gallery`, `library` (with the Add dialog open in a second capture), the five Settings tabs.

**Focus by real Tab presses:** `focus-tab-light` (a Work tab), `focus-table-row-light` (a Problems row), `focus-button-light` (a button), `focus-tile-light`, `focus-composer-light`, and one dark of each.

**Logs to attach:** `preflight.json`, `sidebar-measurements.json` (add Studio at 1280 and 1440), the Playwright output for `studio-layout`, `studio-wire-selection`, `studio-r5` and `studio-r6` specs, a contrast table for dark window buttons, margin captions and arrowheads, and the `md5.txt` diff against round 6.

Files reviewed: all 60 PNGs in `round6/` plus `NOTES.md`, `MY_NOTES.md`, `md5.txt`, `preflight.json`, `sidebar-measurements.json`. Secondary shots (the rest of the Settings tabs, the focus set, `problems-loading`, `library-dark`, `gallery-light`) I read through contact sheets after reading their light or dark twins in full. Source read read-only from `origin/main` at `8d181a8` (code identical to `5095779` for the files cited).
