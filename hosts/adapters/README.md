# Host adapters — pack specialists

Copy these **into the student’s host**, not into this repo’s coding `.cursor/`.
The main host (Claude Code / Codex / Cursor) owns spawn. Arc
does **not** ship a multi-agent runtime (FR19, H5).

Install per-pack wrappers into a **homework** tree:

```text
electrical-engineer hosts install --into /path/to/homework --host all
```

That writes `.cursor/agents/ee-<pack>.md`, `.codex/agents/ee_<pack>.toml`,
`.claude/agents/ee-<pack>.md`. Canonical law: [`specialist-body.md`](specialist-body.md).
Do not run this against this product repo’s `.cursor/`.

| Host | Copy to (student machine) | File |
|------|---------------------------|------|
| Claude Code | project or user agents (Task) | [`claude/pack-specialist.md`](claude/pack-specialist.md) |
| Codex | Codex agent / skill spawn path | [`codex/pack-specialist.md`](codex/pack-specialist.md) |
| Cursor | Task / student project skills | [`cursor/pack-specialist.md`](cursor/pack-specialist.md) |

**Spawn map:** at most two pack specialists. Maths may occupy the second slot.
Handoff is `run_id` plus `./runs/<id>/` (or `children/`). Parent writes `argument.md`.
Same EE MCP. Same `unchecked` law. Live verbs include `propose_composition`.
Chat/Work: do not claim this spawn.

Optional host-side reminder (compaction stays the host): [`hooks.md`](hooks.md).
