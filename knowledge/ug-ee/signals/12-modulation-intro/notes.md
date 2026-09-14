# AM/complex exponential modulation for signals courses

Modulation in a first signals course is a frequency-shift property, not a full communications link. Multiplying a baseband signal by a cosine or by a complex exponential slides its Fourier transform. That slide is how AM radio, mixing, and complex baseband equivalents are introduced before SNR, PLL, and digital constellations. This unit treats multiplication by \(e^{j\omega_c t}\) and by \(\cos(\omega_c t)\), the resulting spectra, recovery by demodulation and lowpass filtering, and the Hilbert/analytic-signal view at UG depth.

## Concepts

Complex exponential modulation is the identity \(y(t)=x(t)e^{j\omega_c t}\leftrightarrow Y(j\omega)=X\bigl(j(\omega-\omega_c)\bigr)\). Every frequency component of \(x\) is increased by \(\omega_c\). If \(x\) is real and baseband, \(Y\) is not Hermitian; \(y\) is complex. Communications engineers still use this object as an analytic or equivalent-baseband representation because a single slide is easier than a pair of slides.

Cosine (AM) modulation uses a real carrier: \(y(t)=x(t)\cos(\omega_c t)\). Because \(\cos(\omega_c t)=\frac12(e^{j\omega_c t}+e^{-j\omega_c t})\), the spectrum is

\[
Y(j\omega)=\frac12 X\bigl(j(\omega-\omega_c)\bigr)+\frac12 X\bigl(j(\omega+\omega_c)\bigr).
\]

A real baseband \(X\) supported on \(|\omega|<\omega_m\) produces two sideband clusters around \(\pm\omega_c\), each of width \(2\omega_m\). If \(\omega_c>\omega_m\), those clusters do not overlap each other or the origin. That inequality is the usual non-overlap condition for conventional AM spectra in a signals course.

Double-sideband suppressed-carrier (DSB-SC) AM is exactly \(x(t)\cos(\omega_c t)\). There is no discrete carrier line unless \(x\) has a DC term. Conventional AM with carrier is \(y=(A+x(t))\cos(\omega_c t)\) with \(|x|<A\) so that the envelope \(A+x\) stays positive; a spectral line of weight proportional to \(A\) then sits at \(\pm\omega_c\). Envelope detection can recover \(A+x\) when the carrier is strong and the overmodulation condition is avoided. DSB-SC cannot be envelope-detected without a carrier; it needs coherent demodulation: multiply again by \(\cos(\omega_c t)\) (or a locally generated cosine locked in phase) and lowpass.

Coherent demodulation algebra: \(x(t)\cos(\omega_c t)\cdot\cos(\omega_c t)=\frac12 x(t)+\frac12 x(t)\cos(2\omega_c t)\). The double-frequency copy lives near \(2\omega_c\) and is rejected by a lowpass filter of cutoff between \(\omega_m\) and \(2\omega_c-\omega_m\). A phase error \(\phi\) in the local oscillator replaces \(\frac12 x\) by \(\frac12 x\cos\phi\), which vanishes at \(\phi=\pi/2\) (a catastrophic fade) and can change sign. Frequency error makes a slow beat.

Single-sideband (SSB) keeps only the upper or lower cluster. One construction is to form the analytic signal \(x+j\hat x\) where \(\hat x\) is the Hilbert transform of \(x\), multiply by \(e^{j\omega_c t}\), and take the real part. The Hilbert transformer is an ideal allpass with phase \(-\pi/2\) on positive frequencies. SSB occupies half the DSB bandwidth at the cost of that Hilbert network (or a bandpass filter that chops one sideband). A signals course only needs the spectral picture and the Hilbert definition, not Weaver’s method.

Frequency multiplexing: several baseband messages with bandwidths \(\omega_{m,i}\) can share one cable if they are shifted to disjoint carrier neighborhoods. Demodulation is a bank of mixers and lowpass filters. Guard bands absorb filter transition widths.

Mixing (heterodyne) is modulation followed by filtering to a new IF. The image frequency is the other input frequency that lands on the same IF after multiplication by the LO; analog receivers need an image-reject filter. In a signals course, draw the two slides \(\pm\omega_{\mathrm{LO}}\) and see which input bands land on the desired IF.

Complex baseband equivalent: a real bandpass signal whose spectrum lives in two narrow clusters around \(\pm\omega_c\) can be written \(x(t)=\operatorname{Re}\{u(t)e^{j\omega_c t}\}\) with a slowly varying complex envelope \(u\). Linear bandpass filtering of \(x\) corresponds to complex lowpass filtering of \(u\) by the shifted \(H(j(\omega+\omega_c))\) on the positive cluster. This is the bridge to later communications and to I/Q mixers.

Modulation is linear in the message if the carrier is independent of the message (AM, DSB, SSB as maps \(x\mapsto y\)). It is not time-invariant, because a delay of \(x\) does not delay \(y\) by the same amount unless the carrier is delayed too. The cascade “modulate, bandpass channel, demodulate” can still be time-invariant from message to recovered message when the carrier is treated as part of the system and phases align.

FM and PM vary the angle of the carrier; they are nonlinear in the message and produce Bessel sidebands. They are mentioned only to mark the boundary of this unit. Sampling with an impulse train is also a modulation (by a periodic pulse train) and was treated under sampling; the spectra are copies, not two sidebands.

Power: if \(x\) is a finite-power baseband signal with power \(P_x\) and zero DC, DSB-SC \(x\cos(\omega_c t)\) has power \(P_x/2\) when the carrier is a unit-amplitude cosine (time average of \(\cos^2\) is \(1/2\)). Conventional AM power splits between carrier \(A^2/2\) and sidebands \(P_x/2\).

Overmodulation (\(\mu>1\)) folds the envelope through zero. A diode envelope detector then follows \(|A+x|\) and produces severe distortion. Coherent demodulation of the same waveform still recovers \(A+x\), including the negative dips, because it is a product identity, not a peak follower.

A square-law device \(y=x^2\) with input \(A\cos(\omega_c t)+m(t)\) produces baseband \(m\) terms and double-frequency terms; it is a crude demodulator for conventional AM with carrier, and a modulator if used the other way (product terms). Signals courses treat it as a nonlinearity that creates new frequencies, then keep the desired term with a filter. That is the same spectral-copy bookkeeping as an ideal multiplier, plus extra harmonics.

I/Q demodulation multiplies by \(\cos\) and by \(-\sin\) (or \(\sin\)) in parallel, lowpasses, and reconstructs a complex envelope. A phase error rotates that complex number; a gain mismatch between I and Q distorts the constellation in a later digital course. At this level: two mixers give enough information to recover both sidebands independently, which is also how SSB can be demodulated without an analog Hilbert transformer at RF.

Frequency-division multiplexing (FDM) is modulation plus bandpass addition. The receiver is a bandpass filter, a mixer, and a lowpass. Guard bands exist because analog filters do not have brick walls. If two clusters overlap, the messages add in those frequencies and cannot be separated by LTI filters.

Complex exponential carriers are not “unphysical.” Quadrature analog hardware implements them with two real wires. Digital baseband processing often stays complex until a last digital-to-analog step creates a real IF or RF waveform.

Switching a carrier on and off with a binary message is on–off keying, a special case of AM with a rectangular \(x(t)\). Its spectrum is a sinc centered at \(\pm\omega_c\). Ringing of a following bandpass filter is convolution with that filter’s \(h\), which is the previous unit.

Synchronous detection of DSB-SC is identical in algebra to sampling’s “multiply by a pulse train and lowpass,” except the multiplier is a single cosine rather than an impulse train, so only two copies exist rather than infinitely many. Seeing both as modulation unifies the pack.

## Equations

Complex modulation: \(x(t)e^{j\omega_c t}\leftrightarrow X(j(\omega-\omega_c))\).

DSB-SC: \(x(t)\cos(\omega_c t)\leftrightarrow \frac12 X(j(\omega-\omega_c))+\frac12 X(j(\omega+\omega_c))\).

Conventional AM: \((A+x(t))\cos(\omega_c t)\) with spectrum \( \frac{A}{2}\bigl(2\pi\delta(\omega-\omega_c)+2\pi\delta(\omega+\omega_c)\bigr)\) plus the DSB-SC spectrum of \(x\) (using \(\cos\leftrightarrow\pi(\delta_{\omega_c}+\delta_{-\omega_c})\) in the CTFT convention of this pack).

Coherent demodulation identity:

\[
\cos(\omega_c t)\cos(\omega_c t+\phi)=\frac12\cos\phi+\frac12\cos(2\omega_c t+\phi).
\]

Hilbert transform (frequency response): \(\hat X(j\omega)=-j\operatorname{sgn}(\omega)X(j\omega)\) for \(\omega\neq 0\). Analytic signal \(x+j\hat x\) has a one-sided spectrum on \(\omega>0\).

SSB-USB (schematic): \(y(t)=x(t)\cos(\omega_c t)-\hat x(t)\sin(\omega_c t)\).

Envelope of conventional AM: \(|A+x(t)|\) when the carrier-frequency oscillation is removed by a peak detector, valid if \(A+x\ge 0\) and \(\omega_c\gg\omega_m\).

## Methods

To sketch a modulated spectrum, draw \(X(j\omega)\), copy it to \(\pm\omega_c\), scale by \(1/2\) for a cosine carrier, and add carrier impulses if \(A\neq 0\). Check overlap: require \(\omega_c>\omega_m\) for a baseband message of highest frequency \(\omega_m\).

To demodulate DSB-SC on paper, multiply by the carrier, expand with the product-to-sum identity, drop terms near \(2\omega_c\) by an ideal LPF of gain 2 if a gain of 1 at baseband is desired.

To recover conventional AM by envelope detection, state the positivity condition \(A\ge |x|_{\max}\) (modulation index \(\mu\le 1\) when \(x\) is a single tone of amplitude \(\mu A\)).

To form a complex envelope, factor \(e^{j\omega_c t}\) out of the positive-frequency cluster and double that cluster (or not, depending on the \(1/2\) convention of I/Q). Keep one convention in a given solution.

When a channel \(H(j\omega)\) is almost constant on each sideband cluster, replace it by a complex gain on the envelope. If \(H\) varies across the cluster, equalize at baseband.

For DT modulation, replace \(\omega\) by \(\Omega\) and remember wrap-around: discrete-time cosine modulation is not free of alias overlap if \(\Omega_c+\Omega_m>\pi\).

To check a sketched spectrum, verify Hermitian symmetry of any real \(y(t)\): magnitudes even, phases odd. A drawing with only a positive-frequency cluster cannot be the CTFT of a real cosine-modulated real message unless the negative cluster is implied.

When computing power of conventional AM with a single-tone message \(x=m A \cos(\omega_m t)\), sideband power is \(m^2 A^2/4\) total (two lines each of amplitude \(m A/2\) with power \((m A/2)^2/2\) each, careful with RMS). Carrier power is \(A^2/2\). Efficiency is sideband power over total, \(\mu^2/(2+\mu^2)\) for that tone. The formula is a good check on the \(1/2\) factors.

## Mistakes

Writing \(X(j(\omega-\omega_c))\) without the companion \(X(j(\omega+\omega_c))\) for a real cosine mixer.

Placing sidebands at \(\omega_c\) with the original baseband width \(\omega_m\) instead of \(2\omega_m\) two-sided width per cluster.

Envelope-detecting DSB-SC or overmodulated AM and expecting \(x(t)\).

Forgetting the \(1/2\) from \(\cos^2\), so the recovered message is off by 2.

Using a local oscillator at the wrong frequency and calling the result a simple gain; it is a residual modulation.

Treating modulation as LTI. Multiplication by a fixed cosine is linear and time-varying.

Confusing FM Bessel spectra with AM sidebands. A single-tone FM has infinitely many lines; AM has two (plus carrier).

Taking Hilbert \(H(j\omega)=-j\operatorname{sgn}(\omega)\) and then using it on a signal with DC without specifying the DC convention (usually \(\hat x\) has zero DC).

Demodulating with \(\sin(\omega_c t)\) while the modulator used \(\cos(\omega_c t)\) and wondering why the LPF output is zero (quadrature null).

Ignoring that a bandpass filter after the modulator can turn DSB into SSB, which then needs a matching demodulator.

Using energy Parseval on a finite-power AM wave without converting to power.

Drawing only \(\omega>0\) and then designing a real impulse response that cannot be real because Hermitian symmetry was dropped.
