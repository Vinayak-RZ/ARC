# Power electronics — syllabus union

Bound: `docs/curriculum-map.md` (IITR, NITT, AICTE-family, MIT/Berkeley, ETH energy track, GATE overlay).

This pack is the UG power-electronics core: switches and SOA, uncontrolled and phase-controlled rectifiers, DC–DC choppers, inverters and PWM, AC voltage controllers, commutation and snubbers, DC and AC drives at converter level, magnetics and thermal, cycloconverters and dual converters. Depth is coursework (assignment, lab numerical, exam-style), not a multi-level-converter research flow or a commercial gate-driver application note.

## Devices and AC–DC

- `01-power-semiconductor-switches` — Diode, SCR, MOSFET, IGBT, SOA
- `02-uncontrolled-rectifiers` — 1ph/3ph diode bridges, overlap
- `03-controlled-rectifiers` — Phase-controlled converters

## DC–DC, DC–AC, AC–AC

- `04-dc-dc-choppers` — Buck, boost, buck-boost, duty
- `05-inverters` — VSI, CSI, 1ph/3ph, harmonic
- `06-ac-voltage-controllers` — Integral cycle, phase AC control
- `07-pwm-techniques` — SPWM, hysteresis, unipolar/bipolar
- `08-commutation-snubbers` — Natural/forced commutation, snubbers

## Drives, magnetics, special converters

- `09-dc-drives` — 1Q-4Q DC drives
- `10-ac-drives` — V/f, CSI, cyclo intro
- `11-converter-magnetics-thermal` — Inductors, transformers, heatsinks
- `12-cyclo-dual-converters` — Cycloconverter and dual converter

## Notes

- Capability ids stay in `docs/ARCHITECTURE.md` §0; this pack does not invent extra EE capabilities.
- Worked items in `questions.md` are original numbers, not GATE or institute papers.
- No `oer/` copies in this pack (original notes plus links in `sources.md`).
