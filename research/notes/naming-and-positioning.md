# Naming and positioning

## Purpose

Score a **product name** (PID Q1) and a **category noun** (what kind of thing this is vs MCP / CLI / plugin / harness / OpenMontage). Reject the working label “Agentic UG EE Studio.” Recommend one pair for the synthesis memo.

## Findings

Claim | Evidence (URL or ledger ID) | Confidence
--- | --- | ---
“Agentic UG EE Studio” fails the sayable-student test: jargon + acronym soup + a video metaphor | sibling self-names in `similar-agentic-domain-systems.md`; this rubric | high
Keep **Electrical Engineer** as the product name. Job-title-as-product is distinctive; CLI/repo already match; coined lab/bench names collide with live products | GitHub search; CircuitLab; EEBench; Fuse; NI Workbench heritage | high
Public category noun: **lab**. OpenMontage’s analog of “studio” for EE students is the course lab, not a production floor | OpenMontage README; student OSS (Zirui, Bhilaee) self-describe as lab | high
Do not use **bench** as the public category: EEBench.org is atopile’s electrical-engineering *agent benchmark*; EEBench is also a physical instrument project; PID already forbids driving a hardware bench | https://eebench.org/ ; Kempten EEBench; `docs/CANNOT_DO.md` CD-MEAS-BENCH | high
Do not use **copilot / assistant** (MATLAB Copilot), **orchestrator** (Karajan), or **MCP server** (SPICEBridge) as the identity | vendor and sibling one-liners | high
Co-solver stays a **mode** (full working + answer), not the category. Students do not search that word | `docs/PID.md` default mode; no student-OSS hits on “co-solver” as a product class | med

### Rejected working label

**Agentic UG EE Studio** — named reject, not a candidate.

- **Agentic** — 2026 repo jargon. OpenMontage uses it; students do not.
- **UG EE** — insider. India-first students say electrical, EEE, or the course name.
- **Studio** — OpenMontage / shotcraft / talkcraft / creator-studio-pack. Video and design. EE siblings (Fuse, AnalogCoder, SPICEBridge, Zirui) never use it.
- Four stacked modifiers is not a spoken name.

### Rubric (applied to every row)

Sayable by a second-year EE student. Distinct from MATLAB Copilot, Eigen, a coding agent, MCP, harness. No plant-floor collision. No studio unless a source shows EE students use it. India-first and still global. GitHub one-liner works. Rename cost if it is a product name. Collision check (search, not a legal opinion).

### Product names

| Candidate | Sayable | Distinct | Collisions | Rename cost | Verdict |
|-----------|---------|----------|------------|-------------|---------|
| **Electrical Engineer** (incumbent) | Yes, long. Spoken: “electrical engineer.” | Yes: job title as the software, not “copilot.” | GitHub hits are course-note dumps and a Julia package `ElectricalEngineering.jl`, not a competing harness-native lab. PyPI has no `electrical-engineer` product in this search. | Zero (repo + CLI already match). | **Keep.** |
| Keep H1, change only subtitle | Yes | Yes if subtitle is “lab” | None new | Zero | This *is* the keep-name strategy. |
| EEBench / EE Bench | Yes | No | [eebench.org](https://eebench.org/) = atopile **electrical engineering agent benchmark** (PCB/SPICE grading). Kempten **EE Bench** = physical FPGA lab hardware. | High and confusing | Kill |
| CircuitLab / Circuit Bench | Yes | No | [circuitlab.com](https://www.circuitlab.com/) commercial sim. PyPI `circuitbench` = ML circuit-design benchmark. | High | Kill |
| Fuse / VoltLab / EEcircuit | Maybe | No | [nimaibhat/fuse](https://github.com/nimaibhat/fuse); VoltLabs VOLT; [EEcircuit.com](https://github.com/eelab-dev/EEcircuit) WASM ngspice | High | Kill |
| Workbench / Electronics Workbench | Yes in lab slang | No | NI / Multisim heritage (“Electronics Workbench”). Sounds like a schematic IDE. | High | Kill |
| ChemCrow-style coinage (OhmCrow, Phasor, Kirchhoff) | Mixed | Maybe | Cute; Kirchhoff is hard to spell; Maxwell collides with Ansys Maxwell (`CD-MACHINES-FEA`) | High | Kill unless a later brand sprint; not this lock |
| OpenEE / OpenLab | Yes | No | OpenLab is a generic everywhere; OpenEE means nothing | High | Kill |

**Product-name pick: Electrical Engineer.** A rename would spend the Q1 lock on a weaker, more collided noun. The problem was never the H1; it was the category nickname.

Runners-up: none worth a CLI rename. If the owner insists on a short alias, use **EE lab** in speech (“run the EE lab”) without changing the binary.

### Category nouns

| Candidate | Student sayable | Collision / risk | Verdict |
|-----------|-----------------|------------------|---------|
| **lab** | Default campus word. “Electrical lab.” | Physical instrument bench is a different thing (already a cannot-do). Student OSS already uses “lab” for coursework sims (Zirui “desktop electrical-lab”; Bhilaee “EE lab experiments”). | **Pick.** |
| coursework lab | Precise, longer | None | Runner-up if “lab” alone feels too hardware |
| system | GitHub-native (OpenMontage “production system”) | Vague for students; “power system” / plant-floor echo | Internal taxonomy only |
| domain system | Accurate for architects | Jargon | Internal only (`research/` and ADRs) |
| bench | Lab-bench slang | EEBench.org + physical EEBench + CD-MEAS-BENCH | Kill for public copy |
| workbench | Engineers know it | NI Electronics Workbench | Kill |
| studio | OpenMontage analog | Video/design; no EE student source | Kill |
| co-solver | Accurate mode | Not a search term | Keep as **mode**, not category |
| environment | MATLAB-ish | Vague | Kill |
| kit / practice | Weak | Kit undersells; practice = law firm | Kill |
| production system | OpenMontage parallel | Plant-floor / power production in EE | Kill in student copy |
| MCP / CLI / plugin / skill / harness | Existing wrong boxes | This is the confusion we are leaving | Kill as identity |

**Category-noun pick: lab.**

Internal (docs, ADRs): **harness-native domain system**, same class as OpenMontage, vertical = undergraduate electrical-engineering lab.

Mode (unchanged): **co-solver**.

### Recommended pair

- **Product name:** Electrical Engineer
- **Category noun:** lab
- **Internal class:** harness-native domain system

**Analog sentence** (OpenMontage → EE):

- OpenMontage: turn your AI coding assistant into a full video production studio.
- Electrical Engineer: **turn your AI coding assistant into an undergraduate electrical-engineering lab.**

**GitHub one-liner:**

Electrical Engineer is an Apache-2.0 **lab** for undergraduate electrical engineering. It sits on Claude Code, Codex, or Cursor, checks numbers with simulators when it can, and labels the rest with the exact token `unchecked`.

**Spoken:** “It’s a lab for electrical, for Claude and Codex — not MATLAB Copilot, not a new ChatGPT.”

### Anti-positioning

| They might think | It is not | It is |
|------------------|-----------|-------|
| MCP | A tool socket | A lab that *has* stdio MCP |
| CLI | The whole product | One surface (`electrical-engineer`) |
| Plugin / skill | A markdown pack | Skills plus simulators, eval, UI |
| Harness | Claude Code / Codex / Cursor | Those hosts; we inhabit them (H3) |
| MATLAB Copilot | In-desktop MATLAB assistant | OSS lab; MATLAB is an optional verifier |
| Siemens Eigen | TIA Portal plant agent | Never plant / PLC |
| Generic coding agent | “Also do circuits” | Named coursework genres + `unchecked` |
| OpenMontage | Video production system | Same *class*, different domain: UG EE lab |
| CircuitLab / EEcircuit | Schematic-in-browser sim | Co-solver + RAG + eval + host adapters |
| EEBench (atopile) | PCB agent leaderboard | Student coursework lab, not a model bakeoff |

### README above-fold (proposal only — do not apply this phase)

H1: Electrical Engineer

One-liner: Apache-2.0 undergraduate electrical-engineering **lab** for Claude Code, Codex, and Cursor (and a local CLI).

Invariant: unverified numbers use the exact token `unchecked`.

Proof: `uv run electrical-engineer eval --pack circuits` (divider `Vout = 5.0`).

Not: MATLAB Copilot, a coding agent that also does circuits, a new harness, Electric Pi.

This is a research proposal. [`README.md`](../../README.md) stays frozen until the vision lock sheet is accepted.

### Why this pair survives India-first and global

India-first students already say “electrical lab” and “EEE lab.” Global UG programs use the same word for coursework labs. “Studio” would read as media. “Bench” would read as hardware or as atopile’s benchmark. “Electrical Engineer” as H1 still matches how the degree is named at Indian and global institutes (`docs/curriculum-map.md`).

## Open questions

- Owner accept/reject of the pair (vision lock sheet).
- Whether spoken alias “EE lab” should appear in the README subtitle. Default: yes, as subtitle, not as a rename.

## Sources

- [`docs/PID.md`](../../docs/PID.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/CANNOT_DO.md`](../../docs/CANNOT_DO.md) — retrieved 2026-09-12 — reliability: primary
- [`research/notes/similar-agentic-domain-systems.md`](similar-agentic-domain-systems.md) — retrieved 2026-09-12 — reliability: primary
- [OpenMontage](https://github.com/calesthio/OpenMontage) — retrieved 2026-09-12 — reliability: primary
- [GitHub search electrical-engineer](https://github.com/search?q=electrical-engineer&type=repositories) — retrieved 2026-09-12 — reliability: secondary
- [CircuitLab](https://www.circuitlab.com/) — retrieved 2026-09-12 — reliability: vendor
- [EEBench by atopile](https://eebench.org/) — retrieved 2026-09-12 — reliability: primary
- [circuitbench on PyPI](https://pypi.org/project/circuitbench/) — retrieved 2026-09-12 — reliability: primary
- [EEcircuit](https://github.com/eelab-dev/EEcircuit) — retrieved 2026-09-12 — reliability: primary
- [Zirui electrical-lab tutoring](https://github.com/handsomeZR-netizen/zirui) — retrieved 2026-09-12 — reliability: secondary
- [Bhilaee simulator](https://github.com/OpenLake/bhilaee-simulator) — retrieved 2026-09-12 — reliability: secondary
- [MATLAB Copilot](https://www.mathworks.com/products/matlab-copilot.html) — retrieved 2026-09-12 — reliability: vendor
- [Kempten EE Bench](https://personalpages.hs-kempten.de/~vollratj/Projekte/2022_EEBench.html) — retrieved 2026-09-12 — reliability: secondary

## Confidence

Overall confidence for this note: high

Keeping the product name is cheap and collision-light. “Lab” is the only category noun that is both student-native and analog to OpenMontage’s “studio” without stealing video language. Confidence would drop if the owner wants a coined brand for GitHub SEO, or if a later trademark screen (not done here) flags “Electrical Engineer” as a product name in a relevant class.
