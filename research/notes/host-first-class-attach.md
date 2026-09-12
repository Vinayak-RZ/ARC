# Host-first-class attach (ChatGPT desktop, dual MCP, pack specialists)

## Purpose

Refine D14–D17 for the Proposed PRD: how ChatGPT **desktop** can share the same kernel contract as Cursor / Claude Code / Codex; how MATLAB as a second MCP must not mint checked numbers; how pack specialist skills load without dumping the corpus into context.

## Findings

Claim | Evidence | Confidence
--- | --- | ---
ChatGPT **desktop** (macOS/Windows) can add a STDIO MCP server; config is shared with Codex CLI / IDE | https://learn.chatgpt.com/docs/extend/mcp | high
ChatGPT **web** does not read local Codex/desktop MCP config, so it cannot run `electrical-engineer mcp` | OpenAI help; vendor MCP setup guides | high
Inside the ChatGPT desktop app, **Codex is a separate view** from Chat / Work | https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex | high
First-class for Chat/Work means the **same kernel contract** (verbs, gates, `unchecked`), not Cursor-class repo editing | plan intake; Osmani harness vs model | high
Chat/Work lack a reliable project `SKILL.md` tree; method should travel as MCP resources (Skills-over-MCP / skill resources) plus a terminal for CLI | Arcade Skills-over-MCP; Anthropic skills+MCP split | med
Skills = method; MCP = reach; progressive disclosure: short root `SKILL.md`, one-level pack references | https://claude.com/blog/skills-explained ; Anthropic skill best practices | high
Always-on tool schemas stay small (5–7). Named recipes reach spice/control nodes. Do not 1:1 wrap every node | Cloudflare Code Mode; HEART/ToolFace; `mcp/server.py` as-built | high
MathWorks ships MATLAB MCP / Agentic Toolkit. A host may run it **beside** EE MCP | https://github.com/matlab/matlab-mcp-server | high
EE kernel is the only path to a **checked** number. MATLAB MCP scalars are evidence until `simulate` / `label` accept them | `docs/PRD.md` FR2; dual-MCP intake | high
Pack specialists: root skill (triggers, verb map, unchecked law) plus `skills/<pack>/` loaded on domain match | Anthropic domain-specific skill folders; this repo’s pack tree | high
Product still works with **no** MATLAB and with **no** frontier host | PID Q-S2; CP-2 open | high

### ChatGPT desktop: three surfaces, one kernel

| Surface | Can run local EE MCP | Skills folders | First-class promise |
|---------|----------------------|----------------|---------------------|
| ChatGPT desktop **Chat / Work** | Yes (STDIO in Settings → MCP servers) | Weak / none | Same verbs + gates; method via MCP-served skills; CLI in a side terminal for `eval` / `ui` |
| ChatGPT desktop **Codex** view | Yes (shared `~/.codex/config.toml`) | Yes (`SKILL.md` / `$skill`) | Full inner loop: skills + MCP + CLI |
| ChatGPT **web** / mobile | No local stdio | No | **Not a host.** Student uses CLI + UI, or desktop |

Do not advertise “install Electrical Engineer in chatgpt.com.” That would silently drop simulators and `unchecked`.

Making Chat/Work first-class without lying about UX:

1. Document Settings → MCP servers → STDIO command `electrical-engineer mcp`.
2. Serve the root skill (and pack chapters on demand) as MCP resources so Chat/Work can load method without `~/.claude/skills`.
3. Tell the student to keep a terminal for `electrical-engineer ui` and `eval`. Chat is not the gold runner.
4. Codex view additionally gets copied/symlinked `skills/<pack>/SKILL.md` like Claude Code.

CLI-without-host remains complete, including local `solve-explain`. ChatGPT desktop is additive.

### Dual MCP: MATLAB is a peer, not a second truth

When the student has a MathWorks licence they may enable MATLAB MCP / Copilot **and** Electrical Engineer MCP on the same host.

| Source | What it is | May mint `unchecked: false` |
|--------|------------|------------------------------|
| EE `simulate` named recipe (`run-spice`, `run-python-control`, `run-matlab-if-present`, load-flow) | Kernel engine | Yes, if the node verified |
| EE `label` / `write-run-summary` | Gate | Yes only if a child verifier succeeded |
| MathWorks MCP / Copilot chat | Peer agent | **No.** Treat as untrusted evidence |
| Host fluent essay | Engineering-argument band | **No** |

Skill law for dual MCP: if MATLAB MCP returns a number, the specialist skill must call EE `simulate` (an EE engine recomputes). Until then the student-facing answer uses the exact token `unchecked`. `label` is a gate over child EE artifacts, not ingest of Copilot scalars. EE wrapping MATLAB internally (`run-matlab-if-present`) stays the preferred path when we can drive MATLAB ourselves. Peer MCP exists so the host can use MathWorks tools we do not wrap (Simulink editor, live scripts). It does not bypass gates.

Product and CI still work with **zero** MATLAB.

### Pack specialist load map

Anthropic pattern: a short overview skill plus domain files one level down, loaded only when the task matches.

```text
skills/
  SKILL.md                 # root: triggers, 5–7 verbs, unchecked law, when to retrieve
  _cross/SKILL.md          # unmatched, photo, compose, eval
  circuits/SKILL.md        # Kirchhoff-before-SPICE; named circuit recipes
  control/SKILL.md
  … remaining packs
  <pack>/reference/        # optional one-level-deep chapters; not dumped every turn
```

Always-on context: root skill + MCP tool schemas + optional current `./runs/<id>/` pointer.

On-demand: matching pack skill, then `reference/*.md`, then RAG `retrieve` (book/chapter/page). Never inject the textbook index into the system prompt.

Host-native subagents (Claude Code Task, Cursor, Codex) may all call the same EE MCP. v1 **ships** pack specialist **skills**, not a custom multi-agent runtime. `.claude/agents/` YAML is a later host-adapter file, not a v1 identity.

### Split ACI (target vs as-built)

As-built MCP (`src/electrical_engineer/mcp/server.py`): `list_workflows`, `run_workflow` (runs the whole YAML DAG, including `solve-explain`). Photo/compose/control-diagram fail closed with `ui_url`.

Target always-on verbs (names illustrative): `list_workflows`, `retrieve`, `clarify`/`open_ui`, `simulate` (named recipe id only), `label`/`summary`, `eval_run`. `run_workflow` remains headless/eval rollback, not the host-path viva.

### D14–D17 refinement (for the Proposed PRD)

- D14: keep product name Electrical Engineer.
- D15: public **lab**; internal **domain kernel**; mode co-solver.
- D16: topology C — host plans/explains; Python owns physics, gates, eval, UI.
- D17: four layers; CLI inner / MCP outer; ChatGPT desktop Chat/Work first-class via MCP + served skills; spend host on viva; clamp numbers; two-band artifacts; dual MATLAB MCP with EE as checked-number authority; pack specialists by progressive disclosure.

Does not reopen H5. Does not drop the YAML runner. Does not add Claude Desktop, Copilot, Gemini, or ChatGPT web as hosts.

## Open questions

- Exact MCP resource URIs for served skills (implementation after PRD accept).
- Whether ChatGPT desktop Chat honors MCP resources the same way Codex does (verify on a machine with the app; until then the PRD requires the contract and a CLI fallback).

## Sources

- [Model Context Protocol — ChatGPT Learn](https://learn.chatgpt.com/docs/extend/mcp) — retrieved 2026-09-12 — reliability: primary
- [ChatGPT Work and Codex — OpenAI Help Center](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) — retrieved 2026-09-12 — reliability: primary
- [Skills explained (Anthropic)](https://claude.com/blog/skills-explained) — retrieved 2026-09-12 — reliability: primary
- [Extending Claude with skills and MCP](https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers) — retrieved 2026-09-12 — reliability: primary
- [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — retrieved 2026-09-12 — reliability: primary
- [Arcade — Skills over MCP](https://www.arcade.dev/blog/skills-over-mcp-explained/) — retrieved 2026-09-12 — reliability: secondary
- [MATLAB MCP Server](https://github.com/matlab/matlab-mcp-server) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/domain-kernel-layering.md`](domain-kernel-layering.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/agentic-kernel-2026.md`](agentic-kernel-2026.md) — retrieved 2026-09-12 — reliability: primary
- [`src/electrical_engineer/mcp/server.py`](../../src/electrical_engineer/mcp/server.py) — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this note: high

Desktop MCP and the Codex-vs-Chat split rest on OpenAI docs. Skills-over-MCP as the Chat/Work method channel is a reasoned attach; confidence would drop if desktop Chat ignores MCP resources — the CLI+UI path still holds.
