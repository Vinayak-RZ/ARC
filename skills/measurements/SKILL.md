# Measurements pack

Load for electrical measurements and instrumentation: errors, uncertainty,
bridges, instrument specs, analog meters, digital meters at UG. Not driving a
physical bench (`CD-MEAS-BENCH`).

## Any question in this pack

1. Name the measurand, instrument, range, and error model (limiting error,
   probable error, loading).
2. Use `measurement-model` / `algebraic-check`. There is no “simulate the lab
   bench” provider in v1.
3. Bridge and potentiometer circuits may use `algebraic-check`; SPICE only if
   the student supplied a netlist **and** the unknown is a circuit quantity.

## Genres

Review a lab reading for loading error. Report genre = error budget +
assumptions in `argument.md`. Never claim a live instrument was polled.
