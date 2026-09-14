# Fourier analysis as mathematics for EE

Fourier methods in this pack are the analysis tools that circuit frequency response, signals courses, and introductory communications all share: trigonometric and complex Fourier series of periodic waveforms, the Fourier transform of an aperiodic finite-energy signal, orthogonality, Parseval, and the algebraic properties (linearity, delay, differentiation, modulation, convolution). Sampling and DFT numerics belong in the signals and DSP packs. This unit keeps the continuous-time mathematics and the EE examples that make the symbols worth learning: square waves on a DC bus, a single rectangular pulse, an exponential decay, and a cosine whose transform is a pair of impulses.

The Fourier transform is the Laplace transform on the \(j\omega\) axis when that restriction is legal (the \(j\omega\) axis lies in the ROC). A causal decaying exponential has both; a never-ending sinusoid has a Fourier transform in the impulse sense and no ordinary Laplace transform without a convergence factor. Knowing which object you are allowed to write is part of the mathematics.

## Concepts

A real signal \(x(t)\) with period \(T_0>0\) and fundamental frequency \(\omega_0=2\pi/T_0\) has a trigonometric series
\[
x(t)=a_0+\sum_{n=1}^\infty \big(a_n\cos n\omega_0 t + b_n\sin n\omega_0 t\big)
\]
under the usual Dirichlet conditions (piecewise smooth on a period; jump discontinuities allowed). The complex form
\[
x(t)=\sum_{n=-\infty}^\infty c_n e^{jn\omega_0 t},\qquad c_n=\frac{1}{T_0}\int_{T_0}x(t)e^{-jn\omega_0 t}\,dt
\]
is the one EE uses for phasor-like harmonics. For real \(x\), \(c_{-n}=c_n^*\), \(a_0=c_0\), \(a_n=c_n+c_{-n}\), \(b_n=j(c_n-c_{-n})\). A cosine of amplitude \(A\) at the \(k\)th harmonic corresponds to \(c_k=c_{-k}=A/2\). That factor of two is the most common coefficient error in the course.

Average power of a periodic signal (Parseval) is \(a_0^2+\tfrac12\sum(a_n^2+b_n^2)\) or \(\sum |c_n|^2\). Each harmonic contributes independently because the complex exponentials are orthogonal on a period. THD calculations in power electronics start from this identity, not from an empirical meter.

The Fourier transform of an aperiodic absolute-integrable signal is
\[
X(j\omega)=\int_{-\infty}^\infty x(t)e^{-j\omega t}\,dt,\qquad x(t)=\frac{1}{2\pi}\int_{-\infty}^\infty X(j\omega)e^{j\omega t}\,d\omega.
\]
Sign conventions and \(2\pi\) placement differ (Hz versus rad/s, unitary versus angular). This pack uses the angular-frequency pair above, matching most UG EE signals books that write \(X(j\omega)\). Duality then has a \(2\pi\) in one direction. Frequency in hertz \(f=\omega/2\pi\) moves the \(2\pi\) onto the other integral. State which pair you are using before copying a table row from another document.

A rectangular pulse of width \(\tau\) and height \(A\) centred at the origin transforms to \(A\tau\operatorname{sinc}(\omega\tau/2\pi)\) or \(A\tau\sin(\omega\tau/2)/(\omega\tau/2)\), depending on the sinc normalisation. The zeros of the spectrum lie at \(f=k/\tau\), \(k\neq 0\). That pattern is the mathematics behind the spectrum of a switching waveform’s one-shot and behind aperture effects.

Differentiation in time multiplies \(X(j\omega)\) by \(j\omega\). Integration divides by \(j\omega\) plus an impulse at \(\omega=0\) to account for any DC that integration would ramp. Delay \(x(t-t_0)\) multiplies the transform by \(e^{-j\omega t_0}\), a linear phase. Modulation \(x(t)\cos\omega_c t\) copies the spectrum to \(\pm\omega_c\) and halves it. Convolution in time is multiplication in frequency; multiplication in time is convolution in frequency (with a \(1/2\pi\) for the angular pair). These theorems are the same list as Laplace, restricted to \(s=j\omega\), plus the two-sided time axis.

Parseval for Fourier transforms (energy):
\[
\int |x(t)|^2 dt = \frac{1}{2\pi}\int |X(j\omega)|^2 d\omega.
\]
Energy spectral density is \(|X(j\omega)|^2/2\pi\) in this normalisation. Rayleigh’s theorem is the same statement. Power signals (eternal sinusoids, periodic waves) do not have finite energy; they use power spectral density and Fourier series or Fourier transforms with impulses.

Gibbs phenomenon: truncated Fourier series of a jump overshoots by about 9 percent of the jump, independent of the number of terms, with the ringing squeezing toward the discontinuity. In power-electronics PWM reconstruction and in brick-wall truncation of spectra, Gibbs is the mathematical name of the ringing, not a lab artefact.

Even and odd extensions determine cosine-only or sine-only series. A square wave that is odd about \(t=0\) has only sine terms (or only odd-\(n\) imaginary \(c_n\)). Choosing the time origin to make a waveform even saves half the integrals. Shifting the origin later is a delay theorem, not a new expansion.

The Dirac impulse \(\delta(t)\) transforms to \(1\). A constant \(A\) transforms to \(2\pi A\delta(\omega)\). A cosine \(A\cos\omega_0 t\) transforms to \(\pi A[\delta(\omega-\omega_0)+\delta(\omega+\omega_0)]\). These distributional identities are required as soon as a DC offset or a pure tone appears in the same problem as an energy signal. They are not optional advanced topics.

Orthogonality of \(\{e^{jn\omega_0 t}\}\) on \([0,T_0]\) is the reason a linear time-invariant circuit in sinusoidal steady state can be solved one harmonic at a time and the outputs added. Superposition is not a new circuit theorem here; it is orthogonality plus linearity.

A Fourier series of a periodic pulse train, taken to the limit of period \(\to\infty\) with pulse shape fixed, becomes the Fourier transform of one pulse. That limiting argument is the conceptual bridge between the two tools. The line spectrum \(c_n\) with spacing \(\omega_0\) densifies into \(X(j\omega)\,d\omega/2\pi\).

## Equations

Period \(T_0\), \(\omega_0=2\pi/T_0\):

\[
c_n=\frac{1}{T_0}\int_{t_0}^{t_0+T_0}x(t)e^{-jn\omega_0 t}\,dt,\qquad a_0=c_0,\ a_n=2\operatorname{Re}c_n,\ b_n=-2\operatorname{Im}c_n
\]
for real \(x\) (with the usual identification \(a_n=c_n+c_{-n}\)).

Parseval (periodic, average power):

\[
\frac{1}{T_0}\int_{T_0}|x|^2 dt = \sum_{n=-\infty}^\infty |c_n|^2.
\]

Fourier transform pair (angular, non-unitary):

\[
X(j\omega)=\int_{-\infty}^\infty x(t)e^{-j\omega t}\,dt,\qquad x(t)=\frac{1}{2\pi}\int_{-\infty}^\infty X(j\omega)e^{j\omega t}\,d\omega.
\]

Rect pulse, \(x(t)=A\) for \(|t|<\tau/2\), else 0:

\[
X(j\omega)=A\tau\frac{\sin(\omega\tau/2)}{\omega\tau/2}=A\tau\operatorname{sinc}\Big(\frac{\omega\tau}{2\pi}\Big)
\]
when \(\operatorname{sinc}(u)=\sin(\pi u)/(\pi u)\). State the sinc convention.

Two-sided exponential \(e^{-a|t|}\) (\(a>0\)):

\[
X(j\omega)=\frac{2a}{a^2+\omega^2}.
\]

Causal exponential \(e^{-at}u(t)\) (\(a>0\)):

\[
X(j\omega)=\frac{1}{a+j\omega}.
\]

Properties:

\[
x(t-t_0)\leftrightarrow e^{-j\omega t_0}X(j\omega),\qquad \frac{dx}{dt}\leftrightarrow j\omega X(j\omega),
\]
\[
x(t)\cos\omega_c t \leftrightarrow \tfrac12\big(X(j(\omega-\omega_c))+X(j(\omega+\omega_c))\big),
\]
\[
x*h \leftrightarrow X(j\omega)H(j\omega).
\]

Distributional pairs:

\[
1 \leftrightarrow 2\pi\delta(\omega),\qquad \cos\omega_0 t \leftrightarrow \pi\big(\delta(\omega-\omega_0)+\delta(\omega+\omega_0)\big).
\]

## Methods

For a periodic waveform, first state \(T_0\) and \(\omega_0\). Sketch one period and decide even/odd. Integrate \(c_n\) or \(a_n,b_n\) on the simplest period interval. Factor \(e^{-j n \omega_0 t_d}\) if the waveform is a delayed version of a standard pulse. Check \(c_0\) as the average value by geometry (area over period) rather than by taking \(n\to 0\) carelessly in a formula that had \(n\) in a denominator; take the limit or compute the average separately.

To invert a finite harmonic list, write the cosine form \(2|c_n|\cos(n\omega_0 t+\arg c_n)\) for each positive \(n\) and add \(c_0\). That is the waveform a spectrum analyser’s line list corresponds to.

For Fourier transforms, exploit even/odd: even \(x\) gives a real even \(X\); odd \(x\) gives a purely imaginary odd \(X\). Use known pairs and theorems rather than integrating from scratch. A triangular pulse is the convolution of two rects, hence a sinc squared. A delayed rect is a rect times \(e^{-j\omega t_0}\).

When both a DC offset and an AC burst appear, split the signal, transform each piece, add. Superposition holds for the transform as a linear operator.

To apply Parseval, decide energy versus power. A single pulse: energy, integrate \(|X|^2 d\omega/2\pi\). A periodic wave: power, sum \(|c_n|^2\). Mixing the two formulae produces a quantity with the wrong units.

If a problem asks for the output of an LTI filter with frequency response \(H(j\omega)\) and a periodic input, multiply each \(c_n\) by \(H(jn\omega_0)\) and invert the series. That is harmonic steady state, the Fourier-series version of phasors.

Truncation: a partial sum \(S_N\) is the inverse transform of the spectrum windowed by a rect in frequency, hence convolution with a sinc in time. Expect overshoot at jumps. Do not “fix” Gibbs by adding more terms in a plot of a jump; the overshoot percentage stays, the duration shrinks.

When relating Laplace and Fourier, check whether \(s=j\omega\) is free of poles on the axis. \(1/(s+a)\) for \(a>0\) becomes \(1/(a+j\omega)\). \(1/s\) is a step whose Fourier transform needs \(\pi\delta(\omega)+1/(j\omega)\). Do not write \(1/(j\omega)\) alone as the Fourier transform of \(u(t)\).

## Mistakes

Dropping the factor \(1/2\) on \(c_n\) for a cosine: \(A\cos\omega_0 t\) has \(c_{\pm 1}=A/2\), not \(A\).

Using \(a_0\) as the average and also writing \(a_0/2\) from an older trigonometric convention in the same problem. Pick one convention and stay with it. In the \(a_0+\sum(a_n\cos+b_n\sin)\) form used here, \(a_0\) is the average, not twice the average.

Confusing \(\operatorname{sinc}(u)=\sin(\pi u)/(\pi u)\) with \(\sin u/u\). The zeros and the scaling of a rect of width \(\tau\) move. Write the \(\sin(x)/x\) expression explicitly if unsure.

Applying the energy Parseval identity to a periodic power signal, or omitting \(1/2\pi\) in the angular-frequency energy identity.

Writing the Fourier transform of \(\cos\omega_0 t\) as a pair of finite lines without impulses, as if it were a series coefficient sitting in a continuous spectrum.

Using one-sided Laplace tables as Fourier tables for signals that are two-sided or that do not decay.

Forgetting conjugate symmetry: a real signal cannot have an arbitrary complex \(X(j\omega)\). If your integral produced a real odd \(X\) for an even real pulse, the \(j\) from \(e^{-j\omega t}\) was dropped.

Integrating a complex exponential over a period and getting \(T_0\) for \(n\neq 0\) because the \(n=0\) formula was used for all \(n\). Orthogonality says the integral is zero for \(n\neq 0\).

Shifting a waveform in time and changing \(|c_n|\) or \(|X(j\omega)|\). Delay affects phase only.

Treating THD as \(\sqrt{\sum_{n=2}^\infty |c_n|^2}/|c_1|\) with two-sided \(c_n\) double-counted, or mixing RMS of a sine (\(A/\sqrt{2}\)) with series coefficients inconsistently. For real periodic \(x\), RMS squared is \(\sum |c_n|^2\); the fundamental RMS is \(\sqrt{2}|c_1|\) when \(c_1=c_{-1}^*\).
