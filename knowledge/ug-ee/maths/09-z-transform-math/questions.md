# Questions — Z as a transform pair

## Q1

### Given

Causal sequence \(x[n]=(1/3)^n u[n]\).

### Find

\(X(z)\) as a rational function of \(z\), and the ROC.

### Solution

Geometric series:
\[
X(z)=\sum_{n=0}^\infty \left(\frac{1}{3}z^{-1}\right)^n=\frac{1}{1-\frac13 z^{-1}},\qquad \left|\frac13 z^{-1}\right|<1\ \Rightarrow\ |z|>\frac13.
\]
Equivalently \(X(z)=z/(z-1/3)\), ROC \(|z|>1/3\).

### Answer

\(X(z)=z/(z-1/3)\), ROC \(|z|>1/3\)

## Q2

### Given

\(X(z)=\dfrac{1}{(1-\frac12 z^{-1})(1-\frac13 z^{-1})}\) with ROC \(|z|>1/2\) (causal).

### Find

\(x[n]\) for all \(n\).

### Solution

Partial fractions in \(z^{-1}\):
\[
X(z)=\frac{A}{1-\frac12 z^{-1}}+\frac{B}{1-\frac13 z^{-1}}.
\]
Cover-up: \(A=(1-1/3)/(1/2-1/3)=(2/3)/(1/6)=4\), wait: at \(z^{-1}=2\), i.e. pole \(1/2\):
\[
A=\frac{1}{1-\frac13\cdot 2}=\frac{1}{1-\frac23}=3,\qquad B=\frac{1}{1-\frac12\cdot 3}=\frac{1}{1-\frac32}=\frac{1}{-1/2}=-2.
\]
Check: \(A+B=1\) for the \(z^0\) numerator 1, \(3-2=1\). Yes. Causal inversion:
\[
x[n]=\big(3\cdot(1/2)^n - 2\cdot(1/3)^n\big)u[n].
\]

### Answer

\(x[n]=\big(3(1/2)^n-2(1/3)^n\big)u[n]\)

## Q3

### Given

Difference equation \(y[n]-\frac12 y[n-1]=x[n]\), rest ICs, \(x[n]=\delta[n]\).

### Find

\(H(z)=Y(z)/X(z)\) and \(h[n]\).

### Solution

Z (causal, rest): \(Y-\frac12 z^{-1}Y=X\), so
\[
H(z)=\frac{1}{1-\frac12 z^{-1}}=\frac{z}{z-1/2},\qquad |z|>1/2.
\]
\[
h[n]=(1/2)^n u[n].
\]
Iterate: \(y[0]=1\), \(y[1]=1/2\), \(y[2]=1/4\), matches.

### Answer

\(H(z)=1/(1-\frac12 z^{-1})\), \(h[n]=(1/2)^n u[n]\)

## Q4

### Given

Causal \(X(z)=\dfrac{0.5z}{(z-1)(z-0.5)}\), ROC \(|z|>1\).

### Find

Whether the final-value theorem applies, and if so \(x[\infty]\). Also \(x[0]\) from the initial-value theorem.

### Solution

Poles of \(X\) at \(1\) and \(0.5\). Poles of \((z-1)X(z)=0.5z/(z-0.5)\) at \(z=0.5\), inside the open unit disk. FVT applies.
\[
x[\infty]=\lim_{z\to 1}(z-1)X(z)=\lim_{z\to 1}\frac{0.5z}{z-0.5}=\frac{0.5}{0.5}=1.
\]
Initial value: \(x[0]=\lim_{z\to\infty}X(z)=0\) (degree denominator exceeds numerator). Check PF: \(X(z)/z=0.5/((z-1)(z-0.5))=A/(z-1)+B/(z-0.5)\), \(A=1\), \(B=-1\), so \(X=z/(z-1)-z/(z-0.5)\), \(x[n]=(1-(0.5)^n)u[n]\), \(x[0]=0\), \(x[\infty]=1\).

### Answer

FVT applies; \(x[\infty]=1\); \(x[0]=0\)

## Q5

### Given

Causal second-order \(H(z)=\dfrac{1}{1-1.2z^{-1}+0.32 z^{-2}}\).

### Find

The poles and whether the causal system is BIBO stable.

### Solution

Denominator \(z^2-1.2z+0.32=0\) after multiplying by \(z^2\). Discriminant \(1.44-1.28=0.16\), \(z= (1.2\pm 0.4)/2\), so \(z=0.8\) and \(z=0.4\). Both magnitudes \(<1\). ROC of the causal system is \(|z|>0.8\), which includes \(|z|=1\). Stable.

### Answer

Poles at \(0.8\) and \(0.4\); BIBO stable (causal)
