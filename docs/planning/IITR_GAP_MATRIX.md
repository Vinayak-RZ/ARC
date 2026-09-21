# IITR Y1–Y3 gap matrix (EE core)

**Source:** IITR NEP PCC EEC-* 2023–24 programme page + `docs/curriculum-map.md` union.  
**Date:** 2026-09-21 (pass 2)  
**Rule:** Each row is **shipped** (recipe/skill/UI path), **partial**, or **blocker** with reason.

| IITR-aligned topic | Pack | Capability / recipe | Status | Notes |
|--------------------|------|---------------------|--------|-------|
| Circuit theory, DC/AC, transients | circuits | `simulate-circuit`, `solve-circuit-problem` | **shipped** | ngspice CLI + PySpice gate; RLC via netlist artifact |
| Network theorems, dividers | circuits | `check-numeric`, `derive-circuit` | **shipped** | eval gold divider-dc-01 |
| Signals & systems (LTI) | signals | `solve-signals-problem` | **shipped** | numeric path; Bode via control pack crossover |
| Classical control, Bode/step | control | `solve-control-problem`, `explain-control` | **shipped** | real matplotlib plots; UI engine panel |
| Control block diagrams | control | `control-diagram-to-model` | **shipped** | `compose-control-blocks` → python-control Bode/step; gold `block-feedback-01` |
| Power system analysis (LF) | power | `solve-power-problem`, `run-load-flow` | **shipped** | pandapower 3-bus demo + tables |
| Symmetrical / unsymmetrical faults | power | `simulate-power-fault` | **shipped** | LG/LL/LLG/3PH sequence; gold lg-01, ll-01 |
| Protection & switchgear (study) | power | `study-protection-setting` | **shipped** | CT ratio, OC pickup, optional distance zone; gold `protection-oc-01` |
| Electrical machines (equiv. circuit) | machines | `solve-machines-problem` | **shipped** | algebraic-check path |
| Power electronics converters | power_electronics | `solve-power-electronics-problem` | **shipped** | numeric coursework path |
| Measurements & instrumentation | measurements | `solve-measurements-problem` | **shipped** | numeric + explain |
| EM fields (UG analytic) | em | `solve-em-problem` | **shipped** | check-numeric / explain |
| Maths for EE (complex, ODE) | maths | `solve-maths-for-ee` | **shipped** | sympy/check path |
| Electric drives (UG intro) | machines | `solve-drives-problem` | **shipped** | OSS DC + IM slip steady-state; gold `dc-drive-speed-01`; Simulink plant optional leftover |
| Digital control intro | control | `solve-digital-control-problem` | **shipped** | discrete TF / ZOH sample, step + z-plane poles; gold `digital-pole-01` |
| Microprocessors lab | electronics | — | **blocker** | out of Arc kernel (no MCU flash/ISA simulator in scope) |
| Communication elective (PG-style) | — | — | **blocker** | PG-only per curriculum-map |
| Full Simulink drive block library | machines | `run-simulink-if-present` | **blocker** | optional MATLAB licence; OSS numeric path shipped above |

## Pass 2 fixes (2026-09-21)

1. Block diagram OSS compose + `control-diagram-to-model` workflow rewrite.  
2. `study-protection-setting` + protection engine + UI table panel.  
3. `solve-drives-problem` + drives engine (DC / IM slip).  
4. `solve-digital-control-problem` + digital pole/step plots.

## Residual blockers (honest)

- **MCU / microprocessor labs** — embedded toolchain out of scope.  
- **PG-only electives** — product bound.  
- **Licensed Simulink drive plant** — optional via Arc MATLAB path; not required for checked UG numbers.
