# Questions — State space UG

Original pedagogical numbers.

## Q1

### Given

\(A=\begin{bmatrix}-3&0\\0&-5\end{bmatrix}\), \(x(0)=\begin{bmatrix}2\\4\end{bmatrix}\).

### Find

\(x(t)\) for \(t\ge 0\).

### Solution

Already diagonal. \(x_1(t)=2e^{-3t}\), \(x_2(t)=4e^{-5t}\).

### Answer

\(x(t)=[2e^{-3t},\ 4e^{-5t}]^\top\).

## Q2

### Given

\(A=\begin{bmatrix}0&1\\-8&-6\end{bmatrix}\).

### Find

Eigenvalues and a modal matrix \(P\) of eigenvectors, and \(\mathrm{tr}A,\det A\).

### Solution

\(\chi(s)=s^2+6s+8=(s+2)(s+4)\). \(\lambda=-2,-4\). \(\mathrm{tr}A=-6\), \(\det A=8\). For \(\lambda=-2\): \((A+2I)v=0\), \(A+2I=\begin{bmatrix}2&1\\-8&-4\end{bmatrix}\), \(2v_1+v_2=0\), \(v=\begin{bmatrix}1\\-2\end{bmatrix}\). For \(\lambda=-4\): \(A+4I=\begin{bmatrix}4&1\\-8&-2\end{bmatrix}\), \(4v_1+v_2=0\), \(v=\begin{bmatrix}1\\-4\end{bmatrix}\). \(P=\begin{bmatrix}1&1\\-2&-4\end{bmatrix}\).

### Answer

\(\lambda=-2,-4\); \(P=\begin{bmatrix}1&1\\-2&-4\end{bmatrix}\); \(\mathrm{tr}=-6\), \(\det=8\).

## Q3

### Given

The \(A\) of Q2, \(B=\begin{bmatrix}0\\1\end{bmatrix}\), constant \(u=3\), \(x(0)=0\).

### Find

The steady state \(x_{ss}\) and \(y_{ss}\) if \(C=[1,0]\), \(D=0\).

### Solution

\(0=Ax_{ss}+B\cdot 3\) ⇒ \(x_{ss}=-3A^{-1}B\). \(A^{-1}=\frac{1}{8}\begin{bmatrix}-6&-1\\8&0\end{bmatrix}\) wait: \(A=\begin{bmatrix}0&1\\-8&-6\end{bmatrix}\), \(\det=8\), \(A^{-1}=\frac{1}{8}\begin{bmatrix}-6&-1\\8&0\end{bmatrix}\). Check: \(A A^{-1}=\frac{1}{8}\begin{bmatrix}0&1\\-8&-6\end{bmatrix}\begin{bmatrix}-6&-1\\8&0\end{bmatrix}=\frac{1}{8}\begin{bmatrix}8&0\\0&8\end{bmatrix}=I\). Yes. \(A^{-1}B=\frac{1}{8}\begin{bmatrix}-1\\0\end{bmatrix}\). \(x_{ss}=-3A^{-1}B=\begin{bmatrix}3/8\\0\end{bmatrix}\). \(y_{ss}=3/8\). Equilibrium of the ODE: \(\dot{x}_1=x_2=0\), \(\dot{x}_2=-8x_1-6x_2+3=0\) ⇒ \(x_1=3/8\), \(x_2=0\).

### Answer

\(x_{ss}=[3/8,\ 0]^\top\); \(y_{ss}=3/8\).

## Q4

### Given

\(A=\begin{bmatrix}-1&1\\0&-1\end{bmatrix}\) (Jordan block), \(x(0)=\begin{bmatrix}0\\1\end{bmatrix}\).

### Find

\(x(t)\).

### Solution

\(e^{At}=e^{-t}\begin{bmatrix}1&t\\0&1\end{bmatrix}\). \(x(t)=e^{-t}\begin{bmatrix}t\\1\end{bmatrix}\).

### Answer

\(x(t)=e^{-t}[t,\ 1]^\top\).

## Q5

### Given

\(A=\begin{bmatrix}0&1\\2&-1\end{bmatrix}\) (note the \(+2\)).

### Find

Whether \(\dot{x}=Ax\) is asymptotically stable, using trace/det or Routh.

### Solution

\(\mathrm{tr}A=-1<0\), \(\det A=-2<0\). Det negative ⇒ one positive and one negative eigenvalue (product negative). Not Hurwitz. \(\chi(s)=s^2+s-2=(s+2)(s-1)\). RHP root at \(+1\).

### Answer

Not asymptotically stable (eigenvalues \(-2,+1\)).
