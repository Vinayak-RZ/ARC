# Round 5 critique (Design lead, 13 Nov 2026)

Build: PR #51, commit `2ba9b3e` on `cursor/arc-ui-polish-ad61`. I opened all 54 PNGs in `round5/` (the folder holds 59 files, not 58: 54 PNGs plus `NOTES.md`, `MY_NOTES.md`, `md5.txt`, `list.txt` and `sidebar-measurements.json`). I compared every md5 with round 4, sampled native pixels (the PNGs are 1280 wide, so coordinates below are native unless I say "scaled"), and read the source at `2ba9b3e` with read-only `git show`. I also **ran the Python side of `2ba9b3e` in a scratch venv** (nothing in your repo was edited, committed or pushed) to settle the "stale captures or false claim" question.

**Total: 32 / 50 (round 1: 25, round 2: 30, round 3: 32, round 4: 33, so -1).** The first drop in five rounds, and it is not because the work got worse. The builder did land real improvements (the loop now fits, selection works, Settings, stale state and a full dark set), but **the captures do not show the new engine code**, and the Studio drawer regressed. If the captures were regenerated from the same commit with a correct backend, I estimate 36 to 37 (see "What the score would be").

**Ready to show Vinayak: NO.** Section near the end.

---

## 1. The big finding: the captures were taken from an older backend than the source

EE Project asked whether the defaults changed in code but the captures are stale, or never changed. **Answer: they changed in code. The captures are stale.** Evidence:

| Check | Source at `2ba9b3e` | Capture shows |
|---|---|---|
| PID defaults (`goldens.py`) | `kp 50, ki 100, kd 5`, DC motor at x 528 (a 72px gap after the PID), scope at x 672 | `Kp 2 · Ki 0.5 · Kd 0.1` on the PID block, **8px** between PID and DC motor (PID right edge 956px, motor left edge 965px) |
| Margins for the PID loop (I ran `analyze()`) | PM **94.6°**, ωcg **8.735 rad/s**, gain margin Infinite, phase crossover none | PM **99.8°**, ωcg **0.05093 rad/s** (the old Kp 2 numbers) |
| Gain margin caption (`margins.py`, `_fmt_gm_db`) | "Phase never reaches −180° from 0.001 to 100,000 rad/s." | "Gain margin is infinite because open-loop gain stays above 0 dB in the analyzed band." (the old wrong text) |
| Phase crossover caption | "Phase stays above −180° from 0.001 to 100,000 rad/s." | "Gain stays above 0 dB ..." (old) |
| Low gain, gain crossover | "Gain stays **below** 0 dB from 0.001 to 100,000 rad/s." (I ran it) | "Gain stays **above** 0 dB" (old) |
| Low gain, phase margin | "Not defined" (no gain crossover) | "Infinite" (old) |
| Step chart (`StepChart.jsx`, `ResultsDock.jsx`) | An SVG chart with a 10 s / 30 s / 100 s / Auto control and a "Not settled" pill, rendered whenever `sim.step_series` exists, else an `<img>` fallback | The `<img>` fallback: matplotlib title inside the plot, 6px ticks, no window control, no pill |

Every mismatch is on the **Python** side (golden, margins, `step_series`), while every **UI** change (new drawer layout, selection outline, floating inspector, wire fit, Settings tables, Cmd+K icons) is visible. So the build served a fresh `ui/dist` against an old engine. The most likely cause is in `scripts/capture_ux_review_round.py`: it starts the server with `python -m electrical_engineer ui` from the repo root, but the package lives under `src/`, so the import resolves to whichever copy is installed in the interpreter (a non-editable install from an earlier round, or a server left running on 8765). It also runs `npm run build` **only if `ui/dist/index.html` is missing**, so the UI can be stale in the other direction. This is an inference from the evidence, not something I could observe running their environment.

**What I verified by running `2ba9b3e` Python** (python-control, scratch venv, nothing of theirs touched):

| Golden | Margins display | Step metrics |
|---|---|---|
| `pid_dc_motor` (Kp 50, Ki 100, Kd 5) | GM Infinite (tip: phase never reaches −180°), PM 94.6°, ωcg 8.735 rad/s, ωcp none (tip: phase stays above −180°) | settled, ends at 1.0000, peak 1.016 (1.6% overshoot) |
| `unity_first_order` | GM Infinite, PM 95.7°, ωcg 9.95 rad/s | **`settled: False`** with a flat curve ending at 0.909 |
| `open_loop_low_gain` | GM Infinite, PM Infinite, ωcg "No crossover in range" (tip: gain stays **below** 0 dB) | **`settled: False`**, flat at 0.001 |

So the new defaults do give a visible, settling step, and the corrected captions are right. Two new engine-side problems turned up:

1. **A flat curve is called "not settled".** `_step_metrics` tests the tail against the *setpoint* (1.0). For `unity_first_order` the loop is 10/(s+11), which settles quickly at 0.909 (a 9% steady-state error). The UI would show the amber pill "Not settled within 10 s" and the footnote "Still rising at 10 s: 0.91", both false: the curve is flat. Same for Low gain at 0.001. That is a visible correctness error waiting to happen the moment the captures are regenerated. Fix in the list (item 3).
2. The PID block label is generated from the golden, so the stale server also explains why `Kp 2 · Ki 0.5 · Kd 0.1` is on every PID capture.

---

## 2. Byte-identical check against round 4 (md5)

| Result | Count | Files |
|---|---|---|
| Identical to round 4 | **4** | `home-empty-light.png`, `home-with-recent-light.png`, `focus-composer-light.png`, `settings-data-light.png` |
| Same name, changed | 31 | all other round 4 names |
| New in round 5 (the dark set) | 19 | `cmdk-open-dark`, `focus-button-light`, `gallery-dark`, `home-scrolled-dark`, `library-dark`, `problem-answer-dark`, `problem-dark`, `problem-stale-dark`, `problem-work-dark`, `problems-list-dark`, `problems-row-hover-dark`, `settings-{about,agents,appearance,data,engines}-dark`, `sidebar-collapsed-dark`, `studio-after-simulate-dark`, `studio-before-simulate-dark` |

All four identical files are declared in `NOTES.md` with a reason, which is the discipline I asked for. `md5.txt` matches the files on disk, and there are no duplicate images inside round 5. Two of the four reasons are really "not done": Home thumbnails and the Continue cards were the round 4 items 8 and 5, now skipped twice.

**Measurements**
- Sidebar (`sidebar-measurements.json`): expanded **240**, collapsed **56**, Cmd+K open **240**, grid `240px 1040px` and `56px 1224px`. **Pass.** Studio at 1280 and 1440 was not recorded (I asked for it in the round 4 checklist).
- Input borders: `#8C8C87` on white, 3.38:1 (Problems search and the Parameters drawer both sampled). Dark input border `#757570` on `#1A1A18`, about 3.9:1. **Pass.**
- Dark contrast, measured: "View engine output" link `#8FB0F5` on `#12261C`, **7.35:1** (was 1.88:1, fixed). "Checked" word 4.71:1 dark and 5.79:1 light (was 3.01:1, fixed). **Dark schematic labels** (`problem-answer-dark.png`, "R1 = 1 kΩ", "R2 = 1 kΩ", "Vin = 10 V") are black on `#1A1A18`, **1.2:1**. **Dark Parameters values** (`problem-stale-dark.png`, Vin 10, R1 1) are black on the field, **1.2:1**.
- No panels overlap in any Studio capture, before and after Simulate, at 1280 and 1440. The layout fix holds.

---

## 3. EE Project's points, verified

| Point | Verdict | Evidence |
|---|---|---|
| Wire fit and block selection now work | **Agree, with one caveat** | After Simulate the feedback wire sits about 85px above the canvas bottom at 1280 (`studio-after-simulate-dark.png`) and fully inside at 1440. Selection: 2px cobalt outline with a 2px offset and the inspector opens (`studio-block-selected-light.png`), and it **persists through Simulate** (`studio-layout-after-simulate-light.png` still shows PID selected). Caveat: that persistence is exactly what hides the loop (inspector point below). Ports are still 8px hollow rings, not the 12px filled handles I specified |
| Margins row crushed by the chart, values run together, phase crossover clipped | **Agree, and I can name the cause** | `studio.css` line 80: `.studio-results-layout { grid-template-columns: minmax(320px, 360px) minmax(0, 1fr) }`. A four-column table needing about 700px is forced into a 360px column, so "99.8°" and "0.05093 rad/s" butt together at 28px and the Phase crossover column slides under the chart card (`studio-layout-after-simulate-light.png`, x 508 to 530 scaled). This is **CSS, independent of the stale backend**, so it will still be broken next round unless fixed. Spec in item 2 |
| Gain margin captions give the wrong reason | **Agree, but fixed in code** | Table in section 1. Not fixed in the captures. In `studio-margins-finite-light.png` it is worse than wrong: the card says "Infinite ... open-loop gain stays above 0 dB" next to a gain crossover of 9.95 rad/s, which contradicts itself on one screen |
| Captures still show Kp 2/0.5/0.1, no pill | **Agree, captures stale** | Section 1 |
| Dark-mode wires have no arrowheads | **Agree** | `studio-before-simulate-dark.png` and `...after-simulate-dark.png`: `r`, `e`, `y` wires end in plain stubs. Cause (probable): `ControlStudio.jsx` line 445 passes `color: "var(--cs-text)"` to React Flow's `MarkerType.ArrowClosed`, which writes it into SVG `stroke` and `fill` presentation attributes, where `var()` is not resolved, so the head falls back to black. Black on `#1A1A18` is invisible. The CSS override at `studio.css` 753 does not rescue it in the capture. Fix in item 6 |
| Inspector popover covers the blocks next to the selection | **Agree** | `studio-layout-after-simulate-light.png`: the 280px card at top 12px right 12px (`.studio-inspector-float`, `position: absolute`, `z-index: 6`) covers the DC motor and Scope, and cuts the feedback wire, in the one capture whose job is to show the loop |
| Dark Recent list shows a duplicate | **Agree, and it is wider than Recent** | `problem-dark.png` Recent: two "Voltage divider · Vout". `home-scrolled-dark.png` Continue: two identical cards. `problems-row-hover-dark.png`/`sidebar-collapsed-dark.png`: two identical rows. `library-light.png`: two "kuphaldt-dc" rows. The data is created by the capture script, but the UI must disambiguate regardless |
| Step chart is still matplotlib-looking | **Agree, stale backend** | Section 1. Note the PNG is bigger than round 4 (about 450 x 215 scaled against 146 x 110) |

---

## 4. Status of round 4's 12 fixes (verified in the captures)

You asked me to check the claim that items 7 to 10 are done. `NOTES.md` does not list items by number; its only claims are the four byte-identical rows and "all other captures differ". Checked against the images:

| # | Round 4 fix | Status | Evidence |
|---|---|---|---|
| 1 | Keep the loop inside the canvas | **Done in the UI, not in the captures' geometry** | Wire inside at 1280 and 1440, light and dark. Still missing in captures: the 48px gap (8px shown, stale golden) and "1st-order plant" overflowing its block (`studio-margins-*`). The `studio-wire-selection.spec.ts` exists in the diff (66 lines) |
| 2 | Selection sticks and looks selected | **Done, one defect** | Outline, inspector, persistence confirmed. Defects: the inspector covers blocks; ports 8px hollow; no dark capture of the selected state |
| 3 | Themed, annotated Step chart | **Not done in the captures** | `StepChart.jsx` exists with axes, setpoint line, cursor readout, `role="img"`. Never rendered in any capture (PNG fallback) |
| 4 | Say when not settled | **Not done in the captures, and the code has a bug** | Pill and window control exist in source and are absent from every image. Logic flags flat curves (section 1) |
| 5 | Correct the margin captions | **Done in code, not done in the captures** | Verified by running the code. Every capture still shows the old text |
| 6 | Finish dark mode and capture all of it | **Partial, good progress** | Done: link 7.35:1, Checked 4.71:1 and 5.79:1, full 19-capture dark set, dark Studio before and after. Not done: arrowheads, schematic labels (1.2:1), Parameters values (1.2:1), Home thumbnails and Gallery figures are white boxes on `#1A1A18`, Copy button is white in Settings > Agents (dark) |
| 7 | Stale state coherent | **Done** (both themes) | Amber strip with a warning icon and one sentence, answer at about 60%, the top-bar "Run again" is the only filled button. Residual: the drawer banner repeats the message ("Answer is stale after your edit.") and its "Run again" still wraps to two lines (`problem-parameters-stale-light.png`, right column, first card) |
| 8 | Home example cards | **Not done** | `home-empty-light.png` and `home-with-recent-light.png` are byte-identical to round 4. Still raw matplotlib PNGs with embedded titles, tile 4 repeats tile 2, tile 6 is a phasor labelled "Signals workout", Continue cards identical, Agent line still "in this repo". **This contradicts any claim that 7 to 10 are done** |
| 9 | Settings, Problems, Cmd+K | **Partial** | Settings **done**: About is a four-row table with no branch name, Engines has "Available" and "Not installed" tags, Appearance has a Light/Dark/System segment. Problems **partly**: `/` in a `kbd`, centred empty and error pages with icon, skeleton rows. Not done: the row rules still stop 106px short of the header and actions (`problems-list-light.png`, `sidebar-collapsed-dark.png`), and Subject and Made by are native selects. Cmd+K **partly**: icons, Actions group, `kbd` chips added. New defects below (centred labels, "GH" chips, faded last row, ring on the query input) |
| 10 | Gallery and Library | **Partial** | H1s now "Gallery" and "Library" with plain subtitles. Still: recipe ids under every caption (`power.swing_equal_area`), uneven card heights, Library table has two identical rows, "Add a source" wraps to two lines, an inline "Add a book" form with native selects and a native file input, no dialog |
| 11 | Detail pass | **Partial** | Done: block shadows removed. Not done: boxed chevron under Work step 2, six palette rows still share the "f" glyph (Step, Ramp, Sine, Transfer Fcn, Saturation, Delay), no V<sub>out</sub> marker on the schematic, duplicate sidebar titles |
| 12 | Capture discipline | **Partial** | Done: theme in every filename and correct (no leaked themes), `sidebar-measurements.json` back, identical files declared with reasons, `focus-tile` focuses an example card. Not done: `focus-tab-light.png` shows the skip link, `focus-table-row-light.png` shows the Activity tab on a Problem page, `focus-button-light.png` shows the Diagram tab, no dark focus captures, and the focus ring is black 2px on those but cobalt on the composer |

Tally in the captures: **done 1, 2, 7** (1 and 2 with defects); **partial 6, 9, 10, 11, 12**; **not done 3, 4, 5, 8**. Items 3, 4 and 5 are done in source and would flip to done once the captures come from the right backend. Item 8 is not done anywhere.

---

## 5. Scores

| # | Criterion | R1 | R2 | R3 | R4 | R5 | One-line reason |
|---|---|---|---|---|---|---|---|
| 1 | Answer-first hierarchy | 3 | 4 | 4 | 4 | 4 | Answer card, Checked strip (7.35:1 link, 4.71:1 word) and the amber stale strip are coherent. Home Continue still shows two identical cards |
| 2 | Layout, spacing, alignment | 2 | 3 | 3 | 4 | **3** | Panels never overlap, but the results drawer is now broken (360px column for a four-column table, values colliding), the palette search collapses to 14px after Simulate, Problems rules 106px short |
| 3 | Typography | 3 | 3 | 3 | 3 | 3 | Block text 13px, Settings tidy. Chart text about 6px, Cmd+K rows centred, tags still 11px |
| 4 | Colour and accent discipline | 3 | 3 | 3 | 3 | 3 | One filled button when stale, link fixed. Dark: schematic labels 1.2:1, Parameters values 1.2:1, white plots, missing arrowheads |
| 5 | Surfaces, borders, elevation | 3 | 3 | 3 | 4 | 4 | Flat hairline Studio panels and flat blocks, a proper elevated popover. Native selects and file input remain in Problems and Library |
| 6 | States and interaction | 3 | 4 | 4 | 3 | **4** | Selection works and persists, stale, empty, error, loading and hover all exist. Focus ring colour inconsistent, three focus captures show the wrong element |
| 7 | Plots | 2 | 2 | 2 | 2 | 2 | Studio chart is a larger PNG with 6px text, no units or annotations. Home and Gallery thumbnails unchanged. The SVG chart exists in code |
| 8 | Schematics and block diagrams | 2 | 3 | 3 | 3 | 3 | Loop fits, orthogonal, 13px labels, selection ring. Dark has no arrowheads, 8px PID to motor gap, "1st-order plant" overflows its block, dark schematic labels illegible |
| 9 | Trust and copy | 2 | 3 | 3 | 3 | **2** | A wrong caption on screen for the third round, "99.8°0.05093 rad/s" reads as one number, the finite-crossover card contradicts itself, duplicates in Recent, Continue and Library. Down one, because these are visible correctness errors |
| 10 | Shell, navigation, consistency | 3 | 4 | 4 | 4 | 4 | 240 and 56 exact, theme labels now right, H1s fixed, full dark set. Cmd+K alignment bug, duplicate Recent |
| | **Total** | **25** | **30** | **32** | **33** | **32 / 50** | Below 38: iterate |

### What the score would be if the captures came from the right backend (estimate, not seen in the UI)
Plots 2 to 3 (SVG chart, window control, pill), Trust 2 to 4 (right captions, "Not settled" logic once fixed), Schematics 3 to 4 (72px gap, labels). That gives **36 to 37**, and 38 with the margins strip fixed (Layout 3 to 4). That is why fix 1 ranks first: it costs about 20 lines of script and unlocks about 5 points that are already built.

---

## 6. Per-screen issues

### Studio (`studio-layout-before-simulate-light.png`, `studio-layout-after-simulate-light.png`, the `-1440` pair, `studio-block-selected-light.png`, `studio-margins-finite-light.png`, `studio-margins-no-crossover-light.png`, `studio-before-simulate-dark.png`, `studio-after-simulate-dark.png`)
- **Results drawer, left column (after Simulate):** margins crushed (cause above). "Gain margin (dB)" header wraps to three lines at 12px, the caption wraps one to two words per line ("Gain margin is infinite because open-loop gain stays above 0 dB in the analyzed band." takes eight lines), and the "Step / Bode / Root locus" tabs sit under it at the bottom.
- **Results drawer, right:** the matplotlib PNG (title inside the plot, tick text about 6px, "Output" with no unit, no setpoint line), a dead `resize` grabber still in the bottom-right corner.
- **Canvas, right edge, `studio-layout-after-simulate-light.png`:** the 280px inspector hides DC motor, Scope, the `y` wire and the right half of the feedback wire.
- **Canvas, between PID and DC motor:** an 8px gap, so the `u` label sits on the PID corner and there is no wire or arrowhead (stale golden).
- **Canvas, dark:** no arrowheads on `r`, `e`, `y`, and the feedback return. Sum block ring is faint grey. Loop is otherwise legible, 13px text.
- **Canvas, `studio-margins-*`:** "1st-order plant" wraps to two lines and the second line is cut by the block bottom, with a port dot drawn on top of the text. The palette calls it "1st-order plant" and the title bar "Finite crossover", so the same block has two names.
- **Palette, after Simulate:** the "Search blocks" field collapses to about 14px tall and loses its padding (it is 32px before Simulate). A flex child with no `flex-shrink: 0`. The list is cut at "Saturation" with no scroll cue.
- **Toolbar:** "Studio / Control Studio" in dark and "Studio / PID DC motor" in light for the same golden. Zoom reads 116% and 119% for the same loop at the same width, because fit depends on content height. That is fine, but report the zoom in the Playwright log.

### Home (`home-empty-light.png`, `home-with-recent-light.png`, `home-scrolled-1280-light.png`, `home-scrolled-1440-light.png`, `home-dark.png`, `home-scrolled-dark.png`)
- **Example cards:** unchanged for three rounds. Raw plots with embedded titles at about 5px, white rectangles on dark (`home-dark.png`), tile 4 repeats tile 2's step response, tile 5 is a thin strip, tile 6 is a power phasor under "Signals workout".
- **Continue row:** two identical "Voltage divider · Vout" cards (light and dark).
- **Composer hint:** "Press Ctrl Enter to solve" in plain text. Platform-aware is right, but render it as `Ctrl` `↵` in two `kbd` chips.
- **Agent line:** "Run electrical-engineer mcp in this repo and connect Cursor or Claude Code. CLI" is cut and still says "in this repo".

### Problem (`problem-answer-light/dark.png`, `problem-work-tab-light.png`, `problem-work-dark.png`, `problem-parameters-drawer-light.png`, `problem-parameters-stale-light.png`, `problem-stale-dark.png`, `problem-dark.png`)
- **Answer card:** strong in both themes. V<sub>out</sub> with a subscript, 5.00 V, one strip.
- **Stale (right column, first card):** the banner repeats the strip's message and its button wraps. In dark the three values (10, 1, 2 kΩ) are near-black on the field.
- **Diagram tab, dark:** schematic labels black on dark (1.2:1) and the wires and symbols are white on a dark plate, so only the text fails. No V<sub>out</sub> marker.
- **Work tab, step 2:** boxed chevron under the subtitle, 36px below the text it expands.

### Problems, Cmd+K, collapsed rail (`problems-*-light.png`, `problems-list-dark.png`, `problems-row-hover-dark.png`, `cmdk-open-light/dark.png`, `cmdk-query-light.png`, `sidebar-collapsed-light/dark.png`)
- **Table:** header band spans the full width, row rules end 106px short. Hover icons (open, rerun, copy) sit beyond the rule with no tooltips in the capture. Two rows with identical titles.
- **Cmd+K, Go to group:** labels are **centred** in the row (Home, Problems, Studio ...) while the Problems group is right-aligned. Both should be left-aligned after the 16px icon. Shortcut chips read "GH", "OP"; write `G` then `H` as two chips or "G H". The last visible row is faded as if disabled (a mask gradient on the list bottom, `cmdk-open-dark.png`). The query input has a 2px near-black ring inside a bordered palette (`cmdk-query-light.png`), a double border.
- **Loading:** eight bars, no toolbar skeleton, fine. **Error:** "Try again" and "Details" are 4px apart; give 12px.

### Gallery, Library, Settings (`gallery-light/dark.png`, `library-light/dark.png`, `settings-*-light/dark.png`)
- **Gallery:** recipe ids under every caption, uneven card heights, dark shows full white figure mats with no frame. SMIB equal-area appears twice (static and GIF) next to each other.
- **Library:** the inline "Add a book" form is permanent, selects and the file field are native, "Add a source" wraps, two "kuphaldt-dc" rows differ only by "Used in" (2 and 6), subtitle floats 24px below the H1.
- **Settings:** About "conditional / ok" in one row reads oddly (Result says conditional, Status says ok). Copy button on Agents is a native white button (also in dark). Data is one sentence.

### Focus (`focus-composer-light.png`, `focus-tab-light.png`, `focus-table-row-light.png`, `focus-tile-light.png`, `focus-button-light.png`)
- Composer cobalt ring correct. Tile ring correct. The other three are black 2px rings on a 4px gap; the playbook colour is `--accent-500`. Wrong elements are focused in three of the five captures.

---

## 7. Specs you asked for

### 7.1 Margins row (fix item 2)
Margins become **one full-width strip above the chart**, four equal cells, never a table.

```css
.studio-results { height: clamp(300px, 42vh, 400px); }          /* 336px at 800 high, canvas keeps >= 300px */
.studio-results-layout { display: grid; grid-template-columns: minmax(0, 1fr);
  grid-template-rows: auto minmax(0, 1fr); gap: 12px; padding: 12px 16px; }
.studio-margins { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0 16px; }
.studio-margin { min-width: 0; }
.studio-margin dt { font: 600 12px/16px var(--font-sans); color: var(--text-secondary); }
.studio-margin dd { margin: 4px 0 0; display: flex; align-items: baseline; gap: 4px; white-space: nowrap;
  font-variant-numeric: tabular-nums; }
.studio-margin .num  { font-size: 24px; line-height: 28px; font-weight: 600; }
.studio-margin .unit { font-size: 12px; color: var(--text-secondary); }
.studio-margin .is-textual { font-size: 16px; line-height: 24px; font-weight: 600; }   /* "No crossover in range" */
.studio-margin-meta { font-size: 12px; line-height: 16px; color: var(--text-muted);
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.studio-search { flex: 0 0 32px; }                                /* stops the palette search collapsing */
```
Labels: "Gain margin", "Phase margin", "Gain crossover", "Phase crossover" (units go beside the value: `12.4 dB`, `94.6 °`, `8.735 rad/s`). Tabs "Step | Bode | Root locus" move to the chart header row on the left, the window control and the settling pill on the right. The `title` attribute carries the full caption when clamped.

### 7.2 Inspector placement
**Dock it, do not float it.** The loop is five blocks in a row, so anything next to a selection covers a neighbour, and a collision-avoiding popover would have to sit above or below, where the feedback wire and the toolbar are.
- When a block is selected, the grid becomes `48px minmax(0, 1fr) 264px`. The palette collapses to its existing 40px icon rail (`.studio-palette-icons` already exists), the inspector takes the freed width. When nothing is selected, `220px minmax(0, 1fr) 0`.
- At 1280 the canvas is 992 − 48 − 264 = about 680px (the round 4 canvas was 772px beside a 220px palette). The loop (5 blocks, 48px gaps) is about 704px at 100%, so with 24px padding fit lands at about 0.90, above the 0.85 floor. If a future change pushes fit below 0.85, use the popover fallback. At 1440 there is plenty of room.
- Below a 1200px viewport width only, fall back to a popover anchored **above** the selected block (Floating UI `flip`, `shift`, `padding: 12`), never over the feedback path.
- Enter and exit with the existing 160ms ease; the canvas re-fits through the `ResizeObserver` already in `FitViewOnChange.jsx`. Escape and pane click clear it.
- Rule for the spec: the inspector's bounding box must not intersect any `.react-flow__node` or `.react-flow__edge-path` box (assertion in 7.5).

### 7.3 "Not settled" and the settled logic
```py
# simulate.py, replace the settled test
tail = y[-max(3, len(y)//10):]
flat = (tail.max() - tail.min()) <= 0.01 * max(abs(tail.mean()), 1e-9)
sse = abs(setpoint - y[-1]) / abs(setpoint or 1.0)
status = ("not_settled" if not flat else
          "settled" if sse <= 0.02 else "settled_off_target")
```
UI (`StepChart.jsx`): `settled` shows no pill and a "Settled at 1.00" label with a 2% band; `settled_off_target` shows a **neutral** pill "Settles at 0.91, 9% below the setpoint"; `not_settled` shows the amber pill "Not settled within 10 s" and "Still rising at 10 s: 0.45 of a setpoint of 1". Never say "rising" unless the tail slope is above zero. Rename `rising_at_end` to `value_at_end`.

### 7.4 Dark arrowheads and dark schematics
- Draw the arrowhead with our own `<marker>`: `<polygon fill="currentColor">` inside a `<g class="studio-arrow">`, with `.studio-arrow { color: var(--cs-wire); }`, `--cs-wire` = `#1A1A18` light, `#E8E8E6` dark. Do not pass `var()` to `MarkerType` colours.
- Schematic SVG text and symbols: `fill: currentColor`, `color: var(--text)`. A schematic must never carry a hard-coded `#000`. Same for the Parameters inputs: `color: var(--text)`, placeholder `--text-muted`.
- Playwright: for every `.studio-arrow polygon`, computed `fill` is not equal to the canvas background and has at least 3:1 against it, in both themes.

### 7.5 Playwright assertions to add (`studio-r5.spec.ts`, saved next to this file)
Saved at `round5/studio-fix/studio-r5.spec.ts`: (a) no `.studio-kpi` or `.num` element has `scrollWidth > clientWidth`, (b) no two `.studio-margin` boxes intersect and none intersects the chart box, (c) inspector box does not intersect any node or edge box while a block is selected, before and after Simulate, (d) arrowhead fill contrast in both themes, (e) preflight: the PID golden has `kp === 50` and the simulate response has `step_series`, so a stale backend fails the run.

---

## 8. Ready to show Vinayak?

**No.**

Threshold: **at least about 38 / 50, no rubric criterion below 3, and no visible correctness errors** (wrong captions, clipped or colliding values, duplicates).

| Gate | Round 5 | Pass? |
|---|---|---|
| Total at or above 38 | 32 (36 to 37 if captures are regenerated correctly) | No |
| No criterion below 3 | Plots 2, Trust 2 | No |
| No wrong captions | Old caption on four Studio captures, contradicting itself on one | No |
| No clipped or colliding values | "99.8°0.05093 rad/s", phase crossover cut to "No" | No |
| No duplicates | Recent, Continue, Problems rows and Library rows | No |

**Exact blockers left**

| # | Blocker | Kind | Effort |
|---|---|---|---|
| B1 | Captures come from an older backend than the source (wrong captions, Kp 2, no chart, no pill, 8px gap) | Build and capture | Hours: editable install, always rebuild `dist`, preflight assert |
| B2 | Margins strip crushed by the 360px column | CSS | Half a day |
| B3 | "Not settled" fires on flat curves (verified by running the code) | Engine and UI copy | Half a day |
| B4 | Inspector covers the loop after Simulate | Layout | Half a day |
| B5 | Dark Studio and schematic correctness: arrowheads, 1.2:1 labels, 1.2:1 input values, white thumbnails | CSS and SVG | One day |
| B6 | Home example cards unchanged for three rounds (raw plots, white in dark, repeats, wrong subject) | Content and component | One to two days |
| B7 | Duplicates in Recent, Continue, Problems, Library | Data and UI | Half a day |
| B8 | Cmd+K alignment, faded last row, ring | CSS | Hours |

Not blockers but expected by the 40 mark: Gallery ids and card heights, Library dialog and native controls, Problems table rule width, distinct palette icons, focus captures.

**Estimate: 2 more rounds.** Round 6 clears B1 to B5 and B7 and B8, which projects to about 37 to 38 with Plots at 3 and Trust at 4, if the builder runs the preflight and shows the SVG chart. Round 7 clears B6 (Home and Gallery thumbnails from tokens), the Library dialog and the dark-mode polish, projecting 40 or more, and is the round to show Vinayak. It becomes **3 rounds** if B1 is not fixed first (every Studio fix after it is unverifiable) or if the Home thumbnails slip again; they have been skipped three rounds running.

---

## 9. Ranked fix list (12, ordered by what moves the "ready" verdict; paste into the next build prompt)

1. **Make the captures prove the build** (`scripts/capture_ux_review_round.py`). Install the package editable (`pip install -e .`) or run the server with `PYTHONPATH=src`. Always run `npm run build` (drop the `if not dist/index.html` guard). Kill anything on 8765 first. After the health check, write `preflight.json` with `git rev-parse --short HEAD`, `electrical_engineer.__file__` (must be under `src/`), the PID golden's `kp`, and whether a simulate response has `step_series`; the run fails if `kp != 50`, if `step_series` is missing, or if the gain margin tip lacks "−180". Print the sha in `NOTES.md`. This alone moves Trust 2 to 4, Plots 2 to 3, Schematics 3 to 4.
2. **Fix the margins layout** (`studio.css` line 80, `ResultsDock.jsx`). Spec 7.1: one full-width four-cell strip above the chart, 24px value with a separate 12px unit, captions clamped to two lines, drawer `clamp(300px, 42vh, 400px)`, search field `flex: 0 0 32px`. Delete the `resize` grabber. Playwright (a) and (b).
3. **Fix "not settled"** (`simulate.py`, `StepChart.jsx`). Spec 7.3: three states, flat curve never labelled rising, "Settles at 0.91, 9% below the setpoint" for steady-state error, pill and 10 s / 30 s / 100 s / Auto control visible in the captures. Add `test_step_metrics.py` with `unity_first_order` (off target), `open_loop_low_gain`, and the PID golden (settled).
4. **Dock the inspector** (`studio.css` 41 to 54, `ControlStudio.jsx`). Spec 7.2: grid becomes `48px 1fr 264px` on selection, palette to icon rail, popover above the block only below 1200px, 12px filled ports, selection capture in light and dark plus one after Simulate. Playwright (c).
5. **Correct the engine captures' remaining defects** (`studio-margins-*`). "1st-order plant" becomes "First-order plant" in palette, block and title, at most two lines of 13px/16px in a 64px block, no port dot over text. PID to motor gap 48px (the golden already has 72px). Distinct 16px Lucide icons for Step, Ramp, Sine, Transfer Fcn, Saturation, Delay.
6. **Dark correctness** (`ControlStudio.jsx` 445, `StaticStudyDiagram.jsx`, `tokens.css`). Spec 7.4: own `<marker>` with `currentColor`, `--cs-wire` token, schematic text `currentColor`, Parameters and all inputs `color: var(--text)`, Settings Copy button themed. Thumbnails and Gallery figures get a 1px `--border` frame and a `#FAFAF9` mat in dark (plots stay light inside it) until token-drawn versions exist. Contrast table for every dark capture attached to NOTES.
7. **Home example cards, finally** (`home-empty-light.png`). Six distinct token-drawn SVG thumbnails, 16:10, no embedded titles, ticks at least 11px at thumbnail scale: Voltage divider (two resistors and a tap), First-order step (response curve), SMIB swing (equal-area curve), DC drive speed (speed against time, rad/s), Digital loop (unit circle with poles), Signals workout (a spectrum). Continue cards carry "Today 17:12"; Agent line "Connect your coding agent" with the command in a `kbd` block, no "in this repo". Composer hint as `Ctrl` `↵` chips.
8. **Disambiguate duplicates everywhere** (Recent, Continue, Problems, Library). Same-title items get a muted second line ("Today 17:12" or the short id). The capture script clears `runs/` before each theme so the set shows one of each unless the shot is *about* duplicates. Library rows merge by source name with a combined "Used in".
9. **Cmd+K polish** (`CommandPalette.jsx`). Left-align every row after the 16px icon, `G` then `H` as two `kbd` chips, remove the bottom fade mask (let the list scroll with a 1px divider), input with a bottom border and no ring, Actions group at normal ink with New problem, Run again, Open in Studio, Toggle sidebar, Toggle theme.
10. **Problems table and filters** (`ProblemsPage.jsx`). Row rules run full width to the actions column; hover icons get tooltips; Subject and Made by become 32px styled selects; tags 12px sentence case; Try again and Details 12px apart.
11. **Gallery and Library finish.** Gallery captions drop `power.swing_equal_area`, cards 16:10 image frames of equal height, a figure shown once with a "GIF" toggle. Library: "Add a source" in one line, the form moves into a dialog with a drop zone and styled selects, 12px under the H1 for the subtitle.
12. **Capture discipline v3.** `focus-tab` must land on a Work tab, `focus-table-row` on a Problems row, `focus-button` on a button (all by Tab presses), focus ring `2px solid var(--accent-500)` everywhere, plus one dark focus capture. Record Studio's sidebar width at 1280 and 1440 in `sidebar-measurements.json`. Make `md5.txt` fail the run for an undeclared identical capture (already declared this round, keep it).

---

## 10. Round 6 checklist

Every capture: theme in the filename, `data-theme` reset first, 1280 x 800 unless stated, `preflight.json` attached.

**Studio (light and dark, 1280 and 1440):**
- `studio-before-simulate-{light,dark}.png`, `studio-after-simulate-{light,dark}.png`: PID block reads `Kp 50 · Ki 100 · Kd 5`, 48px gaps, arrowheads in both themes, loop fully inside the canvas, margins strip on one line with no collisions, chart SVG with axes and units.
- `studio-block-selected-{light,dark}.png` and `studio-block-selected-after-simulate-light.png`: inspector docked in the right column, no block or wire covered.
- `studio-step-settled-light.png` (PID golden, band and "Settled at"), `studio-step-offtarget-light.png` (`unity_first_order`, "Settles at 0.91, 9% below the setpoint"), `studio-step-unsettled-{light,dark}.png` (pill "Not settled within 10 s"), `studio-step-extended-light.png` (Auto or 100 s).
- `studio-margins-finite-light.png`, `studio-margins-no-crossover-light.png` with the corrected captions, and one dark of each.
- `studio-after-resize-light.png`: viewport 120px shorter, loop still inside.

**Dark set, re-taken:** every page from round 5, plus `problems-empty-dark`, `problems-error-dark`, `problems-loading-dark`, `focus-*-dark`. Check each for white boxes and text under 4.5:1.

**Light set that changed:** `home-empty-light` (six distinct thumbnails), `home-with-recent-light` (Continue rows that differ), `cmdk-open/query-light`, `problems-*-light`, `gallery-light`, `library-light` (sources table, plus the Add dialog open), `focus-*` by real Tab presses.

**Logs to attach:** `preflight.json`, `sidebar-measurements.json` (1280 and 1440, Studio included), the Playwright results for `studio-layout.spec.ts`, `studio-wire-selection.spec.ts` and `studio-r5.spec.ts`, a contrast table for dark text, links, the Checked tag and schematic labels, and the `md5.txt` diff against round 5.

Files reviewed (54 PNGs plus `NOTES.md`, `MY_NOTES.md`, `md5.txt`, `list.txt`, `sidebar-measurements.json`): all of the above; I read each PNG directly, with a contact sheet only for the secondary focus, Settings (dark) and Home-scrolled shots after reading their light twins in full.
