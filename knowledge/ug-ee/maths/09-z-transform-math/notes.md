# Z as a transform pair

The (unilateral and bilateral) Z-transform is the discrete-time partner of the Laplace transform. It is the algebra behind linear constant-coefficient difference equations, discrete filters, sampled-data control, and the discrete LTI systems of a signals course. This unit treats \(X(z)\) as a transform pair with a region of convergence (ROC), inversion by partial fractions plus the causal/anti-causal table, and the theorems (shift, convolution, differentiation in \(z\)). DFT/DFS numerical transforms are a different object (signals pack). The bilinear map from \(s\) to \(z\) is mentioned as a bridge to control, not as a full digital-redesign course.

Sampling a continuous \(x_c(t)\) at period \(T\) produces a sequence \(x[n]=x_c(nT)\). The Z-transform does not know about \(T\) until you restore it in \(z=e^{sT}\). Mixing \(n\) (integer) with \(t\) (seconds) in one exponent is a method error.

## Concepts

The bilateral Z-transform is
\[
X(z)=\sum_{n=-\infty}^\infty x[n]z^{-n},
\]
a Laurent series in \(z\in\mathbb{C}\). It converges in an annulus \(R_-<|z|<R_+\). The unilateral transform sums from \(n=0\) to \(\infty\) and is the default for causal sequences and initial-condition problems, analogous to unilateral Laplace. A finite-length sequence converges everywhere except possibly \(0\) and \(\infty\). A right-sided sequence (zero for \(n<N_{\min}\)) has ROC \(|z|>R_-\) (outside a circle). A left-sided sequence has ROC \(|z|<R_+\). Two-sided sequences have a ring, which may be empty.

Poles of a rational \(X(z)\) sit on the boundary of the ROC, not in its interior. The ROC is required to invert: \(X(z)=1/(1-\tfrac12 z^{-1})\) is \(x[n]=(\tfrac12)^n u[n]\) if \(|z|>1/2\), and \(x[n]=-(\tfrac12)^n u[-n-1]\) if \(|z|<1/2\). Writing a formula without ROC is an incomplete pair. For causal LTI systems the ROC is the exterior of the outermost pole, and BIBO stability is equivalent to that ROC including the unit circle \(|z|=1\) (absolute summability of \(h[n]\)). A causal system is stable iff all poles lie inside the open unit disk. That is the discrete analogue of left-half-plane poles.

The unit circle \(z=e^{j\omega}\) (here \(\omega\) is normalised radians per sample) is the discrete-time Fourier transform when it lies in the ROC. Frequency response of a stable rational filter is \(H(e^{j\omega})\). Aliasing and \(2\pi\)-periodicity of DTFT are because \(e^{j\omega}\) is already \(2\pi\)-periodic in \(\omega\).

Shift theorems: a delay \(x[n-n_0]\) multiplies by \(z^{-n_0}\) in the bilateral transform (with ROC unchanged except possibly \(0,\infty\)). Unilateral delay brings in initial samples \(x[-1],\ldots\) similar to Laplace’s \(f(0^-)\). Advance \(x[n+1]\) produces \(z(X(z)-x[0])\) unilaterally. Difference equations are converted to algebraic equations in \(z\) the same way ODEs are converted in \(s\).

Convolution of sequences \(x*h\) becomes \(X(z)H(z)\) with ROC at least the intersection of ROCs. This is FIR and IIR filtering in the transform domain. Partial-fraction inversion of \(H(z)\) (usually written in \(z^{-1}\) for DSP, or as a proper function of \(z\) for control) yields the impulse response as a sum of geometric sequences \(p^n u[n]\) for causal poles \(p\).

Multiplication by \(a^n\) maps \(X(z)\) to \(X(z/a)\), scaling the ROC. Multiplication by \(n\) is \(-z\,dX/dz\). These are the tools that produce \(n a^n u[n]\) from repeated poles, matching Laplace’s \(t e^{at}\).

Final-value theorem: \(x[\infty]=\lim_{z\to 1}(z-1)X(z)\) for unilateral \(X\), when all poles of \((z-1)X(z)\) lie inside the open unit disk (simple pole at \(z=1\) allowed). It fails for poles on the unit circle other than a simple \(z=1\), e.g. an undamped oscillator \((-1)^n\). Initial-value: \(x[0]=\lim_{z\to\infty}X(z)\) for causal sequences (the proper rational function’s finite limit).

Inverse by long division (power series in \(z^{-1}\)) gives as many time samples as you have patience for, useful for FIR checks and for reading the first few Markov parameters of a state-space model. Residue inversion (unit 10) on \(X(z)z^{n-1}\) is the contour-integral definition; for rational functions it is partial fractions.

Relationship to Laplace: if \(x[n]=x_c(nT)\) and \(X_c(s)\) is a Laplace transform, the starred transform and \(z=e^{sT}\) are the bridge. Mapping the left-half \(s\)-plane through \(z=e^{sT}\) sends it to the open unit disk. The bilinear transform \(s=\frac{2}{T}\frac{z-1}{z+1}\) also sends the left half-plane to the disk, without aliasing but with frequency warping \(\omega_c=\frac{2}{T}\tan(\omega_d T/2)\). Digital control uses that map; this unit only needs the geometry.

Finite-word-length effects (quantised coefficients moving poles) belong in the DSP elective. The mathematics here already shows why poles near the unit circle (high-Q resonators, lightly damped discrete plants) are sensitive: a small \(\Delta a\) in a polynomial can move a root across \(|z|=1\).

Units: \(z\) is dimensionless. A discrete transfer function \(H(z)\) mapping volts to volts is dimensionless; mapping a sequence of samples of a current to a voltage carries ohms, same as analog.

## Equations

Bilateral definition and inversion (contour in the ROC, counterclockwise):

\[
X(z)=\sum_{n=-\infty}^\infty x[n]z^{-n},\qquad x[n]=\frac{1}{2\pi j}\oint X(z)z^{n-1}\,dz.
\]

Geometric pair (causal):

\[
a^n u[n]\ \longleftrightarrow\ \frac{1}{1-az^{-1}},\quad |z|>|a|,
\]
equivalently \(z/(z-a)\) for \(|z|>|a|\). Anti-causal:
\[
-a^n u[-n-1]\ \longleftrightarrow\ \frac{1}{1-az^{-1}},\quad |z|<|a|.
\]

Unilateral delay:

\[
x[n-1]u[n]\ \longleftrightarrow\ z^{-1}X(z)+x[-1].
\]
(Conventions on whether \(x[-1]\) appears depend on the exact unilateral definition; state the IC term when solving a difference equation.)

Difference equation (LCCDE):

\[
\sum_{k=0}^N a_k y[n-k]=\sum_{m=0}^M b_m x[n-m].
\]
At rest, \(H(z)=(\sum b_m z^{-m})/(\sum a_k z^{-k})\).

Convolution: \(y=x*h \leftrightarrow Y=XH\) (ROC \(\supset\) intersection).

Differentiation:

\[
n x[n]\ \longleftrightarrow\ -z\frac{dX}{dz}.
\]

Parseval (unit circle in ROC): energy \(\sum |x[n]|^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi}|X(e^{j\omega})|^2 d\omega\).

Bilinear (reference):

\[
s=\frac{2}{T}\frac{z-1}{z+1},\qquad z=\frac{1+sT/2}{1-sT/2}.
\]

## Methods

Write the sequence as right-sided, left-sided, or two-sided, and mark the ROC before inverting. Factor \(X(z)\) in \(z\) (or \(z^{-1}\), consistently). Perform partial fractions in the same variable you will match to the table. A term \(K/(1-pz^{-1})\) with ROC \(|z|>|p|\) inverts to \(K p^n u[n]\). If the ROC is \(|z|<|p|\), invert to \(-K p^n u[-n-1]\).

For a strictly proper rational function in \(z^{-1}\) that is improper in \(z\), first write a polynomial in \(z^{-1}\) plus a strictly proper remainder, or multiply numerator and denominator by \(z^N\) and do partial fractions in \(z\), remembering that
\[
\frac{z}{z-p}\ \longleftrightarrow\ p^n u[n].
\]
The extra \(z\) in the numerator is why many EE tables expand \(X(z)/z\) rather than \(X(z)\).

To solve a linear difference equation: take unilateral Z, insert initial \(y[-1],\ldots,y[-N]\), solve for \(Y(z)\), invert. Check the first few \(y[n]\) by iterating the recurrence from the ICs as a numerical audit.

To test stability of a causal rational \(H(z)\): poles inside the unit disk. For a second-order section \(1/(1-2r\cos\theta\, z^{-1}+r^2 z^{-2})\), poles at \(r e^{\pm j\theta}\); need \(r<1\). Jury’s test is the discrete Routh analogue; for \(n=2\) the \(r<1\) geometry is enough.

When evaluating frequency response, substitute \(z=e^{j\omega}\) only after stability (or after restricting to DTFT existence). Compute magnitude \(|H|\) and phase; linear phase of a symmetric FIR is a polynomial in \(z^{-1}\) with zeros in reciprocal pairs.

For sampled sinusoids, \(x[n]=\cos(\omega_0 n)u[n]\) is *not* the two-sided cosine; its Z-transform is the causal pair with poles at \(e^{\pm j\omega_0}\) on the unit circle, ROC \(|z|>1\), and the DTFT exists only in a distributional sense. The everlasting cosine has a DTFT with impulses and no ordinary Z-transform covering the unit circle as an open ROC.

Map analog poles through \(z=e^{sT}\) for impulse-invariant sketches: \(s=-a\) maps to \(z=e^{-aT}\). Do not map zeros that way for impulse invariance (the method matches residues, not zeros). Bilinear maps both poles and zeros via the algebraic formula, then optionally pre-warps critical frequencies.

To recover a few samples without a full inverse, divide the numerator by the denominator as series in \(z^{-1}\) (causal ROC, \(|z|\) large). The coefficients are \(x[0],x[1],x[2],\ldots\). This long division is the fastest check that a partial-fraction inverse matches the recurrence. For an FIR polynomial \(b_0+b_1 z^{-1}+\cdots+b_M z^{-M}\), the impulse response is already the coefficient list; do not invent poles.

When a closed loop of discrete transfer functions is written, the characteristic polynomial is \(1+L(z)=0\) for negative feedback with loop \(L\). Roots of that polynomial, not the open-loop poles, decide sampled-data stability. A stable plant discretized and then wrapped with a high gain can still push a closed-loop root through the unit circle; the Jury table or a root plot versus gain is the discrete Nyquist substitute at UG level.

Normalised frequency \(\omega=\Omega T\) uses the analog radian frequency \(\Omega\) and the sample period. At Nyquist, \(\omega=\pi\). Writing a digital notch at “50 Hz” without stating \(T\) (or \(f_s\)) is an incomplete specification: the same 50 Hz is \(\omega=\pi/10\) at \(1\ \mathrm{kHz}\) sampling and a different \(\omega\) at \(8\ \mathrm{kHz}\).

## Mistakes

Omitting the ROC and then picking the causal inverse of a left-sided sequence (or vice versa). The same rational function has two standard inverses.

Writing \(H(z)=1/(z-0.5)\) and inverting as \((0.5)^n u[n]\) without the extra \(z\) factor. The pair is \(z/(z-0.5)\leftrightarrow (0.5)^n u[n]\), so \(1/(z-0.5)\leftrightarrow (0.5)^{n-1}u[n-1]\) (causal), not the same sequence.

Using Laplace final-value \(\lim_{s\to 0}sF(s)\) on a Z problem, or \(\lim_{z\to 0}(z-1)X(z)\). The Z final-value uses \(z\to 1\).

Declaring a causal filter with a pole at \(z=-1.1\) “stable because the pole is negative.” Stability is \(|p|<1\), not \(\operatorname{Re}p<0\). The left-half-plane intuition does not transfer without the exponential map.

Substituting \(z=s\) or \(z=j\omega\) for analog frequency. Discrete frequency lives on the unit circle \(z=e^{j\omega}\).

Forgetting \(2\pi\)-periodicity and treating \(\omega=3\pi\) as a new analog frequency rather than \(\omega=\pi\) (Nyquist, alias).

Unilateral shift missing initial conditions, then wondering why the particular solution of a recurrence does not match \(n=0,1\).

Partial fractions of \(X(z)\) instead of \(X(z)/z\) while using a table written for \(X(z)/z\), producing a missing factor.

Bilinear transform without pre-warping, then expecting the analog cutoff \(\omega_c\) to sit at the same digital \(\omega\). It will not, except at DC to first order.

Writing \(\sum_{n=0}^\infty a^n = 1/(1-a)\) without \(|a|<1\), then setting \(a=z^{-1}\) without translating the condition into \(|z|>|a|\).
