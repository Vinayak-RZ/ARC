# Power electronics pack

Load for UG converters and drives-adjacent courses: rectifiers, buck/boost/buck-boost,
inverters, PWM, averaged models, duty-cycle algebra. Not HIL benches
(`CD-PE-HIL`).

## Any question in this pack

1. Name topology, CCM/DCM, ideal vs ESR, the unknown (V, I, duty, ripple).
2. Averaged algebra via `converter-model` / `algebraic-check` first.
3. `lumped-circuit-sim` only if a switched/averaged netlist artifact exists.
4. Waveform plots via `render-figure` from computed points or a provider —
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
