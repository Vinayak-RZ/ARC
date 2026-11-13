#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
uv run ruff check .
uv run pytest -q
uv run python scripts/check_psa_evals.py
uv run pytest -q tests/visual
uv run electrical-engineer eval --pack power
uv run python scripts/pass_k_traps.py
echo "validate_frontier: ok"
