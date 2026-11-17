#!/usr/bin/env bash
# Turn the two Playwright recordings into the README GIFs (960 px wide, 12 fps).
set -euo pipefail
cd "$(dirname "$0")/../.."
OUT=docs/assets/readme
PAL="fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle"
HERO=$(ls -t build/readme-clips/raw-hero/*.webm | head -1)
RECT=$(ls -t build/readme-clips/raw-rect/*.webm | head -1)
ffmpeg -loglevel error -y -ss 1.6 -to 18.9 -i "$HERO" -vf "crop=1384:900:56:0,$PAL" "$OUT/hero-rlc.gif"
ffmpeg -loglevel error -y -ss 2.2 -to 21 -i "$RECT" -vf "crop=1384:720:56:50,$PAL" "$OUT/rectifier-sweep.gif"
ls -la "$OUT"/hero-rlc.gif "$OUT"/rectifier-sweep.gif
