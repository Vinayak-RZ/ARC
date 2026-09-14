# ROC, inverse Z, discrete LTI

The Z-transform is the discrete-time counterpart of the Laplace transform. A sequence \(x[n]\) is mapped to a function \(X(z)\) of a complex variable \(z\), with a region of convergence that is an annulus in the \(z\)-plane. Rational \(X(z)\) are determined by poles, zeros, and the ROC. Discrete LTI systems are described by \(H(z)\) in the same language. This unit covers the bilateral transform, inversion, and the connection to linear constant-coefficient recurrences.

## Concepts

The bilateral Z-transform is \(X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n}\). Absolute convergence at a point implies convergence on a circle of that radius, and typically on an annulus \(r_< < |z| < r_>\). Finite-length sequences have ROC the whole plane except possibly \(z=0\) or \(z=\infty\). Right-sided sequences have ROC \(|z|>r\), the exterior of a circle (including infinity if the sequence is causal and starts at \(n=0\)). Left-sided sequences have ROC \(|z|<R\). Two-sided sequences have a ring.

A standard pair: \(a^n u[n]\leftrightarrow 1/(1-az^{-1})\) with \(|z|>|a|\). The left-sided counterpart \(-a^n u[-n-1]\leftrightarrow 1/(1-az^{-1})\) with \(|z|<|a|\). Same rational function, opposite ROC, opposite time support. This is the discrete echo of the Laplace causal/anticausal pair.

Properties: delay \(x[n-n_0]\) multiplies by \(z^{-n_0}\) (bilateral). Convolution of sequences is a product of Z-transforms on the intersection of ROCs. Multiplication by \(a^n\) scales the \(z\)-plane: \(a^n x[n]\leftrightarrow X(z/a)\). Differentiation: \(n x[n]\leftrightarrow -z\,dX/dz\). The unit circle \(z=e^{j\Omega}\) is the discrete-time Fourier axis; the DTFT exists as an ordinary function when the ROC includes \(|z|=1\).

Unilateral Z-transform sums from \(n=0\) to \(\infty\) and is the tool for recurrences with initial rest or with specified \(x[-1],x[-2],\ldots\). The delay rule then produces those initial samples: \(\mathcal{Z}\{x[n-1]\}=z^{-1}X(z)+x[-1]\), with a convention that \(X\) is unilateral. Signals courses that emphasize ROC use the bilateral transform for inversion problems and the unilateral transform for “solve the recurrence” problems.

Inversion methods: inspection and tables; partial fractions in \(z^{-1}\) or in \(z\); power series (long division) in the ROC; contour integrals (residues) \(x[n]=\frac{1}{2\pi j}\oint X(z)z^{n-1}dz\). For UG work, partial fractions plus the causal/anticausal pair is enough. Expand \(X(z)/z\) if using residues at poles of \(X(z)z^{n-1}\) for \(n\ge 0\), or expand in \(z^{-1}\) to read geometric series.

A discrete LTI system with impulse response \(h[n]\) has system function \(H(z)=\sum h[n]z^{-n}\). A recurrence \(\sum_{k=0}^{N} a_k y[n-k]=\sum_{m=0}^{M} b_m x[n-m]\) with zero initial rest has

\[
H(z)=\frac{\sum_m b_m z^{-m}}{\sum_k a_k z^{-k}}.
\]

Poles are the roots of the characteristic polynomial. FIR filters have \(H(z)\) a polynomial in \(z^{-1}\) (poles only at the origin, ROC \(\mathbb{C}\setminus\{0\}\)). IIR filters have poles of nonzero radius.

Causality: ROC of \(H\) is \(|z|>r\) including infinity, i.e. \(H\) proper as a function of \(z\) for causal rational systems of the usual type. BIBO stability: \(\sum |h[n]|<\infty\), equivalent to ROC of \(H\) including the unit circle. Causal and stable: all poles strictly inside the unit circle. Minimum-phase systems have poles and zeros inside the unit circle; they have a causal stable inverse.

Poles on the unit circle produce everlasting sinusoids or resonances and are not BIBO stable (simple poles on the circle with causal ROC give bounded but not absolutely summable \(h\), e.g. \(u[n]\)). Repeated poles on the circle produce ramps.

The relationship to Laplace: sampling \(x_c(t)\) with period \(T\) and taking the Z-transform of samples is not the same as substituting \(z=e^{sT}\) into a CT Laplace transform without accounting for aliasing (impulse invariance vs. bilinear maps appear in DSP electives). In this unit, treat \(z\) as native to sequences.

A rational \(X(z)\) is a ratio of polynomials in \(z\) or in \(z^{-1}\). Clearing negative powers by multiplying numerator and denominator by \(z^{N}\) moves poles at \(z=0\) into view. A pole at the origin corresponds to a delay (a factor \(z^{-1}\) in an FIR tap). A pole at infinity appears when the sequence is left-sided and grows toward negative time in a way that produces positive powers of \(z\).

The ROC cannot contain poles and is bounded by circles through poles (or 0 or \(\infty\)). After a pole-zero cancellation, a hole in the ROC may fill. Example: \(H(z)=(1-2z^{-1})/(1-2z^{-1})\) for \(z\neq 2\) is 1, ROC everything except possibly the cancelled point, and \(h[n]=\delta[n]\). Without cancellation language, one might think a pole at 2 remains.

Initial-value and final-value theorems exist for unilateral Z: \(x[0]=\lim_{z\to\infty}X(z)\) for causal sequences, and \(x[\infty]=\lim_{z\to 1}(1-z^{-1})X(z)\) if the limit exists, i.e. poles of \((1-z^{-1})X(z)\) lie inside the unit circle. Applying the final-value theorem to a causal oscillator \(1/(1-z^{-1}+z^{-2})\) is illegal.

Stability of a causal second-order real recurrence \(y[n]-2r\cos\theta\, y[n-1]+r^2 y[n-2]=x[n]\) is \(r<1\). The same characteristic polynomial with ROC \(|z|<r\) would be an anticausal system with poles outside if \(r>1\), which can be stable as a left-sided filter. Always pair the polynomial with an ROC.

Convolution of a right-sided sequence with a left-sided sequence can produce a two-sided result whose Z-transform ROC is the intersection, possibly empty. Empty intersection means the convolution sum diverges. That is the discrete analog of multiplying Laplace transforms whose strips miss each other.

Long division gives a series in the ROC direction: outside a circle, expand in \(z^{-1},z^{-2},\ldots\) matching \(n\ge 0\); inside, expand in \(z,z^2,\ldots\) matching \(n\le -1\) (and handle \(n=0\) separately). Doing division in the wrong direction is the usual inverse-Z disaster.

For a finite-length causal sequence of length \(L\), \(H(z)\) is a polynomial in \(z^{-1}\) of degree \(L-1\). All nonzero poles of an FIR filter in \(z^{-1}\) form are at the origin after writing as a function of \(z\). Zeros can sit anywhere; zeros on the unit circle produce exact nulls at those DT frequencies.

## Equations

Definition:

\[
X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n}, \qquad r_< < |z| < r_>.
\]

Causal geometric sequence:

\[
a^n u[n]\ \longleftrightarrow\ \frac{1}{1-az^{-1}},\quad |z|>|a|.
\]

Left-sided:

\[
-a^n u[-n-1]\ \longleftrightarrow\ \frac{1}{1-az^{-1}},\quad |z|<|a|.
\]

Convolution: \(x*h\leftrightarrow X(z)H(z)\) on \(\operatorname{ROC}_x\cap\operatorname{ROC}_h\).

Shift (bilateral): \(x[n-n_0]\leftrightarrow z^{-n_0}X(z)\).

DTFT when \(|z|=1\subset\mathrm{ROC}\): \(X(e^{j\Omega})=X(z)|_{z=e^{j\Omega}}\).

Inverse residue formula:

\[
x[n]=\frac{1}{2\pi j}\oint_C X(z)\,z^{n-1}\,dz,
\]

with \(C\) a counterclockwise contour in the ROC.

## Methods

Determine ROC from support before inverting. Sketch poles. Shade the annulus. Each pole contributes a causal term if the ROC is outside that pole’s radius and an anticausal term if the ROC is inside.

Partial fractions: write \(X(z)=\sum \frac{A_i}{1-p_i z^{-1}}\) (simple poles) plus a polynomial in \(z^{-1}\) if improper in \(z^{-1}\). Match coefficients, or use cover-up on \(X(z)/z\) in the \(z\)-plane form \(\sum A_i z/(z-p_i)\).

To solve a recurrence with rest IC, take unilateral Z, solve \(Y(z)\), invert as a causal sequence. To find \(h[n]\), set \(x=\delta\), equivalently invert \(H(z)\) with the ROC implied by causality if the filter is specified as running forward in \(n\).

Stability test for causal rational \(H\): pole magnitudes \(<1\). For a second-order real pole pair, the quadratic \(z^2-2r\cos\theta\, z+r^2\) needs \(r<1\).

Long division: if ROC is \(|z|>r\), divide so that the series in \(z^{-1}\) is obtained (negative powers). If ROC is \(|z|<R\), expand in positive powers of \(z\).

Check with a known value: \(X(\infty)=x[0]\) for a causal sequence (no positive powers of \(z\)).

To invert a quadratic factor, complete to \(1/(1-2r\cos\theta\, z^{-1}+r^2 z^{-2})\) and use the damped-cosine pair \(r^n \frac{\sin((n+1)\theta)}{\sin\theta}u[n]\) or the complex-pole pair. Matching a phase often needs a sine and a cosine term.

When a recurrence is run backward in \(n\) (anticausal implementation), you are choosing the interior ROC. Numerical instability of a causal implementation of a pole outside the unit circle becomes a stable anticausal implementation of that same pole, at the cost of storing the future. Offline IIR filtering of files sometimes uses exactly that split (forward–backward filtering for zero-phase IIR).

If a problem gives \(H(z)\) and “stable and causal,” you may mark poles inside the unit circle without computing \(h[n]\). If it gives only “stable,” you must consider left-sided inverses of exterior poles.

## Mistakes

Inverting \(1/(1-az^{-1})\) as \(a^n u[n]\) when the ROC is \(|z|<|a|\). The left-sided pair is required.

Using Laplace ROC strips (vertical) in the \(z\)-plane. Z-transform ROC is radial, an annulus.

Forgetting that a finite sequence starting at \(n=-2\) has a pole at infinity in some descriptions and a factor \(z^{2}\) in \(X(z)\).

Claiming FIR filters can be unstable. FIR with finite taps is always BIBO stable; the only “poles” are at 0.

Substituting \(z=e^{j\Omega}\) when the unit circle is not in the ROC and calling it a DTFT.

Dropping the minus in \(-a^n u[-n-1]\). That minus is required for the algebra to match.

Applying the delay property of the unilateral transform without adding the initial-condition terms.

Confusing \(u[-n]\) with \(u[-n-1]\). They differ at \(n=0\); the standard left-sided pair uses \(u[-n-1]\) so that the \(n=0\) term is not double-counted with the causal pair.

Writing \(H(z)=Y(z)/X(z)\) for a system with nonzero initial rest stored in delays; that ratio then depends on the input.

Taking pole radius equal to 1 as BIBO stable for a causal filter. Simple poles on the circle are not \(\ell^1\).

Using the unilateral delay rule on a bilateral sequence that is nonzero for \(n<0\), thereby deleting the past.

Writing ROC as \(\operatorname{Re}z> r\) (a Laplace strip habit). The Z-transform ROC is stated with modulus \(|z|\).

Inverting by residues while using a clockwise contour or forgetting the \(z^{n-1}\) factor, which shifts which poles contribute for \(n=0\).
