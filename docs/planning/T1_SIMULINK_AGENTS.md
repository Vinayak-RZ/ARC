# T1 trials — Simulink + host-agent catalog

Recorded 2026-09-14. No live MATLAB. Score is disk + kernel fail-closed, not a solved `.slx`.

| Trial | Result |
|-------|--------|
| Happy install | `hosts install --into /tmp/ee-hw-sim --host all` → 12×3 files; `ee-simulink` present |
| Empty toolkit | `EE_SIMULINK_TOOLS_JSON` unset → `run-simulink-if-present` `CD-SIMULINK-PLANT` |
| Error / stub | stub `model_read` returns `isError`; kernel stays `unchecked` (pytest) |
| Regression | host `tools/list` has no MATLAB or `model_*` names |
| Product SDLC | `.cursor/agents/ee-*.md` still absent in this repo |

Host-harness spawn of `ee-circuits` as a live Cursor Task is not claimed on this Cloud VM (stdio MCP + run dir would miss `/in-cloud` children).
