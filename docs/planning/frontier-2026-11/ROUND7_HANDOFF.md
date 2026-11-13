# Round 7 handoff (EE stop order)

## Root-cause fix (edges after Simulate)
- `ControlStudio.jsx`: no `is-empty` toggle, `flowKey`, guarded `onEdgesChange`, post-sim resync/remount.
- `studio.css`: fixed `--studio-results-h` from first paint; dropped `.studio.is-empty` wire hacks.
- `ResultsDock.jsx`: placeholder when `!results`.
- `studio-r6.spec.ts`: edge paths with non-empty `d` before/after Simulate @ 1440×900.

## Playwright edge-count test
**Pass** last local run after `d2ea172`; not re-run at handoff.

## Capture (`/tmp/capture-r7.log`)
`uv run python scripts/capture_ux_review_round.py --round 7 2>&1 | tee /tmp/capture-r7.log`

Last lines: final run **completed** (`md5.txt` written). Earlier same log session: duplicate PNG guard, unsettled timeout, 1440 zero-wire on reused session.

## Round-7 PNGs
**62** under `artifacts/ux-review/round-7/` + `md5.txt`, `NOTES.md`, `preflight.json`. Gaps: `studio-block-selected-dark`, `studio-step-unsettled-dark`, `studio-step-extended-dark`, `focus-*-dark`.

## Gates G1–G9
- **G1** Partial — layout fix, 1440 captures, edge spec; CI matrix unsigned.
- **G2** Partial — dark studio PNGs; arrowhead e2e flaky on stale server.
- **G3** Partial — StepChart; limited e2e.
- **G4** Partial — unsettled light only.
- **G5** Likely pass — margins + unit tests.
- **G6** Likely pass — layout constants + captures.
- **G7** Partial — inspector grid; no selected-dark studio.
- **G8** Partial — home captures; thumbnails not fully verified.
- **G9** Partial — focus-light; missing dark focus/selected-dark.

Branch `cursor/arc-ui-round7`. No draft PR opened here.
