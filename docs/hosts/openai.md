# OpenAI / Codex

First-class host: Codex CLI, Codex IDE extension, and the **Codex view**
inside the ChatGPT desktop app. Same kernel contract as Cursor and Claude Code.

ChatGPT desktop **Chat / Work** is documented in [`chatgpt-desktop.md`](chatgpt-desktop.md).
ChatGPT **web** is **not** a host.

1. Configure MCP in `~/.codex/config.toml` (shared with ChatGPT desktop):

   ```toml
   [mcp_servers.electrical_engineer]
   command = "electrical-engineer"
   args = ["mcp"]
   ```

   Or Codex’s MCP add command, equivalent stdio.

2. Reuse the same `skills/` markdown (Codex skills path / `$skill`). Do not
   vendor a second recipe catalog.

3. Local OpenAI-compatible daemons are `EE_LOCAL_LLM_URL` on the **CLI** path
   only. This host uses its own loop.

4. Completeness of v1 **does** require documenting this host; it does **not**
   require every student to subscribe to Codex. CLI + UI remains complete.

5. As-built tools: `list_workflows`, `run_workflow` (never waits). Target:
   [`../PRD.md`](../PRD.md) FR17 (`simulate_attachment`,
   `propose_composition`). Large jobs write `plan.md` first (FR23). Host
   writes `argument.md`.
6. Optional pack specialist: `electrical-engineer hosts install --into <homework> --host codex`
   (or copy
   [`../../hosts/adapters/codex/pack-specialist.md`](../../hosts/adapters/codex/pack-specialist.md)).
   At most two packs; same MCP; parent writes the viva. Not a second product.
7. Do **not** add MATLAB MCP in `config.toml`. Arc mediates MATLAB when
   installed. Peer scalars stay unverified until Arc recomputes them (FR20).
   [`../ON_THE_HARNESS.md`](../ON_THE_HARNESS.md).
