#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="${HOME}/.local/bin:${PATH}"
uv run ruff check .
uv run pytest -q
uv run python -c "from electrical_engineer import bind; bind('algebraic-check')"
uv run electrical-engineer eval --pack circuits
uv run electrical-engineer eval --pack rag-retrieval
uv run electrical-engineer eval --pack explain
uv run electrical-engineer eval --pack unmatched
uv run electrical-engineer eval --pack signals
# Bind must never be 0.0.0.0 in product code.
if grep -R --include='*.py' --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=dist -n '0.0.0.0' src ui 2>/dev/null | grep -v test; then
  echo "refusing 0.0.0.0 bind" >&2
  exit 1
fi
if grep -R --exclude-dir=node_modules --exclude-dir=dist -nE '@deepseek-ai|from cordis|require\(.cordis' src ui pyproject.toml 2>/dev/null | grep -v test; then
  echo "refusing Cordis/DSH runtime" >&2
  exit 1
fi
if find ui -iname '*coinbase*' 2>/dev/null | grep -q .; then
  echo "refusing Coinbase font/wordmark files" >&2
  exit 1
fi
echo "validate.sh OK"
