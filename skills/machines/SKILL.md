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

**UG drives (OSS):** `solve-drives-problem` — DC (`kind: dc`, `v_dc`, `ra_ohm`,
`k_torque`, `t_load_nm`) or IM slip line (`kind: im`, `t_rated_nm`, `slip_rated`,
`t_load_nm`). Checked steady-state speed (rpm). Full Simulink drive plant remains
optional MATLAB/Simulink, not required for coursework numbers.

## Spawn

Host-native name: `ee-machines`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/machines/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `machines`
- Sibling packs: power (network vs machine), power_electronics (drives), maths (phasors)
