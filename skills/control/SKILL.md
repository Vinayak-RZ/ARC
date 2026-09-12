# Control pack

Load for classical UG control: models, TF/SS, stability, time response,
Bode/Nyquist/root locus, simple compensators. Not graduate optimal control.

## Any question in this pack

1. Name the plant (TF or SS), the unknown (pole, Gm/Pm, Kv, settling, PID
   gains), and assumptions (LTI, SISO unless stated).
2. Write the characteristic equation / Routh / final-value **before** plots.
3. Request capabilities:
   - `algebraic-check` for Routh, residues, gain formulas
   - `lti-analysis` for step/Bode/Nyquist/rlocus (python-control or MATLAB)
   - `render-figure` for library plots — never invent a Bode bitmap
   - `ingest-figure` for block-diagram / Bode photos (`control-diagram-to-model`,
     UI confirm, no silent sim)
4. MATLAB-only toolboxes missing → `unchecked`, not a fake plot.

## Genres

Solve and design-to-spec use the same capabilities. Simulate means `lti-analysis`
on a typed TF/SS, not SPICE by default. Explain stays in `argument.md`.

## Do not

Drop `control-diagram-to-model`. Use `simulate-circuit` for a compensator
homework unless there is actually a lumped netlist.
