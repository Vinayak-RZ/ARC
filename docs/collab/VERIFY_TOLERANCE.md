# Lab verify tolerance

Arc uses **one** relative tolerance for derived-vs-simulated checks in the collab loop:

- **Default limit:** 2% of `|derived|` (configurable per problem via `tol` when `0 < tol < 1`).
- **Difference column:** actual relative error (e.g. `0.004%` when nearly equal).
- **Status badge:** `Agrees (limit 2%)` or `Differs by X.X% (limit 2%)` using that same limit.

Simulation always uses the **saved lab `graph.json`** compiled to SPICE, not a parallel hand-written netlist, so the schematic and ngspice see the same topology.