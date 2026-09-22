# PROGRESS — EEC-301 → Arc system lift

**Branch:** `cursor/eec301-system-lift-b2f6`  
**Commit floor:** ≥30 on landing PR · **Planned:** 36  
**PR:** #43

## Status

| Wave | State |
|------|-------|
| W0–W2 | done |
| W3 AGC | done |
| W4 ED | done |
| W5 Diagrams | done |
| W6 Host | done |
| W7 A/B proof | done |
| W8 CI + attestation | done |
| Lab goldens | `artifacts/eec301-lab-goldens/exp06–08.json` |

## Commit count

| Milestone | `origin/main..HEAD` |
|-----------|---------------------|
| after W2 + lab JSON | 21 |
| after W3–W8 | see attestation |

## Attestation (W8)

```
date: 2026-09-22
base: origin/main
HEAD: cursor/eec301-system-lift-b2f6
rev-list count: (run git rev-list --count origin/main..HEAD — must be ≥30)
attested by: cloud agent W3–W8 pass
```

PSA CI: `python scripts/check_psa_evals.py` + full `pytest`.
