# IITR Y1–Y3 gap matrix (EE core)

**Source:** IITR NEP PCC EEC-* 2023–24 programme page + `docs/curriculum-map.md` union.  
**Date:** 2026-09-21  
**Rule:** Each row is **shipped** (recipe/skill/UI path), **partial**, or **blocker** with reason.

| IITR-aligned topic | Pack | Capability / recipe | Status | Notes |
|--------------------|------|---------------------|--------|-------|
| Circuit theory, DC/AC, transients | circuits | `simulate-circuit`, `solve-circuit-problem` | **shipped** | ngspice CLI + PySpice gate; RLC via netlist artifact |
| Network theorems, dividers | circuits | `check-numeric`, `derive-circuit` | **shipped** | eval gold divider-dc-01 |
| Signals & systems (LTI) | signals | `solve-signals-problem` | **shipped** | numeric path; Bode via control pack crossover |
| Classical control, Bode/step | control | `solve-control-problem`, `explain-control` | **shipped** | real matplotlib plots; UI engine panel |
| Control block diagrams | control | `control-diagram-to-model` | **partial** | graph ingest; no Simulink licence required |
| Power system analysis (LF) | power | `solve-power-problem`, `run-load-flow` | **shipped** | pandapower 3-bus demo + tables |
| Symmetrical / unsymmetrical faults | power | `simulate-power-fault` | **shipped** | LG/LL/LLG/3PH sequence; gold lg-01, ll-01 |
| Protection & switchgear (study) | power | `explain-power`, retrieve | **partial** | explain + RAG; no relay vendor EMS (`CD-POWER-EMS`) |
| Electrical machines (equiv. circuit) | machines | `solve-machines-problem` | **shipped** | algebraic-check path |
| Power electronics converters | power_electronics | `solve-power-electronics-problem` | **shipped** | numeric coursework path |
| Measurements & instrumentation | measurements | `solve-measurements-problem` | **shipped** | numeric + explain |
| EM fields (UG analytic) | em | `solve-em-problem` | **shipped** | check-numeric / explain |
| Maths for EE (complex, ODE) | maths | `solve-maths-for-ee` | **shipped** | sympy/check path |
| Electric drives (UG intro) | machines / PE | cross-pack explain | **partial** | **blocker:** no dedicated drives Simulink plant without licence; OSS torque-speed via numeric only |
| Digital control intro | control | explain + `unchecked` | **partial** | z-transform explain; no dedicated z-domain solver this pass |
| Microprocessors lab | electronics | — | **blocker** | out of Arc kernel (no MCU flash/ISA simulator in scope) |
| Communication elective (PG-style) | — | — | **blocker** | PG-only per curriculum-map |

## Fixes applied this ship

1. Real engines (W1) for circuits, control, power.  
2. `simulate-power-fault` recipe + sequence backend for LG/LL/LLG/3PH.  
3. UI engine panels for control plots and power tables (W2).  
4. Power skill pack documents fault recipe (`skills/power/SKILL.md`).

## Remaining honest blockers

- **Drives/Simulink plant:** requires optional MATLAB/Simulink or future OSS drive block library.  
- **MCU labs:** need separate embedded toolchain, not co-solver scope.  
- **PG electives:** explicitly out of product bound.
