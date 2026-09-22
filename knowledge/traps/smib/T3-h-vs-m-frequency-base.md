# T3 — H vs M and frequency base mixup

**Domain:** Swing equation constants (all SMIB labs)

## Symptom

- Uses \(2H/\omega_s \cdot d^2\delta/dt^2 = P_m - P_e\) then plugs
  \(f_0=50\) Hz as \(\omega_s\) without \(2\pi\).
- Swaps **M** (inertia coefficient) and **H** (inertia constant in seconds).
- Integrates in **degrees** while \(H\) and \(P\) are per-unit on radian angle.

## Why it fails

Standard coursework form (EEC-301):

\[
\frac{d\Delta\omega}{dt} = \frac{\pi f_0}{H}(P_m - P_{\max}\sin\delta),
\quad \Delta\omega = \frac{d\delta}{dt}
\]

with \(\omega_s = 2\pi f_0\). Using \(f_0\) where \(\omega_s\) belongs scales
acceleration by \(2\pi\). Degree/radian mix multiplies angles by \(180/\pi\).

## Arc path

1. `SmibCase.accel_coeff()` returns \(\pi f_0/H\) — single source in kernel.
2. `skills/swing-equation/SKILL.md` unit checklist before integration.
3. Cross-read `knowledge/ug-ee/power/06-power-system-stability/notes.md` §Mistakes.

## Bare-agent prompt that should fail

> “Take ω_s = 50 rad/s and δ in degrees for H=5.”

Double error on base and angle unit.
