# Simulink Agentic Toolkit — kernel mediation

## Purpose

How Arc talks to MathWorks **Simulink Agentic Toolkit** without attaching it to the homework host.

## Surface

Same Go `matlab-mcp-server` as MATLAB MCP. Extra tools load via `--extension-file=/path/to/simulink-agentic-toolkit/tools/tools.json` (repeatable; env `MW_MCP_SERVER_EXTENSION_FILE` is `:`/`;`-separated). MATLAB session needs `satk_initialize` (adds toolkit path, `shareMATLABSession`, validates). Requires MATLAB R2023a+ with Simulink. `model_test` wants Simulink Test.

Tools (vendor): `model_read`, `model_edit`, `model_check`, `model_test`, `model_scan`, … Schema dump is ~5–6k tokens **on top of** core MATLAB tools. Host attach recreates the ~10k dump ADR-0016 avoided.

Docs: https://github.com/matlab/simulink-agentic-toolkit — retrieved 2026-09-14.

## Families

| Family | Who sees tools | CI | Fit |
|--------|----------------|----|-----|
| **Kernel `--extension-file`** (chosen) | Arc subprocess only | Stub; no live Simulink | Matches ADR-0016 |
| Host peer toolkit MCP | Homework chat | Would fail CI honesty | Reject |
| Filtered proxy | Still the host | Extra operator | Reject |
| Docs-only this graph | Nobody | Trivial | Rejected by owner: introduce the toolkit |

## Kernel mapping

No new host MCP verb. New provider activity `run-simulink-if-present`. Do not invent a capability id. MATLAB-only plants stay `CD-SIMULINK-PLANT`. Missing `EE_SIMULINK_TOOLS_JSON` / missing binary → fail closed (`ok: false`, `unchecked: true`). Stub must not mint a checked plant number. `model_edit` is not a P0 happy path (read/check first).

`satk_initialize` is a **student-desktop MATLAB-session** step. CI never runs it. Never store MathWorks passwords.

Live licensed Simulink remains Later.

## Recommendation

**Kernel stdio client already in `matlab_mcp.py` grows `--extension-file` when the json path exists. Host never lists `model_*`. Product and CI work with zero Simulink.**
