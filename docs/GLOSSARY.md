# Glossary (for contributors)

Plain words for this repo. **Architecture** ([`ARCHITECTURE.md`](ARCHITECTURE.md)) explains how the lab works. **Decisions** ([`../DECISIONS.md`](../DECISIONS.md)) explain why a lock exists. You do not need [`PID.md`](PID.md) to send a first PR.

| Term | Meaning |
|------|---------|
| **Lab / product** | Electrical Engineer: a local UG EE co-solver (CLI + UI + tools for coding agents). |
| **Student** | Undergraduate electrical engineer doing homework. |
| **Host** | The coding agent the student already uses: Cursor, Claude Code, Codex, or ChatGPT desktop. We do not control it. |
| **Kernel** | Our process: simulators, sympy, gates, files, eval. It is the only source of a **checked** number. |
| **Capability** | What kind of physics check is allowed (`lumped-circuit-sim`, `algebraic-check`, …). Allowlist in architecture §0. |
| **Provider** | The program that honours a capability this pass (ngspice, python-control, …). Swappable. |
| **Unchecked** | Exact token. The number was **not** produced by a kernel provider. Not a synonym (“unverified”). |
| **Two bands** | **Results** (numbers, plots, `unchecked`) vs **Method** (viva / explanation). Method cannot turn a number checked. |
| **Viva** | Oral exam: can the student explain the method, not only quote a number. |
| **Attachment** | A short named replay (YAML) of providers, e.g. simulate this circuit. Not the chat brain. |
| **Composition** | The host proposes a small graph of capabilities; the kernel validates, then runs. |
| **Layer 0–3** | Host (0) → our CLI/MCP attach (1) → kernel (2) → UI and files (3). Not a fifth product layer. |
| **MCP** | Tool protocol so the host can call the kernel. Writes never wait on a human. |
| **Gold / eval** | Licence-clean fixtures. `electrical-engineer eval` scores **results**, plus a separate **method checklist** (not essay style). |
| **UI workbook** | Localhost pages: This problem, Past work, Books, Notes. Not a JSON viewer. [`UI.md`](UI.md). |

## Shorthand you will still see

These live in ADRs and requirement IDs. Expand on first read; do not invent new ones in a PR without a glossary row.

| Shorthand | Expand |
|-----------|--------|
| **H3** | We ship a thin CLI around hosts we do not own. We are not a new agent product. |
| **H5** | The fail: a unique Electrical Engineer chat loop hosts cannot share. |
| **FR** | Functional requirement in [`PRD.md`](PRD.md). |
| **ADR** | Architecture decision in [`../DECISIONS.md`](../DECISIONS.md). |
| **D18–D22** | Proposed doc overlays (composition, capabilities, harness, UI, this critic pass). Not code versions. |
| **ACI** | The 5–7 tools the host should call (list, retrieve, simulate, propose graph, label, …). |
| **PTC** | “Power-tool / confirm” style permission on a tool. We do not put that on physics writes. |
| **GraSP** | A paper about compiling skills to graphs. We are **shaped like** it (propose, then validate). We do not implement that paper. |

## What the kernel can and cannot enforce

| Can enforce (if the host or CLI actually called us) | Cannot enforce |
|-----------------------------------------------------|----------------|
| Bad graphs, unknown capability ids, photo without UI confirm | The host answering only in chat and never calling tools |
| `unchecked` on kernel-written results | A fluent number in Cursor that the student never opens in the UI |
| Gold scores on `eval/gold/` | Whether the student could pass a human viva (we only have a method **checklist**) |
