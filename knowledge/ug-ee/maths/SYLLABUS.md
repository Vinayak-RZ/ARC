# Mathematics for EE — syllabus union

Bound: `docs/curriculum-map.md` (IITR, NITT, AICTE-family, MIT/Berkeley, GATE overlay). This pack is **maths as used in UG EE**, not a mathematics-major analysis sequence.

Engineering mathematics in the union typically appears as first-year ODE/linear algebra/calculus plus later transform methods inside circuits, signals, EM, control, and measurements. GATE EE overlays the same objects (complex numbers, Laplace, Fourier, Z, probability, numerical methods) as tools, not as a separate research syllabus.

## Learning outcomes (pack)

- Use complex arithmetic, Euler, and polar form as the algebra of phasors and impedances.
- Solve constant-coefficient linear ODEs and first-order linear state systems with circuit/control initial conditions.
- Transform and invert unilateral Laplace with a working table, theorems, and legality of the final-value theorem.
- Expand periodic waves in Fourier series and transform energy signals; apply Parseval in the correct (energy vs power) form.
- Compute eigenvalues, quadratic energy forms, and small least-squares solves used in networks and state space.
- Evaluate grad/div/curl and apply Gauss/Stokes in the coordinate system matching an EM boundary.
- Compute expectation, variance, and Gaussian tails for additive noise models.
- Apply bisection/Newton, trapezoid/Simpson, and pivoted elimination at UG scale, with residual checks.
- Invert Z-transforms with an ROC, and test discrete causal stability via the unit disk.
- Invert rational transforms by partial fractions and residues, including repeated and complex poles.

## Units

- `01-complex-numbers-phasors-math` — Complex arithmetic and Euler. Rectangular/polar/exponential form, conjugate, De Moivre, roots, \(j\) convention, three-phase operator \(a\), RMS vs peak phasors, complex power \(S=VI^*\).
- `02-ode-linear-systems` — Linear ODEs and constant-coefficient systems. Characteristic polynomial, damping classes, undetermined coefficients, state matrix exponential, RLC natural/forced split, resonance secular term.
- `03-laplace-transforms` — Laplace tables, theorems, inverse. Unilateral \(0^-\) definition, differentiation/shift/convolution, initial- and final-value hypotheses, partial-fraction inversion, delay \(e^{-sT}\).
- `04-fourier-series-transform-math` — Fourier analysis as maths. Complex FS coefficients, \(c_{\pm 1}=A/2\), CTFT pair and theorems, rect/sinc, distributional tones, Parseval, Gibbs as truncation.
- `05-linear-algebra-ee` — Matrices, eigenvalues, quadratic forms. Rank and inversion, eigenstructure, SPD energy matrices, normal equations, SVD/condition number at UG level, similarity vs congruence.
- `06-vector-calculus` — grad, div, curl, integral theorems. Cartesian/cylindrical/spherical operators, Gauss and Stokes, conservative tests, coaxial Laplace \(\ln\rho\), orientation of \(d\mathbf{S}\).
- `07-probability-random-variables` — RV, expectation, Gaussian noise intro. pmf/pdf/cdf, linearity of expectation, uncorrelated vs independent, \(\mathcal{N}\) and \(Q\)-function, uniform quantisation, binomial packets, adding noise *variances*.
- `08-numerical-methods-ee` — Root finding, integration, linear solves. Bisection and Newton, trapezoid/Simpson, residuals and \(\kappa\), pivoting, stiff Euler warning, digit-count vs iteration count.
- `09-z-transform-math` — Z as a transform pair. Annular ROC, causal geometric pair, LCCDE algebra, unit-disk stability, FVT at \(z\to 1\), \(z=e^{sT}\) vs bilinear geometry.
- `10-partial-fractions-residues` — Partial fractions and residues. Cover-up, repeated poles, real quadratics, Bromwich/residue inversion, \(X(z)/z\) ritual, conjugate residues.

## Deliberately out of this pack

- Circuit topology and device stamps (circuits pack).
- Sampling/DFT as a signals numerical object (signals / DSP elective).
- Maxwell physics beyond the operators (em pack).
- Load-flow Newton as a power-system algorithm (power pack); only the shared scalar/vector Newton idea lives here.
- Pure-math extras: measure-theoretic probability, real analysis, algebraic topology, special-function catalogues beyond Bessel/Legendre *named* in EM.

## Sources policy

Original handbook notes and original worked questions in each unit folder. Link OER in `sources.md`. Do not copy NC (MIT OCW, NPTEL dumps) or commercial textbooks. SPDX copies, if added later, belong in unit `oer/`.
