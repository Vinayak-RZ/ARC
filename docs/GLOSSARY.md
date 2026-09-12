# Glossary (for contributors)

**Status:** Accepted (2026-09-12).

Plain words. [`ARCHITECTURE.md`](ARCHITECTURE.md) is how the lab works. [`../DECISIONS.md`](../DECISIONS.md) is why a lock exists. You do not need [`PID.md`](PID.md) to send a first PR.

| Term | Meaning |
|------|---------|
| **Lab / product** | Electrical Engineer: a local undergraduate EE co-solver (command line, local window, tools for coding agents). |
| **Student** | Undergraduate electrical engineer doing homework. |
| **Host** | The coding agent the student already uses: Cursor, Claude Code, Codex, or ChatGPT desktop. We do not control it. |
| **Kernel** | Our process: simulators, sympy, gates, files, eval. It is the only source of a **checked** number. |
| **Capability** | What kind of physics check is allowed (`lumped-circuit-sim`, `algebraic-check`, …). List in architecture §0. |
| **Provider** | The program that honours a capability this pass (ngspice, python-control, …). Swappable. |
| **Unchecked** | Exact token. The number was **not** produced by a kernel provider. Not a synonym (“unverified”). |
| **Results / Method** | Two sides of a problem: numbers, plots, and `unchecked` vs the viva / explanation. Method cannot turn a number checked. |
| **Viva** | Oral exam: can the student explain the method, not only quote a number. |
| **Attachment** | A short named replay of providers, e.g. simulate this circuit. Not the chat brain. |
| **Composition** | The host proposes a small graph of capabilities; the kernel validates, then runs. |
| **Host / tools / kernel / screens** | The four parts: the student’s coding agent; our CLI and MCP tools; physics and files; the local lab window. |
| **MCP** | The tool protocol so the host can call the kernel. Tool writes never wait on a human. |
| **Gold / eval** | Licence-clean fixtures. `electrical-engineer eval` scores **results**, plus a separate **method checklist** (not essay style). |
| **Lab window** | Local pages: This problem, Past work, Books, Notes. Not a JSON viewer. [`UI.md`](UI.md). |

Requirement numbers (FR…) live only in [`PRD.md`](PRD.md). Decision records live only in [`../DECISIONS.md`](../DECISIONS.md). Do not invent new letter-codes in a PR.

## What the kernel can and cannot enforce

| Can enforce (if the host or CLI actually called us) | Cannot enforce |
|-----------------------------------------------------|----------------|
| Bad graphs, unknown capability ids, photo without UI confirm | The host answering only in chat and never calling tools |
| `unchecked` on kernel-written results | A fluent number in Cursor that the student never opens in the UI |
| Scores on `eval/gold/` | Whether the student would pass a human viva (we only have a method **checklist**) |
