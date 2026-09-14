## Q1
### Given
\(x(t)=\cos(400\pi t)+\cos(1000\pi t)\) sampled at \(f_s=600\,\mathrm{Hz}\) to form \(x[n]=x(n/f_s)\).
### Find
A simplified expression for \(x[n]\) using only frequencies in \([0,\pi]\), and whether the original \(x(t)\) is recoverable from \(x[n]\) by ideal sinc interpolation at this \(f_s\).
### Solution
Frequencies in hertz: \(200\,\mathrm{Hz}\) and \(500\,\mathrm{Hz}\). Nyquist frequency \(f_s/2=300\,\mathrm{Hz}\). The \(200\,\mathrm{Hz}\) term is unaliased: \(\Omega_1=2\pi\cdot 200/600=2\pi/3\).

The \(500\,\mathrm{Hz}\) term: \(500-600=-100\,\mathrm{Hz}\), equivalent to \(100\,\mathrm{Hz}\) cosine (real even spectrum). \(\Omega_2=2\pi\cdot 100/600=\pi/3\).

So \(x[n]=\cos(2\pi n/3)+\cos(\pi n/3)\). Highest original frequency \(500>300\), copies overlap, not recoverable as the original pair; the interpolator would produce \(\cos(400\pi t)+\cos(200\pi t)\) instead of the \(1000\pi\) term.
### Answer
\(x[n]=\cos(2\pi n/3)+\cos(\pi n/3)\); not recoverable.

## Q2
### Given
A real baseband signal with \(X(j\omega)=0\) for \(|\omega|>8000\pi\) (i.e. \(4\,\mathrm{kHz}\)).
### Find
The Nyquist rate in samples per second, and whether \(f_s=8000\,\mathrm{Hz}\) is sufficient in the strict sense.
### Solution
Highest frequency \(f_m=4000\,\mathrm{Hz}\). Nyquist rate \(2f_m=8000\) samples/s. At exactly \(8000\,\mathrm{Hz}\) the spectral copies touch at \(4\,\mathrm{kHz}\). If \(X\) may contain energy at the single frequency \(4\,\mathrm{kHz}\), a sinusoid at Nyquist can alias with its negative image. Strict recoverability wants \(f_s>8000\,\mathrm{Hz}\) or a guarantee that \(X(j 8000\pi)=0\).
### Answer
Nyquist rate \(8000\,\mathrm{Hz}\); \(f_s=8000\,\mathrm{Hz}\) is the boundary, not strictly sufficient without extra conditions.

## Q3
### Given
Ideal impulse sampling of \(x(t)\) with \(T_s=0.002\,\mathrm{s}\), and \(X(j\omega)=0\) for \(|\omega|>400\pi\).
### Find
Whether copies overlap, and an acceptable cutoff \(\omega_c\) for an ideal reconstruction LPF including the required passband gain.
### Solution
\(\omega_m=400\pi\), \(\omega_s=2\pi/T_s=1000\pi\). Then \(2\omega_m=800\pi<\omega_s\), no overlap. Choose \(\omega_m<\omega_c<\omega_s-\omega_m\), i.e. \(400\pi<\omega_c<600\pi\). Gain \(T_s=0.002\).
### Answer
No overlap; e.g. \(\omega_c=500\pi\,\mathrm{rad/s}\), gain \(0.002\).

## Q4
### Given
Samples \(x(nT_s)\) with \(T_s=1\), and the bandlimited interpolant \(y(t)=\sum_n x(n)\operatorname{sinc}(t-n)\) using \(\operatorname{sinc}\theta=\sin(\pi\theta)/(\pi\theta)\). Suppose \(x(n)=\delta[n]\) (Kronecker).
### Find
\(y(t)\) and \(y(1/2)\).
### Solution
Only the \(n=0\) term survives: \(y(t)=\operatorname{sinc}(t)\). Then \(y(1/2)=\operatorname{sinc}(1/2)=\sin(\pi/2)/(\pi/2)=2/\pi\).
### Answer
\(y(t)=\operatorname{sinc}(t)\), \(y(1/2)=2/\pi\).

## Q5
### Given
A sinusoid \(x(t)=\cos(2\pi\cdot 450 t)\) sampled at \(f_s=400\,\mathrm{Hz}\).
### Find
The principal alias frequency in hertz in \([-200,200]\) and the discrete-time sequence.
### Solution
\(450-400=50\,\mathrm{Hz}\) lies in \([-200,200]\). Thus \(x[n]=\cos(2\pi\cdot 50\cdot n/400)=\cos(\pi n/4)\).
### Answer
\(50\,\mathrm{Hz}\); \(x[n]=\cos(\pi n/4)\).

## Q6
### Given
Two candidate rates \(f_s=8\,\mathrm{kHz}\) and \(f_s=12\,\mathrm{kHz}\) for a real signal occupying \(0\) to \(5\,\mathrm{kHz}\).
### Find
Which rates, if either, satisfy the baseband sampling theorem, and the principal alias of a \(5\,\mathrm{kHz}\) tone at \(8\,\mathrm{kHz}\) sampling.
### Solution
Need \(f_s>10\,\mathrm{kHz}\). So \(8\,\mathrm{kHz}\) fails, \(12\,\mathrm{kHz}\) succeeds. At \(8\,\mathrm{kHz}\), a \(5\,\mathrm{kHz}\) tone aliases to \(5-8=-3\,\mathrm{kHz}\), i.e. a \(3\,\mathrm{kHz}\) cosine.
### Answer
Only \(12\,\mathrm{kHz}\) works; alias of \(5\,\mathrm{kHz}\) at \(f_s=8\,\mathrm{kHz}\) is \(3\,\mathrm{kHz}\).
