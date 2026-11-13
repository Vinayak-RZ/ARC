#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
uv run ruff check .
uv run pytest -q
uv run python scripts/check_psa_evals.py
uv run python scripts/check_circuit_evals.py
uv run pytest -q tests/visual
uv run electrical-engineer eval --pack power
uv run python scripts/pass_k_traps.py
uv run python -c "from electrical_engineer.rlvr_env import ArcRlvrEnv, contract_json; print(contract_json())"
uv run python scripts/rlvr_dummy_rollout.py
uv run python scripts/build_benchmark_v01.py
uv run python scripts/grade_benchmark_v01.py
echo "validate_frontier: ok"
