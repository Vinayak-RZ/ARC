# Failure report — Kernel harden corpus

Linked to `artifacts/kernel-harden/CORPUS_INDEX.jsonl`.

## Summary

- **completed:** 120  
- **with trace_path:** 120  
- **unchecked:** 110  
- **checked:** 10  

## Classes

### F1 — `unchecked_reason` fallback mislabel (`unmatched`)

**Before:** `_unchecked_reason` returned `unmatched` whenever no detector fired.  
**Evidence:** explain/control/signals/etc. rows with `recipe_id` not containing `unmatched` yet reason=`unmatched`.  
**run_id samples:** see index filter `unchecked_reason==unmatched` excluding recipe `unmatched-cosolver`.  
**Fix (I1):** add reason `labeled` when label path produced unchecked; update ARCHITECTURE enum.

### F2 — `no-provider` on simulate-circuit

**Evidence:** six `simulate-circuit` rows.  
**After:** keep fail-closed; document as honest hole unless ngspice bind present. Optional scenario skip when provider absent — not a silent number.

### F3 — `gate-closed` on simulate-after-confirm

**Evidence:** eight rows.  
**After:** expected without `confirmed.json`; host trials should confirm or expect gate-closed. Treat as pass when reason matches expect.

### F4 — Checked voltage divider

**Evidence:** ten `solve-circuit-problem` rows with divider problem.  
**After:** regression gold remains authority.

### F5 — Intentional unmatched-cosolver

**Evidence:** eight unmatched pack rows.  
**After:** reason must stay `unmatched`.

## Open

- Deeper pack problem fixtures (P1 / later).
- Held-out ids reserved in `artifacts/kernel-harden/HELD_OUT_IDS.txt` (24).
