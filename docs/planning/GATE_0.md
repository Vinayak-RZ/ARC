# Gate 0 — graph-of-loops ship (W1–W7)

**Status:** Closed 2026-09-21. Do not re-ask on resume.

Skill: `.cursor/skills/graph-of-loops/QUESTIONS.md`. XOR: `graph-engineering` not loaded.

## Research (5–10 lines)

Arc H1 kernel is complete (CLI, YAML runner, localhost UI, MCP, eval). Simulation providers `run-spice`, `run-python-control`, and `run-load-flow` exist as seams but return placeholder/missing results without optional engines. Ship graph wires real ngspice/PySpice RLC, python-control Bode/step plots, and pandapower/sequence fault study, then dedicated control/power UI, fault gold, polish, QA, IITR gap fill, and README domain screenshots last.

## Locked answers (owner 2026-09-21)

| Topic | Answer |
|-------|--------|
| **User** | UG EE student (IITR-like Y1–Y3) |
| **Job** | Solve/verify coursework with checked numbers + real sims |
| **Done when** | Live RLC sim + control Bode/step + power fault demo (UI/CLI); 4–5 domain screenshots in `docs/media/` + README; IITR Y1–Y3 gaps filled or documented with hard blocker |
| **Out of scope** | PG-only EE; live MATLAB/Simulink licence requirement; ChatGPT desktop pack spawn; KiCad/full CAD; PyPI + marketing site |
| **Constraints** | Extend this repo; inherit stack; truth in git + local run artifacts; no multi-tenant auth; CLI + localhost UI; local only |
| **Engines** | ngspice/PySpice RLC; python-control Bode/step; pandapower and/or sequence-network OSS for faults |
| **Budget** | 2–3h wall clock; coalesce commits; **PRIORITY=QUALITY** |

## Wave order (mandatory)

W1 Real engines → W2 Control+power UI → W3 Fault coverage → W4 UI polish → W5 QA → W6 IITR gaps → W7 README shots (after W6).

## Open spikes

None blocking execution. ngspice system binary required alongside PySpice on Linux CI may be optional-extra only.
