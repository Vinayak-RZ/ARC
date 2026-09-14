# CTFT and properties, Parseval

The continuous-time Fourier transform (CTFT) represents an aperiodic finite-energy signal as an integral of complex exponentials \(e^{j\omega t}\) over a continuum of frequencies. Where the Fourier series used a discrete harmonic grid, the transform uses a density \(X(j\omega)\). The same object, interpreted in the sense of distributions, also handles everlasting sinusoids and constants as impulses in frequency. This unit states the pair, the algebraic properties used constantly in later units, and Parseval’s energy identity.

## Concepts

For an absolutely integrable signal the analysis integral

\[
X(j\omega)=\int_{-\infty}^{\infty}x(t)e^{-j\omega t}\,dt
\]

converges uniformly to a continuous bounded function of \(\omega\). Square-integrable signals have a transform in \(L^2\) (Plancherel). Many engineering signals are neither: a unit step, a sinusoid, a signum, a ramp. Those are handled with distributions (impulses, principal values) or as limits of damped exponentials. Undergraduate tables list both ordinary and impulsive transforms; using a table entry without noting the sense is a common source of paradoxes (the transform of \(1\) is \(2\pi\delta(\omega)\), not zero).

The inverse

\[
x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(j\omega)e^{j\omega t}\,d\omega
\]

puts the \(2\pi\) on the synthesis side. Some authors write frequency in hertz and move \(2\pi\) differently; some put \(1/\sqrt{2\pi}\) on both sides. This handbook uses radian frequency and the asymmetric \(2\pi\) in the inverse.

Duality: if \(x(t)\leftrightarrow X(j\omega)\), then \(X(jt)\leftrightarrow 2\pi x(-\omega)\) in this convention. Duality explains why a rectangle in time is a sinc in frequency and a rectangle in frequency is a sinc in time. Time scaling \(x(at)\) becomes \(\frac{1}{|a|}X(j\omega/a)\): compression in time expands frequency. A time shift multiplies by \(e^{-j\omega t_0}\) and does not change \(|X|\). A frequency shift \(e^{j\omega_0 t}x(t)\) translates \(X(j(\omega-\omega_0))\); that is complex baseband modulation.

Differentiation in time multiplies by \(j\omega\). Differentiation in frequency multiplies by \(-jt\) on the time side. Integration in time divides by \(j\omega\) and adds a possible \(\pi X(0)\delta(\omega)\) term tracking accumulated DC. Convolution in time is multiplication in frequency: \(x*h\leftrightarrow X(j\omega)H(j\omega)\). Multiplication in time is convolution in frequency with a \(1/(2\pi)\) factor: \(x(t)y(t)\leftrightarrow\frac{1}{2\pi}X*Y\). These two theorems are why LTI filtering is a product of transforms and why a time window smears a spectrum.

Parseval (energy):

\[
\int_{-\infty}^{\infty}|x(t)|^2\,dt=\frac{1}{2\pi}\int_{-\infty}^{\infty}|X(j\omega)|^2\,d\omega.
\]

The quantity \(|X(j\omega)|^2/(2\pi)\) is an energy spectral density. For power signals one uses a power spectral density from a truncated-window limit; that is a different object (Wiener–Khinchin in a later stochastic course). Do not apply the energy Parseval to an everlasting cosine without first windowing or using impulsive spectra carefully: the left side diverges.

Hermitian symmetry: real \(x\) implies \(X(-j\omega)=X^*(j\omega)\). Even real signals have real even transforms; odd real signals have purely imaginary odd transforms. Causality plus reality imposes Kramers–Kronig relations between the real and imaginary parts of \(X(j\omega)\) (or of a stable causal \(H(j\omega)\)); the undergraduate form is that the real part determines the imaginary part via a Hilbert transform when \(H\) is analytic in the right half-plane.

Standard pairs worth memorizing: \(\operatorname{rect}(t/\tau)\leftrightarrow \tau\operatorname{sinc}(\omega\tau/(2\pi))\) with a stated sinc convention; \(e^{-at}u(t)\leftrightarrow 1/(a+j\omega)\) for \(a>0\); \(e^{-a|t|}\leftrightarrow 2a/(a^2+\omega^2)\); \(\delta(t)\leftrightarrow 1\); \(1\leftrightarrow 2\pi\delta(\omega)\); \(\operatorname{sgn}(t)\leftrightarrow 2/(j\omega)\) as a principal value; \(u(t)\leftrightarrow \pi\delta(\omega)+1/(j\omega)\); \(\cos(\omega_0 t)\leftrightarrow\pi\bigl(\delta(\omega-\omega_0)+\delta(\omega+\omega_0)\bigr)\).

The relationship to CTFS: a single pulse \(p(t)\) with transform \(P(j\omega)\), repeated every \(T_0\), has series coefficients \(a_k=\frac{1}{T_0}P(jk\omega_0)\). Sampling the transform of one period (or of one pulse) at harmonic frequencies yields the series. Conversely, the CTFT of a periodic signal is an impulse train with weights \(2\pi a_k\) at \(\omega=k\omega_0\).

Units: if \(x(t)\) is in volts and \(t\) in seconds, \(X(j\omega)\) is in volt-seconds (volts per hertz if \(f\) is used). Keeping dimensions prevents dropping \(2\pi\).

The Fourier transform is a change of orthonormal basis, not a magician. Time localization and frequency localization trade off: a short pulse has a wide sinc; a long pulse has a narrow sinc. The product of RMS durations (with a stated definition) has a lower bound of the same family as Heisenberg’s inequality. Windowing a long record to compute a spectrum is therefore a design choice: the window’s transform convolves with the true spectrum (multiplication theorem) and smears lines.

Uniqueness: if two \(L^1\) functions have the same transform, they are equal almost everywhere. At a jump, the inverse integral converges to the average, just as a Fourier series does. Point values of \(x\) at discontinuities are not what the inverse “means.”

Analyticity: an exponentially decaying causal signal has a transform that extends to a half-plane as a Laplace transform. Compactly supported time signals have entire transforms (Paley–Wiener), which cannot be zero on an interval unless the signal is identically zero. That is why ideal bandlimited interpolation uses infinite sinc tails, and why causal ideal brick-wall filters are impossible.

Tables disagree about the sign in the analysis exponent and about \(f\) versus \(\omega\). Before combining two table entries, confirm the pair. Mixing a \(+j\omega t\) analysis exponent with a handbook inverse that also uses \(+j\omega t\) will conjugate every result.

A periodic signal’s transform is an impulse train. Multiplying that train by a frequency response \(H(j\omega)\) is harmonic filtering. Convolving a pulse transform with an impulse train is the Poisson summation picture of sampling. These distribution identities are the same Poisson formula written in two domains.

If \(x(t)\) is real and even, computing \(X(j\omega)=2\int_0^{\infty}x(t)\cos(\omega t)\,dt\) halves the work. If it is real and odd, \(X(j\omega)=-2j\int_0^{\infty}x(t)\sin(\omega t)\,dt\). Use those shortcuts on rect, triangle, and signum-type problems.

Numerical DFT approximations of a CTFT require a time step, a window length, and a statement of which frequency grid was used. They belong after sampling theory. In this unit, exact pairs and properties are the intended tools.

## Equations

Forward and inverse CTFT:

\[
X(j\omega)=\int_{-\infty}^{\infty}x(t)e^{-j\omega t}\,dt, \qquad
x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(j\omega)e^{j\omega t}\,d\omega.
\]

Linearity, shift, scale:

\[
ax+by\leftrightarrow aX+bY, \qquad
x(t-t_0)\leftrightarrow e^{-j\omega t_0}X(j\omega), \qquad
x(at)\leftrightarrow\frac{1}{|a|}X\Bigl(\frac{j\omega}{a}\Bigr).
\]

Modulation and convolution:

\[
e^{j\omega_0 t}x(t)\leftrightarrow X\bigl(j(\omega-\omega_0)\bigr), \qquad
(x*h)(t)\leftrightarrow X(j\omega)H(j\omega),
\]

\[
x(t)y(t)\leftrightarrow\frac{1}{2\pi}\int_{-\infty}^{\infty}X(j\theta)Y\bigl(j(\omega-\theta)\bigr)\,d\theta.
\]

Parseval / Plancherel:

\[
\langle x,y\rangle=\frac{1}{2\pi}\langle X,Y\rangle, \qquad
E_x=\frac{1}{2\pi}\int |X(j\omega)|^2\,d\omega.
\]

Differentiation:

\[
\dot x(t)\leftrightarrow j\omega X(j\omega), \qquad
-jt\,x(t)\leftrightarrow \frac{d}{d\omega}X(j\omega).
\]

Duality (this convention): \(X(jt)\leftrightarrow 2\pi x(-\omega)\).

## Methods

To compute a transform from the definition, insert the formula, split at breakpoints, and integrate exponentials. For \(e^{-at}u(t)\) the integral is \(1/(a+j\omega)\) when \(\operatorname{Re}a>0\). For a pulse, the integral is a difference of exponentials that rearranges into a sinc.

To invert, prefer tables and properties over contour integrals unless a Laplace ROC problem is already in play. Partial fractions of a rational \(X(j\omega)\) that came from a causal stable transform invert as causal exponentials. If poles sit on the \(j\omega\) axis, add the impulsive DC terms from the table.

Property-first solutions: a triangular pulse is a rectangle convolved with itself, so its transform is a squared sinc. A delayed pulse only needs a phase factor. A cosine times a pulse is a pair of shifted pulse spectra, each of half amplitude.

Energy in a frequency band: if a problem asks for the energy in \(|\omega|<\omega_c\) and \(X\) is known, integrate \(|X|^2/(2\pi)\) over that band. If \(x\) is real, the spectrum is even in magnitude and one may double a one-sided integral.

To relate series and transform, compute \(P(j\omega)\) of one pulse, then sample. Check \(a_0\) against the pulse area over \(T_0\).

When a signal is neither \(L^1\) nor \(L^2\), introduce a convergence factor \(e^{-\varepsilon|t|}\), transform, and let \(\varepsilon\downarrow 0\) in the distribution sense. That is how \(u(t)\) acquires \(\pi\delta(\omega)\).

Energy in a frequency band is not the energy of the bandlimited projection unless you also remove the complementary band. Parseval applied to \(H(j\omega)X(j\omega)\) with an ideal LPF \(H\) is the correct energy after filtering.

If a problem asks for \(x(0)\) from \(X\), the inversion integral at \(t=0\) is \(\frac{1}{2\pi}\int X(j\omega)\,d\omega\), which is also related to the area of the spectrum. Conversely \(X(0)=\int x(t)\,dt\), the area in time. Those two area identities are the \(k=0\) Fourier-series statements in the aperiodic limit.

Differentiation under the integral to obtain \(j\omega X\) requires domination or distributional interpretation when \(x\) has jumps: the derivative then includes impulses, and \(j\omega X\) still holds in the distribution sense.

## Mistakes

Dropping the \(2\pi\) in Parseval or in the multiplication theorem. Convolution in frequency carries \(1/(2\pi)\) in this convention.

Using \(f\) in hertz inside a formula written for \(\omega\), or writing \(X(f)=\int x(t)e^{-j\omega t}dt\) with mixed symbols.

Applying \(X(j\omega)=1/(a+j\omega)\) to \(e^{-at}u(t)\) when \(a\le 0\). The analysis integral then diverges; the two-sided Laplace ROC is the right language.

Treating \(\operatorname{sinc}\) without defining \(\sin(\pi\theta)/(\pi\theta)\) versus \(\sin\theta/\theta\). State the convention when a numerical zero location is required.

Inverting \(j\omega X(j\omega)\) as \(x(t)\) instead of \(\dot x(t)\).

Forgetting Hermitian symmetry and producing a complex time signal from a “real” odd magnitude model.

Using energy Parseval on a periodic signal without converting to power / impulse trains.

Writing the transform of \(\delta(t-t_0)\) as \(\delta(\omega-\omega_0)\). The correct pair is \(e^{-j\omega t_0}\).

Confusing \(X(j\omega)\) with a Laplace \(X(s)\) evaluated at \(s=j\omega\) when the ROC does not include the axis. The Fourier transform may fail to exist even if a Laplace transform does.

Sign errors in modulation: \(e^{+j\omega_0 t}\) shifts \(X\) to the right by \(\omega_0\).

Calling \(\operatorname{rect}\) and \(\operatorname{sinc}\) a pair without matching width parameters. If the time pulse has width \(\tau\), the first sinc zero sits at \(2\pi/\tau\) in \(\omega\) (or \(1/\tau\) in hertz), not always at \(1\).

Using duality twice and dropping the \(2\pi\) and the time reversal \(x(-\omega)\). Duality is the fastest way to get a triangle-frequency pair from a squared sinc in time, but the constants must be tracked.
