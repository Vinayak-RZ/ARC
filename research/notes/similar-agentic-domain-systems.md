# Sibling domain systems — catalog

## Purpose

Place Electrical Engineer in a landscape of systems that encode a profession for an AI agent. Record each project’s **self-name**, layer, what to steal, and what not to steal. Feeds the naming note.

## Findings

Claim | Evidence (URL or ledger ID) | Confidence
--- | --- | ---
The same-class pattern is a **repo that inhabits a coding harness** and supplies pipelines, tools, knowledge, QC, and an end artifact — OpenMontage’s one-liner is the type specimen | https://github.com/calesthio/OpenMontage | high
anything2explainer names itself a **skill** but denies CLI identity: “the whole method an AI coding agent needs to finish the film” | https://github.com/Vincentwei1021/anything2explainer | high
EE-adjacent OSS today is mostly **MCP / research agents / canvas products**, not harness-native coursework systems | AnalogCoder, SPICEPilot, SPICEBridge, Fuse (rows below) | high
Vendor copilots (MATLAB Copilot, Siemens Eigen) own the **toolchain loop**, which PID already listed as nearby-wrong | MathWorks Copilot page; Siemens Eigen page; `docs/PID.md` | high
Self-names cluster: “production system / studio” (video), “skill” (thin or thick), “agent” (research), “MCP server” (tool), “orchestrator” (Karajan), “assistant / copilot” (vendors) | this catalog | high

### How to read the tiers

- **Same class:** profession encoded on Claude Code / Codex / Cursor; host is the loop.
- **Thinner pack:** skills or plugins; little verifier spine.
- **Owns the loop:** domain agent with tools as truth, but *they* are the harness.
- **Nearby-wrong:** vendor-in-toolchain, generic coding agent, skill-list, or H4/H5.

Star counts are snapshots on 2026-09-12, not a quality score.

### Same class (profession on a coding harness)

| Project | Self-name / one-liner | Layer | Steal | Do not steal | Conf. |
|---------|----------------------|-------|-------|--------------|-------|
| [OpenMontage](https://github.com/calesthio/OpenMontage) (~58k) | “The first open-source, agentic video production system.” Also: turn your AI coding assistant into a full video production studio. | Domain system on Claude/Cursor/Copilot. YAML pipelines, 100+ tools, 700+ skills, checkpoints, Backlot. | Sit on the harness. Canonical artifacts. Provider selectors. Stage contracts. HITL at irreversible beats. | “All intelligence in markdown.” Crash-resume as identity. “Studio” as EE category (video metaphor). | high |
| [anything2explainer](https://github.com/Vincentwei1021/anything2explainer) (~1.0k) | “Topic in, narrated explainer video out.” Calls itself a Claude Code / Codex **skill**. “It is not a CLI.” Whole method: template, primitives, QC, four checkpoints, reference film. | Thick skill + deterministic Remotion renderer (not generative video). | Paper trail of artifacts. Quantitative QC. Human checkpoints at cost-of-change. Reference output as quality bar. Deterministic renderer analog = SPICE, not a vision model inventing circuits. | PolyForm Noncommercial (we stay Apache-2.0). No CLI-without-host path. Markdown-only method. | high |
| [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (~8.1k) | “AI video skill for Claude Code and Codex — cinematic product videos with Remotion.” Also “motion-design studio.” | Skill + recipe cards + template. | Recipe cards with implementation, not vibes. Aesthetic QA criteria as files. | Shot-card volume as the product. Studio wording. | high |
| [video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) (~0.9k) | “Agent skill that turns Claude Code / Codex into a motion-design studio for voiceover-driven explainer videos.” | Same family as shotcraft. | Triple-acceptance loop until checks pass (Karajan-like QC). | Same as shotcraft. | med |
| [karajan-code](https://github.com/manufosela/karajan-code) (~35) | “Local multi-agent coding orchestrator” with 22 pipeline roles, TDD, MCP; runs on existing subscriptions. | Software-production pipeline **inside** Claude/Codex/Gemini. Deterministic stages: intent, acceptance, guards, TDD. | Split LLM roles from non-LLM gates. Host subscriptions, not a hidden API key. | Software-factory metaphor as EE identity. SonarQube-shaped tooling. | med |

**Implication:** Electrical Engineer already has pipelines (YAML), tools (nodes), MCP, UI, eval. It is closer to this tier than to a plugin. It does not yet teach a host agent the whole method (skills are stubs). OpenMontage is the class analog; Karajan is the QC analog; anything2explainer is the “method + deterministic renderer” analog (renderer = ngspice / python-control).

### Thinner profession packs

| Project | Self-name | Layer | Steal | Do not steal | Conf. |
|---------|-----------|-------|-------|--------------|-------|
| [legal-skills](https://github.com/chen-friedman/legal-skills) | “Open-Source AI Agent Skills for Legal Professionals.” Cross-platform agentskills.io. | One flagship skill; structured `.casebase/` artifacts; local extractors. | Portable skill format. Canonical output files. Fail-visible missing tools (flag, do not fake). | Calling EE “just a skill.” Legal privacy regex as a product. | high |
| [legal-toolkit](https://github.com/jdrodriguez/legal-toolkit) | Claude Code plugin: legal productivity skills. | Plugin / slash commands. | Command surface for genres. | Plugin as the whole identity. | low |
| [creator-studio-pack](https://github.com/flight505/skill-forge/tree/main/plugins/packages/creator-studio-pack) | “Transform Claude Code into your complete creative studio.” | Plugin suite (many small skills). | One-liner pattern (“turn Claude into X”). | Inflated plugin count; studio metaphor. | med |

### Owns the loop (domain agent, tools as truth)

| Project | Self-name | Layer | Steal | Do not steal | Conf. |
|---------|-----------|-------|-------|--------------|-------|
| [ChemCrow](https://github.com/ur-whitelab/chemcrow-public) / [paper](https://www.nature.com/articles/s42256-024-00832-8) | LLM chemistry **agent**; 18 expert tools; GPT-4 plans. | Own ReAct loop. Tools fix exact ops LLMs fail. | Tools as truth. Expert-designed tool surface. Name pattern: discipline + crow. | Own harness (H5). Lab actuation (PID plant-floor analog). | high |
| [paper-qa](https://github.com/Future-House/paper-qa) (~9.2k) | “High accuracy RAG for answering questions from scientific documents with citations.” | Agentic RAG (PaperQA2): search, gather evidence, generate answer, citation traversal. | Citations as contract. Refuse when evidence is thin (cousin of `unchecked`). | Replacing EE RAG spike with PaperQA as the product. | high |
| [AnalogCoder](https://github.com/laiyao1/AnalogCoder) | “Analog Circuit Design via Training-Free Code Generation.” AAAI 2025 LLM **agent**. PySpice + skill library of subcircuits. | Research agent; owns the loop. 20/24 benchmark circuits. | Generate → simulate → repair. Skill library of working circuits. Gold tasks. | Analog IC as public promise (UG bound). Training-free agent as identity. | high |
| [SPICEPilot](https://github.com/ACADLab/SPICEPilot) | Framework for LLM SPICE code generation, benchmarking, error mitigation. | Research bench, not a student product. | Difficulty-tagged gold. Error identification before claiming a pass. | Becoming a SPICE-codegen leaderboard. | med |
| [SPICEBridge](https://github.com/clanker-lover/spicebridge) | “MCP server that gives AI assistants direct access to ngspice.” | **MCP** — tool layer, not the domain system. Already in this repo’s source ledger (S19). | Typed sim tools; spec verification against targets. | Identity = MCP. Cloud tunnel as default. | high |
| [Fuse](https://github.com/nimaibhat/fuse) | README: “agents for electrical engineering.” Web canvas + Claude agent (`add_component`, `connect`, `run_simulation`). | Owns UI + agent loop (H5-shaped). | Live schematic as shared understanding (our localhost UI is the honest cousin). | FastAPI agent loop in-process. KiCad-clone canvas. | med |

### Nearby-wrong

| Project | Self-name | Why wrong for this product | Conf. |
|---------|-----------|----------------------------|-------|
| [MATLAB Copilot](https://www.mathworks.com/products/matlab-copilot.html) | “AI assistant optimized for MATLAB.” In-desktop chat, autocomplete, tests. | Vendor loop inside MATLAB. PID nearby-wrong. We use MATLAB **if present** as a verifier, not as the product. | high |
| [Eigen Engineering Agent](https://www.siemens.com/eigen-engineering-agent) | “Siemens’ next-gen AI for automation engineering. Connected to TIA Portal.” | Plant / PLC toolchain. PID never. | high |
| Generic coding agent (“also do circuits”) | Harness. | No EE genre contracts, no `unchecked`, no simulators. PID is-not. | high |
| Awesome skill lists / 380-skill packs | Skill catalogs. | A list is not a coursework system. | med |
| Electric Pi fork / greenfield harness | H4 / H5. | Locked out (`docs/PID.md`, ADR-0001). | high |

### Name-language harvest (for the naming note)

Spoken category words these projects actually use:

- **system** — OpenMontage (“video production system”)
- **skill** — anything2explainer, shotcraft, talkcraft, legal-skills (undersells thick repos)
- **studio** — OpenMontage one-liner, shotcraft, talkcraft, creator-studio-pack (video/design)
- **orchestrator** — Karajan (software pipeline)
- **agent** — ChemCrow, AnalogCoder, Eigen, Fuse
- **assistant / copilot** — MATLAB Copilot (vendor)
- **MCP server** — SPICEBridge
- **RAG** — PaperQA

None of the EE-adjacent OSS projects call themselves a “studio.” Fuse says “agents for electrical engineering.” AnalogCoder says “agent.” SPICEBridge says “MCP server.” The empty slot is a **student-facing coursework system that sits on a coding harness with simulators as truth.**

## Open questions

- Is Fuse maintained enough to keep as a UI cousin, or only a one-star sketch?
- Do MathWorks agentic toolkits (already S8–S10) count as same-class if they stay MATLAB-hosted?

## Sources

- [OpenMontage README](https://github.com/calesthio/OpenMontage) — retrieved 2026-09-12 — reliability: primary
- [anything2explainer README](https://github.com/Vincentwei1021/anything2explainer) — retrieved 2026-09-12 — reliability: primary
- [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) — retrieved 2026-09-12 — reliability: primary
- [video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) — retrieved 2026-09-12 — reliability: primary
- [karajan-code](https://github.com/manufosela/karajan-code) — retrieved 2026-09-12 — reliability: primary
- [legal-skills README](https://github.com/chen-friedman/legal-skills) — retrieved 2026-09-12 — reliability: primary
- [legal-toolkit](https://github.com/jdrodriguez/legal-toolkit) — retrieved 2026-09-12 — reliability: secondary
- [creator-studio-pack](https://github.com/flight505/skill-forge/tree/main/plugins/packages/creator-studio-pack) — retrieved 2026-09-12 — reliability: secondary
- [ChemCrow Nature paper](https://www.nature.com/articles/s42256-024-00832-8) — retrieved 2026-09-12 — reliability: paper
- [chemcrow-public](https://github.com/ur-whitelab/chemcrow-public) — retrieved 2026-09-12 — reliability: primary
- [paper-qa](https://github.com/Future-House/paper-qa) — retrieved 2026-09-12 — reliability: primary
- [AnalogCoder](https://github.com/laiyao1/AnalogCoder) — retrieved 2026-09-12 — reliability: primary
- [SPICEPilot](https://github.com/ACADLab/SPICEPilot) — retrieved 2026-09-12 — reliability: primary
- [SPICEBridge](https://github.com/clanker-lover/spicebridge) — retrieved 2026-09-12 — reliability: primary
- [Fuse](https://github.com/nimaibhat/fuse) — retrieved 2026-09-12 — reliability: primary
- [MATLAB Copilot](https://www.mathworks.com/products/matlab-copilot.html) — retrieved 2026-09-12 — reliability: vendor
- [Eigen Engineering Agent](https://www.siemens.com/eigen-engineering-agent) — retrieved 2026-09-12 — reliability: vendor
- [`docs/PID.md`](../../docs/PID.md) — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this note: high

Same-class and vendor rows are from live READMEs and product pages. Plugin-pack rows are thinner (legal-toolkit GitHub page returned little README body). A Fuse rewrite or a MathWorks skills-on-Claude launch would move rows between tiers.
