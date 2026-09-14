# Nyquist, aliasing, reconstruction

Sampling converts a continuous-time signal into a discrete-time sequence. Reconstruction tries to go back. The sampling theorem says that a signal whose Fourier transform vanishes outside \(|\omega|<\omega_m\) is determined by its values at uniform instants if the sampling rate exceeds \(2\omega_m\) (Nyquist rate in radians per second, or twice the highest hertz frequency). When that bandlimit fails, aliases fold into the baseband and no LTI interpolator can separate them. This unit treats ideal impulse sampling, the discrete-time sequence view, aliasing arithmetic, and ideal lowpass reconstruction, plus practical hold circuits at the level of a signals course.

## Concepts

Ideal impulse sampling forms the impulse train \(x_s(t)=x(t)p(t)\) with \(p(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT_s)\). In the frequency domain, multiplication by a periodic impulse train is convolution with another impulse train:

\[
X_s(j\omega)=\frac{1}{T_s}\sum_{k=-\infty}^{\infty}X\bigl(j(\omega-k\omega_s)\bigr), \qquad \omega_s=\frac{2\pi}{T_s}.
\]

Copies of \(X(j\omega)\) sit at every multiple of \(\omega_s\). If those copies do not overlap, a gain-\(T_s\) ideal lowpass filter with cutoff between \(\omega_m\) and \(\omega_s-\omega_m\) recovers \(X\) and therefore \(x\). The critical sampling frequency \(\omega_s=2\omega_m\) packs the copies edge to edge; an ideal brick-wall filter still works in the \(L^2\) sense if \(X\) has no energy at the single point \(\omega_m\), but any real filter needs a guard band. The Nyquist rate is \(2f_m\) samples per second when \(X(j2\pi f)=0\) for \(|f|>f_m\).

The sequence \(x[n]=x(nT_s)\) has DTFT \(X_d(e^{j\Omega})=\frac{1}{T_s}\sum_k X\bigl(j(\Omega/T_s-k\omega_s)/1\bigr)\) with \(\Omega=\omega T_s\). Discrete-time frequency is \(2\pi\)-periodic. The mapping \(\Omega=\omega T_s\) wraps CT frequencies that differ by \(\omega_s\) to the same \(\Omega\). That wrap is aliasing.

Aliasing arithmetic: a CT cosine at frequency \(f\) sampled at \(f_s\) is indistinguishable from a cosine at \(f+m f_s\) for any integer \(m\), and also from the folded frequency \(f_s-f\) with a possible sign (complex conjugate) on the negative image. The principal alias in \([-f_s/2,f_s/2]\) is obtained by subtracting multiples of \(f_s\) until the remainder lies in that interval, folding at \(\pm f_s/2\). A rotating phasor \(e^{j\omega t}\) sampled is \(e^{j\omega T_s n}\); it coincides with a lower-rate phasor when \(\omega T_s\) differs by a multiple of \(2\pi\).

Bandpass sampling (undersampling a bandpass signal whose energy lives in a higher Nyquist zone) can be legal if the zone copies tile without overlap. That is a specialized condition; the default UG statement is baseband: sample faster than twice the highest frequency, not twice the bandwidth, unless a bandpass hypothesis is explicit.

Reconstruction: the Whittaker–Shannon interpolator is

\[
x(t)=\sum_{n}x(nT_s)\operatorname{sinc}\Bigl(\frac{t-nT_s}{T_s}\Bigr)
\]

with \(\operatorname{sinc}\theta=\sin(\pi\theta)/(\pi\theta)\). Each sinc is the impulse response of the ideal lowpass filter, centered at a sampling instant. The interpolator is noncausal and infinite in time. Practical DACs use a zero-order hold (ZOH): hold \(x(nT_s)\) constant for \(T_s\) seconds. The ZOH frequency response is a sinc with linear phase; it droops in the baseband and images leak unless an analog reconstruction filter follows. A first-order hold connects samples with lines. Oversampling plus a mild analog filter is the usual engineering compromise.

Antialiasing filters analog-bandlimit \(x(t)\) before the sampler. Without them, energy above \(f_s/2\) folds in and cannot be removed later by a digital filter that sees only the aliases. The antialiasing cutoff is placed below \(f_s/2\) with a transition band that trades residual aliasing against passband delay.

Sampling is linear and time-varying as a map from CT to CT (impulse train modulation). As a map from CT to DT it is linear and not shift-invariant on the CT axis except for shifts that are integer multiples of \(T_s\). Reconstruction of the bandlimited subspace is a projection; sampling is invertible on that subspace and not invertible on all of \(L^2\).

Sinc interpolation at exactly the Nyquist rate is sensitive to phase: a sinusoid at \(f_s/2\) sampled at its zeros is the zero sequence. Strict inequality \(f_s>2f_m\) avoids that pathology for energy signals whose transform is supported on a closed interval inside \((-f_s/2,f_s/2)\).

Quantization, another operation in an ADC, is nonlinear and is not part of the classical sampling theorem. Finite wordlength is a later DSP unit. Clock jitter modulates sample instants and creates a noise-like error; UG treatment notes it as a perturbation of \(T_s\).

Bandlimitedness is a mathematical model. No nonzero finite-duration analog waveform is bandlimited in the Paley–Wiener sense. Laboratory “bandlimited” means “energy outside \(B\) is small compared with a stated tolerance.” Sampling then has a small alias residual rather than a theorem identity. Antialiasing filters make that residual a design parameter.

The spectrum copies in \(X_s(j\omega)\) have the same shape as \(X\), scaled by \(1/T_s\). If \(X\) already contains energy above \(\omega_s/2\), the copies overlap and addition (not a simple “fold a line”) occurs where they sit on top of each other. For a pair of discrete tones the addition is just two phasors in the same bin; for continuous spectra it is a density sum. You cannot uniquely undo a sum of two unknown pieces.

Downsampling a discrete sequence by an integer \(M\) is a second sampling operation: keep every \(M\)th sample. The DTFT is then an \(M\)-fold alias of the original DTFT. An integer upsampler inserting zeros is not interpolation; a following lowpass (the digital interpolation filter) is what reconstructs the in-between samples. Those multirate identities belong with DSP electives but explain why “sample then decimate” needs a digital antialias filter.

A cosine at frequency \(f_s/2\) sampled at instants \(nT_s\) is \((-1)^n\) times the value at \(t=0\). If that first sample is zero, every sample is zero. The theorem’s strict inequality avoids relying on a single phase.

Reconstruction error from ZOH can be computed in the frequency domain as the difference between \(T_s\operatorname{sinc}(\cdot)e^{-j\omega T_s/2}\) and the ideal brick wall of gain \(T_s\). Oversampling by \(L\) shrinks the analog images to neighborhoods of \(L f_s\) and flattens the sinc droop in the baseband, which is why audio DACs oversample.

If a problem gives \(x[n]=\cos(\Omega n)\) and asks for a possible analog \(x(t)\) at a given \(T_s\), infinitely many analog frequencies \(\Omega/T_s+2\pi k/T_s\) are consistent. The baseband choice \(k=0\) with \(\Omega\in[-\pi,\pi]\) is the reconstruction that an ideal digital-to-analog interpolator at that \(T_s\) would produce.

## Equations

Impulse train and sampled signal:

\[
p(t)=\sum_{n}\delta(t-nT_s), \qquad x_s(t)=x(t)p(t)=\sum_n x(nT_s)\delta(t-nT_s).
\]

Poisson copy formula:

\[
X_s(j\omega)=\frac{1}{T_s}\sum_{k}X\bigl(j(\omega-k\omega_s)\bigr), \qquad \omega_s=\frac{2\pi}{T_s}.
\]

Nyquist condition (baseband): if \(X(j\omega)=0\) for \(|\omega|>\omega_m\) and \(\omega_s>2\omega_m\), then \(x\) is recoverable by ideal lowpass filtering of \(x_s\) with cutoff \(\omega_c\) satisfying \(\omega_m<\omega_c<\omega_s-\omega_m\) and passband gain \(T_s\).

Alias in hertz: \(f_{\mathrm{alias}}=f-m f_s\) chosen so that \(|f_{\mathrm{alias}}|\le f_s/2\).

Ideal interpolation:

\[
x(t)=\sum_{n=-\infty}^{\infty}x(nT_s)\operatorname{sinc}\Bigl(\frac{t}{T_s}-n\Bigr).
\]

ZOH: \(H_{\mathrm{ZOH}}(j\omega)=T_s e^{-j\omega T_s/2}\operatorname{sinc}(\omega T_s/(2\pi))\) with a stated sinc, times the discrete-time spectrum of the coefficient sequence.

DT frequency: \(\Omega=\omega T_s\), unique modulo \(2\pi\).

## Methods

To decide whether sampling is invertible, find the highest frequency in \(X(j\omega)\) (or in a sum of sinusoids). Compare \(f_s\) to twice that frequency. If several sinusoids are present, each aliases separately; draw them on a frequency axis with copies at \(\pm f_s,\pm 2f_s,\ldots\) and see collisions.

To find the observed discrete-time frequency of a sampled cosine \(A\cos(2\pi f t)\), compute \(\Omega=2\pi f/f_s\) and reduce modulo \(2\pi\) into \([-\pi,\pi]\). The sequence is \(A\cos(\Omega n)\). If \(\Omega=\pi\) and samples hit zeros, the sequence can vanish.

To reconstruct ideally, apply the sinc sum only when the bandlimit hypothesis holds. For a finite list of samples of a non-bandlimited pulse, the sinc sum is the bandlimited interpolant, not necessarily the original pulse.

To design a minimal \(f_s\) for a baseband signal of bandwidth \(B\) hertz, take \(f_s>2B\). For a guard band \(G\), take \(f_s>2B+2G\) in the simplest symmetric placement.

When a problem gives a DTFT and a sampling period, convert \(\Omega\) to \(\omega=\Omega/T_s\) and remember \(2\pi\) periodicity before claiming uniqueness of the CT signal.

Sketch spectra: draw \(X(j\omega)\), then draw copies. Overlap regions are where aliasing energy appears. An ideal LPF of cutoff \(\pi/T_s\) always returns the principal period of \(X_s\), which equals \(X\) if and only if there was no overlap.

When converting a problem from hertz to radians, write \(f_s\) and \(2\pi f_s\) once in a margin and never mix them in the same inequality. The most common exam arithmetic error in this unit is \(\omega_s=2\pi f_s\) forgotten, so that \(2\omega_m\) is compared with \(f_s\).

If samples are not equally spaced, the classical theorem does not apply. Nonuniform sampling can still determine a bandlimited signal under extra density conditions, but that is not UG reconstruction by sinc of spacing \(T_s\).

## Mistakes

Using \(f_s>B\) instead of \(f_s>2B\) for baseband signals. Nyquist rate is twice the highest frequency, not the two-sided bandwidth counted twice in a confused way: a real signal with energy up to \(B\) hertz has two-sided support \(2B\) hertz wide, and the copies of that two-sided block must not overlap, which again requires \(f_s>2B\).

Stating the theorem for non-bandlimited signals (“sample a step at any rate and reconstruct”). A step is not bandlimited; sinc interpolation of its samples is not the step.

Forgetting the gain \(T_s\) in the analog reconstruction filter. Impulse-sampled spectra are scaled by \(1/T_s\).

Confusing \(\omega\) and \(f\), or writing Nyquist rate as \(2\omega_m\) in hertz.

Treating ZOH output as equal to the original analog waveform. It is a staircase plus images.

Ignoring that a cosine at \(f_s+f_0\) aliases to \(f_0\) with the same sequence as a true \(f_0\) cosine.

Reducing frequencies into \([0,f_s]\) instead of folding at \(f_s/2\), missing the mirror aliases.

Claiming discrete-time processing can undo analog aliasing after the sampler.

Using \(\operatorname{sinc}\) interpolation with \(\sin(x)/x\) and \(\sin(\pi x)/(\pi x)\) interchangeably without rescaling the time axis.

Taking a finite number of samples of a bandlimited everlasting signal and expecting exact reconstruction; the theorem uses an infinite sequence.
