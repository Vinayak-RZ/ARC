## Q1
### Given
\(h(t)=e^{-2t}u(t)+e^{3t}u(-t)\).
### Find
Whether the LTI system is causal and whether it is BIBO stable.
### Solution
Support of \(h\) includes \(t<0\) (the \(e^{3t}u(-t)\) term), so noncausal.

Absolute integral: \(\int_0^{\infty}e^{-2t}dt=1/2\), and \(\int_{-\infty}^{0}e^{3t}dt=1/3\), both finite. \(\|h\|_1=5/6<\infty\), BIBO stable.

ROC of \(H(s)\) is \(-2<\operatorname{Re}s<3\), which includes the \(j\omega\) axis, consistent with stability.
### Answer
Noncausal; BIBO stable.

## Q2
### Given
Causal \(H(s)=\frac{s-4}{(s+1)(s-2)}\).
### Find
BIBO stability of the causal system, and the ROC.
### Solution
Causal ROC is to the right of the rightmost pole, \(\operatorname{Re}s>2\). The \(j\omega\) axis is not in the ROC. The pole at \(s=2\) lies in the right half-plane. Not BIBO stable.

(The zero at \(s=4\) does not cancel that pole.)
### Answer
Not BIBO stable; ROC \(\operatorname{Re}s>2\).

## Q3
### Given
The same algebra \(H(s)=\frac{s-4}{(s+1)(s-2)}\) with ROC \(-1<\operatorname{Re}s<2\).
### Find
Causality, BIBO stability, and a sketch of which poles are causal versus anticausal.
### Solution
The ROC is a strip, so \(h\) is two-sided: pole at \(-1\) is to the left of the ROC (causal exponential \(e^{-t}u(t)\)), pole at \(+2\) is to the right (anticausal). Not causal.

The \(j\omega\) axis lies in the strip, so the CTFT exists in \(L^1\) sense if residues cooperate: yes, both exponentials decay away from the origin in their half-lines. BIBO stable and noncausal.
### Answer
Noncausal; BIBO stable.

## Q4
### Given
Discrete \(h[n]=(1.2)^n u[n]\).
### Find
Causality and BIBO stability, and whether \(H(e^{j\Omega})\) exists as an ordinary DTFT.
### Solution
Supported on \(n\ge 0\): causal. \(\sum |h[n]|=\sum (1.2)^n\) diverges. Not BIBO. ROC \(|z|>1.2\) excludes the unit circle, so no ordinary DTFT.
### Answer
Causal, not BIBO; ordinary DTFT does not exist.

## Q5
### Given
Memoryless system \(y(t)=\sin\bigl(x(t)\bigr)\).
### Find
Whether the system is BIBO stable, linear, and causal.
### Solution
If \(|x|\le M\), then \(|y|\le 1\), so BIBO. Not linear: \(\sin(2x)\neq 2\sin x\) in general. Memoryless implies causal.
### Answer
BIBO stable, nonlinear, causal.

## Q6
### Given
Causal discrete filter \(H(z)=\frac{1}{(1-\frac12 z^{-1})(1-2z^{-1})}\).
### Find
The causal \(h[n]\) in closed form and BIBO stability.
### Solution
Poles at \(z=1/2\) and \(z=2\). Causal ROC \(|z|>2\). Partial fractions in \(z^{-1}\):

\[
H(z)=\frac{A}{1-\frac12 z^{-1}}+\frac{B}{1-2z^{-1}}.
\]

Cover-up: \(A=1/(1-2\cdot 2)=-1/3\) at \(z^{-1}=2\). \(B=1/(1-\frac12\cdot\frac12)=4/3\) at \(z^{-1}=1/2\).

Causal: \(h[n]=\bigl[-\frac13(\frac12)^n+\frac43 2^n\bigr]u[n]\). The \(2^n\) term grows. Not BIBO.
### Answer
\(h[n]=\bigl(-\frac13(\frac12)^n+\frac43 2^n\bigr)u[n]\); not BIBO stable.
