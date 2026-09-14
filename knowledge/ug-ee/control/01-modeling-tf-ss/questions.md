# Questions — TF, SS, linearization

Original pedagogical numbers.

## Q1

### Given

A translational plant \(2\ddot{y}+6\dot{y}+10 y = 4 u\), zero initial conditions, output \(y\), input \(u\).

### Find

The transfer function \(G(s)=Y(s)/U(s)\) and the DC gain.

### Solution

Laplace with zero ICs: \((2s^2+6s+10)Y=4U\), so \(G(s)=4/(2s^2+6s+10)=2/(s^2+3s+5)\). DC gain \(G(0)=2/5=0.4\).

### Answer

\(G(s)=2/(s^2+3s+5)\); \(G(0)=0.4\).

## Q2

### Given

State model
\[
A=\begin{bmatrix}-2&0\\1&-3\end{bmatrix},\quad
B=\begin{bmatrix}1\\0\end{bmatrix},\quad
C=\begin{bmatrix}0&1\end{bmatrix},\quad
D=0.
\]

### Find

\(G(s)=C(sI-A)^{-1}B\).

### Solution

\(sI-A=\begin{bmatrix}s+2&0\\-1&s+3\end{bmatrix}\), \(\det=(s+2)(s+3)\). Inverse:
\[
(sI-A)^{-1}=\frac{1}{(s+2)(s+3)}\begin{bmatrix}s+3&0\\1&s+2\end{bmatrix}.
\]
Then \((sI-A)^{-1}B=\frac{1}{(s+2)(s+3)}\begin{bmatrix}s+3\\1\end{bmatrix}\), so \(G(s)=1/[(s+2)(s+3)]\).

### Answer

\(G(s)=1/[(s+2)(s+3)]\).

## Q3

### Given

Tank: area \(A_c=2\,\mathrm{m}^2\), outflow \(q_{\mathrm{out}}=\sqrt{h}\) in m³/s with \(h\) in m, inflow \(q_{\mathrm{in}}\) in m³/s. Equilibrium at \(h_e=4\,\mathrm{m}\).

### Find

Linearized \(\dot{\tilde{h}}=a\tilde{h}+b\tilde{q}_{\mathrm{in}}\) coefficients \(a,b\).

### Solution

Nonlinear: \(2\dot{h}=q_{\mathrm{in}}-\sqrt{h}\). Equilibrium: \(q_{\mathrm{in},e}=\sqrt{4}=2\). Jacobian: \(\partial f/\partial h=-(1/2)h^{-1/2}/2=-1/(4\sqrt{h})\) because \(\dot{h}=(1/2)(q_{\mathrm{in}}-\sqrt{h})\), so \(A=\partial\dot{h}/\partial h=-(1/2)\cdot(1/(2\sqrt{h}))=-1/(4\sqrt{h})\). At \(h_e=4\), \(a=-1/8=-0.125\,\mathrm{s}^{-1}\). \(b=\partial\dot{h}/\partial q_{\mathrm{in}}=1/2=0.5\,\mathrm{m}^{-2}\).

### Answer

\(a=-0.125\,\mathrm{s}^{-1}\), \(b=0.5\,\mathrm{m}^{-2}\).

## Q4

### Given

Inverted pendulum (angle from upward vertical) \(\ddot{\phi}-9\phi=u\). States \(x=[\phi,\dot{\phi}]^\top\), input \(u\), output \(\phi\).

### Find

The matrices \(A,B,C,D\).

### Solution

\(\dot{x}_1=x_2\), \(\dot{x}_2=9x_1+u\). So \(A=\begin{bmatrix}0&1\\9&0\end{bmatrix}\), \(B=\begin{bmatrix}0\\1\end{bmatrix}\), \(C=\begin{bmatrix}1&0\end{bmatrix}\), \(D=0\). Open-loop poles at \(s=\pm 3\).

### Answer

\(A=\begin{bmatrix}0&1\\9&0\end{bmatrix}\), \(B=\begin{bmatrix}0\\1\end{bmatrix}\), \(C=[1,0]\), \(D=0\).

## Q5

### Given

Armature-controlled DC motor with \(L=0\), \(R=2\,\Omega\), \(k_t=k_b=0.5\,\mathrm{N\cdot m/A}\), \(J=0.05\,\mathrm{kg\cdot m}^2\), \(b=0.01\,\mathrm{N\cdot m\cdot s}\), load torque zero. Input \(v_a\), output \(\omega\).

### Find

First-order transfer function \(\Omega(s)/V_a(s)\).

### Solution

Algebraic electrical: \(i_a=(v_a-k_b\omega)/R\). Mechanical: \(J\dot{\omega}=k_t i_a-b\omega=(k_t/R)v_a-(k_t k_b/R+b)\omega\). Numbers: \(k_t/R=0.25\), \(k_t k_b/R=0.125\), so \(0.05\dot{\omega}=0.25 v_a-(0.125+0.01)\omega=0.25 v_a-0.135\omega\). Thus \(\dot{\omega}+2.7\omega=5 v_a\), \(G(s)=5/(s+2.7)\).

### Answer

\(G(s)=5/(s+2.7)\).
