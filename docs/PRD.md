# Product Requirements Document — Arc

**Status:** Proposed (2026-09-12). Supersedes Accepted D0 (2026-09-10) pending owner review.  
**Date:** 2026-09-12  
**Licence of this product’s code:** Apache License 2.0  
**Identity:** [`PID.md`](PID.md) (Proposed, same pass).  
**This pass does not implement MCP/skill code.** As-built vs target is explicit in §4.

---

## 1. Thesis, name, licence

**Thesis.** **Arc** turns a coding assistant into an undergraduate electrical engineer. It is an Apache-2.0, forever-open-source **domain kernel** that wraps a rented frontier agent loop (Cursor, Claude Code, Codex, ChatGPT desktop) so the student gets a checked assignment — method, numbers, viva — without us becoming a new harness. A branded **local CLI** and **persistent localhost UI** are a complete path with no AI host. The host plus pack skills compose the job; a **capability registry** is the physics contract; **providers** (simulators, sympy, RAG facade) are swappable; **short** physics attachments stay as replay; allowlisted capability graphs are **validated then run**. Mega YAML that includes `solve-explain` is not the host-path brain. Every in-bound UG question has a complete path: a provider checks the unknown, or the exact token **unchecked**. It is shaped by **real UG coursework** at Indian and global institutes. GATE is an eval instrument, not the product bound. PG, civil, and mechanical are out of the public promise.

| Field | Requirement |
|-------|-------------|
| Name | **Arc** (CLI/repo stay `electrical-engineer` / `Electrical-Engineer` this pass) |
| Repo | `Electrical-Engineer` |
| CLI | `electrical-engineer` (`run`, `workflows`, `mcp`, `eval`, `ui`, `rag`, `memory`) |
| UI | Persistent localhost workspace on `127.0.0.1` (critical surface). Chrome identity is the Arc icon (`assets/brand/arc-icon.png`). |
| Public one-liner | Turn your AI coding assistant into an undergraduate electrical engineer |
| Public category | Undergraduate electrical-engineering co-solver |
| Internal class | **domain kernel** (host owns the loop; we own capabilities, providers, skills, gates) |
| Mode | Co-solver (full working + answer + evidence, or exact token `unchecked`) |
| Licence | Apache-2.0 for *our* code; textbooks never redistributed in git |
| Commercial | Forever OSS in this repo; no paid tier |
| Geography | India first; global UG EE must not be a thin afterthought |

Rejected public nickname: “Agentic UG EE Studio”. “Bench” is not the public noun (EEBench.org; physical instrument benches).

## 2. Users and non-users

**Users (v1).** UG EE / EEE students, India first, including colleges without MATLAB-fluent TAs. Global UG students taking equivalent cores. Self-learners on the same UG cores. GATE/IES aspirants may use exam-style items; that does not make this a GATE-only product.

**Non-users (v1).** Faculty/TA product features. PG as a promised audience. Working plant / protection / tape-out engineers as the identity.

**Never.** Civil, mechanical, or manufacturing students as this product. Live PLC / plant actuation.

## 3. Goals, non-goals, v1 vs later

### Goals

- Help UG students finish **and understand** EE assignments: correct enough to use, explained enough for a viva, **visible** in a local UI.
- Run **locally** as a CLI without requiring any AI host. Capability providers (circuit sim, LTI, load-flow, algebraic-check) work with **no** model. A probeable viva on the CLI-without-host path needs a configured local model or BYO key (`solve-explain`); without a model the evidentiary band is still complete and the argument band is `unchecked` or omitted — that is honest, not a silent fail.
- Also run **inside** Cursor, Claude Code, Codex, and **ChatGPT desktop** under the same kernel contract (MCP + CLI; skills folders where the host loads them; MCP-served or pinned root skill on Chat/Work). ChatGPT **web** is not a host.
- Spend the host on method, viva, and missing-data interview. Clamp numbers, invented spice DAGs, and photo confirm in the kernel.
- Invoke **named workflows** a student understands; fall through to a short co-solver that never auto-simulates.
- Accept **BYO API keys**, **local models**, and **BYO textbooks** (tagged; inventoryable).
- Check numbers with tools when possible; use the exact token **unchecked** when not.
- Measure capability with `eval/gold/` tasks; GATE tags are one overlay, not the bound.

### Non-goals

- Electric Pi (H4) or a from-scratch agent harness (H5).
- Second git repo.
- PG public promise.
- Faculty LMS, tutor-default, paid hosting.
- Civil / mechanical / manufacturing packs.
- Shipping copyrighted textbooks or third-party exam PDFs in git.
- Replacing MATLAB, KiCad, or professional EDA.
- ChatGPT web, Claude Desktop, GitHub Copilot, Gemini CLI as v1 hosts.
- Claiming ChatGPT Chat has Cursor-class repo editing.

### v1 vs later

| Now (public promise) | Later (same repo, unpublished until promised) |
|----------------------|-----------------------------------------------|
| UG coursework **lab** (domain kernel) | Optional `--profile` for PG; not advertised |
| H3 CLI + MCP + **persistent localhost UI**; Cursor, Claude Code, Codex inner-loop, Chat/Work contract | HTTP MCP |
| Split host ACI (5–7 verbs including `propose_composition`); `run_workflow` as short-attachment / eval rollback | Code Mode / PTC on **reads** only if retrieve tools proliferate |
| Chat/Work method: pin root skill (pack-on-demand not claimed) | Skills-over-MCP implemented and verified on a desktop Chat install |
| Named circuits + control + **solve+explain for every curriculum pack** (capability path even when YAML is thin) | Deeper gold / BYOK |
| OSS verifiers first-class; MATLAB optional **engine** and optional **peer MCP** | Deeper Simulink when licence exists |
| Photo-to-netlist **stub** (UI confirm, no sim) | Simulate the confirmed netlist |
| `eval/gold/` layout + `electrical-engineer eval` | Larger gold bank (still licence-clean) |
| Pack specialist **skills** (progressive disclosure) | Host-adapter subagent YAML (`.claude/agents/` etc.) |

## 4. Shipped vs restructure

The kernel spine already exists. This PRD mostly **restructures** how the host talks to it. It does not ask for a new harness.

### Keep (as-built, still required)

| Piece | Where |
|-------|--------|
| H3: hosts own the LLM loop; CLI is not a unique harness | [`PID.md`](PID.md), [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Python 3.11+ CLI: `run`, `workflows`, `mcp`, `eval`, `ui`, `rag`, `memory` | `src/electrical_engineer/` |
| YAML DAG runner, short attachments as **capability bindings**, unmatched → `unmatched-cosolver`, never invent **capability or provider ids** | runner + [`WORKFLOWS.md`](WORKFLOWS.md) |
| Exact token `unchecked`; `label-unchecked` in code | `nodes/registry.py` |
| Photo/compose/control-diagram fail closed on MCP with `ui_url` | `mcp/server.py` |
| Persistent UI on `127.0.0.1`; student need not use Cursor | `electrical-engineer ui` |
| Gold eval CLI and `eval/gold/` layout | `electrical-engineer eval` (divider gold is not a live SPICE proof) |
| Registered sim seams: spice / python-control / load-flow / matlab-if-present | **this-pass providers** of capabilities (bodies may fail closed) |
| Tagged local RAG + memory markdown | CLI `rag`, `memory` |
| Pack skill files exist (`skills/<pack>/SKILL.md`) | pack method for every curriculum pack; root `skills/SKILL.md` names coverage law |
| Run dir `./runs/<id>/` is audit, not crash-resume | ARCHITECTURE Q29 |

Honesty about seams (keep the **contracts**, do not advertise them as proven gold engines): `run-spice` / `run-python-control` / `run-load-flow` / `run-matlab-if-present` are **this-pass providers**. As-built bodies may fail closed or set `ok` on import. `solve-explain` is not only an LLM node: `_solve_value` can mint `unchecked: false` (ohms/divider) — that mint is a **defect** under FR9/FR18/FR21, not a kept engine. CLI `run` with omitted id does **not** yet call the hybrid classifier (exits usage); the classifier is specified, not wired. Pack skills now carry UG method; capability→provider bind in the runner is a later code plan.

### Restructure (requirements in this PRD; code in a later plan)

| As-built | Target |
|----------|--------|
| MCP tools: `list_workflows`, `run_workflow` (whole DAG including `solve-explain`) | 5–7 always-on verbs including `propose_composition`; host writes the viva; `run_workflow` = short-attachment / eval rollback |
| Pack `SKILL.md` files are four-line stubs | Root skill + pack specialists with UG method + capability ids (done in docs). Optional one-level `reference/` still empty. Runner still names provider keys |
| `solve-explain` LLM **and** `_solve_value` minting checked ohms/divider | Host-path argument band; node must not mint checked; CLI-without-host essay only |
| Hybrid classifier specified; CLI omitted-id not wired | Wire classifier on CLI-without-host only; host composes via ACI |
| ChatGPT / OpenAI documented as Codex-shaped only; completeness “does not require this host” | ChatGPT **desktop** first-class; ChatGPT **web** excluded |
| MATLAB only as `run-matlab-if-present` | Also allow MathWorks MCP as a **peer**; EE still owns checked numbers |
| `summary.json` folds numbers + citations | Two bands: `evidentiary.json` seed (`summary.json` today) vs `argument.md` |
| Pre-runner classifier when id omitted | Host classifies when a host is present; small classifier stays for CLI-without-host |
| Router never invents a DAG; new graphs only `compose-from-parts` | Host may **propose** allowlisted **capabilities**; kernel binds providers, validates then runs; unmatched still cannot auto-spice |

## 5. Four-layer architecture (H3)

Normative detail: [`ARCHITECTURE.md`](ARCHITECTURE.md). Catalog: [`WORKFLOWS.md`](WORKFLOWS.md). Attach research: [`../research/notes/host-first-class-attach.md`](../research/notes/host-first-class-attach.md).

```text
Layer 0  Rented harness     Cursor / Claude Code / Codex / ChatGPT desktop
Layer 1  Attach             CLI inner · MCP outer · 5–7 ACI verbs · served skills on Chat/Work
Layer 2  Domain kernel      skills · capability registry · providers · short attachments · validator · gates · eval · stores
Layer 3  Surfaces           localhost UI · evidentiary.json · argument.md
```

No Layer 4. Eval stays in Layer 2; two-band files stay in Layer 3.

| Layer | Owns | Must not own |
|-------|------|----------------|
| 0 Host | Context window, permissions, the inner loop, the viva, write `argument.md` | Kirchhoff as truth, inventing capability ids, minting checked ohms, unique EE chat loop |
| 1 Attach | CLI, MCP verbs including `propose_composition`, skill load, optional MATLAB MCP | 1:1 wrap of every provider; PTC on physics writes; mega `run_workflow` as host-path viva |
| 2 Kernel | Capability registry, providers, validator, RAG, short YAML replay, `unchecked` | A second host-incompatible chat loop (H5); long YAML as the chat brain; locking the thesis to one simulator |
| 3 UI / artifacts | Confirm, plots, citations, two-band viewer | A ChatGPT-clone console; WAN bind; KiCad clone |

**Falsifier for H3:** if the CLI or UI grows a custom harness that hosts cannot share, stop and return to owner (that is H5). A Python multi-turn composition dialog **or a Python specialist fan-out** is that falsifier.

**Runner law (kept):** no model calls inside the DAG runner except through **registered nodes**, plus one **pre-runner** classifier when the workflow id is omitted **and no host is driving**. The DAG runner itself is deterministic. Short YAML attachments are **genre contracts** and **eval rollback**, not the professional-workflow brain.

**Spend / clamp.** Spend the frontier host on method, viva, and student interview. Clamp checked `Vout`, invented capability ids, photo topology, and MATLAB scalars unless they passed an EE provider. Host may propose an allowlisted **capability** graph; the kernel binds providers, validates then runs.

---

## 6. Agent interaction

This chapter is the host-path contract. It answers: who loops, what is in context, which tools exist, how the agent finds the rest, how RAG and simulation attach, and how other agents (pack specialists, MATLAB MCP) collaborate. Normative attach research: [`../research/notes/host-first-class-attach.md`](../research/notes/host-first-class-attach.md).

### 6.1 Who owns the loop

| Situation | Loop owner | EE kernel role |
|-----------|------------|----------------|
| Cursor / Claude Code / Codex / ChatGPT desktop Codex view | The **host** agent | Tools, skills, gates, artifacts |
| ChatGPT desktop Chat / Work | The **host** chat agent (weaker editor) | Same MCP verbs + served skills; CLI in a side terminal for `ui` / `eval` |
| No AI host (PID complete path) | None. CLI `run` / local `solve-explain` | Engines, YAML, UI, eval |
| ChatGPT **web** / mobile | Not supported | Student uses CLI + UI or desktop |

The host **plans** (and on a large job writes `plan.md` first), interviews the student, chooses KCL vs nodal vs phasor, then **executes** kernel verbs, and writes the **engineering-argument** band. The kernel never needs a second multi-turn chat product. Local `solve-explain` is the fallback brain when no host is configured. It is not the host-path viva.

### 6.2 Always-on context (every EE turn)

Feed **only**:

1. **Root skill** (`skills/SKILL.md`): triggers (this is an EE lab, not a generic coder), the 5–7 verb map, unmatched law, `unchecked` law, **coverage law**, plan-then-execute on large jobs. Keep this short (progressive disclosure).
2. **MCP tool schemas** for the always-on verbs (not every registered node).
3. **Optional pointer** to the current `./runs/<id>/` if the student already started a run.
4. Host-native project files the student already opened (assignment PDF, netlist). We do not auto-dump [`ARCHITECTURE.md`](ARCHITECTURE.md) or [`WORKFLOWS.md`](WORKFLOWS.md) into the system prompt.

Never always-on:

- The textbook corpus or the vector index
- Every pack `SKILL.md` (packs load on domain match, at most two)
- Full YAML of every recipe
- A `propose_composition` **graph body** in tool **results** (returns `run_id` + paths)
- Gold eval fixtures
- MATLAB Copilot system prompts

Token intent: root skill plus the always-on tool schemas stay small. Do not enumerate every node.

### 6.3 On-demand context (load when the task matches)

| Trigger | Load | How |
|---------|------|-----|
| Domain match (circuits, control, …) | `skills/<pack>/SKILL.md` | Host skill loader, or MCP resource (Chat/Work) |
| Specialist chapter | `skills/<pack>/reference/*.md` (one level deep from the pack skill) | Host reads the linked file; do not nest |
| Needs a citation or formula from a book the student has rights to | RAG `retrieve` with book/chapter/folder/domain filters | MCP read verb; max passages as today (3) |
| Continuing a run | `./runs/<id>/` evidentiary file + `argument.md` + netlist/plots | Host or CLI reads files |
| Eval | gold item + recipe id | `eval_run` / CLI `eval`, not chat paste of gold |

Empty RAG is **visible**. Do not silently proceed as if the book was retrieved.

### 6.4 Tools the host may call

**Always-on ACI (target, 5–7 verbs).** Names are illustrative; implementation is a later plan. As-built today is `list_workflows` + `run_workflow`.

| Verb | Kind | Direct | Notes |
|------|------|--------|-------|
| `list_workflows` | read | yes | Catalog. Host-path rows are **short attachments**; mega `solve-*`/`explain-*` marked rollback |
| `retrieve` | read | yes | Tagged RAG; citations evidentiary |
| `open_ui` / `clarify` | read (+ questions) | yes | MCP **never waits**. Returns `ui_url` |
| `simulate_attachment` | write | yes | Named **short** physics id only. Never `solve-explain` inside |
| `propose_composition` | write | yes | Graph of **capability ids and/or registered provider ids** + typed ports. `apply: false` validates and records `plan.md` (no physics run). `apply: true` validates then runs. Returns `run_id` + paths, not the graph body |
| `label` / `summary` | write | yes | Gate over child EE artifacts only (FR20). `check-numeric` also cannot ingest Copilot scalars |
| `eval_run` | write | yes | Gold replay. **CLI** on Chat/Work; not required as an MCP tool there |

`run_workflow` (as-built mega-apply) remains valid as **headless/eval rollback** and as `electrical-engineer run <id>` for **short** attachments. On the **host path** it must not own `solve-explain`.

**Never a host tool:** invent a capability or provider id; confirm photo topology without UI; present fluent `Vout` as checked; session-defined `lookup_vout_guess`; PTC on physics-write providers.

**Do not** wrap `run-spice`, `run-matlab-if-present`, `run-load-flow`, `retrieve-passage`, `solve-explain` as extra MCP tools. Capabilities are reached through the verbs above.

### 6.5 How the agent searches tools

1. Root skill lists the verbs and when to use them. Large jobs: write `plan.md` before write verbs.
2. `list_workflows` (or the skill’s attachment table) picks a **short** id (`simulate-circuit`, …), **or** the host calls `propose_composition`.
3. Pack specialist skill names verbs in fully qualified form (`electrical-engineer:simulate_attachment`) so hosts with several MCP servers do not miss them.
4. There is **no** v1 tool-search over 45 node schemas. Engine allowlist is server-side.

### 6.6 Simulation

- Physics attaches through **short named YAML attachments** or a **validated** graph of capabilities/providers ([`ARCHITECTURE.md`](ARCHITECTURE.md) §0 and §4–§6).
- Router **never invents capability or provider ids**. Unmatched → `unmatched-cosolver` only (no auto-simulate). Host-path unmatched has **no** `solve-explain`.
- New graphs: `propose_composition` (host; allowlisted capabilities; kernel binds providers and validates) **or** `compose-from-parts --advanced` (CLI; human-gated). Caps 16 nodes / 24 edges. `solve-explain` is not on the host-path allowlist. `lumped-circuit-sim` requires a **netlist artifact** on a typed port.
- `repair_max: 2` then `label-unchecked` or ask-human — never a fake pass.
- MCP simulation that would wait on a human **fails closed** with `ui_url` (preflight MATLAB / photo / `ask-human` on proposed graphs).
- Gold eval scores **evidentiary** artifacts (example: `Vout = 5.0` on divider-dc-01), not the essay.

### 6.7 RAG

- Local index. BYO PDFs/scans through the **ingest pipeline** (drop → gate → extract → chunk → index → retrieve). Inventory (`rag list`). Filters: book, chapter, folder, domain.
- Host path: `retrieve` is a **read verb**. CLI path: `retrieve-passage` node inside a named recipe. `rag add` / `memory` stay **CLI** (Chat/Work side terminal) until a later read-verb split.
- Citations: book + chapter + page the student has rights to use.
- Circuit-homework **photos** go through `photo-to-netlist` / `ingest-figure`, not RAG-as-netlist.
- BYO content cannot override gates or `unchecked` and cannot mint a capability.
- Do not inject top-k passages into the system prompt on every turn. Retrieve when the specialist skill says the claim needs a source.
- Empty retrieval is **visible**.

### 6.8 Collaboration with other agents

**Pack specialists (v1 we ship).** One root skill plus per-pack skills. The host (or its native subagents) loads the matching pack. We do **not** ship a custom multi-agent runtime. Claude Code Task / Cursor / Codex subagents may all call the **same** EE MCP; that is the host’s feature, not a second product. Spawn **map:** at most two pack specialists (maths may take the second slot), started only from the host’s Task/subagent UI. The CLI, MCP, and UI never fan out specialists. Handoff is `run_id` + `./runs/<id>/` files. Copy adapter prompts from [`../hosts/adapters/`](../hosts/adapters/). Chat/Work does not claim pack spawn until Skills-over-MCP.

**MATLAB (optional peer).** The host may run MathWorks MCP / Copilot **beside** EE MCP when the student has a licence. Skill law: MATLAB MCP numbers are **untrusted evidence**. They become checked only if EE `simulate` / `label` accepts them (including via `run-matlab-if-present`). Product and CI work with **zero** MATLAB.

**Not v1:** multi-student shared cloud projects; faculty agents; plant-floor agents; MATLAB Copilot as the product identity.

### 6.9 Two-band artifacts

| Band | Who writes | May contain | Must not |
|------|------------|-------------|----------|
| Evidentiary | Engines + gates | Numbers, `.cir`, plots, citations, `unchecked`, gold diffs | Host judgment presented as SPICE |
| Engineering argument | Host, or local `solve-explain` fallback | Method, viva, labeled inference | Minting a checked scalar |

`write-run-summary` / `summary.json` is the seed of `evidentiary.json` (**one writer**; after rename, alias or replace — never dual live files). A host-authored `argument.md` next to it must not flip `unchecked` to false. Kernel also writes `observation.json` (or seed fields): capability/provider ids, node ok, `unchecked_reason`, retrieve empty — **not** a second numeric band and **not** gold.

### 6.10 Per-host attach (summary)

| Host | Skills | EE MCP | CLI | First-class |
|------|--------|--------|-----|-------------|
| Cursor | `.cursor/skills` or project skills | `.cursor/mcp.json` stdio `electrical-engineer mcp` | yes | yes |
| Claude Code | project / user skills | `.mcp.json` stdio | yes | yes |
| Codex CLI / IDE / desktop Codex view | Codex skills / `$skill` | `~/.codex/config.toml` | yes | yes |
| ChatGPT desktop Chat / Work | Served via MCP resources | Settings → MCP servers, STDIO | side terminal | yes (same **contract**, weaker editor) |
| ChatGPT web / mobile | no | no local stdio | yes, separately | **no** |
| CLI + UI only | n/a | n/a | yes | yes (complete path) |

Detail: [`hosts/README.md`](hosts/README.md).

---

## 7. Functional requirements

FR17–FR23 are the host-path restructure. FR24 is observation (D20).

**FR1 Co-solver.** Default behaviour is full working + final answer + assumptions. Not hint-first tutor. Not faculty mode. Mathematics in answers is valid LaTeX plus a plaintext fallback.

**FR2 Label unchecked.** If a number did not come from an **EE kernel** verifier, the student-facing answer **and** the evidentiary run summary must contain the exact token `unchecked`. Synonyms are not the contract. Never present it as a simulation or lab result. Peer MATLAB MCP / Copilot output does not satisfy this FR until it re-enters EE `simulate` / `label`.

**FR3 Branded CLI.** A student can run `electrical-engineer` on Linux, macOS, or Windows (`pip` / `uv`, Python 3.11+) for the same EE tasks without an AI host. Commands: `run`, `workflows`, `mcp`, `eval`, `ui`, `rag`, `memory`. Deterministic engines work with no model. Local `solve-explain` (argument band) requires a configured local model or BYO key; without one, skip the essay and keep the evidentiary band.

**FR4 Host adapters.** The same kernel **contract** (verbs, gates, `unchecked`) loads in **Cursor**, **Claude Code**, **Codex** (CLI / IDE / desktop Codex view), and **ChatGPT desktop Chat / Work**. ChatGPT **web** and **mobile** are not hosts. First-class means that contract, not identical IDE UX and not identical skill loaders.

- Codex view is the OpenAI **inner-loop** host (skill folders + MCP + CLI), same shape as Cursor / Claude Code.
- Chat/Work is first-class **contract** with a weaker editor: MCP STDIO + pinned root skill until Skills-over-MCP is verified on that app; `ui` / `eval` in a side terminal. Pack-on-demand (FR19) on Chat/Work is not claimed until resources work. Do not count ChatGPT desktop as a fifth harness separate from Codex view — they share `~/.codex/config.toml`.
- This **repo’s** root `AGENTS.md` is the Arc **coding** SDLC. Do not overload it with student lab instructions. Student Cursor attach is [`hosts/cursor.md`](hosts/cursor.md): symlink **root + active pack** into the **student’s** `~/.cursor/skills` or their homework repo, never into this repo’s `.cursor/skills/` (vendored coding skills).

**FR5 Model adapters.** Support (a) the host’s subscription model, (b) user API keys, (c) local models. Architecture must not lock a single vendor. The DAG **runner** does not own a hidden LLM loop.

**FR6 Local-first.** Default is on-device CLI + local files + UI bound to `127.0.0.1`. No product cloud. No silent upload of PDFs or keys.

**FR7 Portable core.** Skills + MCP are the portable layer. The CLI wraps them with a **deterministic YAML workflow runner**. The CLI must not become a unique multi-thousand-line agent loop.

**FR8 Ug policy.** Public profile is `ug-coursework`. Out-of-pack questions: try with **unchecked** or state out of enabled packs — not a silent PG mode.

**FR9 Eval runner.** `electrical-engineer eval` (and `--pack`) against [`../eval/gold/`](../eval/gold/README.md). Gold items name a `recipe_id`. CI must not require MATLAB. `EE_ALLOW_ALL` may skip gates in CI; it must **not** disable `unchecked`. Gold scores the **evidentiary** band, not the essay. `unchecked: false` in gold is legal **only** when `summary.verifier` is an EE engine on the FR20 allowlist. `solve-explain` must not mint checked values (it may write the argument band). As-built gold that scores an LLM/node-minted `value` as checked is a **defect to fix in a later eval plan**, not a PRD exception.

**FR10 Named workflows.** Default CLI path is a **short physics attachment** from [`WORKFLOWS.md`](WORKFLOWS.md) (`electrical-engineer run simulate-circuit`) **or** a capability graph. Explicit id skips classify. On the CLI-without-host path, if id omitted, one classifier call; if top-1 and top-2 are within 0.15, ask the student. On the **host path**, the host calls `simulate_attachment` or `propose_composition` (FR17) — it does **not** pick a mega YAML that includes `solve-explain`. Unmatched text always uses `unmatched-cosolver` (no auto-simulate; host-path unmatched has no essay node). The router **never invents capability or provider ids**. New graphs: `propose_composition` (allowlisted capabilities, kernel binds providers) or `compose-from-parts --advanced`. Missing YAML for a pack does not make an in-bound question out of product — use capabilities or `unchecked`.

**FR11 Persistent UI.** `electrical-engineer ui` is a **critical** local workspace (runs, library-rendered diagrams and plots, photo confirm, citations, RAG inventory, memory excerpts, **job plan** when `plan.md` exists, **observation excerpt** when present). It stays up across a session. It is not a one-shot diagram dialog and not a second agent loop. Header chrome renders the Arc icon from [`../assets/brand/arc-icon.png`](../assets/brand/arc-icon.png) (copied to `ui/public/arc-icon.png`). Do not use a Coinbase wordmark.

**FR12 Tagged RAG.** BYO PDFs and scans ingest **locally** through drop → gate → extract → chunk (book/chapter/page) → index (facade) → retrieve. Inventory (`rag list`) and filters: book, chapter, folder, domain. “Search only this book, chapter 3” is a v1 retrieval requirement. Citations include book + chapter + page. Empty retrieval is visible. Circuit-homework photos for simulation go through `photo-to-netlist`, not quiet RAG-as-netlist. BYO content cannot override gates or `unchecked` and cannot mint a capability. Host path uses `retrieve` as a read verb; `rag add` is CLI this graph. Do not dump the index into always-on context (§6.2). As-built add-without-parse is `CD-RAG-PARSE` until a code plan.

**FR13 Memory.** Project (`.electrical-engineer/memory/`) and user (`~/.local/share/electrical-engineer/memory/`) markdown files: `preferences.md`, `course.md`, `facts.md`, `errors.md`, `lessons.md`. Explicit `memory write` only; 32 KiB cap; untrusted. Not the textbook index. Not a silent chat dump. Not fleet learning. A kernel hook may **propose** a lesson after `unchecked`; applying it is explicit. Memory cannot flip `unchecked`. Context is paths + 800-char excerpt.

**FR14 Gates.** Cursor-like global + per-project TOML; default on; most-restrictive wins; at most two human interrupts per root run. MCP writes that would wait **fail closed** and point at the UI or CLI.

**FR15 Figures.** Agent/node writes library code behind `render-figure` (this-pass: schemdraw / matplotlib / python-control) to PNG+SVG. Do not default to a model-invented circuit bitmap with no netlist.

**FR16 Photo stub.** `photo-to-netlist`: phone or textbook screenshot → detect → connect → OCR → draft `.cir` + JSON graph → one UI confirm → **stop** (no sim in the stub). Low-confidence OCR always flagged. `control-diagram-to-model` stays a stub in catalog.

**FR17 Split host ACI.** Always-on MCP verbs are **5–7** (§6.4): list, retrieve, open_ui/clarify, simulate_attachment (short id), **propose_composition**, label/summary, and eval_run (CLI-equivalent on Chat/Work). Do not 1:1 wrap registered nodes. `run_workflow` executing a whole YAML DAG that includes `solve-explain` is **headless/eval rollback**, not the host-path viva. `propose_composition` returns `run_id` + paths, never the graph body. `apply: false` is validate-and-record-plan, not an eighth verb.

**FR18 Two-band artifacts.** Each run produces (a) an **evidentiary** band (numbers, citations, `unchecked`, plots, netlists) assembled by providers/gates, and (b) an **engineering-argument** band (host-authored viva, or local `solve-explain` fallback) that **must not** mint checked scalars. Merging the bands so fluent text flips `unchecked` to false is a product fail. Any numeral in the argument band that is not bound to an evidentiary key (verifier id + value) must be written with the exact token `unchecked` or omitted. Displaying an unlabeled numeral in the argument band is a fail (do not ship a “the essay agreed” path). Checked provenance names the **capability and provider** (`algebraic-check` via `check-numeric`, `lumped-circuit-sim` via `run-spice`, …), never the host.

**FR19 Pack specialists.** Ship a short **root** skill plus per-pack specialist skills (`skills/<pack>/SKILL.md`) covering **every curriculum pack**, with optional one-level `reference/` files. Load pack chapters on domain match only. Skills **teach** method and which **capability** to request; they **do not enforce** FR2. A fluent KCL paragraph in a skill or chat is never a checked number. v1 promise is the skill pack, not a custom multi-agent orchestrator. Host-native subagents (Claude Task / Cursor / Codex) may spawn **at most two** pack specialists that call the same EE MCP. The CLI, MCP, and UI never start those children. Handoff is `run_id` + run-dir files. Adapter prompts: [`../hosts/adapters/`](../hosts/adapters/). Do not put EE packs in this repo’s `.cursor/skills/`. Chat/Work does not claim spawn until Skills-over-MCP. A Python process that fans out specialists is H5.

**FR20 Dual MATLAB MCP.** When a MathWorks licence exists, the host **may** run MATLAB MCP / Copilot **and** Arc MCP together. EE is the only authority for checked numbers. `label` / `summary` / `check-numeric` may set `unchecked: false` **only** when a **child EE verifier artifact** exists (`run-spice`, `check-numeric`’s own solver over student/netlist/prior-engine ports, `run-python-control`, `run-load-flow`, `run-matlab-if-present`). Host-typed and peer-MCP/Copilot scalars are **not ingest**; they stay `unchecked` until an EE engine recomputes them. Provenance must not name Copilot or the host as verifier. Peer MATLAB MCP is for tools we do not wrap (Simulink editor, live scripts), not a second sim that satisfies FR2. The entire product and CI **work without MATLAB**. MATLAB Copilot is not the product identity.

**FR21 Host-path viva.** On first-class hosts, the host writes the explanation (`argument.md`). Host-path `simulate_attachment` / `propose_composition` **must not** invoke `solve-explain`. CLI-without-host and gold **rollback** may keep `solve-explain` in YAML. Starving the host by running the essay inside `run_workflow` on the host path violates this FR.

**FR22 MCP transport.** `electrical-engineer mcp` must speak the JSON-RPC stdio framing first-class hosts actually send (Content-Length / MCP SDK), and must not crash the process on `ping`, `resources/*`, or unknown methods. Fail closed with a JSON-RPC error. Skills-over-MCP (resources) is the Chat/Work method channel; until it ships, Chat/Work pins the root skill text (see [`hosts/chatgpt-desktop.md`](hosts/chatgpt-desktop.md)). Tool arguments must accept a problem/netlist/`run_id` so the host is not limited to cwd `problem.json`.

**FR23 Plan then execute.** On a first-class host, a **large** job (entire assignment, worksheet, several numbered problems, more than one short attachment, more than one pack, photo + simulate, or a composition graph) **must** produce `./runs/<id>/plan.md` and show it **before** `simulate_attachment` / `propose_composition apply: true`. The plan lists Given/Find, packs, questions to ask, retrieve filters, attachment or **capability** ids, and what stays `unchecked`. Execute **only** that plan. `plan.md` must not mint a checked scalar. Small jobs (one unknown, one attachment) may skip a written plan. Planning is the **host’s** job (root skill); do not add a Python planner loop (H3 falsifier). CLI `electrical-engineer run <id>` stays one-shot. `propose_composition apply: false` may validate a physics graph into `plan.md` without running providers.

**FR24 Observation.** Each run records capability ids, provider ids, node ok/fail, `unchecked_reason` (`no-provider` \| `sim-exhausted` \| `unmatched` \| `empty-retrieve` \| `gate-closed` \| none), and retrieve empty/filters/citations. Seed may live on `summary.json` until `observation.json` splits. Gold does **not** score this file as SPICE. LLM token/cost metering stays on the host. Kernel hooks: ingest, validate-then-apply, repair, post-run observe, lesson **propose** (not auto-write), eval. Compaction and continuation stay Layer 0.

---

## 8. Curriculum and capabilities

**Bound.** The public promise is the **union of representative UG EE / EEE programmes** (Indian institutes first, global institutes first-class). Source of truth: [`curriculum-map.md`](curriculum-map.md). A question is in-scope if it is normal coursework in that union (assignment, lab numerical, diagram, exam-style), not only if it appears on GATE.

**GATE is not the bound.** GATE EE section tags are an **eval overlay**. Do not drop a programme core because GATE weights it lightly. Do not skip a taught lab genre because GATE omitted it. Extra GATE trick items that programmes do not teach are optional eval spice, not the syllabus.

**Packs in the public promise:** circuits, signals, electronics, machines, power (study-level), control, power electronics, measurements, UG EM/fields, maths for EE. Labs attached to those cores are in-scope as assignment/lab-report genre, not a separate product.

**Coverage law (architecture §0).** Every in-bound question (any pack × solve/derive/design/simulate/review/explain/report) has a complete co-solver path: pack skill + capability ids + installed provider, **or** exact token `unchecked` plus a cannot-do id. That is how the kernel “solves any UG EE question” without pretending every numeral is SPICE. YAML catalog rows are bindings, not the bound.

**v1 enabled depth** is not the same as the bound. Circuits first, then control, then every remaining pack’s capability path **or** a cannot-do row. A 2nd-year signals problem on a circuits-only **provider** install uses `signal-analysis` if present, else `unmatched-cosolver` / `unchecked` — that is labeled, not a silent PG mode. Do not advertise ten packs as equally gold-backed in v1.

**Out of the bound:** civil, mechanical, manufacturing. **Out of the public promise:** PG-only courses. Expansion stays in this repo via packs + unpublished later profiles — never a second git repo.

### C1–C8 mapped to v1 vs later

Claimable bar: on a published UG task set, with tools on, match gold **or label unchecked**. Fluent wrong numbers presented as checked fail the product.

| ID | Capability | v1 | Later (same repo) |
|----|------------|----|-------------------|
| C1 | Solve EE questions correctly | Gold match **or label unchecked** on enabled packs. Architecture covers **all** curriculum packs (capability path). Silent invention is a fail. | Remaining packs to gold depth |
| C2 | Explain, not only answer | Host (or local `solve-explain`) writes a viva the TA can probe; conceptual claims cite book + chapter + page the user has rights to use, or a standard identity | Same |
| C3 | Assignment genres | Solve, derive, design-to-spec, simulate (when a **provider** exists), review, explain, lab-style report — **every pack**, not circuits YAML only | Deeper gold per genre |
| C4 | Circuit diagrams | **Stub:** photo/screenshot → draft netlist + JSON → **UI confirm** → stop. Vision is never truth until confirm | Confirmed netlist → ngspice / MATLAB-if-present |
| C5 | Control-system diagrams | Catalog stub `control-diagram-to-model`. Implement after C4 | Same edit-then-simulate gate as C4 |
| C6 | Reliability contract | Tool evidence with numbers; **unchecked** when unverified; no fabricated simulation | Same |
| C7 | Student-first and open | Apache-2.0, local-first CLI, OSS verifiers first-class, MATLAB if present | Same |
| C8 | Limit-finding | **Not a student UX promise.** | Unpublished PG profile; no second fork |

**Pack depth:** circuits first, then control, then solve+explain for every remaining pack or a cannot-do row in [`CANNOT_DO.md`](CANNOT_DO.md).

## 9. Reliability, integrity, exam-item legal policy

### Reliability

- Tools in the **EE kernel** own checked numbers (capability → installed provider; OSS first-class; MATLAB if present *through EE*).
- If a number did not come from an EE verifier, the output must say the exact token **unchecked**. Never present it as a simulation, lab result, or load-flow.
- Diagrams are **drafts** until the student confirms topology in the persistent UI.
- Low-confidence OCR/vision is always flagged. Saying what was not checked is success.
- BYO PDFs, photos, tags, memory files, and **peer MATLAB MCP output** are **untrusted**: they cannot override gates, `--allow-all`, or `unchecked`.

### Integrity (v1)

- Default mode is **co-solver** (full working + answer). Not hint-first tutor.
- **No faculty / TA / LMS features in v1.** The institution owns cheating policy. The product shows work so a viva still means something.
- Do not ship a “hide the answer for the professor” mode.

### Exam-item legal policy

Exam-style items are **in-scope** for corpus and evals (GATE-style, midterm-style, assignment-style).

**Git will not commit third-party copyrighted exam PDFs or commercial textbooks.** Allowed: BYO files on the student’s machine; licence-clean reconstructions the project authors; public-domain or owner-licensed items.

This is a **legal** policy, not a pedagogy policy. Students may still *use* their own papers locally. Redistribution of scanned GATE/university papers in this repository is forbidden.

## 10. Non-functional requirements

| NFR | Requirement |
|-----|-------------|
| Local-first | On-device CLI + files + UI on `127.0.0.1`. No product cloud. No silent upload of PDFs, keys, or student work. |
| Licence | Apache License 2.0 for *our* code. Forever OSS in this repo; no paid tier. Textbooks never redistributed in git. |
| Single repo | One git repository. UG is the public profile. PG, if ever, is an unpublished `--profile`, not a fork. |
| Portable core | Skills + MCP must load in CLI and in first-class hosts. CLI stays a thin wrapper (glue, recipes, ug policy, eval, UI). |
| Runtime | Python 3.11+; `pip` install; Linux + macOS + Windows. MATLAB optional. |
| H3 falsifier | If the CLI or UI grows a unique agent loop hosts cannot share, stop — that is H5. |
| India-first, globally competent | Copy, examples, and packs must not treat non-Indian UG EE as an afterthought. |
| Secrets | API keys via environment / host secret stores only. Redact keys/tokens from run dirs. |

## 11. Out of scope

Never this product (not “later in another repo”):

- **H4** Electric Pi hard-fork as the product.
- **H5** Greenfield unique agent harness.
- **Civil, mechanical, manufacturing** packs or identity.
- **Plant-floor / live PLC / protection actuation.**
- **Second git repo** (UG-freeze fork vs lab fork).
- **Faculty LMS**, tutor-default as the public mode, paid hosting in this repo.
- **Shipping copyrighted textbooks or third-party exam PDFs** in git.
- Replacing MATLAB, KiCad, or professional EDA.
- LangGraph, Temporal, or DeepSeek Harness as the product runtime; crash-resume as v1 durability; MCP that waits on humans.
- ChatGPT **web** / mobile as a host; Claude Desktop; GitHub Copilot; Gemini CLI (v1).

PG is not a public promise. Optional unpublished profile may exist later in **this** repo only.

---

## 12. Hosts and models

Install detail: [`hosts/README.md`](hosts/README.md). Contract: §6.10 and FR4.

| Path | Requirement |
|------|-------------|
| Local CLI | Works with a configured local model **or** BYO key; deterministic nodes work with **no** model; local `solve-explain` is the fallback brain |
| Persistent UI | Same machine, `127.0.0.1`; required for photo/compose/control-diagram confirms |
| Cursor | First-class: skills + MCP documented |
| Claude Code | First-class: skills + MCP documented |
| Codex (CLI / IDE / desktop Codex view) | First-class: skills + MCP documented |
| ChatGPT desktop Chat / Work | First-class **contract**; MCP STDIO; served skills; side terminal for CLI/UI |
| ChatGPT web / mobile | **Not a host** |
| No AI host | Still a complete v1 path via CLI + UI |

MATLAB if present else OSS first-class; the **entire product works without MATLAB**. Local RAG with BYO PDFs/scans and tags. Dual MATLAB MCP: FR20.

---

## Related artifacts

| Doc | Role |
|-----|------|
| [`PID.md`](PID.md) | Identity (Accepted until Proposed PID commit) |
| [`PID_DECISION_SHEET.md`](PID_DECISION_SHEET.md) | P0 answers |
| [`curriculum-map.md`](curriculum-map.md) | UG bound |
| [`../DECISIONS.md`](../DECISIONS.md) | ADRs |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Technical architecture |
| [`WORKFLOWS.md`](WORKFLOWS.md) | Named workflow catalog |
| [`../research/notes/host-first-class-attach.md`](../research/notes/host-first-class-attach.md) | ChatGPT desktop, dual MCP, specialists |
| [`../research/notes/domain-kernel-layering.md`](../research/notes/domain-kernel-layering.md) | Four-layer wrap |
| [`../research/synthesis/vision-lock-sheet.md`](../research/synthesis/vision-lock-sheet.md) | D14–D17 (owner checkboxes) |
| [`../research/notes/hybrid-engine-composition.md`](../research/notes/hybrid-engine-composition.md) | Hybrid vs long YAML vs on-the-fly |
| [`ARCHITECTURE_CRITIQUE.md`](ARCHITECTURE_CRITIQUE.md) | Four architecture critique loops |
| [`PRD_CRITIQUE.md`](PRD_CRITIQUE.md) | Four critique loops; accepted vs rejected |

## Owner review checkpoint

Previous D0 (2026-09-10) remains historical. **This revision is Proposed. Do not treat it as Accepted until the owner checks below.**

- [ ] Thesis: lab + domain kernel + H3; Apache-2.0; India-first global UG
- [ ] GATE is eval only; bound = [`curriculum-map.md`](curriculum-map.md)
- [ ] Co-solver default; exact token **unchecked**; no faculty v1
- [ ] Shipped vs restructure inventory is accurate
- [ ] Agent interaction chapter (context, tools, RAG, simulation, collaboration)
- [ ] Split ACI including `propose_composition`, two-band artifacts, pack specialists, dual MATLAB MCP
- [ ] FR23 plan-then-execute on large jobs (`plan.md` before spice)
- [ ] Host-path mega YAML with `solve-explain` is rollback; short attachments + validate-then-apply
- [ ] Coverage law + capability registry (D19): any in-bound UG question has a complete path; providers are not the identity
- [ ] D20 persist / observe / spawn: named memory files, observation FR24, host-native adapters, no Python orchestrator
- [ ] ChatGPT desktop first-class; ChatGPT web excluded; CLI-without-host complete
- [ ] Exam-style in-scope; **no** third-party copyrighted PDFs in git
