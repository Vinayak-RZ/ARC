# Audit — Kernel harden canes (Wave 8)

Self-audit of the graph that just shipped on `cursor/ee-kernel-harden-trace-8db3`.
The job was not to add another layer of hardness. It was to look at what the
canes actually produced, keep what held, and fix what the corpus could not fail.

## What the canes did

| Wave | Cane | What actually shipped | Held? |
|------|------|------------------------|-------|
| 0 | 22 loop plans + plan-harden | Plans exist; some promised files (`export_unagent.py`) were missing until I3 | Partial |
| 1 | JSONL traces + 120 scenarios + UI excerpts | `TraceWriter` + UI excerpts real; scenarios were placeholder prompts | Partial |
| 2 | validate + boot | `validate.sh` green | Yes |
| 3 | 120 host trials | 120 traces on disk | Yes, ungraded |
| 4 | Critique + I1 | `labeled` vs `unmatched` is a real honesty fix | Yes |
| 5 | Unagent + Improveness + I2 | Unagent ABSTAIN is the right answer for a tool kernel; I2 export was still poisoned by `bool(ok)` | Partial |
| 6–7 | Harden + case study | Docs-out exists; `PROGRESS.md` had been overwritten | Partial |

## What the first corpus could not tell us

The Wave 3 index reported `unmatched: 96` because `_unchecked_reason` fell through.
I1 fixed that lie. The next lie was quieter: after I1 almost everything became
`labeled`, including runs where the host can act.

Probe of one scenario per recipe (post-I1, pre-I3):

| Recipe | Reason then | Reason now (I3) |
|--------|-------------|-----------------|
| `solve-circuit-problem` (numeric) | None (verified) | None |
| `explain-*` (no optional tool) | labeled | labeled |
| `explain-control`, `solve-control-problem` | labeled | **no-provider** |
| `simulate-circuit` | no-provider | no-provider |
| `simulate-after-confirm`, `photo-to-netlist`, `control-diagram-to-model` | labeled / gate-closed | **gate-closed** |
| `unmatched-cosolver` | unmatched | unmatched |

`labeled` is honest only when the kernel answered and said the answer is
unverified. It is not honest when the next step is "install python-control"
or "confirm this draft".

## Graded corpus (I3)

120/120 PASS on this machine. Expectations come from the recipe YAML, not from
whatever the kernel printed.

| `unchecked_reason` | Wave 3 (pre-I1) | After I1 (index stale) | After I3 (graded) |
|--------------------|-----------------|------------------------|-------------------|
| unmatched | 96 | 8 (recipe-true) | 8 |
| labeled | 0 | majority | 68 residual |
| no-provider | 6 | 6 | 18 |
| gate-closed | 8 | 8 | 16 |
| None (verified) | 10 | 10 | 10 |

Injection pack still cannot flip `unchecked`. The payloads now actually say so
(`disable_gates`, `mark_checked`) instead of `"prompt": "ug ee scenario"`.

## Advisor export (I2 + I3)

`to_unagent_events` already refused to map `unchecked` → `error`. That was not
enough: `bool(out.get("ok"))` turned a missing `ok` into `False`, so explain /
label / retrieve nodes looked like tool crashes. Unagent then ABSTAINed with
`failure_rate=1.00`. The ABSTAIN was still the right class of answer (do not
flip tools to LLMs); the rate was a measurement bug.

Reproduce the export:

```bash
uv run python scripts/kernel_harden/export_unagent.py
```

`unagent_events_v2.json` was byte-identical to `unagent_events.json` and is gone.

## Repo hygiene the canes broke

- `PROGRESS.md` had been replaced with a wave table. Restored from `main` and
  appended a kernel-harden section.
- `.gitignore` globbed all `*.jsonl` under `artifacts/kernel-harden/`, so the
  committed index needed `git add -f`. Now only `raw/` is ignored.
- `IMPLEMENTATION_PLAN.md` is a live pointer; the Simulink plan is archived.
  That is intended for this graph.

## What we did not add

- OpenTelemetry / Langfuse (Gate 0).
- A second agent loop (H5).
- Fake SPICE / python-control numbers.
- Auto-apply of Unagent refactors.

## Remaining honest holes

- `labeled` still dominates explain/derive/review/maths/signals. That is the
  product: those recipes do not mint a checked scalar. Deeper fixtures would
  change the *text*, not the reason.
- Optional providers (`PySpice`, `control`, `pandapower`) stay fail-closed.
- Figure ingest waits on a human confirm; `gate-closed` is the contract.
