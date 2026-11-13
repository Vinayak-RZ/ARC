#!/usr/bin/env bash
# Fail if shipped docs advertise the wrong recipe count vs catalog.py.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
COUNT="$(uv run python -c "from electrical_engineer.catalog import list_workflow_ids; print(len(list_workflow_ids()))")"
fail=0
check_file() {
  local f="$1"
  if grep -qE '\b27\b (named )?lab recipes' "$f" 2>/dev/null; then
    echo "drift: $f still says 27 recipes (catalog has $COUNT)"
    fail=1
  fi
  if grep -qE '\b27 recipes' "$f" 2>/dev/null; then
    echo "drift: $f still says 27 recipes (catalog has $COUNT)"
    fail=1
  fi
}
check_file README.md
check_file hosts/agents/INDEX.md
if ! grep -q "$COUNT" README.md 2>/dev/null; then
  echo "drift: README.md should mention $COUNT named lab recipes"
  fail=1
fi
exit "$fail"
