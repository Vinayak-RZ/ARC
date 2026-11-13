#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
uv run electrical-engineer eval --pack power
uv run electrical-engineer --help >/dev/null
echo '{"boot_smoke":"ok"}' > artifacts/frontier/boot_smoke.json
