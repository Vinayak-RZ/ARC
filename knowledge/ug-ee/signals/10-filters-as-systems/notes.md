# Ideal filters, distortion, group delay

A filter is an LTI system used to reshape a spectrum. Ideal filters in a signals course are brick-wall frequency responses: gain constant on a passband, exactly zero on a stopband, with a specified linear phase or zero phase. They are noncausal and unrealizable as analog lumped circuits, but they are the reference against which delay, distortion, and practical approximations are judged. This unit defines ideal lowpass, highpass, bandpass, and bandstop responses, then introduces magnitude distortion, phase distortion, group delay, and the distortionless-transmission condition.

## Concepts

Distortionless transmission means the output is a scaled, delayed copy of the input: \(y(t)=K x(t-t_d)\) with \(K>0\) and \(t_d\) real. In the frequency domain that is \(H(j\omega)=K e^{-j\omega t_d}\) at every frequency where \(X(j\omega)\) has energy. Magnitude is constant; phase is linear through the origin (or affine with an integer number of \(2\pi\) wraps that still correspond to a pure delay on a given band). If the input is bandlimited, it is enough that this identity hold on the support of \(X\).

Magnitude (amplitude) distortion occurs when \(|H(j\omega)|\) is not constant on the band of interest. Different frequency components are then amplified differently. A non-flat loudspeaker or a Chebyshev passband ripple is magnitude distortion. An equalizer tries to undo it.

Phase distortion occurs when \(\arg H(j\omega)\) is not linear in \(\omega\). Components slip relative to each other even if the magnitude is flat. A picture that makes this concrete is a square wave through an allpass filter with nonlinear phase: harmonic phases move, the time waveform changes shape, the spectrum magnitudes may stay the same. Human hearing is relatively insensitive to some phase changes; image and pulse systems are not. Communications pulse shapes care about both.

Phase delay at a frequency \(\omega_0\) is \(t_p(\omega)=-\theta(\omega)/\omega\) where \(H=|H|e^{j\theta}\). It is the delay of a everlasting cosine at that frequency, in the sense that \(K\cos(\omega t+\theta)=K\cos\bigl(\omega(t-t_p)\bigr)\). Group delay is \(t_g(\omega)=-d\theta/d\omega\). It is the delay of the envelope of a narrowband packet centered at \(\omega\). For a pure delay \(H=e^{-j\omega t_d}\), both \(t_p\) and \(t_g\) equal \(t_d\). When \(\theta(\omega)\) is nonlinear, a pulse envelope can arrive at a different time than the carrier phase, and different packets at different center frequencies disperse. That dispersion is group-delay distortion.

Ideal lowpass: \(H_{\mathrm{lp}}(j\omega)=e^{-j\omega t_d}\) for \(|\omega|<\omega_c\) and \(0\) for \(|\omega|>\omega_c\) (sometimes a specified gain \(K\)). The impulse response is a shifted sinc, infinite in both time directions unless \(t_d\to\infty\), hence noncausal. Ideal highpass is \(1-H_{\mathrm{lp}}\) in the zero-delay case, or more carefully \(e^{-j\omega t_d}\) outside the stopband. Ideal bandpass passes an interval \([\omega_1,\omega_2]\) and its negative counterpart for real filters. Ideal bandstop is the complement. Real analog filters cannot have jump discontinuities in \(H(j\omega)\) if they are rational and stable; the Gibbs-like transition must occupy a finite band. Paley–Wiener-type constraints also forbid a causal stable filter from being exactly zero on a frequency interval of positive length while remaining square-integrable in a certain sense; the ideal stopband is a limit.

Generalized linear phase: \(\theta(\omega)=-\alpha\omega+\beta\) on the passband, with \(\beta=0\) or \(\beta=\pm\pi/2\) common (the latter for differentiators or Hilbert transformers). FIR filters can have exact generalized linear phase if the tap vector is symmetric or antisymmetric. IIR analog filters cannot have exact linear phase over a band except in trivial cases; they approximate constant group delay (Bessel) or ignore delay and optimize magnitude (Butterworth, Chebyshev, elliptic). Those named approximations belong mostly to a circuits or DSP course; here the point is the specification, not the ladder network.

Allpass systems have \(|H(j\omega)|=1\) (or a constant) and nontrivial phase. They equalize group delay or independently set phase. A first-order analog allpass is \((s-a)/(s+a)\) with \(a>0\) up to a sign that keeps it causal and stable. Cascading allpass sections sculpts \(t_g(\omega)\).

A linear-phase FIR differentiator has antisymmetric taps and a \(j\omega\) magnitude in the passband, hence both a \(\pi/2\) intercept and a rising gain; it is not distortionless, by design. Calling every deviation from a pure delay “distortion” is correct only when the goal was distortionless transmission.

Nonlinear systems produce new frequencies (harmonics, intermodulation). That is nonlinear distortion and is not a group-delay topic. Keep the LTI hypothesis explicit.

Discrete-time ideal filters are \(2\pi\)-periodic in \(\Omega\). An ideal DT lowpass has passband \(|\Omega|<\Omega_c<\pi\) and stopband up to \(\pi\), then repeats. Sampling and digital filtering implement those responses; analog reconstruction still needs an analog image filter.

Bandwidth versus delay: a narrower passband typically produces a longer impulse response (time-frequency scaling of the sinc). An ideal LPF of cutoff \(\omega_c\) has mainlobe width on the order of \(2\pi/\omega_c\). You cannot have arbitrarily sharp frequency cuts and arbitrarily short \(h(t)\) at once. Practical filters spend transition bandwidth to shorten ringing and to allow causality.

Causality plus a high-frequency gain that does not vanish too slowly constrains how much phase lag you must accept (Bode gain–phase relations). A minimum-phase system has the least group delay among systems with a given magnitude response and a causal stable inverse. Non-minimum-phase zeros (right half-plane zeros, or zeros outside the unit circle) add extra delay without changing \(|H|\). That extra delay is visible as a precursor-free but stretched tail in analog filters, or as zeros that a linear-phase FIR would have reflected outside the circle if one forced a given magnitude.

Pulse distortion is often specified as overshoot, rise time, and ringing period. Rise time tracks the inverse of bandwidth. Overshoot and ringing track both the sharpness of the cutoff and the group-delay peak near the band edge. Bessel (maximally flat delay) analog filters exist to keep \(t_g\) flat at the expense of a slower magnitude cutoff. Butterworth is maximally flat magnitude, not maximally flat delay.

An ideal Hilbert transformer and an ideal differentiator are filters with specified magnitude and phase, not distortionless channels. Passing a cosine through a Hilbert transformer yields a sine (a \(\pi/2\) phase shift) without changing amplitude; that is the mechanism behind SSB and envelope extraction via the analytic signal.

Group delay of a cascade of LTI stages adds. Magnitude responses multiply. An equalizer that flattens \(t_g\) is often an allpass cascade, leaving \(|H|\) untouched. An equalizer that flattens \(|H|\) is a magnitude equalizer and generally changes \(t_g\). Doing both is a joint approximation problem.

For a real FIR linear-phase filter of odd length and even symmetry, \(H(e^{j\Omega})=A(\Omega)e^{-j\Omega M/2}\) with \(A(\Omega)\) real and even. Zeros of \(A\) inside the passband create \(\pi\) phase jumps if \(A\) changes sign; some authors still call this generalized linear phase. A passband zero is usually a design defect for a “flat delay” data filter.

## Equations

Distortionless:

\[
H(j\omega)=K e^{-j\omega t_d} \quad\text{on the support of }X, \qquad y(t)=K x(t-t_d).
\]

Phase and group delay, \(\theta(\omega)=\arg H(j\omega)\):

\[
t_p(\omega)=-\frac{\theta(\omega)}{\omega}, \qquad t_g(\omega)=-\frac{d\theta}{d\omega}.
\]

Ideal delay: \(t_p(\omega)=t_g(\omega)=t_d\).

Ideal LPF impulse response (gain 1, delay \(t_d\), cutoff \(\omega_c\)):

\[
h(t)=\frac{\omega_c}{\pi}\operatorname{sinc}\Bigl(\frac{\omega_c}{\pi}(t-t_d)\Bigr)
\]

with \(\operatorname{sinc}\theta=\sin(\pi\theta)/(\pi\theta)\).

Cascade: group delays add when magnitudes multiply (LTI cascade): \(t_g^{\mathrm{tot}}=t_{g1}+t_{g2}\).

Allpass first-order analog (causal stable, \(a>0\)):

\[
H(s)=\frac{a-s}{a+s}, \qquad |H(j\omega)|=1, \qquad t_g(\omega)=\frac{2a}{a^2+\omega^2}.
\]

Hilbert transformer (ideal): \(H(j\omega)=-j\operatorname{sgn}(\omega)\) (up to a delay), magnitude 1, phase \(-\pi/2\) on \(\omega>0\).

## Methods

To test distortionless transmission, write \(H(j\omega)\) in polar form on the input band. Check constant \(|H|\) and linear \(\theta(\omega)=-\omega t_d+\beta\) with \(\beta\) compatible with a real delay (usually \(\beta=0\) or a frequency-independent sign). If the input is a single cosine, constant group delay is invisible; use at least two frequencies or a pulse.

To compute group delay from a rational \(H(j\omega)\), write \(\theta=\Im\log H\), or use

\[
t_g(\omega)=-\Im\Bigl\{\frac{1}{H}\frac{dH}{d\omega}\Bigr\}
\]

carefully with a continuous phase branch. For FIR linear phase, read \(t_d=(N-1)/2\) samples from the tap length \(N\) when symmetry holds.

To sketch an ideal filter output, pass each Fourier component that lies in the passband with the specified delay and kill the rest. For a periodic input, keep harmonics with \(|k\omega_0|<\omega_c\).

When comparing two filters with the same \(|H|\) and different \(\theta\), look at a time-domain pulse: ringing, precursor (noncausal), and asymmetric tails are phase effects as well as bandwidth effects.

For DT, replace \(\omega\) by \(\Omega\), remember periodicity, and measure delay in samples. A linear-phase FIR of length \(M+1\) (order \(M\)) with even symmetry has delay \(M/2\) samples.

To check distortion of a square wave, keep the harmonic amplitudes if \(|H|\) is flat and watch relative harmonic phases. If the 3rd harmonic slips by \(\pi\) relative to the fundamental, the waveform can invert its peak shape. Computing a few partial sums makes the point without a full inverse transform.

When \(H(j\omega)\) is given as a real even function (zero phase), the impulse response is even: a noncausal smoother. Adding a bulk delay \(e^{-j\omega t_d}\) with \(t_d\) larger than the practical support of the truncated sinc produces an approximately causal FIR. That is the usual window method in DSP, viewed from this unit as “ideal LPF times a delay.”

## Mistakes

Calling constant group delay the same as zero delay. A long cable can have large flat \(t_g\) and still be distortionless.

Using phase delay and group delay interchangeably for broadband pulses.

Expecting a causal analog Butterworth filter to have linear phase. Its \(t_g(\omega)\) peaks near the cutoff.

Treating an ideal LPF as causal because “it only removes high frequencies.” The sinc has tails for \(t<0\).

Forgetting negative frequencies in real bandpass specifications; a real filter’s \(H(j\omega)\) must satisfy Hermitian symmetry.

Adding phase delays instead of group delays when cascading. Phases add; group delays (derivatives) add; phase delays \(-\theta/\omega\) do not add in a simple way.

Plotting \(\arg H\) with jumps of \(2\pi\) and differentiating through the jump, producing fake impulses in \(t_g\). Unwrap phase first; true discontinuities of \(\pi\) at real-axis zeros are real and do affect delay.

Claiming FIR filters always have linear phase. Only symmetric or antisymmetric taps do.

Using \(|H(j\omega)|=0\) on a band as a causal stability-compatible exact spec without acknowledging it is an idealization.

Measuring delay from the first nonzero sample of a causal \(h[n]\) and calling it group delay. That is support delay, not \(t_g(\Omega)\) at a passband frequency.
