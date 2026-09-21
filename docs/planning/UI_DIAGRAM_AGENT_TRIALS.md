# UI diagram agent trials

Generated: 2026-09-21 18:21 UTC

Method: compose from `skills/ui-diagrams/examples/` (agent copy path), not README recipe seeds.
Each domain uses a **distinct** run id `trl-<domain>-<stamp>` and must produce a **distinct** PNG SHA-256.

| Domain | Status | Shapes | dark_frac | SHA-256 (prefix) | PNG | Run id |
|--------|--------|--------|-----------|------------------|-----|--------|
| rlc | PASS | 17 | 0.0190 | `5314a73c35a08310…` | `docs/media/trials/trial-rlc.png` | `trl-rlc-20260921T182119Z` |
| control | PASS | 12 | 0.0138 | `70e7ed9468959c27…` | `docs/media/trials/trial-control.png` | `trl-control-20260921T182119Z` |
| power | PASS | 17 | 0.0309 | `cdae3a8db55dec19…` | `docs/media/trials/trial-power.png` | `trl-power-20260921T182119Z` |
| protection | PASS | 9 | 0.0164 | `b108a59bdd1fa641…` | `docs/media/trials/trial-protection.png` | `trl-protection-20260921T182119Z` |
| drives | PASS | 11 | 0.0109 | `b4d1282b479e1c29…` | `docs/media/trials/trial-drives.png` | `trl-drives-20260921T182119Z` |

## Full SHA-256
- `rlc`: `5314a73c35a083106995e9347bd6e0de4ec0bcdd9a6c30ef500f6372d1412812`
- `control`: `70e7ed9468959c274c60cc51757ea2dbd1e2cfda97d91bab48a69995c0d55d54`
- `power`: `cdae3a8db55dec19ab33945cadf3fe69227af2607f7c8e3b57ea857092ea8602`
- `protection`: `b108a59bdd1fa6415c60ecf3fd040371bdcfac6ca62c6b2d6fb84ee40d395607`
- `drives`: `b4d1282b479e1c2940846de667eead098255bf45901341b2ddb14fd3712972b9`

Skill: `skills/ui-diagrams/SKILL.md`. Checker: `scripts/check_ui_diagram_artifacts.py --examples`.
