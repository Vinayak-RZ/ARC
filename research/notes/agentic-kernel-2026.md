# Agentic kernel 2026 — harvest for Electrical Engineer

## Purpose

Translate an owner-uploaded architecture memo (written for a different product, a manufacturing handoff kernel nicknamed Stamped) plus three 2026 blogs into Electrical Engineer vocabulary. Answer: what is a **domain kernel**, how it wraps a rented frontier loop, and which patterns to steal versus refuse. This note does not import Stamped ADRs, SKUs, plant/PO freeze, or a manufacturing UI.

## Findings

Claim | Evidence | Confidence
--- | --- | ---
“Kernel,” “studio,” and “harness” name three different products; mixing them reverses H3 | Owner-uploaded memo §1; Osmani Agent Harness Engineering; `docs/PID.md` H3 | high
Electrical Engineer is the **domain kernel** class: host owns the loop; we own engines, skills, gates that cannot be talked past | Memo §0; OpenMontage; this repo’s H3 | high
Attach order in 2026 is **CLI inner loop**, then Code Mode / programmatic tool calling on **reads**, then **MCP outer loop** | Firecrawl MCP vs CLI; Cloudflare Code Mode; Anthropic PTC | high
A decent model plus a great *host* harness beats rebuilding the harness | Osmani Apr 2026 | high
Naive MCP (one tool per REST/node) burns context; Code Mode cut 2,500 endpoints to `search()` + `execute()` (~1,000 tokens vs ~1.17M) | Cloudflare Feb 2026 | high
Skills are method, not an ACL; gates belong in code | Thoughtworks; Karajan; `docs/ARCHITECTURE.md` runner law | high
2026 models are good at reading a whole packet, arguing a route, interviewing, writing a brief; they remain bad at catalog identity, numbers, and self-verify | Memo §8 | high
Chopping professional work into schema-constrained micro-calls **starves** the model; EE’s analog is `run_workflow` executing a YAML DAG that includes `solve-explain` | Memo §8; `src/electrical_engineer/mcp/server.py`; `nodes/photo.py` `solve-explain` | high
Steal **no-bypass write path** from executive kernels (`kernel.submit()`, IGX). Do not steal their loop | KAIJU arXiv 2604.02375; agent-kernel | med
Headless YAML replay stays as **eval rollback**, not a second chat product | Memo §7; `docs/ARCHITECTURE.md` eval | high

### Three products (do not mix)

| | Domain kernel | Executive kernel | Agentic studio |
|---|---|---|---|
| Examples | OpenMontage, ChemCrow-shaped tools, **Electrical Engineer** | KAIJU, agent-kernel | OpenMontage-as-product, Reel Studio |
| Loop owner | Frontier **host** (Claude Code, Codex, Cursor) | Their runtime; LLM is a stateless planner | Host plus project memory, timeline, approvals |
| What they sell | Domain engines + artifacts + gates | Scheduling, dispatch, `kernel.submit()` | A production workspace |
| Steal | Shape WS-G already leaned toward (H3 / topology C) | Structural no-bypass writes; impact ≤ min(intent, clearance, scope) | Attach shape (project, checkpoints, MCP verbs) |
| Do not steal | “Intelligence only in markdown” | **The loop itself** (that is H5) | Video timeline / ChatGPT-clone UI |

**Domain kernel, in one line:** wrap the rented core agentic loop so it can do a specific job, without becoming the loop.

**Executive kernel, in one line:** the LLM plans a graph; compiled code schedules and gates; tool schemas cannot run themselves. If the host can call a function behind the gate, the invariant is dead.

**Studio, in one line:** a project the host drives through MCP (open, queue, review, export). Analog for GTM attach, not for EE’s localhost UI.

Public category for Electrical Engineer stays **lab** (`notes/naming-and-positioning.md`). Internal class tightens from “harness-native domain system” to **domain kernel**. “Studio” remains a named reject.

### Three 2026 blogs

1. **Addy Osmani — Agent Harness Engineering** (Apr 2026). Agent = model + harness. Failures are configuration. Rent Claude Code / Codex / Cursor rather than rebuild them. Pair with **Own the Outer Loop**: the host runs the inner loop; humans and *our gates* own verification. Independent check, not the model’s “done.”

2. **Cloudflare — Code Mode** (Feb 2026). Wrap APIs as `search()` + `execute()` so the model writes code against typed APIs; intermediates stay out of the context window. Sibling: Anthropic **code execution with MCP** and first-party **programmatic tool calling (PTC)**. This is the 2026 answer to wrapping every node as an MCP tool.

3. **Firecrawl — MCP vs CLI in 2026** (Jun 2026). Inner loop = CLI (the model already knows `gh` / shells). Outer loop = MCP (no shell, OAuth, audit, multi-user). Steinberger’s “mcp were a mistake” was ergonomics, not a kill shot. Do not MCP-wrap commands the model already types. MCP earns its keep when there is no man page — EE simulators, `unchecked`, photo confirm, eval gold.

Cite, do not feature: Thoughtworks (a skill is not an anti-corruption layer); Rebecca de Prey (API vs MCP); polar-mcp ADR 0001 (Python core, thin adapters).

### What works / what does not (EE translation)

**Works**

| Pattern | Why | EE hook |
|---|---|---|
| Durable domain core; CLI / MCP as thin adapters | polar-mcp; de Prey | `src/electrical_engineer/` engines; CLI and MCP call `execute()`, they are not the physics |
| Few always-on tools; rest deferred | Code Mode; HEART/ToolFace | Today MCP has two verbs; the *write* verb is too coarse, not too many |
| CLI inner, MCP outer | Firecrawl | `electrical-engineer run/eval/ui` for students and hosts with a shell; stdio MCP for Cursor tool lists |
| Skills = method; tools = reach + ACL | Thoughtworks | `skills/*/SKILL.md` teach Kirchhoff-before-SPICE; nodes mint numbers |
| Propose → validate → apply | GraSP; do not trust an LLM DAG | Router never invents a spice DAG; `compose-from-parts` is the only new-graph path |
| Code-shaped **reads** (PTC later) | Cloudflare, Anthropic PTC | RAG retrieve, list workflows, maybe “ask the student” — not spice writes |
| Structural write path | KAIJU / agent-kernel | Spice/control/load-flow, `label-unchecked`, photo confirm, compose — host cannot skip |
| Headless replay | Eval gold | YAML runner scores `Vout = 5.0`; not a second chat |

**Does not work**

| Anti-pattern | Why | EE refusal |
|---|---|---|
| 45–664 tool schemas in context | Token tax; worse selection | Do not 1:1 wrap every registered node as MCP |
| Owned harness | Osmani; PID H5 | Do not build Electrical-Engineer-owned Claude Code |
| Gates only in `SKILL.md` | OpenMontage purity is wrong for Kirchhoff | `unchecked`, unmatched, photo confirm stay predicates in Python |
| MCP wrapping `gh` / `kubectl` | Model already knows CLI | MCP for spice/gates/eval, not for `ls` |
| Unvalidated LLM DAG | GraSP helps; trusting ToolWeave-style plans does not | Named YAML or `compose-from-parts --advanced`; never session-invented `run_spice_guess` |
| JIT session-invented domain verbs | Two-speed JIT is for a *coding* harness | Host may not define `lookup_vout_guess` |
| Chopping the professional job into micro-calls | Memo §8 starve | Do not hide viva/method inside `solve-explain` on the host path |

### Spend 2026 intelligence — do not starve it

Stamped’s mistake: nine schema-constrained LLM steps so the model never saw the whole manufacturing study. 2026 models are good at the briefing; they are still bad at SKUs and self-verify.

EE analog of starve: MCP `run_workflow` / CLI `execute(wid)` runs the whole YAML DAG, including `solve-explain` as a registered node (`nodes/photo.py`). Pack skills are four-line stubs (`skills/circuits/SKILL.md`). The pre-runner classifier is a tiny LLM call when the id is omitted. The host never does the viva.

**Spend the host on:** choose KCL vs nodal, interview the student for missing data, write the explanation, read a netlist and argue whether the topology matches the problem, retrieve which chapter, repair a derivation after a check fails.

**Clamp in engines:** presenting `Vout` as checked, inventing a spice DAG, confirming a photo topology without the UI, MATLAB numbers, load-flow scalars, minting a fluent essay as a verified number.

Headless YAML runner stays for gold replay. That is rollback, not a second chat product. `solve-explain` on the local-model path stays for students without a host (PID Q-S2). It is not the host-path brain.

### Two-band leave-behind (direction)

1. **Evidentiary** — spice/control/load-flow numbers, citations, `unchecked`, gold diffs. Deterministic assemble. Floor = node outputs + gates.
2. **Engineering argument** — host-authored explanation, labeled so it cannot mint scalars. May cite the evidentiary band.

Do not merge the bands. A viva that silently writes `Vout = 5` into `summary.json` as checked is the EE analog of laundering inference as a cited extract.

### Always-on vs never-a-host-tool (sketch)

Reads OK for later PTC: RAG retrieve, `list_workflows`, maybe list open clarifying questions.

Direct only, never PTC: spice / matlab / load-flow / control writes, `label-unchecked` if it can mint checked numbers, photo confirm, compose, eval apply.

Never a host tool that bypasses gates: inventing a spice DAG, presenting fluent `Vout` as checked, confirming topology without UI.

Five to seven **always-on** verbs is the 2026 catalog size (memo §3, Artifi 9-vs-664). Today we have two MCP tools; one of them is a mega-apply. The repair is to split the ACI, not to explode it. Concrete verb list lives in `notes/domain-kernel-layering.md`.

### Supporting papers (cite, not the reading list)

- HEART / ToolFace (arXiv 2609.01736) — retrieve tools at inference; do not enumerate 25k schemas.
- GraSP (arXiv 2604.17870) — compile skills to a typed DAG; 2–3 focused skills beat a dump.
- HyperAgent — schema-level hypergraph for composition.
- KAIJU (arXiv 2604.02375) — plan vs execute; IGX. **Clearance** maps to EE gates, not to a prompt.

Improveness / Unagent vocabulary in the uploaded memo is harvest-only: frozen physics in the kernel, thin HostPort adapters, filesystem evidence already in `./runs/<id>/`. Not RSI. Not a second OS.

## Open questions

- Owner accept of D17 (domain kernel layering, spend/clamp, two-band, ACI split) on the vision lock sheet.
- Whether Code Mode / PTC is a 2026 research freeze or a later attach once read tools proliferate (memo default: do not start there).
- Exact 5–7 verb names — proposed in the layering note, not locked here.

## Sources

- Owner-uploaded memo “Agentic kernel 2026 — architecture memo” (2026-09-12, written for Stamped / manufacturing handoff; informs that product’s ADR 0038; not an Electrical Engineer ADR) — retrieved 2026-09-12 — reliability: primary
- [Addy Osmani — Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) — retrieved 2026-09-12 — reliability: secondary
- [Addy Osmani — Own the Outer Loop](https://addyosmani.com/blog/own-the-outer-loop/) — retrieved 2026-09-12 — reliability: secondary
- [Cloudflare — Code Mode](https://blog.cloudflare.com/code-mode-mcp/) — retrieved 2026-09-12 — reliability: vendor
- [Anthropic — Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) — retrieved 2026-09-12 — reliability: primary
- [Anthropic — Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) — retrieved 2026-09-12 — reliability: primary
- [Firecrawl — MCP vs CLI in 2026](https://www.firecrawl.dev/blog/mcp-vs-cli) — retrieved 2026-09-12 — reliability: secondary
- [Thoughtworks — Your agent skill is not an anti-corruption layer](https://www.thoughtworks.com/insights/blog/generative-ai/your-agent-skill-not-anti-corruption-layer) — retrieved 2026-09-12 — reliability: secondary
- [KAIJU](https://arxiv.org/abs/2604.02375) — retrieved 2026-09-12 — reliability: paper
- [HEART / ToolFace](https://arxiv.org/abs/2609.01736) — retrieved 2026-09-12 — reliability: paper
- [GraSP](https://arxiv.org/abs/2604.17870) — retrieved 2026-09-12 — reliability: paper
- [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/PID.md`](../../docs/PID.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/domain-system-architecture-patterns.md`](domain-system-architecture-patterns.md) — retrieved 2026-09-12 — reliability: primary
- [`src/electrical_engineer/mcp/server.py`](../../src/electrical_engineer/mcp/server.py) — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this note: high

The three-product split and attach order rest on primary 2026 blogs plus this repo’s H3 lock. Spend-vs-clamp is a judgment transferred from another vertical; it would drop if owner lock keeps `solve-explain` as the host-path brain, or if PTC on spice writes is later demanded.
