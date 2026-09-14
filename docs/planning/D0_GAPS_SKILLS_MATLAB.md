# D0 gaps — pack skills + MATLAB mediation

**Status:** Closed 2026-09-14. B* nodes fill these. Authority: [`R0_SOLUTIONS.md`](R0_SOLUTIONS.md), [`GATE_0_SKILLS_MATLAB.md`](GATE_0_SKILLS_MATLAB.md).

## skills

Thin method bodies exist for 10 cores + maths + `_cross` (`skills/<pack>/SKILL.md`). Gaps:

- No `knowledge/ug-ee/<pack>/INDEX.md` or `COVERAGE.yaml` unit links
- No `## Retrieve (scaffold)` heading (When / Filters / Index: TBD)
- No spawn name (`ee-<pack>`)
- No sibling-pack pointers
- No explicit “EE MCP only; never `evaluate_matlab_code` / never host MATLAB MCP”
- Electives under `knowledge/ug-ee/electives/` must stay unskilled this graph

## hosts/adapters

Generic one-file specialists (`cursor|codex|claude/pack-specialist.md`). Gaps:

- No per-pack wrappers (`ee-circuits`, …)
- No `electrical-engineer hosts install --into <dir>`
- Bodies omit empty-retrieve law and knowledge **links** (not dumps)
- Product `.cursor/` must stay coding SDLC (already forbidden in `docs/hosts/cursor.md` item 7)

## MATLAB stub

`src/electrical_engineer/nodes/sim.py` `run_matlab_if_present` always `_missing("matlab")`. Gaps:

- No stdio NDJSON client (`matlab_mcp.py`)
- No `EE_MATLAB_MCP_BIN` / `MW_MCP_SERVER_MATLAB_ROOT` / timeout
- No fake MCP stub tests (`initialize` + `tools/call`)
- Missing-MATLAB path must stay fail-closed (`tests/unit/test_sim_seams.py`)

## FR20 peer path

Host docs still allow attaching MathWorks MCP beside Arc (`docs/hosts/cursor.md` item 6, `docs/hosts/README.md`, `docs/ON_THE_HARNESS.md` “Coming next”). UI chip still says `MATLAB · coming next`. Happy path this graph: host → Arc MCP only; Arc → MATLAB MCP internally. Peer dual-MCP remains a clamp (scalars `unchecked`), not the install.

## UI / trials / harden

- Chip copy not yet “optional, via Arc when installed”
- No host-harness log (`T1_HOST.md`)
- No impeccable critique of the live UI this graph
- Whole-tree ponytail-review not yet run on this branch
