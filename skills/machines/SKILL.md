# Machines pack

Load for transformers and DC/IM/synchronous machines at UG: equivalent
circuits, phasors, OC/SC / no-load tests, torque-speed, efficiency.
Not FEA / Ansys Maxwell (`CD-MACHINES-FEA`). Not plant actuation.

## Any question in this pack

1. Name the machine, test or regime (no-load, blocked rotor, rated, starting).
2. Draw the equivalent circuit; per-unit if the problem is in pu.
3. Request `machine-model` (phasor / eq-circuit algebra). Optional numeric
   provider if registered; otherwise `algebraic-check`.
4. No live PLC / starter write. No full-wave magnetics as a promise.

## Genres

Lab-report OC/SC is in-bound (report genre). Starting transients without a
provider stay `unchecked`. Do not route a transformer homework through
`lumped-circuit-sim` unless the student supplied a lumped netlist.
