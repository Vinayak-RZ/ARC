# Hybrid engine composition vs long YAML vs on-the-fly

## Purpose

Decide how a first-class host should attach physics: long named YAML as the chat brain, unconstrained on-the-fly tool graphs, or a hybrid of typed engines plus short attachments plus validate-then-apply. Record which of layers 0–3 must move, and whether a new Layer 4 is earned.

## Findings

Claim | Evidence | Confidence
--- | --- | ---
Undergraduate EE needs **both** Anthropic workflows (spice, label, photo) and an agent-shaped host (method, viva, missing-data interview) | Anthropic *Building effective agents*; `workflows/circuits/solve-circuit-problem.yaml` vs `simulate-circuit.yaml` | high
Long YAML that includes `solve-explain` starves the host and is the wrong length for a 2026 coding agent | `solve-circuit-problem.yaml`; PRD FR21; kernel layering note | high
GraSP: load **2–3** focused skills; **compile** retrieved skills to a typed DAG; verify nodes; locality-bounded repair. Do not execute a raw LLM graph | arXiv 2604.17870 | high
ChemCrow pattern: the model plans; **expert tools** own numbers. Kirchhoff/SPICE is the same split | ChemCrow Nature 2024; analog in AnalogCoder generate→sim→repair | high
OpenMontage YAML is a **stage map the host reads**; Python is tools + persistence. Steal schemas and HITL, not “intelligence only in markdown” | OpenMontage ARCHITECTURE.md | high
ToolWeave-style free composition (LLM authors a DAG of any tools at runtime, no domain allowlist) is how fluent `Vout` gets labeled SPICE. Steal type-check; reject new engine nodes in-session | clawrXiv 2026.00002 | high
As-built MCP is only `list_workflows` + `run_workflow`. Hybrid quality cannot live in Layer 2 prose while Layer 1 still mega-applies | `src/electrical_engineer/mcp/server.py` | high
Four-layer table stays. **L2 and L3 must rewrite.** **L1 must change** (ACI). **L0 contract** must name host duties. **L4 is not earned** | this note’s layer table | high

### Three composition options

| Option | What the host does | What Python does | Verdict for EE |
|--------|-------------------|------------------|----------------|
| A — Long YAML brain | Pick one recipe id (`solve-circuit-problem`) | Runner executes retrieve → `solve-explain` → check → label → summary | Reject on **host path**. Starves viva (FR21). Keep only as CLI-without-host / gold **rollback**, and even there prefer **short** physics YAML. |
| B — Unconstrained on-the-fly | Author any tool DAG (`run-spice` + invented `lookup_vout_guess`) | Execute whatever typed | Reject for **writes**. ToolWeave shows the lure; unmatched law and `unchecked` die. |
| C — Hybrid quality | Load 2–3 pack skills; call 5–7 ACI verbs; optionally **propose** an allowlisted engine graph; write `argument.md` | Engines, short attachments, **validator**, gates, eval replay | **Accept.** QUALITY = spend host on viva; clamp physics in engines; still replayable. |

Option C is not OpenMontage purity (YAML as the only control plane, no Python runner). Student-without-host and `electrical-engineer eval` still need a runner. It is not Topology A (gates in markdown). It reopens D13 “router never invents a DAG” **only** into: host may propose a graph of **already registered engines**; the kernel **validates then runs**. Session-invented activities remain forbidden.

### Mapping papers onto EE

**Anthropic workflows vs agents.** A workflow is a predefined code path. An agent is a model directing tools. Spice with `repair_max: 2`, photo confirm, and `label-unchecked` are workflows: same netlist should replay. Choosing KCL vs nodal, interviewing the student, writing the viva are agent-shaped. Today’s `solve-circuit-problem` puts the agent-shaped work **inside** a workflow node (`solve-explain`). That is the starve.

**GraSP.** Focused 2–3 skills beat dumps — pack stubs at `skills/circuits/SKILL.md` (four lines) fail this. Compilation between retrieval and execution is the missing L2 piece: `propose_composition` is a **proposal**, not apply. Node-level verification is already `check-numeric` / spice / `unchecked`. Locality-bounded repair is already `repair_max: 2` on named simulate nodes — keep it inside the engine, not as a host rewrite of Kirchhoff.

**ChemCrow / AnalogCoder.** GPT (or the rented host) plans; expert tools own the exact ops models fail. Do not wrap every node as MCP (45-tool dump). Do not let the host freeze a fluent number as SPICE.

**OpenMontage.** Steal: host reads a catalog; canonical artifact schemas; HITL at irreversible beats (photo, compose). Do not steal: “Python provides tools and persistence only”; crash-resume as identity; video timeline UI. A slightly wrong cut is survivable; a slightly wrong `Vout` is a product fail.

**ToolWeave (clawrXiv).** The agent constructs a typed DAG at planning time; a runtime validates acyclicity and types then executes. Steal the **validate** step. Reject constructing nodes that are not in the engine registry (`lookup_vout_guess`). Unmatched still cannot auto-attach spice because text “looks like a netlist.”

### What is already short enough

[`workflows/circuits/simulate-circuit.yaml`](../../workflows/circuits/simulate-circuit.yaml) is the target length for a **physics attachment**: load netlist → `run-spice` (`repair_max: 2`) → `label-unchecked` → `write-run-summary`. No retrieve. No `solve-explain`.

[`workflows/circuits/solve-circuit-problem.yaml`](../../workflows/circuits/solve-circuit-problem.yaml) is the anti-pattern on the host path: retrieve → `solve-explain` → check → label → summary.

Host-path catalog should advertise **short attachments** (`simulate-circuit`, `simulate-after-confirm`, `photo-to-netlist`, `unmatched-cosolver` without an essay node). Mega `solve-*` / `explain-*` YAML that embed `solve-explain` remain **headless/eval rollback** until a later code plan splits them.

### Layers that must move

Canonical numbering stays 0–3. Do not invent Layer 4 for taxonomy.

| Layer | Move this pass (docs) | Why | Do not |
|-------|----------------------|-----|--------|
| **L2 Domain kernel** | **Must rewrite.** Engines as typed tools; short attachments; validator for allowlisted graphs; YAML = replay not chat brain | Main focus. GraSP compile lives here. | Drop YAML runner; drop `unchecked`; gold as LLM-as-judge |
| **L3 Surfaces** | **Must rewrite.** `evidentiary.json` + host `argument.md`; UI two-band viewer; MCP returns `run_id` + file URIs | Main focus. Two-band is the leave-behind. | ChatGPT-clone UI; WAN bind; KiCad clone |
| **L1 Attach** | **Required.** ACI 5–7 verbs including `propose_composition`; `run_workflow` = short-attachment / eval rollback; host docs name the verbs | Mega `run_workflow` makes L2 fiction | 1:1 node MCP; PTC on spice writes; MCP wait |
| **L0 Harness** | **Contract only.** Host loads 2–3 pack skills, **plans then executes** large jobs (`plan.md`), calls ACI, writes `argument.md`, treats `unchecked` as law | Hybrid unreachable if the rented loop still “just run the YAML” | Unique Electrical Engineer chat loop (H3 falsifier). ChatGPT web as host |
| **L4 (new)** | **Withhold.** Eval stays L2e; pack method stays L2a | Four-layer table is not lying. Eval/governance split would be taxonomy churn | Renumber 0–3 to create an L4 |

```text
Host (+ pack skill)                         L0 contract
  large job? write plan.md first
  → Kernel ACI (5–7 verbs)                  L1
      retrieve | simulate_attachment
      propose_composition | label
      open_ui | eval | list_workflows
  → Validator (allowlist + typed ports)     L2
  → Engine registry                         L2
  → ./runs/<id>/evidentiary.json            L3
      + plan.md + argument.md               L0 writes, L3 stores
  → localhost UI two-band viewer            L3
```

Always-on ACI stays **5–7 verbs**. `propose_composition` **replaces** “simulate = named id only” as the extra write: the host may pass either a **short attachment id** or a **graph of registered engine ids** with typed ports. The kernel rejects unknown activities, unmatched auto-spice, photo-without-UI, and graphs over the existing 16/24 cap. `compose-from-parts --advanced` remains the human-gated cousin for students on the CLI.

### Spend vs clamp (composition)

| Spend (host) | Clamp (kernel) |
|--------------|----------------|
| Which pack skill to load (2–3, not ten) | Engine registry; no session-defined verbs |
| Write `plan.md` on an entire-assignment job, then execute only that plan | `plan.md` cannot mint checked ohms; no Python planner loop |
| Method (KCL vs nodal); viva in `argument.md` | Checked scalars only from engines or `unchecked` |
| Propose retrieve then spice, or skip retrieve | Validator; unmatched cannot auto-spice |
| Ask the student when values are missing | MCP never waits; `open_ui` / `ui_url` |
| Read `evidentiary.json` and cite it | Argument band cannot flip `unchecked` |

### Anti-patterns

- Keep today’s long YAML as the **host-path** brain.
- OpenMontage “intelligence only in markdown” for Kirchhoff.
- Dump every registered node as an MCP tool.
- ToolWeave unrestricted graph authoring for spice writes.
- Add Layer 4 because the user said “L1 or L4.” Adjacent layers are L0 and L1.
- Grow a host-incompatible inner loop so composition “has somewhere to live.”

## Open questions

- Exact JSON shape of a proposed graph (engine id + port map). Default: reuse compose typed-port records; no new schema language until a code plan.
- Whether `list_workflows` stays the catalog name or becomes `list_attachments` once mega solve YAML retires on the host path. Default: keep the name; catalog marks host-path vs rollback.
- When to thicken pack `SKILL.md` bodies (circuits worked example vs all packs). Default: architecture names the contract; circuits example can wait for a skill plan unless critique demands it in ARCHITECTURE.

## Sources

- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — retrieved 2026-09-12 — reliability: primary
- [GraSP — Graph-Structured Skill Compositions for LLM Agents](https://arxiv.org/abs/2604.17870) — retrieved 2026-09-12 — reliability: paper
- [ChemCrow](https://www.nature.com/articles/s42256-024-00832-8) — retrieved 2026-09-12 — reliability: paper
- [OpenMontage ARCHITECTURE](https://github.com/calesthio/OpenMontage/blob/main/docs/ARCHITECTURE.md) — retrieved 2026-09-12 — reliability: primary
- [ToolWeave (clawrXiv 2026.00002)](https://clawrxiv.org/papers/2026.00002) — retrieved 2026-09-12 — reliability: paper
- [`notes/domain-kernel-layering.md`](domain-kernel-layering.md) — retrieved 2026-09-12 — reliability: primary
- [`workflows/circuits/solve-circuit-problem.yaml`](../../workflows/circuits/solve-circuit-problem.yaml) — retrieved 2026-09-12 — reliability: primary
- [`workflows/circuits/simulate-circuit.yaml`](../../workflows/circuits/simulate-circuit.yaml) — retrieved 2026-09-12 — reliability: primary
- [`src/electrical_engineer/mcp/server.py`](../../src/electrical_engineer/mcp/server.py) — retrieved 2026-09-12 — reliability: primary
- [`skills/circuits/SKILL.md`](../../skills/circuits/SKILL.md) — retrieved 2026-09-12 — reliability: primary
- Proposed [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this note: high

Would drop if owner lock keeps mega `run_workflow` as the only host write, or demands unconstrained spice invention, or insists on adding Layer 4 without a missing concern.
