# EM / fields pack

Load for UG fields: electrostatics, magnetostatics, Maxwell in integral form
as taught to EE, uniform plane waves, lossless transmission lines. Not a
research EM programme. Not CST/HFSS as the product path (`CD-EM-HFSS`).

## Any question in this pack

1. Name the configuration (charge, current, boundary, line) and the unknown
   (E, H, D, B, Γ, VSWR, Smith — UG).
2. Use `fields-analytic` / `algebraic-check` (closed form, phasor TEM).
3. Full-wave numeric solvers are cannot-do; label `unchecked` rather than
   invent S-parameters.
4. `lumped-circuit-sim` is the wrong default for “find E at P.”

## Genres

Derive and explain are common. Simulate means analytic/numeric identity, not
SPICE, unless the problem reduced to a lumped model the student stated.

## Spawn

Host-native name: `ee-em`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/em/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `em`
- Sibling packs: circuits (lumped vs field), power (lines at study level), maths (vector calculus)
