# PID decision sheet — answer these

**P0 status:** answered 2026-09-09 and locked in [`PID.md`](PID.md).  
**P1 status:** not answered by owner; PRD records **proposed defaults** for review.  
**P2 status:** unanswered (deferred).

## Owner answers (P0)

| ID | Answer |
|----|--------|
| Q1 | **Arc** (public name, 2026-09-13). Repo stays `Electrical-Engineer`; CLI stays `electrical-engineer` until a code rename. |
| Q2 | India first; must not lack globally |
| Q3 | Apache License 2.0 (owner said 2.2; 2.0 is the current Apache licence, confirmed) |
| Q4 | Local-first CLI; also Cursor / Claude Code / OpenAI; BYO API key; local models |
| Q5 | Forever OSS; no paid product in this repo |
| Q6 | Thesis rewritten (see PID §1) |
| Q7 | Not GATE-bounded; GATE is an eval check; bound = UG courses at multiple Indian and global institutes |
| Q8 | PG not a public promise |
| Q9 | One repo only |
| Q10 | Civil / mechanical never |
| Q-H | **H3** (branded CLI wrapping portable H1 core) |
| Q-H2 | Yes — policy in CLI + skills (not a Pi fork constitution) |
| Q-H3 | N/A (not H4) |
| Q-H4 | N/A for v1 (H3; Cursor/Claude/OpenAI are first-class hosts) |
| Q-S | CLI **and** existing coding harnesses (Cursor, Claude Code, OpenAI) |
| Q-S2 | Yes — student need not use Cursor |
| Q-S3 | `electrical-engineer` |
| Q-R1 | B — label unchecked |
| Q-R2 | A — co-solver |
| Q-R3 | A — no faculty features in v1 |
| Q-R4 | Exam-style items in-scope; **git will not commit third-party copyrighted PDFs**; BYO allowed (legal policy in PRD) |

## P1 proposed defaults (owner may override at PRD review)

| ID | Proposed |
|----|----------|
| Q-V1 / Q-V2 | MATLAB if present; OSS first-class; design for mixed licences |
| Q-K1 | Local RAG (BYO PDFs; no commercial books in git) |
| Q-C | C1–C3 + C6–C7 in first slice; C4 P1; C5 after C4 |
| Q-D1 | Circuits first, then control |
| Q-E3 | Same repo, PG unpublished (not a second fork) |
| Q-N2 | A — no civil/mechanical packs |

## Architecture-aligned product shape (2026-09-10)

Owner answers that upgrade the **product definition** (PRD FRs) without reopening P0. Detail: [`ARCHITECTURE.md`](ARCHITECTURE.md) (still **Proposed**).

| Topic | Product shape |
|-------|----------------|
| Surfaces | CLI + stdio MCP + **persistent localhost UI** (critical) |
| Workflows | Named recipes; hybrid router; unmatched never auto-simulates |
| Unchecked | Exact token `unchecked` (no synonyms) |
| RAG | Inventory + book/chapter/folder tags; quality is first-class |
| Memory | Capped markdown files, two scopes, untrusted |
| Eval | `eval/gold/` + `electrical-engineer eval` |
| MATLAB | Optional; whole product works without it |
| Photo | Stub: UI confirm, no sim in first slice |

Original questions follow for traceability.

---

Reply in chat by ID (example: `Q1 = B`, `Q-H = H4`, comments after).  
**P0** = do not lock the PID without this. **P1** = needed before v1 code. **P2** = can wait.

Skip is allowed: write `skip — reason`. Do not leave P0 blank if you want an Accepted PID.

Legend for harness (same as `PID.md` §6):

- **H1** Portable skills + MCP + local RAG (no owned harness)
- **H2** H1 + optional Pi package
- **H3** Branded CLI wrapping H1 (not a full unique harness)
- **H4** Electric Pi — hard fork of Pi, EE constitution in the harness
- **H5** Greenfield harness from zero

---

## P0 — identity and bounds

**Q1. Public product name**  
A. Keep `Electrical-Engineer`  
B. `Electric Pi` (or similar) even if we do not fork Pi  
C. A student-facing name (write it)  
D. CLI name different from GitHub name (write both)

**2026-09-13 amendment:** public name is **Arc** (C + D). GitHub repo and CLI binary stay `Electrical-Engineer` / `electrical-engineer` until a code rename. README one-liner: turn your AI coding assistant into an undergraduate electrical engineer (not “lab”).

**Q2. Primary audience geography**  
A. India UG/PG first, English UI, international welcome  
B. Global UG EE equally  
C. India only for v1

**Q3. Licence for *our* code (not textbooks)**  
A. MIT  
B. Apache-2.0  
C. AGPL-3.0 (copyleft if someone ships a hosted tutor)  
D. Other (write)

**Q4. Locality bar**  
A. Fully local possible (models + RAG + sim on machine); cloud LLM optional  
B. Cloud LLM OK; RAG and PDFs stay local  
C. Cloud LLM + cloud vision OK  
D. Local models required (no API keys)

**Q5. Commercial**  
A. Fully OSS, no paid product in this repo ever  
B. OSS core, later paid hosted/faculty tier in a different product  
C. Undecided, design as if A

**Q6. One-sentence product definition**  
Accept the PID thesis, or paste your rewrite.

**Q7. UG-bounded means**  
A. GATE EE syllabus + typical Indian UG assignments  
B. That plus IIT/NIT core courses even if beyond GATE  
C. Any English-language UG EE worldwide  
D. Write a custom bound (which universities / which years 1–4)

**Q8. PG in the *public* product**  
A. Not in the promise; only a later fork/profile  
B. PG coursework in v1 promise too  
C. PG allowed in UI but marked experimental

**Q9. Two-copy vision**  
A. Two git repos/forks (UG frozen vs lab)  
B. One repo, two release tags  
C. One install, `--profile ug|pg|research`  
D. Monorepo packs; UG is default install set  
E. Combination (write)

**Q10. Non-EE core (civil, mechanical, manufacturing)**  
A. Never in this product  
B. Out of v1; architecture may keep pack sockets  
C. You want a family of products later under one harness

---

## P0 — harness and surface (the main product choice)

**Q-H. Harness (pick one primary)**  
H1 / H2 / H3 / H4 / H5  
If hybrid: write primary + “also ship ___”.

**Q-H2. If not H4:** are you OK with EE verification policy living in skills/CLI rather than a forked Pi constitution?  
A. Yes  
B. No — then H4 or H5

**Q-H3. If H4 Electric Pi:** still ship portable MCP/skills so Cursor users work?  
A. Yes, dual (fork + portable core)  
B. No, students must use Electric Pi  
C. Portable core first, fork later

**Q-H4. Pi MCP gap:** if we need MCP on Pi, you prefer  
A. Depend on `pi-mcp-adapter` (or successor)  
B. We write/maintain the MCP extension  
C. Don’t care; Cursor is the real host  
D. Fork Pi partly *to add* first-class MCP

**Q-S. Primary student surface for v1**  
A. Cursor / Claude Code / Codex (MCP + skills)  
B. CLI  
C. Local web/chat UI  
D. Pi interactive CLI  
E. A then B (hosts first, CLI for evals)  
F. Other

**Q-S2. Must a student who never uses Cursor be able to run v1?**  
A. Yes (CLI or UI required)  
B. No (Cursor-class host is OK for v1)

**Q-S3. Branded command name** (if CLI or fork)  
Write it, or `none`.

---

## P0 — reliability and integrity

**Q-R1. Unverified numeric answers**  
A. Hard refuse (no number without tool)  
B. Number allowed if labelled “unchecked, do not trust”  
C. Model may answer; tools optional

**Q-R2. Academic integrity default mode**  
A. Co-solver: full working + answer (student’s ethics)  
B. Tutor: hints first, full solution on request  
C. Tutor until N turns, then unlock  
D. Faculty-configurable; default B  
E. Separate “exam” vs “homework” modes

**Q-R3. Faculty / TA features in v1**  
A. None  
B. Review-student-solution mode only  
C. Generate assignment variants + rubric  
D. Later

**Q-R4. Live GATE / university exam papers in the corpus**  
A. Never  
B. Only expired / official practice, licence-clean  
C. User BYO only

---

## P1 — verification and knowledge

**Q-V1. Numeric backend default**  
A. MATLAB/Simulink if present, else OSS, and OSS must feel first-class  
B. OSS-primary; MATLAB extra  
C. MATLAB required for v1  
D. I have a MATLAB licence on the machines that matter (yes/no) — answer even if you pick A/B/C

**Q-V2. Confirm MATLAB situation**  
A. Personal or campus licence, will use MCP  
B. No licence, OSS only for now  
C. Mixed (you have it, many students will not) — design for C

**Q-V3. OSS SPICE preference if we must pick one later**  
A. ngspice (open)  
B. LTspice (if students already have it)  
C. Defer; spike both  
D. No opinion

**Q-K1. RAG in v1**  
A. Required (local Chroma/sqlite-vec)  
B. v0 skills-only, RAG immediately after  
C. RAG only if BYO PDF works; no embedding-pack distribution  
D. Skip RAG until evals prove models fail without it

**Q-K2. Embedding packs on GitHub Releases**  
A. Goal, after per-title licence review  
B. Never redistribute embeddings; BYO ingest only  
C. OER / openly licensed texts only

**Q-K3. Languages of textbooks / UI**  
A. English only  
B. English UI; user may BYO Hindi (or other) PDFs  
C. Hindi UI in scope later  
D. Other languages (write)

**Q-K4. Fine-tune / custom EE model**  
A. Out of scope; use frontier + local APIs  
B. Interested later  
C. Want a local small model story in v1

---

## P1 — diagrams and capabilities

**Q-C. v1 capability slice** (pick one)  
A. C1 C2 C6 C7 only (text + tools, no vision)  
B. A + C3 genres except report  
C. A + C3 + C4 circuits diagrams  
D. Full C1–C7 including C5 control diagrams  
E. Custom list (write IDs)

**Q-C2. If diagrams slip:** is a text-only co-solver still a product you would ship?  
A. Yes  
B. No, diagrams are the point  
C. Ship text, but do not call it v1 success

**Q-C3. Circuit vision locality**  
A. Local VLM only  
B. Optional cloud vision with a warning  
C. Defer until local is good enough

**Q-C4. Schematic editor**  
A. Minimal local web canvas  
B. Export to KiCad / existing tool and edit there  
C. ASCII/Schemdraw + SVG is enough for v1  
D. Defer with C4

**Q-D1. First domain pack (depth before breadth)**  
A. Circuits only  
B. Circuits + control  
C. Circuits + power  
D. All GATE sections thin  
E. Other pair (write)

**Q-D2. GATE MCQ vs long assignments**  
A. Long assignments / numerical first  
B. GATE-style MCQ first  
C. Both in v1  
D. Assignments first, GATE later

**Q-D3. Lab reports (genre Report)**  
A. v1  
B. After solve/explain work  
C. Out of UG product

---

## P1 — evals and the “limits of AI” mission

**Q-E1. Public eval**  
A. Yes, licence-clean gold tasks in-repo or a sibling repo  
B. Private until quality is decent  
C. Metrics only, tasks not public (prevents training contamination)

**Q-E2. Success metric you would accept as “v1 worked”**  
Write in your words (e.g. “circuits pack, 50 gold items, refuse-unverified never violated, explanations I would mark 7/10”). Do not invent a fake %. We will turn your words into a rubric.

**Q-E3. C8 research-fork timing**  
A. After UG v1  
B. Parallel from the start (same repo, different profile)  
C. Separate repo when UG is boring to you

---

## P1 — install, platforms, models

**Q-P1. Target OS for v1**  
A. Linux + macOS + Windows  
B. Linux first (you and CI)  
C. Whatever Cursor users already have

**Q-P2. Student laptop assumption**  
A. Cheap 8 GB RAM must work (OSS + API model)  
B. 16 GB OK (local embeddings + small VLM)  
C. Desktop/lab machine OK for diagrams

**Q-P3. Default LLM**  
A. User brings any API (OpenAI/Anthropic/etc.)  
B. Recommend one paid API  
C. Recommend local (Ollama) as default  
D. You will pick a vendor later; architecture must not lock

**Q-P4. Offline exam-hall mode**  
A. Not a goal  
B. Nice-to-have later  
C. Hard requirement

---

## P2 — product extras (answer if you already know)

**Q-X1. Logo / branding now?** A. Later  B. Yes, with PID

**Q-X2. Discord/community?** A. No  B. Later  C. Yes with v1

**Q-X3. Instructor LMS (Moodle/Google Classroom)?** A. Never  B. Later  C. Influences v1

**Q-X4. Mobile?** A. Never  B. Later  C. WhatsApp/Telegram bot interest (write)

**Q-X5. Voice?** A. No  B. Later

**Q-X6. Multi-user / class roster?** A. No, single student machine  B. Later faculty

**Q-X7. Telemetry?** A. None  B. Opt-in anonymous eval stats  C. Required for the limit-finding mission

**Q-X8. Contribution model**  
A. You + agents only for a while  
B. Public issues, DCO/CLA later  
C. Full community from v1

**Q-X9. Trademark / GitHub org name** — keep `Vinayak-RZ/Electrical-Engineer`?  
A. Yes  B. Move to an org (write name)

**Q-X10. README stance after PID accepted**  
A. Keep research-honest (“no shipped agent”) until code exists  
B. Rewrite as product landing immediately (even pre-code)

**Q-X11. Spec Kit (`.specify/` constitution → spec → plan)**  
A. Yes, after Accepted PID  
B. nawab plan only, skip Spec Kit  
C. PID is enough, go to a thin implement plan

**Q-X12. Language of agent explanations**  
A. English  
B. English + optional simple-English  
C. Student can ask Hindi explanations (model-dependent)

**Q-X13. Notation**  
A. SI only  
B. SI + common Indian textbook mixed units with conversion  
C. Match the user’s question

**Q-X14. Photographed handwritten numerical work (not just circuit diagrams)**  
A. v1  B. Later  C. Out

**Q-X15. MATLAB Copilot vs this product**  
A. Complementary (we are the assignment/diagram agent; Copilot is in-MATLAB)  
B. We should overlap Copilot (in-MATLAB workflows)  
C. No opinion

**Q-X16. Relationship to Cursor**  
A. First-class host among several  
B. *The* host for v1  
C. Implementation tool only; students need not use Cursor

**Q-X17. Hard step limit / autonomy**  
A. Short loops, lots of checkpoints (safer teaching)  
B. Long loops OK if tools check  
C. You decide per mode (tutor short, co-solver longer)

**Q-X18. Human checkpoint on:** (multi-select)  
A. Every simulation  
B. Only diagram topology  
C. Any file write  
D. Netlist export  
E. None beyond first run

**Q-X19. Error budget:** if the agent is unsure between two methods  
A. Show both + tool-check both  
B. Pick one, state the assumption  
C. Ask the student

**Q-X20. “Pretty much any question”** — when a question is outside packs  
A. Refuse with “out of UG profile / out of enabled packs”  
B. Try anyway, label unverified  
C. Auto-enable research profile

---

## P2 — Electric Pi specifically (answer if Q-H is H4 or you are tempted)

**Q-PI1.** Fork point: track Pi `main` how often? A. Closely  B. Periodic merges  C. Soft fork, rarely merge  

**Q-PI2.** Default EE constitution in the fork: write any *must* rules besides verify-or-refuse and explain-with-assumptions.

**Q-PI3.** Interactive TUI themes/modes (tutor/co-solver/reviewer) — P0 for the fork? A. Yes  B. Later  

**Q-PI4.** Are you prepared to maintain TypeScript extension surface as Pi changes? A. Yes  B. That’s why you prefer H1/H2

---

## P2 — naming the expansion sockets (optional now)

**Q-N1.** First expansion you personally care about after UG circuits:  
A. Control diagrams  B. Power systems  C. Machines  D. PG analog  E. Something else (write)  
This does not have to be v1; it tells us where to leave the thickest sockets.

**Q-N2.** Would you ever want this harness reused for a *civil* or *mechanical* student agent as a separate pack family?  
A. No  B. Maybe, keep names EE-specific anyway  C. Yes, keep domain-agnostic core names (`packs/`, `policy/`, `verifiers/`)

---

## Freeform (please use)

**Q-F1.** What would make you *delete the repo* as a failure?  
**Q-F2.** What would make you call v1 a success even if diagrams are ugly?  
**Q-F3.** Anything you think I assumed wrongly in `PID.md`?  
**Q-F4.** Priority for the main harness trade-off: `SPEED` | `PORTABILITY` | `IDENTITY` | `CONTROL` | `SIMPLICITY` | mix (write).

---

## How I will use your answers

1. Fill OPEN rows in `PID.md`.  
2. Mark harness H* as **Accepted** (or a stated hybrid).  
3. Shrink v1 to the slice you picked.  
4. Only then write the execution plan (nawab / Spec Kit if you chose Q-X11).  
5. I will **not** start product code until you accept that plan.

If you want to answer in batches, do **all P0 first**. That is enough for a second PID revision.
