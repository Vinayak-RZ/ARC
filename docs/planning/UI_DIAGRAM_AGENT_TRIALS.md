# UI diagram agent trials

Generated: 2026-09-21 18:29 UTC

## Improve cycle 1

- Added stress modes: baseline, perturbed values, from-spec (no example file copy).
- Control runs seed `bode.png` / `step.png` via `attach_sidecar_artifacts`.
- Checker rejects bad fixtures under `eval/gold/ui-diagrams/bad/`.
- Rubric dimensions 1–5; canonical PNG per domain = best stress case (target overall ≥4).

### Stress matrix

| Domain | Mode | Status | Shapes | dark_frac | Overall | Plots | SHA-256 (prefix) |
|--------|------|--------|--------|-----------|---------|-------|------------------|
| rlc | baseline | PASS | 17 | 0.0188 | 5 | yes | `ddbee26f1270…` |
| rlc | perturbed | PASS | 17 | 0.0190 | 5 | yes | `d76b308c1204…` |
| rlc | from_spec | PASS | 17 | 0.0193 | 5 | yes | `b937818700ac…` |
| control | baseline | PASS | 12 | 0.0138 | 5 | yes | `68b301e7f3f2…` |
| control | perturbed | PASS | 12 | 0.0137 | 5 | yes | `26846fe5026e…` |
| control | from_spec | PASS | 12 | 0.0137 | 5 | yes | `dbf44450d6d1…` |
| power | baseline | PASS | 17 | 0.0309 | 5 | yes | `998be731da12…` |
| power | perturbed | PASS | 17 | 0.0307 | 5 | yes | `4d72c8762913…` |
| power | from_spec | PASS | 17 | 0.0309 | 5 | yes | `7184876ac220…` |
| protection | baseline | PASS | 9 | 0.0164 | 5 | yes | `fb5dc99343a0…` |
| protection | perturbed | PASS | 9 | 0.0164 | 5 | yes | `f3c1eea4592f…` |
| protection | from_spec | PASS | 9 | 0.0165 | 5 | yes | `ff9dce54b3b3…` |
| drives | baseline | PASS | 11 | 0.0108 | 5 | yes | `1f1cc88337c4…` |
| drives | perturbed | PASS | 11 | 0.0108 | 5 | yes | `9f6b555986b3…` |
| drives | from_spec | PASS | 11 | 0.0110 | 5 | yes | `9fe4f5e749dc…` |

### Canonical PNGs (committed)

- **rlc** (from_spec): score 5/5, `docs/media/trials/trial-rlc.png`, `b937818700ac81bde064fbfd1bbf9ed3455762c73da0a40e7daeaa5a3ce87269`
- **control** (from_spec): score 5/5, `docs/media/trials/trial-control.png`, `dbf44450d6d1ab6c89ba7e0ae2f7ebfa787dce7807e734b2586bcef4fc89eadd`
- **power** (from_spec): score 5/5, `docs/media/trials/trial-power.png`, `7184876ac2203ceac29b1c793d2f7802578fd81851c7cb7142532d0a89cc9173`
- **protection** (from_spec): score 5/5, `docs/media/trials/trial-protection.png`, `ff9dce54b3b353c6aec1c753bb93f6a6147070bb361d0e2b19a52bb1912ced31`
- **drives** (from_spec): score 5/5, `docs/media/trials/trial-drives.png`, `9fe4f5e749dccf05599237f05ac379b698cd7d7e8d9696f5720c92f0798852e1`

Skill: `skills/ui-diagrams/SKILL.md`. Stress: `scripts/trial_agent_ui_diagrams_stress.py`.
