# Partial fractions and residues

Inverting Laplace transforms, Z-transforms, and contour integrals in UG EE is one skill with two dialects: partial fractions of a rational function, and residues of a meromorphic function. This unit is that skill. It is the algebraic endgame of units 03 and 09 and the minimum complex analysis needed to close a Bromwich or a \(z^{n-1}X(z)\) contour. It is not a first course in holomorphic functions, Cauchy’s theorem in full generality, or conformal maps. Analyticity is used only as far as “poles are isolated, residues are coefficients of \(1/(s-p)\), Cauchy’s integral formula computes them.”

Every strictly proper rational function of a complex variable can be written as a sum of principal parts at its poles plus, if the function is improper, a polynomial. Inverse Laplace and inverse Z tables are those principal parts term by term. Computing the coefficients incorrectly is how a correct \(Y(s)\) becomes a wrong waveform.

## Concepts

A function \(F(s)\) is rational if it is a ratio of polynomials. Assume the representation is coprime (cancelled common factors). Poles are the zeros of the denominator. A pole of order \(m\) at \(p\) means \((s-p)^m\) divides the denominator exactly once as a highest power. Order 1 is simple. At a simple pole the Laurent series has a \(K/(s-p)\) term and no worse; \(K\) is the residue \(\operatorname{Res}(F,p)\). At a pole of order 2 there is also \(A/(s-p)^2\). Inverse Laplace of \(1/(s-p)^{k+1}\) is \(t^k e^{pt}/k!\) times the unit step (unilateral, ROC to the right of the pole). That is why the partial-fraction coefficients are the time-domain amplitudes.

Cover-up (Heaviside) for a simple pole:
\[
K=\operatorname{Res}(F,p)=(s-p)F(s)\big|_{s=p}=\frac{N(p)}{D'(p)}
\]
when \(F=N/D\) and \(D(p)=0\neq N(p)\). The derivative form is convenient when \(D\) is already expanded and \(p\) is known. For a quadratic real factor that you refuse to split, the residue at each complex pole is still cover-up; combining conjugate residues produces a real damped sinusoid (unit 03).

For a pole of order \(m\) at \(p\),
\[
A_k=\frac{1}{(m-k)!}\frac{d^{m-k}}{ds^{m-k}}\Big[(s-p)^m F(s)\Big]_{s=p},\qquad k=1,\ldots,m,
\]
with the \(1/(s-p)^k\) coefficient \(A_k\). In particular the residue is \(A_1\), the coefficient of \(1/(s-p)\), which for \(m=2\) is the derivative formula in unit 03. Students often compute only \(A_m\) (the easiest cover-up) and omit \(A_1\), dropping a \(e^{pt}\) term next to \(t e^{pt}\).

Improper functions: if \(\deg N\ge \deg D\), divide first. The quotient is a polynomial in \(s\) (impulses and their derivatives under Laplace). Partial fractions apply to the strictly proper remainder. For Z-transforms, “proper” is discussed in \(z^{-1}\) or after extracting \(X(z)/z\); follow the table you are matching.

Complex conjugate symmetry: real coefficients imply residues at \(\bar{p}\) are conjugates of residues at \(p\). Computing one and conjugating is faster and avoids a second cover-up error. If your two residues at conjugate poles are not conjugates, the arithmetic is wrong or the original polynomials were not real.

Cauchy’s integral formula says that if \(F\) is analytic inside and on a simple closed positively oriented contour \(C\),
\[
\frac{1}{2\pi j}\oint_C \frac{F(s)}{(s-p)^{n+1}}ds = \frac{F^{(n)}(p)}{n!}.
\]
The residue theorem says the integral of a meromorphic \(F\) is \(2\pi j\) times the sum of residues inside, for a positively oriented simple closed contour (and suitable vanishing at infinity if the contour is a large circle). Closing the Bromwich line to the left for \(t>0\) (where \(e^{st}\) decays as \(\operatorname{Re}s\to -\infty\)) picks up all poles of \(F(s)e^{st}\) in the left half-plane plus any on the way, giving the usual causal inverse. For \(t<0\) one closes to the right and gets zero if \(F\) is strictly proper and all poles are to the left of the Bromwich line (causal functions). That is the inversion integral of unit 03 made finite.

At infinity, a strictly proper Laplace transform vanishes; Jordan’s lemma justifies the arc contribution \(\to 0\) under standard degree hypotheses. UG EE uses the residue theorem as a licence to invert by residues, not as a proof course.

Simple zeros of \(N(s)\) are zeros of \(F\). A cancelled pole-zero pair is not a pole of the reduced function; the residue at a cancelled location is zero because the function is removable or analytic there after reduction. Unreduced state-space models may still contain the mode (unit 03 warning).

Z-transform inversion:
\[
x[n]=\sum_k \operatorname{Res}\big(X(z)z^{n-1},\, p_k\big)
\]
over poles inside the ROC-bounded contour. For causal sequences and \(n\ge n_{\min}\), the contour is a large circle enclosing all poles. The extra \(z^{n-1}\) shifts pole orders: a simple pole of \(X\) remains simple in \(X(z)z^{n-1}\) for each fixed \(n\), unless a pole at 0 is created when \(n-1<0\). Handle \(n=0\) separately if \(X\) has relative degree issues at the origin.

Partial fractions over the reals keep irreducible quadratics:
\[
\frac{Bs+C}{s^2+2\zeta\omega_n s+\omega_n^2}
\]
and complete the square. Partial fractions over \(\mathbb{C}\) split those into simple poles. Both are correct; the real form matches the damped-sine table without Euler.

Repeated real poles appear in critically damped circuits, in \(1/s^2\) (ramps), and in \(1/(s+a)^2\) (the \(t e^{-at}\) of a repeated eigenvalue). Distinct poles are the generic case; a numerical polynomial solver may split a double root into two close simple roots with large opposite residues — ill-conditioning, unit 08.

Multiplication of rational functions (cascade of transfer functions) is addition of poles unless cancellation. The residue at a pole of the product is not the product of residues in general; recompute on the product.

## Equations

Simple-pole residue:

\[
\operatorname{Res}(F,p)=\lim_{s\to p}(s-p)F(s).
\]

Order-\(m\) residue:

\[
\operatorname{Res}(F,p)=\frac{1}{(m-1)!}\lim_{s\to p}\frac{d^{m-1}}{ds^{m-1}}\big[(s-p)^m F(s)\big].
\]

Laplace pairs (causal):

\[
\frac{1}{s-p}\leftrightarrow e^{pt}u(t),\qquad \frac{1}{(s-p)^{k+1}}\leftrightarrow \frac{t^k}{k!}e^{pt}u(t).
\]

Cover-up with \(F=N/D\), simple zero of \(D\):

\[
\operatorname{Res}(F,p)=\frac{N(p)}{D'(p)}.
\]

Residue theorem (positive orientation, finitely many poles inside):

\[
\frac{1}{2\pi j}\oint_C F(s)\,ds = \sum_{p\ \mathrm{inside}} \operatorname{Res}(F,p).
\]

Bromwich (sketch): \(f(t)=\sum_{\text{poles left of }\gamma}\operatorname{Res}\big(F(s)e^{st}\big)\) for \(t>0\) under standard hypotheses.

Z inversion (poles of \(X(z)z^{n-1}\) inside \(C\)):

\[
x[n]=\sum \operatorname{Res}\big(X(z)z^{n-1}\big).
\]

Real quadratic:

\[
\frac{\omega}{(s+\alpha)^2+\omega^2}\leftrightarrow e^{-\alpha t}\sin\omega t\, u(t),\qquad
\frac{s+\alpha}{(s+\alpha)^2+\omega^2}\leftrightarrow e^{-\alpha t}\cos\omega t\, u(t).
\]

## Methods

Factor the denominator completely over \(\mathbb{R}\) or \(\mathbb{C}\). Confirm strict properness; divide if needed. Write the template with undetermined \(K_i\), \(A,B\) for repeats, and \(Bs+C\) for real quadratics. Solve by cover-up where poles are simple, by derivative formulae where they repeat, and by equating coefficients as a check (clear the denominator and match powers; this also catches arithmetic errors).

For a simple pole, prefer cover-up over a linear system of all coefficients: it isolates one number. For two simple poles, two cover-ups. Then optionally expand and compare the \(s^{n-2}\) coefficient with the original as an audit.

When poles are \(\alpha\pm j\omega\), compute \(K=\operatorname{Res}(F,\alpha+j\omega)\), write
\[
2\operatorname{Re}\big(K e^{(\alpha+j\omega)t}\big)=2|K|e^{\alpha t}\cos(\omega t+\arg K)
\]
for real time functions (Laplace). Keep \(\arg K\) in the correct quadrant (unit 01).

For \(X(z)/z\) expansion: form \(X(z)/z\), partial-fraction that, multiply back by \(z\), then invert each \(z/(z-p)\). This is the control-engineering ritual; it is equivalent to residues of \(X(z)z^{n-1}\).

To invert using residues directly, multiply \(F(s)e^{st}\), residue at a simple pole \(p\) is \(K e^{pt}\) with \(K=(s-p)F(s)|_p\). At a double pole, differentiate \((s-p)^2 F(s)e^{st}\) once, divide by \(1!\), evaluate; the product rule produces the \(t e^{pt}\) and \(e^{pt}\) pair.

If a pole sits on the imaginary axis, the Bromwich line is indented or the inversion is distributional (persistent sinusoids, unit 03 FVT warning). For UG circuit inverse Laplace, use the table on those poles rather than arguing about indentations: \(s/(s^2+\omega^2)\leftrightarrow \cos\omega t\).

When a numerical \(Y(s)\) comes from a circuit, residues at natural poles are modal amplitudes fixed by initial conditions and zeros. A residue of 0 means that mode is not excited (a zero cancelled it, or ICs sit on a node of that eigenvector).

Work an example both in \(s\) and in a completed-square quadratic if the poles are complex, to confirm the same \(A,B\) of \(e^{-\alpha t}(A\cos\omega t+B\sin\omega t)\).

## Mistakes

Forgetting the derivative term at a repeated pole, keeping only \(A/(s-p)^2\) and dropping \(B/(s-p)\). The inverse then cannot match two conditions at that mode.

Cover-up at \(s=p\) while still dividing by another copy of \((s-p)\) that was not cancelled, or cancelling too many copies.

Using \(N(p)/D(p)\) instead of \(N(p)/D'(p)\). \(D(p)=0\) by definition of a pole.

Mixing Laplace and Z templates: inverting \(1/(z-p)\) as \(e^{pt}\) or \(1/(s-p)\) as \(p^n\).

Neglecting to divide an improper \(F(s)\), inventing a residue at infinity incorrectly, and missing \(\delta(t)\).

Taking residues of \(F(s)\) instead of \(F(s)e^{st}\) when claiming to use Bromwich, then wondering where the exponentials went. (Partial fractions of \(F\) first, then multiply each term by the exponential, is the safe order.)

Sign error on contour orientation: clockwise close-left would flip the residue sum. The convention is counterclockwise positive; the left-half-plane close for \(t>0\) is clockwise in the plane’s usual drawing if you go down the Bromwich and close left — actually: Bromwich goes up (\(\gamma-j\infty\) to \(\gamma+j\infty\)). Closing left makes a counterclockwise contour. Get this wrong and every inverse flips sign.

Conjugate residues that are not conjugates because \(\omega\) was taken as \(-j\) inconsistently in one pole.

Partial fractions of \(X(z)\) with terms \(K/(z-p)\) while inverting as \(p^n u[n]\) without the factor \(z\) in the numerator.

Cancelling a pole and then using residue formulae on the unreduced expression at that point and reporting a finite residue for a removable singularity that should be 0 after reduction.

Ill-conditioned split of a double pole into \(1/(s-p-\varepsilon)-1/(s-p+\varepsilon)\) with huge residues, then rounding them in a calculator and destroying the \(t e^{pt}\) shape. Keep repeats symbolic when they are exact.
