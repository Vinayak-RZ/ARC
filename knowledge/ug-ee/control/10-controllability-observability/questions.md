# Questions — PBH, canonical forms

Original pedagogical numbers.

## Q1

### Given

\(A=\begin{bmatrix}-1&0\\0&-2\end{bmatrix}\), \(B=\begin{bmatrix}1\\0\end{bmatrix}\).

### Find

Whether \((A,B)\) is controllable, using \(\mathcal{C}\) and using PBH.

### Solution

\(AB=\begin{bmatrix}-1\\0\end{bmatrix}\), \(\mathcal{C}=\begin{bmatrix}1&-1\\0&0\end{bmatrix}\), rank 1 \(<2\). Uncontrollable. PBH at \(\lambda=-2\): \([\lambda I-A,\ B]=\begin{bmatrix}-1&0&1\\0&0&0\end{bmatrix}\), rank 1. The mode \(-2\) is uncontrollable. At \(\lambda=-1\): rank 2.

### Answer

Not controllable; mode \(\lambda=-2\) fails PBH.

## Q2

### Given

\(A=\begin{bmatrix}0&1\\-6&-5\end{bmatrix}\), \(B=\begin{bmatrix}0\\1\end{bmatrix}\), \(C=\begin{bmatrix}2&1\end{bmatrix}\).

### Find

Controllability, observability, and \(G(s)\).

### Solution

Companion pair with \(B=[0,1]^\top\) is controllable: \(\mathcal{C}=[B,AB]=\begin{bmatrix}0&1\\1&-5\end{bmatrix}\), \(\det=-1\neq 0\). \(\mathcal{O}=\begin{bmatrix}2&1\\-6&-3\end{bmatrix}\), \(\det=0\), not observable. Resolvent sandwich: \((sI-A)^{-1}B=\frac{1}{s^2+5s+6}\begin{bmatrix}1\\s\end{bmatrix}\), \(G=(2+s)/(s^2+5s+6)=(s+2)/[(s+2)(s+3)]=1/(s+3)\). Cancelled mode \(s=-2\) is unobservable (CCF is always controllable).

### Answer

Controllable, not observable; \(G(s)=1/(s+3)\).

## Q3

### Given

\(A=\begin{bmatrix}0&1\\-2&-3\end{bmatrix}\), \(B=\begin{bmatrix}0\\1\end{bmatrix}\). Desired closed-loop poles \(-4,-5\).

### Find

State-feedback \(K=[k_1,k_2]\) so that \(A-BK\) has those poles.

### Solution

\(A-BK=\begin{bmatrix}0&1\\-2-k_1&-3-k_2\end{bmatrix}\). Characteristic \(s^2+(3+k_2)s+(2+k_1)\). Want \(s^2+9s+20\). Thus \(3+k_2=9\) ⇒ \(k_2=6\), \(2+k_1=20\) ⇒ \(k_1=18\). \(K=[18,6]\).

### Answer

\(K=[18,\ 6]\).

## Q4

### Given

\(A=\begin{bmatrix}-4&0\\1&-1\end{bmatrix}\), \(C=\begin{bmatrix}0&1\end{bmatrix}\).

### Find

Observability via PBH.

### Solution

Eigenvalues \(-4,-1\). PBH at \(\lambda=-4\): \(\lambda I-A=\begin{bmatrix}0&0\\-1&-3\end{bmatrix}\), stacked with \(C\): rows \((0,0)\), \((-1,-3)\), \((0,1)\). Rank 2. At \(\lambda=-1\): \(\lambda I-A=\begin{bmatrix}3&0\\-1&0\end{bmatrix}\), plus \(C=(0,1)\). Rows \((3,0)\), \((-1,0)\), \((0,1)\), rank 2. Observable. (Mode \(-4\) is seen through the coupling \(A_{21}=1\).)

### Answer

Observable (PBH rank 2 at both eigenvalues).

## Q5

### Given

SISO plant with a non-minimal realization of order 3 whose \(G(s)\) is \(2/(s+2)\) after cancellation of a factor \((s-1)/(s-1)\).

### Find

Whether the realization can be internally asymptotically stable, and what PBH must report for \(\lambda=1\).

### Solution

The cancelled RHP factor means an eigenvalue \(+1\) of \(A\) is uncontrollable, unobservable, or both. That mode is unstable, so the realization is not internally asymptotically stable even though \(G\) is Hurwitz. PBH fails at \(\lambda=1\): either \(\mathrm{rank}[\lambda I-A,\ B]<3\) or \(\mathrm{rank}[\lambda I-A;\ C]<3\) (or both).

### Answer

Not internally AS; PBH fails at \(\lambda=1\).
