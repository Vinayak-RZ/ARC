# T3 — H vs M and frequency base mixup

**Domain:** Swing equation constants (Exp 6; AGC inertia in Exp 7) · Trap catalog T3

## Failure modes (bare agent)

**Exp 6 swing**

- PDF: \(d\Delta\omega/dt = (\pi f_0/H)(P_m - P_e)\). Agents write \(\omega_s/(2H)\) with
  \(\omega_s=2\pi f_0\) **correctly** (= \(\pi f_0/H\)) **or** wrongly use \(f_0/H\),
  \(2\pi f_0/H\), or treat \(\Delta\omega\) in **Hz**.
- Mix **inertia constant H** (MJ/MVA, seconds) with AGC area **M** (pu·s) — different models.

**Exp 7 (preview)**

- Report \(\Delta f\) in pu as Hz (forget ×60).
- Reuse **f₀ = 50 Hz** from Exp 6 inside the Exp 7 twin (PDF: **60 Hz**).

## Lab truth (Exp 6)

Formulation in `exp06.json` notes: \(d\Delta\omega/dt = (\pi f_0/H)(P_m - P_{\max}\sin\delta)\).

At prefault equilibrium (\(P_e = P_m\)), acceleration must be **zero** at δ₀ from JSON.

## Arc path

1. `SmibCase.accel_coeff()` → \(\pi f_0/H\) only.
2. `skills/swing-equation/SKILL.md` unit checklist.
3. CI: `test_swing_rhs_accel_coeff_trap_t3`.
4. Exp 7 goldens staged in `artifacts/eec301-lab-goldens/exp07.json` (W3).

## Bare-agent prompt that should fail

> “Take ω_s = 50 rad/s and δ in degrees for H=5.”

Double error on base and angle unit.
