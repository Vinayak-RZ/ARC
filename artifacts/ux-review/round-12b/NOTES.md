# Round 12B captures

PNG count: 170

Includes round-11 coverage, 1280×800 home scroll companions (incl. `home-scrolled-1280-dark.png`), collab-03–05 (live forward-Euler mismatch), rectifier topology sweep (two α per topology), and `lab-rectifier-full3-rl-alpha75` (Vo ≈ 145.1 V).

Capture HEAD (product): `a50a39f` · bundle commit `4dc3666` · merged collab `a5d1fc1` · CI run [`43996013108`](https://github.com/Vinayak-RZ/ARC/actions/runs/43996013108).

## On-screen number flags

- **collab-03b**: Answer line shows **Settling (2%) 5.85 ms** (analytic `settling_2pct_entry_s`); copy target was 5.83 ms.
- **collab-05**: Intentional **forward-Euler derived ~11.96 V** vs **ngspice ~11.63 V** (mismatch card).
- **collab-05**: Run headline may still read **Vc,peak ≈ 11.63 V** while verify reports derived **11.96 V** — expected for the bad-derive demo.

## Known issues

- Automated dark vs light luminance pairs flagged (spot-check): cmdk-open-dark.png; collab-01-run-sim-vs-derived-agrees-dark.png; collab-02-lab-provenance-vc-activity-dark.png; collab-03-out-of-date-ask-rederive-dark.png; collab-03b-after-rederive-agrees-dark.png; collab-04-changes-r1-chip-dark.png; collab-04b-after-restore-dark.png; collab-05-forward-euler-mismatch-dark.png
- `/api/runs/{id}` can omit `circuit_derive`/`rlc_transient` in the payload even when files exist on disk (headline still renders via `lab_verify` + `formatAnswer`).
