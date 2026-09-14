# Numerical methods for EE

Undergraduate electrical engineering uses numerical methods whenever a closed form is unavailable or clumsy: a nonlinear diode equation, a definite integral for rms of a tabulated waveform, a nodal system too large for hand inversion, or a characteristic polynomial’s roots. This unit is the core algorithms at UG level: bracketing and Newton for scalars, numerical quadrature, and linear solves (Gaussian elimination, and the idea of iterative methods). It is not a course in finite elements or stiff ODE packages, though the same residual-and-Jacobian thinking appears in Newton–Raphson load flow in the power pack.

Floating-point reality belongs in the method: double precision has about 16 decimal digits; subtracting nearly equal numbers loses them; a condition number of \(10^8\) on a \(2\times 2\) can already eat half the digits of a 7-digit calculator. Algorithms are judged by stability and cost, not only by the textbook error formula on infinite-precision reals.

## Concepts

A nonlinear scalar equation \(f(x)=0\) is the model of a diode-resistor circuit’s KVL, of a transcendental intercept in a magnetic-circuit B-H curve, or of a unity-gain frequency defined implicitly. A bracketing method (bisection) needs \(f(a)f(b)<0\) and continuity; it halves the interval and cannot lose the root. Convergence is linear: error \(\sim 1/2^n\). Newton’s method \(x_{k+1}=x_k-f(x_k)/f'(x_k)\) is locally quadratic if \(f'(x_*)\neq 0\), and it can diverge or hunt if started badly or if \(f'\) is tiny (a multiple root, a flat diode exponential at large reverse bias in a poorly scaled model). Secant replaces \(f'\) by a difference quotient; it is the derivative-free cousin used when the Jacobian is expensive. In load flow, Newton–Raphson is this idea in \(n\) dimensions: \(J\Delta x=-f(x)\), with \(J\) the Jacobian of the mismatch.

Stopping criteria must mix residual and step: stop when \(|f(x_k)|\) is small *and* \(|x_{k+1}-x_k|\) is small relative to the scale of \(x\). A residual of \(10^{-12}\) on \(f(x)=e^{40x}-2\) is not the same as on \(f(x)=x-2\). Scale equations (per-unit, normalisation) before iterating.

Polynomial roots: companion-matrix eigenvalues (unit 05) are the robust route in software. Hand methods: factoring, quadratic formula, and maybe one Newton polish. Routh–Hurwitz (control pack) counts unstable roots without finding them. Do not use an un-stabilised companion in a hand 4-by-4 det expansion as a “numerical method.”

Numerical differentiation: the forward difference \((f(x+h)-f(x))/h\) has truncation \(O(h)\) and roundoff \(O(\varepsilon/h)\); the sweet \(h\) is not machine epsilon. Central difference \(O(h^2)\) is better. In circuits, you rarely differentiate tabulated data if you can fit a spline or use an analytic device model. Sensitivity \(\partial y/\partial p\) is a derivative; adjoint methods are later.

Numerical integration (quadrature) computes \(\int_a^b f(x)\,dx\) from samples. Trapezoid rule on uniform panels of width \(h\) is
\[
\frac{h}{2}\big(f_0+2f_1+\cdots+2f_{n-1}+f_n\big)
\]
with error \(O((b-a)h^2 f'')\) if \(f''\) is bounded. Simpson’s rule (\(n\) even) is \(O(h^4)\) and is the default UG improvement. Gauss quadrature with \(n\) nodes integrates polynomials of degree \(2n-1\) exactly; it is how many libraries compute inner products. In EE, rms is \(\sqrt{\frac{1}{T}\int_0^T v^2(t)\,dt}\); average power is \(\frac{1}{T}\int v i\,dt\). Both are quadratures. A scope that samples \(N\) points per period and uses trapezoid is doing this unit.

Improper integrals and singularities (a \(1/\sqrt{x}\) near 0, an oscillatory Fourier integral) need a change of variable or a specialised oscillatory integrator. Blind trapezoid on a jump is first-order at best and should be split at the discontinuity.

Linear systems \(Ax=b\): Gaussian elimination with partial pivoting is the UG workhorse. Without pivoting, a small pivot from a nearly singular nodal matrix (or a bad scaling) destroys the answer. LU factorisation reuses the elimination on many right-hand sides (that is harmonic analysis at many frequencies with a fixed sparse pattern, or a time-stepping method with a fixed companion matrix). Symmetric positive definite energy matrices should be factored by Cholesky: half the work, and a failed factorisation diagnoses a modelling error (unit 05). Iterative methods (Jacobi, Gauss–Seidel) are the same updates as load-flow Gauss–Seidel: cheap per step, convergence depends on a spectral radius \(<1\). They are not a replacement for a 3-by-3 hand solve.

Condition number \(\kappa(A)=\|A\|\|A^{-1}\|\) bounds the relative error in \(x\) by roughly \(\kappa\) times the relative residual or data error. A Hilbert-like matrix from polynomial fitting is a famous disaster; fitting in an orthogonal basis (or using QR) is the fix. In EE, a mixed circuit with pico-farads and thousands of henries, un-normalised, produces huge \(\kappa\). Per-unit and SI prefixes exist to prevent that.

Nonlinear systems: diode-resistor networks, implicit integration of stiff transients (backward Euler), and Newton load flow all solve \(f(x)=0\) in \(\mathbb{R}^n\). Damping (step length control) and a good initial guess (flat start versus previous time step) decide success. UG exams usually ask one Newton step by hand, not a production solver.

ODE numerics (preview): forward Euler \(x_{k+1}=x_k+h f(t_k,x_k)\) is simple and can be unstable for stiff circuits (a tiny parasitic time constant forces tiny \(h\)). Backward Euler solves an implicit equation per step and damps stiff modes. Trapezoidal rule (the companion of bilinear transform in discrete control) is A-stable for linear test equations. Choosing \(h\) relative to the smallest time constant is the engineering content; the formula is secondary.

Interpolation: piecewise linear between samples is what a DSO draw does. Polynomial interpolation through many points oscillates (Runge). For a smooth device curve, a cubic spline or a physically based model beats a degree-12 interpolant.

Error: absolute \(|\tilde{x}-x|\), relative \(|\tilde{x}-x|/|x|\) (undefined at \(x=0\)). Truncation error is the method’s if arithmetic were exact. Roundoff is finite precision. Total error is not always their sum in the worst direction, but UG estimates treat them separately and take the larger.

## Equations

Bisection after \(n\) steps on \([a,b]\): interval length \((b-a)/2^n\), root error bound half of that.

Newton:

\[
x_{k+1}=x_k-\frac{f(x_k)}{f'(x_k)}.
\]
Quadratic: \(e_{k+1}\approx C e_k^2\) when \(f'(x_*)\neq 0\), \(C=f''(x_*)/(2f'(x_*))\).

Secant:

\[
x_{k+1}=x_k-f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}.
\]

Trapezoid and Simpson (uniform \(h\), \(n=(b-a)/h\)):

\[
T=\frac{h}{2}(f_0+2\sum_{i=1}^{n-1}f_i+f_n),\qquad
S=\frac{h}{3}(f_0+4f_1+2f_2+\cdots+4f_{n-1}+f_n).
\]

Forward/central differences:

\[
f'(x)=\frac{f(x+h)-f(x)}{h}+O(h)=\frac{f(x+h)-f(x-h)}{2h}+O(h^2).
\]

Gaussian elimination: \(A=LU\) (after permutation \(PA=LU\)). Solve \(Ly=Pb\), \(Ux=y\).

Residual and backward error: \(r=b-A\tilde{x}\). A small \(r\) means \(\tilde{x}\) solves a nearby system; if \(\kappa\) is large, \(\tilde{x}\) may still be far from \(A^{-1}b\).

Relative perturbation bound (schematic, consistent norms):

\[
\frac{\|\Delta x\|}{\|x\|}\lesssim \kappa(A)\frac{\|\Delta b\|}{\|b\|}.
\]

Forward Euler / backward Euler on \(\dot{x}=f(x)\):

\[
x_{k+1}=x_k+h f(x_k),\qquad x_{k+1}=x_k+h f(x_{k+1}).
\]

## Methods

Before choosing a method, ask whether a substitution (Lambert W for a diode with series R, a phasor closed form, a Laplace inversion) already solves it. Numerical methods are for the remainder.

For a scalar root: plot or evaluate \(f\) at a few points, bracket, bisection until you have a safe start, then Newton if \(f'\) is easy. In a diode KVL \(I_s(e^{v/\eta V_T}-1)+(v-V_{cc})/R=0\), work in volts, maybe use \(i\) as the unknown to keep exponentials from overflowing, and cap the Newton step.

For an integral of a sampled period, use trapezoid unless the waveform is quadratic-smooth and \(n\) is even, then Simpson. If the waveform has corners (rectified sine), split the integral at the kinks; Simpson across a kink loses order.

For \(Ax=b\) with \(n=2,3\), eliminate by hand with partial pivoting: swap so the largest remaining column entry is the pivot. Substitute back. Compute the residual as a check. For SPD \(2\times 2\), Cholesky is \(A=LL^T\) with \(L_{11}=\sqrt{a_{11}}\).

To estimate a derivative from data, use central differences in the interior and a step \(h\) of several sample spacings if the data are noisy (noise amplifies as \(1/h\)).

To integrate a stiff linear test \(\dot{x}=-\lambda x\) with \(\lambda>0\) large, check the forward-Euler stability region \(|1-h\lambda|<1\), i.e. \(h<2/\lambda\). If the circuit also has a 50 Hz period of interest, that tiny \(h\) is painful: use backward Euler or a library implicit solver.

Report answers with a digit count matching the method: bisection after 10 steps on a unit interval is good to about \(10^{-3}\), not 12 decimals.

When implementing Newton in a spreadsheet for a small network, compute the Jacobian from analytic device stamps if you can; finite-difference Jacobians need a step that balances truncation and roundoff, the same as numerical differentiation.

## Mistakes

Starting Newton at a point where \(f'=0\) or is tiny (the top of a diode exponential overflow, a multiple root) and declaring “no solution.”

Using bisection without a sign change: an even-multiplicity root never brackets.

Applying Simpson with an odd number of panels (odd \(n\)). The formula as usually written needs even \(n\).

Estimating \(\int_0^{2\pi}\cos^2\theta\,d\theta\) by two samples and claiming rms of a sine is 1. Undersampling is aliasing (signals pack) as well as quadrature error.

Gaussian elimination without pivoting on \(\begin{pmatrix}\varepsilon&1\\1&1\end{pmatrix}\), then taking \(\varepsilon\to 0\) in float.

Inverting \(A\) to solve one \(Ax=b\), paying \(n^3\) then \(n^3\) again conceptually, and accumulating more roundoff than LU plus solve.

Treating a small residual as a small error in \(x\) on an ill-conditioned nodal matrix.

Forward Euler with \(h=10^{-3}\) on a circuit that has a \(10^{-9}\ \mathrm{s}\) parasitic, then blaming the device model for oscillation of the numerical solution.

Differencing a noisy DSO trace with \(h=\) one sample, producing a derivative that looks like noise, then integrating it and wondering why the integral drifts (you amplified then tried to smooth).

Writing relative error when the true value is 0 (a null voltage). Use an absolute tolerance referenced to a full-scale voltage.

Using degree-\(n-1\) interpolation through \(n\) Chebyshev-unrelated samples on a Runge-like function and trusting the interpolant between samples.

Forgetting units inside \(f'(x)\) in Newton: \(f\) in volts, \(x\) in amperes, \(f'\) in ohms. The update \(f/f'\) then has units of amperes, as it should. Mixing mA and A in \(x\) but not in \(f'\) scales the step by 1000.
