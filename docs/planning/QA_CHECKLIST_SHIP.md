# QA checklist — ship graph W5

| # | Check | Command / evidence | Pass |
|---|-------|-------------------|------|
| 1 | Unit+integration tests | `uv run pytest -q` | pass |
| 2 | Validate orchestrator | `./scripts/validate.sh` | pass |
| 3 | RLC CLI demo | `uv run electrical-engineer run simulate-circuit` with `problem.json` cir fixture | pass |
| 4 | Control CLI demo | `uv run electrical-engineer run solve-control-problem` | pass |
| 5 | Fault CLI demo | `uv run electrical-engineer run simulate-power-fault` + LG problem | pass |
| 6 | UI build | `npm --prefix ui run build` | pass |
| 7 | Artifact API | `pytest tests/integration/test_ui_artifacts.py` | pass |
| 8 | Power faults | `pytest tests/integration/test_power_faults.py` | pass |
| 9 | Scenario bank | `pytest tests/unit/test_scenario_bank.py` | pass |

Self-check screenshots (not README marketing): `docs/planning/qa-shots/` optional; engine verification uses run artifacts under `runs/`.
