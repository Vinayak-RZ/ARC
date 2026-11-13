# Node plan: B9: tutoring mode

| Field | Value |
|-------|-------|
| **Node id** | `B9` |
| **Job** | Host Socratic policy + Arc numeric oracle gold for explain genre |
| **Wave** | 4 (P1) |
| **Depends on (data)** | Gate 0 Q6 |
| **Write paths** | `skills/_cross/**`, `eval/gold/explain/**`, `docs/**` |
| **Model** | inherit |

## Objective

Certified tutoring = correct numbers + Socratic host, not model fine-tune (report #02 AITEE pattern).

## Contract

**Output:** `{ "tutoring_pilot": "deferred" | "ok" }`

## Commits

Optional 2 commits if P1 approved.

## Non-goals

SocraticLM fine-tune in-repo.
