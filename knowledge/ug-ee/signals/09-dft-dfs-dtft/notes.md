# DTFT, DFS, DFT relations

Three discrete-frequency objects live in a signals course: the DTFT of an aperiodic sequence (a \(2\pi\)-periodic function of a continuous frequency \(\Omega\)), the DFS/DTFS of a periodic sequence (a discrete list of \(N\) coefficients), and the DFT of a finite vector (another list of \(N\) numbers, implemented by the FFT). They are not competing definitions of “the” transform; they are restrictions of one Poisson/aliasing picture to different time supports. This unit relates them, states the pairs, and records the properties used in UG problems.

## Concepts

The discrete-time Fourier transform of an absolutely summable sequence is

\[
X(e^{j\Omega})=\sum_{n=-\infty}^{\infty}x[n]e^{-j\Omega n}, \qquad
x[n]=\frac{1}{2\pi}\int_{2\pi}X(e^{j\Omega})e^{j\Omega n}\,d\Omega.
\]

\(X(e^{j\Omega})\) is always \(2\pi\)-periodic when it exists. Real sequences have Hermitian DTFTs. A rectangular window of length \(L\) has a Dirichlet-kernel (periodic sinc) transform. Exponential decay \(a^n u[n]\) with \(|a|<1\) has a rational DTFT \(1/(1-ae^{-j\Omega})\). Sequences that are not \(\ell^1\) but are \(\ell^2\) still have DTFTs in an \(L^2\) sense on the circle. Periodic sequences are not \(\ell^1\); their DTFTs are impulse trains on the circle, and the impulse weights are the DTFS coefficients times \(2\pi\).

The DFS of an \(N\)-periodic sequence is the finite pair already used in the Fourier-series unit. If one period of that sequence is stored as a vector of length \(N\), the DFT of that vector is

\[
X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}, \qquad
x[n]=\frac{1}{N}\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N},
\]

in the common signal-processing convention that puts \(1/N\) on the inverse. Comparing with the DTFS pair that put \(1/N\) on analysis, one has \(X[k]=N a_k\) on one period. Always state which convention is in force when mixing books.

Sampling the DTFT of a finite-length sequence of length at most \(N\) at \(\Omega_k=2\pi k/N\) yields the DFT of that sequence padded with zeros to length \(N\). Conversely, interpolating DFT samples with a Dirichlet kernel recovers the DTFT of a time-limited sequence. If the true sequence is longer than \(N\), frequency sampling aliases in time: the IDFT sees \(\sum_m x[n+mN]\), a time-aliased wrap.

The DFT implements circular convolution: multiplying two length-\(N\) DFTs and inverting gives \(x\circledast h\), not linear convolution, unless zeros were padded to at least \(L_x+L_h-1\). Overlap-add and overlap-save are block methods that use this fact to filter long streams with an FIR \(h\).

Parseval for DTFT: \(\sum |x[n]|^2=\frac{1}{2\pi}\int_{2\pi}|X(e^{j\Omega})|^2 d\Omega\). For DFT: \(\sum_{n=0}^{N-1}|x[n]|^2=\frac{1}{N}\sum_{k=0}^{N-1}|X[k]|^2\) in the convention above. Scaling mismatches here are almost always a \(1/N\) error.

Resolution versus length: a length-\(N\) DFT of a sinusoid that is not an integer number of cycles in the window shows leakage, a sampled Dirichlet kernel, not a single bin. Zero-padding interpolates that kernel; it does not add new measurement information or “increase Rayleigh resolution” of two closely spaced tones. Window functions (Hann, Hamming) trade mainlobe width for sidelobe height; they belong in a DSP elective but appear as leakage control in this unit’s pictures.

Relationship summary:

- Aperiodic, infinite time \(\to\) DTFT, continuous \(2\pi\)-periodic frequency.
- Periodic, infinite time, period \(N\) \(\to\) DFS, \(N\) discrete frequencies; DTFT is impulses at those frequencies.
- Finite vector, length \(N\) \(\to\) DFT; equals samples of the DTFT of the finite (zero outside) sequence.
- Sampling in time \(\leftrightarrow\) periodization in frequency (CTFT to DTFT).
- Periodization in time \(\leftrightarrow\) sampling in frequency (DTFT to DFT/DFS).

The FFT is an algorithm that computes the DFT in \(O(N\log N)\) arithmetic, not a fourth transform. Radix-2 lengths are convenient, not theoretically required.

Shift properties: a circular shift of a DFT vector multiplies by \(e^{-j2\pi k n_0/N}\). A linear shift of a time-limited sequence whose support slides off the window is not a circular shift; pad first if linear delay is intended.

A rectangular window’s DTFT is a Dirichlet kernel \(e^{-j\Omega(L-1)/2}\sin(\Omega L/2)/\sin(\Omega/2)\). Sampling that kernel at \(2\pi k/N\) with \(N=L\) produces the DFT of a length-\(L\) box, which is \(L\) at bin 0 and 0 at other bins: the zeros of the Dirichlet kernel land on the other bins. If the box is zero-padded, those zeros no longer hit every bin and you see the sidelobes. That is the entire leakage story for a truncated cosine that is not an integer number of cycles: you are sampling a shifted Dirichlet kernel, not two impulses.

Orthogonality of DFT columns is why a cosine with an integer number of cycles occupies two conjugate bins and zeros elsewhere (for even length, a Nyquist bin can also appear for \((-1)^n\)). Non-integer cycles break orthogonality relative to the DFT basis and leak.

The relationship to sampling: taking one period of a periodic discrete-time signal is analogous to windowing; the DFS coefficients are exact. Taking a finite record of an aperiodic sequence and computing a DFT is always exact for that windowed record and approximate for the original DTFT. There is no paradox if the object is named.

Matrix view: the DFT is multiplication by a Vandermonde matrix of the \(N\)th roots of unity. Invertibility is the geometric sum of those roots. Conditioning is excellent in exact arithmetic; in floating point, FFTs of huge \(N\) still work well, unlike some real sinusoidal bases.

Parseval’s \(1/N\) in the DFT convention of this unit matches the idea that bins \(X[k]\) grow with \(N\) for a coherent tone (height \(\sim N A/2\)) while time energy grows with \(N\) for a lasting sinusoid window. Energy spectral density plots therefore often display \(|X[k]|^2/N\) or a physical scaling with \(f_s\).

Two-dimensional DFT and spectrograms are extra; UG 1-D relations already explain why a spectrogram window length trades time versus frequency smear, because each column is a windowed DFT.

## Equations

DTFT pair as above. DFT pair as above.

Circular convolution:

\[
(x\circledast h)[n]=\sum_{m=0}^{N-1}x[m]h[(n-m)\bmod N]\ \longleftrightarrow\ X[k]H[k].
\]

Frequency sampling:

\[
X[k]=X(e^{j\Omega})\big|_{\Omega=2\pi k/N}
\]

when \(x[n]=0\) outside \(0,\ldots,N-1\).

Time aliasing:

\[
x_{\mathrm{alias}}[n]=\sum_{m}x[n+mN], \quad n=0,\ldots,N-1.
\]

Modulation: \(e^{j\Omega_0 n}x[n]\leftrightarrow X(e^{j(\Omega-\Omega_0)})\).

Parseval (DFT, this convention):

\[
\sum_{n=0}^{N-1}|x[n]|^2=\frac{1}{N}\sum_{k=0}^{N-1}|X[k]|^2.
\]

## Methods

Choose the object from the time support. Everlasting aperiodic decay: DTFT or Z on the unit circle. Period \(N\): DFS/DFT of one period. A computer array of length \(N\): DFT, with an explicit story about what the missing samples were (zeros, or one period of a periodic model).

To compute a small DFT, use the definition or factor as a geometric sum. A constant vector has \(X[0]=N x[0]\) and \(X[k]=0\) for \(k\not\equiv 0\). An impulse \(\delta[n]\) has DFT \(1\) in every bin. A cosine of exactly \(k_0\) cycles in the window occupies bins \(k_0\) and \(N-k_0\).

To get linear convolution via DFT: zero-pad both sequences to \(M\ge L_x+L_h-1\), multiply DFTs, inverse DFT, keep \(M\) samples.

To relate DTFT plots to DFT stems, mark \(\Omega=2\pi k/N\). If the DTFT is smooth, DFT samples track it. If the sequence was implicitly periodic, the “DTFT” is impulsive and the DFT samples the weights.

When a problem gives \(X[k]\) and asks \(x[n]\), use the inverse sum. Check \(n=0\) against \(\frac{1}{N}\sum X[k]\).

To move between DTFT and Z: if the ROC includes the unit circle, substitute \(z=e^{j\Omega}\). If a pole sits on the circle, the DTFT may still exist as a principal-value plus impulses (the DTFT of \(u[n]\) is a classic table pair with a \(\pi\)-periodic impulse train plus \(1/(1-e^{-j\Omega})\)). Do not substitute blindly.

A length-\(N\) circular shift by \(n_0\) samples is \(x[(n-n_0)\bmod N]\). Its DFT is \(X[k]e^{-j2\pi k n_0/N}\). Linear convolution delay without padding wraps the tail; that wrap is time aliasing of the delayed sequence.

When relating sampling rate \(f_s\) to bin \(k\), analog frequency is \(k f_s/N\) for \(k=0,\ldots,N/2\) on a real signal (Nyquist bin at \(N/2\) if \(N\) even). Negative frequencies occupy \(k=N-1,N-2,\ldots\).

## Mistakes

Treating the DFT as samples of a CTFT of a staircase analog signal without the sampling-period scale.

Using linear convolution theorems with unpadded DFTs.

Forgetting \(2\pi\)-periodicity and treating \(\Omega=3\pi\) as distinct from \(\Omega=\pi\).

Putting \(1/N\) on both DFT directions, or on neither, then using a Parseval identity from the other convention.

Claiming zero-padding increases the ability to separate two tones closer than about \(2\pi/N\). It interpolates the same kernel.

Writing DTFT integrals from \(0\) to \(1\) as if \(\Omega\) were in cycles without converting \(d\Omega\).

Identifying DFS coefficient \(a_k\) with DFT bin \(X[k]\) without the factor \(N\).

Using a two-sided infinite sum for a DFT of a window that was defined only on \(0,\ldots,N-1\) but with nonzero implied samples outside.

Confusing \(\Omega\) (radians per sample) with \(f_s\)-scaled analog frequency when labeling plots.

Assuming every real sequence has a real DFT. Hermitian yes; real DFT only for even sequences in a circular sense.

Treating \(k=N\) as a new bin. It equals \(k=0\). The range \(k=0,\ldots,N-1\) is a complete set of DFT frequencies and should be the only bins reported unless a centered axis is drawn on purpose.

Using a one-sided frequency axis \([0,\pi]\) and then applying a complex modulation theorem that needs the full \([-\pi,\pi]\) or \([0,2\pi]\) view.

Claiming the DFS of a length-\(N\) periodic impulse train is a periodic impulse train in \(k\) of the same spacing without the \(1/N\) (or \(N\)) scale that the chosen pair requires.

Forgetting that zero-padding in time interpolates in frequency, while zero-padding in frequency (inserting bins) interpolates in time—and the latter is not a legal DFT lengthening unless you also respect conjugate symmetry for real data.
