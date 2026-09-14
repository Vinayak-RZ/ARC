# Analog and digital electronics

Pack path: `knowledge/ug-ee/electronics`. Bound: `SYLLABUS.md` and `docs/curriculum-map.md`. Checker: `python scripts/check_knowledge_tree.py --pack electronics`.

## Analog (units 01–08)

| ID | Title | Notes |
|----|-------|-------|
| [01-semiconductor-diodes](01-semiconductor-diodes/) | Diodes, rectifiers, clippers, clampers | Shockley, PIV, C-input ripple, Zener |
| [02-bjt-biasing-small-signal](02-bjt-biasing-small-signal/) | BJT regions, bias, hybrid-π | Regions, divider bias, CE/CC/CB |
| [03-fet-mosfet](03-fet-mosfet/) | JFET/MOSFET characteristics and bias | Shockley, square law, body effect |
| [04-opamp-linear](04-opamp-linear/) | Ideal op-amp, inverting/noninverting, instrumentation | Golden rules, in-amp, slew |
| [05-opamp-nonlinear-applications](05-opamp-nonlinear-applications/) | Comparators, Schmitt, precision rectifiers | Hysteresis, superdiode |
| [06-feedback-amplifiers](06-feedback-amplifiers/) | Four feedback topologies, desensitivity | Black, impedances, loop gain |
| [07-oscillators](07-oscillators/) | Barkhausen, RC, LC, crystal | Wien, Colpitts, 555 |
| [08-voltage-regulators-power-amps](08-voltage-regulators-power-amps/) | Series regulators, class A/B/AB | Dropout, SOA, crossover |

## Digital (units 09–14)

| ID | Title | Notes |
|----|-------|-------|
| [09-number-systems-boolean](09-number-systems-boolean/) | Number systems, codes, Boolean algebra | Two's complement, K-map |
| [10-combinational-logic](10-combinational-logic/) | Gates, mux, decoder, adder, hazards | MSI, static-1 hazard |
| [11-sequential-logic-fsm](11-sequential-logic-fsm/) | Latches, flip-flops, counters, FSM | Setup/hold, Moore/Mealy |
| [12-adc-dac-logic-families](12-adc-dac-logic-families/) | DAC/ADC, TTL/CMOS levels | LSB, SAR/flash, fan-out |
| [13-memory-hdl-intro](13-memory-hdl-intro/) | ROM/RAM, PLA, Verilog/VHDL intro | Capacity, latch inference |
| [14-cmos-inverter-timing](14-cmos-inverter-timing/) | CMOS inverter, delay, power | VTC, 0.69 RC, \(CV^2f\) |

Each unit has `notes.md`, `questions.md`, `sources.md`. Optional Kuphaldt CC BY excerpts live in `oer/` on selected analog (Vol. III) and digital (Vol. IV) units.

OER index: http://www.ibiblio.org/kuphaldt/electricCircuits/ (CC BY 4.0). Ledger: `knowledge/SOURCE_LEDGER.md` K5.
