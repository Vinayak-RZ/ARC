# DFT, FFT, and introductory FIR/IIR design

A DSP elective starts where the signals pack’s DTFT/DFS/DFT unit ends: you must *compute* with the DFT, count FFT arithmetic, force linear convolution through a circular one, and design short FIR and IIR filters that a UG can finish on paper. This unit is those four skills. It is not a filter-bank thesis, an FFT-hardware paper, or a copy of any DSP guidebook.

## Concepts

The **DFT** of a length-\(N\) sequence \(x[n]\), \(n=0,\ldots,N-1\), is
\[
X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\qquad k=0,\ldots,N-1,
\]
with inverse
\[
x[n]=\frac{1}{N}\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N}.
\]
\(X[k]\) is exactly the DTFT of the finite-support \(x\), sampled at \(\omega_k=2\pi k/N\). It is also the DFS coefficients of the periodic extension \(\tilde x[n]=x[n\bmod N]\). Parseval:
\[
\sum_n |x[n]|^2=\frac{1}{N}\sum_k |X[k]|^2.
\]
DC bin \(X[0]=\sum x[n]\). For real \(x\), \(X[N-k]=\overline{X[k]}\). The \(k=N/2\) bin (Nyquist, \(N\) even) is real.

Direct DFT costs \(N^2\) complex multiply-adds. A **radix-2 FFT** exists when \(N=2^m\). Cooley–Tukey splits \(X[k]\) into DFTs of even and odd samples (decimation-in-time) or of the two half-length frequency halves (decimation-in-frequency). Each split is \(N/2\) twiddles plus two length-\(N/2\) DFTs. Recursing to length 2 (a butterfly \(a\pm b\)) gives
\[
N_{\mathrm{mul}}\approx \frac{N}{2}\log_2 N,\qquad N_{\mathrm{add}}\approx N\log_2 N
\]
complex multiplies and adds, ignoring the cheap \(\pm 1,\pm j\) twiddles some lectures subtract. For \(N=64\): DFT \(4096\) muls, FFT \(192\) muls. Bit-reversed addressing appears in in-place DIT: the time index is loaded in bit-reversed order, or the frequency output comes out reversed. UG exams ask the count and one 8-point flowgraph, not a SIMD FFT.

**Circular convolution** \(y[n]=\sum_{m=0}^{N-1}x[m]h[(n-m)\bmod N]\) is multiplication of DFTs: \(Y[k]=X[k]H[k]\). **Linear** convolution of length-\(L\) \(x\) and length-\(M\) \(h\) has length \(L+M-1\). It equals an \(N\)-point circular convolution iff \(N\ge L+M-1\). Practice: zero-pad both sequences to \(N\), DFT, multiply, IDFT. If you skip padding, time-domain aliasing wraps the tail of the linear result onto the head. Overlap-add and overlap-save are the streaming versions: break \(x\) into blocks, pad or wrap, add the overlapping tails (OLA) or discard the wrap (OLS). UG needs the length condition and one 4-point numerical, not a production partitioned-FFT FIR.

**FIR** filters: \(y[n]=\sum_{k=0}^{M} b_k x[n-k]\), poles only at the origin, always BIBO-stable. Linear phase if the coefficients are symmetric \(b_k=b_{M-k}\) (type I/II) or antisymmetric (type III/IV). Group delay \(M/2\) samples for a length-\((M+1)\) symmetric FIR. The **window method** designs a linear-phase FIR from an ideal brick-wall impulse response
\[
h_d[n]=\frac{\sin\bigl(\omega_c(n-\alpha)\bigr)}{\pi(n-\alpha)},\quad \alpha=M/2,
\]
with \(h_d[\alpha]=\omega_c/\pi\), then \(b_n=w[n]h_d[n]\) for \(n=0,\ldots,M\) and \(w\) a finite window (rectangular, Hamming, Hann, Blackman). Rectangular: narrowest mainlobe, worst sidelobes (\(\approx -13\,\mathrm{dB}\)). Hamming: sidelobes \(\approx -41\,\mathrm{dB}\), wider transition. Transition width scales as \(1/M\). Frequency sampling and Parks–McClellan (equiripple) exist; UG intro stops at windowing plus the phrase “equiripple is optimal in minimax.”

**IIR** filters: rational \(H(z)=\frac{\sum b_k z^{-k}}{1+\sum a_k z^{-k}}\), poles inside the open unit disk for causal stability. Analog prototypes (Butterworth, Chebyshev I/II, elliptic) map to digital by **impulse invariance** or **bilinear transform**. Impulse invariance: \(h[n]=T h_c(nT)\), poles \(z=e^{sT}\), aliases analog frequency; good for band-limited analog filters, bad for highpass (aliasing). Bilinear:
\[
s=\frac{2}{T}\frac{z-1}{z+1},
\]
maps the analog \(j\Omega\) axis onto the unit circle with warping \(\Omega=(2/T)\tan(\omega T/2)\). Prewarp each critical analog frequency: design the analog filter at \(\Omega_p=(2/T)\tan(\omega_p T/2)\), then substitute. Butterworth analog \(|H(j\Omega)|^2=1/(1+(\Omega/\Omega_c)^{2N})\) is the usual paper prototype. Direct-form I/II, cascade of biquads, and parallel form are realization comments: cascade biquads are the practical default because coefficient quantization wrecks a single high-order polynomial (next unit).

Frequency response of a digital filter is \(H(e^{j\omega})\). FIR can be plotted from the real amplitude \(A(\omega)\) times \(e^{-j\omega M/2}\). IIR is evaluated by substituting \(z=e^{j\omega}\) or by pole-zero geometry: magnitude is product of distances to zeros over distances to poles.

Windows in one line each: Hann \(w[n]=0.5-0.5\cos(2\pi n/M)\); Hamming \(0.54-0.46\cos(2\pi n/M)\); Blackman adds a \(4\pi n/M\) term. Do not memorize Blackman’s constants unless the paper prints them.

A **phase-linear** IIR does not exist with a causal rational \(H(z)\) other than trivial \(z^{-k}\); if you need linear phase, use FIR (or filtfilt offline, which is non-causal).

This unit’s exam jobs: a 4- or 8-point DFT by hand, an FFT multiply count, a pad length, a 5-tap window FIR at \(\omega_c=\pi/2\), and a first-order bilinear map.

## Equations

Twiddle: \(W_N=e^{-j2\pi/N}\), \(X[k]=\sum_n x[n]W_N^{kn}\).

Radix-2 counts: \(\frac{N}{2}\log_2 N\) complex multiplies, \(N\log_2 N\) complex adds.

Linear-convolution length: \(L+M-1\). Circular equals linear when \(N\ge L+M-1\).

Ideal lowpass FIR (causal, delay \(\alpha=M/2\)):
\[
h_d[n]=\frac{\sin\bigl(\omega_c(n-\alpha)\bigr)}{\pi(n-\alpha)},\quad h_d[\alpha]=\frac{\omega_c}{\pi}.
\]

Bilinear and prewarp:
\[
s=\frac{2}{T}\frac{z-1}{z+1},\qquad \Omega=\frac{2}{T}\tan\frac{\omega T}{2}.
\]

First-order analog lowpass \(H(s)=a/(s+a)\) bilinear with \(c=2/T\):
\[
H(z)=\frac{a(z+1)}{(c+a)z+(a-c)}.
\]

Parseval and DC as above. Hamming window:
\[
w[n]=0.54-0.46\cos\bigl(2\pi n/M\bigr),\quad n=0,\ldots,M.
\]

## Methods

Hand DFT: use \(W_4= -j\) cycles, \(W_8=e^{-j\pi/4}\). Compute \(X[0]\) as the sum and \(X[N/2]\) as the alternating sum first; they are real for real data and catch arithmetic errors. Exploit periodicity \(W^{k+N}=W^k\) and \(W^{N/2}=-1\).

FFT count: write \(N=2^m\), report \((N/2)m\) muls. If the question says “real multiplies,” a complex mul is four real muls and two adds unless they use the 3-mul algorithm; state the convention. UG usually wants complex muls.

Linear via circular: choose \(N\) as the next convenient FFT length \(\ge L+M-1\) (often the next power of two). Zero-pad. If they force \(N=L\) without pad, compute the wrapped result and say it is not the linear convolution.

Window FIR: pick odd length so \(\alpha\) is integer (type I). Evaluate \(h_d[n]\) at each tap, multiply by \(w[n]\), plot or list. Check DC gain \(\sum b_n\) if a unity-gain lowpass is required; scale \(b\leftarrow b/\sum b\) if asked. Do not use `sinc` libraries in an exam; write \(\sin(x)/x\) with \(x=\omega_c(n-\alpha)\).

Bilinear IIR: prewarp \(\Omega_c=(2/T)\tan(\omega_c T/2)\). Design analog \(H(s)\) at that \(\Omega_c\). Substitute \(s=(2/T)(z-1)/(z+1)\), clear \((z+1)\) powers, collect \(b_k,a_k\). Check \(H(1)\) equals analog \(H(0)\) for a lowpass. For a highpass analog prototype, bilinear still works; impulse invariance does not (aliasing).

Stability: after design, poles of \(H(z)\) must satisfy \(|p|<1\). Bilinear maps analog LHP poles into the disk automatically. Impulse invariance maps \(s=a\) (Re \(a<0\)) to \(z=e^{aT}\) also inside. Coefficient rounding can push a pole out — next unit.

Realization: write the difference equation from \(H(z)\) in negative powers, causal (current output from current input and old samples). Direct form II uses one delay chain for poles and zeros.

## Mistakes

Calling the DFT a “sampled DTFT of the infinite signal” without the implicit window of length \(N\). Spectral leakage is that window’s DTFT (a Dirichlet kernel) convolved with the true DTFT.

Using \(N^2\) as the FFT cost, or \(\log N\) without the \(N/2\) factor.

Circular convolution of length \(N=L=M\) reported as linear.

Forgetting to zero-pad, then blaming the FFT.

FIR “always linear phase” — only if coefficients are (anti)symmetric and the filter is applied as a whole; truncating a symmetric \(h_d\) off-centre breaks it.

Setting \(\alpha=0\) in \(h_d[n]\) then claiming a causal linear-phase filter of length \(M+1\). That \(h_d\) is noncausal; you must shift by \(M/2\).

Bilinear without prewarp, then wondering why the cutoff is at the wrong digital frequency. The error is small if \(\omega T\ll 1\) and huge near Nyquist.

Impulse-invariance on a highpass or bandstop analog filter.

Stability test \(|a_k|<1\) on the polynomial coefficients instead of on the poles. A quadratic \(1-1.5z^{-1}+0.56z^{-2}\) is stable (poles \(0.7,0.8\)) even though \(1.5>1\).

Normalizing FIR by \(b_0\) instead of \(\sum b_n\) when DC gain is specified.

Twiddle sign: \(e^{+j2\pi kn/N}\) in the analysis DFT (that is the inverse).

Taking \(N=8\) Hamming with formula \(\cos(2\pi n/8)\) but \(n=0\ldots 7\) and \(M=7\) in one lecture versus \(M=8\) in another. The window length is the FIR length \(M+1\); be consistent with the problem’s \(M\).

A worked 8-point DFT of \(x=\{1,1,1,1,0,0,0,0\}\) is the Dirichlet kernel sampled: \(X[k]=e^{-j3\pi k/8}\sin(\pi k/2)/\sin(\pi k/8)\) for \(k\not\equiv 0\bmod 8\), and \(X[0]=4\). That pattern is spectral leakage of a rectangular window of length 4 sitting inside length 8. Zero-padding to \(N=16\) interpolates the same DTFT; it does *not* recover frequency resolution lost to the four-sample aperture. Students who “increase FFT size” to separate two tones 0.05 cycles/sample apart still need a longer *record*, not more zeros.

Group delay of a type-I FIR of order \(M\) even is \(M/2\) samples at every frequency where the real amplitude \(A(\omega)\) does not change sign. A sign change is a phase jump of \(\pi\), which is still generalized linear phase. IIR Butterworth bilinear has nonlinear phase: a square wave through it rings asymmetrically. If the lab asks for “no phase distortion,” the answer is FIR (or offline filtfilt), not a sharper elliptic IIR.

Frequency-sampling design places \(H[k]\) on a grid and IDFTs to \(h[n]\). It is easy and can put exact zeros on DFT bins (notch at \(k_0\)), but the response *between* bins can overshoot; a transition bin of 0.5 is the usual UG patch. Parks–McClellan (Remez) equalizes ripples; the exam name is enough.

For IIR, a bilinear Butterworth lowpass of order 2: analog \(H(s)=\Omega_c^2/(s^2+\sqrt{2}\Omega_c s+\Omega_c^2)\). Prewarp \(\Omega_c=(2/T)\tan(\omega_c T/2)\), substitute \(s=(2/T)(z-1)/(z+1)\), obtain a biquad \(H(z)=(b_0+b_1 z^{-1}+b_2 z^{-2})/(1+a_1 z^{-1}+a_2 z^{-2})\) with \(b_1=2b_0\), \(b_2=b_0\) (the analog zeros at infinity become zeros at \(z=-1\)). That double zero at Nyquist is the bilinear signature of a lowpass prototype. Direct-form II: one delay line \(w[n]=x[n]-a_1 w[n-1]-a_2 w[n-2]\), \(y[n]=b_0 w[n]+b_1 w[n-1]+b_2 w[n-2]\).

FFT butterflies: a DIT radix-2 stage computes \(X=A+W B\), \(Y=A-W B\). In-place overwrite needs a bit-reversed load. If you add the two half-length DFTs without the twiddle on the odd half, you have computed something that is not the DFT. Count of stages is \(\log_2 N\); each stage has \(N/2\) butterflies.

Window comparison at UG depth: to roughly halve a rectangular-window transition width, double \(M\). Hamming versus rectangular: you buy sidelobes for a wider mainlobe, so a Hamming design of the same \(M\) has a slower cutoff and a flatter stopband. Blackman is still wider. Do not mix a Hamming \(h[n]\) with a rectangular frequency-response plot from an older solution set.
