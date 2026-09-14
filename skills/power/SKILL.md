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
4. Missing provider → `unchecked`, never a fluent “converged” voltage.

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
