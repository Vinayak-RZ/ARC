# Electronics pack

Load for devices, analog circuits, digital electronics, linear ICs / op-amps
at UG depth. Not foundry PDK or analog tape-out (`CD-ELEC-PDK`, `CD-TAPEOUT`).

## Any question in this pack

1. Name the region/model (ideal op-amp, small-signal, large-signal, CMOS
   switch, gate delay) and the unknown.
2. Device equations and identities via `algebraic-check` first.
3. `lumped-circuit-sim` only for an analog netlist artifact (bias point, AC
   gain), never as a PDK stand-in.
4. Digital: truth tables / timing algebra; do not invent an HDL simulator
   unless a registered provider exists — else `unchecked`.

## Genres

Design-to-spec at UG (bias, gain, cutoff) is in-bound. Tape-out, layout vs
foundry DRC, and research analog IC are out. Photos of schematics use
`ingest-figure` (confirm, no silent sim).
