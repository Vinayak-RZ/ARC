# Circuits pack

Load for circuit theory: DC/AC, network theorems, transients, phasors,
resonance, two-ports. Not device physics (electronics), not machines.

## Any question in this pack

1. Name Given / Find / assumptions (ideal elements, DC vs sinusoidal SS).
2. Choose method: Ohm + KCL/KVL, nodal/mesh, Thevenin/Norton, superposition,
   phasor, Laplace transient — **before** a simulator.
3. Request capabilities (do not mint ohms):
   - `algebraic-check` for hand/symbolic last lines
   - `lumped-circuit-sim` **only** with a netlist artifact
   - `render-figure` for library schematics
   - `ingest-figure` for homework photos (UI confirm, no silent sim)
   - `retrieve-citation` when a book claim is needed
4. No installed provider → exact token `unchecked`.

## Genres

| Genre | Do |
|-------|----|
| Solve | Laws first; sim only to check a netlist |
| Derive | Keep the argument in `argument.md`; optional last-line `algebraic-check` |
| Design | UG component/to-spec; still capability-checked or `unchecked` |
| Simulate | Short attachment or `lumped-circuit-sim` graph; `repair_max: 2` then label |
| Review | Recompute; do not rubber-stamp a student PDF |
| Explain | Viva without new scalars |
| Report | Lab numerical + library plots |

## UI construction

For localhost schematics (series RLC sheet, confirm topology), load **`skills/ui-diagrams/SKILL.md`**. Write `graph.json` from `skills/ui-diagrams/examples/rlc_graph.json`; validate with `scripts/check_ui_diagram_artifacts.py`. `render-figure` does not replace an empty canvas.

## Do not

Auto-spice unmatched text. Invent a circuit PNG. Treat MATLAB Copilot as SPICE.

## Spawn

Host-native name: `ee-circuits`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/circuits/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `circuits`
- Sibling packs: electronics (devices vs network), power (three-phase), maths (Laplace transients)
