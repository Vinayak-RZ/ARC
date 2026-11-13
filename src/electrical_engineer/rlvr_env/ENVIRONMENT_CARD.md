# Arc RLVR environment card (v0.1)

## Summary

Importable Gym-style environment for rule-based verifiable rewards over the Arc trap catalog (T1 to T10). External researchers can train routers or policies against the same deterministic engines and tolerances Arc uses in CI. This package does not ship weight training or hosted RL loops.

## Interface

| Method | Behavior |
|--------|----------|
| `reset(seed=...)` | Returns `trap_id`, natural-language `prompt`, and backing `engine` key. |
| `step(action)` | `action` is `{"trap_id", "submission": {...}}`. Returns reward `0.0` or `1.0`, `terminated=True`. |

Rewards come from `electrical_engineer.rlvr_env.rewards.grade_trap`, which reuses PSA and trap regression numerics (SMIB, AGC, ED, diagram signs, integrator policy, defaults).

## Install

```bash
uv sync --extra engines
python -c "from electrical_engineer.rlvr_env import ArcRlvrEnv; print(ArcRlvrEnv())"
```

## Manifest

Version `0.1`, ten traps. See `manifest.json` in this directory.

## Example rollout

```bash
uv run python scripts/rlvr_dummy_rollout.py
```

Runs an oracle policy through all traps end to end and prints JSON including the contract block.

## Provenance

- Trap prompts: `proofs/ablation/trap_prompts.yaml` (T1, T2, T6 plus extended traps in ablation tests).
- Trap index: `artifacts/frontier/trap_suite_index.json`.
- No held-out live A/B sheets, exam PDFs, or sealed `REFERENCE.json` content.

## Licence

Same as the Arc repository (Apache-2.0). Lab numerics are license-clean reconstructions from `artifacts/eec301-lab-goldens/`.
