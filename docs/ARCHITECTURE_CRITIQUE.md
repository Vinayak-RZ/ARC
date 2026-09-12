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

(pending)

## Loop 3 — UI / artifacts / token budget

(pending)
