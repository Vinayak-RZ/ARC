# Questions — Laplace transforms

## Q1

### Given

\(f(t)=3e^{-2t}u(t)+2\delta(t)\).

### Find

\(F(s)=\mathcal{L}\{f\}(s)\) (unilateral).

### Solution

Linearity and the table:
\[
\mathcal{L}\{e^{-2t}u(t)\}=\frac{1}{s+2},\qquad \mathcal{L}\{\delta(t)\}=1.
\]
\[
F(s)=\frac{3}{s+2}+2.
\]
As a single rational function:
\[
F(s)=\frac{2(s+2)+3}{s+2}=\frac{2s+7}{s+2}.
\]

### Answer

\(F(s)=2+3/(s+2)=(2s+7)/(s+2)\)

## Q2

### Given

\(\ddot{y}+3\dot{y}+2y=u(t)\), \(y(0^-)=1\), \(\dot{y}(0^-)=0\).

### Find

\(Y(s)\) and \(y(t)\) for \(t>0\).

### Solution

Laplace of the ODE:
\[
\big(s^2 Y-s y(0^-)-\dot{y}(0^-)\big)+3\big(sY-y(0^-)\big)+2Y=\frac{1}{s}.
\]
\[
(s^2+3s+2)Y - s - 3 = \frac{1}{s}.
\]
\[
(s+1)(s+2)Y = s+3+\frac{1}{s}=\frac{s(s+3)+1}{s}=\frac{s^2+3s+1}{s}.
\]
\[
Y(s)=\frac{s^2+3s+1}{s(s+1)(s+2)}.
\]
Partial fractions:
\[
Y=\frac{A}{s}+\frac{B}{s+1}+\frac{C}{s+2}.
\]
Cover-up: \(A=(1)/(1\cdot 2)=1/2\). \(B=(1-3+1)/((-1)(1))=(-1)/(-1)=1\). \(C=(4-6+1)/((-2)(-1))=(-1)/2=-1/2\).
Check \(B\): numerator at \(s=-1\) is \(1-3+1=-1\), denominator without \((s+1)\) is \(s(s+2)=(-1)(1)=-1\), \(B=(-1)/(-1)=1\). Yes.
\[
y(t)=\big(\tfrac12 + e^{-t} - \tfrac12 e^{-2t}\big)u(t).
\]
Initial-value check: \(sY(s)\to 1\) as \(s\to\infty\), matches \(y(0^+)=1\) (no impulse, states continuous in this second-order form with finite right-hand side). Final value: \(sY\to 1/2\), and \(y(\infty)=1/2\), which is the DC gain \(1/2\) of \(1/(s^2+3s+2)\) times a unit step.

### Answer

\(Y(s)=(s^2+3s+1)/(s(s+1)(s+2))\), \(y(t)=(1/2+e^{-t}-e^{-2t}/2)u(t)\)

## Q3

### Given

\(F(s)=\dfrac{s+3}{(s+1)^2+4}\).

### Find

The causal inverse \(f(t)\).

### Solution

Complete the square already: \((s+1)^2+2^2\). Write
\[
F(s)=\frac{(s+1)+2}{(s+1)^2+4}=\frac{s+1}{(s+1)^2+4}+\frac{2}{(s+1)^2+4}.
\]
Table: \(e^{-t}\cos 2t\) and \(e^{-t}\sin 2t\), the sine row needing a 2 in the numerator for \(\omega=2\):
\[
f(t)=\big(e^{-t}\cos 2t + e^{-t}\sin 2t\big)u(t)=e^{-t}(\cos 2t+\sin 2t)\,u(t).
\]

### Answer

\(f(t)=e^{-t}(\cos 2t+\sin 2t)\,u(t)\)

## Q4

### Given

\(Y(s)=\dfrac{10}{s(s^2+4)}\).

### Find

Whether the final-value theorem applies, and \(y(t)\) for \(t>0\).

### Solution

Poles of \(Y\) at \(0,\ \pm j2\). Poles of \(sY(s)=10/(s^2+4)\) at \(\pm j2\), on the imaginary axis, not in the open left half-plane. Final-value theorem does **not** apply; \(y(t)\) has a persistent sinusoid.
Partial fractions:
\[
Y=\frac{A}{s}+\frac{Bs+C}{s^2+4}.
\]
\(A=10/4=2.5\). Then \(2.5(s^2+4)+Bs^2+Cs=10\), so \((2.5+B)s^2+Cs+10=10\). Thus \(C=0\), \(B=-2.5\).
\[
Y=\frac{2.5}{s}-\frac{2.5 s}{s^2+4}.
\]
\[
y(t)=\big(2.5 - 2.5\cos 2t\big)u(t).
\]
No single final value exists; the waveform oscillates between \(0\) and \(5\).

### Answer

FVT does not apply; \(y(t)=2.5(1-\cos 2t)\,u(t)\)

## Q5

### Given

Causal convolution: \(f(t)=e^{-t}u(t)\), \(g(t)=u(t)\).

### Find

\((f*g)(t)\) for \(t>0\) two ways: product of transforms, and the time integral.

### Solution

\(F(s)=1/(s+1)\), \(G(s)=1/s\), product \(1/(s(s+1))=1/s-1/(s+1)\). Inverse:
\[
(f*g)(t)=(1-e^{-t})u(t).
\]
Time domain for \(t>0\):
\[
\int_0^t e^{-\tau}\,d\tau = 1-e^{-t}.
\]
The two methods agree.

### Answer

\((f*g)(t)=(1-e^{-t})u(t)\) for \(t>0\)
