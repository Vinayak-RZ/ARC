# T1 — Wrong Pmax on equal-area / δ_cr

**Domain:** SMIB transient stability (EEC-301 Exp 6 class)

## Symptom

Agent uses a single \(P_{\max}\) for prefault, during-fault, and post-fault
curves, or applies post-fault \(P_{\max}^{(3)}\) inside the \(\delta_{\mathrm{cr}}\)
formula while the fault segment still has \(P_{\max}^{(2)}\).

## Why it fails

The transfer reactance changes three times: steady, faulted, cleared. Equal-area
accelerating area uses \(P_e^{\mathrm{fault}}(\delta)=P_{\max}^{(2)}\sin\delta\);
decelerating area uses \(P_{\max}^{(3)}\). Mixing stages shifts
\(\delta_{\mathrm{cr}}\) by tens of degrees.

## Arc path

1. Load `skills/swing-equation/SKILL.md` — stage table before algebra.
2. Compute with `critical_clearing_angle()` in `engines/smib_swing.py`.
3. Golden check: EEC-301 default case \(\delta_{\mathrm{cr}}\approx 79.53^\circ\),
   \(\cos\delta_{\mathrm{cr}}\approx 0.1817\) (`eec301_reference()`).

## Bare-agent prompt that should fail

> “Find critical clearing angle for Pm=0.9, Pmax=1.5, H=5.”

Missing stage split → wrong \(\delta_{\mathrm{cr}}\).
