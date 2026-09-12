# EM / fields pack

Load for UG fields: electrostatics, magnetostatics, Maxwell in integral form
as taught to EE, uniform plane waves, lossless transmission lines. Not a
research EM programme. Not CST/HFSS as the product path (`CD-EM-HFSS`).

## Any question in this pack

1. Name the configuration (charge, current, boundary, line) and the unknown
   (E, H, D, B, Γ, VSWR, Smith — UG).
2. Use `fields-analytic` / `algebraic-check` (closed form, phasor TEM).
3. Full-wave numeric solvers are cannot-do; label `unchecked` rather than
   invent S-parameters.
4. `lumped-circuit-sim` is the wrong default for “find E at P.”

## Genres

Derive and explain are common. Simulate means analytic/numeric identity, not
SPICE, unless the problem reduced to a lumped model the student stated.
