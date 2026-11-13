# Control Studio survey (Nov 2026)

Scope: open block-diagram editors and simulators suitable for Arc Control Studio. MATLAB/Simulink are proprietary; no MathWorks code is ported or referenced for implementation.

## Candidates

| Tool | License | Editor | Simulation / analysis | Notes |
| --- | --- | --- | --- | --- |
| [bdsim](https://github.com/petercorke/bdsim) (Peter Corke) | MIT | Python scripts + optional diagram UI | Continuous-time block evaluation | Strong teaching fit; diagram model is Python-first. |
| PathSim | MIT | Python API | Continuous, discrete, hybrid | Stiff solvers and events; no mainstream React canvas in-repo. |
| Scilab Xcos | GPL-2.0 / CeCILL | Desktop graphical | Hybrid, Modelica bridge | GPL copyleft is heavy for embedding in Arc pip package. |
| OpenModelica / OMEdit | OSMC-PL / AGPL | Desktop graphical | Acausal physics + control | Excellent for Modelica; overkill for UG linear control homework graphs. |
| Collimator (`pycollimator`) | MIT (library) | Cloud UI mostly proprietary | JAX differentiable sim | Useful API patterns; visual editor not OSS. |
| [python-control](https://github.com/python-control/python-control) `interconnect` | BSD-3 | Code-first | LTI compose, Bode, rlocus, margins | Already an Arc dependency; canonical verifier for goldens. |
| Simupy | BSD-2 | Python `BlockDiagram` | ODE time-stepping | Nice teaching blocks; overlaps bdsim/PathSim. |
| [@xyflow/react](https://github.com/xyflow/xyflow) | MIT | React canvas | N/A (wiring UI only) | Already vendored in `ui/package.json`. |
| Rete.js | MIT | Node graph UI | N/A | General node editor; less control-domain semantics. |
| tldraw | MIT (source) | Whiteboard | N/A | Great freeform; weak typed ports for EE blocks. |
| JointJS | Commercial / Rappid | Diagram SDK | N/A | License cost and bundle size argue against default Arc UI. |

## Recommendation

**Ship Arc Control Studio as:**

1. **Canonical model**: versioned JSON schema (`arc.control_studio.v1`) owned by Arc, persisted beside runs and studio sessions.
2. **Verifier / simulator**: **python-control** (BSD) for LTI reduction, time responses, and classical analysis plots rendered through the existing **Arc Visual Kit** (`render_control.py`, design tokens).
3. **Canvas**: **@xyflow/react** (MIT), already in the localhost UI; extend with control block types, palette, inspector, undo, and auto-layout consistent with Visual Kit tokens.
4. **Do not embed** GPL desktop stacks (Xcos, OMEdit) or proprietary Simulink paths as defaults.
5. **Optional future**: MIT PathSim or bdsim as an alternate time-domain backend behind the same JSON model if nonlinear or hybrid goldens demand it; keep python-control as the regression authority for linear UG items.

Attribution: bdsim (Corke, MIT), python-control (Murray et al., BSD), xyflow (MIT) cited in this document and in module docstrings where patterns are inspired.

## Human + agent collaboration

| Need | Choice |
| --- | --- |
| Shared live diagram | HTTP session store + polling (websocket optional later); MCP and CLI mutate the same JSON |
| Authorship | Append-only operation log with `author: human \| agent` and undo pointer |
| Explanations | Block-attached notes/comments in the diagram model |
| Verification | Algebraic loop detection, port wiring checks, Arc trap rules (summer sign, gain units), golden parity vs independent python-control |

## Out of scope for wave 1

- Full Modelica import
- Simulink `.slx` read/write
- Nonlinear operator blocks beyond saturation and simple PID anti-windup heuristics
