# Vision lock sheet (WS-G)

## Purpose

Owner accept/reject for class, names, orchestrator split, and layering.

**2026-09-12:** D14–D17 are written into **Proposed** [`docs/PRD.md`](../../docs/PRD.md), [`docs/PID.md`](../../docs/PID.md), and [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md). Owner checkboxes below stay empty until you Accept. Root `README.md` is **not** rewritten this pass.

## Findings

Claim | Evidence | Confidence
--- | --- | ---
Research recommends: keep product name Electrical Engineer; public category **lab**; internal class **domain kernel**; topology **C** plus CLI-inner/MCP-outer layering | `synthesis/domain-system-recommendation.md`; `notes/domain-kernel-layering.md` | high
H3, UG bound, `unchecked`, co-solver mode, student-without-Cursor, Apache-2.0, no plant-floor stay frozen even if this sheet is accepted | `docs/PID.md` | high

### Frozen (do not reopen here)

- H3 branded CLI wrapping portable skills + MCP; not H4; not H5
- Licence Apache-2.0; forever OSS in this repo
- UG coursework bound; GATE is eval overlay; PG not a public promise
- Exact token `unchecked`; co-solver default; no faculty v1
- Student need not use Cursor (CLI + localhost UI)
- Civil / mechanical / plant-floor / second git repo: never
- YAML runner as deterministic backbone (D13); no crash-resume

### Proposed (accept or reject)

**D14 Product name**

- Keep **Electrical Engineer** (repo `Electrical-Engineer`, CLI `electrical-engineer`).
- [ ] Accept
- [ ] Reject — write the alternative here only after a new naming note

Written into Proposed PID/PRD 2026-09-12 (not owner-Accepted).

**D15 Category noun**

- Public: **lab** (undergraduate electrical-engineering lab).
- Internal: **domain kernel** (harness-native; same class as OpenMontage).
- Mode: co-solver (unchanged).
- Named reject: “Agentic UG EE Studio”.
- Analog: turn your AI coding assistant into an undergraduate electrical-engineering lab.
- [ ] Accept
- [ ] Reject

Written into Proposed PID/PRD 2026-09-12 (not owner-Accepted).

**D16 Orchestrator split**

- Topology C: host agent orchestrates the *work*; Python owns verifiers, gates, eval, UI.
- Router still never invents a spice DAG. Unmatched never auto-simulates.
- Does not reopen H5. Does not drop the YAML runner.
- [ ] Accept
- [ ] Reject (A markdown control plane / B YAML-as-brain)

Written into Proposed PID/PRD/ARCHITECTURE 2026-09-12 (not owner-Accepted).

**D17 Domain-kernel layering**

- Four layers: (0) rented host harness, (1) attach (CLI inner, MCP outer; Chat/Work pin until Skills-over-MCP), (2) domain kernel, (3) UI + two-band artifacts.
- Spend the host on method, viva, student interview. Clamp numbers, invented spice DAGs, photo confirm, and `unchecked` in code.
- Host-path ACI: 5–7 verbs; mega `run_workflow` that includes `solve-explain` is headless/eval rollback, not the only chat path.
- Dual MATLAB MCP allowed; EE is the only checked-number authority.
- Steal no-bypass writes from executive kernels. Do not steal their loop (H5). Do not steal studio timeline UI.
- [ ] Accept
- [ ] Reject

Written into Proposed PRD FR17–FR22 / ARCHITECTURE §2 2026-09-12 (not owner-Accepted).

**D18 Host-path composition (hybrid quality)**

- Host + 2–3 pack skills (on-demand) compose the job. Typed engines own numbers. Short physics attachments stay as YAML replay. Host may `propose_composition` of **allowlisted** engines; kernel **validates then runs**.
- Mega YAML including `solve-explain` retires on the **host path** (CLI/gold rollback only).
- Reopens D13 “router never invents a DAG” **only** this far — not ToolWeave free spice, not session-invented `lookup_vout_guess`.
- L0 contract and L1 ACI updated because the hybrid requires them. **No Layer 4.**
- Large jobs **plan then execute** (`plan.md` before spice). `propose_composition apply: false` validates without running. Not an eighth verb. Not a Python planner (H3).
- [ ] Accept
- [ ] Reject

**D19 Capability-first coverage (any UG EE question)**

- Capability registry is the domain contract; providers and YAML/UI/RAG engines are this-pass freezes.
- Coverage law: every in-bound pack × genre has a complete path (check or `unchecked`).
- `propose_composition` may name capability ids; kernel binds providers. Pack skills teach method, not a single simulator.
- [ ] Accept
- [ ] Reject

Written into Proposed ARCHITECTURE §0, PRD FR10/FR19, pack `skills/` 2026-09-12 (not owner-Accepted).

**D20 Harness persist, observe, spawn**

- Host owns loop, compaction, continuation, and native specialist spawn. Kernel owns runs, memory files, RAG ingest pipeline, observation, deterministic hooks.
- Memory improves **this student** only: explicit write; `lessons.md` proposed after `unchecked`, never silent.
- Adapter prompts in `hosts/adapters/`. Not a Python multi-agent runtime (H5).
- [ ] Accept
- [ ] Reject

Written into Proposed ARCHITECTURE §0.3/§2.5/§10–§11, PRD FR13/FR19/FR24, `hosts/adapters/` 2026-09-12 (not owner-Accepted).

**D21 Student-facing lab UI**

- Four nav pages (This problem, Past work, Books, Notes) + Confirm / Ask overlays. Maps kernel files to cards, tables, figure grids, rendered prose.
- Never present `.md` / `.json` / YAML as the product. DESIGN-coinbase. Exact token `unchecked` stays with a plain gloss.
- No reasoning-mode node in composition graphs.
- [ ] Accept
- [ ] Reject

Written into Proposed [`docs/UI.md`](../../docs/UI.md), ARCHITECTURE §9, PRD FR11, ADR-0012 2026-09-12 (not owner-Accepted).

**D22 Host-skip, glossary, viva axis**

- Lab-checked = kernel Results only. Chat freelance is `CD-HOST-SKIP`. CLI+UI backstop. No Python nag-loop.
- How vs why: architecture preamble + [`docs/GLOSSARY.md`](../../docs/GLOSSARY.md); ADRs stay dense.
- Eval two axes: numbers vs method checklist. Not a human viva (`CD-VIVA-SIGNAL`).
- [ ] Accept
- [ ] Reject

Written into Proposed ARCHITECTURE (How the lab works; When the host does not comply; §14), PRD FR25/FR26, ADR-0013 2026-09-12 (not owner-Accepted).

### Later docs pass

**Done as Proposed (2026-09-12), not Accepted:** PID category/hosts, PRD thesis + agent interaction, ARCHITECTURE four-layer map, hybrid L2/L3 composition (D18), capability-first coverage (D19), harness persist/observe/spawn (D20), student-facing lab UI (D21), critic follow-up host-skip/glossary/viva (D22).

**Still waiting on owner Accept:** checkboxes above; then root `README.md` (product-readme) and `DECISIONS.md` ADR (ADR-0009 through ADR-0013 stay **proposed** until then).

Would not change until a **code** plan: runner capability→provider bind, RAG extract/chunk, observation writer, `memory write`, MCP verb split, **UI pages in `ui/`**, `expect-viva.json` scorer, CLI binary name, PyPI, HTTP MCP.

### Stop line

Owner checkboxes above are empty on purpose. Root README is unchanged until you Accept. This pass did not ship MCP verb splits, ingest parsers, or React UI pages. Root `skills/SKILL.md` is coverage + plan-then-execute + memory/spawn law. Pack specialists copy from `hosts/adapters/`. Student UI IA is [`docs/UI.md`](../../docs/UI.md).

## Open questions

- Spoken alias “EE lab” in the README subtitle (naming note default: yes, as subtitle only).

## Sources

- [`research/synthesis/domain-system-recommendation.md`](domain-system-recommendation.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/naming-and-positioning.md`](../notes/naming-and-positioning.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/domain-system-architecture-patterns.md`](../notes/domain-system-architecture-patterns.md) — retrieved 2026-09-12 — reliability: primary
- [`research/DECISION_REGISTER.md`](../DECISION_REGISTER.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/agentic-kernel-2026.md`](../notes/agentic-kernel-2026.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/domain-kernel-layering.md`](../notes/domain-kernel-layering.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/hybrid-engine-composition.md`](../notes/hybrid-engine-composition.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/PID.md`](../../docs/PID.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/UI.md`](../../docs/UI.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/GLOSSARY.md`](../../docs/GLOSSARY.md) — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this sheet: high

The recommendations are sourced. The checkboxes are the owner decision; empty boxes are intentional, not unfinished tokens.
