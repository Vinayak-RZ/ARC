# Failure report — Kernel harden corpus

Linked to `artifacts/kernel-harden/CORPUS_INDEX.jsonl`.
Audit: [`AUDIT_KERNEL_HARDEN.md`](AUDIT_KERNEL_HARDEN.md).

## Summary

- **completed:** 120
- **with trace_path:** 120
- **grade:** 120 pass / 0 fail / 0 skip (this machine)
- **unchecked:** 110
- **checked:** 10

## Classes

### F1 — `unchecked_reason` fallback mislabel (`unmatched`) — I1

**Before:** `_unchecked_reason` returned `unmatched` whenever no detector fired.
**Evidence:** Wave 3 index, 96 rows.
**Fix (I1):** residual became `labeled`; `unmatched` reserved for unmatched recipes.

### F2 — `no-provider` on simulate-circuit

**Evidence:** six `simulate-circuit` rows (capability-bound `lumped-circuit-sim`).
**After:** keep fail-closed; document as honest hole unless ngspice bind present.

### F3 — `gate-closed` on simulate-after-confirm

**Evidence:** eight rows in Wave 3.
**After I3:** also `photo-to-netlist` and `control-diagram-to-model` (16 rows).
Treat as pass when reason matches expect.

### F4 — Checked voltage divider

**Evidence:** ten `solve-circuit-problem` rows with a numeric `expected`.
**After:** still the only verified pack; injection variants of the same recipe stay `labeled`.

### F5 — Intentional unmatched-cosolver

**Evidence:** eight unmatched rows (four pack + four injection).
**After:** reason must stay `unmatched`. Injection cannot flip it.

### F6 — `labeled` masking a missing provider — I3

**Before:** `_missing()` did not stamp `CD-NO-PROVIDER`, so recipes that name
`run-python-control` directly (`solve-control-problem`, `explain-control`)
fell through to `labeled`.
**Evidence:** post-I1 probe; 12 control-explain/solve rows.
**Fix:** stamp `cannot_do` in `_missing`; 18 `no-provider` rows after I3.

### F7 — `labeled` masking awaiting-confirm — I3

**Before:** only `error in {unconfirmed, gate}` counted as `gate-closed`.
Figure ingest writes `confirmed: false` and a `draft.cir` instead.
**Evidence:** `photo-to-netlist`, `control-diagram-to-model` post-I1 probe.
**Fix:** `confirmed is False` → `gate-closed`.

### F8 — `bool(ok)` poisoning Unagent — I3

**Before:** `ok=bool(out.get("ok"))` turned a missing field into `False`.
**Evidence:** `unagent-report.md` `failure_rate=1.00` on explain/label/retrieve.
**Fix:** tri-state `_node_ok`; export `error` only when `ok is False`.

### F9 — Ungraded corpus — I3

**Before:** 120 rows with traces, zero expectations, placeholder prompts.
**Fix:** `expect` block + `trial_driver` grade. `scripts/kernel_harden/annotate_scenarios.py --check`.

## Open

- Explain/derive/review remain `labeled` by design until a verifier exists.
- Held-out ids reserved in `artifacts/kernel-harden/HELD_OUT_IDS.txt` (24).
