#!/usr/bin/env bash
# Mutation testing for verify path, netlist compiler, and IDMT solver (independent TE).
set -euo pipefail
cd "$(dirname "$0")/../.."
uv sync --extra dev --extra engines --extra control >/dev/null
export MUTMUT_QUIET=1
ART="/opt/cursor/artifacts/mutmut-report.txt"
rm -f .mutmut-cache
uv run mutmut run >>"$ART" 2>&1 || true
uv run mutmut results >>"$ART" 2>&1 || true
echo "Wrote $ART"