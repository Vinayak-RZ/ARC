# CTFS/DTFS and properties

A periodic signal that is reasonably well behaved can be written as a discrete superposition of harmonically related complex exponentials. That expansion is the Fourier series. In continuous time the harmonics are \(e^{jk\omega_0 t}\) with \(\omega_0=2\pi/T_0\). In discrete time a periodic sequence of period \(N\) has exactly \(N\) distinct harmonics, and the series is a finite sum (the discrete-time Fourier series, DTFS). This unit treats analysis and synthesis formulas, coefficient properties, and the link to LTI filtering of periodic inputs.

## Concepts

Let \(x(t)\) satisfy \(x(t+T_0)=x(t)\) for all \(t\), with fundamental frequency \(\omega_0=2\pi/T_0\). The trigonometric form uses \(\cos(k\omega_0 t)\) and \(\sin(k\omega_0 t)\). The complex form

\[
x(t)=\sum_{k=-\infty}^{\infty} a_k e^{jk\omega_0 t}
\]

is more compact and matches the eigenfunction language of LTI systems. The analysis integral

\[
a_k=\frac{1}{T_0}\int_{T_0}x(t)e^{-jk\omega_0 t}\,dt
\]

is the inner product against the \(k\)th harmonic, normalized so that the complex exponentials are orthonormal in \(L^2[0,T_0]\) after dividing by \(T_0\). Different authors put the \(1/T_0\) on the synthesis side instead; this handbook puts it on the analysis side, which makes \(a_0\) equal to the average value.

Dirichlet conditions are sufficient for pointwise convergence at points of continuity and to the midpoint of the jump at a discontinuity: over a period, \(x\) is absolutely integrable, has finitely many maxima and minima, and has finitely many finite jumps. Square-integrable periodic signals converge in \(L^2\); Gibbs ringing appears near jumps for partial sums. The series does not “fail” at a jump; it converges to the average of the left and right limits.

Real signals have Hermitian coefficients \(a_{-k}=a_k^*\). Even real signals have real \(a_k\) (cosine series). Odd real signals have purely imaginary, odd \(a_k\) (sine series). A time shift multiplies \(a_k\) by \(e^{-jk\omega_0 t_0}\). Differentiation multiplies \(a_k\) by \(jk\omega_0\). Integration divides by \(jk\omega_0\) for \(k\neq 0\) provided \(a_0=0\). Products of periodic signals with the same period correspond to discrete convolution of coefficient sequences. Periodic convolution of two signals of period \(T_0\) corresponds to \(T_0 a_k b_k\) in this normalization.

Parseval’s relation for the power of a periodic signal is \(P_x=\sum_k |a_k|^2\) with the analysis-side \(1/T_0\) used here. Equivalently \(P_x=\frac{1}{T_0}\int_{T_0}|x|^2\). Harmonic power is a budget: filtering that kills a coefficient subtracts \(|a_k|^2\) from the total power.

A periodic pulse train of pulses of width \(\tau\) and height \(A\) has a sinc envelope of coefficients. A full-wave rectified sinusoid has only even or only certain harmonics depending on the period chosen. Choosing the wrong \(T_0\) (an integer multiple of the fundamental) merely inserts zero coefficients between the true harmonics; the waveform is still expanded correctly, but the indexing is not fundamental.

Discrete-time periodic sequences with period \(N\) live on a circle of \(N\) points. There are only \(N\) distinct frequencies \(2\pi k/N\) for \(k=0,\ldots,N-1\), because \(e^{j2\pi(k+N)n/N}=e^{j2\pi kn/N}\). The DTFS is therefore a finite invertible transform:

\[
x[n]=\sum_{k=\langle N\rangle} a_k e^{j2\pi kn/N}, \qquad
a_k=\frac{1}{N}\sum_{n=\langle N\rangle}x[n]e^{-j2\pi kn/N}.
\]

Again the \(1/N\) may be moved. The DFT is the same pair on one period, usually with the \(1/N\) on the inverse transform in signal-processing libraries. DTFS coefficients are themselves periodic with period \(N\).

An LTI system driven by a periodic input in the steady state (when BIBO stable) produces a periodic output whose coefficients are \(b_k=H(jk\omega_0)a_k\) in CT, or \(b_k=H(e^{j2\pi k/N})a_k\) in DT. That is harmonic steady-state analysis: each eigenfunction is scaled by the frequency response. Unstable poles on the harmonic grid make the formula illegal.

DC, RMS of a sinusoid, and THD are series facts. The DC term is \(a_0\). A single real cosine \(A\cos(\omega_0 t+\phi)\) has \(a_1=\frac{A}{2}e^{j\phi}\) and \(a_{-1}=\frac{A}{2}e^{-j\phi}\). RMS of a zero-mean periodic waveform is \(\sqrt{\sum_{k\neq 0}|a_k|^2}\) in this normalization. Distortion metrics compare leftover harmonic power to the fundamental.

Convergence rate tracks smoothness. A discontinuous periodic waveform has coefficients that decay like \(1/k\). A continuous waveform with a jump in the derivative (a triangular wave) decays like \(1/k^2\). Each extra derivative that exists and is of bounded variation buys another power of \(1/k\). That is why a truncated series looks acceptable for a sinusoid after one term and terrible for a square wave after three terms. Term-by-term differentiation of a series is legal when the resulting series still converges appropriately; differentiating a square-wave series produces a train of impulses whose coefficients do not decay.

The analysis integral can be taken over any interval of length \(T_0\). Shifting the interval multiplies each \(a_k\) by a consistent phase only if you also redefine the time origin; if you keep the same origin and merely move the integration window, the coefficients do not change, because you are still integrating one full period of a periodic integrand. Use the interval that makes the algebra shortest: a symmetric interval for even/odd functions, or \([0,T_0]\) when the formula is written with steps starting at zero.

Complex Fourier series are inner products on \(L^2[0,T_0]\). Completeness of the harmonic family is a theorem of analysis; engineering use is that piecewise smooth periodic signals are determined by \(\{a_k\}\). Two different piecewise smooth periodic signals cannot share all coefficients. Truncation, however, can make them look similar: a low-pass periodic signal is exactly a trigonometric polynomial.

A periodic train of impulses \(\sum_n \delta(t-nT_0)\) has \(a_k=1/T_0\) for every \(k\) (flat spectrum). That distributional series is the Poisson kernel for sampling theory. Ordinary functions that approximate the train (narrow tall pulses) have sinc envelopes that are almost flat out to \(1/\tau\).

Discrete-time Fourier series hide a 2π-periodicity in the frequency index. Plotting \(a_k\) only for \(k=0,\ldots,N-1\) is complete; plotting through \(k=N\) repeats \(a_0\). Negative indices \(k=-1\) coincide with \(k=N-1\). Real even sequences have real even \(a_k\) on that circular axis.

When an LTI system is not stable, a periodic input can still produce a periodic particular solution plus natural modes. The “filter the harmonics” recipe is the particular solution, equal to the unique bounded steady state only when those modes decay. An ideal oscillator driven at its own frequency produces a resonant term \(t\sin(\omega_0 t)\) that is not periodic in the usual bounded sense.

## Equations

CTFS pair (this handbook’s normalization):

\[
a_k=\frac{1}{T_0}\int_{T_0}x(t)e^{-jk\omega_0 t}\,dt, \qquad
x(t)=\sum_{k=-\infty}^{\infty}a_k e^{jk\omega_0 t}, \qquad \omega_0=\frac{2\pi}{T_0}.
\]

Trigonometric conversion for real \(x\):

\[
x(t)=A_0+\sum_{k=1}^{\infty}\bigl(A_k\cos(k\omega_0 t)+B_k\sin(k\omega_0 t)\bigr),
\qquad
A_0=a_0,\quad a_k=\frac{A_k-jB_k}{2}\ (k>0).
\]

Parseval (power):

\[
\frac{1}{T_0}\int_{T_0}|x(t)|^2\,dt=\sum_{k=-\infty}^{\infty}|a_k|^2.
\]

Shift, scale, derivative:

\[
x(t-t_0)\leftrightarrow a_k e^{-jk\omega_0 t_0}, \qquad
\frac{dx}{dt}\leftrightarrow jk\omega_0 a_k.
\]

Rectangular pulse train, height \(A\), width \(\tau\), period \(T_0\):

\[
a_0=\frac{A\tau}{T_0}, \qquad
a_k=\frac{A\tau}{T_0}\operatorname{sinc}\Bigl(\frac{k\tau}{T_0}\Bigr)
\]

with \(\operatorname{sinc}\theta=\sin(\pi\theta)/(\pi\theta)\). Zeros of the envelope sit at \(k=T_0/\tau\) when that ratio is an integer.

DTFS pair:

\[
a_k=\frac{1}{N}\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}, \qquad
x[n]=\sum_{k=0}^{N-1}a_k e^{j2\pi kn/N}.
\]

LTI filtering of CT harmonics: \(b_k=H(j k\omega_0)\,a_k\).

## Methods

To compute CTFS coefficients, pick any convenient interval of length \(T_0\). Exploit even/odd symmetry to reduce to a cosine or sine integral. Use the pulse-train sinc formula when the waveform is a shifted rectangle; then apply the shift property.

To go from a trigonometric plot (a cosine of amplitude \(A\) and phase \(\phi\)) to complex coefficients, write \(A\cos(\theta)=\frac{A}{2}(e^{j\theta}+e^{-j\theta})\) and read \(a_{\pm 1}\).

Partial sums: if a problem asks for the RMS of the first \(M\) harmonics, sum \(|a_k|^2\) over those \(k\) (including negatives). Gibbs overshoot is about 9% of the jump and does not vanish with \(M\); only the \(L^2\) error and the width of the ringing shrink.

For DTFS, compute the finite sum directly for small \(N\). Use FFT mentally: a constant sequence has \(a_0\) equal to that constant (with \(1/N\) on analysis, \(a_0\) is the average, which equals the constant). An impulse train of period \(N\) that is \(N\delta[n \bmod N]\) has flat \(a_k=1\).

To filter a periodic input, evaluate \(H\) only at the harmonic frequencies that have nonzero \(a_k\). Do not integrate a Fourier transform of one period unless you are relating CTFS to CTFT of a windowed pulse (the coefficients sample the pulse transform, scaled).

When the period is ambiguous, state the fundamental. A square wave that already looks like period \(T\) might also be described with period \(2T\) if a hidden asymmetry is absent; extra coefficients then vanish.

A practical computation path for a piecewise polynomial period: integrate by parts, or differentiate until impulses appear, take the series of the impulses (easy), then divide coefficients by \(jk\omega_0\) the same number of times, fixing \(a_0\) from the average. That method is robust for sawtooth and trapezoid waves.

Check power two ways when the waveform is simple: time-average of \(x^2\) over a period versus \(\sum |a_k|^2\). Disagreement means a missed negative index or a wrong \(1/T_0\).

For DTFS, the FFT of one period is the fastest numerical path. Scale it to match the handbook’s \(1/N\) placement before comparing with a hand calculation of \(a_k\).

## Mistakes

Putting \(1/T_0\) on both analysis and synthesis, or on neither, and then using Parseval from a different book. Pick one pair and stay consistent.

Integrating over the wrong interval length, or using \(\omega_0=1/T_0\) without \(2\pi\).

Forgetting negative-index coefficients when computing power: \(|a_1|^2+|a_{-1}|^2=2|a_1|^2\) for a real cosine.

Using the CTFS of a non-periodic gated sinusoid. A finite burst is an energy signal; use the Fourier transform.

Claiming the series equals the jump value at a discontinuity. It equals the average of the limits.

Confusing DTFS with DTFT: the DTFT of a periodic sequence is an impulse train in frequency; the DTFS is the list of those impulse weights.

Applying \(H(j\omega)\) to a harmonic whose frequency is \(k\omega_0\) but writing \(H(jk)\) without \(\omega_0\).

Taking a full-wave rectified sine of a \(50\,\mathrm{Hz}\) sinusoid and assigning fundamental \(50\,\mathrm{Hz}\). The rectified waveform has fundamental \(100\,\mathrm{Hz}\).

Using circular identities for CTFS products without conjugating when energy (not coefficient convolution) is wanted.

Writing DTFS sums with infinite \(k\) as if discrete harmonics were not \(N\)-periodic.
