# Architecture patterns for a harness-native EE domain system

## Purpose

Score three topologies for Electrical Engineer against locked EE constraints, using OpenMontage, Anthropic’s workflow/agent split, the Agent Patterns Catalog, ChemCrow, and Karajan as sources. Answer: where should planning live, and where must physics live?

## Findings

Claim | Evidence (URL or ledger ID) | Confidence
--- | --- | ---
Anthropic splits **workflows** (predefined code paths) from **agents** (the LLM directs its own tool use). EE needs both: named recipes for simulation attachment, an agent for explanation and method choice | https://www.anthropic.com/research/building-effective-agents | high
OpenMontage puts the coding assistant in the control plane: YAML manifests, stage-director skills, Python tools, JSON checkpoints, optional human approval. Python is tools plus persistence, not a second LLM loop | https://github.com/calesthio/OpenMontage/blob/main/docs/ARCHITECTURE.md | high
ChemCrow’s result is the same split in chemistry: GPT-4 plans; 18 expert tools supply answers the model cannot compute (math, IUPAC, lab) | https://www.nature.com/articles/s42256-024-00832-8 | high
This repo’s core-engineering note already recorded that pattern for EE: LLM plans and explains; SPICE/MATLAB/control are numeric truth | `research/notes/ai-core-engineering-landscape.md` | high
Karajan is the closest “code owns QC” sibling: markdown roles for agent stages, **deterministic** stages for intent, acceptance tests, guards, TDD — no LLM on those gates | https://github.com/manufosela/karajan-code | med
Locked EE constraints forbid topology A as a clone: unmatched never auto-simulates; photo confirm is not SPICE; runner is deterministic; H3 falsifier is a unique host-incompatible loop | `docs/ARCHITECTURE.md` §§2, 4–7; `docs/PID.md` H3 | high
Production catalog patterns that already match this repo: tool use, routing, step budget, decision log, sandbox isolation, HITL at a risk boundary. Catalog ids remain MCP-PENDING (agent-patterns MCP unreachable here) | https://www.agentpatternscatalog.org/agentic-ai-design-patterns/ ; `docs/ARCHITECTURE.md` | high
Topology **C (hybrid)** is the best fit: host agent orchestrates the *work*; Python owns physics, artifacts, eval; named pipelines are genre contracts, not a second harness | this note’s scoring table | med

### Anthropic’s distinction, mapped onto EE

Anthropic: workflows are LLMs and tools on **predefined code paths**; agents are systems where the **LLM dynamically directs** process and tools. They advise starting simple, measuring, and adding a loop only when a single call fails.

EE assignment work is mixed:

- **Workflow-shaped:** attach SPICE, run python-control, label `unchecked`, confirm a photo topology. These paths must not be invented because a prompt “looks like a netlist.”
- **Agent-shaped:** choose KCL vs nodal, write a viva explanation, decide which textbook chapter to retrieve, repair a wrong derivation after a check fails.

OpenMontage is almost all agent-shaped (creative cuts). ChemCrow is agent-shaped planning with workflow-shaped tools. Karajan splits the pipeline into LLM roles and non-LLM guards. Electrical Engineer today is almost all workflow-shaped (YAML DAG), with `solve-explain` as one registered node.

### Topology A — agent as control plane, intelligence in markdown

OpenMontage’s own architecture: there is **no runtime Python orchestrator**; Claude Code / Cursor / Copilot reads `pipeline_defs/*.yaml`, a per-stage director skill, calls a `BaseTool` registry, writes a checkpoint, self-reviews, asks a human if the manifest says so.

Steal: three-layer knowledge (what exists / how this project uses it / how the vendor API works); canonical artifacts with schemas; provider selectors; HITL at irreversible creative beats; the **host is the loop**.

Do not steal: “all intelligence lives in skill instructions.” ChemCrow and this repo’s landscape note both say models fail basic exact operations. A fluent wrong `Vout` labelled as SPICE is a product fail. OpenMontage can absorb a slightly wrong cut; EE cannot.

Also weak for PID Q-S2: a student need not use Cursor. Topology A without a CLI path for deterministic nodes drops that lock.

### Topology B — CLI YAML FSM as the brain (today)

This is Anthropic’s **workflow**: hybrid router picks a named recipe; in-process DAG; runner law (no model calls except registered nodes plus one pre-runner classifier); unmatched → `unmatched-cosolver` only.

Keep: eval/gold replay; `unchecked` contract; gates; run-dir isolation; student-without-host spice/control/load-flow; H3 falsifier.

Cost: the YAML runner **substitutes** for the host agent’s planning. Pack skills are pedagogy stubs. Public identity reads as “CLI plus MCP,” which undersells the class OpenMontage occupies. As frontier harnesses improve, a competing mini-orchestrator is the thing PID told us not to become (H5), just from the other direction.

### Topology C — hybrid (recommended)

Host coding agent (Claude Code / Codex / Cursor) plans, explains, reviews, and drives the professional workflow. Python owns verifiers, simulators, RAG, gates, eval, and the localhost workspace. Named YAML recipes remain **genre contracts** for attaching physics. The router still never invents a spice DAG.

```text
Frontier harness (Claude Code / Codex / Cursor)
        |
        v
Electrical Engineer (domain system)
   host agent: method, explanation, review
   code: spice / control / load-flow / sympy / RAG / unchecked / eval
   files: named pipelines, skills, run dir, localhost UI
        |
        v
Checked coursework artifacts
```

This is OpenMontage’s **layering** (sit on the harness) plus Karajan’s **deterministic guards** plus ChemCrow’s **tools as truth**. It does not reopen H3: the CLI must not grow a unique multi-turn loop hosts cannot share. `solve-explain` on the local-model path stays a registered node for students without a host; it is not a second hidden agent in MCP.

Describe this as a **harness-native domain system**, not a “studio.” OpenMontage’s marketing word is theirs.

### Pattern map (what to keep vs adopt)

| Pattern | Source | EE use |
|---------|--------|--------|
| Augmented LLM | Anthropic; catalog | Host agent + retrieval + tools + memory. Do not reimplement the host loop. |
| Tool use (typed) | catalog; ChemCrow | Nodes and MCP tools with schemas. Numbers come from tools. |
| Routing | Anthropic; `docs/ARCHITECTURE.md` §4 | Named recipe or unmatched. Never invent a DAG. |
| Prompt chaining | Anthropic | retrieve → solve-explain → check-numeric / spice → summary |
| Evaluator-optimizer | Anthropic; `repair_max: 2` | Sim-repair then `label-unchecked` or `ask-human`, never a fake pass |
| Orchestrator-workers | Anthropic; OpenMontage parallel shots | Optional later for pack-parallel explain; not a v1 identity |
| HITL at risk boundary | catalog HITL; OpenMontage approval; EE gates | Photo, MATLAB, compose, outside writes. MCP never waits. |
| Step budget | catalog; EE 16/24, 2 interrupts, 10 min ceiling | Keep. |
| Decision log | catalog; EE `./runs/<id>/` | Keep as **audit**, not crash-resume (Q29). |
| Sandbox isolation | catalog; run-dir writes | Keep. |
| Canonical artifacts + schemas | OpenMontage | Adopt for solution / netlist / plot / citations; do not copy video checkpoint resume. |
| Provider selector | OpenMontage TTS/video selectors | MATLAB-if-present vs ngspice / python-control. Capability-first, not a third rule. |
| Three-layer knowledge | OpenMontage | Layer 1 (tools) must be **thicker** than OpenMontage’s: physics cannot live only in markdown. Layers 2–3 (conventions, vendor skills) can grow. |
| Agent-computer interface | Anthropic appendix 2 | Tool docs as carefully as prompts. Current pack `SKILL.md` files are too thin for a host agent to run the system. |

**MCP-PENDING:** agent-patterns MCP was unreachable in this environment; catalog citations are page-level, not pattern ids.

### Scoring against EE constraints

| Constraint | A markdown control plane | B YAML as brain | C hybrid |
|------------|--------------------------|-----------------|----------|
| Tools own numbers or exact token `unchecked` | Fail unless Python still owns sim | Pass | Pass |
| Unmatched never auto-simulates | Fail if agent may attach spice | Pass | Pass (router law stays) |
| Photo confirm ≠ SPICE | Possible via skill; easy to skip | Pass | Pass (gate stays) |
| Student without Cursor | Weak | Pass | Pass (deterministic nodes + optional local `solve-explain` node) |
| H3 falsifier (no unique host-incompatible loop) | Pass if host *is* the loop | Pass today; drift risk if FSM grows | Pass if CLI stays glue |
| Ride frontier planning | Pass | Fight | Pass |
| Gold eval replay | Weak (agent variance) | Pass | Pass (score the verifier artifacts, not the essay) |

**Pick: C.** Overturn only if a later note shows that host agents cannot be taught named-recipe discipline, or that a student-without-host path is being dropped by owner lock.

## Open questions

- How much of today’s YAML DAG should the **host** drive versus `electrical-engineer run <id>` still executing the whole recipe? Answered in `notes/domain-kernel-layering.md` (host narrates and writes the viva; named `run` stays eval/headless rollback). Owner lock is D17.
- Which artifacts deserve OpenMontage-style JSON schemas in v1 (netlist, `summary.json`, citations) versus later?
- Whether a tool registry / selector object is needed, or the existing separate `run-spice` / `run-matlab-if-present` / `run-load-flow` nodes are enough.

## Sources

- [Building effective agents (Anthropic)](https://www.anthropic.com/research/building-effective-agents) — retrieved 2026-09-12 — reliability: primary
- [OpenMontage Architecture](https://github.com/calesthio/OpenMontage/blob/main/docs/ARCHITECTURE.md) — retrieved 2026-09-12 — reliability: primary
- [ChemCrow, Nature Machine Intelligence](https://www.nature.com/articles/s42256-024-00832-8) — retrieved 2026-09-12 — reliability: paper
- [Agentic AI design patterns (Agent Patterns Catalog)](https://www.agentpatternscatalog.org/agentic-ai-design-patterns/) — retrieved 2026-09-12 — reliability: secondary
- [karajan-code](https://github.com/manufosela/karajan-code) — retrieved 2026-09-12 — reliability: primary
- [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/PID.md`](../../docs/PID.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/ai-core-engineering-landscape.md`](ai-core-engineering-landscape.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/architecture-qa-gate.md`](architecture-qa-gate.md) — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this note: high

The Anthropic split, OpenMontage control plane, ChemCrow tool-truth, and this repo’s locked runner law are primary documents. Confidence would drop if OpenMontage later added a Python orchestrator, or if the owner dropped the student-without-host lock.
