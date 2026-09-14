# Unagent recommend — Arc kernel-harden corpus

**Tool:** `superdeterminism` (Unagent) via `--adapter custom`  
**Input:** `artifacts/kernel-harden/unagent_events.json` (40 runs → 388 events)  
**Outputs:** `unagent-report.json`, stdout narrative

## Headline

Unagent **ABSTAINed** on FlipToDet / FlipToNondet for all reconstructed nodes (`check`, `explain`, `label`, `retrieve`, `solve`, `spice`, …). No auto-apply.

## Interpretation for Arc (domain kernel)

- Arc nodes are already **deterministic tools** (SPICE, numeric check, label). Unagent correctly refuses to flip them to LLM steps.
- High observational “failure_rate” in the first export was an adapter artifact: mapping `unchecked` → `error=true`. Honest `unchecked` / `labeled` is not a tool crash.
- **I2 action:** export mapper treats `unchecked` as a successful fail-closed outcome unless `ok is False` for a hard node error.

## Canary

simulation ≠ production; recommendations are design-time only.
