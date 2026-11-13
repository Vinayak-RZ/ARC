# Round 3 critique (Design lead, 13 Nov 2026)

Build: PR #51, commit `0449c4a` on `cursor/arc-ui-polish-ad61`. I opened all 35 PNGs in `round3/` (34 at 1280 x 800, `home-scrolled-1440.png` at 1440 x 800), `NOTES.md`, `md5.txt` and `sidebar-measurements.json`, sampled native pixels for the disputed items, and read the Studio source at `0449c4a` with `git show` (read-only, nothing edited or pushed). Coordinates are native pixels unless I say "scaled" (the viewer shows a 0.8x copy).

**Total: 32 / 50 (round 1: 25, round 2: 30, so +2).** The builder's self-score is 47/60, about 39/50 on this scale. I do not agree with it: Studio is still broken, dark mode is broken in four places, and the Settings About tab is a raw markdown dump.

What improved: the shell, the Problems states, Cmd+K, the light-theme schematic, the Home composer and the margin logic. What did not: the Studio layout, which has now failed two rounds in a row. I found the cause this time (next section). It is two stale CSS rules, not the grid.

---

## Studio overlay: root cause and fix

**Verdict: the grid landed, and two older rules in the same file overrule it.** The builder ported `studio.css` from `cursor/control-studio-6ef3` and added the new `.studio` grid at the top of the file (lines 12 to 25). The old standalone-page rules further down were never deleted. Same specificity, later in the file, so they win.

I rebuilt the page from the real CSS (`tokens.css` and `studio.css` at `0449c4a`, the real class names and DOM order, the real `.product-shell > .workspace` wrapper) and measured it at 1280 x 800 in Chromium. It reproduces the screenshot to within a few pixels:

| Box | Screenshot (native) | My reproduction of the repo CSS | After my fix |
|---|---|---|---|
| Canvas | x 484, y 112, 492 x 494 | x 484, y 116, 492 x **496** | 492 x **372** |
| Palette | 220 x 184 | 220 x **180** | 220 x 372 |
| Results drawer | y 296, 480 tall | y 296, **480** tall | y 488, 288 tall |
| Canvas overlaps results | yes, about 316px | yes, **316px** | no |

Reproduction files and `before.png`, `after.png` are in `round3/studio-fix/`.

### The five faults, in order of damage

1. **Stale `.studio-canvas` rule, lines 435 to 442.** It sets `min-height: max(420px, min(62vh, 560px))`, which is 496px at 800px high. It beats `min-height: 0` from the grid rule at line 131. A grid item's own `min-height` is respected even when the track is smaller, so the 184px row is overflowed by a 496px box. Lines 444 to 449 do the same for `.studio-canvas-inner` and `.react-flow`. **This is the overlay.**
2. **The results row takes the space first.** `grid-template-rows: 44px minmax(0, 1fr) minmax(160px, 60vh)`. A `minmax(160px, 60vh)` track grows to its maximum (480px) before the `1fr` row is resolved, so the canvas row is left with about 184px. Even with fault 1 gone the canvas would be 184px tall.
3. **`.studio-canvas` is `position: relative` with no stacking context.** Positioned boxes paint above non-positioned siblings regardless of DOM order, so the canvas paints over the results drawer instead of being hidden by it. That is why it looks like a modal. The `z-index: 2 !important` rules on `.react-flow__nodes` also leak into the page's stacking context for the same reason.
4. **Stale `.studio-palette` rule (lines 344 to 354), `max-height: 220px` at line 348.** The palette has both `.studio-palette` and `.studio-palette-pane`, so it is also capped at 220px and shows five rows with no scroll cue. Stale `.studio-inspector` (`max-height: min(54vh, 520px)`) and `.studio-results-stage` (`min-height: 280px`, image `max-height: min(52vh, 420px)`) add the same kind of fixed sizes. They also re-add `border-radius` and a full border, so the panels look like four separate cards.
5. **A global `.empty { max-width: 36rem }` in `ui/src/tokens.css` (line 720) hits `.studio-results.empty`.** Before Simulate the drawer is only 576px wide (264 to 840) instead of spanning the grid. That is the narrow "Run Simulate to see the step response" box in `studio.png`. Rename the modifier to `is-empty`.

Not the cause: `transform: scale` (React Flow's viewport transform is inside an `overflow: hidden` box), a missing `min-width: 0` (the middle column already has `minmax(0, 1fr)`), and the shell wrapper (`.product-workspace` is a flex child with a definite height).

### Exact fix

Apply `round3/studio-fix/studio-layout.fix.patch` (135 lines, `patch -p1 --dry-run` is clean against `0449c4a`). The part that matters:

```css
/* 1. one grid, with a results row that cannot starve the canvas */
.cs-app.control-studio.studio {
  --studio-results-h: clamp(200px, 36vh, 340px);
  grid-template-rows: 44px minmax(280px, 1fr) var(--studio-results-h);
  min-height: 560px;            /* .product-workspace scrolls below this */
}
.cs-app.control-studio.studio.is-empty { --studio-results-h: 120px; }   /* before Simulate */

/* 2. the canvas is a clipped, isolated grid item */
.studio-canvas {
  grid-area: canvas;
  position: relative;
  isolation: isolate;           /* keeps React Flow's z-index inside the canvas */
  contain: layout paint;
  min-height: 0;
  min-width: 0;
  overflow: hidden;
  border-right: 1px solid var(--cs-border);
  background: var(--cs-surface);
}

/* 3. delete the legacy block at lines 435 to 449 and replace it with */
.studio-canvas-inner,
.studio-canvas-inner .react-flow { width: 100%; height: 100%; min-height: 0; }

/* 4. delete max-height and the card border from .studio-palette, .studio-inspector;
      results becomes a flex column so the plot fits inside it */
.studio-results { display: flex; flex-direction: column; border-top: 1px solid var(--cs-border); overflow: auto; }
.studio-results-stage { flex: 1 1 0; min-height: 0; }
.studio-results-stage img { width: 100%; height: 100%; min-height: 0; object-fit: contain; }
```

Two JSX edits go with it:

```jsx
// ControlStudio.jsx
<section className={`cs-app control-studio studio${results ? "" : " is-empty"}`}>
// ResultsDock.jsx: rename the modifier so the global .empty rule stops matching
<footer className={`studio-results${stale ? " is-stale" : ""}${results ? "" : " is-empty"}`} ...>
// and delete the duplicate hint: when `margins` is null, MarginTable and the stage both print "Run Simulate..."
```

Result at 1280 x 800: bar 44, canvas row 372, results 288 (120 before Simulate). No box intersects another, and the plot sits inside the drawer instead of running off the bottom.

### Playwright assertion

`round3/studio-fix/studio-layout.spec.ts`. It reads the bounding boxes of `.studio-canvas`, `.studio-palette-pane`, `.studio-inspector` and `.studio-results`, fails if any pair intersects by more than 0.5px, and fails if any box leaves `.studio`. It runs before Simulate, clicks `.cs-simulate-btn`, waits for the plot image to decode, and runs again. It also checks that the plot sits inside the drawer, that no margin caption sits under the canvas, and (second test) that block text is at least 10.9px on screen. Run with `STUDIO_URL=http://localhost:5173/?view=studio npx playwright test studio-layout`, at 1280 x 800 and 1440 x 900.

I ran the pre-Simulate half against my static copies of the layout (the Simulate half needs the live app): **the old CSS fails** (`canvas overlaps results by {"w":492,"h":316}`), **the fixed CSS passes** at both viewports. Below 1280 wide, Studio needs the shell sidebar collapsed to 56px (at 1024 the canvas is only 236px wide), so the spec is limited to 1280 and up.

---

## Measurements you asked for

**Sidebar width** (border sampled at y = 700 in every PNG, compared with `sidebar-measurements.json`):

| State | Spec | Measured | Verdict |
|---|---|---|---|
| Expanded | 240px | border at x = 239 in 34 of 35 captures (including the 1440 one). JSON says `240px 1040px` | **Pass** |
| Collapsed | 56px | `sidebar-collapsed.png` border at x = 55. JSON says `56px 1224px` | **Pass** |
| Cmd+K open | 240px | `cmdk-open.png` and `cmdk-query.png` both at 239. The round 2 glitch (71px) is gone | **Pass** |

**Input borders:** Home composer, Problems search, Library fields, Parameters drawer: `#8C8C87`, 3.38:1 on white, 3.23:1 on the canvas. **Pass.** Dark inputs `#757570`: 3.76:1 on `#1A1A18`, 4.05:1 on `#121211`. **Pass.** Chips, secondary buttons and the Library file picker still use `#E4E4E2` (1.27:1). They carry text, so I do not require 3:1.

**Muted text:** `#70706C` is live. The composer hint measures 4.97:1 on white. **Pass.**

**Focus rings:** composer and dark button show a solid 2px cobalt ring. `focus-tile.png` shows a white 1px-looking ring on dark that I read as 2px `--text-primary`; acceptable. `focus-tab.png` and `focus-table-row.png` show **no visible focus indicator at all** (the capture either did not focus the element or the ring is missing). Treat both as failures until recaptured.

**Dark-theme text that fails contrast:** the Checked strip body text is `#A3A39E` on a pale mint `#E8F5EE` strip: **2.26:1** (`dark-problem.png`, `focus-tab.png`). Schematic labels are pure black on `#1A1A18`: **1.2:1** (`dark-problem.png`).

---

## Scores

| # | Criterion | R1 | R2 | R3 | One-line reason |
|---|---|---|---|---|---|
| 1 | Answer-first hierarchy | 3 | 4 | 4 | `problem-answer.png`: eyebrow, title, meta, `V_out = 5.00 V`, green strip with icon and "View engine output", tabs. A stale answer still shows the green "Solved ... matched" strip |
| 2 | Layout, spacing, alignment | 2 | 3 | 3 | Shell exact, Home grid is now 3 x 2. Studio overlay persists, Problems table stops 105px short of the search field, Library is still a pinned 750px column |
| 3 | Typography | 3 | 3 | 3 | Subscripts and type ramp are clean on the Problem page. Tags still 11px uppercase, Studio block text about 7.7px, About tab is monospace markdown |
| 4 | Colour and accent discipline | 3 | 3 | 3 | Light theme is disciplined. Dark theme: light mint strip, white Step plot, white thumbnails, invisible schematic labels, black arrowheads. Two filled blue buttons in the stale state |
| 5 | Surfaces, borders, elevation | 3 | 3 | 3 | Hairlines hold. Studio panels are still four separate cards with a 16px soft shadow on blocks (`0 6px 16px`) |
| 6 | States and interaction | 3 | 4 | 4 | Loading skeleton (8 rows), empty, error, row hover actions, stale, focus rings on 3 of 5 captures. Misses: no block selection captured, no focus on tab and row, Library still native controls |
| 7 | Plots | 2 | 2 | 2 | Gallery unchanged (embedded titles, about 7px ticks). Home thumbnails are raw crops. Step plot is a white figure in dark and is clipped at the bottom of the drawer |
| 8 | Schematics and block diagrams | 2 | 2 | 3 | Light schematic is a 4 (Vin beside the battery, subscripts, spacing). Block diagram: no overlaps, orthogonal feedback, ports on edges, 96 x 56 blocks, but text 7.7px, arrowheads and labels broken in dark, nothing selected. Scored on the weaker |
| 9 | Trust and copy | 2 | 3 | 3 | Margin logic is now honest ("Infinite", "No crossover in range" with the sweep named). But the Phase margin and gain crossover values are hidden behind the canvas in every capture. About leaks a branch name and `pass^k`. Gallery says "kernels" and shows recipe ids |
| 10 | Shell, navigation, consistency | 3 | 4 | 4 | 240 and 56 exact, Cmd+K glitch gone, Recent row quiet. "Books" H1 under "Library", duplicate Recent titles, no Recent dots in the collapsed rail |
| | **Total** | **25** | **30** | **32 / 50** | Still below 40: iterate |

---

## EE Project's claims, verified

| Claim | Verdict | Evidence |
|---|---|---|
| Home, the answer card with its Checked strip, and the divider schematic are much better | **Agree for the light theme, disagree for dark** | Light: `home-empty.png` has a single bordered composer, a 3 x 2 grid and the example cards read clearly. `problem-answer.png` has a mint strip with a check icon, a sentence and a link, and the schematic is large with `V_in = 10 V` beside the battery. Dark: in `dark-problem.png` the strip stays pale mint with grey text at 2.26:1, and every schematic label is black on near-black (1.2:1), so the circuit has no readable values. Home thumbnails remain raw plots (see per-screen notes) |
| Studio canvas still floats over the palette and results in `studio-after-simulate.png` and `dark-studio.png`; the fixed-grid fix did not land | **Agree on the symptom, correct on the cause** | The grid did land. Two later rules override it (root cause above). The canvas is x 484 to 976, y 112 to 606. It sits in the middle column, so it does not touch the palette or inspector boxes; it covers the results drawer from y 296 to 606. The palette is clipped by the grid row and its own 220px cap, not by the canvas |
| Margin captions are clipped behind the canvas | **Agree, with a worse consequence** | `studio-after-simulate.png`: only "Gain margin (dB)" and the right half of "Phase crossover (rad/s)" are visible. The Phase margin and Gain crossover captions **and their values** are fully hidden, so the builder's "PID wcg about 0.051, PM about 99.8 degrees" cannot be verified from any capture. The "Infinite" caption is cut at x 484 |
| Step plot in dark mode is a white figure | **Agree** | `dark-studio.png`: the plot is a `#FFFFFF` figure at x 422 to 1097, y 472 to 775 on a `#121211` panel. The dark renderer exists in the repo (`artifacts/visual-goldens/dark/control/`), so the endpoint can be asked for it |
| Block labels are tiny at 64% zoom | **Agree** | Toolbar shows 64%. Block text is 12px, so it renders at about 7.7px (the "PID" kind label too). The cause is the fit logic, below |

### Why 64%

`FitViewOnChange.jsx` fits the block span to 80% of the pane width (`WIDTH_FILL = 0.8`) and clamps zoom only at 0.25. The pane is 492px wide because the inspector (280px) is always open and empty. The five blocks span about 611px at 100%, so the fit lands at 64%. Widening the pane and flooring the zoom fixes both (fix 2).

### Are the margins now plausible?

I cannot see the Phase margin or gain crossover values, so I judge only what is visible. Gain margin "Infinite" and phase crossover "No crossover in range" are **consistent** for a PID on a first or second order motor: the phase never reaches -180 degrees. This matches the `studio-r1/populated.png` answer for the same loop. The builder's PM 99.8 degrees at 0.051 rad/s is physically plausible (the integral term dominates at that frequency, so the PID phase is about -78 degrees and a light plant lag leaves L near -80 degrees). The sweep edge rejection works: no value sits at 1e-3 or 1e5. Still missing: the regression test (the same loop with and without an unconnected Gain k = 1 must give the same margins) and a capture that shows all four values.

---

## Status of round 2's 12 fixes

| # | Round 2 fix | Status | Evidence |
|---|---|---|---|
| 1 | Studio layout as a grid | **Not done in effect** | Rules, toolbar, palette search and results drawer exist, but stale rules still overlay the canvas (`studio-after-simulate.png`, `dark-studio.png`). Root cause and patch above |
| 2 | Margin values and copy | **Done** | "Infinite", "No crossover in range", sweep stated, edge rejection. Left: captions hidden, text KPIs at 28px wrap to two lines, the sweep reads "0.001 to 100000 rad/s" (use "10^-3 to 10^5 rad/s" or "0.001 to 100,000"), no regression test shown |
| 3 | Block diagram | **Partial** | Done: 96 x 56, no overlaps, no stray Gain, orthogonal feedback, plain signal labels in light, dot grid. Not done: legible text, zoom pill, inspector on selection (`studio-block-selected.png` is pixel-identical to `studio.png` above y 295, nothing is selected), shadows, human block names (`plant_first_order`) |
| 4 | Theme Studio, thumbnails, figures | **Partial** | Studio chrome now follows dark. Not done: Step plot (white), thumbnails (white tiles in `dark-home.png`), signal chips, arrowheads, schematic labels |
| 5 | Home tiles and composer | **Partial** | Done: 3 x 2 grid, single composer border, `Shortcut` shows "Ctrl", Continue and Agent captured. Not done: one frame (thumbs are 128px wide, left-aligned in 250px cards), unique correct images ("DC drive speed" shows the power dispatch plot; "Signals workout" shows a Bode plot), no embedded titles ("Nyquist - open-loop L(s)" is cropped mid-title), no `kbd` styling |
| 6 | Verification strip and stale | **Partial** | Strip restored with icon, tint and link. Stale dims the answer and adds a banner. Not done: strip does not change when stale, two filled "Run again" buttons, "Checked" tag missing, dark strip |
| 7 | Cmd+K | **Partial** | Groups, `kbd` hints, footer, correct 240px sidebar, placeholder. Missing: row icons, the Actions group has one row ("Toggle theme") rendered in grey like a disabled item, the Problems row is grey too |
| 8 | Problems list | **Partial** | Title Case chips with counts, Subject and Made by filters, hover actions (`problems-row-hover.png`), 8-row skeleton, quiet Recent on load. Not done: `/` hint inside the search, header on `--surface-subtle`, tags 12px sentence case, table full width, centred empty and error states |
| 9 | Recent row and chip | **Done** | Dot, title, status icon. No subject chip, no "Agent ready" chip. Remaining: identical titles in the list |
| 10 | Gallery, Library, Settings | **Partial** | Settings opens on Agents, five tabs captured, segmented Appearance. Not done: Library H1 still "Books", native controls, `commercial-byo`; Gallery still says "kernels", shows `power.swing_equal_area` ids and unaligned captions; About is raw markdown |
| 11 | Token and type corrections | **Partial** | `--text-muted` 4.97:1 live, subscripts in the schematic. Not done: `label` style for group headers and table heads, step text subscripts ("Vout from Vin, R1, R2"), Library checkbox border |
| 12 | Finish the schematic | **Done in light, broken in dark** | `problem-answer.png`: `V_in` at the battery, spaced labels, subscripts, ground visible. `dark-problem.png`: labels invisible |

Tally: 3 done (2, 9, 12 with the dark exception), 8 partial, 1 not done.

---

## Per-screen issues

### Studio (`studio.png`, `studio-after-simulate.png`, `studio-block-selected.png`, `studio-margins-no-crossover.png`, `dark-studio.png`)
- **Canvas, centre (all five):** a 492 x 494px white box floating over the results drawer. Cause above.
- **Palette, left column:** five rows (Step, Ramp, Sine, Gain, and a half-cut Sum) then a hard clip at y 295 with no scroll cue. 220px column is right; the 220px cap is wrong.
- **Inspector, right column, `studio-block-selected.png`:** still says "Select a block to tune parameters, then Simulate again." No block has the selected ring. The capture did not select anything; the builder's note ("select PID") is not supported by the image.
- **Results drawer, `studio.png`:** a 576px box reading "Run Simulate to see the step re..." twice (the margin hint and the stage hint), cut at the canvas edge.
- **Results drawer, `studio-after-simulate.png`:** margin KPIs "Infinite" and "...ossover in range" visible, middle two hidden. Tabs Step, Bode, Root locus fine. The Step plot is cropped at the bottom (no x axis, no time unit), and its y axis is labelled "Output" with no unit.
- **Block diagram, canvas centre:** 64% zoom, text about 7.7px. The wiring is good: ports on the block edges, orthogonal feedback from DC motor to the Sigma block, arrowheads, `r e u y` labels as plain text. Orange dot at the DC motor's bottom port is unexplained.
- **Block diagram, `studio-margins-no-crossover.png`:** blocks read "step", "plant_first_order", "Scope". A snake_case identifier fills the whole block width. Use "First-order plant". Zoom is 111% here and 64% in the PID capture, so fit is inconsistent.
- **`dark-studio.png`:** wires are white but arrowheads are black (invisible), signal labels `r e u y` sit in pale chips with light text, and the plot is white.

### Home (`home-empty.png`, `home-with-recent.png`, `home-scrolled-1280.png`, `home-scrolled-1440.png`, `dark-home.png`)
- **Composer, top:** one clear border, "Circuits" chip, hint, filled "Solve" disabled in a pale blue. Footer reads "Press Ctrl Enter to solve": platform-aware (pass) but with no `kbd` styling and no separator ("Ctrl+Enter").
- **Example grid:** 3 x 2 at 1280, 3 x 2 at 1440. Thumbnails are about 128 x 80px, left-aligned inside 250px cards, so each card has a dead right half. Tile 2 shows an embedded title at about 5px. Tile 4 ("DC drive speed") shows the power dispatch plot with "Gen 1/2/3" labels, which is wrong for a DC drive. Tile 5 ("Digital loop") is a cropped Nyquist plot: the title "Nyquist - open-loop L(s) = 10..." and the axis ticks are cut. Tile 6 ("Signals workout") is a Bode plot.
- **`home-scrolled-1280.png` is a dark-theme capture** (the filename says nothing about theme). It shows Continue with two identical cards ("Voltage divider · Vout", both "CHECKED") and an Agent section whose sentence is cut at the right edge ("...Claude Code. CLI") and says "in this repo", which is developer copy.
- **`home-scrolled-1440.png`:** content has about 60px padding each side (24px at 1280), so the padding changes with width. Pick one value (24px) and cap the content width instead.
- **`dark-home.png`:** thumbnails are white rectangles on `#1A1A18`.

### Problem (`problem-answer.png`, `problem-work-tab.png`, `problem-parameters-drawer.png`, `problem-parameters-stale.png`, `dark-problem.png`)
- **Answer card:** the best screen in the build. Subscripted `V_out`, 36px value, unit in secondary ink.
- **Strip:** pale mint, `--success` icon, sentence, "View engine output". No "Checked" tag.
- **Diagram tab:** full-width container, schematic fills about 60%, ground symbol sits right at the fold. No `V_out` marker across R2, which is the quantity the card reports.
- **Work tab:** four steps, author at the right in plain text. Step 2 still has a boxed chevron button under its subtitle instead of an end-of-row chevron, and the step text has no subscripts.
- **Parameters drawer:** units inside the field ("V", "kΩ"), labels above. Good.
- **Stale (`problem-parameters-stale.png`):** answer greys to 60%, drawer banner "Answer is stale after your edit." with a filled "Run again" that wraps to two lines. The top-bar "Run again" is also filled: two primary buttons. The green strip still says the answer matched, which contradicts the stale state.
- **Dark:** see the contrast numbers above. Dark theme also leaves two identical Recent rows.

### Problems (`problems-list.png`, `problems-row-hover.png`, `problems-loading.png`, `problems-error.png`, `problems-empty.png`, `sidebar-collapsed.png`)
- **Filter row:** "Press / to focus" is loose text to the left of the chips. Subject and Made by are native `<select>` controls at a different height from the 28px chips.
- **Table:** header and rows end at x 1150 while the search field ends at x 1255 (105px short). Tags "CIRCUITS" and "CHECKED" are 11px uppercase. Header row is not on `--surface-subtle`.
- **Row hover (dark):** three small icons (open, re-run, copy) appear at the right, beyond the end of the row rule (x 1150), with no labels or tooltips captured.
- **Loading:** 8 skeleton bars with no filter row. **Error and empty:** a bare sentence and one filled button on a blank page. No icon, no centring, no "Details".
- **Collapsed:** 56px rail is correct, no tooltip capture, no Recent dots.

### Cmd+K (`cmdk-open.png`, `cmdk-query.png`)
- Placeholder "Search or run a command", groups "GO TO", "PROBLEMS", "ACTIONS" in 11px caps, `G H` style chips, footer with a fade. Sidebar stays 240px.
- Rows have no icons. "Toggle theme" and the Problems row are grey, so they look disabled. The Actions group has one row. In `cmdk-query.png` the input has a heavy full blue 2px ring inside the dialog; use a bottom border only.

### Gallery and Library (`gallery.png`, `library.png`)
- **Gallery:** H1 "Visuals" under a "Gallery" top bar and nav item. Subtitle "Engine-bound figures. Numbers come from Arc kernels, not prompts." Captions show `power.swing_equal_area`, `power.agc_trace`, `power.dispatch_curve`. Image heights differ per card so titles sit at different y values (348, 374, 348). "GIF" is a white pill.
- **Library:** H1 "Books", then a single 600px form (native selects, a native "Choose File" control, `commercial-byo`, an enabled-looking checkbox) with a pale disabled "Ingest" at the fold. The one book row ("kuphaldt-dc CC-BY · 2 chunks") is unstyled. "chunks" is internal jargon.

### Settings (`settings-agents.png`, `settings-engines.png`, `settings-appearance.png`, `settings-data.png`, `settings-about.png`)
- **Tabs:** underline tabs, readable, active tab is clear. Content is a thin heading and a line of text with a rule below, then 450px of empty canvas.
- **Agents:** one code box, no copy button. **Engines:** four dots and sentences ("SPICE when ngspice is installed"), amber for MATLAB and Simulink "(optional)". **Appearance:** Light, Dark, System segmented control, System selected, no description. **Data:** "Problems are stored under ./runs in this workspace." **About:** the scorecard markdown printed raw in monospace, with backticks, `**` markers, "pass^k", a branch name (`cursor/frontier-execution-7a2f`) and a table that runs off the bottom. This is the worst-looking screen in the build.

### Focus (`focus-button.png`, `focus-composer.png`, `focus-tab.png`, `focus-table-row.png`, `focus-tile.png`)
- Button, composer and tile show a ring. Tab and table row show none. Four of the five captures are dark without saying so.

---

## Prioritised fix list (12, paste into the next build prompt)

1. **Fix the Studio layout at the source** (`studio.png`, `studio-after-simulate.png`, `dark-studio.png`).
   - Apply `round3/studio-fix/studio-layout.fix.patch` to `ui/src/control-studio/studio.css`. Delete the stale `.studio-canvas` block (lines 435 to 449), the `max-height` on `.studio-palette` (line 348) and `.studio-inspector` (line 813), and the card border and radius on the palette, inspector and results. Add `isolation: isolate; contain: layout paint` to `.studio-canvas`. Grid rows: `44px minmax(280px, 1fr) var(--studio-results-h)` with `--studio-results-h: clamp(200px, 36vh, 340px)`, `120px` when the section has `is-empty`.
   - Rename `.studio-results.empty` to `.is-empty` in the JSX and CSS (the global `.empty { max-width: 36rem }` clips it to 576px). Delete the duplicate "Run Simulate..." line.
   - Add `studio-layout.spec.ts` to CI. It must pass before any Studio capture is sent.
2. **Make block text legible** (`studio.png`).
   - Rule: block text never renders below 11px on screen. Rendered size is font-size times zoom. Set block name and parameter text to 13px (kind label too, or remove it when it repeats the name), PID block 168 x 56px, other blocks 96 x 56px. Fit view floors at 0.85 (13px x 0.85 = 11.05px): in `FitViewOnChange.jsx` use `WIDTH_FILL = 0.92` and `Math.max(newZoom, 0.85)` and cap at 1.25.
   - Give the canvas room: collapse the 280px inspector column to 0 until a block is selected, so the pane is 772px wide and fit lands near 100%. On selection, open it and centre the selected block.
   - Optional, for deliberate zoom-out: `font-size: max(13px, calc(11px / var(--studio-zoom)))` with `--studio-zoom` set from `onMove`. The spec asserts at least 10.9px at the fitted zoom.
   - Block names in human words ("Step", "Sum", "PID", "DC motor", "First-order plant", "Scope"), never identifiers.
3. **Make dark mode work in Studio and on the Problem page** (`dark-studio.png`, `dark-problem.png`, `dark-home.png`).
   - Checked strip uses tokens, not fixed mint: dark `--success-tint` about `#12261C`, text `--text-primary` (at least 7:1), icon `--success-text`.
   - Schematic labels and symbols use `currentColor` or `--text-primary` (they are `#000` today, 1.2:1).
   - Arrowheads: `.react-flow__arrowhead * { fill: var(--cs-text); stroke: var(--cs-text); }` (the `var()` in the marker `color` prop does not resolve, so they fall back to black). Signal labels `r e u y`: no chip, `--text-secondary`.
   - Step, Bode and Root locus: pass the theme to the plot endpoint and refetch on `data-theme` change (dark renders already exist under `artifacts/visual-goldens/dark/control/`).
4. **Show every margin value, and keep them honest** (`studio-after-simulate.png`).
   - All four captions and values visible. Textual results ("Infinite", "No crossover in range") use a 20px/28px KPI so they stay on one line; numeric ones stay at 28/32. Range copy "0.001 to 100,000 rad/s".
   - Add the regression test: PID (Kp 2, Ki 0.5, Kd 0.1) with the DC motor gives identical margins with and without an unconnected Gain k = 1.
   - Capture the loop with a finite crossover (for example a plain integrator plus first-order plant) so a number is shown at least once.
5. **Fix the Home thumbnails properly** (`home-empty.png`, `dark-home.png`).
   - One frame per card: full card width, 112px high, `--surface-subtle`, 12px padding, `object-fit: contain`, centred. No embedded titles, no cropped axes, ticks at least 11px at the thumbnail scale (draw simple figures, not downscaled gallery plots).
   - Six correct images: DC drive speed shows speed against torque, Digital loop a full unit-circle pole plot, Signals workout a spectrum or a filter response. Thumbnails render from tokens so they follow dark.
   - Continue cards: two rows that differ ("Voltage divider · Vout" twice is a data problem). Append the time ("Today 17:12") or number them. Agent section: "Connect your coding agent" plus the command in a `kbd` block, no "in this repo".
6. **Make the stale state coherent** (`problem-parameters-stale.png`).
   - When stale, the strip becomes `--warning-tint` with a 16px `alert-triangle`: "Out of date. Values changed after the last check. Run again to re-check." The answer drops to 60%. Only the top-bar "Run again" is filled; the drawer banner action is a text link ("Run again") on one line.
   - Add the "Checked" tag (22px, 12px/500, `--success-tint`) to the passing strip.
7. **Fix Settings About and Engines** (`settings-about.png`, `settings-engines.png`).
   - About: "Arc 0.1" and a four-row table (Check, Result, Status) from the scorecard, no branch name, no `pass^k`, no backticks, collapsed "Details" disclosure for the rest.
   - Engines: table with "Available" or "Not installed" 22px tags; remove the amber "(optional)" rows or move them under "Optional".
   - Agents: add a copy button to the command box. Appearance: one-line description per option.
8. **Finish Problems** (`problems-list.png`, `problems-error.png`, `problems-empty.png`).
   - Table spans the full 1044px content width. Header 36px on `--surface-subtle`, `label` style. Tags 12px/500 sentence case ("Circuits", "Checked"). Put `/` in a `kbd` inside the search input and delete "Press / to focus". Native selects become 28px styled menus.
   - Empty: centred, 64px top padding, 16px icon, title "No problems yet" (20px), line "Try an example to see Arc check an answer.", one secondary "Try an example". Error: icon, "Problems did not load", "Try again" secondary, "Details" disclosure. Loading includes the filter row.
   - Row hover icons get tooltips: "Open", "Run again", "Duplicate".
9. **Finish Cmd+K and shortcuts** (`cmdk-open.png`, `home-empty.png`).
   - 16px Lucide icon on every row. Actions group: New problem, Run again (Ctrl+Enter), Open in Studio, Toggle sidebar (Ctrl+B), Toggle theme, Connect an agent. Normal ink on all rows (grey only for disabled). Input: bottom border only, no full blue ring.
   - `<Shortcut>` renders `<kbd>` per key with a "+" between: "Press `Ctrl` `Enter` to solve" on Windows and Linux, "⌘ Enter" on macOS.
10. **Rebuild Gallery and Library** (`gallery.png`, `library.png`).
    - H1 "Gallery" and "Library". Gallery subtitle "Figures checked by the engines." Captions are the title only (no `power.swing_equal_area`). Fixed 16:10 image frame so titles align. "GIF" becomes a neutral 22px tag.
    - Library: a sources table (Name, Kind, Subject, Used in) with search and "Add a source", which opens a 480px dialog. Styled 36px selects, a drop zone, labels "Textbook" and "Circuits" instead of `commercial-byo`. Content centred at 960px.
11. **Type and detail pass** (everywhere).
    - Group labels, table heads, eyebrows: one `label` style (11px, 600, uppercase, `--text-secondary`); tags 12px sentence case.
    - Work step 2: chevron at the row end instead of a boxed button; step text with subscripts ("V<sub>out</sub> from V<sub>in</sub>, R<sub>1</sub>, R<sub>2</sub>"). Authors as 22px tags.
    - Schematic: add a V<sub>out</sub> marker across R2 and keep the ground symbol 24px above the fold.
    - Block shadows off (`box-shadow: none`; 1px `--border-strong`). Zoom pill bottom-left of the canvas (32px, `--elevation-1`).
12. **Fix the focus states and captures** (`focus-tab.png`, `focus-table-row.png`).
    - Tabs and table rows get `:focus-visible { outline: 2px solid var(--accent-500); outline-offset: -2px; }`. Capture with real Tab key presses, not `.focus()`.
    - Name every capture with its theme (`-light` or `-dark`). Four focus captures, `home-scrolled-1280` and `problems-row-hover` are dark today and say nothing.

---

## Capture checklist for round 4

Each capture needs its filename, theme suffix and the exact action. Light theme unless stated.

- `studio-layout-before-simulate-light.png` and `studio-layout-after-simulate-light.png` at 1280 x 800, plus the same at 1440 x 900. Attach the `studio-layout.spec.ts` result (all green) and `getBoundingClientRect()` values for canvas, palette, inspector, results.
- `studio-block-selected-light.png`: click the PID block with the mouse. Inspector populated (name, Kp, Ki, Kd with units), selected ring on the block, no other block selected.
- `studio-fit-light.png`: fit zoom shown in the toolbar (at least 85%), and a text-size report: the smallest block text size in rendered px (at least 11).
- `studio-margins-all-four-light.png`: all four captions and values visible for PID on the DC motor. `studio-margins-no-crossover-light.png`: textual KPI on one line. `studio-margins-finite-light.png`: a case with numbers in every card.
- `dark-studio-before-simulate.png` and `dark-studio-after-simulate.png`: themed plot, visible arrowheads, readable signal labels.
- `dark-problem-answer.png` with the Diagram tab: readable labels, themed strip. `dark-home.png` scrolled to show all six thumbnails, Continue and Agent. `dark-problem-stale.png`.
- `problem-parameters-stale-light.png`: amber strip, one filled button.
- `home-empty-light.png` at 1280 and 1440 with all six tiles visible (scroll if needed) and the composer footer with `kbd` keys. A macOS UA capture or a `<Shortcut>` unit test for the "⌘" variant.
- `cmdk-open-light.png` with the Actions group visible and icons, sidebar width asserted at 240 after `transitionend`. `cmdk-query-light.png`.
- Focus, by pressing Tab from a known start: `focus-tab-light.png`, `focus-table-row-light.png`, `focus-button-light.png`, `focus-tile-light.png`, `focus-composer-light.png`, plus one dark.
- Problems: list at full width, hover with tooltip, loading with filter row, empty (centred), error with Details. `sidebar-collapsed-light.png` with a tooltip showing.
- Gallery with aligned captions and no ids, Library with the sources table and the Add dialog open, all five Settings tabs including the new About and Engines.
- `sidebar-measurements.json`: keep expanded 240, collapsed 56, Cmd+K open 240, and add Studio at 1280 and 1440.
- A `md5.txt` where no two captures that should differ are identical (round 3: `studio.png` and `studio-block-selected.png` differ by nothing visible).

Files reviewed (35): `cmdk-open`, `cmdk-query`, `dark-home`, `dark-problem`, `dark-studio`, `focus-button`, `focus-composer`, `focus-tab`, `focus-table-row`, `focus-tile`, `gallery`, `home-empty`, `home-scrolled-1280`, `home-scrolled-1440`, `home-with-recent`, `library`, `problem-answer`, `problem-parameters-drawer`, `problem-parameters-stale`, `problem-work-tab`, `problems-empty`, `problems-error`, `problems-list`, `problems-loading`, `problems-row-hover`, `settings-about`, `settings-agents`, `settings-appearance`, `settings-data`, `settings-engines`, `sidebar-collapsed`, `studio-after-simulate`, `studio-block-selected`, `studio-margins-no-crossover`, `studio`.
