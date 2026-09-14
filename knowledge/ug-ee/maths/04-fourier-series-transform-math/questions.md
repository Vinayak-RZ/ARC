# Questions — Fourier analysis as maths

## Q1

### Given

Period \(T_0=2\ \mathrm{s}\). One period: \(x(t)=1\) for \(0<t<1\), \(x(t)=0\) for \(1<t<2\). (Periodic pulse train, duty \(1/2\).)

### Find

Complex coefficients \(c_n\) for all integers \(n\), including \(c_0\).

### Solution

\(\omega_0=2\pi/T_0=\pi\ \mathrm{rad/s}\). Average:
\[
c_0=\frac{1}{2}\int_0^1 1\,dt=\frac12.
\]
For \(n\neq 0\):
\[
c_n=\frac{1}{2}\int_0^1 e^{-jn\pi t}\,dt=\frac{1}{2}\cdot\frac{1-e^{-jn\pi}}{jn\pi}.
\]
\(e^{-jn\pi}=(-1)^n\). For even \(n\neq 0\), \(1-(-1)^n=0\), so \(c_n=0\). For odd \(n\), \(1-(-1)=2\),
\[
c_n=\frac{1}{2}\cdot\frac{2}{jn\pi}=\frac{1}{jn\pi}.
\]
Equivalently \(c_n=e^{-jn\pi/2}\sin(n\pi/2)/(n\pi)\) by factoring a delay of \(0.5\ \mathrm{s}\) on a centred pulse; the odd-\(n\) result \(1/(jn\pi)\) is enough.

### Answer

\(c_0=1/2\); \(c_n=0\) for even \(n\neq 0\); \(c_n=1/(jn\pi)\) for odd \(n\)

## Q2

### Given

\(x(t)=4\cos(50t)+3\sin(50t)\) (a single-frequency real sinusoid).

### Find

The two-sided Fourier-series coefficients at \(\omega_0=50\) (treat the period as \(2\pi/50\)), i.e. \(c_{-1},c_0,c_1\).

### Solution

Rewrite:
\[
4\cos 50t = 2e^{j50t}+2e^{-j50t},\qquad 3\sin 50t = \frac{3}{2j}(e^{j50t}-e^{-j50t})=-j\frac{3}{2}e^{j50t}+j\frac{3}{2}e^{-j50t}.
\]
\[
c_1=2-j\tfrac32,\qquad c_{-1}=2+j\tfrac32,\qquad c_0=0.
\]
Check: \(|c_1|=\sqrt{4+2.25}=\sqrt{6.25}=2.5\), and amplitude of the sine-cosine pair is \(\sqrt{4^2+3^2}=5=2|c_1|\).

### Answer

\(c_1=2-j1.5\), \(c_{-1}=2+j1.5\), \(c_0=0\)

## Q3

### Given

\(x(t)=e^{-3t}u(t)\).

### Find

The Fourier transform \(X(j\omega)\) in rectangular form, and \(|X(j\omega)|\) at \(\omega=0\) and as \(\omega\to\infty\).

### Solution

\[
X(j\omega)=\int_0^\infty e^{-3t}e^{-j\omega t}\,dt=\frac{1}{3+j\omega}=\frac{3}{9+\omega^2}-j\frac{\omega}{9+\omega^2}.
\]
\(|X(j0)|=1/3\). As \(\omega\to\infty\), \(|X|\sim 1/|\omega|\to 0\).

### Answer

\(X(j\omega)=1/(3+j\omega)\); \(|X(j0)|=1/3\); \(|X(j\omega)|\to 0\) as \(\omega\to\infty\)

## Q4

### Given

The centred rect: \(x(t)=2\) for \(|t|<0.05\ \mathrm{s}\), \(x(t)=0\) otherwise.

### Find

\(X(j\omega)\) and the frequencies in hertz of the first spectral zeros (smallest \(|f|>0\)).

### Solution

Width \(\tau=0.1\ \mathrm{s}\), height \(A=2\):
\[
X(j\omega)=2\cdot 0.1\cdot\frac{\sin(\omega\cdot 0.05)}{\omega\cdot 0.05}=\frac{0.2\sin(0.05\omega)}{0.05\omega}.
\]
Zeros when \(0.05\omega=k\pi\) for integer \(k\neq 0\), i.e. \(\omega=20\pi k\ \mathrm{rad/s}\), \(f=10k\ \mathrm{Hz}\). First zeros at \(\pm 10\ \mathrm{Hz}\).

### Answer

\(X(j\omega)=0.2\sin(0.05\omega)/(0.05\omega)\); first zeros at \(f=\pm 10\ \mathrm{Hz}\)

## Q5

### Given

Periodic \(x\) with \(c_0=1\), \(c_{\pm 1}=0.5\), \(c_{\pm 2}=0.2\), all other \(c_n=0\). (Real, even harmonics specified conjugate-symmetric.)

### Find

Average power \(P=\sum |c_n|^2\).

### Solution

\[
P=|c_0|^2+|c_1|^2+|c_{-1}|^2+|c_2|^2+|c_{-2}|^2=1+0.25+0.25+0.04+0.04=1.58.
\]

### Answer

\(P=1.58\) (in the squared-amplitude units of \(x\))
