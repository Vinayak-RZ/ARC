# Round 13B captures

PNG count: 276

Includes round-11 coverage, 1280×800 home scroll companions (incl. `home-scrolled-1280-dark.png`), collab loop through 06, and rectifier sweep (R + RL × topologies × α grid; readouts checked vs closed form).

Capture HEAD: `3b59db3` · CI run `44025468905` · `git_dirty_lines`: 2.

## Capture environment

Product tree: detached `3b59db3e04e9d6d19e90bc57d2045b685b211d44` (PR #62 / `cursor/collab-loop-f29f`). Capture used ephemeral worktree script tweaks only (not committed to #62): `ARC_UX_CAPTURE_DIR`, collab-04b simulate via API+reload, collab-05 `tol=0.001` on `rlc-bad-derive` so forward-Euler vs ngspice surfaces as Differs in the UI, and `home-scrolled-1280-dark.png` from the collab pass.

## Numeric audit (screens with paired numbers)

Spot-check of collab, control, and rectifier frames (plus capture-time closed-form asserts for all 144 rectifier grid PNGs): **no unintended cross-label disagreements.**

| Screen | Paired values | Verdict |
| --- | --- | --- |
| `collab-01-*` | Headline, derived, simulated all **11.630 V** @ **3.628 ms** | Consistent |
| `collab-03b-*` | Settling **5.8x ms** headline vs work ζ=1 critically damped | Consistent |
| `collab-04b-*` | Restored **11.630 V** @ **3.628 ms** | Consistent |
| `collab-05-*` | Derived **11.645 V** vs simulated **11.630 V** (0.1% / limit 0% after capture `tol=0.001`) | **Expected intentional mismatch** |
| `collab-06-*` | Run agrees card vs studio step **0.909** / **0.36 s** | Consistent |
| `lab-rectifier-*` | Vo, Io, PF vs sliders (e.g. semi1 R α=30: **193.20 V**, **19.32 A** with **R=10 Ω**) | Consistent |
| `problem-control-checked-lab-agreement-*` | Simulated vs derived step metrics | Consistent (capture asserts) |

At default example `tol=2%`, forward-Euler bad derive agrees ngspice (~0.13% error); mismatch UI requires the capture-only `tol=0.001` nudge documented above.

## Known issues

- Automated dark vs light luminance pairs flagged (spot-check): cmdk-open-dark.png; collab-01-run-sim-vs-derived-agrees-dark.png; collab-02-lab-provenance-vc-activity-dark.png; collab-03-out-of-date-ask-rederive-dark.png; collab-03b-after-rederive-agrees-dark.png; collab-04-changes-r1-chip-dark.png; collab-04b-after-restore-dark.png; collab-05-forward-euler-mismatch-dark.png
