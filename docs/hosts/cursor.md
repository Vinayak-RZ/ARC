# Cursor

First-class host. Same kernel contract as Claude Code, Codex, and ChatGPT desktop.

1. Copy or symlink pack skills from `skills/*/SKILL.md` into `.cursor/skills/`
   (or the Cursor skills path you already use). Prefer the **root** skill plus
   the pack you are working in (progressive disclosure; FR19).
2. Add a project or user MCP stdio server in `.cursor/mcp.json` whose command
   is `electrical-engineer mcp` (from a venv where the package is installed).
3. As-built tools: `list_workflows`, `run_workflow`. Photo / compose / C5 ids
   **fail closed** and return a `ui_url` — they never wait on stdio. Target
   verbs: [`../PRD.md`](../PRD.md) FR17 (`simulate_attachment`,
   `propose_composition`, …). Host writes `plan.md` on large jobs (FR23) then
   `argument.md`; do not mega-apply `solve-circuit-problem`.
4. Persistent UI is `electrical-engineer ui` on `127.0.0.1:8765`.
5. Cursor is optional. CLI + UI without Cursor is a complete v1 path.
6. Do **not** add MATLAB MCP to `.cursor/mcp.json`. Arc calls MATLAB MCP
   internally via `run-matlab-if-present` when `matlab-mcp-server` is on the
   machine. Peer MATLAB / Copilot scalars stay `unchecked` until Arc
   recomputes them (FR20 clamp). See [`../ON_THE_HARNESS.md`](../ON_THE_HARNESS.md).
7. Do **not** copy EE packs into this product repo’s `.cursor/skills/`
   (that tree is coding SDLC). Symlink root + active pack into **your**
   homework project or `~/.cursor/skills`.
8. Optional student `AGENTS.md` (homework repo, not this repo): ≤10 lines —
   this is an EE lab; load the root skill; large jobs plan then execute;
   host writes the viva; numbers only via EE MCP or `unchecked`.
9. Optional pack specialist: `electrical-engineer hosts install --into <homework> --host cursor`
   (or copy
   [`../../hosts/adapters/cursor/pack-specialist.md`](../../hosts/adapters/cursor/pack-specialist.md)).
   Never into this product repo’s `.cursor/skills/` or `.cursor/agents/`.
   At most two packs. Handoff is the run dir.
