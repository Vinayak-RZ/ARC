# Analog modulation: AM, DSB, SSB, FM, and SNR intro

An EEE communication elective treats modulation as a way to park a baseband message at a carrier that an antenna and a channel will carry. This unit is AM (with and without carrier), DSB-SC, SSB, NBFM/WBFM, Carson’s bandwidth, and a first SNR comparison. It is not a coding-theory course, not a mixer-spurs application note, and not a copy of MIT OCW lecture text.

## Concepts

A real baseband message \(m(t)\) occupies \(|F|<W\) hertz (audio: a few kilohertz). A **carrier** \(A_c\cos(2\pi f_c t)\) with \(f_c\gg W\) can be amplitude- or angle-modulated so the transmitted spectrum sits in a radio band.

**AM (DSB with carrier)**:
\[
s(t)=A_c\bigl(1+\mu\,\hat m(t)\bigr)\cos(2\pi f_c t),
\]
where \(\hat m\) is \(m\) scaled to \(|\hat m|\le 1\) and \(\mu\in(0,1]\) is the **modulation index**. Overmodulation \(\mu>1\) makes the envelope cross zero and a simple diode envelope detector distorts. The spectrum is a carrier line plus two sidebands, copies of \(M(f)\) centred at \(\pm f_c\). **Bandwidth** \(B_{\mathrm{AM}}=2W\). Power: if the carrier power is \(P_c=A_c^2/2\) (ohm-normalized), total
\[
P_t=P_c\bigl(1+\tfrac12\mu^2 P_{\hat m}\bigr)
\]
and for a tone \(\hat m=\cos(2\pi f_m t)\), \(P_{\hat m}=1/2\), so \(P_t=P_c(1+\mu^2/2)\). Each sideband gets \(P_c\mu^2/4\); both sidebands together \(P_c\mu^2/2\). Efficiency \(\eta=(P_t-P_c)/P_t=\mu^2/(\mu^2+2)\) for a tone — at \(\mu=1\), \(\eta=1/3\). Most of the power sits in the carrier, which carries *no* message. That is why AM broadcast still uses it: envelope detection is a diode and a capacitor.

**DSB-SC** (double-sideband suppressed carrier): \(s=A_c m(t)\cos(2\pi f_c t)\). Bandwidth still \(2W\), no carrier line, power all in sidebands. Demodulation needs a **coherent** local oscillator at the same \(f_c\) (and phase). A phase error \(\phi\) multiplies the recovered message by \(\cos\phi\); a frequency error makes a beat. Costas loops recover the carrier from the suppressed-carrier signal.

**SSB**: keep one sideband, drop the other (and the carrier). Bandwidth \(W\). USB: \(s=A_c m\cos(2\pi f_c t)\mp A_c \hat m_H \sin(2\pi f_c t)\) with \(\hat m_H\) the Hilbert transform of \(m\) (the sign chooses USB/LSB). Filter method: generate DSB-SC and brick-wall one sideband. Phasing method: the Hilbert formula. Vestigial sideband (VSB) keeps a tail of the unwanted sideband for TV-like spectra with a low-frequency-rich message; mention only.

**Angle modulation.** Instantaneous phase \(\theta(t)=2\pi f_c t+\phi(t)\). **PM**: \(\phi(t)=k_p m(t)\). **FM**: \(\phi'(t)=2\pi k_f m(t)\), i.e.
\[
s(t)=A_c\cos\bigl(2\pi f_c t+2\pi k_f\int^t m(\tau)\,d\tau\bigr).
\]
Tone message \(m=A_m\cos(2\pi f_m t)\): FM **modulation index** \(\beta=\Delta f/f_m\) with peak deviation \(\Delta f=k_f A_m\). PM index is \(k_p A_m\). The tone FM spectrum is
\[
s(t)=A_c\sum_{n=-\infty}^{\infty}J_n(\beta)\cos\bigl(2\pi(f_c+n f_m)t\bigr),
\]
Bessel \(J_n(\beta)\). In principle infinite sidebands; **Carson’s rule** for occupied bandwidth
\[
B_{\mathrm{C}}\approx 2(\beta+1)f_m=2(\Delta f+f_m)
\]
(about 98 percent of power). **NBFM** \(\beta\ll 1\): only \(n=0,\pm 1\) matter, bandwidth \(\approx 2f_m\) like AM, but the sidebands are in quadrature with the carrier (that is why NBFM demodulated as AM fails). **WBFM** \(\beta\gtrsim 1\): bandwidth \(\approx 2\Delta f\). Commercial FM: \(\Delta f=75\,\mathrm{kHz}\), \(W\approx 15\,\mathrm{kHz}\), \(\beta=5\), Carson \(180\,\mathrm{kHz}\), channel spacing \(200\,\mathrm{kHz}\).

FM **amplitude is constant** \(A_c\). Nonlinear amplifiers (class C) are legal; AM needs linearity. Narrowband interference that is mostly amplitude is reduced by a limiter before the FM detector — the capture effect.

**Superheterodyne** receiver sketch: RF filter, mixer with local oscillator \(f_{LO}=f_c+f_{IF}\) (high side) or \(f_c-f_{IF}\), IF filter at a fixed \(f_{IF}\) (455 kHz AM, 10.7 MHz FM), detector. **Image** frequency \(f_{\mathrm{im}}=f_c+2f_{IF}\) (high-side LO) must be rejected by the RF filter. UG numerical: given \(f_c\) and \(f_{IF}\), find \(f_{LO}\) and \(f_{\mathrm{im}}\).

**SNR intro** (ohm-normalized, AWGN). Message power \(P_m\), noise PSD \(N_0/2\). Baseband SNR after an ideal lowpass of width \(W\) is \(S/N=P_m/(N_0 W)\) if we had sent the message as baseband. AM envelope detector (tone, \(\mu\), high CNR):
\[
\mathrm{SNR}_{\mathrm{out}}=\frac{\mu^2/2}{1+\mu^2/2}\cdot\frac{A_c^2/2}{N_0 W}=\eta\cdot\mathrm{CNR}_{\mathrm{sideband\ scale}}.
\]
The usual comparison: DSB-SC coherent \(\mathrm{SNR}_{\mathrm{out}}=P_t/(N_0 W)\) with \(P_t\) all in sidebands; AM wastes carrier so its SNR is worse by \(\mu^2/(\mu^2+2)\). SSB coherent uses bandwidth \(W\) not \(2W\) of noise, so it matches DSB-SC SNR for the same sideband power. FM (WBFM, high CNR) has
\[
\mathrm{SNR}_{\mathrm{out}}=3\beta^2(\beta+1)\,\frac{P_t}{N_0 B_{\mathrm{C}}/2}\ \text{order-of-magnitude}
\]
or the textbook form \(3\beta^2 P_t/(N_0 W)\) relative to a notional baseband — **FM SNR improves as \(\beta^2\)** at the cost of bandwidth (the SNR–bandwidth trade). Below a **threshold** CNR (around 10–12 dB), the FM advantage collapses (clicks). UG should know the direction of the inequalities and Carson, not a full discriminator-noise derivation.

Detection summary: AM — envelope (cheap) or coherent (better, needs \(\mu\) and a PLL). DSB-SC/SSB — coherent. FM — limiter-discriminator, PLL, or quadrature detector.

This unit’s exam jobs: \(P_t=P_c(1+\mu^2/2)\), \(B=2W\) vs \(W\), \(\beta=\Delta f/f_m\), Carson \(2(\Delta f+f_m)\), image \(f_c\pm 2f_{IF}\).

## Equations

Tone AM:
\[
P_c=\frac{A_c^2}{2},\quad P_t=P_c\bigl(1+\tfrac{\mu^2}{2}\bigr),\quad P_{\mathrm{SB}}=P_c\frac{\mu^2}{2},\quad \eta=\frac{\mu^2}{\mu^2+2},\quad B=2W.
\]
DSB-SC: \(s=A_c m\cos(2\pi f_c t)\), \(B=2W\), \(P_t=A_c^2 P_m/2\).

SSB: \(B=W\). Hilbert pair \(m+j\hat m_H\) is analytic.

FM tone:
\[
\Delta f=k_f A_m,\quad \beta=\frac{\Delta f}{f_m},\quad B_{\mathrm{C}}=2(\beta+1)f_m=2(\Delta f+f_m).
\]
NBFM condition \(\beta\ll 1\). Bessel carrier vanish: \(J_0(\beta)=0\) at \(\beta\approx 2.40, 5.52,\ldots\) (carrier-null method to measure \(\beta\)).

High-side LO:
\[
f_{LO}=f_c+f_{IF},\qquad f_{\mathrm{im}}=f_{LO}+f_{IF}=f_c+2f_{IF}.
\]

FM SNR (high CNR, tone, textbook UG form):
\[
\mathrm{SNR}_{\mathrm{FM}}\approx 3\beta^2\,\mathrm{SNR}_{\mathrm{ref}},\qquad \mathrm{SNR}_{\mathrm{ref}}=\frac{P_t}{N_0 W}.
\]

## Methods

AM power: identify whether \(P_c\) or \(A_c\) is given. Tone: use \(\mu^2/2\). If \(m(t)\) is not a tone, replace \(\mu^2/2\) by \(\mu^2\langle\hat m^2\rangle\). Total sideband power is half-and-half USB/LSB.

Bandwidth table: AM and DSB-SC \(2W\); SSB \(W\); FM Carson \(2(\Delta f+W)\) using \(W\) as the highest message frequency.

FM index: \(\beta=k_f A_m/f_m\). If they give \(k_f\) in Hz/V and \(A_m\) in volts, \(\Delta f=k_f A_m\) in hertz. Do not mix rad/s: \(k_f\) in Hz/V versus \(2\pi k_f\) in rad/s/V.

Carson versus Bessel: if they ask “commercial 98 percent,” Carson. If they ask “which harmonics,” look at \(J_n(\beta)\) significant until \(n\approx \beta+1\) or \(\beta+2\).

Receiver image: draw \(f_c\), \(f_{LO}\), \(f_{IF}=|f_{LO}-f_c|\). The other RF that mixes to the same IF is \(f_{LO}+f_{IF}\) if \(f_{LO}>f_c\). RF filter must notch that.

SNR comparison in one sentence: coherent DSB-SC and SSB (same transmitted *information* power) beat AM; WBFM beats them all above threshold at the price of spectrum; NBFM does not buy SNR.

Envelope detector: RC too large, diagonal clipping; too small, ripple. Time-constant between \(1/f_c\) and \(1/W\).

## Mistakes

Using \(P_t=P_c(1+\mu^2)\) (forgot the tone’s \(1/2\)).

SSB bandwidth \(2W\).

FM bandwidth \(2W\) for \(\beta=5\).

\(\beta=\Delta f\cdot f_m\) instead of quotient.

Mixing peak deviation \(\Delta f\) with frequency deviation *constant* \(k_f\).

Image as \(f_c+f_{IF}\) not \(f_c+2f_{IF}\).

Claiming AM is constant envelope.

Coherent detection of AM *without* saying it can also be envelope-detected when \(\mu\le 1\) and a carrier is present.

FM SNR formula below threshold as if \(\beta^2\) still held.

Hilbert SSB formula with both signs the same, producing DSB.

Ohm-normalized \(A_c^2/2\) treated as \(A_c^2\) (a factor-of-two power error that wrecks \(\eta\)).

Pre-emphasis/de-emphasis forgotten in FM audio (boosts high \(f_m\) before TX, inverse after RX) — if the question mentions 50 µs or 75 µs, that is the de-emphasis time constant, not a carrier period.

Worked AM phasors: a tone AM at \(\mu=1\) is a carrier phasor \(A_c\) plus two sideband phasors of length \(A_c/4\) each that rotate opposite ways and whose *sum* is always collinear with the carrier (that is why the envelope is \(A_c|1+\cos\omega_m t|\) and never goes negative at \(\mu=1\)). At \(\mu>1\) the collinear sum can reverse the resultant — the envelope detector then folds and the audio distorts. DSB-SC has no carrier phasor; the two sidebands still sum along a line that *reverses*, which is why the envelope is \(|m(t)|\) and why you need a coherent axis.

SSB phasing method in steps: split \(m(t)\) into a 0° path and a 90° Hilbert path; mix the first with \(\cos 2\pi f_c t\) and the second with \(\sin 2\pi f_c t\); add or subtract to cancel USB or LSB. A Hilbert transformer is an all-pass with \(-\pi/2\) for \(f>0\); FIR approximations need many taps at audio, which is why the filter method (crystal or DSP IF filter) dominates radios.

FM generation: a VCO with \(f=f_c+k_f m(t)\) is direct FM. Indirect FM (Armstrong) integrates \(m\) to make PM and then a narrowband PM modulator plus multipliers to grow \(\beta\). Demodulation: a limiter strips AM, a discriminator (slope of a tank, or a delay-and-multiply quadrature detector) maps frequency to voltage, then de-emphasis. A PLL with the VCO tracking \(s(t)\) has the VCO control voltage as the message — the same loop as in digital-control intuition, with a lowpass as the message filter.

Capture effect: two FM carriers in the same limiter-discriminator, the stronger one wins and the weaker is suppressed, unlike AM where they add as beats. Threshold: when CNR in the IF is too low, the limiter-discriminator emits Poisson-like clicks; SNR then falls faster than the linear \(\beta^2\) law. Broadcast FM stays above threshold by using enough \(P_t\) and a 200 kHz channel.

Superhet numerical extra: low-side injection \(f_{LO}=f_c-f_{IF}\) (only if \(f_c>f_{IF}\)) puts the image at \(f_c-2f_{IF}\). Double conversion (first IF high, second IF 455 kHz) eases image rejection because \(2f_{IF}\) is large at the first mixer. Tracking of RF and LO capacitors on an AM broadcast radio is a three-point alignment problem in the lab course, not a GATE trick.

SNR budget in one table the exam likes: for the same \(P_t\) and the same \(W\), coherent SSB and DSB-SC match; AM \(\mu=1\) is 4.8 dB worse (\(\eta=1/3\)); WBFM \(\beta=5\) is on the order of \(3\beta^2=75\) (18.8 dB) better than the baseband reference *above threshold*, paid for by \(B_{\mathrm{C}}=180\,\mathrm{kHz}\) versus \(W=15\,\mathrm{kHz}\). Do not quote that 18.8 dB as a field measurement; quote it as the textbook scaling.

Power in FM is \(A_c^2/2\) regardless of \(\beta\) (constant envelope). Bessel check: \(\sum_n J_n^2(\beta)=1\), so sideband powers re-partition but the total stays \(P_c\). At a carrier null \(J_0(\beta)=0\), all the power is in sidebands — a lab method to calibrate \(\beta\).
