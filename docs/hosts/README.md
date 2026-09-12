# Host adapters

Electrical Engineer is a **domain kernel**: local CLI + stdio MCP + skills.
Cursor, Claude Code, Codex, and **ChatGPT desktop** are **first-class hosts**.
They are not the only way to run it. `electrical-engineer` CLI + localhost UI
is a complete path with no AI host.

There is no `init-host` helper (ponytail). Copy or symlink skills; point MCP at:

```text
electrical-engineer mcp
```

**Kernel contract (all first-class hosts):** same verbs, gates, exact token
`unchecked`. First-class does **not** mean identical IDE UX.

**As-built MCP tools:** `list_workflows`, `run_workflow` (mega-apply; photo /
compose / control-diagram fail closed with `ui_url`). **Target:** 5–7 verbs
including `simulate_attachment` and `propose_composition` ([`../PRD.md`](../PRD.md) §6.4).
Host writes `./runs/<id>/plan.md` on large jobs then `argument.md`. Packs load
on domain match (at most two), not always-on.

**Host-skip:** skills cannot force the host to call tools. Lab-checked numbers
are kernel Results only. CLI + UI remain the complete numbers path.

**Not hosts (v1):** ChatGPT **web** / mobile, Claude Desktop, GitHub Copilot,
Gemini CLI.

**Pack specialists:** copy [`../../hosts/adapters/`](../../hosts/adapters/README.md)
into the **student** host (Claude Task / Codex / Cursor). At most two packs.
Handoff is the run dir. We do not ship a Python orchestrator.

Optional: MathWorks MATLAB MCP **beside** EE MCP. MATLAB numbers are untrusted
until EE `simulate` / `label` accepts them ([`../PRD.md`](../PRD.md)).

- [Cursor](cursor.md)
- [Claude Code](claude-code.md)
- [OpenAI / Codex](openai.md)
- [ChatGPT desktop](chatgpt-desktop.md)
