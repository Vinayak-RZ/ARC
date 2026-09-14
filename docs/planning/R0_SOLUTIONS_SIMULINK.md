# R0 solutions — host-agent catalog + Simulink mediation

Landscapes: [`host-agent-catalog-landscape.md`](../../research/notes/host-agent-catalog-landscape.md), [`simulink-toolkit-mediation.md`](../../research/notes/simulink-toolkit-mediation.md). Prior: [`R0_SOLUTIONS.md`](R0_SOLUTIONS.md) (pack specialists + MATLAB).

## Recommendation

1. Canonical EE specialist cards in `hosts/agents/` (12 names + INDEX). OpenMontage analog: domain catalog in the product tree; host dirs are install targets.
2. `electrical-engineer hosts install` copies those cards into the **homework** Cursor/Codex/Claude agent dirs. Never this product `.cursor/`.
3. Cards optimized for host spawn: inherit model/MCP, local same-checkout only, no nested Task, no `/in-cloud` worktrees.
4. Kernel MATLAB MCP client passes `--extension-file` when `EE_SIMULINK_TOOLS_JSON` points at toolkit `tools.json`. New activity `run-simulink-if-present`. Fail closed to `CD-SIMULINK-PLANT`.
5. Host `tools/list` still has no MATLAB/Simulink names. Live MATLAB Later.

## Rejects

- 48–88 SDLC role agents (the “77 skills” orchestrators)
- EE cards in product `.cursor/agents/`
- H5 Python specialist fan-out
- Host-attached Simulink Agentic Toolkit
- New capability ids
- Minting checked plants from a CI stub

## ADR impact

- **Amend ADR-0015:** catalog path `hosts/agents/`; Cloud spawn law; `ee-simulink` as 12th card.
- **ADR-0017:** Simulink toolkit kernel-mediated. Supercedes ADR-0016 “Simulink Later” for the attach path only; live licensed desktop stays Later.

## Catalog pattern ids

MCP-PENDING (`recommend_recipe` unreachable this session). Cite OpenMontage agent-first + Cursor subagent isolation.
