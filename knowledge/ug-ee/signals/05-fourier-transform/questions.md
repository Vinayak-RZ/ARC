## Q1
### Given
\(x(t)=e^{-4t}u(t)\).
### Find
\(X(j\omega)\) and the energy \(E_x\) two ways (time and Parseval).
### Solution
\(X(j\omega)=\int_0^{\infty}e^{-4t}e^{-j\omega t}dt=1/(4+j\omega)\).

Time energy: \(\int_0^{\infty}e^{-8t}dt=1/8\).

Parseval: \(\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{1}{16+\omega^2}\,d\omega=\frac{1}{2\pi}\cdot\frac{1}{4}\arctan(\omega/4)\Big|_{-\infty}^{\infty}=\frac{1}{8}\).
### Answer
\(X(j\omega)=1/(4+j\omega)\), \(E_x=1/8\).

## Q2
### Given
A pulse \(x(t)=2\) for \(|t|\le 3\) and \(0\) otherwise.
### Find
\(X(j\omega)\) and the frequencies where \(X=0\).
### Solution
\[
X(j\omega)=\int_{-3}^{3}2e^{-j\omega t}dt=2\cdot\frac{2\sin(3\omega)}{\omega}=4\cdot 3\cdot\frac{\sin(3\omega)}{3\omega}=12\operatorname{sinc}\Bigl(\frac{3\omega}{\pi}\Bigr)
\]

if \(\operatorname{sinc}\theta=\sin(\pi\theta)/(\pi\theta)\). Zeros when \(3\omega=m\pi\) for integer \(m\neq 0\), i.e. \(\omega=m\pi/3\), \(m=\pm 1,\pm 2,\ldots\). At \(\omega=0\), \(X=12\).
### Answer
\(X(j\omega)=12\sin(3\omega)/(3\omega)\) for \(\omega\neq 0\), \(X(0)=12\); zeros at \(m\pi/3\), \(m\neq 0\).

## Q3
### Given
\(x(t)=\operatorname{rect}(t)\) with transform \(X(j\omega)=\operatorname{sinc}(\omega/(2\pi))\) in the \(\sin(\pi\theta)/(\pi\theta)\) convention, and \(y(t)=x(t)\cos(50t)\).
### Find
\(Y(j\omega)\) in terms of \(X\).
### Solution
\(\cos(50t)=\frac12(e^{j50t}+e^{-j50t})\). Modulation gives

\[
Y(j\omega)=\frac12 X\bigl(j(\omega-50)\bigr)+\frac12 X\bigl(j(\omega+50)\bigr).
\]
### Answer
\(Y(j\omega)=\frac12 X(j(\omega-50))+\frac12 X(j(\omega+50))\).

## Q4
### Given
\(h(t)=e^{-t}u(t)\) and \(x(t)=e^{-t}u(t)\).
### Find
The Fourier transform of \(y=x*h\) using the convolution theorem, then invert.
### Solution
\(X(j\omega)=H(j\omega)=1/(1+j\omega)\), so \(Y(j\omega)=1/(1+j\omega)^2\).

Inverse: \(t e^{-t}u(t)\) has transform \(1/(1+j\omega)^2\). Thus \(y(t)=t e^{-t}u(t)\).
### Answer
\(Y(j\omega)=1/(1+j\omega)^2\), \(y(t)=t e^{-t}u(t)\).

## Q5
### Given
Real energy signal with \(X(j\omega)=0\) for \(|\omega|>10\), and \(\int_{-\infty}^{\infty}|x(t)|^2 dt=5\).
### Find
\(\frac{1}{2\pi}\int_{-10}^{10}|X(j\omega)|^2\,d\omega\) and \(\int_{0}^{\infty}|x(t)|^2 dt\) if also \(x\) is even.
### Solution
Parseval plus the bandlimit give \(\frac{1}{2\pi}\int_{-10}^{10}|X|^2=5\). If \(x\) is even and real it is not necessarily one-sided in time; even means \(x(-t)=x(t)\), so energy on the positive axis is half of the total minus half of the origin, i.e. \(5/2\).
### Answer
The frequency integral equals 5; if \(x\) is even, \(\int_0^{\infty}|x|^2=5/2\).

## Q6
### Given
\(x(t)=\delta(t-2)-\delta(t+2)\).
### Find
\(X(j\omega)\) and whether \(x\) is even or odd.
### Solution
\(X(j\omega)=e^{-j2\omega}-e^{j2\omega}=-2j\sin(2\omega)\). The time signal is odd: \(x(-t)=\delta(-t-2)-\delta(-t+2)=\delta(t+2)-\delta(t-2)=-x(t)\). The transform is purely imaginary and odd in \(\omega\), consistent with a real odd signal.
### Answer
\(X(j\omega)=-2j\sin(2\omega)\); odd.
