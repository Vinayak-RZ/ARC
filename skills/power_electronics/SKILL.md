# Power electronics pack

Load for UG converters and drives-adjacent courses: rectifiers, buck/boost/buck-boost,
inverters, PWM, averaged models, duty-cycle algebra. Not HIL benches
(`CD-PE-HIL`).

## Web-verify

MOSFET/diode datasheet values belong in `context_claims` for **`web-verify`**
(Rds(on), Vf, Qg). Cite sources as `[n]`; similar converter homework pages go under
**Similar solved problems**.

## Any question in this pack

1. Name topology, CCM/DCM, ideal vs ESR, the unknown (V, I, duty, ripple).
2. **Exam v2** (`study-power-electronics-v2`): `ccm_buck` with `problem.json` (`vin`, `vout`,
   `l`, `c`, `fs`, `value_key`, `expected`). Table: `docs/AGENT_ROUTING.md`.
3. Averaged algebra via `converter-model` / `algebraic-check` first.
4. `lumped-circuit-sim` only if a switched/averaged netlist artifact exists.
5. Waveform plots via `render-figure` from computed points or a provider —
   never a vision-invented switching PNG. No provider → exact token `unchecked`.

## Genres

Design-to-spec (L, C, duty for a UG spec) is in-bound. Hardware-in-the-loop
and thermal FEA are cannot-do.

## Spawn

Host-native name: `ee-power-electronics`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/power-electronics/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `power-electronics`
- Sibling packs: electronics (devices), machines (drives), power (grid interface)
