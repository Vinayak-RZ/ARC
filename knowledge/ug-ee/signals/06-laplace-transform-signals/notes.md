# ROC, unilateral Laplace, system functions

The Laplace transform is a Fourier transform with an exponential weight \(e^{-\sigma t}\). That weight can make a growing or everlasting signal integrable. The set of \(\sigma\) (equivalently of complex \(s=\sigma+j\omega\)) for which the integral converges is the region of convergence (ROC). Without the ROC, a rational algebraic expression \(X(s)\) is ambiguous: the same formula can belong to a causal exponential or to an anticausal one. This unit treats bilateral and unilateral Laplace transforms, ROC rules, inversion by partial fractions, and LTI system functions.

## Concepts

The bilateral (two-sided) Laplace transform is

\[
X(s)=\int_{-\infty}^{\infty}x(t)e^{-st}\,dt.
\]

Absolute convergence at a point \(s_0\) implies convergence in a vertical strip containing \(s_0\), typically \(\alpha < \operatorname{Re}s < \beta\). The strip may extend to \(+\infty\) or \(-\infty\). Rational transforms have poles; the ROC never contains poles and is bounded by vertical lines through poles (or by infinity). A finite-support signal has ROC equal to the whole plane (except possibly \(s=\infty\) as a degree issue). A right-sided signal (zero for \(t<T_1\)) has an ROC that is a right half-plane, to the right of the rightmost pole if \(X\) is rational. A left-sided signal has a left half-plane ROC. A two-sided signal has a strip.

The unilateral (one-sided) transform integrates from \(0^-\) or \(0^+\) to \(\infty\) and is the tool for causal initial-value problems. Differentiation then brings in \(x(0^-)\). Engineers solving circuit transients almost always want the unilateral transform. Signals-and-systems inversion and ROC arguments almost always want the bilateral transform. Mixing the two without comment produces missing initial-condition terms.

Standard pair: \(e^{-at}u(t)\leftrightarrow 1/(s+a)\) with ROC \(\operatorname{Re}s > -\operatorname{Re}a\). The anticausal pair \(-e^{-at}u(-t)\leftrightarrow 1/(s+a)\) with ROC \(\operatorname{Re}s < -\operatorname{Re}a\). Same algebra, opposite ROC, opposite time support. Partial fractions must be completed by choosing, for each pole, a causal or anticausal exponential according to the ROC.

Properties: time shift \(x(t-t_0)\) multiplies by \(e^{-s t_0}\) (bilateral). Frequency-domain shift \(e^{s_0 t}x(t)\) replaces \(s\) by \(s-s_0\) and shifts the ROC. Convolution in time is a product of transforms when the ROC contains the intersection of the two ROCs (possibly enlarged after pole-zero cancellation). The final-value theorem \(x(\infty)=\lim_{s\to 0}sX(s)\) requires that all poles of \(sX(s)\) lie in the open left half-plane; applying it to a sinusoid is illegal. The initial-value theorem \(x(0^+)=\lim_{s\to\infty}sX(s)\) holds for unilateral transforms of causal signals under mild conditions.

An LTI system function is \(H(s)=Y(s)/X(s)\) when the system is initially at rest, equivalently \(H(s)=\int h(t)e^{-st}\,dt\) with ROC determined by \(h\). Poles of \(H\) are natural frequencies. Zeros are frequencies blocked in the eigenfunction sense. A proper rational \(H\) corresponds to a differential equation; the degree of the denominator is the order. Improper \(H\) contains differentiators.

Causality plus BIBO stability: the ROC of \(H\) must include the \(j\omega\) axis, and for a causal system the ROC is a right half-plane, so all poles must lie in \(\operatorname{Re}s<0\). Stability without causality allows poles in the right half-plane if the ROC is a strip that still includes the axis (anticausal left-sided exponentials decaying toward \(-\infty\)). That combination is not a real-time device but is legal as a filter on recorded data.

Partial-fraction inversion of a proper rational \(X(s)\): factor the denominator, expand, and map each term \(A/(s-p)\) to \(A e^{pt}u(t)\) or to \(-A e^{pt}u(-t)\) according as the ROC lies to the right or left of \(p\). Repeated poles produce \(t^{m}e^{pt}\) factors. Cover-up is enough for simple poles. If the degree of the numerator is not smaller, divide first (impulses and derivatives of impulses).

The relationship to the Fourier transform: if the ROC includes \(\operatorname{Re}s=0\), then \(X(j\omega)=H(s)|_{s=j\omega}\) in the ordinary sense. If the axis is a boundary of the ROC, a Fourier transform may still exist as a principal value plus impulses (unit step). If the axis is outside the ROC, the CTFT does not converge.

Multivariable and delay systems: \(e^{-sT}\) is a delay of \(T\). Transcendental system functions appear in transmission lines and sampled-data holds. Undergraduate inversion still uses residues when a rational multiplier is present.

The abscissa of convergence can be read from growth. If \(|x(t)|\le C e^{\alpha t}\) for large positive \(t\) and \(x\) is right-sided, the ROC includes \(\operatorname{Re}s>\alpha\). If a left-sided signal grows at most as \(e^{\beta t}\) as \(t\to-\infty\), the ROC includes \(\operatorname{Re}s<\beta\). Matching both sides of a two-sided signal produces a strip. Polynomial growth \(t^m e^{\alpha t}\) does not move the abscissa relative to the pure exponential, but it raises the pole order.

Unilateral Laplace of a derivative uses \(0^-\) so that an impulse at the origin in \(x'(t)\) is captured when \(x\) jumps at \(t=0\). Circuit problems that write KVL for \(t>0\) with capacitor voltage \(v(0^-)\) are using that convention. If a source impulse dumps charge at \(t=0\), \(v(0^+)\neq v(0^-)\), and the transform still works if the impulse is included in the equation.

Partial fractions with complex poles: keep conjugate pairs for real signals, or combine them into a quadratic and invert as a damped cosine with a phase. Completing the square in the denominator of a second-order term yields the standard \(\omega_n, \zeta\) pair. Underdamped causal inversion is \(e^{-\zeta\omega_n t}\sin(\omega_d t+\phi)u(t)\) with \(\omega_d=\omega_n\sqrt{1-\zeta^2}\).

System functions of cascades multiply; of parallel combinations add; of negative-feedback loops become \(G/(1+GH)\) in the usual block-diagram algebra, with an ROC that must be re-determined from the closed-loop poles, not blindly intersected. Cancellation of a plant pole by a compensator zero does not remove the mode from a non-minimal state realization.

The Fourier transform of a causal exponential is the Laplace transform evaluated on the axis when \(\operatorname{Re}a>0\). That special case is why \(1/(a+j\omega)\) appears in both tables. When \(a=0\), Laplace of \(u(t)\) is \(1/s\) with \(\operatorname{Re}s>0\), while the CTFT of \(u(t)\) needs the extra \(\pi\delta(\omega)\). Boundary ROC is the warning flag.

Bromwich inversion is the inverse Laplace integral along a vertical line in the ROC. Closing the contour to the left for \(t>0\) (Jordan’s lemma, exponential decay of \(e^{st}\) in the left half-plane when \(t>0\)) picks up right-sided residues. Closing to the right for \(t<0\) picks up left-sided residues. That is the geometric reason ROC chooses causal versus anticausal terms. UG courses usually skip the contour and remember the outcome as the partial-fraction rule.

## Equations

Bilateral definition and ROC strip \(\alpha<\operatorname{Re}s<\beta\).

Unilateral:

\[
X_u(s)=\int_{0^-}^{\infty}x(t)e^{-st}\,dt, \qquad
\mathcal{L}\{x'(t)\}=sX_u(s)-x(0^-).
\]

Causal exponential:

\[
e^{-at}u(t)\ \longleftrightarrow\ \frac{1}{s+a},\quad \operatorname{Re}s>-\operatorname{Re}a.
\]

Anticausal:

\[
-e^{-at}u(-t)\ \longleftrightarrow\ \frac{1}{s+a},\quad \operatorname{Re}s<-\operatorname{Re}a.
\]

Convolution: \(x*h\leftrightarrow X(s)H(s)\) on \(\operatorname{ROC}_x\cap\operatorname{ROC}_h\) (possibly larger).

Integration (causal): \(\int_{0^-}^{t}x(\tau)\,d\tau\leftrightarrow X(s)/s\) with a possibly tightened ROC.

Initial and final values (unilateral, with the hypotheses stated above):

\[
x(0^+)=\lim_{s\to\infty}sX(s), \qquad
x(\infty)=\lim_{s\to 0}sX(s).
\]

System function of a constant-coefficient ODE \(\sum_{k=0}^{N}a_k y^{(k)}=\sum_{m=0}^{M}b_m x^{(m)}\):

\[
H(s)=\frac{\sum_m b_m s^{m}}{\sum_k a_k s^{k}}.
\]

## Methods

Identify support of \(x\) first: right-sided, left-sided, two-sided, or finite. That almost determines the ROC shape. Then compute or table \(X(s)\) and cut out poles.

To invert, expand in partial fractions. Draw poles on the \(s\)-plane and shade the given ROC. Each pole is associated with the unique exponential whose ROC can contain that shade on the appropriate side of the pole.

For unilateral ODE problems, transform the differential equation, insert initial conditions, solve for \(Y(s)\), invert. Do not use the bilateral pair on a \(t>0\) circuit problem if \(x(0^-)\) is given.

To test whether \(H(j\omega)\) is a Fourier frequency response, check that \(\operatorname{Re}s=0\) lies in the ROC of \(H\). Then BIBO stability is \(\int|h|<\infty\), which for rational causal \(H\) is all poles in the open left half-plane.

Pole-zero cancellation: a cancelled pole still constrains an ROC if it was a pole of an intermediate product; after cancellation the ROC may enlarge. Example: a differentiator following an integrator.

When \(X(s)\) is improper, write \(X(s)=\) polynomial \(+\) proper remainder. The polynomial inverts to \(\delta\), \(\delta'\), \ldots

Use the final-value theorem only after confirming that \(y(t)\) approaches a finite limit, equivalently that poles of \(sY(s)\) are strictly stable.

When an ROC is not stated, a problem that says “causal system” or “\(t\ge 0\) with rest IC” is telling you the ROC is a right half-plane. A problem that gives a two-sided formula for \(x(t)\) is telling you to intersect the half-planes of each piece. Silence about ROC in a bilateral inversion problem is incomplete; do not default to causal if the support was two-sided.

To build \(H(s)\) from an ODE, move to rest IC, replace \(d/dt\) by \(s\), and form \(Y/X\). Check properness: if the numerator degree exceeds the denominator, expect delta derivatives in \(h(t)\). Many circuit admittances are improper (a capacitor \(sC\)).

Sanity checks after inversion: \(x(0^+)\) versus initial-value theorem; area \(\int_0^\infty x(t)\,dt = X(0)\) when the axis is in the ROC of a causal transform; growth versus the rightmost pole.

## Mistakes

Writing \(1/(s+a)\) without an ROC, then inverting as a causal exponential when the problem stated a left-sided signal.

Using the final-value theorem on \(Y(s)=\omega/(s^2+\omega^2)\), which corresponds to a cosine that has no final value.

Confusing \(0^-\) and \(0^+\) in the differentiation rule, dropping a jump.

Evaluating \(H(s)\) at \(s=j\omega\) when a pole sits on the axis and calling that the CTFT.

Assuming every rational \(H(s)\) is causal. Causality is an ROC (or a “proper and ROC right-sided”) statement, not a ratio of polynomials alone.

Forgetting that ROC is a vertical strip: drawing disks around poles as if this were a Z-transform.

Canceling a pole and a zero and then claiming a new ROC that includes a remaining pole.

Applying unilateral Laplace to two-sided signals and missing the \(t<0\) part.

Mixing Fourier \(2\pi\) factors into Laplace inversion. Laplace inversion is a vertical Bromwich integral \(\frac{1}{2\pi j}\int X(s)e^{st}ds\), not the Fourier inverse with \(s=j\omega\) unless the path is the axis and the ROC allows it.

Treating \(e^{s_0 t}\) as a shift in time rather than a shift in \(s\).
