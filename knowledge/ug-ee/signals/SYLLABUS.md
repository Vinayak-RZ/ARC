# Signals and systems — syllabus union

Bound: docs/curriculum-map.md (IITR, NITT, AICTE-family, MIT/Berkeley, GATE overlay).

Pack path: `ug-ee/signals`. Twelve units. Original notes and worked questions; MIT OCW / NPTEL are link-only in each unit `sources.md`.

## Outcomes

After this pack a UG EE student can classify waveforms; test LTI properties; convolve; expand periodic signals; use CTFT and Parseval; invert Laplace with an ROC; sample and reconstruct with aliasing arithmetic; invert Z-transforms; relate DTFT/DFS/DFT; specify ideal filters and group delay; apply BIBO and causality tests; and shift spectra with AM / complex exponential modulation.

## Units

- `01-signal-classifications` — Continuous/discrete, energy/power, even/odd, periodic. Impulse and step, periodicity tests for CT and DT sinusoids, \(E_x\) and \(P_x\).
- `02-lti-systems-properties` — Linearity, time-invariance, memory, invertibility. Eigenfunctions \(e^{st}\) and \(z^n\); when \(h=\mathcal{S}\{\delta\}\) characterizes a system.
- `03-convolution` — Continuous and discrete convolution. Graphical breakpoints, support addition, circular versus linear convolution.
- `04-fourier-series` — CTFS/DTFS and properties. Hermitian coefficients, Parseval power, harmonic filtering by \(H(jk\omega_0)\).
- `05-fourier-transform` — CTFT and properties, Parseval. Duality, convolution/multiplication theorems, standard pairs including distributions.
- `06-laplace-transform-signals` — ROC, unilateral Laplace, system functions. Causal versus anticausal pairs, initial/final value hypotheses.
- `07-sampling-reconstruction` — Nyquist, aliasing, reconstruction. Impulse train copies, principal aliases, sinc interpolation versus ZOH.
- `08-z-transform` — ROC, inverse Z, discrete LTI. Annular ROC, partial fractions, recurrences, unit-circle versus DTFT.
- `09-dft-dfs-dtft` — DTFT, DFS, DFT relations. Frequency sampling, time aliasing, circular convolution and padding.
- `10-filters-as-systems` — Ideal filters, distortion, group delay. Distortionless transmission, phase versus group delay, linear-phase FIR.
- `11-bibo-stability-causality` — BIBO, causality, ROC implications. \(\|h\|_1\) test, pole locations for causal stability, nonlinear BIBO counterexamples.
- `12-modulation-intro` — AM/complex exponential modulation for signals courses. DSB-SC spectra, coherent demodulation, envelope AM, Hilbert/SSB sketch.

## Sequence

Units 01–03 are the time-domain core. 04–06 are CT frequency-domain tools. 07 connects CT to DT. 08–09 are discrete transforms. 10–12 apply the tools to filters, stability, and modulation.
