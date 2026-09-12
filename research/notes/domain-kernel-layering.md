# Domain-kernel layering (Electrical Engineer)

## Purpose

Answer, at the layer level: what Electrical Engineer wraps, who owns the core agentic loop, where physics and gates live, how CLI / MCP / later Code Mode attach, and what is already right versus what to optimize. Complements topology C in `domain-system-architecture-patterns.md`. Does not rewrite `docs/ARCHITECTURE.md`.

## Findings

Claim | Evidence | Confidence
--- | --- | ---
Internal class is a **domain kernel**: rented host loop + owned engines, skills, gates, eval | `notes/agentic-kernel-2026.md`; H3; topology C | high
Four layers: (0) rented harness, (1) attach, (2) domain kernel, (3) two-band artifacts / UI | this note’s stack | high
Layer 0 is already correct (H3). Do not grow a unique host-incompatible loop | `docs/PID.md`; `docs/ARCHITECTURE.md` H3 falsifier | high
Layer 1 is half-right: dual CLI + MCP exists; MCP `run_workflow` is a mega-apply that starves the host | `mcp/server.py`; Firecrawl; kernel memo §8 | high
Layer 2 physics/gates/eval/run-dir are the durable core and should stay | YAML runner; `unchecked`; unmatched; photo fail-closed | high
Layer 2 method (skills) and host-path explanation are starved | four-line pack `SKILL.md`; `solve-explain` as a registered node | high
Always-on ACI target is 5–7 verbs, not one mega `run_workflow` and not one MCP tool per node | kernel memo §3; Code Mode | med
Two-band artifacts (evidentiary vs engineering argument) is the leave-behind shape | kernel memo §8; `unchecked` token | high
Headless YAML runner is eval rollback, not a second chat product | kernel memo §7; `eval/` gold | high

### Stack (who handles what)

```text
Layer 0 — Rented harness (not ours)
  Cursor / Claude Code / Codex / configured local model in a host
  Owns: context window, permissions, subagents, compaction, the inner loop
  Must not: Kirchhoff, spice truth, `unchecked`, gold replay

Layer 1 — Attach (thin adapters)
  1a CLI inner loop     electrical-engineer run | eval | ui | rag | mcp
  1b MCP outer loop     stdio tools for hosts without wanting a shell
  1c Later: Code Mode / PTC on READS only (retrieve, list, maybe clarify)
  Must not: 1:1 wrap every node; PTC on spice/confirm/compose/label

Layer 2 — Domain kernel (what we own)
  2a Method     skills/  — how an EE student thinks (today: stubs)
  2b Engines    nodes    — spice, control, load-flow, sympy, matlab-if-present
  2c Recipes    YAML     — genre contracts for attaching physics (not the chat brain)
  2d Gates      code     — unmatched, photo confirm, compose allowlist, `unchecked`
  2e Eval       gold     — replay runner; scores evidentiary artifacts
  2f Stores     local    — ./runs/<id>/, memory markdown, RAG index
  2g ACI        verbs    — propose / validate / apply; today execute() is all-or-nothing apply

Layer 3 — Surfaces
  3a Localhost UI   confirm, compose, control-diagram, plots (human gates)
  3b Artifacts      two bands: evidentiary numbers vs host-authored argument
```

This is OpenMontage’s *sit on the harness* plus Karajan’s *gates in code* plus ChemCrow’s *tools as truth*, named as a kernel so we do not rebuild Claude Code and do not put physics only in markdown.

---

### Layer 0 — Rented harness

Osmani 2026: agent = model + harness; failures are configuration; a decent model with a great host harness beats a great model with a bad one. Electrical Engineer already decided this (H3, not H5). The host owns the core agentic loop. We wrap it so it can do undergraduate EE.

What Layer 0 should do on a coursework problem:

- Read the assignment as a whole (text, figure, prior run dir).
- Choose method (KCL vs nodal vs phasor).
- Ask the student when data is missing.
- Call kernel verbs for retrieve / simulate / label / confirm.
- Write the viva (engineering-argument band).
- Stop when gates refuse.

What Layer 0 must not do:

- Present a fluent `Vout` as checked.
- Invent a spice DAG because a prompt “looks like a netlist.”
- Confirm a photo topology without the UI.
- Bypass `unchecked`.

H3 falsifier unchanged: if the CLI grows a custom multi-turn loop hosts cannot share, stop. An executive kernel (KAIJU `kernel.submit()` as *the* runtime) would take the loop back. That is H5 with extra papers. Steal only the no-bypass write path.

Student-without-host (PID Q-S2) is a Layer 0 *absence*, not a second product. CLI + local `solve-explain` node + spice/control with no model remains a complete path. That node is a fallback, not the host-path brain.

---

### Layer 1 — Attach

Firecrawl 2026: CLI is the inner loop; MCP is the outer loop. Cloudflare Code Mode / Anthropic PTC: model writes code against a small typed surface; intermediates stay out of context.

**Today**

| Adapter | What it does | Diagnosis |
|---------|--------------|-----------|
| CLI `run` | Router → YAML DAG → `execute(wid)` | Correct for explicit ids and eval. Over-owns explanation when the host is present |
| CLI `eval` / `ui` / `rag` | Gold, human gates, inventory | Correct; keep |
| MCP `list_workflows` | Read catalog | Correct; PTC-safe later |
| MCP `run_workflow` | `execute(wid)` or fail-closed with `ui_url` | Correct fail-closed on photo/compose/control-diagram. Incorrect as the *only* host write: it runs `solve-explain` inside the DAG |

MCP never waits (ARCHITECTURE). That constraint stays. Elicitation, if a later MCP spec adds it, is transport for “ask the student,” not a second ledger.

**Attach order (research freeze, not a code change)**

1. CLI first — students, eval, hosts that already have a shell. The model already types commands.
2. MCP for Cursor/Claude tool lists, no-shell, audit-shaped calls.
3. Code Mode / PTC **later**, and only if **read** tools proliferate (RAG fan-out, catalog search). Do not start a Code Mode sandbox in this research pass.

**Proposed always-on ACI (5–7 verbs)**

Direction, not shipped names:

| Verb | Layer | Direct | PTC later | Notes |
|------|-------|--------|-----------|-------|
| `list_workflows` | read | yes | yes | Already exists |
| `retrieve` | read | yes | yes | RAG; citations stay evidentiary |
| `clarify` / ask-human | read+write of questions | yes | read list yes; answer no | MCP still never blocks; returns `ui_url` |
| `simulate` named recipe | write | yes | **no** | Only named YAML ids; never invented DAG |
| `label_unchecked` / summary | write | yes | **no** | Can mint checked vs `unchecked` |
| `eval_run` | write | yes | **no** | Gold replay |
| `open_ui` | read | yes | yes | Point at confirm/compose |

`run_workflow` as “do the entire assignment including the essay” is the mega-apply to retire on the **host path**. It can remain as headless rollback (`electrical-engineer run <id>` for eval and for students who want one command).

Never-a-host-tool: invent spice DAG, confirm topology without UI, freeze a fluent number as SPICE, session-defined `lookup_vout_guess`.

Do not wrap `run-spice`, `run-matlab-if-present`, `run-load-flow`, `retrieve-passage`, `solve-explain` as six extra MCP tools. That is the 45-endpoint anti-pattern. Named recipes already compose those nodes.

---

### Layer 2 — Domain kernel internals

This is the durable product. Polar-mcp / de Prey: Python core, thin adapters. Thoughtworks: a skill is not an ACL.

#### 2a Method (skills)

Pack files today are pedagogy stubs (example: `skills/circuits/SKILL.md` is four lines). Topology C asked the host to plan and explain; stubs cannot teach a host the whole method.

Skills should tell the host: name the unknown, write KCL/KVL, when to call `simulate` vs when `unchecked`, when to stop and ask, how to write the argument band without minting scalars. Skills do not enforce those rules. Nodes and gates do.

OpenMontage can put more intelligence in markdown because a slightly wrong cut is survivable. EE cannot. Keep skills thick on *method*, thin on *numbers*.

#### 2b Engines (nodes)

Registered activities: spice, control, load-flow, matlab-if-present, retrieve, photo stages, `label-unchecked`, `write-run-summary`, `solve-explain`. One activity each. Numbers come from here or the exact token `unchecked`.

Keep capability-first provider selection (MATLAB if present, else ngspice / python-control). Do not invent a third rule.

`solve-explain` is the starve point on the host path: it is an LLM node inside the DAG (`nodes/photo.py`), so MCP/`run` owns the viva. On the local-only path it stays legitimate. Split: host writes the argument band; the node remains a fallback when no host is configured.

#### 2c Recipes (YAML)

D13 freeze: in-process DAG + tiny FSM; YAML recipes; Python node functions; not LangGraph/Temporal. D16: the runner is the **physics backbone**, not the professional-workflow brain.

Named recipes are genre contracts: “this is how we attach spice to a circuits problem.” The router never invents a DAG. Unmatched → `unmatched-cosolver` only. `run-recipe` child depth ≤ 3. `compose-from-parts` is the only new-graph path (typed ports, 16 nodes / 24 edges).

GraSP-shaped lesson: do not trust an LLM-authored DAG; compile/validate, then apply. We already validate by refusing invention. A later propose → validate → apply ACI would let the host *narrate* which named recipe to run, not author new node graphs in the session.

#### 2d Gates (no-bypass)

Karajan / KAIJU steal: if the host can call a function behind the gate, the invariant is opt-in and dead.

Already in code:

- Unmatched never auto-simulates.
- Photo / compose / control-diagram fail closed on MCP with `ui_url`.
- `label-unchecked` walks child outputs; fluent text does not count as checked.
- Compose allowlist and step budget.

IGX mapping for EE (vocabulary only): impact of a write ≤ min(intent, clearance, scope). Intent = named recipe or compose. Clearance = gates.toml / UI confirm. Scope = run-dir isolation. A beautiful wrong `Vout` still fails if no verifier artifact exists.

Gates only in `SKILL.md` is the OpenMontage purity we already rejected.

#### 2e Eval

Gold packs score evidentiary artifacts (`Vout = 5.0` on divider-dc-01). That is the outer loop Osmani named: independent check, not the model’s “done.”

Headless replay of the YAML chain is rollback (kernel memo §7), analogous to Stamped keeping a deterministic eval path after the host owns the briefing. Do not grow eval into a second chat product. Do not score the essay as if it were SPICE.

Held-out hygiene (Self-Harness idea in the uploaded memo): a packet the host did not see. Direction for later eval design, not this pass.

#### 2f Stores

`./runs/<id>/` is audit, not crash-resume (Q29). Memory markdown and local RAG stay local. Hosts do not own the textbook corpus.

#### 2g ACI vs `execute()`

Today `execute(wid)` is the apply. Propose/validate are implicit (explicit id, or classifier, or unmatched). On the host path, classification is a job the 2026 model can do in the harness (spend). The pre-runner classifier is a micro-call that starves context the same way Stamped’s nine extractors did.

Keep `execute()` as the engine entry for named recipes and eval. Add (later, after lock) a validate step the host can call: “may I run `simulate-circuit` on this netlist?” returning gates, not running spice yet.

---

### Layer 3 — Surfaces and two-band artifacts

**UI.** Persistent localhost workspace: runs, plots, citations, photo confirm, compose, control-diagram. Not a ChatGPT clone. Not a video timeline. Not a KiCad clone. MCP never waits; the UI is where humans wait.

**Two bands**

| Band | Who writes | What it may contain | What it may not |
|------------------|-----------|---------------------|-----------------|
| Evidentiary | Engines + gates | Numbers, `.cir`, plots, citations, `unchecked`, gold diffs | Host judgment presented as SPICE |
| Engineering argument | Host (or local `solve-explain` fallback) | Method, viva, “why this topology,” labeled inference | Minting a checked scalar |

`write-run-summary` today folds value + citations + unchecked into one `summary.json`. That is a seed of the evidentiary band. It is not yet an explicit split: a future host-authored markdown next to `summary.json` should not be allowed to flip `unchecked` to false.

Do not merge the bands. A PE (here: a TA or the student in viva) must see which sentences are measured and which are judgment.

---

### What is already right

- H3 / topology C: rent the loop; do not build H5.
- YAML runner as deterministic physics DAG + eval replay (D13).
- Router never invents a spice DAG; unmatched never auto-simulates.
- Photo confirm ≠ SPICE; MCP fail-closed with `ui_url`.
- Exact token `unchecked`; `label-unchecked` in code.
- Dual CLI + MCP adapters over one Python core.
- Localhost UI for human gates; student need not use Cursor.
- Gold eval on numbers (`eval/gold/circuits/divider-dc-01`).
- Run dir as audit; no crash-resume.
- Apache-2.0; UG bound; no plant-floor; MATLAB optional.

These are the kernel. Optimize around them; do not replace them with markdown control planes or an owned harness.

### What to optimize (after owner lock, not this note’s code)

1. **Stop starving the host.** Host path: skills teach method; host writes the argument band; MCP/CLI call retrieve/simulate/label/eval; `solve-explain` is fallback for no-host.
2. **Split the mega-apply.** Keep `run <id>` for eval and one-command students. Host ACI: 5–7 verbs, propose/validate/apply, never one tool per node.
3. **Thicken skills** without moving gates into markdown.
4. **Name two artifact bands** so explanation cannot launder numbers.
5. **Give classification back to the host** when a host is present; keep the small classifier for CLI-omitted-id without a host.
6. **Defer Code Mode / PTC** until read tools actually proliferate. Do not build a sandbox to look 2026.
7. **Do not** drop YAML, `unchecked`, unmatched law, H3, or student-without-host.

### Spend vs clamp (EE table)

| Spend (host) | Why 2026 is enough | Kernel role |
|--------------|-------------------|-------------|
| Read the assignment + figure + prior run | Long context + vision in the rented harness | Tools fetch; host reasons |
| Choose KCL vs nodal vs phasor; viva | This is the coursework job | Skills; argument band |
| Interview the student for missing values | Host conversation | `clarify`; UI if MCP |
| Fan-out RAG reads | PTC later | `retrieve` |
| Compare two methods after a check fails | Evaluator-optimizer, host-driven | Simulate again; do not fake pass |

| Clamp (engines/gates) | Why | Hook |
|-----------------------|-----|------|
| Checked `Vout` / bus voltage / ω_n | Models still invent numbers | spice/control/load-flow or `unchecked` |
| Invented spice DAG | Unmatched law | Named YAML or compose only |
| Photo topology | Vision ≠ netlist truth | UI confirm |
| MATLAB scalars | Licence + numeric truth | `run-matlab-if-present` |
| Fluent essay as checked | Laundering | Two-band; `label-unchecked` |
| Session-invented verbs | JIT-Agent is for coding harnesses | Catalog allow-list |

Stamped translation (do not copy terms into PID): SKU → invented node voltage; freeze/PO → presenting unchecked as SPICE; PE brief → viva/explanation; assemble → evidentiary `summary.json`.

### Anti-patterns (refuse)

- Electrical-Engineer-owned Claude Code (H5 / executive kernel).
- Topology A: intelligence only in markdown.
- Topology B as public identity: YAML FSM as the brain that fights the host.
- 45 MCP tools wrapping nodes 1:1.
- PTC on spice writes.
- Gates only in SKILL.md.
- Merging argument band into evidentiary `summary.json`.
- Scoring gold on the essay.
- Plant-floor / second git repo / “studio” as the public noun.

---

## Open questions

- Owner accept/reject of D17 (this layering) on the vision lock sheet.
- Exact verb names and whether `run_workflow` remains as an alias for headless apply.
- When (if ever) to add Code Mode `search()` + `execute()` over retrieve/list.
- Which files in `./runs/<id>/` become the argument band versus staying in chat.

## Sources

- [`research/notes/agentic-kernel-2026.md`](agentic-kernel-2026.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/domain-system-architecture-patterns.md`](domain-system-architecture-patterns.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/PID.md`](../../docs/PID.md) — retrieved 2026-09-12 — reliability: primary
- [`src/electrical_engineer/mcp/server.py`](../../src/electrical_engineer/mcp/server.py) — retrieved 2026-09-12 — reliability: primary
- [`src/electrical_engineer/nodes/photo.py`](../../src/electrical_engineer/nodes/photo.py) — retrieved 2026-09-12 — reliability: primary
- [`src/electrical_engineer/nodes/registry.py`](../../src/electrical_engineer/nodes/registry.py) — retrieved 2026-09-12 — reliability: primary
- [`skills/circuits/SKILL.md`](../../skills/circuits/SKILL.md) — retrieved 2026-09-12 — reliability: primary
- [Firecrawl — MCP vs CLI in 2026](https://www.firecrawl.dev/blog/mcp-vs-cli) — retrieved 2026-09-12 — reliability: secondary
- [Cloudflare — Code Mode](https://blog.cloudflare.com/code-mode-mcp/) — retrieved 2026-09-12 — reliability: vendor
- [Addy Osmani — Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) — retrieved 2026-09-12 — reliability: secondary
- [KAIJU](https://arxiv.org/abs/2604.02375) — retrieved 2026-09-12 — reliability: paper

## Confidence

Overall confidence for this note: high

Layer 0/2d/2e map onto accepted architecture. Layer 1 verb split and two-band files are a design recommendation; confidence would drop if owner lock keeps mega `run_workflow` as the only host path, or demands PTC on simulators.
