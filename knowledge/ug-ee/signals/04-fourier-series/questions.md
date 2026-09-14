## Q1
### Given
A real periodic signal with period \(T_0=4\) and, on \((-2,2)\), \(x(t)=t\). (Periodic sawtooth extension.)
### Find
The complex CTFS coefficients \(a_k\) for all \(k\), using analysis on \((-2,2)\).
### Solution
\(\omega_0=2\pi/4=\pi/2\). For \(k=0\), \(a_0=\frac{1}{4}\int_{-2}^{2}t\,dt=0\) (odd).

For \(k\neq 0\),

\[
a_k=\frac{1}{4}\int_{-2}^{2}t e^{-jk(\pi/2)t}\,dt.
\]

Integration by parts with \(u=t\), \(dv=e^{-j k\pi t/2}dt\): the boundary term is \(\frac{1}{4}\bigl[t\frac{e^{-jk\pi t/2}}{-jk\pi/2}\bigr]_{-2}^{2}\) plus an integral of an exponential. The endpoints give \(\frac{1}{4}\cdot\frac{2}{-jk\pi/2}\bigl(2e^{-jk\pi}-(-2)e^{jk\pi}\bigr)\). Since \(e^{\pm jk\pi}=(-1)^k\), the parenthesis is \(4(-1)^k\). Then \(\frac{1}{4}\cdot\frac{4(-1)^k}{-j k\pi/2}=\frac{2(-1)^k}{-j k\pi}=\frac{2j(-1)^k}{k\pi}\).

The remaining integral is proportional to \(\int e^{-j k\pi t/2}dt\) over a whole number of cycles and vanishes. Thus \(a_k=\frac{2j(-1)^k}{k\pi}\) for \(k\neq 0\), \(a_0=0\).
### Answer
\(a_0=0\), \(a_k=2j(-1)^k/(k\pi)\) for \(k\neq 0\).

## Q2
### Given
A periodic pulse train: \(x(t)=3\) for \(|t|<1/2\) inside each period of length \(T_0=2\), and 0 on the rest of the period.
### Find
\(a_k\) for all \(k\), and the average power.
### Solution
Duty \(\tau=1\), \(A=3\), \(T_0=2\), \(\omega_0=\pi\). Average \(a_0=3\cdot 1/2=3/2\).

\[
a_k=\frac{3}{2}\operatorname{sinc}\Bigl(\frac{k}{2}\Bigr)=\frac{3}{2}\cdot\frac{\sin(k\pi/2)}{k\pi/2}
=\frac{3\sin(k\pi/2)}{k\pi}\quad(k\neq 0).
\]

Power: \(\frac{1}{2}\int_{-1/2}^{1/2}9\,dt=9/2\). (Parseval would sum the same \(|a_k|^2\).)
### Answer
\(a_0=3/2\), \(a_k=3\sin(k\pi/2)/(k\pi)\) for \(k\neq 0\); \(P_x=9/2\).

## Q3
### Given
DT sequence \(x[n]\) of period \(N=4\) with one period \((x[0],x[1],x[2],x[3])=(2,0,-2,0)\).
### Find
DTFS coefficients \(a_k\) for \(k=0,1,2,3\) with the \(1/N\) on analysis.
### Solution
\(a_k=\frac14\sum_{n=0}^{3}x[n]e^{-j2\pi kn/4}=\frac14\bigl(2-2 e^{-j\pi k}\bigr)=\frac14\bigl(2-2(-1)^k\bigr)\).

So \(a_k=1\) when \(k\) is odd and \(a_k=0\) when \(k\) is even. Explicitly \(a_0=0\), \(a_1=1\), \(a_2=0\), \(a_3=1\).
### Answer
\(a_0=0\), \(a_1=1\), \(a_2=0\), \(a_3=1\).

## Q4
### Given
A stable CT LTI system with \(H(j\omega)=\frac{1}{1+j\omega}\) and periodic input \(x(t)=4\cos(3t)\).
### Find
The steady-state output \(y_{ss}(t)\).
### Solution
Write \(x(t)=2 e^{j3t}+2 e^{-j3t}\), so \(a_1=2\), \(a_{-1}=2\) relative to \(\omega_0=3\), \(T_0=2\pi/3\).

\(H(j3)=\frac{1}{1+j3}\). Magnitude \(1/\sqrt{10}\), phase \(-\arctan 3\).

Then \(y_{ss}(t)=4\cdot\frac{1}{\sqrt{10}}\cos\bigl(3t-\arctan 3\bigr)\).
### Answer
\(y_{ss}(t)=\frac{4}{\sqrt{10}}\cos(3t-\arctan 3)\).

## Q5
### Given
Real CTFS coefficients \(a_0=1\), \(a_1=a_{-1}=2\), \(a_2=a_{-2}=-j/2\), and \(a_k=0\) otherwise, with \(\omega_0=5\).
### Find
A trigonometric expression for \(x(t)\).
### Solution
DC is 1. The pair \(a_{\pm 1}=2\) is \(2e^{j5t}+2e^{-j5t}=4\cos(5t)\).

The pair \(a_2=-j/2\), \(a_{-2}=(+j/2)\) because \(a_{-2}=a_2^*\) for a real signal: \((-j/2)^*=j/2\). Then

\[
a_2 e^{j10t}+a_{-2}e^{-j10t}=\frac{-j}{2}e^{j10t}+\frac{j}{2}e^{-j10t}
=\sin(10t),
\]

using \(\sin\theta=(e^{j\theta}-e^{-j\theta})/(2j)\) and \(-j/2=1/(2j)\). Check: \(1/(2j)=-j/2\), yes, so this is exactly \(\sin(10t)\).
### Answer
\(x(t)=1+4\cos(5t)+\sin(10t)\).

## Q6
### Given
A square wave of period \(2\pi\), \(x(t)=1\) on \((0,\pi)\) and \(x(t)=-1\) on \((\pi,2\pi)\), odd extension.
### Find
\(a_k\) and the power in the fundamental pair \(k=\pm 1\).
### Solution
Odd, period \(2\pi\), \(\omega_0=1\). Cosine (even) coefficients vanish. \(a_0=0\).

\[
a_k=\frac{1}{2\pi}\int_{0}^{\pi}e^{-jkt}dt+\frac{1}{2\pi}\int_{\pi}^{2\pi}(-1)e^{-jkt}dt.
\]

For even \(k\neq 0\) the two intervals cancel. For odd \(k=2m+1\), \(a_k=\frac{2}{j\pi k}\) wait: standard result \(a_k=\frac{1-(-1)^k}{j\pi k}\) for \(k\neq 0\), so \(a_k=\frac{2}{j\pi k}\) for odd \(k\) and 0 for even \(k\neq 0\).

\(|a_1|^2+|a_{-1}|^2=2\cdot\bigl|2/(j\pi)\bigr|^2=2\cdot 4/\pi^2=8/\pi^2\).

Total power is \(\frac{1}{2\pi}\int_0^{2\pi}1\,dt=1\).
### Answer
\(a_k=2/(j\pi k)\) for odd \(k\), else \(0\) (\(k\neq 0\)), \(a_0=0\); fundamental pair power \(8/\pi^2\).
