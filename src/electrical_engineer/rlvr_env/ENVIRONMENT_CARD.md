# Arc RLVR environment card (v0.1)

## Interface

`reset(seed, trap_id=...)` returns:

- `question`: self-contained prompt (no repo paths)
- `givens`: numeric parameters and units for this episode
- `answer_schema`: named fields, units, tolerances
- `held_out_eval`: true when `seed` is in 9000..9999

`step({"submission": {...}})` grades **numeric answers only** via Arc engines. Self-reported flags and copying givens score 0.

## Seeds

Training: `0..8999`. Held-out evaluation: `9000..9999` (see `seeds.json`).

## Example

```bash
uv run python scripts/rlvr_dummy_rollout.py
uv run python -c "from electrical_engineer.rlvr_env import ArcRlvrEnv; e=ArcRlvrEnv(); print(e.reset(seed=17, trap_id='T1'))"
```
