# Electrical-Engineer — Agent instructions

This repository vendors [cursor-config-coding](https://github.com/Vinayak-RZ/cursor-config-coding) at `.cursor/` (rules, skills, MCP). Pin: see [`.cursor/VENDOR.md`](.cursor/VENDOR.md). Do not duplicate the shared SDLC in this file — point at skills by name.

Product: **Electrical-Engineer** — a UG EE co-solver (named workflows, simulators, persistent local UI) that can do the coursework an undergrad electrical engineer is asked to do.
GitHub: [`Vinayak-RZ/Electrical-Engineer`](https://github.com/Vinayak-RZ/Electrical-Engineer).

## What this repo is

A coding workspace for building and evolving that co-solver (analysis, circuits, signals, power, labs, and related undergrad EE workflows). Prefer deterministic tools and verified calculations over free-form LLM guesses when correctness matters. Authority: [`docs/PID.md`](docs/PID.md), [`docs/PRD.md`](docs/PRD.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). Do not invent capability ids; use the registry in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) §0 or add a [`docs/CANNOT_DO.md`](docs/CANNOT_DO.md) row.

## Current status

Product execution graph **complete through H1** on `cursor/ee-product-execution-9e9d`: CLI, YAML runner, localhost UI, MCP, recipes, eval, boot + trials. Authority remains [`docs/PID.md`](docs/PID.md), [`docs/PRD.md`](docs/PRD.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/UI.md`](docs/UI.md). Proposed overlays **D19** (capability-first), **D20** (host loop + persist/observe/spawn), **D21** (student-facing lab workbook; no raw `.md`/`.json`; no reasoning-mode node). Providers (ngspice, YAML, FastAPI, …) are this-pass freezes, not the thesis. Do not invent EE capabilities that are not in those docs or in [`docs/CANNOT_DO.md`](docs/CANNOT_DO.md). This file is **coding SDLC**, not the student lab prompt.

---

# Coding — Agent Mode

**ponytail → nawab-plans (lite default in Plan mode) → spec-kit for greenfield → implement → validate → commit.**

- **Code:** read `.cursor/skills/ponytail/SKILL.md` before any edit (lazy senior ladder). Always-on: `ponytail.mdc`.
- **Plan mode:** load `nawab-plans` at **lite** unless asked for standard/project or the work is multi-package. Lite template: `.cursor/skills/nawab-plans/PLAN.template.lite.md`. See `planning.mdc`.
- **Greenfield / specs-first:** `speckit-*` after `.specify/` exists. Guide: [docs/cursor-config/SPEC_KIT.md](docs/cursor-config/SPEC_KIT.md) (pin **v1.0.6**).
- **graph-engineering:** only if named. Never auto-chain. Not graphify.
- **README:** `readme` router — this repo’s landing is product-readme (OSS co-solver); internals companion is `extensive-readme`.
- Inventory: [skills-manifest.json](skills-manifest.json)

## Architecture (when designing)

| Domain | Skill | Rule |
|--------|-------|------|
| Frontend / UI / Next.js | `frontend-architecture` | `frontend-architecture.mdc` |
| Backend / API / data | `backend-architecture` | `backend-architecture.mdc` |
| AI agents / LLM / tools | `agentic-system-design` | `agentic-systems.mdc` |
| Any major trade-off | `system-design-tradeoffs` | `trade-offs.mdc` |

For agent harness design, prefer `agentic-system-design` and the agent-patterns MCP ([docs/cursor-config/MCP_SETUP.md](docs/cursor-config/MCP_SETUP.md)). Config: `.cursor/mcp.json`.

## Git

Conventional commits after milestones (`git-commit-discipline.mdc`). Auto-push at **≥ 10** unpushed, or when asked.

## Companion repos

- [cursor-config-coding](https://github.com/Vinayak-RZ/cursor-config-coding) — source of the vendored `.cursor/`
- [cursor-config-buisness](https://github.com/Vinayak-RZ/cursor-config-buisness) — PM/GTM/research
- [cursor-config-design](https://github.com/Vinayak-RZ/cursor-config-design) — decks, video, visual
