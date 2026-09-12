# PRD critique log (Proposed)

Lead merges. Critics were readonly. Owner intake (ChatGPT desktop first-class, dual MATLAB MCP, split ACI, no ChatGPT web) is not overturned by a critic.

## Loop 1 — fitness (student / harness / TA)

### Accepted

- CLI-without-host: numbers with no model; viva needs local/BYO model or a host; argument band omitted/`unchecked` without a model is honest.
- Public bound vs v1 enabled pack depth called out (ten packs are not equally gold in v1).
- FR18: unlabeled numerals in the argument band fail; provenance names the verifier.
- FR21: host-path YAML must not call `solve-explain`; gold/CLI rollback may keep it.
- FR22: MCP must speak host JSON-RPC framing and not crash on unknown methods; tool I/O includes problem/netlist/`run_id`. As-built NDJSON/`problem.json`-only is a later code defect, now a requirement.

### Rejected (reason)

- Make ChatGPT **web** a host — owner intake; web has no local stdio.
- Drop dual MATLAB MCP / FR20 — owner intake; clamp law stays.
- Printable Given/Find lab-report template as v1 FR — later; `summary.json` + argument band is the v1 leave-behind.
- Cut H3 vocabulary and split ACI from the PRD — implementers need them; student README is a later pass.
- Treat Skills-over-MCP as already shipped — FR22 + host doc: pin root skill until resources exist.
- LLM-as-judge of viva — not added.

## Loop 2 — attach (ChatGPT / dual-MCP / Cursor)

### Accepted

- Chat/Work is first-class **contract**, not skill-loader parity; pin ≠ FR19; Skills-over-MCP stays a Chat/Work method requirement; `eval` is CLI.
- Codex view is the OpenAI inner-loop host; do not market “four harnesses” as if ChatGPT desktop were a fifth runtime. Shared `~/.codex/config.toml`.
- FR20: `label` cannot ingest Copilot/host scalars; only child EE verifier artifacts mint checked numbers.
- This repo `AGENTS.md` stays coding SDLC. Student Cursor: symlink into the student’s skills path; optional ≤10-line homework `AGENTS.md`.

### Rejected (reason)

- Drop Chat/Work from FR4 first-class — owner intake. Degradation is documented, not a demotion to “supported MCP only.”
- Reopen research D5 “MATLAB MCP is the primary verifier” as product identity — PRD: OSS first-class, MATLAB optional.

## Loop 3 — cut (ponytail / sibling / unchecked)

### Accepted

- Pin is v1 Chat/Work method; Skills-over-MCP verify is later. Unify verb count to 5–7. Drop PTC column and v1 Code Mode sentence. `eval_run` is CLI on Chat/Work.
- FR19: skills teach Kirchhoff; they do not enforce FR2 (not Topology A).
- FR9: gold checked only with named EE verifier; `solve-explain` must not mint checked; as-built `ohms-perturbed` is a later eval defect, not a PRD exception.

### Rejected (reason)

- Delete C8, FR10 0.15, reliability §9 restatement — D0 floor / student-facing policy.
- New Kirchhoff residual engine as a separate v1 FR — `check-numeric` / spice already are the predicates.
- Canonical artifact schema framework and eval/gold code rewrite this pass — later plan.
- Demote Chat/Work again — already handled in loop 2.

## Loop 4 — consistency (PID / ARCHITECTURE / shipped)

### Accepted

- Proposed PID (next commit) must: public category **lab**, internal **domain kernel**, mode co-solver; hosts = Cursor, Claude Code, Codex inner-loop, ChatGPT desktop Chat/Work contract; web excluded; host picks recipe id; two-band; FR17–FR22.
- Proposed ARCHITECTURE outline must: four layers; runner-law host clause; 5–7 ACI target vs as-built two tools; ChatGPT desktop in the map; two-band `summary.json`; classifier only when no host driving.
- Inventory honesty: sim nodes are seams; `_solve_value` mint is a defect; omitted-id classifier unwired; divider gold is not live SPICE.

### Rejected (reason)

- Silent new engines in this PRD — none added. Control/LF/spice **implementations** stay a later code plan; contracts remain.
- Rewriting eval gold or MCP framing in this docs pass — FR9/FR22 name the defects; code later.
