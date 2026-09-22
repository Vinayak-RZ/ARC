# Swing-equation (classical SMIB)

Load for **transient stability** coursework: classical one-machine-infinite-bus
(OMIB), equal-area criterion, and fixed-step integration (Euler, modified Euler,
RK4). Not multi-machine eigenanalysis, not voltage stability, not PSS design.

## Any question in this pack

1. State the **stage** Pmax values (pre-fault, during-fault, post-fault) and
   mechanical power Pm. Wrong Pmax on the wrong segment is trap **T1**.
2. Write the **state form** before coding:
   - \( \dot\delta = \Delta\omega \)
   - \( \dot{\Delta\omega} = (\pi f_0 / H)(P_m - P_{\max}\sin\delta) \)
   with δ in **electrical radians**, H in MJ/MVA on the machine base, \(f_0\) in Hz.
3. Prefault equilibrium: \(\delta_0 = \sin^{-1}(P_m/P_{\max}^{(1)})\), \(\Delta\omega_0=0\).
4. Equal-area \(\delta_{\mathrm{cr}}\) when \(P_{\max}^{(2)} \neq 0\): use the
   closed form in EEC-301 Exp 6 (not the bolted-fault \(P_e=0\) parabola).
5. **Critical clearing time:** bisect on \(t_c\) with the same integrator you
   report; align \(t_c\) to the step grid (trap **T2**). Instability indicator
   for coursework: first-swing \(\delta > \pi\) rad within the study window.
6. Call kernel helpers (`electrical_engineer.engines.smib_swing`) for checked
   δ₀, δ_cr, t_cr against `docs/planning/eec301-lift/EEC301_EXP6_GOLDEN.md`.

## Forbidden shortcuts (trap T9)

When the lab sheet says student-written integrators:

- Do **not** call MATLAB `ode45`, SciPy `solve_ivp`, or black-box ODE solvers.
- Implement Euler, modified Euler (Heun), and RK4 explicitly on the 2-state vector.

## Units (trap T3)

- \(H\) is inertia constant (s); \(M = 2H/\omega_s\) is a different coefficient.
- \(\omega_s = 2\pi f_0\) uses **electrical** frequency in rad/s.
- Do not mix mechanical shaft degrees with electrical \(P_{\max}\sin\delta\).

## Spawn

Host-native pack: `ee-power`. Load `skills/power/SKILL.md` for faults/load flow;
load **this file** when the prompt mentions swing equation, equal-area, CCT, or
SMIB transient stability.

## Knowledge

- `knowledge/ug-ee/power/06-power-system-stability/notes.md`
- Traps: `knowledge/traps/smib/` (T1–T3)
- Golden tolerances: `docs/planning/eec301-lift/EEC301_EXP6_GOLDEN.md`
