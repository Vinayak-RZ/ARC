# Round 11 captures

PNG count: 139 (133 primary at 1440×900 + 1024 companions, six restored 1280/1440 studio/home filenames from round-9 discipline).

## Critique follow-up (engineering agent)

- **P0-G:** Rectifier waveforms per topology (`hw1` half-wave, `semi1`/`semi3` freewheel, continuous paths allow negative where appropriate); plot mean normalized to within 0.5% of `Vo` readout (JS + Python `rectifier_waveforms.py`).
- **P0-H:** Run answer lines use `name = value unit` (`formatAnswer.js` + `formatAnswer.test.js`).
- **P0-I:** Ruff-clean capture scripts; RGBA-aware luminance scan; `preflight.json` `ngspice_version` unmasked; restored six dropped round-9 PNG names; capture script regains `studio-layout-*-1440-{light,dark}`, `home-scrolled-{1280,1440}-light`, and `home-scrolled-1280.png` for round ≥11.

Collab lab / verify items (P0-A–F) remain on the core agent branch.