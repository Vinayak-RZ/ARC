# Host-agent catalog landscape (OpenMontage vs SDLC fleets)

## Purpose

Answer: how should Arc put **named EE specialists** in this repo so Cursor / Codex / Claude (including Cursor Cloud) can spawn them, without an Arc-owned loop (H5) and without polluting product `.cursor/` (coding SDLC).

Retrieved vendor pages: 2026-09-14.

## Problem

Skills = method in the parent window. Subagents = isolated child sessions the **rented host** starts. Arc already generates wrappers at `hosts install` time. Clone search does not find `ee-circuits` cards. README does not count spawnable agents.

The owner asked to look at **OpenMontage** and at “77 specialised agents.”

## Solution families

| Family | Mechanism | In-repo placement | Host spawn | H5 risk | Fit |
|--------|-----------|-------------------|------------|---------|-----|
| **OpenMontage agent-first** | Coding assistant *is* the orchestrator. Python is tools + persistence. Domain markdown lives in `skills/`, `AGENT_GUIDE.md`. Host files point at that catalog. | Product tree, not coding `.cursor/` | L0 host | None | **Chosen analog** |
| **Canonical agent cards + install** | Commit Cursor-format `hosts/agents/ee-*.md` + INDEX. `hosts install` copies into homework `.cursor/agents/`, `.codex/agents/`, `.claude/agents/`. | `hosts/agents/` searchable | L0 host Task | None if Arc never starts the child | **Chosen shape** |
| **SDLC orchestrator fleet** | 48–88 generic roles (PM, UX, DevOps) + 77 skills. Example: Prathmesh2000/cursor_agent-orchestrator (48 agents, 77 skills); KS-Cursor-Orchestrator (~88 agents synced to `~/.cursor/agents/`). | Often dumped into user `.cursor/` | Host Task | None at runtime; **wrong domain** | **Reject** |
| **Product `.cursor/agents/`** | EE cards next to coding SDLC agents | This repo `.cursor/` | Cursor Cloud would spawn EE children on the product repo | Low, but SDLC collision | **Reject** (cursor.md item 7) |
| **Arc supervisor+workers** | LangGraph / CrewAI / A2A | Python | Our process | **H5 forbidden** | **Reject** |

OpenMontage counts **layers separately** (pipelines / tools / skills), not one inflated agent number. Arc should count: undergraduate packs, spawnable specialists, named recipes.

Cursor Cloud `/in-cloud` and isolated worktrees get a **different checkout and MCP**. EE specialists must stay **local, same checkout** so `./runs/<id>/` and stdio MCP stay on one machine. Cards must say so.

## Per-host card fields (optimize for host spawn)

- Cursor: YAML `name`, `description` (Task auto-delegate), `model: inherit`. Not `is_background`. Not worktree isolation.
- Codex: `name`, `description`, `developer_instructions`; inherit parent MCP.
- Claude: YAML frontmatter + body; inherit tools; no nested Task.

## Recommendation

Commit **12** cards under `hosts/agents/` plus `INDEX.md`. Install into homework only. Do not copy 77 SDLC roles. Do not put EE cards in product `.cursor/agents/`.

## Sources

- https://github.com/calesthio/OpenMontage — agent-first; retrieved 2026-09-14
- https://cursor.com/docs/subagents — project vs user vs Cloud isolation
- https://github.com/Prathmesh2000/cursor_agent-orchestrator — 48 agents / 77 skills (SDLC, not domain)
- https://github.com/kscius/KS-Cursor-Orchestrator — ~88 agents synced to `~/.cursor/agents/`
- [`pack-specialist-spawn-landscape.md`](pack-specialist-spawn-landscape.md)
