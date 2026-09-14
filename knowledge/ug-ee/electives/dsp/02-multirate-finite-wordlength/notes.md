# Multirate DSP and finite wordlength

Changing the sample rate and then implementing the arithmetic in a finite number of bits are the two reasons a paper FIR/IIR and a chip disagree. This unit is integer decimation and interpolation (with the anti-alias / anti-image filters they require) and the UG model of quantization, roundoff, overflow, coefficient perturbation, and limit cycles. It is not a polyphase filter-bank course and not a copy of any DSP guidebook.

## Concepts

A discrete-time sequence \(x[n]\) is already sampled at some \(f_s=1/T\). **Decimation** by an integer \(M\) keeps every \(M\)th sample: \(y[n]=v[nM]\), where \(v\) is a filtered version of \(x\). Without that filter, the DTFT of the kept samples is
\[
Y(e^{j\omega})=\frac{1}{M}\sum_{k=0}^{M-1}X\bigl(e^{j(\omega-2\pi k)/M}\bigr)
\]
(up to the usual \(v=x\) case). The \(M\) shifted copies overlap unless \(X\) is band-limited to \(|\omega|<\pi/M\). Therefore a digital **anti-alias lowpass** with cutoff \(\pi/M\) (and gain 1 in the passband, or gain \(1\) before downsampling) must precede the compressor. In Hertz: output rate \(f_s/M\), useful analog bandwidth \(f_s/(2M)\). Example: \(f_s=8\,\mathrm{kHz}\), \(M=4\), output \(2\,\mathrm{kHz}\), anti-alias cutoff \(1\,\mathrm{kHz}\).

**Interpolation** by \(L\) inserts \(L-1\) zeros between samples (expander) then **anti-image** lowpass filters with cutoff \(\pi/L\) and gain \(L\) (to restore the baseband amplitude; the expander’s spectrum is \(X(e^{j\omega L})\), images at \(2\pi k/L\)). Output rate \(L f_s\). A cascade interpolate-by-\(L\) then decimate-by-\(M\) (or the reverse, with care) implements a rational rate change \(L/M\). When \(L\) and \(M\) are not coprime, cancel the common factor first.

**Noble identities** (UG catchphrase): a filter \(H(z^M)\) after a compressor equals the compressor after \(H(z)\); a filter \(H(z^L)\) before an expander equals the expander before \(H(z)\). They let you rewrite a naive filter-then-downsample as an efficient **polyphase** bank: split \(h[n]\) into \(M\) subsequences \(e_k[n]=h[nM+k]\), filter the delayed input streams at the *low* rate. UG should recognize “polyphase means run the FIR at the lower rate,” not derive a full commutator drawing under time pressure.

Multistage decimation: a large \(M=M_1 M_2\) is often two filters plus two compressors. The first filter can be wide and cheap (half-band FIR is popular) because the remaining alias region is still far; the second filter is narrower but runs slower. Same idea for interpolation. Half-band FIR: every other tap zero except the centre, cutoff \(\pi/2\).

CIC (cascaded integrator-comb) filters appear in one-line form as cheap multiplierless decimators; they have a sinc-like response and usually a compensating FIR. Mention, do not design, at this depth.

**Finite wordlength.** A b-bit two’s-complement fraction in \((-1,1)\) has quantization step \(\Delta=2^{-(b-1)}\) (one sign bit, \(b-1\) magnitude bits). A mid-riser or mid-tread quantizer maps a real \(x\) to the nearest level (rounding) or toward zero / \(-\infty\) (truncation). Rounding error is modelled as uniform white noise on \((-\Delta/2,\Delta/2)\), variance \(\sigma_e^2=\Delta^2/12\), uncorrelated with \(x\) if the signal is “busy.” Truncation of two’s-complement has a nonzero mean (a DC offset) and the same variance order. **SQNR** for a full-scale sinusoid occupying the whole range is
\[
\mathrm{SQNR}\approx 6.02b+1.76\quad(\mathrm{dB}),
\]
about \(6\,\mathrm{dB}\) per extra bit. For a less-than-full-scale signal, subtract \(20\log_{10}(1/\text{peak})\). ADC wordlength sets the *input* SQNR; internal ALU wordlength sets *roundoff* noise after each multiply.

Each real multiply in a fixed-point FIR, if the product is quantized back to b bits, injects a noise source of variance \(\Delta^2/12\). A length-\((M+1)\) direct-form FIR has \(M+1\) such sources at the output (if every tap rounds), so output roundoff variance \((M+1)\Delta^2/12\) before the filter’s own gain on the input quantization. IIR is worse: roundoff is filtered by the *recursive* part, so poles near the unit circle amplify noise (and can sustain **limit cycles**).

**Overflow.** Two’s-complement wrap-around turns a large positive into a large negative (a 2’s-complement overflow oscillation in IIR is famous). **Saturation** (clip to \(\pm 1\)) is preferred in DSP ALUs. Scaling the input or the internal nodes so that \(|y|<1\) in the worst case (L1 scaling: scale by \(1/\sum |h[n]|\)) prevents overflow at the cost of SQNR. L2 scaling uses \(\|h\|_2\) and is statistical, not worst-case.

**Coefficient quantization.** Replacing \(a_k,b_k\) by b-bit values moves poles and zeros. Poles in a high-order direct-form polynomial are extremely sensitive (companion-matrix perturbation). Cascade **biquads** (second-order sections) keep each pair of poles in a \(1+a_1 z^{-1}+a_2 z^{-2}\) with \(a_2=r^2\), \(a_1=-2r\cos\theta\), so radius and angle are quantized separately and stay sane. Coupled-form realizations exist for poles very near \(z=1\). UG numerical: a pole at \(0.99\) in 8-bit fractional precision — the nearest representable radius might be \(0.992\) or \(0.984\), changing the 3 dB bandwidth.

**Limit cycles.** In a stable IIR with quantization, the state can fail to go to zero with zero input: a periodic small oscillation (granular limit cycle) or a large overflow cycle. A first-order section \(y[n]=a y[n-1]+e[n]\) with rounding can stick at a deadband of width about \(\Delta/(2(1-|a|))\). Avoidance: more bits, magnitude truncation toward zero (can kill granular cycles), or no recursion (use FIR). Exam phrase: “limit cycles are zero-input closed orbits of the quantized state.”

Fixed-point versus floating-point: IEEE float hides most of this at UG cost in area/energy. Audio DSP and cheap MCUs still teach Q15. Q15 means 1 sign + 15 fraction bits, \(\Delta=2^{-15}\), range \([-1,1-2^{-15}]\).

Block floating-point and rounding-mode tables are extra. This unit’s jobs: \(f_s/M\), cutoff \(\pi/M\), interpolator gain \(L\), SQNR \(6.02b+1.76\), \(\Delta^2/12\), and “use biquads.”

## Equations

Compressor (after ideal anti-alias):
\[
y[n]=x[nM],\qquad f_{s,\mathrm{out}}=\frac{f_s}{M},\qquad \omega_c=\frac{\pi}{M}.
\]
Expander:
\[
v[n]=\begin{cases}x[n/L],& n=0\bmod L,\\ 0,&\text{else,}\end{cases}
\qquad H_{\mathrm{img}}(e^{j\omega})\ \text{cutoff }\pi/L,\ \text{gain }L.
\]
Rational rate: \(f_{s,\mathrm{out}}=(L/M)f_s\).

Quantization step (signed fraction, \(b\) bits):
\[
\Delta=2^{-(b-1)},\qquad \sigma_e^2=\frac{\Delta^2}{12}\quad(\text{rounding}).
\]
Sinusoid SQNR:
\[
\mathrm{SQNR}_{\mathrm{dB}}\approx 6.02\,b+1.76.
\]
FIR roundoff at output (independent rounding of \(M+1\) products):
\[
\sigma_{r,\mathrm{out}}^2=(M+1)\frac{\Delta^2}{12}.
\]
Biquad pole:
\[
a_2=r^2,\qquad a_1=-2r\cos\theta.
\]
First-order deadband (rule of thumb):
\[
|y|\le \frac{\Delta}{2(1-|a|)}.
\]
L1 overflow-free scale:
\[
G=\frac{1}{\sum_n |h[n]|}.
\]

## Methods

Decimation design: (1) write \(f_{s,\mathrm{out}}=f_s/M\); (2) set anti-alias cutoff \(f_s/(2M)\) analog, \(\pi/M\) digital at the *input* rate; (3) choose FIR length from transition width if specs exist, else name “lowpass \(\pi/M\)”; (4) downsample. If the signal is already band-limited (e.g. a baseband message of 3.4 kHz on 16 kHz going to 8 kHz), the anti-alias can be milder, but the exam usually wants \(\pi/M\).

Interpolation: insert zeros, lowpass at \(\pi/L\) with gain \(L\). Check a DC input: expander of a DC sequence \(A,A,A,\ldots\) is \(A,0,0,\ldots\) whose average is \(A/L\); gain \(L\) restores \(A\).

Rational convert: factor \(L/M\), put interpolation first if you need to preserve bandwidth that decimation would kill (standard: interpolate then decimate so the intermediate rate is high). Example \(8\,\mathrm{kHz}\to 12\,\mathrm{kHz}\) is \(L/M=3/2\): upsample by 3 to 24 kHz, down to 12 kHz.

SQNR: if they give full-scale sine, use \(6.02b+1.76\). If they give peak \(A<1\), add \(20\log_{10}A\). If they give \(\Delta\) only, \(\sigma_e^2=\Delta^2/12\), sine power \(A^2/2\), SQNR \(=10\log_{10}((A^2/2)/\sigma_e^2)\).

Roundoff in FIR: count multiplies that round. A symmetric linear-phase FIR can share taps (one multiply per pair) — fewer noise sources. State that if the question is picky.

Coefficient poles: convert \(r,\theta\) to \(a_1,a_2\), quantize \(a_1,a_2\) to the grid \(k\Delta\), convert back, report \(\Delta r\). Prefer cascade sections.

Overflow: if \(\sum |h|=4\) and input peak 1, output peak up to 4; scale input by \(1/4\) or grow the accumulator by 2 bits. Prefer saturation arithmetic in words.

Limit cycles: for zero input, iterate \(y[k]=\mathrm{round}(a y[k-1])\) from a small start; if it does not reach 0, you have a cycle. Report the deadband bound if a numerical is asked.

## Mistakes

Decimating first then filtering — aliases are already folded and cannot be filtered apart.

Anti-alias cutoff \(\pi\) instead of \(\pi/M\), or quoting the *output*-rate \(\pi\) without converting.

Interpolator gain 1, then DC is \(L\) times too small (or, applying gain \(L\) *and* another analog-style \(T\) factor).

SQNR \(6b\) without the \(0.02\) and \(+1.76\), presented as exact rather than sine/full-scale.

Using \(\Delta=2^{-b}\) for a signed fraction that includes a sign bit (off by one bit: \(6\,\mathrm{dB}\)).

Treating truncation as zero-mean.

Overflow wrap in a resonator (\(r\approx 1\)) as “just another quantization noise.” It is a nonlinear oscillator.

Quantizing a 6th-order direct-form IIR and blaming the analog prototype when poles have left the disk.

FIR “has no finite-wordlength issues.” Coefficient rounding still changes the frequency response; input quantization still sets SQNR. What FIR *avoids* is recursive limit cycles.

Polyphase as “a different filter,” not an identical \(H(z)\) at lower multiply rate.

Changing \(M\) without changing the anti-alias spec in a two-stage design (the first stage’s stopband only needs to protect the *next* Nyquist, not the final one — a feature, not a bug, if you compute it).

A numerical walk-through of two-stage decimation: \(f_s=48\,\mathrm{kHz}\) down to \(8\,\mathrm{kHz}\) (\(M=6=2\times 3\)). Stage 1, \(M_1=2\): half-band lowpass at \(12\,\mathrm{kHz}\), then 24 kHz. Stage 2, \(M_2=3\): lowpass at \(4\,\mathrm{kHz}\) (the *final* Nyquist), then 8 kHz. The first filter’s transition can extend toward 12 kHz because everything above 12 kHz will alias only into 12–24 kHz, which the second filter will kill. A single-stage 48→8 filter must be narrow *and* run at 48 kHz: more taps at a higher rate. That is why audio codecs cascade cheap CIC or half-band stages.

Q15 arithmetic: a coefficient \(0.9\) is \(0.9\times 2^{15}=29491\) (integer). Product of two Q15 numbers is Q30; you shift right 15 (or 14 with rounding) to return to Q15. Forgetting the shift is a factor \(2^{15}\) overflow. Guard bits in an accumulator (32-bit acc, 16-bit data) absorb FIR tap sums before a final sat-and-store.

Coefficient grid for a biquad: \(a_2=r^2\). If \(r=0.99\), \(a_2=0.9801\). With 8-bit signed fraction \(\Delta=2^{-7}\), nearest \(a_2\) is \(125/128=0.9766\) or \(126/128=0.9844\), so \(r=\sqrt{a_2}\) becomes \(0.988\) or \(0.992\). The 3 dB bandwidth of a resonator scales as \(1-r\); a 0.002 error in \(r\) near \(0.99\) is a 20 percent bandwidth error. Cascade sections, and pair poles with nearby zeros, before you spend bits.

Limit-cycle demo worth doing on paper: \(y[n]=\mathrm{round}_\Delta(0.9 y[n-1])\), \(\Delta=0.1\), start \(y=0.5\). Sequence 0.5, 0.5, 0.5, … can stick if rounding goes to nearest (0.45→0.5). Magnitude truncation toward zero yields 0.4, 0.4? actually 0.36→0.4 or down to 0. That is why some DSP libraries offer convergent rounding plus saturate, and why FIR is the lazy stable default when latency allows.
