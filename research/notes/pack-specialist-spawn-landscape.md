# Pack-specialist spawn landscape (Cursor / Codex / Claude Code)

## Purpose

Answer: how do Cursor, Codex, and Claude Code get **ready-made undergraduate EE pack specialists** (method + cross-links + empty `retrieve` scaffold) **without** a custom multi-agent runtime (H5 forbidden). This note is the spawn half of R_SURVEY. It reuses, not copies, [`host-first-class-attach.md`](host-first-class-attach.md), [`harness-landscape.md`](harness-landscape.md), [`agentic-kernel-2026.md`](agentic-kernel-2026.md), [`hosts/adapters/`](../../hosts/adapters/), and the spawn map in [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) §0.3.

Retrieved vendor pages: 2026-09-14.

## Problem

Arc is a **domain kernel**: rented hosts own the inner loop; Python owns engines, gates, and `unchecked`. Students (and host agents) must load **pack method** — Kirchhoff-before-SPICE, capability ids, at-most-two packs — without dumping `knowledge/ug-ee/**` into the system prompt.

The product already ships:

- Short pack skills (`skills/<pack>/SKILL.md`) plus a root skill.
- One **generic** adapter prompt per host under `hosts/adapters/{cursor,codex,claude}/pack-specialist.md`. The parent names the pack.
- An encyclopedic knowledge tree. This graph’s retrieval is an **empty scaffold** (visible miss, no RAG over `knowledge/` yet).
- Spawn map: the **rented host** may start **at most two** pack specialists (maths may take the second slot). CLI, MCP, and UI **never** spawn. Handoff is `run_id` + `./runs/<id>/` (or `children/`). Parent writes `argument.md`. Same EE MCP. Children must not mint checked numbers or skip UI confirm.

What is missing is a **portable install** so Cursor / Codex / Claude Code discover those specialists as **named, spawnable agents** in the student’s **homework** repo — not in this product’s coding `.cursor/` (SDLC skills live there; EE packs must not).

H5 falsifier (PID / PRD FR19): a Python process that interviews, plans, and fans out specialists. Google A2A, LangGraph, CrewAI, and an owned Task tool are that class.

ChatGPT **web** is not a host. Chat/Work does not claim pack spawn until Skills-over-MCP is verified on a desktop install. Cloud subagents and git worktrees are **off** for this graph (Gate 0): specialists must share the parent checkout so `./runs/<id>/`, localhost UI, and stdio MCP stay on one machine.

## Solution families

| Family | Mechanism | Who owns spawn | Context cost | Portable to Cursor / Codex / Claude | H5 risk | Evidence URL |
|--------|-----------|----------------|--------------|-------------------------------------|---------|--------------|
| **Host-native custom subagents** | Named agent files the host’s Task / subagent UI can pick. Isolated child window; parent gets a summary. | **L0 host** (Cursor Agent tool, Codex spawn, Claude `Task`) | Child window is extra tokens; parent stays clean. Cheap vs dumping 10 packs. | **Yes** — all three ship custom agents in 2026. Formats differ (see next section). Cursor also reads `.claude/agents/` and `.codex/agents/` for compatibility. | **None** if Arc never starts the child. Matches spawn map. | https://cursor.com/docs/subagents |
| **Skills-only progressive disclosure** | `SKILL.md` name+description always-on (~100 tokens); body on match; `references/` one level down. No child agent. | **Nobody spawns.** Main host loads pack skill on domain match. | Lowest. Anthropic: keep body under ~500 lines; metadata first. | **Yes** — Agent Skills spec is shared (`SKILL.md`). Codex `$skill` / skills dir; Cursor skills; Claude skills. | **None.** Method only; gates stay in Python. | https://agentskills.io/specification |
| **Skills-over-MCP** | MCP server lists `skill://` resources (`skills/list`, `skills/get`, `resources/read`). Host that lacks a project `SKILL.md` tree still gets method. SEP-2640; OpenAI shipped a scanner before the SEP merged. | Host still owns any spawn. Server **serves files**, does not fan out agents. | Catalog is small; full `SKILL.md` on demand. Same disclosure as filesystem skills. | **Partial.** Codex/ChatGPT plugins import MCP-served skills. Cursor + Claude Code already read local `skills/`. Chat/Work is the gap this family fills. | **None** if we only serve markdown. **H5** if the MCP server starts child loops. | https://www.arcade.dev/blog/skills-over-mcp-explained/ |
| **One generic specialist + pack argument (today’s adapters)** | One body per host: “load the pack the parent named.” Parent prompt carries `pack=` + `run_id`. As-built: `hosts/adapters/*/pack-specialist.md`. | **L0 host**, if the student copied the generic file. Discovery is weak: Task tools match **descriptions**, not runtime arguments. | One agent schema in the picker. Pack skill still loaded on demand. | **Yes**, but the host may never auto-delegate “circuits” vs “control” because there is only one description. | **None.** Same spawn map. | https://cursor.com/docs/subagents |
| **Per-pack thin wrappers from one body** | Canonical handoff+law in `hosts/adapters/`. Install generates `ee-circuits`, `ee-control`, … files whose YAML/TOML `description` names the pack; body is the shared specialist law + “load `skills/<pack>/SKILL.md`”. | **L0 host.** Picker sees one row per pack; still **at most two** live children. | N descriptions in the agent list (small). Only 1–2 bodies enter a child window. | **Yes** if an installer emits Cursor `.md`, Codex `.toml`, Claude `.md` from one source. Cursor markdown ≠ Codex TOML — do not share one file. | **None** if generation is files-on-disk, not a Python orchestrator. | https://developers.openai.com/codex/subagents |
| **Custom multi-agent runtime / A2A (reject)** | Arc-owned loop: LangGraph, CrewAI, Google A2A (`message/send`, Agent Cards), ADK `RemoteA2aAgent`, a Python fan-out. Message bus instead of run-dir files. | **Our process.** That is the H3/H5 falsifier. | High (second loop, extra schemas, bus state). | False portability: we would reimplement three hosts poorly. | **Forbidden (H5).** A2A is agent-to-agent; MCP is agent-to-tool. We need the latter. | https://a2a-protocol.org/latest/ |
| **Tool-search / Code Mode** | Do not enumerate 2,500 tools. Cloudflare `search()` + `execute()` (~1k tokens). HEART/ToolFace: retrieve tools at inference. Anthropic PTC / code-execution-with-MCP for **reads**. | Host loop unchanged. We shrink **ACI**, not specialists. | Fixes MCP tool tax. Does **not** teach KCL or spawn a circuits child. | Portable as an MCP shape later. Not how Task/subagent pickers work today. | **None** on **read** verbs. **High** if PTC wraps spice/label writes. | https://blog.cloudflare.com/code-mode-mcp/ |
| **Plugin marketplaces** | Bundle skills + agents + MCP into `.cursor-plugin/`, `.claude-plugin/`, `.codex-plugin/` and list them in a marketplace.json. Student `/plugin install`. Agent Plugins 1.0 is a vendor-neutral `plugin.json` + `skills/` + `mcp.json`. | Still the **host** after install. Marketplace is distribution, not a runtime. | Same as the files it unpacks. | **Yes in principle** (all three have marketplaces in 2026). Manifests are **not** the same file. Cross-harness repos exist (community), but they are extra packaging. | **None** as packaging. **H5** if a plugin ships an orchestration server. | https://cursor.com/docs/reference/plugins |

Skills vs subagents (vendor split, all three hosts agree in prose): **skills = method** any agent can load; **subagents = isolated worker** with its own window and (optionally) tool limits. EE needs **both**: short pack skills for the main host, plus at most two spawned specialists on large jobs. Do not encode Kirchhoff only inside a subagent — then a skills-only student has no method. Do not spawn a specialist for a one-unknown divider — Cursor’s own docs say use a skill for single-purpose work.

## Per-host file formats (2026)

Install targets are the **homework** (or user-global) tree. Never this product repo’s coding `.cursor/`.

### Cursor — `.cursor/agents/*.md` (YAML frontmatter)

Docs: https://cursor.com/docs/subagents

| | |
|--|--|
| Paths | Project: `.cursor/agents/`. User: `~/.cursor/agents/`. Also scans `.claude/agents/` and `.codex/agents/` (Claude/Codex compatibility). On name clash, `.cursor/` wins. |
| File | Markdown. YAML frontmatter then prompt body. |
| Fields | `name` (optional; else filename), `description` (Task-tool hint — this is how auto-delegate works), `model` (`inherit` or a model id, optional `[effort=high]`), `readonly`, `is_background`. |
| Built-ins | Explore, Bash, Browser — not EE packs. Do not collide with those names. |
| Cloud / isolation | `/in-cloud` and isolated worktrees get a **different** checkout and MCP from `cursor.com/agents`, not local stdio. **Off** for EE specialists (Gate 0). Handoff `./runs/<id>/` would miss. |
| Skills vs agents | Skills: `.cursor/skills/<name>/SKILL.md`. Agents: `.cursor/agents/<name>.md`. A circuits **skill** is always-on method; a circuits **agent** is the spawnable child. |

Minimal shape:

```markdown
---
name: ee-circuits
description: UG EE circuits pack specialist. Use for KCL/KVL, phasors, transients. Load skills/circuits. Same EE MCP. Do not mint checked ohms.
model: inherit
---
(canonical body: one pack, run_id handoff, no nested spawn)
```

### Codex — `.codex/agents/*.toml`

Docs: https://developers.openai.com/codex/subagents

| | |
|--|--|
| Paths | Project: `.codex/agents/`. User: `~/.codex/agents/`. Built-ins: `default`, `worker`, `explorer`. A custom file with the same `name` wins. |
| File | **Standalone TOML**, not markdown. Codex treats it as a config layer for the spawned session. |
| Required | `name`, `description`, `developer_instructions` (the body). |
| Optional | `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config` (inherit from parent if omitted — **prefer inherit** so the child keeps `electrical-engineer` MCP). |
| Caps | `[agents]` in `config.toml`: `enabled`, `max_concurrent_threads_per_session`, default model/effort. Product spawn map still caps **two** EE packs even if Codex would allow more. |
| ChatGPT Work | Hosted subagents; **no** local sandbox / local MCP. Not an EE pack host. Codex **view** on desktop shares `~/.codex/config.toml` with CLI. |

Minimal shape:

```toml
name = "ee_circuits"
description = "UG EE circuits pack specialist. Use for KCL/KVL, phasors, transients."
developer_instructions = """
(canonical body)
"""
```

Do not expect Cursor to execute this TOML as a first-class Cursor agent; Cursor’s compatibility scan of `.codex/agents/` is documented next to **markdown** agent files. Emit **both** `.cursor/agents/*.md` and `.codex/agents/*.toml`.

### Claude Code — `.claude/agents/` (YAML frontmatter)

Docs: https://code.claude.com/docs/en/sub-agents

| | |
|--|--|
| Paths | Project: `.claude/agents/` (walks up from cwd; closest `name` wins). User: `~/.claude/agents/`. Recursive subfolders allowed; identity is the `name` field, not the path. |
| File | Markdown + YAML frontmatter. Body = system prompt (child does **not** get full Claude Code system prompt). |
| Required | `name`, `description`. |
| Useful optionals | `model: inherit`, `skills: [arc, circuits]` (preload — **full** skill body injected; keep the list to root + **one** pack), `mcpServers: ["electrical-engineer"]` or inherit, `disallowedTools` if we want to block nested `Task`. `isolation: worktree` — **do not set** (breaks run-dir handoff). `background` — parent should wait for evidentiary files; prefer foreground. |
| Plugins | Plugin agents ignore `hooks`, `mcpServers`, `permissionMode`. Fine for later marketplace; v1 copy files into project `.claude/agents/`. |
| Skills | `.claude/skills/<name>/SKILL.md`. Skill frontmatter `agent:` can fork into a named subagent; inverse is subagent `skills:` preload. For EE, **preload one pack**, do not dump the tree. |

`/agents` wizard is gone as of Claude Code v2.1.198; edit files on disk.

### Shared install contract (all three)

1. Canonical **text** lives in `hosts/adapters/` (one body per host dialect, or one body + thin templates).
2. Install **into the homework repo** (or `~/.<host>/agents/`):
   - `.cursor/agents/ee-<pack>.md`
   - `.codex/agents/ee_<pack>.toml`
   - `.claude/agents/ee-<pack>.md`
3. Pack set this graph: **10 cores + maths + `_cross`** (no electives). Wrapper count ≤ 12. Live children **≤ 2**.
4. Each wrapper: load root skill + **one** `skills/<pack>/SKILL.md`; call **same** EE MCP; handoff `run_id` + `./runs/<id>/`; parent writes `argument.md`; no nested specialists; no checked ohms; no skipped UI confirm; `retrieve` when a citation is needed; **empty retrieve is visible**; **do not paste** `knowledge/ug-ee/**`.
5. Skills stay short. Cross-links are paths (`knowledge/ug-ee/<pack>/INDEX.md`, optional one-level `skills/<pack>/reference/`), not dumped chapters.
6. Product repo `.cursor/` stays coding SDLC. `docs/hosts/cursor.md` already forbids copying EE packs there.

## Recommendation

**Ship files the three hosts already spawn. Do not ship a runtime.**

1. **Canonical adapters** stay under `hosts/adapters/` (evolve today’s generic bodies so they name the empty-retrieve law and knowledge **links**). That is the source of truth for specialist law.
2. **Install into homework** `.cursor/agents/`, `.codex/agents/`, `.claude/agents/` as **per-pack thin wrappers** generated from that one body. Descriptions must include pack keywords so Task auto-delegate works. This is family “per-pack wrappers” + family “host-native custom subagents.”
3. **Keep skills-only as the default path.** Main host loads root + at most two pack `SKILL.md` files without spawning anyone. Spawn is for large / parallel pack work (e.g. circuits + maths), not for every question. Cursor’s own table: skill for one-shot method; subagent for isolated multi-step work.
4. **Do not put EE agents in this product’s `.cursor/`.** Homework or `~/.cursor/agents/` only.
5. **Skills stay short; knowledge tree is linked, not dumped.** Progressive disclosure (Agent Skills spec): metadata → `SKILL.md` → one-level reference → `retrieve`. This graph’s retrieve is an **empty scaffold** — the specialist must still *call* it and treat a miss as visible, not invent a page number and not slurp `knowledge/`.
6. **Skills-over-MCP** is the Chat/Work attach (already in host-first-class-attach). Not required to unblock Cursor/Codex/Claude Code spawn. Do not claim Chat/Work pack spawn until a desktop Chat install proves `resources/read` on served skills.
7. **Code Mode / tool-search** is the later answer to MCP tool tax (`search`+`execute` on **reads**). It does not replace pack agents. Do not PTC spice/label.
8. **Plugin marketplaces** are a later distribution wrapper around the same files (three manifests). Not this graph’s identity. Copy/symlink is enough for v1.
9. Cap **two** concurrent EE specialists in adapter prose even when Codex `max_concurrent_threads_per_session` is higher. CLI / MCP / UI never grow a spawn verb.

Today’s “one generic + pack argument” remains a valid **fallback** if a host cannot list 12 agents, but it is not the ready-made picker story. Wrappers are cheap files; they are not a second product.

## Rejects

| Reject | Why |
|--------|-----|
| Custom multi-agent runtime, LangGraph, CrewAI, Temporal, an Arc Task server | H5. PID H3 falsifier; FR19; ARCHITECTURE §0.3. |
| Google **A2A** / ADK remote agents / Agent Cards | Agent-to-agent bus. We need MCP (agent-to-tool) + host-native spawn + filesystem handoff. |
| Python specialist orchestrator inside CLI, MCP, or UI | Same falsifier. No `spawn_pack` MCP tool. |
| EE agents inside **this** repo’s `.cursor/` | Collides with coding SDLC. `docs/hosts/cursor.md` item 7. |
| Dumping `knowledge/ug-ee/**` into agent bodies or always-on prompts | Opposite of progressive disclosure; blows context; stale vs the tree. |
| One MCP tool per node; wrapping MATLAB MCP as a peer the host calls for checked numbers | Tool tax; FR20 mediation is a different landscape note. |
| ChatGPT **web** as a host; Chat/Work pack spawn before Skills-over-MCP verify | No local stdio; no project agents tree. |
| Cursor **cloud** subagents, Claude `isolation: worktree`, Codex hosted Work agents as EE specialists | Different checkout / no local ngspice / no `127.0.0.1` UI. Gate 0: cloud subagents and worktrees **off**. |
| Nested specialist spawn; more than two live packs; children writing `argument.md` | Spawn map. Parent owns the viva. |
| Encoding gates only in markdown | Skills are not an ACL (`agentic-kernel-2026.md`). `unchecked` stays in Python. |
| Elective packs as spawnable agents this graph | Gate 0: 10 cores + maths + `_cross` only. |
| Shipping a public plugin marketplace as the v1 install | Extra manifests, review queues, SHA pins. Copy from `hosts/adapters/` is enough. Revisit after wrappers work in three homework trees. |

## Sources

Vendor / primary (retrieved 2026-09-14 unless noted):

- [Cursor — Subagents](https://cursor.com/docs/subagents) — `.cursor/agents/*.md` YAML; also `.claude/agents/` and `.codex/agents/`; skills vs subagents table — reliability: primary
- [Cursor — Plugins reference](https://cursor.com/docs/reference/plugins) — `.cursor-plugin/plugin.json`, `agents/` in plugins, marketplace.json — reliability: primary
- [OpenAI — Codex subagents](https://developers.openai.com/codex/subagents) — `.codex/agents/*.toml`; required `name` / `description` / `developer_instructions`; built-ins `default`/`worker`/`explorer` — reliability: primary
- [OpenAI — Codex plugins](https://developers.openai.com/codex/plugins) — plugin directory in Work/desktop Codex; not Chat/IDE/mobile — reliability: primary
- [OpenAI — Build / package Codex plugins](https://developers.openai.com/codex/build-plugins) — `.codex-plugin/plugin.json` — reliability: primary
- [Claude Code — Subagents](https://code.claude.com/docs/en/sub-agents) — `.claude/agents/` YAML; `skills` preload injects **full** skill; `isolation: worktree` — reliability: primary
- [Claude Code — Skills](https://code.claude.com/docs/en/skills) — `SKILL.md`; `context: fork` / `agent:` — reliability: primary
- [Claude Code — Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) — `.claude-plugin/marketplace.json` — reliability: primary
- [Agent Skills specification](https://agentskills.io/specification) — progressive disclosure levels; ≤500-line `SKILL.md`; one-level references — reliability: primary
- [Anthropic — Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — metadata then body then files — reliability: primary
- [Anthropic — Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — domain folders; no nested refs — reliability: primary
- [Anthropic — Skills explained](https://claude.com/blog/skills-explained) — skills vs subagents vs MCP (2026-03-05) — reliability: primary
- [Arcade — Skills over MCP](https://www.arcade.dev/blog/skills-over-mcp-explained/) — OpenAI shipped scanner; SEP not necessarily merged — reliability: secondary
- [MCP SEP-2640 Skills Extension](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2640) — `skill://`, `skills/list`, `skills/get` — reliability: primary (draft SEP)
- [Cloudflare — Code Mode](https://blog.cloudflare.com/code-mode-mcp/) — `search()` + `execute()`, ~1k tokens vs enumerating APIs — reliability: vendor
- [A2A protocol](https://a2a-protocol.org/latest/) — agent-to-agent; complementary to MCP, not a substitute for host Task — reliability: primary

This repo (reuse, not vendor):

- [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) §0.3 spawn map — at most two; CLI/MCP/UI never spawn
- [`docs/PRD.md`](../../docs/PRD.md) FR19
- [`docs/PID.md`](../../docs/PID.md) H3/H5
- [`docs/hosts/cursor.md`](../../docs/hosts/cursor.md), [`openai.md`](../../docs/hosts/openai.md), [`claude-code.md`](../../docs/hosts/claude-code.md)
- [`hosts/adapters/`](../../hosts/adapters/) — today’s generic specialist + pack argument
- [`research/notes/host-first-class-attach.md`](host-first-class-attach.md) — Skills-over-MCP for Chat/Work; pack load map
- [`research/notes/harness-landscape.md`](harness-landscape.md) — hosts already have subagents; do not pick a fourth harness
- [`research/notes/agentic-kernel-2026.md`](agentic-kernel-2026.md) — domain kernel; Code Mode on reads; skills ≠ ACL
- [`docs/planning/GATE_0_SKILLS_MATLAB.md`](../../docs/planning/GATE_0_SKILLS_MATLAB.md) — cores+maths+`_cross`; empty retrieve; cloud/worktrees off

## Confidence

Overall confidence for this note: **high** on formats and the H5 reject; **medium** on Skills-over-MCP completeness for Chat/Work and on whether Cursor’s `.codex/agents/` compatibility path parses Codex TOML or only markdown.

Host-native custom agents are documented by all three vendors on 2026-09-14. The spawn map and “no EE files in product `.cursor/`” are already accepted product law. Per-pack wrappers are a file generation choice, not a new runtime. Confidence would drop if a host stopped loading project agent files, or if Chat/Work were later required to spawn packs without MCP resources.
