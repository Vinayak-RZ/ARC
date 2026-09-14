# Continuous/discrete, energy/power, even/odd, periodic

A signal is a function that carries information. In undergraduate electrical engineering the independent variable is almost always time, written \(t\) in continuous time and \(n\) in discrete time. The dependent variable may be voltage, current, flux, a sampled sequence, or an abstract waveform used to test a system. Classification is not decoration: energy versus power decides which inner product and which Parseval identity apply; even versus odd decides which Fourier coefficients vanish; continuous versus discrete decides which convolution integral or sum is legal; periodic versus aperiodic decides whether a Fourier series or a Fourier transform is the natural expansion. This unit is the vocabulary for the rest of the pack.

## Concepts

Continuous-time (CT) signals are defined on a real interval, typically all of \(\mathbb{R}\) or \(t \ge 0\). Discrete-time (DT) signals are defined on the integers, typically all of \(\mathbb{Z}\) or \(n \ge 0\). A DT signal may arise by sampling a CT signal, \(x[n] = x_c(nT_s)\), or it may be native (daily load, clocked register contents, a recurrence). Sampling is not required for a sequence to be a legitimate signal. Digital signals are a further restriction: a DT signal whose amplitude is quantized to a finite alphabet. Amplitude quantization is a separate classification from the time-axis classification; a staircase analog waveform is still CT.

Deterministic signals are fully specified by a formula or a table. Random signals are families of waveforms with a probability law; energy and power then become expected values. This handbook stays with deterministic waveforms except when a definition needs an ensemble average for context. Finite-support signals vanish outside a bounded interval. Right-sided signals vanish for \(t < 0\) (or \(n < 0\)); left-sided signals vanish for \(t > 0\). Two-sided signals are nonzero on both sides of the origin. Causal signals in the usual engineering convention are right-sided and start at the origin; the word causal is also used for systems, so keep the noun explicit.

The unit impulse and unit step are the two most used elementary signals. In CT, \(\delta(t)\) is a distribution: \(\int_{-\infty}^{\infty} \delta(t)\,dt = 1\) and \(\int x(t)\delta(t-t_0)\,dt = x(t_0)\) when \(x\) is continuous at \(t_0\). The unit step \(u(t)\) is 1 for \(t > 0\), 0 for \(t < 0\), and conventionally \(1/2\) or 1 at \(t=0\) depending on the author; products with ordinary functions do not care about a single point. The relation \(\delta(t) = du/dt\) is distributional. In DT, \(\delta[n]\) is an ordinary sequence that is 1 at \(n=0\) and 0 elsewhere, and \(u[n]\) is 1 for \(n \ge 0\). There is no mystery about the value at the origin in discrete time.

Even and odd parts extract symmetry. A signal is even if \(x(-t)=x(t)\) (or \(x[-n]=x[n]\)) and odd if \(x(-t)=-x(t)\). Any signal with a two-sided domain splits uniquely as \(x = x_e + x_o\) with \(x_e(t)=\frac12(x(t)+x(-t))\) and \(x_o(t)=\frac12(x(t)-x(-t))\). The even part of a real signal has a real Fourier transform; the odd part has a purely imaginary, odd transform. Products of two even or two odd signals are even; an even times an odd signal is odd. Integrals of odd functions over symmetric intervals vanish when they exist. Complex conjugate symmetry \(x(-t)=x^*(t)\) is the Hermitian condition used for real spectra of complex baseband envelopes.

Periodicity is a shift invariance of the waveform itself. A CT signal is periodic if there exists \(T>0\) such that \(x(t+T)=x(t)\) for all \(t\) in the domain. The smallest such \(T\) is the fundamental period. A DT signal is periodic if there exists a positive integer \(N\) with \(x[n+N]=x[n]\) for all \(n\). A continuous sinusoid \(\cos(\omega t)\) is always periodic for \(\omega \ne 0\), with period \(2\pi/|\omega|\). A discrete sinusoid \(\cos(\omega n)\) is periodic if and only if \(\omega/(2\pi)\) is rational. Sums of periodic signals are periodic when a common period exists, i.e. when the period ratio is rational in CT for sinusoids, or when the discrete frequencies share a common multiple of \(2\pi\). Almost-periodic sums (incommensurate frequencies) are not periodic; they still have a Fourier transform in the sense of distributions, with lines at those frequencies.

Energy and power are inner-product notions, not circuit power unless the signal happens to be a voltage on \(1\,\Omega\). The instantaneous energy density of a CT signal is \(|x(t)|^2\). Total energy is \(E_x = \int_{-\infty}^{\infty}|x(t)|^2\,dt\). Average power over \([-T,T]\) is \(\frac{1}{2T}\int_{-T}^{T}|x(t)|^2\,dt\), and the signal power is the limit as \(T\to\infty\) when the limit exists. A finite-energy (square-summable) signal has \(0 < E_x < \infty\) and then necessarily \(P_x=0\). A finite-power signal has \(0 < P_x < \infty\) and typically infinite energy (a never-ending sinusoid, a periodic pulse train, a nonzero constant). Some signals have neither finite energy nor finite power (a ramp \(t\,u(t)\)). In discrete time, \(E_x=\sum_{n=-\infty}^{\infty}|x[n]|^2\) and \(P_x=\lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}|x[n]|^2\). Parseval identities later identify \(E_x\) with an \(L^2\) norm of a transform and \(P_x\) with a sum of squared Fourier-series coefficients.

Bounded signals satisfy \(\sup |x| < \infty\). Every finite-energy CT signal that is also bounded is not automatically finite-power in a useful sense: energy finite already forces power zero. Conversely, a bounded everlasting sinusoid is finite-power and infinite-energy. Square-summable sequences vanish at infinity; bounded everlasting discrete sinusoids do not. The space \(\ell^2(\mathbb{Z})\) is the discrete energy space; \(\ell^\infty\) is the bounded sequences. BIBO stability later uses \(\ell^1\) on impulse responses, which is a different norm.

Time scaling \(x(at)\) compresses the waveform if \(|a|>1\) and expands it if \(|a|<1\). Time reversal is \(a=-1\). Time shift \(x(t-t_0)\) delays a waveform when \(t_0>0\) if the plot is against \(t\). Mixing these operations requires a fixed order: write the argument as \(a(t-t_0)\) or \(at-b\) and track which is which. Amplitude scaling \(A x(t)\) is linear. Adding a DC offset is affine, not linear through the origin. Complex exponential signals \(e^{st}\) with \(s=\sigma+j\omega\) are the eigenfunctions of CT LTI systems. Discrete exponentials \(z^n\) play the same role for DT LTI systems.

A periodic pulse train, a single pulse, and a sampled pulse are three different objects. The periodic pulse train is a power signal and has a Fourier series. The single pulse is an energy signal and has a Fourier transform that is continuous in frequency. Sampling the pulse produces a DT energy sequence whose DTFT is \(2\pi\)-periodic. Confusing these three is the most common classification error in exam solutions.

Real-world laboratory traces are finite-length. A captured oscilloscope record is an energy signal on its displayed window; if one pretends it continues forever as a periodic copy, one has manufactured a power signal and a discrete spectrum. The classification therefore depends on the mathematical model, not on the physical generator alone. State the model before computing energy or power.

## Equations

Unit impulse and step, CT:

\[
\int_{-\infty}^{\infty} \delta(t)\,dt = 1, \qquad
\int_{-\infty}^{\infty} x(t)\delta(t-t_0)\,dt = x(t_0), \qquad
u(t) = \int_{-\infty}^{t}\delta(\tau)\,d\tau.
\]

Discrete counterparts:

\[
\delta[n] =
\begin{cases}
1, & n=0,\\
0, & n\neq 0,
\end{cases}
\qquad
u[n]=\sum_{k=-\infty}^{n}\delta[k],
\qquad
x[n]=\sum_{k=-\infty}^{\infty} x[k]\delta[n-k].
\]

Even and odd parts:

\[
x_e(t)=\frac{x(t)+x(-t)}{2}, \qquad
x_o(t)=\frac{x(t)-x(-t)}{2}, \qquad
x(t)=x_e(t)+x_o(t).
\]

Energy and power, CT:

\[
E_x=\int_{-\infty}^{\infty}|x(t)|^2\,dt, \qquad
P_x=\lim_{T\to\infty}\frac{1}{2T}\int_{-T}^{T}|x(t)|^2\,dt.
\]

Energy and power, DT:

\[
E_x=\sum_{n=-\infty}^{\infty}|x[n]|^2, \qquad
P_x=\lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}|x[n]|^2.
\]

For a CT sinusoid \(A\cos(\omega t+\phi)\) one has \(E_x=\infty\) and \(P_x=A^2/2\). For a complex exponential \(A e^{j\omega t}\) the power is \(|A|^2\). A periodic CT signal with period \(T_0\) and finite one-period energy \(E_1\) has power \(P_x=E_1/T_0\). A DT periodic signal with period \(N\) has \(P_x=\frac{1}{N}\sum_{n=\langle N\rangle}|x[n]|^2\).

Period tests:

\[
x(t+T)=x(t)\ \forall t \iff \text{periodic with period }T,
\qquad
\cos(\omega n)\ \text{periodic}\iff \frac{\omega}{2\pi}\in\mathbb{Q}.
\]

A sum \(x_1+x_2\) of two CT periodic signals with periods \(T_1,T_2\) is periodic if and only if \(T_1/T_2\) is rational; a common period is then an integer combination of \(T_1\) and \(T_2\).

Time-scaling energy: if \(y(t)=x(at)\) with \(a\neq 0\) and \(x\) finite-energy, then \(E_y=E_x/|a|\). Amplitude scaling: \(E_{Ax}=|A|^2 E_x\) and \(P_{Ax}=|A|^2 P_x\).

Inner product on energy signals:

\[
\langle x,y\rangle=\int_{-\infty}^{\infty} x(t)y^*(t)\,dt
\quad\text{or}\quad
\sum_n x[n]y^*[n],
\qquad
\|x\|^2=\langle x,x\rangle=E_x.
\]

Cauchy–Schwarz then bounds \(|\langle x,y\rangle|^2 \le E_x E_y\). Orthogonal even/odd parts satisfy \(\langle x_e,x_o\rangle=0\) for real signals when the integrals exist, so \(E_x=E_{x_e}+E_{x_o}\).

## Methods

Classify a waveform in a fixed order. First, name the time axis: CT or DT. Second, write the explicit formula including steps and windows so the support is clear. Third, test periodicity by seeking \(T\) or \(N\); if the signal is a sum of sinusoids, test the frequency ratios. Fourth, compute \(E_x\) if the integral or sum is obviously finite (finite support, exponential decay). If energy diverges, compute the power limit. If both diverge, say so. Fifth, extract even and odd parts only when the domain is two-sided; a causal signal that is nonzero only for \(t\ge 0\) is neither even nor odd unless it is identically zero on one side in a compensating way.

To test DT periodicity of \(e^{j\omega n}\), reduce \(\omega\) modulo \(2\pi\) and check whether \(\omega=2\pi(k/N)\) for integers \(k,N\) with \(N>0\). The smallest such \(N\) is the fundamental period when \(k\) and \(N\) are coprime. If \(\omega/\pi\) is irrational, the sequence is not periodic, even though it is almost periodic and bounded.

To compute energy of a piecewise exponential, split the integral at the breakpoints, use \(\int_0^{\infty} e^{-2\alpha t}\,dt=1/(2\alpha)\) for \(\alpha>0\), and include \(|A|^2\). For a rectangular pulse of height \(A\) and width \(\tau\), \(E_x=A^2\tau\) and \(P_x=0\). For a periodic repetition of that pulse with period \(T_0>\tau\), \(P_x=A^2\tau/T_0\).

To form even and odd parts of a causal pulse, extend the formula to negative time by writing \(x(t)\) with \(u(t)\), then apply the definitions. The even part will put half the pulse on each side; the odd part will put a positive half on the right and a negative half on the left. Do not claim a causal pulse is even.

When a problem gives a plot, read the axes. A stem plot is DT. A continuous curve is CT. A staircase that holds between sampling instants is still a CT interpolation, not a sequence, unless the problem states \(x[n]\).

For operations, apply time shift and scale by substituting into the argument, then sketch support. Example: \(x(2t-4)=x\bigl(2(t-2)\bigr)\) is a compression by 2 followed by a delay of 2, or a delay of 4 followed by compression by 2; both descriptions match that algebraic form. Check one breakpoint to confirm.

## Mistakes

Treating \(\delta(t)\) as an ordinary function with \(\delta(0)=\infty\) and using it inside nonlinear maps as if it were a number. The sifting property is the definition that matters; \(\delta^2(t)\) is not a defined distribution in the undergraduate toolkit.

Declaring \(x[n]=\cos(n)\) periodic because a cosine “looks periodic.” Here \(\omega=1\), and \(1/(2\pi)\) is irrational, so the sequence is not periodic.

Using \(P=A^2/2\) for a cosine that is gated on for a finite time. A gated cosine is finite-energy; its power is zero. The \(A^2/2\) formula is the everlasting power.

Writing \(E=\int |x|\,dt\) instead of \(\int |x|^2\,dt\). The \(L^1\) integral is related to BIBO tests on impulse responses, not to signal energy.

Forgetting the \(2N+1\) (or \(2T\)) in the power limit and reporting a one-sided average that is off by a factor of two.

Claiming that every CT sinusoid sum is periodic. \(\cos t+\cos(\sqrt{2}\,t)\) is not periodic.

Mixing \(u(t)\) conventions at \(t=0\) inside an impulse product. \(u(t)\delta(t)\) is subtle; \(f(t)\delta(t)=f(0)\delta(t)\) requires continuity of \(f\) at 0. Prefer writing \(u(t)\) away from a single point or using \(u(t-0^+)\) when a circuit initial-condition argument needs a side.

Calling a sampled everlasting sinusoid an energy signal because a computer array is finite. The mathematical model is infinite-duration unless a window is part of the specification.

Using CT energy formulas on sequences or DT sums on functions of a real variable. The measure is \(dt\) versus counting measure.

Shifting and scaling in the wrong order and then misreading the delay. Always rewrite \(x(at-b)\) as \(x\bigl(a(t-b/a)\bigr)\) to read the physical delay \(b/a\).
