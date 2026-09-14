# Analog and digital electronics — syllabus union

Bound: `docs/curriculum-map.md` (IITR, NITT, AICTE-family, MIT/Berkeley, GATE overlay).

This pack is the UG analog + digital electronics core: devices and linear/nonlinear analog circuits (01–08), then number systems through CMOS timing (09–14). Depth is coursework (assignment, lab numerical, exam-style), not analog-IC research flows or a full HDL/RTL job.

## Analog

- `01-semiconductor-diodes` — Diodes, rectifiers, clippers, clampers
- `02-bjt-biasing-small-signal` — BJT regions, bias, hybrid-π
- `03-fet-mosfet` — JFET/MOSFET characteristics and bias
- `04-opamp-linear` — Ideal op-amp, inverting/noninverting, instrumentation
- `05-opamp-nonlinear-applications` — Comparators, Schmitt, precision rectifiers
- `06-feedback-amplifiers` — Four feedback topologies, desensitivity
- `07-oscillators` — Barkhausen, RC, LC, crystal
- `08-voltage-regulators-power-amps` — Series regulators, class A/B/AB

## Digital

- `09-number-systems-boolean` — Number systems, codes, Boolean algebra
- `10-combinational-logic` — Gates, mux, decoder, adder, hazards
- `11-sequential-logic-fsm` — Latches, flip-flops, counters, FSM
- `12-adc-dac-logic-families` — DAC/ADC, TTL/CMOS levels
- `13-memory-hdl-intro` — ROM/RAM, PLA, Verilog/VHDL intro
- `14-cmos-inverter-timing` — CMOS inverter, delay, power

## Notes

- Capability ids stay in `docs/ARCHITECTURE.md` §0; this pack does not invent extra EE capabilities.
- OER copies are short Kuphaldt Vol. III / Vol. IV excerpts (CC BY 4.0) under unit `oer/` folders. Kuphaldt JFET/IGFET and sequential chapters marked incomplete at retrieve date are linked, not treated as full handbooks.
- Worked items in `questions.md` are original numbers, not GATE or institute papers.
