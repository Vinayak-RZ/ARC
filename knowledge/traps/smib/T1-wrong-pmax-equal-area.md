# T1 — Wrong Pmax on equal-area / δ_cr

**Domain:** SMIB transient stability (EEC-301 Exp 6) · Trap catalog T1

## Failure mode (bare agent)

Compute δcr with a **single** Pmax, or swap fault/post amplitudes:

\[
\cos\delta_{\mathrm{cr}} =
\frac{P_m(\delta_{\max}-\delta_0) + P_{\max}^{\mathrm{post}}\cos\delta_{\max}
- P_{\max}^{\mathrm{fault}}\cos\delta_0}
{P_{\max}^{\mathrm{post}} - P_{\max}^{\mathrm{fault}}}
\]

Common mistakes:

- Plug **Pmax_pre = 2.0** into the numerator/denominator instead of fault/post pair.
- Set **Pmax_fault = 0** for a “bolted fault” when the PDF gives **0.5 pu**.
- Use **δmax = π − arcsin(Pm/Pmax_pre)** instead of **post-fault** Pmax = 1.5.

Shifts δcr by many degrees (e.g. correct ≈ **79.53°** → wrong).

## Lab truth (do not invent)

From `artifacts/eec301-lab-goldens/exp06.json` → `equal_area`:

| Quantity | Value |
|----------|-------|
| δ₀ | 26.743683950403007° |
| δmax | 143.13010235415598° |
| δcr | 79.53240997193419° |
| cos δcr | 0.18167930768699725 |

## Arc path

1. `skills/swing-equation/SKILL.md` — three-stage Pmax table before algebra.
2. `critical_clearing_angle()` in `engines/smib_swing.py`.
3. CI: `tests/unit/test_smib_swing.py::test_exp06_equal_area_matches_lab_json`.

## Bare-agent prompt that should fail

> “Find critical clearing angle for Pm=0.9, Pmax=1.5, H=5.”

Missing stage split → wrong δcr.
