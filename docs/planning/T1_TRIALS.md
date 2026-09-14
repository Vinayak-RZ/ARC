# T1 trials — student CLI/UI and host MCP

Recorded 2026-09-13 after [R1_BOOT.md](R1_BOOT.md). Live runs plus locked tests. Result column uses `pass` or `N/A`.

| # | Role | Scenario | Result | Evidence |
|---|------|----------|--------|----------|
| 1 | student CLI | Happy P0 circuits attachment `solve-circuit-problem` divider Vin=10 R1=R2=1k | pass | **PASS** checked `value=5.0`; R1 `e54q-20260913T083849Z`; gold `divider-dc-01` |
| 2 | student CLI/UI | Empty RAG + empty UI run list | pass | **PASS** `retrieve({book_id:no-such-book}).empty true`; UI sidebar “No runs yet” when list empty; `/api/runs` returns `{runs:[…]}` |
| 3 | student CLI | Invented capability id rejected | pass | **PASS** `bind("lookup_vout_guess")` and MCP `propose_composition` → `unknown id`; `waits: false` |
| 4 | regression | Unmatched no auto-spice; photo MCP `ui_url` | pass | **PASS** `unmatched-cosolver` blob has no `run-spice`; photo `simulate_attachment` `ui_url` `http://127.0.0.1:8765/` |
| 5 | auth | Product auth | N/A — no product auth | Local CLI/MCP; no login surface |
| 6 | FR9 | `solve-explain` does not mint checked | pass | **PASS** `test_fr9_no_mint`; R1 solve node `unchecked: true` while check-numeric is the checked verifier |
| 7 | two-band | Argument cannot flip `unchecked` | pass | **PASS** badge uses `obj.unchecked === true`; `/api/runs` serves `evidentiary` + `argument` separately (`test_two_band_payload`) |
| 8 | non-circuits | Signals complete path or `unchecked` | pass | **PASS** gold `eval/gold/signals/lti-path-01` token `unchecked`; no forced spice |
| 9 | student UI | Two-band on 127.0.0.1 | pass | **PASS** slots `run.evidentiary` `run.argument` `run.plan` `run.observation`; health `bind 127.0.0.1` |
| 10 | MCP | tools/list 5–7 including `propose_composition` | pass | **PASS** seven verbs in R1 MCP log; `test_mcp_aci` |
| 11 | UX empty | No crash, honest empty | pass | **PASS** workspace empty copy; RAG empty visible; 404 run `state: failed` |
| 12 | UX error | Fail-closed visible | pass | **PASS** MCP `isError` + `ui_url`; UI `.failed` text uses `--ee-semantic-down` |
| 13 | UX a11y | Keyboard / WCAG | pass | **PASS** skip-link, 2px focus, `alt="Arc"`, `aria-live`, DESIGN-coinbase `#0052ff` |
| 14 | photo | waiting-human / confirm still no sim | pass | **PASS** `confirmed.json` `simulate: false`; photo YAML has no `run-spice` |
| 15 | badge | `unchecked` exact token in UI or CLI JSON | pass | **PASS** pill `unchecked`; CLI simulate-circuit `"token": "unchecked"` |

MCP-as-agent: #3, #4, #10. Student CLI/UI: the rest. Auth is N/A.

## Kernel queue (2026-09-14 skills/MATLAB graph)

| # | Role | Scenario | Result | Evidence |
|---|------|----------|--------|----------|
| K1 | kernel | Stub MATLAB MCP returns ok evidentiary | pass | **PASS** fake stdio `evaluate_matlab_code` → `ans = 42`; `unchecked: false` |
| K2 | kernel | Missing MATLAB fail-closed | pass | **PASS** `_missing("matlab")` `unchecked: true` |
| K3 | kernel | MATLAB stub error / no code | pass | **PASS** no `code`/`script_path` → still missing, never a fake pass |
| K4 | regression | SPICE missing still unchecked | pass | **PASS** `ngspice/PySpice not available` |
| K5 | MCP | tools/list has no MATLAB tools | pass | **PASS** seven Arc verbs only |
| K6 | retrieve | Scaffold empty is visible | pass | **PASS** `retrieve({book_id:no-such-book}).empty true` |

