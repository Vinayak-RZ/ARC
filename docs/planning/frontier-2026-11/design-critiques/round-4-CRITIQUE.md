# Round 4 critique (Design lead, 13 Nov 2026)

Build: PR #51, commit `610a558` on `cursor/arc-ui-polish-ad61`. I opened all 35 PNGs in `round4/` plus `NOTES.md`, `MY_NOTES.md`, `md5.txt` and `list.txt` (the folder holds 39 files, not 37, and there is no `sidebar-measurements.json` this round). I compared every capture's md5 with round 3, sampled native pixels, and read the Studio source at `610a558` with `git show` (read-only, nothing edited or pushed). Coordinates are native pixels unless I say "scaled".

**Total: 33 / 50 (round 1: 25, round 2: 30, round 3: 32, so +1).** The builder's self-report is accurate: it finished Studio layout, block legibility and part of dark mode and Home, and deferred everything else. Six captures are byte-identical to round 3 (`cmdk-open`, `cmdk-query`, `problems-empty`, `problems-error`, `problems-list`, `sidebar-collapsed`), so nothing in those areas moved.

The Studio overlay is fixed, which is the largest single improvement in four rounds. The score barely moves because eight of twelve fixes were not started, and the work that landed exposed three new Studio defects (wire off the canvas, a plot you cannot read, a selection that does not stick).

---

## Measurements you asked for

**No panel overlaps, before and after Simulate: confirmed in the images.**

| Capture | Canvas | Results drawer | Palette | Verdict |
|---|---|---|---|---|
| `studio-layout-before-simulate-light.png` (1280) | x 483 to 1255, y 111 to 656 | y 656 to 775, one line of copy, full width (was 576px wide) | x 272 to 483, full height | No intersection |
| `studio-layout-after-simulate-light.png` (1280) | x 483 to 1255, y 111 to 488 | y 488 to 775, margins, tabs, plot | full height, clipped by scroll | No intersection |
| `...-1440-light.png` pair (1440 x 900) | same grid, taller | same | same | No intersection |

The canvas is 772px wide (palette 220 plus a 0px inspector, as designed), the toolbar sits above all three, and the drawer's top border runs the full width. Margin captions are all visible. This matches the layout spec result (3/3). **But the spec is green while the picture is wrong**: it measures panel boxes, not what is drawn inside the canvas, so it cannot see the clipped wire. See the next section.

**Sidebar** (border sampled at y = 700): 239 (240px) in 34 of 35 captures including `-1440`, 55 (56px) in `sidebar-collapsed-light.png`. **Pass.** No JSON was supplied, so I could not check Cmd+K or Studio widths against the test's own numbers.

**Input borders:** `#8C8C87`, 3.38:1 on white (Problems search sampled). **Pass.**

**Dark-theme contrast now measured** (from `focus-tab-light.png`, which is actually dark, see captures below):
- Checked strip body text `#F4F4F3` on `#12261C`: **14.46:1** (was 2.26:1). Fixed.
- "View engine output" link `#1D47A3` on `#12261C`: **1.88:1.** Fails. `--accent-700` was not given a dark value.
- "Checked" word `#2F9E6A`: 4.71:1 in dark, **3.01:1 in light** on the mint strip. Fails in light at 12px.

---

## EE Project's points, verified

| Point | Verdict | Evidence and cause |
|---|---|---|
| Panels no longer overlap | **Agree** | Table above |
| After Simulate the feedback wire runs off the bottom of the canvas | **Agree, and I found the cause** | Next section |
| Step plot is a tiny, unthemed PNG | **Agree** | Section "Step plot" |
| Step response climbs and never settles | **The presentation is wrong; the shape is consistent with the margins** | Section "Settling" |
| `studio-block-selected` still shows no selection | **Agree, and the capture is the same picture as `before-simulate`** | Section "Selection" |
| Dark capture is thin, only `home-dark` | **Agree, and worse than it looks** | Section "Dark captures" |

---

## Feedback wire off the canvas: cause and fix

**What the images show.** `studio-layout-after-simulate-light.png`: the canvas ends at y 488 (native) and the two vertical legs of the feedback wire, at x 689 and x 1016, run into that edge and stop. The horizontal return and the arrowhead into the sum block are never drawn. Same at 1440 (`...-1440-light.png`). Before Simulate the whole loop is visible (`before-simulate`), with the return at y 499 of a canvas ending at 656.

**Cause, from `610a558`:**
1. **`FitViewOnChange.jsx` fits once and never again on resize.** It runs on `revision`, `nodeCount` and `agentBump` and at 100, 600 and 1400 ms. Simulate grows the results drawer, so the canvas drops from 545px to 377px tall after the fit has finished. The blocks stay where they were (centred in the old 545px box, so now 63px low) and the wire falls off the new bottom edge.
2. **It measures only `.react-flow__node .studio-block`.** The feedback path (`edges.jsx`: `midY = max(sourceY, targetY) + 72`) hangs 72 flow units below the lowest block, and it is not part of the bounds. Even with a correct resize, the fit would centre the blocks and ignore the wire.
3. **It fits width only.** `WIDTH_FILL = 0.92` is applied to the horizontal span, so height is never checked.
4. **The toolbar's Fit button uses `fitView({ padding: 0.2 })` on nodes only**, so it has the same blind spot.

**Fix.** Replace `FitViewOnChange.jsx` with a fit that uses what is actually drawn, and re-runs when the canvas is resized:

```jsx
import { useCallback, useEffect } from "react";
import { useReactFlow } from "@xyflow/react";

const MIN_ZOOM = 0.85;   // 13px block text x 0.85 = 11.05px, the on-screen floor
const MAX_ZOOM = 1.25;
const PAD = 24;          // px between drawn content and the canvas edge

/** Union of blocks, wires, arrowheads and tap dots, in flow coordinates. */
function contentBounds(screenToFlowPosition) {
  const rects = [...document.querySelectorAll(
    ".studio-canvas .studio-block, .studio-canvas .react-flow__edge-path, .studio-canvas .react-flow__arrowhead, .studio-canvas .react-flow__edge circle",
  )].map((el) => el.getBoundingClientRect()).filter((r) => r.width || r.height);
  if (!rects.length) return null;
  const a = screenToFlowPosition({ x: Math.min(...rects.map((r) => r.left)),  y: Math.min(...rects.map((r) => r.top)) });
  const b = screenToFlowPosition({ x: Math.max(...rects.map((r) => r.right)), y: Math.max(...rects.map((r) => r.bottom)) });
  return { x: a.x, y: a.y, w: b.x - a.x, h: b.y - a.y };
}

export function useFitContent() {
  const { setViewport, screenToFlowPosition } = useReactFlow();
  return useCallback((duration = 0) => {
    const pane = document.querySelector(".studio-canvas")?.getBoundingClientRect();
    const c = pane && contentBounds(screenToFlowPosition);
    if (!pane || !c) return;
    const zoom = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM,
      Math.min((pane.width - 2 * PAD) / c.w, (pane.height - 2 * PAD) / c.h)));
    setViewport({
      zoom,
      x: pane.width / 2 - (c.x + c.w / 2) * zoom,
      y: pane.height / 2 - (c.y + c.h / 2) * zoom,
    }, { duration });
  }, [setViewport, screenToFlowPosition]);
}

export function FitViewOnChange({ revision, nodeCount, agentBump = 0, fitRef }) {
  const fit = useFitContent();
  useEffect(() => { if (fitRef) fitRef.current = fit; }, [fit, fitRef]);   // the toolbar Fit button calls this too
  useEffect(() => {
    if (nodeCount < 1) return undefined;
    const ts = [100, 600, 1400].map((ms) => setTimeout(() => fit(ms === 100 ? 180 : 0), ms));
    return () => ts.forEach(clearTimeout);
  }, [revision, nodeCount, agentBump, fit]);
  useEffect(() => {                                    // the missing piece: refit when the canvas changes size
    const pane = document.querySelector(".studio-canvas");
    if (!pane) return undefined;
    let t;
    const ro = new ResizeObserver(() => { clearTimeout(t); t = setTimeout(() => fit(0), 120); });
    ro.observe(pane);
    return () => { ro.disconnect(); clearTimeout(t); };
  }, [fit]);
  return null;
}
```

Two small companions:
- `edges.jsx`: `const drop = 40;` (was 72). The return path only needs to clear the block by about 32px plus the tap dot.
- `ControlStudio.jsx`: `translateExtent` on `<ReactFlow>` set to the content bounds plus 80px, so the user can pan but not lose the loop; and `fitRef.current` (the Fit button) comes from the hook above, not `fitView`.

**Playwright assertion that every edge path sits inside the canvas:** `round4/studio-fix/studio-wire-selection.spec.ts`, helper `contentOutsideCanvas`. It reads `getBoundingClientRect()` of every `.react-flow__edge-path`, arrowhead, tap dot and `.studio-block`, and fails if any leaves the canvas rect inset by 8px. It runs before Simulate, after Simulate, after selecting a block and after a pure viewport resize, at 1280 x 800 and 1440 x 900. I checked the helper on a static page: a path that ends 50px below the canvas is reported, a block inside is not. The existing layout spec stays; it checks the panels, this one checks what is drawn.

**Two more defects in the same canvas** (`studio-layout-before-simulate-light.png`, `studio-margins-finite-light.png`):
- PID to DC motor has about 8px of gap (PID ends x 761, DC motor starts x 769, scaled), so the `u` wire and its arrowhead are not visible; only a stray `u` label and a left port. Set the layout gap to 48px between every pair of blocks. The 168px PID block must not eat the gap.
- "First-order plant" wraps to two lines in a 56px block and the second line ("plant") is cut by the bottom edge and collides with the bottom port. Allow two lines at 13px/16px inside a 64px block, or shorten to "1st-order plant" (the palette already uses that wording, so the two disagree). Pick one name and use it in both places.

---

## Step plot

**What the images show.** `studio-layout-after-simulate-light.png` and `-1440`: a matplotlib PNG about 146 x 110px, centred in a 950 x 110px stage, with a white face on the grey stage. Title, ticks and axis labels are about 3px. It is not themed, not interactive and has no annotations. Cause: the stage is only 110px tall (the 288px drawer minus the margin table and tabs), and `object-fit: contain` shrinks a 4:3 picture to that height.

**Specification (replace the `<img>` with a client chart):**
- **Renderer:** a client chart drawn from tokens, not a PNG. Hand-rolled SVG or uPlot. The API returns data, not a picture: `{ t: number[], y: number[], setpoint: 1, unit: "rad/s", metrics: { settled: bool, settling_time_s, overshoot_pct, rise_time_s, final_value, window_s } }`. It must repaint on `data-theme` change with no refetch. Drop the `?theme=` PNG route for this chart (keep it for Gallery and exports).
- **Size:** fills the drawer stage, 100% width and at least 220px high. Make the drawer two columns: left 360px (tabs, then the four margins as a 2 x 2 grid), right the chart. The drawer is `clamp(240px, 40vh, 380px)` tall, so the stage is at least 190px at 800px high. Remove `resize: vertical` (it shows a grabber that does nothing in a grid row), or make a real splitter.
- **Axes:** x "Time (s)", y "Speed (rad/s)" for the DC motor, otherwise "Output". Never just "Output" when the unit is known. 5 to 6 ticks per axis, labels 12px tabular, one decimal rule per axis. Axis lines 1px `--border-strong`; gridlines 1px `--border`, horizontal only.
- **Line:** 2px `--accent-500`. Setpoint: 1px dashed `--text-secondary`, labelled "Setpoint 1" at the right end. No chart title (the tab says "Step").
- **Annotations, only when they exist:** a shaded 2% band (`--accent-50`) around the setpoint with a dashed vertical line and the label "Settled at 3.2 s"; a 6px marker at the peak with "Overshoot 12%" when overshoot is above 1%; "Rise time 0.4 s" as a bracket on the 10 to 90% span. Labels are 12px in `--text-primary` on a `--surface` pill so they never sit on the line.
- **Cursor:** vertical crosshair with a readout "t = 4.2 s, 0.31 rad/s". Plot, ticks and annotations are keyboard reachable (arrow keys move the cursor). Container has `role="img"` and an `aria-label` that states the headline ("Closed-loop step response, rises to 0.45 rad/s at 10 s, not settled").
- **Dark:** plot background transparent on `--surface`, grid `--border`, text `--text-secondary`. No white figure.
- **Playwright:** no `<img>` in `.studio-results-stage`; one `svg[role=img]` with width at least 90% of the stage and height at least 200px; the smallest `<text>` font size is at least 11px; axis labels contain a unit in parentheses.

## Settling: presentation only

**What I can say from the images.** The curve in `...-1440-light.png` jumps to about 0.2 in 1.5 s, then climbs almost linearly to about 0.45 at 10 s. I am not checking the engine, but the curve and the margin cards agree with each other, which narrows EE Project's question:
- A fast step to about 0.2 followed by a slow tail is what a PI loop does when the plant's DC gain is low. With Kp = 2, 2G0 / (1 + 2G0) = 0.2 gives a plant DC gain G0 of about 0.125.
- The integral tail then has a time constant of about (1 + Kp G0) / (Ki G0) = 1.25 / 0.0625 = 20 s. The Gain crossover card says 0.05093 rad/s, so 1/ωcg is about 19.6 s. These match.
- A response of 0.2 + 0.8 (1 - e^(-t/20)) reads 0.51 at 10 s against about 0.45 on the plot. Close enough for a PID with a derivative term.
- So this is a coherent slow loop, not an open-loop ramp. What is worth checking is whether a DC motor with a plant gain near 0.125 is the intended model. A speed loop that slow is unusual.

**The UI problem is the 10 s window.** `simulate.py` defaults `t_final = 10.0`. With a 20 s time constant the window can never show the settling, and the plot implies a result it does not have. Rules:
1. **Say it.** When the response has not settled inside the window, show an amber pill on the chart, "Not settled within 10 s", and set the step stats to "Not settled" (never a number). Add the line "Still rising at 10 s: 0.45 of a setpoint of 1." Use "Settled" only when the last 10% of the window stays inside the 2% band.
2. **Offer the fix.** A segmented control "10 s | 30 s | 100 s | Auto" on the chart header. Auto picks `t_final = clamp(6 / ωcg, 10, 600)` s when a gain crossover exists (here about 118 s) and shows the value ("Window 118 s").
3. **Show the window** in the x-axis label whenever it is not the default: "Time (s), window 118 s".
4. **Never extrapolate.** Do not draw or print a predicted final value. If the engine can prove the final value (type 1 or higher loop, unit setpoint), show "Final value 1 (steady-state error 0)" as engine output with its source tag.

---

## Selection: why `studio-block-selected-light.png` shows nothing

**The image.** It is `studio-layout-before-simulate-light.png` with 9 pixels different. There is no outline on PID, no inspector, the canvas is still 772px wide.

**Cause, from `610a558`:**
- The capture script (`capture_ux_review_round.py`, lines 223 to 238) clicks the PID block, waits for `.studio.has-selection` (passes at once), waits 700ms and takes the shot. So the click did select.
- Selection lives on the node objects (`n.selected`), set by `onNodeClick`. But `ControlStudio.jsx` lines 235 to 245 rebuild the entire node list from `session.diagram` with `diagramToFlow()` whenever `validation`, `session.diagram`, `session.presence`, `highlight` or `blockIssues` change, and `paint()` (line 154) does the same on every SSE `revision` message. `diagramToFlow` (`utils.js`) never sets `selected`, so every rebuild silently deselects.
- Validation and the SSE refresh resolve a few hundred milliseconds after load and after a click. The class check passes in that window, the repaint then wipes the selection, and the 700ms wait lets the screenshot see the cleared state. This is a race, so I have not reproduced it live; it is the one place in the file that can produce exactly this picture, and the fix is safe either way.

**Fix.** Keep the selected id in state and re-apply it on every rebuild:

```jsx
const [selectedId, setSelectedId] = useState(null);
const selectedIdRef = useRef(null);
selectedIdRef.current = selectedId;
const withSelection = (list) => list.map((n) => ({ ...n, selected: n.id === selectedIdRef.current }));

// in paint(): setNodes(withSelection(flow.nodes));
// in the rebuild effect (line 243): setNodes(withSelection(flow.nodes));
const selected = useMemo(() => nodes.find((n) => n.id === selectedId) ?? null, [nodes, selectedId]);

<ReactFlow
  onNodeClick={(_, node) => setSelectedId(node.id)}
  onPaneClick={() => setSelectedId(null)}
  onKeyDown={(e) => e.key === "Escape" && setSelectedId(null)}
  ...
/>
```
Also drop `highlight` (a fresh object each paint) from the rebuild effect's dependency list; key it on `highlight.ids` size instead.

**Selected-state spec:**
- **Block:** `outline: 2px solid var(--accent-500); outline-offset: 2px; border-color: var(--accent-500); box-shadow: none`. Today it is a 2px pale tint (`--accent-50`) ring, which is not an outline and is invisible at this zoom.
- **Handles:** every port on the selected block grows from 10px to 12px, filled `--accent-500` with a 2px `--surface` ring. Other blocks keep 10px outline-only ports. Connection drag still works from any port.
- **Inspector:** opens within 160ms (opacity 0 to 1, 8px slide, `cubic-bezier(0.22, 1, 0.36, 1)`), heading is the block name at 13px/600 ("PID"), a type tag, then 36px fields with units (Kp, Ki, Kd), Apply on blur. Closes on Escape or pane click; focus returns to the block.
- **Layout consequence:** a 280px inspector column shrinks the canvas from 772px to 492px, and a 700px loop cannot fit there at the 0.85 zoom floor. Make the inspector a floating panel inside the canvas (right edge, 280px wide, `--elevation-2`, the one place a shadow is correct), keep the canvas at 772px, and after selecting pan the diagram only if the selected block sits under the panel.
- **Capture step:** click the block with the mouse (not `.focus()`), then `waitForTimeout(800)`, then assert `.studio-block.is-selected` count is 1 and the outline computed style, then screenshot. `studio-wire-selection.spec.ts` contains this test, and it also checks that the selection survives a Simulate repaint.

---

## Dark captures

Round 4 supplies one deliberate dark capture (`home-dark.png`). Four more `-light` files are actually dark: `focus-tab-light.png`, `focus-table-row-light.png`, `focus-tile-light.png`, `problems-row-hover-light.png`, and `home-scrolled-1280-light.png` too. The theme leaked from an earlier capture and was never reset, so every theme label in the folder is unreliable. Round 5 needs a full dark set, taken after an explicit `data-theme` reset (list in the checklist).

What the leaked dark pages already tell me: dark strip text is fixed (14.46:1), the link is not (1.88:1), Home thumbnails are still white rectangles on `#1A1A18` (`home-dark.png`), and the Problem page, Problems list and Home look right otherwise.

---

## Scores

| # | Criterion | R1 | R2 | R3 | R4 | One-line reason |
|---|---|---|---|---|---|---|
| 1 | Answer-first hierarchy | 3 | 4 | 4 | 4 | Answer card is strong. Strip gained a "Checked" word at 3.01:1 in light, and a stale answer still shows the green strip |
| 2 | Layout, spacing, alignment | 2 | 3 | 3 | 4 | Studio is one grid with no overlaps, 772px canvas, full-width drawer. Problems table is still 105px short of the search field, Library is a pinned column, PID to motor gap is 8px |
| 3 | Typography | 3 | 3 | 3 | 3 | Block text is now 13px at 115 to 125% zoom, which is a real fix. The plot text is about 3px, tags are still 11px uppercase, About is monospace markdown |
| 4 | Colour and accent discipline | 3 | 3 | 3 | 3 | Dark strip text fixed (14.46:1). Dark link 1.88:1, Home thumbnails white in dark, two filled blue buttons when stale |
| 5 | Surfaces, borders, elevation | 3 | 3 | 3 | 4 | Studio is now flush hairline panels in one workspace. Blocks keep a soft shadow, Problems and Library unchanged |
| 6 | States and interaction | 3 | 4 | 4 | 3 | Selection is wiped by a repaint (cause above), stale state unchanged, focus captures mislabelled, rest unchanged. Down one: a state is now known broken |
| 7 | Plots | 2 | 2 | 2 | 2 | Studio plot is 146 x 110px with 3px text. Gallery and Home thumbnails are still raw PNGs, one duplicated |
| 8 | Schematics and block diagrams | 2 | 3 | 3 | 3 | Light schematic is a 4. Blocks are legible, orthogonal, no overlaps, but the feedback wire leaves the canvas after Simulate, one wire is hidden by an 8px gap and one label overflows its block |
| 9 | Trust and copy | 2 | 3 | 3 | 3 | All four margins now visible and consistent with the step shape. But the captions give the wrong reason, the step plot implies a result at 10 s, and About still leaks a branch name |
| 10 | Shell, navigation, consistency | 3 | 4 | 4 | 4 | 240 and 56 exact. Theme labels in the capture set are wrong, Library H1 still "Books" |
| | **Total** | **25** | **30** | **32** | **33 / 50** | Still below 40: iterate |

### A trust bug in the margin captions (new, `studio-margins-no-crossover-light.png`, `studio-layout-after-simulate-light.png`)

The numbers are good. For the PID loop, 0.05093 rad/s and 99.8 degrees are consistent with the step curve (above), and in `studio-margins-finite-light.png` the First-order plant gives 9.95 rad/s and 95.7 degrees: 180 - atan(9.95) = 95.7, so that pair is internally exact. The explanatory lines are not:
- Gain margin "Infinite because open-loop gain stays above 0 dB in the analyzed band" is the wrong reason. A gain margin is infinite when the phase never reaches -180 degrees. Replace with "Phase never reaches -180° from 0.001 to 100,000 rad/s."
- Phase crossover "No crossover in range. Gain stays above 0 dB ..." has the same swap. It should read "Phase stays above -180° from 0.001 to 100,000 rad/s."
- In the "Low gain" capture the gain crossover card says "Gain stays above 0 dB". The DC gain there is far below 1 (round 3's plot topped out near 0.0008), so it should say **below**. Pick "above" or "below" from the sign of the gain at the sweep ends.
- Phase margin "Infinite ... at the gain crossover" in a loop with "No crossover in range" refers to a crossover that does not exist. Use "Not defined" with "No gain crossover in range."

---

## Status of round 3's 12 fixes (verified in the images)

| # | Round 3 fix | Status | Evidence |
|---|---|---|---|
| 1 | Studio layout at the source | **Done** | No box intersects before or after Simulate (1280 and 1440). Residual: palette scrolls with no cue (cut at "Delay (Pade)"), a dead `resize` grabber on the drawer |
| 2 | Legible block text | **Done, two defects** | 13px text at 115 to 125%, human names, no inspector column until selection, PID 168px. Defects: the wire and label problems above, "1st-order plant" in the palette against "First-order plant" on the block |
| 3 | Dark mode | **Partial** | Strip text fixed, but link 1.88:1, thumbnails white, and Studio, schematic, arrowheads and plot are not captured in dark, so unverified |
| 4 | Margins | **Partial** | All four values and captions visible, textual KPI on one line, range reads "0.001 to 100,000 rad/s". The explanatory copy is wrong (above), the regression test was not shown |
| 5 | Home thumbnails | **Partial** | 112px frame, contained, centred. Still raw matplotlib PNGs with embedded titles at about 5px. "DC drive speed" now shows the same first-order step plot as "First-order step"; "Signals workout" shows a power phasor diagram; Continue still shows two identical cards; Agent copy is unchanged |
| 6 | Stale state and Checked tag | **Partial** | "Checked" word added (plain green text, 3.01:1 in light). Stale state is unchanged: green strip, two filled "Run again" buttons, banner wraps |
| 7 | Settings About and Engines | **Not done** | `settings-about-light.png` is the same raw markdown with a branch name; Engines still bullet sentences |
| 8 | Problems | **Not done** | `problems-list`, `problems-empty`, `problems-error` are byte-identical to round 3 |
| 9 | Cmd+K and shortcuts | **Not done** | `cmdk-open` and `cmdk-query` are byte-identical to round 3: no icons, one Actions row in grey, heavy blue input ring, plain "Ctrl Enter" text |
| 10 | Gallery and Library | **Not done** | Gallery still "Visuals" with recipe ids and "kernels"; Library still "Books" with native controls and `commercial-byo` |
| 11 | Type and detail pass | **Not done** | Boxed chevron on Work step 2, uppercase 11px tags, no V<sub>out</sub> marker, block shadows |
| 12 | Focus states | **Partial** | A white 2px ring shows on the skip link and the Activity tab (dark theme). `focus-tile` shows no focus on any element, `focus-tab` is the skip link, `focus-table-row` is a tab, and four captures are dark under a `-light` name |

Tally: 2 done, 5 partial, 5 not done. The builder's own tally (items 3 and 5 to 12 partial or not done) matches mine except that I count item 4 as partial and item 12 as partial, and I downgrade nothing it called done.

---

## Per-screen issues

### Studio (`studio-layout-before-simulate-light.png`, `studio-layout-after-simulate-light.png`, `...-1440-light.png` pair, `studio-block-selected-light.png`, `studio-margins-finite-light.png`, `studio-margins-no-crossover-light.png`)
- **Canvas, bottom:** after Simulate the feedback wire is cut at the canvas edge (cause and fix above).
- **Canvas, between PID and DC motor:** no visible `u` wire or arrowhead, only a `u` label overlapping the PID corner.
- **Canvas, DC motor and Scope:** `y` wire is fine. The tap dot (orange) at the DC motor's bottom port still has no legend.
- **Canvas, `studio-margins-finite-light.png`:** the first block ("First-order plant") overflows its box; the `e` label between the sum block and the plant is missing, and the feedback wire is cut off again after Simulate.
- **Palette, left:** 16 rows, no scroll cue, cut mid-row after Simulate; a 32px search field is fine. The icon for "Transfer Fcn", "Saturation", "Delay (Pade)", "Scope", "DC motor", "1st-order plant" is the same "f" glyph, so six rows look identical. Use distinct 16px Lucide icons.
- **Results drawer, left:** four margins in one row with captions, values and meta lines. Text KPI ("No crossover in range") at 20px on one line. Wrong explanatory copy (above).
- **Results drawer, right:** the tiny plot (146 x 110px). Tabs "Step | Bode | Root locus" sit above it, fine. A `resize` grabber in the bottom-right corner does nothing.
- **Toolbar:** Fit, zoom value ("115%", "125%"), Undo, Redo, Simulate; one filled button. The zoom reads 115% in one capture and 125% in another for the same loop because fit changes with width.
- **`studio-block-selected-light.png`:** identical to the before capture. No outline, no inspector.

### Home (`home-empty-light.png`, `home-with-recent-light.png`, `home-scrolled-1280-light.png`, `home-scrolled-1440-light.png`, `home-dark.png`)
- **Example cards:** 112px grey frame with a centred plot. The plots are still raw, tiny and titled ("Unity-feedback step response" at about 5px). Tile 4 and tile 2 show the same figure. Tile 5 is a thin Nyquist strip with its title cut. Tile 6 is a power phasor diagram labelled "Signals workout".
- **`home-scrolled-1280-light.png` is dark.** It shows Continue with two identical "Voltage divider · Vout" cards and an Agent line that is cut ("...Claude Code. CLI") and says "in this repo".
- **`home-dark.png`:** thumbnails are white rectangles on dark.
- **Composer:** one border, hint "Press Ctrl Enter to solve" in plain text, no `kbd`.

### Problem (`problem-answer-light.png`, `problem-work-tab-light.png`, `problem-parameters-drawer-light.png`, `problem-parameters-stale-light.png`)
- **Strip:** "Checked" is a smaller green word floating above the baseline of the sentence, not a tag. Contrast 3.01:1.
- **Stale:** unchanged from round 3 (answer greys, strip stays green, two filled "Run again").
- **Work tab, step 2:** boxed chevron under the subtitle, step text without subscripts.
- **Diagram tab:** schematic as in round 3, no V<sub>out</sub> marker.

### Problems, Cmd+K, collapsed rail (`problems-list-light.png`, `problems-empty-light.png`, `problems-error-light.png`, `problems-loading-light.png`, `problems-row-hover-light.png`, `cmdk-open-light.png`, `cmdk-query-light.png`, `sidebar-collapsed-light.png`)
- The first six named files except `problems-loading` and `problems-row-hover` are byte-identical to round 3, so every round 3 issue stands: table 105px short, uppercase tags, loose "Press / to focus", bare empty and error pages, no row icons in Cmd+K, a heavy blue ring on the query input.
- `problems-row-hover-light.png` is dark and shows three unlabelled icons beyond the end of the row rule.

### Gallery, Library, Settings (`gallery-light.png`, `library-light.png`, `settings-*-light.png` x5)
- All unchanged. Gallery: "Visuals" H1, recipe ids, uneven image heights. Library: "Books", native controls. About: raw markdown with a branch name, `pass^k`, and a table running off the bottom. Sidebar Recent now lists four sessions, which is fine.

### Focus (`focus-composer-light.png`, `focus-tab-light.png`, `focus-table-row-light.png`, `focus-tile-light.png`)
- Composer: solid cobalt 2px ring, correct. Others: see the status table.

---

## Prioritised fix list (12, paste into the next build prompt)

1. **Keep the loop inside the canvas** (`studio-layout-after-simulate-light.png`).
   - Replace `FitViewOnChange.jsx` with the `useFitContent` hook and `ResizeObserver` above: bounds are the union of blocks, wires, arrowheads and tap dots, zoom clamped 0.85 to 1.25, padding 24px, re-run on canvas resize. The toolbar Fit button calls the same function. Feedback `drop` 72 to 40. `translateExtent` = content bounds plus 80px.
   - Layout gap 48px between every pair of blocks (PID to DC motor is 8px, so `u` has no wire). Block label at most two lines of 13px/16px in a 64px block, one name per block ("First-order plant" in the palette too).
   - Add `studio-wire-selection.spec.ts` to CI next to `studio-layout.spec.ts`.
2. **Make block selection stick and look selected** (`studio-block-selected-light.png`).
   - Store `selectedId` in state and re-apply it in `paint()` and the rebuild effect (code above). `highlight` out of the effect deps.
   - Selected block: `outline: 2px solid var(--accent-500); outline-offset: 2px`, no tint ring. Ports 12px filled cobalt. Inspector floats inside the canvas (280px, `--elevation-2`, 160ms) with name, type, Kp, Ki, Kd fields with units. Escape and pane click clear it.
3. **Replace the Step PNG with a themed, annotated chart** (`...-1440-light.png`).
   - Client SVG or uPlot from `{t, y, setpoint, unit, metrics}`, filling the stage (at least 220px high), drawer in two columns (360px margins left, chart right) at `clamp(240px, 40vh, 380px)`. Axes "Time (s)" and "Speed (rad/s)", gridlines `--border`, line 2px `--accent-500`, dashed setpoint, 2% band, "Settled at" and "Overshoot" labels only when they exist, cursor readout, `role="img"` summary. Remove the dead `resize` grabber.
4. **Say when the response has not settled** (`...-1440-light.png`).
   - Amber pill "Not settled within 10 s", step stats read "Not settled", "Still rising at 10 s: 0.45 of a setpoint of 1". Window control "10 s | 30 s | 100 s | Auto", Auto = `clamp(6 / ωcg, 10, 600)` s and the window shown in the x label. Never extrapolate a final value. (EE Project: for this loop the curve and ωcg agree; check that a plant DC gain near 0.125 is intended.)
5. **Correct the margin captions** (`studio-margins-no-crossover-light.png`).
   - Gain margin infinite: "Phase never reaches -180° from 0.001 to 100,000 rad/s." Phase crossover none: "Phase stays above -180° from ...". Gain crossover none: "Gain stays above 0 dB ..." or "below 0 dB ..." chosen from the sign at the sweep ends. Phase margin with no gain crossover: "Not defined" and "No gain crossover in range."
6. **Finish dark mode and capture all of it** (`home-dark.png`, `focus-tab-light.png`).
   - Dark `--accent-700` for links: `#8FB0F5` or lighter (at least 4.5:1 on `#12261C`; today 1.88:1). "Checked" as a 22px tag, text `--success-text` on `--success-tint` at 4.5:1 or better in both themes (light is 3.01:1).
   - Home thumbnails, Gallery figures and Studio plots from tokens so none is a white box. Verify Studio arrowheads, signal labels, schematic labels and the new chart in dark.
7. **Make the stale state coherent** (`problem-parameters-stale-light.png`).
   - Strip becomes `--warning-tint` with a 16px `alert-triangle`: "Out of date. Values changed after the last check. Run again to re-check." Answer at 60%. One filled button (top-bar "Run again"); the drawer banner action is a one-line text link.
8. **Fix the Home example cards for real** (`home-empty-light.png`).
   - Six distinct, correct, token-drawn thumbnails: DC drive speed shows speed against time for a motor (not the first-order plot), Signals workout a spectrum or filter response (not a power phasor), Digital loop a full unit-circle pole plot. No embedded titles, ticks at least 11px at thumbnail scale. Continue cards must differ (append "Today 17:12"). Agent line: "Connect your coding agent", the command in a `kbd` block, no "in this repo".
9. **Do Settings, Problems and Cmd+K now** (all byte-identical to round 3).
   - About: "Arc 0.1" and a four-row table (Check, Result, Status), no branch name, no `pass^k`. Engines: table with "Available" or "Not installed" tags.
   - Problems: table full width, header on `--surface-subtle`, tags 12px sentence case, `/` in a `kbd` inside the search, centred empty and error pages with icon, title, line and one secondary button.
   - Cmd+K: 16px icon per row, Actions group (New problem, Run again, Open in Studio, Toggle sidebar, Toggle theme), normal ink on every row, bottom-border input with no blue ring. `<Shortcut>` renders one `kbd` per key.
10. **Gallery and Library** (unchanged since round 1).
    - H1 "Gallery" and "Library". Captions without `power.swing_equal_area`. 16:10 image frames. Library as a sources table plus an "Add a source" dialog, styled 36px selects, a drop zone, "Textbook" and "Circuits" instead of enums.
11. **Detail pass.**
    - Work step 2: chevron at the row end, subscripts in the step text. V<sub>out</sub> marker on the schematic. Block `box-shadow: none`. Palette icons distinct for each block type. Sidebar duplicate titles disambiguated.
12. **Capture discipline** (`focus-*`, `home-scrolled-1280-light.png`).
    - Reset `data-theme` before every capture and put the theme in the filename. `focus-tile` must focus an example card, `focus-table-row` a Problems row, `focus-tab` a Work tab, each by Tab key presses. Restore `sidebar-measurements.json`. Make `md5.txt` fail the run when a capture is byte-identical to the previous round without a reason in NOTES.md.

---

## Capture checklist for round 5

Every capture: theme in the filename, `data-theme` reset first, 1280 x 800 unless stated.

**Studio (light and dark, 1280 and 1440 wide):**
- `studio-before-simulate-{light,dark}.png`, `studio-after-simulate-{light,dark}.png`: whole feedback loop inside the canvas, plus the Playwright log with `contentOutsideCanvas` returning `[]`.
- `studio-after-resize-light.png`: viewport height reduced by 120px, loop still inside.
- `studio-block-selected-{light,dark}.png`: PID clicked with the mouse, 800ms wait, 2px cobalt outline, 12px handles, inspector open with Kp, Ki, Kd. `studio-block-selected-after-simulate-light.png`: selection still present after Simulate.
- `studio-step-settled-light.png`: a loop that settles, showing the band, "Settled at", and "Overshoot" labels. `studio-step-unsettled-{light,dark}.png`: PID on the DC motor with the pill "Not settled within 10 s". `studio-step-extended-light.png`: window set to Auto or 100 s.
- `studio-margins-finite-light.png` and `studio-margins-no-crossover-light.png` with the corrected captions.
- `studio-circuit-mode-light.png` (the "Circuit" segment), if it is in scope, so the toolbar toggle is shown once.

**Dark set (full, all pages):** `home-dark`, `home-scrolled-dark`, `problem-answer-dark` (Diagram tab, readable labels), `problem-work-dark`, `problem-stale-dark`, `problems-list-dark`, `problems-row-hover-dark`, `cmdk-open-dark`, `gallery-dark`, `library-dark`, `settings-{agents,engines,appearance,data,about}-dark`, `sidebar-collapsed-dark`, plus the Studio pair above. Each page checked for white boxes and text under 4.5:1.

**Light set that changed or must be re-taken:** `problem-stale-light` (amber strip, one filled button), `home-empty-light` and `home-scrolled-{1280,1440}-light` (six distinct thumbnails, Continue rows that differ), `problems-list/empty/error/loading/row-hover-light` (with tooltips on the hover icons), `cmdk-open/query-light` (with Actions and icons), `gallery-light`, `library-light` (sources table and Add dialog open), the five Settings tabs.

**Focus, by real Tab presses:** `focus-tab-light` (a Work tab), `focus-table-row-light` (a Problems row), `focus-tile-light` (an example card), `focus-button-light`, `focus-composer-light`, and one dark of each.

**Measurements and logs to attach:** `sidebar-measurements.json` (expanded 240, collapsed 56, Cmd+K open 240, Studio at 1280 and 1440); the Playwright results for `studio-layout.spec.ts` and `studio-wire-selection.spec.ts`; a contrast table for the dark link, the Checked tag and the amber strip; `md5.txt` with a diff against round 4 showing which captures changed.

Files reviewed (35 PNGs): `cmdk-open-light`, `cmdk-query-light`, `focus-composer-light`, `focus-tab-light`, `focus-table-row-light`, `focus-tile-light`, `gallery-light`, `home-dark`, `home-empty-light`, `home-scrolled-1280-light`, `home-scrolled-1440-light`, `home-with-recent-light`, `library-light`, `problem-answer-light`, `problem-parameters-drawer-light`, `problem-parameters-stale-light`, `problem-work-tab-light`, `problems-empty-light`, `problems-error-light`, `problems-list-light`, `problems-loading-light`, `problems-row-hover-light`, `settings-about-light`, `settings-agents-light`, `settings-appearance-light`, `settings-data-light`, `settings-engines-light`, `sidebar-collapsed-light`, `studio-block-selected-light`, `studio-layout-after-simulate-1440-light`, `studio-layout-after-simulate-light`, `studio-layout-before-simulate-1440-light`, `studio-layout-before-simulate-light`, `studio-margins-finite-light`, `studio-margins-no-crossover-light`. Plus `NOTES.md`, `MY_NOTES.md`, `md5.txt`, `list.txt`.
