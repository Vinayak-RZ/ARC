# Power pack

Load for study-level power systems: per-unit, T&D, load flow, balanced/unbalanced
faults, protection as coursework (relay settings on paper), not EMS dispatch
(`CD-POWER-EMS`) and not live grid write.

## Any question in this pack

1. Name the network (one-line / Ybus / given data) and the unknown (V, P, |I|,
   pu, fault level).
2. Per-unit and power-flow equations via `algebraic-check` when the network is
   small enough to do by hand.
3. `power-network-study` only with a **network artifact** (case file / typed
   bus list). Unmatched text is not a pandapower case.
4. Named fault study: `simulate-power-fault` with `problem.json` fields
   `fault_type` (`LG`, `LL`, `LLG`, `3PH`), `faulted_phases` when not the canonical
   a-ground / a–b pair, `z1_pu`, `z2_pu`, `z0_pu`. Engine returns `I0/I1/I2` and
   `I_phase_pu` (magnitude + angle vs prefault `Va`), not a single `sqrt(3)*V` scalar.
   Per-unit base trap: `symmetrical-fault-study` + `engines/pu_base` rescores every
   element onto the system MVA/kV before summing `Z1`.
5. After every solve/study engine step, **`web-verify`** runs: list stale-risk
   constants in `context_claims`, search the web (host MCP) or offline fixtures,
   cite with `[n]` in the answer, and file similar worked problems.
6. Exam-style kernels: `docs/AGENT_ROUTING.md` + recipes `ed-penalty-study`,
   pack workflows `study-*-v2`, `run-ee-v2-solver` with `solver` + `expected` in
   `problem.json`.
6. **SMIB transient / equal-area / CCT:** `skills/swing-equation/SKILL.md` +
   `engines/smib_swing` (goldens `artifacts/eec301-lab-goldens/exp06.json`).
7. **Two-area AGC (Exp 7):** `skills/agc-two-area/SKILL.md` + `engines/agc_two_area`.
8. **Economic dispatch λ (Exp 8):** `skills/economic-dispatch-lambda/SKILL.md` +
   `engines/ed_lambda`.
9. Study-level protection (no EMS): `study-protection-setting` with CT ratio,
   relay pickup (secondary A), fault current; optional `zone_reach_ohm` +
   `v_line_kv` for simple distance zone check.
10. Missing provider → `unchecked`, never a fluent “converged” voltage.

## UI construction

Power SLD + LG inset: **`skills/ui-diagrams/SKILL.md`**. Write `control_diagram.json` with `diagramKind: power_fault` or run `simulate-power-fault` so the kernel seeds the same shape.

## Genres

Design-to-spec is UG (conductor/transformer sizing at study level), not
operations. Simulate means study-level load flow / fault, not SPICE of a grid.

## Spawn

Host-native name: `ee-power`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/power/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `power`
- Sibling packs: machines (transformer/machine), power_electronics (converters), circuits (three-phase)
