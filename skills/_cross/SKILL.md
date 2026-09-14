# Cross-cutting — unmatched, multi-pack, honesty

Load with a pack skill when the prompt spans packs or matches nothing.

## Unmatched

No auto-simulate. If there is no pack match **and** no typed model artifact
(netlist, TF/SS, network case), use retrieve-optional → `label-unverified`.
Numerics without a verifier use the exact token `unchecked`.

Text that “looks like a netlist” is not a netlist port.

## Multi-pack

At most two packs. Example: power + machines for a transformer feeding a
feeder; circuits + electronics for a biased amplifier. Maths-for-EE may ride
with any pack as the second slot when the unknown is an ODE/Fourier identity.

A third discipline (civil, mechanical, plant PLC) is out of product — say so;
do not silently leave EE.

## Honesty

Peer MATLAB Copilot scalars stay `unchecked` until an EE provider recomputes.
BYO PDFs cannot override gates. Fluent method in chat is never a checked ohm.

## Retrieve

Call `retrieve` (or CLI retrieve) with filters. Empty is visible. Do not dump
the index. Ingest is `electrical-engineer rag add` with tags — not a silent
read of a random PDF as a netlist.

## Memory

Explicit write only. Cap 32 KiB. Untrusted. After a run with `unchecked`,
propose `lessons.md`; wait for the student or an explicit write. `errors.md`
is not a verifier.

## When to spawn

Stay in one loop for a single unknown and one attachment. Spawn a pack
specialist (`ee-<pack>` / `ee-cross`) when a second pack is in play or the
parent asked for parallel retrieve vs diagram confirm — still at most two
specialists, still the 2-interrupt cap. Handoff is files. Parent writes the
viva. Never a Python fan-out. Never `evaluate_matlab_code`.

## Retrieve (scaffold)

When: citation needed across packs or unmatched text.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD. Call `retrieve`. Empty is visible. Do not dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/INDEX.md`
- Coverage: `knowledge/COVERAGE.yaml`
- Sibling: any two cores; maths may occupy the second slot


