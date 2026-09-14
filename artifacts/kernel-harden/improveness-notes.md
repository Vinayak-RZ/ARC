# Improveness tooling notes — applied to Arc

Sibling repo: `Vinayak-RZ/Improveness` (cloned to `/tmp/Improveness` for this run).

## Techniques we adopt (Option B)

1. **Frozen physics:** `eval_runner/score.py` and gold expect contracts are not edited by improver prompts. Scorer changes need ADR.
2. **Held-in / held-out:** `artifacts/kernel-harden/HELD_OUT_IDS.txt` (24 ids). I1/I2 makers must not train on those scenario ids.
3. **Grader ≠ improver:** improve log + patches reviewed by separate validate/checker; Unagent never auto-applies.
4. **Filesystem evidence plane:** corpus index, traces, reports on disk under `artifacts/kernel-harden/`.

## What we do *not* do

- Do not mount DeepSeek Harness / Cordis as Arc runtime (H5 reject; validate.sh already bans Cordis).
- Do not use public Terminal-Bench as fitness.

## I2 bullets from this pass

- Fix Unagent export: `unchecked` is not `error`.
- Keep labeled reason honest (I1).
- Document ABSTAIN as success of determinism advisor on a tool-shaped kernel.
