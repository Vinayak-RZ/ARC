## Q1
### Given
\(x[n]=\bigl(\frac12\bigr)^n u[n]+2^n u[-n-1]\).
### Find
\(X(z)\) and the ROC.
### Solution
First term: \(1/(1-\frac12 z^{-1})\) with \(|z|>1/2\).

Second term: \(2^n u[-n-1]= - \bigl(-2^n u[-n-1]\bigr)\). The pair \(-a^n u[-n-1]\leftrightarrow 1/(1-az^{-1})\) for \(|z|<|a|\) with \(a=2\) gives \(2^n u[-n-1]\leftrightarrow -1/(1-2z^{-1})\) for \(|z|<2\).

Intersection: \(1/2<|z|<2\). Algebra: \(X(z)=\frac{1}{1-\frac12 z^{-1}}-\frac{1}{1-2z^{-1}}\).
### Answer
\(X(z)=\frac{1}{1-\frac12 z^{-1}}-\frac{1}{1-2z^{-1}}\), ROC \(\frac12<|z|<2\).

## Q2
### Given
\(X(z)=\frac{1}{1-\frac14 z^{-1}}\) with ROC \(|z|<1/4\).
### Find
\(x[n]\).
### Solution
The causal pair is illegal because the ROC is inside the pole radius \(1/4\). Use \(-a^n u[-n-1]\) with \(a=1/4\):

\[
x[n]=-\Bigl(\frac14\Bigr)^n u[-n-1].
\]
### Answer
\(x[n]=-(1/4)^n u[-n-1]\).

## Q3
### Given
A causal system \(y[n]-\frac14 y[n-1]=x[n]+x[n-1]\), rest IC.
### Find
\(H(z)\), \(h[n]\), and whether the system is BIBO stable.
### Solution
\(H(z)=(1+z^{-1})/(1-\frac14 z^{-1})\), ROC \(|z|>1/4\) by causality.

Partial fractions: \(H(z)=\frac{1+z^{-1}}{1-\frac14 z^{-1}}=A\frac{1}{1-\frac14 z^{-1}}\) plus possibly a constant. Divide: \(1+z^{-1}= -4(1-\frac14 z^{-1})+5\), so \(H(z)=-4+\frac{5}{1-\frac14 z^{-1}}\).

Thus \(h[n]=-4\delta[n]+5(\frac14)^n u[n]\). Equivalently \(h[0]=1\) from the recurrence with \(x=\delta\), and \(h[n]=5(\frac14)^n\) for \(n\ge 1\)? Check \(h[0]=-4+5=1\), \(h[n]=5(1/4)^n\) for \(n>0\). Pole magnitude \(1/4<1\), stable.
### Answer
\(H(z)=(1+z^{-1})/(1-\frac14 z^{-1})\), \(h[0]=1\), \(h[n]=5(1/4)^n\) for \(n\ge 1\); BIBO stable.

## Q4
### Given
\(H(z)=\frac{z}{z-\frac12}\) with ROC \(|z|>1/2\).
### Find
The response to \(x[n]=(1/3)^n u[n]\).
### Solution
\(X(z)=1/(1-\frac13 z^{-1})\), \(|z|>1/3\). Product \(Y(z)=H(z)X(z)\) on \(|z|>1/2\).

\(H(z)=1/(1-\frac12 z^{-1})\). So \(Y(z)=\frac{1}{(1-\frac12 z^{-1})(1-\frac13 z^{-1})}\). Partial fractions: \(\frac{A}{1-\frac12 z^{-1}}+\frac{B}{1-\frac13 z^{-1}}\) with \(A=3\), \(B=-2\).

Causal ROC: \(y[n]=\bigl[3(\frac12)^n-2(\frac13)^n\bigr]u[n]\).
### Answer
\(y[n]=\bigl(3(1/2)^n-2(1/3)^n\bigr)u[n]\).

## Q5
### Given
Finite sequence \(x[0]=3\), \(x[1]=-1\), \(x[n]=0\) otherwise.
### Find
\(X(z)\), ROC, and \(x[n]\) recovered by inverse on that ROC.
### Solution
\(X(z)=3-z^{-1}\). ROC is all \(z\neq 0\). Inverse is exactly the two-tap sequence given. (At \(z=0\), \(X\) has a pole of order 1.)
### Answer
\(X(z)=3-z^{-1}\), ROC \(\mathbb{C}\setminus\{0\}\); inverse is \(\{3,-1\}\) at \(n=0,1\).

## Q6
### Given
Causal \(H(z)=\frac{1}{1-2z^{-1}}\).
### Find
Whether \(H(e^{j\Omega})\) exists as a DTFT of \(h\), and \(h[n]\).
### Solution
Pole at \(z=2\), causal ROC \(|z|>2\), which does not include the unit circle. \(h[n]=2^n u[n]\) is not absolutely summable and grows. The DTFT does not converge as an ordinary function.
### Answer
\(h[n]=2^n u[n]\); DTFT does not exist as an ordinary function.
