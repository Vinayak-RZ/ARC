# Product Identity Document (PID) — Electrical Engineer

**Status:** Accepted (2026-09-12). Aligns with Accepted [`PRD.md`](PRD.md). P0 locks (2026-09-09) still hold; this revision adds lab / domain kernel / ChatGPT desktop / capability coverage.  
**Date:** 2026-09-12  
**Requirements authority after this:** [`PRD.md`](PRD.md)  
**How it is built:** [`ARCHITECTURE.md`](ARCHITECTURE.md)

Thin CLI around existing coding agents, Apache-2.0, UG vs PG, one repo, and the exact token `unchecked` are **not** reopened.

---

## 1. Thesis

Electrical Engineer is an Apache-2.0, forever-open-source undergraduate electrical-engineering **lab**: a **domain kernel** that wraps a rented frontier agent loop (Cursor, Claude Code, Codex, ChatGPT desktop) so the student gets a checked assignment without us becoming a new harness. A branded **local CLI** plus a **persistent localhost UI** are a complete path with no AI host. The kernel’s identity is **coverage of UG EE coursework** (every in-bound pack × genre has a complete co-solver path) via a **capability registry**; simulators, YAML attachments, and the UI stack are swappable providers. Named **short physics attachments** attach simulators; they are not the chat brain. On a large job the host **plans then executes**. The host may propose an allowlisted capability graph; the kernel validates then runs. The product checks numbers with whatever installed provider can honour the capability and labels unverified numbers with the exact token **unchecked**. It is shaped by **real UG coursework** at Indian and global institutes. GATE is an eval instrument, not the product bound. PG, civil, and mechanical are out of the public promise.

## 2. Identity

| Field | Value |
|-------|--------|
| Public name | Electrical Engineer |
| GitHub repo | `Electrical-Engineer` |
| CLI (default) | `electrical-engineer` |
| Public category | Undergraduate electrical-engineering **lab** |
| Internal class | **domain kernel** (host owns the loop; we own **capabilities**, providers, skills, gates) |
| Mode | Co-solver (full working + answer + evidence, or exact token `unchecked`) |
| Geography | India first; must not be weak for global UG EE |
| Licence (our code) | Apache License 2.0 |
| Commercial | Forever OSS in this repo; no paid tier |
| Locality | Local-first CLI + persistent UI on `127.0.0.1`; optional Cursor / Claude Code / Codex / ChatGPT desktop; BYO API key; local models |
| How we ship | **Thin CLI** wrapping portable skills + MCP + local RAG. Deterministic YAML runner as physics/eval backbone. Hosts own the inner loop and the viva. Not an Electric Pi fork. Not a from-scratch chat app. |
| Surfaces | CLI `electrical-engineer`, stdio MCP, **persistent localhost UI** as a **lab workbook** (not a file dump): [`UI.md`](UI.md) |
| Hosts (first-class) | Cursor; Claude Code; Codex (CLI / IDE / desktop Codex view); ChatGPT desktop Chat/Work (**contract**, weaker editor). ChatGPT **web**/mobile are not hosts. |
| Workflows | Short physics attachments **bind** capabilities; host `simulate_attachment` or `propose_composition` of capability ids; CLI-without-host may classify; unmatched co-solver (no essay on host path); does not invent capability or provider ids |
| Repo copies | **One repo only** |
| Unverified numbers | Exact token **unchecked**; never presented as simulation; EE kernel is the only checked-number authority |
| Faculty / TA | None in v1 |
| PG | Not a public promise |
| Civil / mechanical / manufacturing | Never in this product |

**Is:** a student-facing, open, checkable UG electrical-engineering **lab** (domain kernel) that can take **any in-bound UG EE question** (method + checked number or exact token `unchecked`), with named workflows, swappable simulators, tagged local RAG, and a persistent local UI so the student and the host agent can **see** the work.  
**Is not:** Siemens Eigen, MATLAB Copilot, Cadence Cerebrus, an ngspice wrapper, a YAML catalog, a plant-floor controller, a faculty LMS, a GATE-only drill app, a general coding agent with “also do circuits,” a video studio, or a unique agent harness that hosts cannot share.  
**Invariant:** EE tools own checked numbers; unverified numbers use the exact token **unchecked**; diagrams are drafts until the student confirms in the UI; no commercial textbooks in git; peer MATLAB MCP cannot mint checked numbers.

Rejected public nickname: “Agentic UG EE Studio”. “Bench” is not the public noun.

## 3. Who it is for

**Primary:** UG electrical engineering students — India first, including colleges without a MATLAB-fluent TA — who have assignments, labs, and diagrams in circuits, machines, power, control, signals, and electronics. Global UG EE remains first-class.

**In v1 as users, not extra products:** GATE/IES aspirants (exam-style; eval + BYO). Self-learners on UG-equivalent courses.

**Not in v1:** faculty/TA features, PG promise, working plant engineers, civil/mechanical students.

**Never:** control-room operators, live PLC writes, tape-out analog as the product identity.

## 4. Bound: UG coursework, not GATE

Public promise = **union of representative UG EE programmes** (Indian institutes + global institutes). See [`curriculum-map.md`](curriculum-map.md). GATE EE is an **eval overlay**, not the ceiling. Expansion stays in this repo via packs — never a second git repo. v1 **enabled** pack depth may be thinner than the bound ([`PRD.md`](PRD.md) §8).

## 5. Success bar (C1–C8)

Same IDs as `README.md`. Claimable bar: on a published UG task set, with tools on, match gold **or label unchecked**. Fluent wrong numbers presented as checked fail the product. v1 vs later is in the PRD.

## 6. Thin CLI around existing coding agents

```text
Student
  ├─ electrical-engineer CLI   (named workflows, gates, eval, rag inventory)
  ├─ persistent localhost UI   (127.0.0.1; shared understanding)
  └─ Cursor / Claude Code / Codex / ChatGPT desktop
           │
     skills + MCP (5–7 target verbs including propose_composition; as-built: list + run_workflow)
           │
     models: host subscription | BYO API key | local LLM
           │
     verifiers: OSS first-class; MATLAB if present through EE
```

Four layers: (0) rented host harness, (1) attach, (2) domain kernel, (3) UI + two-band artifacts. Detail: [`ARCHITECTURE.md`](ARCHITECTURE.md), [`PRD.md`](PRD.md) §5–§6.

The CLI is a **thin wrapper**: glue, ug profile, co-solver defaults, a **deterministic YAML DAG runner** (short attachments + eval replay), eval, and the local UI. It must not grow into a unique agent loop, including a Python multi-turn composition dialog **or a Python specialist orchestrator**. Hosts keep their own loops, may spawn pack specialists, and write the viva (`argument.md`). The kernel persists runs, memory, and the RAG index and writes observation; it does not compact context or bill tokens.

## 7. Trust (locked)

| Topic | Stance |
|-------|--------|
| Unverified numbers | Exact token **unchecked** in the answer and in the evidentiary band; never call them simulation |
| Diagrams | Draft until the student confirms in the persistent UI |
| Integrity | Co-solver default; institution owns cheating policy; no faculty mode in v1 |
| Student data | Local by default; no silent upload |
| Plant / PLC write | Out of product |
| Copyright | No commercial PDFs in git; BYO or licensed embedding packs |
| Exam items | Exam-style tasks in-scope; **no** third-party copyrighted PDFs committed; BYO allowed |
| Peer MATLAB MCP | Untrusted until an EE engine recomputes |

## 8. Non-goals

- Electric Pi fork, and a from-scratch unique chat app
- Second git repo / UG-freeze fork
- PG as a public promise
- Civil, mechanical, manufacturing
- Faculty LMS, paid product, plant-floor copilots
- Replacing MATLAB or KiCad
- Shipping copyrighted textbooks or live exam PDFs in git
- ChatGPT web/mobile, Claude Desktop, GitHub Copilot, Gemini CLI as v1 hosts

## 9. P1 (accepted with architecture)

| Topic | Stance |
|-------|----------|
| MATLAB vs OSS | MATLAB if present (EE node and/or peer MCP); OSS first-class otherwise; **product works without MATLAB** |
| RAG | Local store; BYO drop → gate → extract → chunk → index → retrieve; inventory + book/chapter/folder tags; no commercial books in git |
| Memory | Project + user markdown; explicit write; `lessons.md` not silent; local-only |
| Persistent UI | First-class local workspace (`electrical-engineer ui`) |
| v1 slice | C1–C3, C6–C7 plus UI + eval layout; C4 photo stub; C5 after C4 |
| First pack | Circuits first, then control ([`WORKFLOWS.md`](WORKFLOWS.md)) |
| Host spawn | Host-native pack specialists (`hosts/adapters/`); not a Python orchestrator |
| Host tools | 5–7 tools including `propose_composition` of **capability ids**; large jobs write `plan.md` first; `run_workflow` = short-attachment / eval rollback ([`PRD.md`](PRD.md) requirement 17) |

## 10. Related artifacts

| Doc | Role |
|-----|------|
| [`PRD.md`](PRD.md) | Requirements |
| [`PRD_CRITIQUE.md`](PRD_CRITIQUE.md) | Four critique loops |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Technical architecture |
| [`ARCHITECTURE_CRITIQUE.md`](ARCHITECTURE_CRITIQUE.md) | Hybrid architecture critique |
| [`WORKFLOWS.md`](WORKFLOWS.md) | Named workflow catalog |
| [`hosts/README.md`](hosts/README.md) | Host install |
| [`PID_DECISION_SHEET.md`](PID_DECISION_SHEET.md) | Historical P0 answers |
| [`curriculum-map.md`](curriculum-map.md) | UG bound |
| [`../DECISIONS.md`](../DECISIONS.md) | ADRs |
| [`UI.md`](UI.md) | Student-facing lab window |
| [`../research/synthesis/vision-lock-sheet.md`](../research/synthesis/vision-lock-sheet.md) | Owner accept/reject sheet |
| [`GLOSSARY.md`](GLOSSARY.md) | Contributor words |

## Sources

- Owner P0 answers (2026-09-09) — reliability: primary
- [`PID_DECISION_SHEET.md`](PID_DECISION_SHEET.md) — reliability: primary
- [`PRD.md`](PRD.md) (2026-09-12) — reliability: primary

## Confidence

Overall confidence that **licence, thin CLI around existing agents, UG bound, and `unchecked` stay locked:** high.  
Overall confidence that **lab / domain kernel / ChatGPT desktop** match owner intake: high.
