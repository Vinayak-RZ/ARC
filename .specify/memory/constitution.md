# Arc Constitution

**Version:** 1.0.0  
**Ratified:** 2026-09-09 (PID P0)  
**Last amended:** 2026-09-13 (public name Arc; README analog without “lab”)

Non-negotiable product law. Feature specs, architecture, and code MUST comply.
Amendments require an owner decision recorded in `DECISIONS.md`.

## Principles

### I. H3 harness, never H4 or H5

The product is a branded CLI wrapping portable skills, stdio MCP, local RAG, and a
deterministic YAML DAG runner. Hosts (Cursor, Claude Code, OpenAI) own the main
LLM loop. The CLI MUST NOT grow a unique agent harness hosts cannot share (H5).
The product MUST NOT be an Electric Pi / Cordis / DSH fork (H4).

### II. Exact token `unchecked`

If a number did not come from a verifier, the student-facing answer AND the run
summary MUST contain the exact token `unchecked`. Synonyms are not the contract.
Unverified numbers MUST NOT be presented as simulation or lab results.

### III. Local-first, localhost UI

Default is on-device files plus a persistent UI bound to `127.0.0.1` only.
No product cloud. No silent upload of PDFs, keys, or student work. Secrets live
in environment / host stores. Run dirs MUST redact keys.

### IV. UG coursework bound

Public promise is the union of representative UG EE programmes
(`docs/curriculum-map.md`). GATE is an eval overlay, not the syllabus.
PG is not a public promise. Civil, mechanical, and manufacturing are never
this product. One git repository only.

### V. Apache-2.0 and copyright hygiene

Our code is Apache License 2.0, forever OSS in this repo, no paid tier.
Git MUST NOT contain commercial textbooks or third-party exam PDFs.
BYO files on the student machine are allowed and untrusted: they MUST NOT
override gates or `unchecked`.

### VI. Named workflows, not invented graphs

The router picks a catalog id, asks when scores are within 0.15, or uses
`unmatched-cosolver`. The router MUST NOT invent a DAG. New graphs only via
`compose-from-parts --advanced` (typed ports, ≤16 nodes, ≤24 edges).
MCP `run_workflow` MUST never wait on humans (fail closed + `ui_url`).

### VII. Diagrams are drafts until confirm

Photo and control-diagram stubs write a draft then stop. Simulation of a
photo-derived netlist MUST wait for explicit UI confirm. Low-confidence OCR
MUST be flagged.

## Governance

- P0 PID locks (H3, Apache-2.0, UG, `unchecked`, one repo) reopen only with a
  new owner decision.
- Versioning: MAJOR = principle removal/redefinition; MINOR = new principle;
  PATCH = wording.
- Compliance: `scripts/validate.sh` and eval injection tests enforce II, III, VI
  where automated.
