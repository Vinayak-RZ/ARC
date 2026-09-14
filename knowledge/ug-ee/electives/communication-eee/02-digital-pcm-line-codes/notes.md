# Sampling, PCM, line codes, and ISI intro

Digital communication for EEE starts by turning a bandlimited analog waveform into bits, sending those bits as pulses on a wire or a baseband channel, and not letting the pulses destroy their neighbours. This unit is the sampling theorem as used in PCM, quantization noise, A-law/µ-law as names, PCM bit rate, line codes, Nyquist ISI, and the raised-cosine pulse. It is not source/channel coding theory, not OFDM, and not a copy of MIT OCW.

## Concepts

**Sampling.** A real signal whose spectrum is zero for \(|F|\ge W\) is determined by samples at \(f_s>2W\) (Nyquist rate \(2W\)). Reconstruction is an ideal lowpass of gain \(T=1/f_s\) and cutoff \(f_s/2\), i.e. sinc interpolation. At exactly \(f_s=2W\) you need a non-realizable brick wall and a message with no energy at \(W\); practice uses a margin (telephony: \(W=3.4\,\mathrm{kHz}\), \(f_s=8\,\mathrm{kHz}\)). If the sampler is a train of impulses, the spectrum repeats every \(f_s\); overlap is **aliasing**. Anti-alias analog lowpass *before* the sampler. A zero-order hold (DAC) adds a sinc envelope; digital compensation or a reconstruction filter follows.

**Quantization.** Each sample is mapped to one of \(L=2^n\) levels (n bits). Uniform steps \(\Delta=(x_{\max}-x_{\min})/L\). Error \(e\in(-\Delta/2,\Delta/2)\) modelled as uniform, variance \(\Delta^2/12\). For a full-scale sine, SQNR \(\approx 6.02n+1.76\,\mathrm{dB}\) (same formula as the DSP pack). Peak SNR \(20\log_{10}(L\sqrt{12}/(2\sqrt{2}))\) variants appear; UG default is “about \(6n\,\mathrm{dB}\)”. **Companding** (compress then expand): µ-law (North America/Japan) and A-law (ITU, India/Europe) put finer steps near zero so quiet speech has better SNR. Standard PCM voice: 8-bit companded samples at 8 kHz \(\Rightarrow 64\,\mathrm{kbit/s}\) (DS0). Without companding, 12-bit linear is a rough equivalent for speech.

**PCM system:** anti-alias \(\to\) sample \(\to\) quantize \(\to\) encode bits. Regeneration: a mid-link slicer decides 0/1 and writes a clean pulse; analog AM cannot do that. Bit rate
\[
R_b=n f_s
\]
for one channel; TDM of \(N\) voice channels plus framing gives T1/E1 numbers (T1: 24 channels \(\times 8\) bits + 1 framing bit at 8 kHz \(=1.544\,\mathrm{Mbit/s}\)). UG should compute \(R_b=n f_s\) and maybe a TDM multiplex of identical channels, not the full T-carrier framing map.

**Line codes** (baseband pulse alphabets). Goals: DC balance (transformers, capacitors), clock content (edges for CDR), bandwidth, and error detection. **NRZ-L**: high=1, low=0, DC if long runs, spectrum sinc-shaped with energy at DC, first null \(R_b\). **NRZ-M** (differential) encodes *changes*. **RZ**: pulse occupies half the bit, more bandwidth (first null \(2R_b\)), better clock. **AMI** (bipolar): 0 is 0 V, 1s alternate \(+A,-A\); no DC, spectrum null at DC, first lobe to \(R_b\); a violation flags an error; long zero runs starve the clock (hence **HDB3** / **B8ZS** replace runs of zeros with deliberate violations — names only). **Manchester** (biphase): 0 is high-then-low, 1 is low-then-high (or vice versa) in one bit; edge in the *middle* of every bit; DC-free; first-null bandwidth \(\sim 2R_b\); Ethernet 10BASE-T used it. **Miller** (delay encode) halves some transitions. **2B1Q** / **4-PAM** for two bits per symbol: symbol rate \(R_b/2\), nicer bandwidth, needs more SNR. **Scrambling** breaks long runs without expanding bandwidth.

Power spectral sketches (no need to derive in an exam): NRZ has a sinc\(^2\) at DC; AMI has a lobe peaking near \(R_b/2\) and a null at DC; Manchester has little DC and energy toward \(R_b\).

**ISI.** A pulse \(g(t)\) sent every \(T_b=1/R_b\) (or every \(T_s\) for multilevel) produces samples \(y(kT)=\sum a_n g((k-n)T)\). **Nyquist ISI criterion**: \(g(kT)=0\) for \(k\neq 0\), equivalently the folded spectrum \(\sum_m G(f+m/T)\) is constant on \([-1/(2T),1/(2T)]\). The **sinc pulse** \(g(t)=\mathrm{sinc}(t/T)\) is Nyquist with bandwidth \(1/(2T)\) (the Nyquist minimum \(R_b/2\) for binary). It is infinite in time and sensitive to timing jitter. **Raised cosine** family:
\[
G(f)=\begin{cases}
T,& |f|\le \frac{1-\alpha}{2T},\\
\frac{T}{2}\bigl(1+\cos\bigl(\frac{\pi T}{\alpha}(|f|-\frac{1-\alpha}{2T})\bigr)\bigr),& \frac{1-\alpha}{2T}<|f|\le\frac{1+\alpha}{2T},\\
0,& |f|>\frac{1+\alpha}{2T},
\end{cases}
\]
excess bandwidth factor \(\alpha\in[0,1]\). Occupied bandwidth
\[
B=\frac{1+\alpha}{2}\,R_{\mathrm{sym}}.
\]
For binary \(R_{\mathrm{sym}}=R_b\). \(\alpha=0\) is sinc; \(\alpha=1\) doubles bandwidth to \(R_b\) and the time pulse decays as \(1/t^3\) (kinder). Root-raised-cosine split equally between TX and RX implements a matched filter whose cascade is Nyquist.

**Eye diagram:** overlay bits on a scope triggered at the symbol rate. Vertical opening: noise margin. Horizontal opening: timing margin. ISI closes the eye; the best sampling instant is the widest opening.

**Equalization** (name-level): a linear transversal filter undoes channel ISI (zero-forcing vs MMSE). Decision-feedback equalizer uses past decisions. UG intro stops at “if the pulse is not Nyquist, equalize or slow down.”

**PCM vs DM/ADM:** delta modulation sends 1-bit slopes at a high oversampling rate; slope overload versus granular noise. Mention if the syllabus list includes it; this pack’s title is PCM and line codes.

This unit’s exam jobs: \(f_s>2W\), \(R_b=n f_s\), SQNR \(6n\,\mathrm{dB}\), Manchester vs AMI vs NRZ bandwidth, \(B=(1+\alpha)R_b/2\).

## Equations

Nyquist:
\[
f_s>2W,\qquad x(t)=\sum_k x(kT)\,\mathrm{sinc}\bigl(\tfrac{t-kT}{T}\bigr)\quad(T=1/f_s).
\]
PCM:
\[
L=2^n,\quad R_b=n f_s,\quad \Delta=\frac{x_{\max}-x_{\min}}{L},\quad \sigma_q^2=\frac{\Delta^2}{12}.
\]
Sine SQNR \(\approx 6.02n+1.76\,\mathrm{dB}\).

TDM of \(N\) identical PCM channels (ignore framing):
\[
R_{\mathrm{mux}}=N n f_s.
\]

Raised cosine:
\[
B=\frac{(1+\alpha)R_{\mathrm{sym}}}{2}.
\]
Binary Nyquist minimum \(B_{\min}=R_b/2\).

AMI encoding of bits \(b_k\in\{0,1\}\): amplitude \(0\) if \(b_k=0\), else \((-1)^{p}A\) toggling \(p\) on each 1.

Manchester (one convention): pulse \(+A\) then \(-A\) for 1, opposite for 0, each half-bit \(T_b/2\).

## Methods

Sampling numerical: if \(W\) is given as “highest frequency,” \(f_{s,\min}=2W\). If a guard is stated (e.g. 10 percent), multiply. For a sum of tones, \(W\) is the largest tone.

PCM bit rate: bits per sample times samples per second. For stereo, twice. For a 4-channel logger at 12 bit, 1 kHz: \(R_b=4\cdot 12\cdot 1000=48\,\mathrm{kbit/s}\).

Quantization: if they give \(\Delta\) and peak, \(L=(\text{range})/\Delta\), \(n=\log_2 L\) (ceil if not a power of two — then you cannot use those exact levels). SQNR with sine: \(6.02n+1.76\). With a peak-to-peak range \(2A_{\mathrm{peak}}\) unused, include loading.

Line-code pick: transformer / capacitor coupling \(\Rightarrow\) no DC \(\Rightarrow\) AMI or Manchester, not plain NRZ. Need clock from data \(\Rightarrow\) Manchester or scrambled AMI. Tight bandwidth \(\Rightarrow\) NRZ or multilevel, not Manchester.

Raised cosine: identify whether \(R_b\) or \(R_{\mathrm{sym}}\) (PAM). Plug \(\alpha\). If they give \(B\) and \(R_b\), solve \(\alpha=2B/R_b-1\) and check \(0\le\alpha\le 1\).

Eye: more ISI \(\Rightarrow\) vertical close; jitter \(\Rightarrow\) horizontal close. Sampling at the eye centre.

When mixing DSP sampling and comms sampling: the reconstruction formula is the same; PCM adds a *quantizer* and a *bit mapper*. Aliasing is still illegal.

## Mistakes

Nyquist as \(f_s>W\) (missing the 2).

\(R_b=f_s\) forgetting bits per sample.

SQNR \(6n\) treated as exact for a DC signal (a DC sitting on a step can have zero error or \(\Delta/2\), not \(\Delta^2/12\)).

A-law versus µ-law numericals without the formula given — if the paper does not print the compressor, only name them.

Manchester “same bandwidth as NRZ.” It is roughly double.

AMI for a string of 1s producing a DC block — AMI *alternates*, so 1111 is \(+A,-A,+A,-A\), no DC. Zeros are the AMI clock problem.

Raised-cosine \(B=(1+\alpha)R_b\) missing the 2.

Using \(\alpha>1\).

Sinc pulse claimed as time-limited.

Equalizer as a way to beat the Shannon limit (it is a way to approach Nyquist on a dispersive cable, not extra capacity from nowhere).

T1 rate \(24\times 64\,\mathrm{kbit/s}=1.536\,\mathrm{Mbit/s}\) reported as 1.544 without the framing bit; the extra 8 kbit/s is framing. State which you mean.

Sampling a 4 kHz *passband* at 8 kHz without bandpass-sampling theory — if the signal is 100–104 kHz, ordinary \(2W=8\,\mathrm{kHz}\) works only with a bandpass sampler; a naive lowpass sampler needs \(>208\,\mathrm{kHz}\). UG default messages are baseband.

PCM encoding of one sample: a 4-bit natural binary code for levels \(0\ldots 15\) is not the same as a two’s-complement code for a bipolar signal. Telephony µ-law uses a sign bit plus a chord/mantissa (not a linear 8-bit two’s complement). If an exam gives a uniform mid-riser table, follow the table; do not invent µ-law numbers.

A TDM frame sketch: 32 timeslots of 8 bits at 8 kHz is the E1 family (\(2.048\,\mathrm{Mbit/s}\)); slot 0 framing, slot 16 signalling in some mappings. UG arithmetic is \(32\times 8\times 8000=2.048\,\mathrm{Mbit/s}\). North-American T1: 24 slots plus one framing bit per 125 µs frame: \(24\times 8+1=193\) bits \(\times 8000=1.544\,\mathrm{Mbit/s}\). Do not mix E1 and T1 bit rates.

Line-code spectra you can sketch in 30 seconds: draw \(f=0\), \(R_b/2\), \(R_b\). NRZ: peak at 0, first null at \(R_b\). AMI: 0 at DC, peak near \(R_b/2\), null at \(R_b\). Manchester: 0 at DC, energy through \(R_b\), first significant null near \(2R_b\). If the channel is transformer-coupled at 0 Hz, NRZ fails and AMI/Manchester survive.

Nyquist pulse extra: a rectangular time pulse of width \(T_b\) has a sinc spectrum and *severe* ISI on a bandlimited cable. The raised-cosine is a frequency-domain construction that *forces* the folded spectrum to be flat. Root-raised-cosine at TX and RX: each has square-root of \(G(f)\); the matched filter maximizes SNR for white noise while the cascade remains Nyquist. Timing error still causes ISI because the RC pulse’s zero crossings move; \(\alpha=1\) is more robust than \(\alpha=0\).

Eye-diagram measurement: a 10–90 percent rise on the opening, a peak-to-peak jitter as a fraction of \(T_b\), and a vertical opening in volts compared with the slicer threshold. An equalizer that opens the eye by boosting high frequency also boosts noise — the MMSE tap solution, not zero-forcing, is the one that knows that trade.

Delta modulation in one paragraph so a mixed syllabus does not surprise you: a 1-bit quantizer on the *difference* \(x(t)-\hat x(t)\), a staircase predictor \(\hat x\), sampling far above Nyquist. Slope overload when \(|x'|\) exceeds \(\Delta f_s\); granular noise when \(x\) is quiet and the staircase hunts by \(\pm\Delta\). Adaptive \(\Delta\) (ADM) tries both. PCM at 8 kHz × 8 bits remains the EEE default voice number.

Clock recovery: a PLL or an edge-triggered resonant tank locked to the average transition rate. AMI with long zeros has no edges — B8ZS/HDB3 insert violations so the PLL does not drift. Manchester never lacks a mid-bit edge, which is why it is popular in isolated links despite the bandwidth.
