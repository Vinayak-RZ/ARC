# Maths-for-EE pack

Load when the unknown is an EE-used identity: complex algebra, ODE/Laplace as
circuit or control setup, Fourier as a signals tool, numerical methods as
used in cores. Not a full CAS replacement (`CD-MATHS-CAS`).

## Any question in this pack

1. Name the identity class and how it attaches to an EE pack (second slot).
2. `algebraic-check` and/or `signal-analysis` (sympy when present).
3. If sympy cannot check it, `unchecked` — do not invent a residue.

## Genres

Usually solve/derive. Do not open `lumped-circuit-sim` for a Fourier integral
unless the student also asked a circuit question (then load circuits as the
other pack).

## Spawn

Host-native name: `ee-maths`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/maths/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `maths`
- Sibling packs: circuits, signals, control (second slot only)
