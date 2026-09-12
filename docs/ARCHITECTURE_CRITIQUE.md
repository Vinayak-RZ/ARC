# Architecture critique log (Proposed hybrid)

Lead merges. Critics were readonly. Owner locks (H3, QUALITY hybrid, ChatGPT desktop first-class, dual MATLAB MCP, no ChatGPT web, no unconstrained spice) are not overturned by a critic.

## Loop 1 — EE capability / GraSP / ChemCrow

### Accepted

- Hybrid Option C is the right split: host + 2–3 pack skills compose; typed engines own numbers; short attachments stay code; `propose_composition` is validate-then-apply, not ToolWeave.
- Mega `solve-circuit-problem` (retrieve → `solve-explain` → check) stays off the **host path**. Short length = `simulate-circuit`.
- Do not overclaim “GraSP compile.” There is no skill-to-DAG compiler. Wording is **GraSP-shaped**: host proposes registered engines; kernel verifies; `repair_max: 2` stays in simulate engines.
- `propose_composition` allowlist **excludes** `solve-explain`. `run-recipe` children must be short attachments (no nested mega solve YAML). That was the host-path hole (FR21 starve via nest/essay).
- `check-numeric` is first-class on the proposed graph (hand KCL without spice).
- Host-path `unmatched-cosolver`: no essay node; host writes `argument.md`. CLI/gold rollback may keep `solve-explain`.
- Pack stubs are a **method** hole, not a number hole. Skill-body rewrite is a later plan; architecture names the contract. Gates stay in code (FR19).
- Two-band + FR18 unlabeled-numeral fail stays. `argument.md` cannot machine-flip `unchecked`. Human-facing launder waits on the two-band viewer (Layer 3) — specified, not coded this pass.
- PRD FR10/FR17 still say “named id only / compose-from-parts only.” Lead will align those in the PRD delta commit, not by reverting `propose_composition`.

### Rejected (reason)

- Add Layer 4 — eval and pack method already sit in L2; taxonomy is not capability.
- 1:1 MCP dump of registered nodes — FR17 / 45-tool anti-pattern.
- Unconstrained session-invented write DAGs — unmatched law and `unchecked` die.
- Full GraSP skill-compiler before hybrid is useful — typed engines + validator are enough; compile overclaim was a wording bug.
- Delete `solve-explain` entirely — breaks CLI-without-host viva (FR3).
- Treat thick `SKILL.md` as the clamp — Topology A; reject.
- Equate “host may wire `run-spice`” with “host may invent `lookup_vout_guess`” — different trust failures; only the latter is closed as ToolWeave.

### Severity

should-fix (merged). One critic said blocker on as-built `_solve_value` mint and mega `run_workflow`; those remain **known code defects** named in Proposed PRD, not architecture omissions. Docs now close the `solve-explain` / `run-recipe` allowlist hole.

## Loop 2 — H3 / unmatched / dual-MCP / student-without-host / L4

### Accepted

- H3 holds. `propose_composition` is one write verb on a rented loop. A Python multi-turn composition dialog would be the H3/H5 falsifier — named as such in ARCHITECTURE.
- Student-without-host remains complete for **numbers**. Viva is Layer 0 or `solve-explain` fallback.
- Unmatched auto-spice needs a **machine** predicate: spice requires a netlist artifact on a typed port; unmatched is a kernel signal, not skill prose.
- FR20 applies to `check-numeric` as well as `label`: no host/peer Copilot scalars as checked ingest.
- `propose_composition` on MCP must **preflight** ask gates (MATLAB, photo, `ask-human`) and fail closed. Named in the gates table. Do not implement MCP wait.
- Layer 4 **withheld**. Eval stays 2e; pack method stays 2a; two-band stays L3. Four-layer table is not lying.

### Rejected (reason)

- Equating `propose_composition` with a new EE agent product — it is validate-then-apply, not a chat loop.
- Claiming student-without-host is incomplete because the host writes viva — numbers stay complete.
- Dual MATLAB MCP can mint checked through `label` by design — FR20 already closes peer ingest; hole was underspecified `check-numeric`.
- Revert to named-id-only to save unmatched — clamps belong in the validator.
- Add Layer 4 for eval, pack-method, host skills, or two-band — each already has a home.

### Severity

should-fix (merged: unmatched predicate, check-numeric FR20, MCP preflight). L4 verdict: withhold.

## Loop 3 — UI / artifacts / token budget

### Accepted

- Two-band viewer is **specified, not coded**. As-built UI dumps `summary.json` in one pane. ARCHITECTURE now names that gap; filling `run.bands` is a later UI plan, not this docs pass.
- FastAPI+React freeze stays. A static viewer cannot do photo confirm / gates (FR11).
- Always-on is **root skill + 5–7 verb schemas**, not 2–3 packs. Packs load on domain match. Layer 0 contract updated.
- MCP must not return the `propose_composition` graph body; allowlist is server-side so always-on schema stays small.
- Chat/Work pin of root skill stays; do not paste every pack.
- Prose two-band contract is enough this pass. On-disk JSON Schema stays a later P1 (§17 non-goal). Reconcile: §13 names keys; §17 bans Draft-07 files this architecture.
- `summary.json` / `evidentiary.json`: one writer. After rename, alias or replace — never dual live files.

### Rejected (reason)

- Replace FastAPI+React with a static viewer — breaks FR11.
- Merge bands into one “answer” chrome — FR18 product fail.
- In-browser LLM to author `argument.md` — H5.
- Block the architecture on renaming `summary.json` this pass — seed/alias is enough.
- Raise the 800-char budget so MCP can return the DAG — paths-not-bodies dies next.
- Always-on every pack on Chat/Work — contradicts pin-root.
- Ship `schemas/*.json` because OpenMontage has them — YAGNI this docs pass.
- Dual-write summary + evidentiary for compat — two sources of truth.

### Severity

should-fix (merged). One critic called missing UI two-band a **blocker** for FR18 student-facing split. Lead: that is a **code/UI** blocker for a later plan; this pass is docs. The architecture now states the as-built hole so it cannot be mistaken for shipped.

## Loop 4 — Capability-first / any UG question / stack independence

Lead: docs overlay D19. Critics readonly if a later pass runs them. Owner locks (H3, `unchecked`, UG bound, QUALITY hybrid, ChatGPT desktop, no unconstrained spice) stay.

### Accepted

- Architecture identity is **UG coverage**, not ngspice / YAML / FastAPI / LightRAG. Those remain this-pass freezes (§0 identity table).
- Fourteen **capability ids** are the allowlist for `propose_composition`. Provider keys (`run-spice`, …) remain the Python registry until a code plan binds capability→provider.
- **Coverage law:** every curriculum-map pack × seven genres has a complete path. “Solve any UG EE question” = that path, not omniscience and not PG/plant/tape-out.
- Pack `SKILL.md` bodies are method (Given/Find, capabilities, honest holes), not four-line spice pointers. Gates stay in code (FR19).
- `CD-NO-PROVIDER` and `CD-YAML-GAP` are successful co-solver outcomes, not architecture bugs.
- Do not add Layer 4 for the capability table. It lives in L2 next to the provider map.

### Rejected (reason)

- Delete YAML / Python runner so the kernel is “just skills” — student-without-host and eval still need replay (FR3/FR9).
- One unconstrained “run whatever tool the host names” capability — unmatched and `unchecked` die (same as ToolWeave).
- Make FastAPI+React or LightRAG the domain — Layer 3/RAG already had facades; D19 only says so in the identity table.
- Claim v1 gold already covers ten packs equally — depth ≠ bound (PRD §8).
- Rename every as-built activity in Python this pass — docs overlay; code plan later.

### Severity

should-fix (merged in docs). Code still speaks provider keys; that is named, not hidden.

## Loop 5 — Persist / observe / hooks / spawn

Lead: docs overlay D20. No product Python. Owner locks (H3, `unchecked`, local-first) stay.

### Accepted

- Harness split: host owns compaction, continuation, spawn; kernel owns ingest, validate-then-apply, observe, memory write law.
- Named memory files including `lessons.md`; explicit write; propose-not-apply after `unchecked`.
- `observation.json` (or summary seed) with `unchecked_reason`; gold still scores evidentiary only.
- BYO RAG pipeline in prose; `CD-RAG-PARSE` for as-built add-without-chunk.
- Pack specialists are **host-native** adapter markdown under `hosts/adapters/`. Handoff is the run dir. Parent writes `argument.md`.

### Rejected (reason)

- Python orchestrator / CLI that fans out specialists — H5.
- Silent chat-dump memory or fleet learning — FR6 / untrusted.
- Compaction middleware inside the runner — Layer 0.
- Scoring `observation.json` or `errors.md` as SPICE — FR9/FR18.
- Chat/Work pack spawn this pass — Skills-over-MCP not verified.

### Severity

should-fix (merged in docs). Extract/chunk, observation file split, and MCP retrieve remain later code.

## Loop 6 — Student-facing lab UI

Lead: docs overlay D21. No product Python / React. Owner locks (H3, `unchecked`, DESIGN-coinbase tokens) stay.

### Accepted

- Four nav pages + two overlays. Kernel files map to lab surfaces.
- No raw `.md` / `.json` / YAML as the product. Copy dictionary in [`UI.md`](UI.md).
- No reasoning-mode node (host reasons between verbs).

### Rejected (reason)

- Keep as-built `<pre>` JSON viewer — fails the student.
- Dual “power user files” mode in v1 — owner asked for one non-technical product.
- In-UI chat or DAG editor — H5 / host-path composition.
- In-DAG LLM node — FR21 / H5.

### Severity

should-fix (merged in docs). Implementing `ui/` pages waits on a UI code plan.

## Appendix — what changed in docs vs what waits for code

| Specified this pass | Waits for a code plan |
|---------------------|------------------------|
| Hybrid L2/L3, L1 ACI verbs, L0 contract, no L4 | MCP verb split, validator, `propose_composition` |
| Plan-then-execute (FR23); `plan.md`; `apply: false` | Kernel persist of `plan.md`; UI `run.plan` slot |
| Two-band file contract; `run.bands` target | UI two-band viewer, `argument.md` API |
| Host-path unmatched without essay | Split mega YAML recipes |
| FR20 on `check-numeric`; unmatched netlist-port predicate | Engine port checks in Python |
| Capability registry + coverage law (D19); pack method skills | Capability→provider bind in the runner; gold per pack |
| D20 persist/observe/hooks/spawn; BYO ingest pipeline; `hosts/adapters/` | RAG extract/chunk; `observation.json` writer; `memory write` CLI; MCP retrieve |
| D21 lab workbook pages; no file dump; no reasoning-mode node | Implement `ui/` pages, two-pane This problem, Books/Notes |
| Known defects remain named: `_solve_value` mint, as-built two MCP tools | Eval gold / MCP framing fixes |
