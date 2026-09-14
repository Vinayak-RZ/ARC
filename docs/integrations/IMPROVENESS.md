# Integration — Improveness × Arc

## Role

[Improveness](https://github.com/Vinayak-RZ/Improveness) is a **self-improving host-harness plugin** family. Arc does **not** mount it as runtime. We steal vocabulary and gates:

| Improveness idea | Arc mapping |
|------------------|-------------|
| Frozen physics | Don’t edit `eval_runner/score.py` without ADR |
| Self-Harness held-in/out | `artifacts/kernel-harden/HELD_OUT_IDS.txt` |
| Grader ≠ improver | validate/checker ≠ patch maker |
| Evidence plane | `runs/`, corpus index, improve log |
| Refuse public Terminal-Bench as fitness | Corpus is UG EE host trials |

## Notes from this run

See `artifacts/kernel-harden/improveness-notes.md`.

## Non-goals

- DeepSeek Harness / Cordis as Arc loop (H5 / validate refuse)
- I3: a corpus without an `expect` block is a log, not a trial; grader reads the scenario contract, not the improver's traces.
