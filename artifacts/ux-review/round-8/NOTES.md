# Round 8 captures

Code commit and `preflight.json` `git_sha` are identical, `git_dirty_lines` is 0. 75 PNGs (69 in round 7, plus 6 new: dark composer, tile and table-row focus; dark finite and no-crossover margins; dark settled step). md5 against round 7 (not round 4): 13 of the 69 shared names are byte-identical, 56 changed, 0 dropped (the generated line below only compares a legacy name pattern; this count was computed with a direct md5 diff).

Generated comparison: problems-list-light.png unchanged from round 7

## Gate self-score (Design's G1 to G9)

| Gate | Self-score | Proof |
|---|---|---|
| G1 wires, heads, labels, both widths, both themes | pass | `_assert_studio_wires` runs on every Studio snap; `studio-wire-selection.spec.ts` now fails on unmeasurable elements and asserts 5 wires and at least 10 measured elements |
| G2 dark arrowheads | pass | `studio-r5` dark test now resolves each wire's `marker-end` to its `<marker>` and requires the head paint to equal the wire colour (before: only counted `marker-end`) |
| G3 step chart | pass | band and settle marker now drawn: `studio-step-settled-light.png`, `studio-step-settled-dark.png` ("0.43 s" dotted line, "±2% band" label and edge lines) |
| G4 not-settled and off-target | pass | unchanged from round 7 (`studio-step-unsettled-*`, `studio-step-offtarget-light.png`) |
| G5 caption 4.5:1 and 12px | pass | `--cs-text-muted` now `var(--ee-color-muted)`, duplicate 11px block deleted. Measured: light rgb(112,112,108) on white 4.97:1, dark rgb(163,163,158) on rgb(26,26,24) 6.88:1, both 12px. `studio-r7.spec.ts` caption tests pass. `studio-margins-{finite,no-crossover}-{light,dark}.png` |
| G6 forward-path gap, one block name | pass | unchanged (`studio-r6.spec.ts`) |
| G7 inspector never clipped | pass | unchanged (`studio-block-selected-*`) |
| G8 thumbnails read | pass, with well | dark `--ee-color-surface-soft` is `#121211`, stale `.example-thumb-accent` rule deleted, `studio-r7.spec.ts` well test passes both themes (1.05 to 1.25). DC drive speed is now an under-damped speed response with a load dip, distinct from First-order step |
| G9 focus captures right | pass | Every focus capture is reached by real Tab presses from a non-focusable start point, and `document.activeElement` is asserted before the screenshot and again after it. `focus-log.json` records what was active. Ring is 2px cobalt (`--ee-color-primary`: rgb(47,111,235) light, rgb(107,147,245) dark) |

## Focus captures: what is active

| Capture | Active element | Tab presses | Computed outline |
|---|---|---|---|
| `focus-composer-light.png` | `textarea` `.composer-input`  | 2 | solid 2px rgba(0, 0, 0, 0) |
| `focus-tile-light.png` | `button` `.example-card` "VinVoutCircuit" | 3 | solid 2px rgb(47, 111, 235) |
| `focus-table-row-light.png` | `button` aria-label="Open problem" `.row-action-quiet`  | 7 | solid 2px rgb(47, 111, 235) |
| `focus-tab-light.png` | `button` role=tab `.tab-underline` "Work" | 2 | solid 2px rgb(47, 111, 235) |
| `focus-button-light.png` | `button` `.text-link` "Run again" | 6 | solid 2px rgb(47, 111, 235) |
| `focus-composer-dark.png` | `textarea` `.composer-input`  | 2 | solid 2px rgba(0, 0, 0, 0) |
| `focus-tile-dark.png` | `button` `.example-card` "VinVoutCircuit" | 3 | solid 2px rgb(107, 147, 245) |
| `focus-table-row-dark.png` | `button` aria-label="Open problem" `.row-action-quiet`  | 7 | solid 2px rgb(107, 147, 245) |
| `focus-tab-dark.png` | `button` role=tab `.tab-underline` "Work" | 2 | solid 2px rgb(107, 147, 245) |
| `focus-button-dark.png` | `button` `.text-link` "Run again" | 6 | solid 2px rgb(107, 147, 245) |

Notes: the composer ring is drawn on the composer card (the textarea keeps a transparent outline by design). The Problems list rows are not focusable; the target is the row's "Open problem" action, which now becomes visible on `:focus-within` (it was opacity 0 on keyboard focus, so the first attempt showed no ring). "Run again" is the stale banner button in the open Parameters drawer; it is now styled from tokens (it was a native white button in dark).

## Fix list self-score (Design round 7, section 9)

| # | Item | Score | Evidence |
|---|---|---|---|
| 1 | Margin captions | done | above, G5 |
| 2 | Focus captures plus this table | done | above, G9 |
| 3 | Work step expander | done | `.step-expand` styled from tokens, `aria-label="Show working"`, chevron rotates when open; `problem-work-dark.png` and `problem-work-light.png`. Not done: step 2 expanded by default |
| 4 | Thumbnail well, both themes | done | `home-dark.png`, `home-empty-light.png` |
| 5 | Specs | done, merge not done | `studio-r7.spec.ts` added (4 tests), r5 dark test strengthened, wire-selection fails on unmeasurable elements, `retries: 0`, critiques 3 to 7 under `docs/planning/frontier-2026-11/design-critiques/`. 27 of 27 e2e pass at retries 0. PR #58 is not merged (user decides) |
| 6 | Settle wording | not done (out of scope for this half-round) | |
| 7 | Plot annotations | partial | band and settle marker done; overshoot peak dot and label not drawn |
| 8 | Before-Simulate drawer skeleton | not done | |
| 9 | Palette scroll affordance | not done | |
| 10 | Problems list finish | not done | |
| 11 | Gallery and Library finish | not done | |
| 12 | Capture hygiene | partial | md5 baseline is now the previous round; Recent still lists scenario sessions ("Low gain", "Finite crossover", "Control Studio") in Studio captures; preflight does not probe the Finite crossover golden |
