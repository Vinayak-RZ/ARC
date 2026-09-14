# R0 solutions — pack specialists + MATLAB mediation

**Status:** Closed 2026-09-14. A1 must cite this file.  
Gate 0: [`GATE_0_SKILLS_MATLAB.md`](GATE_0_SKILLS_MATLAB.md).  
Landscapes: [`pack-specialist-spawn-landscape.md`](../../research/notes/pack-specialist-spawn-landscape.md), [`matlab-mcp-mediation-landscape.md`](../../research/notes/matlab-mcp-mediation-landscape.md).

## Working hypotheses

Planning-turn sketch (confirm or replace):

1. Kernel stdio MCP client behind `run-matlab-if-present`; host never lists MATLAB tools.
2. Canonical specialist law in `hosts/adapters/`; `electrical-engineer hosts install` copies per-pack wrappers into the **homework** `.cursor/agents/`, `.codex/agents/`, `.claude/agents/`.
3. No EE agents in this product repo’s coding `.cursor/`.
4. Retrieve scaffold empty (heading contract only).
5. Simulink Agentic Toolkit Later.

## Evidence

Vendor docs 2026-09-14: Cursor subagents (markdown YAML), Codex subagents (TOML), Claude Code agents (markdown YAML). MATLAB MCP Server five tools, `new`/`nodesktop`/`disable-telemetry`, single-seat licence. mcp-proxy does not filter tools. `matlab.engine` and REST/MPS are extra products. H5 runtimes (LangGraph, A2A) remain forbidden.

## Recommendation

**Keep the working hypotheses.** Implement them.

| Decision | Keep or change |
|----------|----------------|
| Kernel MCP client | **Keep.** No host MATLAB MCP. Fail closed if missing. |
| hosts/adapters + install | **Keep.** Per-pack thin wrappers from one body. Skills-only remains the default path; spawn for large/parallel pack work. |
| No EE agents in product `.cursor/` | **Keep.** |
| Retrieve scaffold empty | **Keep.** Specialist must still *call* retrieve and treat miss as visible. Do not dump `knowledge/`. |
| Simulink Later | **Keep.** P0 `.m` evaluate/run is enough. |

FR20 peer dual-MCP stays a **clamp** if a student attaches MATLAB MCP anyway (scalars still `unchecked`). It is not the recommended attach.

## ADR impact

- **ADR-0015** (pack specialists): host-native custom agents; per-pack wrappers; install into homework; at most two live children; CLI/MCP/UI never spawn; skills short + knowledge links; H5 rejected.
- **ADR-0016** (MATLAB mediation): kernel NDJSON stdio client; flags `session-mode=new`, `nodesktop`, `disable-telemetry=true`; stub speaks `initialize` + `tools/call`; no new host verb; no `mcp` PyPI dep unless a stop fails; never store passwords.

## Open spikes

- Exact protocolVersion the Go MATLAB binary negotiates (stub should echo 2024-11-05 / 2025-*).
- Whether Cursor’s `.codex/agents/` compatibility path parses Codex TOML or only markdown — emit both formats.
- Chat/Work pack spawn still blocked on Skills-over-MCP verify (not this graph’s P0).
