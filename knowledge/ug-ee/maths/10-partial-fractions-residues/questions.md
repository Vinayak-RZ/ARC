# Questions — Partial fractions and residues

## Q1

### Given

\(F(s)=\dfrac{s+4}{(s+1)(s+2)}\), strictly proper, distinct simple poles.

### Find

Partial-fraction coefficients and the causal inverse \(f(t)\).

### Solution

\[
F(s)=\frac{A}{s+1}+\frac{B}{s+2}.
\]
Cover-up: \(A=(4-1)/(2-1)=3\), \(B=(4-2)/(-2+1)=2/(-1)=-2\).
Check: \(A+B=1\) matches leading numerator/denominator \(s/s^2\).
\[
f(t)=(3e^{-t}-2e^{-2t})u(t).
\]
Residue form: \(\operatorname{Res}(F,-1)=3\), \(\operatorname{Res}(F,-2)=-2\).

### Answer

\(F=3/(s+1)-2/(s+2)\); \(f(t)=(3e^{-t}-2e^{-2t})u(t)\)

## Q2

### Given

\(F(s)=\dfrac{1}{(s+2)^2(s+5)}\).

### Find

The expansion including the repeated-pole terms, and \(f(t)\).

### Solution

\[
F=\frac{A}{(s+2)^2}+\frac{B}{s+2}+\frac{C}{s+5}.
\]
\(A=(s+2)^2 F|_{s=-2}=1/(-2+5)=1/3\).
\(C=1/(-5+2)^2=1/9\).
\(B=\frac{d}{ds}[(s+2)^2 F]_{s=-2}=\frac{d}{ds}[1/(s+5)]_{s=-2}=-1/(s+5)^2|_{s=-2}=-1/9\).
Check: \(B+C=0\) so no \(1/s\) at infinity from those; equivalently equate \(s^0\): \(A\cdot 1 + \cdots\).
\[
f(t)=\Big(\frac13 t e^{-2t} -\frac19 e^{-2t} +\frac19 e^{-5t}\Big)u(t).
\]

### Answer

\(A=1/3\), \(B=-1/9\), \(C=1/9\); \(f(t)=\big(\tfrac13 t e^{-2t}-\tfrac19 e^{-2t}+\tfrac19 e^{-5t}\big)u(t)\)

## Q3

### Given

\(F(s)=\dfrac{2s+6}{s^2+2s+5}\).

### Find

A real inverse \(f(t)\) by completing the square (do not leave complex residues uncombined).

### Solution

\(s^2+2s+5=(s+1)^2+4\). Numerator \(2(s+1)+4\):
\[
F=\frac{2(s+1)+4}{(s+1)^2+2^2}=2\cdot\frac{s+1}{(s+1)^2+4}+2\cdot\frac{2}{(s+1)^2+4}.
\]
\[
f(t)=\big(2e^{-t}\cos 2t + 2e^{-t}\sin 2t\big)u(t)=2e^{-t}(\cos 2t+\sin 2t)\,u(t).
\]
Complex check: poles \(-1\pm j2\). Residue at \(-1+j2\):
\[
K=\frac{2(-1+j2)+6}{2j2}=\frac{4+j4}{j4}=\frac{1+j}{j}=-j(1+j)=1-j
\]
after \(1/j=-j\). Then \(2\operatorname{Re}(K e^{(-1+j2)t})=2e^{-t}\operatorname{Re}((1-j)(\cos 2t+j\sin 2t))=2e^{-t}(\cos 2t+\sin 2t)\). Matches.

### Answer

\(f(t)=2e^{-t}(\cos 2t+\sin 2t)\,u(t)\)

## Q4

### Given

\(X(z)=\dfrac{z}{(z-1)(z-0.5)}\), causal ROC \(|z|>1\). Invert by expanding \(X(z)/z\).

### Find

\(x[n]\) for \(n\ge 0\).

### Solution

\[
\frac{X(z)}{z}=\frac{1}{(z-1)(z-0.5)}=\frac{A}{z-1}+\frac{B}{z-0.5}.
\]
\(A=1/(1-0.5)=2\), \(B=1/(0.5-1)=-2\).
\[
X(z)=\frac{2z}{z-1}-\frac{2z}{z-0.5}.
\]
\[
x[n]=\big(2-2(0.5)^n\big)u[n].
\]

### Answer

\(x[n]=2\big(1-(1/2)^n\big)u[n]\)

## Q5

### Given

Simple closed contour \(C\) the circle \(|s|=3\) positively oriented. \(F(s)=\dfrac{e^{s}}{s(s-1)}\).

### Find

\(\oint_C F(s)\,ds\) using residues. (Poles at \(0\) and \(1\) both lie inside \(|s|=3\); \(e^{s}\) entire.)

### Solution

Simple poles. \(\operatorname{Res}(F,0)=e^{0}/(0-1)=-1\). \(\operatorname{Res}(F,1)=e^{1}/(1)=e\).
Residue theorem:
\[
\oint_C F=2\pi j\big(-1+e\big)=2\pi j(e-1).
\]

### Answer

\(2\pi j(e-1)\)
