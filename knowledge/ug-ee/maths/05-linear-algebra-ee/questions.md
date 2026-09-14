# Questions — Linear algebra for EE

## Q1

### Given

\[
A=\begin{pmatrix}4&2\\1&3\end{pmatrix},\qquad b=\begin{pmatrix}2\\1\end{pmatrix}.
\]

### Find

\(\det A\), \(A^{-1}\), and \(x=A^{-1}b\).

### Solution

\(\det A=12-2=10\).
\[
A^{-1}=\frac{1}{10}\begin{pmatrix}3&-2\\-1&4\end{pmatrix}.
\]
\[
x=\frac{1}{10}\begin{pmatrix}3\cdot 2+(-2)\cdot 1\\-1\cdot 2+4\cdot 1\end{pmatrix}=\frac{1}{10}\begin{pmatrix}4\\2\end{pmatrix}=\begin{pmatrix}0.4\\0.2\end{pmatrix}.
\]
Check: \(A x=\begin{pmatrix}4\cdot 0.4+2\cdot 0.2\\0.4+3\cdot 0.2\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix}\).

### Answer

\(\det A=10\), \(A^{-1}=\frac{1}{10}\begin{pmatrix}3&-2\\-1&4\end{pmatrix}\), \(x=(0.4,\ 0.2)^T\)

## Q2

### Given

\[
A=\begin{pmatrix}0&1\\-8&-6\end{pmatrix}
\]
(companion form of \(\ddot{y}+6\dot{y}+8y=0\)).

### Find

Eigenvalues and a corresponding eigenvector for each.

### Solution

\(\chi(\lambda)=\det(\lambda I-A)=\lambda(\lambda+6)+8=\lambda^2+6\lambda+8=(\lambda+2)(\lambda+4)\). Eigenvalues \(\lambda=-2,-4\).

For \(\lambda=-2\): \((-2I-A)\) wait: use \((A-\lambda I)v=0\). \(A+2I=\begin{pmatrix}2&1\\-8&-4\end{pmatrix}\), so \(2v_1+v_2=0\), \(v=\begin{pmatrix}1\\-2\end{pmatrix}\).

For \(\lambda=-4\): \(A+4I=\begin{pmatrix}4&1\\-8&-2\end{pmatrix}\), \(4v_1+v_2=0\), \(v=\begin{pmatrix}1\\-4\end{pmatrix}\).

### Answer

\(\lambda=-2\) with \(v=(1,-2)^T\); \(\lambda=-4\) with \(v=(1,-4)^T\)

## Q3

### Given

Real symmetric
\[
A=\begin{pmatrix}2&1\\1&2\end{pmatrix}.
\]

### Find

Eigenvalues, an orthonormal eigenbasis, and whether \(A\) is positive definite. Also \(q(x)=x^T A x\) for \(x=(1,1)^T\).

### Solution

\(\lambda^2-4\lambda+3=0\), \((\lambda-1)(\lambda-3)=0\), \(\lambda=1,3\), both positive, so \(A\succ 0\).

\(\lambda=3\): \((A-3I)=\begin{pmatrix}-1&1\\1&-1\end{pmatrix}\), \(v=(1,1)^T\), unit \(u_1=(1/\sqrt{2},1/\sqrt{2})^T\).

\(\lambda=1\): \(A-I=\begin{pmatrix}1&1\\1&1\end{pmatrix}\), \(v=(1,-1)^T\), unit \(u_2=(1/\sqrt{2},-1/\sqrt{2})^T\).

\[
q(1,1)=\begin{pmatrix}1&1\end{pmatrix}\begin{pmatrix}3\\3\end{pmatrix}=6.
\]
Also \(q=3\|P_{\lambda=3}x\|^2+1\|P_{\lambda=1}x\|^2\); \(x=\sqrt{2}\,u_1\), so \(q=3\cdot 2=6\).

### Answer

\(\lambda=3,1\); \(u=(1,1)^T/\sqrt{2}\) and \((1,-1)^T/\sqrt{2}\); SPD yes; \(q(1,1)=6\)

## Q4

### Given

Overdetermined
\[
A=\begin{pmatrix}1&0\\1&1\\1&2\end{pmatrix},\qquad b=\begin{pmatrix}1\\2\\2\end{pmatrix}.
\]

### Find

The least-squares \(\hat{x}=(\hat{x}_1,\hat{x}_2)^T\) minimizing \(\|Ax-b\|_2\).

### Solution

\[
A^T A=\begin{pmatrix}3&3\\3&5\end{pmatrix},\qquad A^T b=\begin{pmatrix}5\\6\end{pmatrix}.
\]
\(\det(A^T A)=15-9=6\).
\[
\hat{x}=\frac{1}{6}\begin{pmatrix}5&-3\\-3&3\end{pmatrix}\begin{pmatrix}5\\6\end{pmatrix}=\frac{1}{6}\begin{pmatrix}25-18\\-15+18\end{pmatrix}=\frac{1}{6}\begin{pmatrix}7\\3\end{pmatrix}=\begin{pmatrix}7/6\\1/2\end{pmatrix}.
\]

### Answer

\(\hat{x}=(7/6,\ 1/2)^T\)

## Q5

### Given

Diagonalizable \(A=P\Lambda P^{-1}\) with \(\Lambda=\operatorname{diag}(-1,-3)\),
\[
P=\begin{pmatrix}1&1\\1&2\end{pmatrix}.
\]

### Find

\(e^{A t}\) at general \(t\), and \(e^{A\cdot 0}\).

### Solution

\(\det P=1\), \(P^{-1}=\begin{pmatrix}2&-1\\-1&1\end{pmatrix}\).
\[
e^{At}=P\begin{pmatrix}e^{-t}&0\\0&e^{-3t}\end{pmatrix}P^{-1}=\begin{pmatrix}e^{-t}&e^{-3t}\\e^{-t}&2e^{-3t}\end{pmatrix}\begin{pmatrix}2&-1\\-1&1\end{pmatrix}.
\]
First row: \((2e^{-t}-e^{-3t},\ -e^{-t}+e^{-3t})\). Second: \((2e^{-t}-2e^{-3t},\ -e^{-t}+2e^{-3t})\).
\[
e^{At}=\begin{pmatrix}2e^{-t}-e^{-3t}& -e^{-t}+e^{-3t}\\ 2e^{-t}-2e^{-3t}& -e^{-t}+2e^{-3t}\end{pmatrix}.
\]
At \(t=0\): \(\begin{pmatrix}2-1&-1+1\\2-2&-1+2\end{pmatrix}=I\).

### Answer

\(e^{At}=\begin{pmatrix}2e^{-t}-e^{-3t}& e^{-3t}-e^{-t}\\ 2e^{-t}-2e^{-3t}& 2e^{-3t}-e^{-t}\end{pmatrix}\); \(e^{0}=I\)
