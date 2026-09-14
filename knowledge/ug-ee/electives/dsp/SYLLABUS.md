# Digital signal processing — syllabus union

Bound: `docs/curriculum-map.md` (IITR, NITT, AICTE-family, MIT/Berkeley, GATE overlay). Signals-and-systems DFT/sampling is assumed; this pack is the DSP *elective* layer.

This pack is UG digital signal processing: DFT/FFT and introductory FIR/IIR design, then multirate (decimation/interpolation) and finite-wordlength effects. Depth is coursework (assignment, lab numerical, exam-style), not wavelet research, adaptive filters as a thesis, or MATLAB-only toolboxes as the checked answer.

## Units

- `01-dft-fft-filters` — DFT/FFT, FIR/IIR design intro
- `02-multirate-finite-wordlength` — Decimation, quantization effects

## Outcomes

After this pack a UG EEE student can evaluate a small DFT by hand; count radix-2 multiplies; pad for linear convolution via circular DFT; design a short linear-phase FIR by the window method; bilinear-map a first-order analog prototype; choose anti-alias cutoffs for integer decimation; and estimate SQNR and roundoff variance.

## Notes

- Capability ids stay in `docs/ARCHITECTURE.md` §0; this pack does not invent extra EE capabilities.
- Worked items in `questions.md` are original numbers, not GATE or institute papers.
- No `oer/` copies. [Smith DSP Guide](https://www.dspguide.com) (ledger **K10**) and MIT OCW are **link only** in unit `sources.md`.
