# Machines pack

Load for transformers and DC/IM/synchronous machines at UG: equivalent
circuits, phasors, OC/SC / no-load tests, torque-speed, efficiency.
Not FEA / Ansys Maxwell (`CD-MACHINES-FEA`). Not plant actuation.

## Any question in this pack

1. Name the machine, test or regime (no-load, blocked rotor, rated, starting).
2. Draw the equivalent circuit; per-unit if the problem is in pu.
3. **Exam v2** (`study-machines-v2`): `transformer_regulation`, `dc_motor_shunt`,
   `induction_air_gap_split` — see `docs/AGENT_ROUTING.md`.
4. Request `machine-model` (phasor / eq-circuit algebra). Optional numeric
   provider if registered; otherwise `algebraic-check`.
5. No live PLC / starter write. No full-wave magnetics as a promise.

## Genres

Lab-report OC/SC is in-bound (report genre). Starting transients without a
provider stay `unchecked`. Do not route a transformer homework through
`lumped-circuit-sim` unless the student supplied a lumped netlist.

## UI construction

DC drive chain in the UI: **`skills/ui-diagrams/SKILL.md`** (`diagramKind: drives_dc` or `solve-drives-problem`).

**UG drives (OSS):** `solve-drives-problem` — DC (`kind: dc`, `v_dc`, `ra_ohm`,
`k_torque`, `t_load_nm`) or IM slip line (`kind: im`, `t_rated_nm`, `slip_rated`,
`t_load_nm`) or **exact per-phase EC** (`kind: im_ec` with `r1_ohm`, `x1_ohm`,
`r2p_ohm`, `x2p_ohm`, `xm_ohm`, `slip`, `v_line_v`, `poles`, `f_hz`). Engine
exports `developed_torque_Nm`, `stator_current_A`, `slip_at_max_torque`, and
`rotor_speed_rpm` (3-phase air-gap power). Full Simulink plant remains optional.

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
