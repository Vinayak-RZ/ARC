## Q1
### Given
\(x(t)=e^{-3t}u(t)+e^{2t}u(-t)\).
### Find
\(X(s)\) and the ROC.
### Solution
The causal term \(e^{-3t}u(t)\) transforms to \(1/(s+3)\) with \(\operatorname{Re}s>-3\).

The anticausal term \(e^{2t}u(-t)\) equals \(-(-e^{2t}u(-t))\). Pair: \(-e^{at}u(-t)\leftrightarrow 1/(s-a)\) with \(\operatorname{Re}s<a\). Here \(a=2\), so \(e^{2t}u(-t)\leftrightarrow -1/(s-2)\) with \(\operatorname{Re}s<2\).

Sum: \(X(s)=\frac{1}{s+3}-\frac{1}{s-2}\) with ROC the intersection \(-3<\operatorname{Re}s<2\).

Combined algebra: \(X(s)=\frac{(s-2)-(s+3)}{(s+3)(s-2)}=\frac{-5}{(s+3)(s-2)}\) on that strip.
### Answer
\(X(s)=-5/((s+3)(s-2))\), ROC \(-3<\operatorname{Re}s<2\).

## Q2
### Given
\(X(s)=\frac{1}{(s+1)(s-4)}\) with ROC \(\operatorname{Re}s>4\).
### Find
\(x(t)\).
### Solution
Partial fractions: \(\frac{1}{(s+1)(s-4)}=\frac{A}{s+1}+\frac{B}{s-4}\). Cover-up: \(A=-1/5\), \(B=1/5\).

ROC is to the right of both poles, so both terms are causal:

\[
x(t)=\frac15\bigl(e^{4t}-e^{-t}\bigr)u(t).
\]
### Answer
\(x(t)=\frac15(e^{4t}-e^{-t})u(t)\).

## Q3
### Given
The same \(X(s)=\frac{1}{(s+1)(s-4)}\) but ROC \(-1<\operatorname{Re}s<4\).
### Find
\(x(t)\).
### Solution
Same residues \(A=-1/5\), \(B=1/5\). Now the ROC lies to the right of \(s=-1\) (causal for that pole) and to the left of \(s=4\) (anticausal for that pole):

\[
x(t)=-\frac15 e^{-t}u(t)-\frac15 e^{4t}u(-t).
\]

(The second term uses \(-B e^{4t}u(-t)\) because \(B/(s-4)\) with left-sided ROC inverts to \(-B e^{4t}u(-t)\).)
### Answer
\(x(t)=-\frac15 e^{-t}u(t)-\frac15 e^{4t}u(-t)\).

## Q4
### Given
A causal LTI system \(H(s)=\frac{s+2}{s^2+3s+2}\) and input \(x(t)=u(t)\), rest initial conditions.
### Find
\(y(t)\) for \(t\ge 0\).
### Solution
Poles at \(s=-1,-2\). Causal, both in the open left half-plane, so stable. \(X(s)=1/s\), \(Y(s)=\frac{s+2}{s(s+1)(s+2)}=\frac{1}{s(s+1)}\) after canceling \(s+2\) (valid for this input path; the cancelled mode is not excited).

\(Y(s)=\frac{1}{s}-\frac{1}{s+1}\), so \(y(t)=(1-e^{-t})u(t)\).
### Answer
\(y(t)=(1-e^{-t})u(t)\).

## Q5
### Given
Unilateral Laplace, \(x(t)\) causal, \(X(s)=\frac{2s+6}{s^2+4s+3}\).
### Find
\(x(0^+)\) and \(x(\infty)\) by the initial- and final-value theorems, then invert to check.
### Solution
Initial: \(\lim_{s\to\infty}sX(s)=\lim_{s\to\infty}\frac{2s^2+6s}{s^2+4s+3}=2\).

Final: poles of \(sX(s)=\frac{s(2s+6)}{(s+1)(s+3)}\) at \(-1,-3\), both stable. \(\lim_{s\to 0}sX(s)=0\).

Inversion: \(\frac{2s+6}{(s+1)(s+3)}=\frac{A}{s+1}+\frac{B}{s+3}\), \(A=(2(-1)+6)/((-1)+3)=2\), \(B=(2(-3)+6)/((-3)+1)=0\). So \(x(t)=2e^{-t}u(t)\). Then \(x(0^+)=2\), \(x(\infty)=0\), matching both theorems. (A common error is to evaluate \(X(0)\) instead of \(sX(s)\) at \(0\).)
### Answer
\(x(0^+)=2\), \(x(\infty)=0\); \(x(t)=2e^{-t}u(t)\).

## Q6
### Given
\(h(t)=-e^{5t}u(-t)\).
### Find
\(H(s)\), ROC, and whether the Fourier transform \(H(j\omega)\) exists as an ordinary function.
### Solution
This is the anticausal pair for pole at \(s=5\): \(H(s)=1/(s-5)\) with \(\operatorname{Re}s<5\). The \(j\omega\) axis has \(\operatorname{Re}s=0<5\), so it lies in the ROC. \(H(j\omega)=1/(j\omega-5)\) exists as an ordinary square-integrable function (the impulse response is in \(L^1\) because \(|h(t)|=e^{5t}\) for \(t<0\), and \(\int_{-\infty}^{0}e^{5t}dt=1/5<\infty\)).
### Answer
\(H(s)=1/(s-5)\), \(\operatorname{Re}s<5\); yes, \(H(j\omega)=1/(j\omega-5)\).
