## Q1
### Given
The continuous-time signal \(x(t)=4e^{-3t}u(t)+2e^{2t}u(-t)\).
### Find
The energy \(E_x\) and the power \(P_x\). Classify as energy, power, or neither.
### Solution
Split the energy integral at \(t=0\):

\[
E_x=\int_{-\infty}^{0}|2e^{2t}|^2\,dt+\int_{0}^{\infty}|4e^{-3t}|^2\,dt
=\int_{-\infty}^{0}4e^{4t}\,dt+\int_{0}^{\infty}16e^{-6t}\,dt.
\]

The first integral is \(4\cdot\frac{1}{4}=1\). The second is \(16\cdot\frac{1}{6}=\frac{8}{3}\). Thus \(E_x=1+\frac{8}{3}=\frac{11}{3}\), which is finite and positive. The power of any finite-energy signal is zero: the \(1/(2T)\) average of a finite integral vanishes as \(T\to\infty\).
### Answer
\(E_x=11/3\), \(P_x=0\); finite-energy signal.

## Q2
### Given
The discrete-time signal \(x[n]=\cos(3\pi n/8)+\sin(3\pi n/4)\).
### Find
Whether \(x[n]\) is periodic and, if so, the fundamental period \(N\).
### Solution
A complex exponential \(e^{j\omega n}\) (hence a real sinusoid of that \(\omega\)) is periodic iff \(\omega/(2\pi)\) is rational.

For \(\cos(3\pi n/8)\), \(\omega_1=3\pi/8\), so \(\omega_1/(2\pi)=3/16\), already rational. The smallest positive integer \(N_1\) with \(N_1\cdot(3\pi/8)=2\pi k\) for some integer \(k\) is \(N_1=16\) with \(k=3\).

For \(\sin(3\pi n/4)\), \(\omega_2=3\pi/4\), \(\omega_2/(2\pi)=3/8\). Then \(N_2\cdot(3\pi/4)=2\pi m\) gives \(N_2=8\) when \(m=3\).

A common period is \(\mathrm{lcm}(16,8)=16\). No smaller positive common period works for the first term, so the fundamental period of the sum is 16.
### Answer
Periodic with fundamental period \(N=16\).

## Q3
### Given
\(x(t)=3\operatorname{rect}(t/2)\) where \(\operatorname{rect}(\theta)=1\) for \(|\theta|<1/2\), \(1/2\) at \(|\theta|=1/2\), and 0 otherwise.
### Find
The even and odd parts of \(x(t)\), and \(E_x\).
### Solution
\(\operatorname{rect}(t/2)\) equals 1 for \(|t|<1\), so \(x(t)\) is a pulse of height 3 on \((-1,1)\). This waveform is even: \(x(-t)=x(t)\). Therefore \(x_e(t)=x(t)\) and \(x_o(t)=0\).

Energy: \(E_x=\int_{-1}^{1}9\,dt=18\). The two endpoints have measure zero.
### Answer
\(x_e=x\), \(x_o=0\), \(E_x=18\).

## Q4
### Given
\(x[n]=(-1)^n u[n]\).
### Find
Energy, power, and whether the sequence is periodic for \(n\in\mathbb{Z}\) after extending the same formula without \(u[n]\), i.e. compare \(y[n]=(-1)^n\) with \(x[n]\).
### Solution
For \(x[n]\), \(|x[n]|^2=1\) for all \(n\ge 0\) and 0 for \(n<0\). The energy sum \(\sum_{n=0}^{\infty}1\) diverges, so \(E_x=\infty\). The power is

\[
P_x=\lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=0}^{N}1=\lim_{N\to\infty}\frac{N+1}{2N+1}=\frac12.
\]

So \(x\) is a finite-power, one-sided sequence and is not periodic on \(\mathbb{Z}\) because the left side is identically zero while the right side alternates.

The two-sided \(y[n]=(-1)^n\) satisfies \(y[n+2]=y[n]\) for all \(n\), so it is periodic with fundamental period 2. Its energy is infinite and its power is \(1\).
### Answer
\(x\): \(E=\infty\), \(P=1/2\), not periodic. \(y\): periodic with \(N=2\), \(P=1\).

## Q5
### Given
\(x(t)=\cos(2t)+\cos(\pi t)\).
### Find
Whether \(x(t)\) is periodic, and if so a fundamental period.
### Solution
Periods of the summands: \(T_1=\pi\) for \(\cos(2t)\) because \(2(T_1)=2\pi\); \(T_2=2\) for \(\cos(\pi t)\) because \(\pi T_2=2\pi\). The ratio \(T_1/T_2=\pi/2\) is irrational. No integers \(m,k\) satisfy \(m\pi=2k\) except the trivial zero, so there is no common period. The sum is not periodic.
### Answer
Not periodic.

## Q6
### Given
A discrete pulse \(x[n]=5\) for \(n=0,1,2\) and \(x[n]=0\) otherwise.
### Find
\(E_x\), \(P_x\), and the energy of the even part of \(x\).
### Solution
\(E_x=3\cdot 25=75\). Finite energy implies \(P_x=0\).

Even part: \(x_e[n]=\frac12(x[n]+x[-n])\). Then \(x_e[0]=5\), \(x_e[1]=x_e[-1]=\frac52\), \(x_e[2]=x_e[-2]=\frac52\), and 0 elsewhere. Energy of the even part:

\[
E_{x_e}=25+2\cdot\Bigl(\frac{25}{4}\Bigr)+2\cdot\Bigl(\frac{25}{4}\Bigr)=25+\frac{25}{2}+\frac{25}{2}=50.
\]

(The odd part carries the remaining 25, and \(E_x=E_{x_e}+E_{x_o}\) for this real finite-energy sequence.)
### Answer
\(E_x=75\), \(P_x=0\), \(E_{x_e}=50\).
