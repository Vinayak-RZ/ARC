#!/usr/bin/env bash
# C1: keep trial PNGs under ~400 KiB width cap for git hygiene.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/docs/media/trials"
if ! command -v convert >/dev/null 2>&1; then
  echo "trim_trials_media: imagemagick not installed; skip"
  exit 0
fi
for f in "$DIR"/*.png; do
  [[ -f "$f" ]] || continue
  convert "$f" -resize '1200x1200>' -strip "$f"
done
echo "trim_trials_media: ok"
