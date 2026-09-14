# Claude Code

First-class host. Same kernel contract as Cursor, Codex, and ChatGPT desktop.

1. Point Claude Code MCP at stdio command `electrical-engineer mcp`
   (user `~/.claude.json` or project `.mcp.json`).
2. Attach `skills/<pack>/SKILL.md` as project or user skills. Load the pack
   that matches the assignment; do not dump every pack into always-on context.
3. Use fully qualified tool names when several MCP servers are present
   (`electrical-engineer:list_workflows`).
4. `run_workflow` never blocks on a human gate. Use the localhost UI for
   confirm. Target split ACI: [`../PRD.md`](../PRD.md) FR17
   (`simulate_attachment`, `propose_composition`). Large jobs: `plan.md`
   first (FR23). Do not run mega YAML that includes `solve-explain` on this
   host path.
5. Host-native subagents (Task) may call the same EE MCP. We do not ship a
   custom multi-agent runtime (FR19). Run
   `electrical-engineer hosts install --into <homework> --host claude`
   (or copy
   [`../../hosts/adapters/claude/pack-specialist.md`](../../hosts/adapters/claude/pack-specialist.md)).
   At most two pack specialists. Handoff is
   `run_id` + `./runs/<id>/`. Parent writes `argument.md`.
6. Claude Code is optional. The CLI works without it.
7. Do **not** add MATLAB MCP beside Arc. Arc mediates MATLAB when the binary
   is installed. Peer scalars stay unverified until Arc recomputes them
   (FR20). [`../ON_THE_HARNESS.md`](../ON_THE_HARNESS.md).
