# Questions — Vector calculus

## Q1

### Given

\(V(x,y,z)=4x^2 y - 3z\) volts, point \(P=(1,2,0)\).

### Find

\(\nabla V\) at \(P\), and the directional derivative toward \(\hat{u}=(3\hat{x}+4\hat{y})/5\).

### Solution

\[
\nabla V=(8xy,\ 4x^2,\ -3).
\]
At \(P\): \((16,\ 4,\ -3)\).
\[
\nabla V\cdot\hat{u}=\frac{16\cdot 3 + 4\cdot 4 + (-3)\cdot 0}{5}=\frac{48+16}{5}=12.8\ \mathrm{V/m}.
\]

### Answer

\(\nabla V|_P=(16,4,-3)\ \mathrm{V/m}\); directional derivative \(12.8\ \mathrm{V/m}\)

## Q2

### Given

\(\mathbf{A}=3x\hat{x}+2y\hat{y}-z\hat{z}\) on the unit cube \(0\le x,y,z\le 1\).

### Find

The flux \(\oiint_S\mathbf{A}\cdot d\mathbf{S}\) using the divergence theorem.

### Solution

\(\nabla\cdot\mathbf{A}=3+2-1=4\). Volume of the cube is \(1\).
\[
\text{flux}=\iiint 4\,dV=4.
\]
(Direct face-by-face check: \(x=1\) face contributes \(3\), \(x=0\) contributes \(0\); \(y=1\) contributes \(2\); \(z=1\) contributes \(-1\); opposite faces at 0 for those components that vanish. Total \(3+2-1=4\).)

### Answer

\(4\) (in the units of \(\mathbf{A}\) times area)

## Q3

### Given

\(\mathbf{F}=-y\hat{x}+x\hat{y}\) in the \(z=0\) plane. Curve \(C\) is the circle \(x^2+y^2=4\) travelled counterclockwise.

### Find

\(\oint_C\mathbf{F}\cdot d\mathbf{\ell}\) using Stokes, and \(\nabla\times\mathbf{F}\).

### Solution

Cartesian curl:
\[
\nabla\times\mathbf{F}=\hat{z}\big(\partial_x(x)-\partial_y(-y)\big)=\hat{z}(1+1)=2\hat{z}.
\]
Surface the disk \(x^2+y^2\le 4\), \(\hat{n}=\hat{z}\), area \(4\pi\).
\[
\iint (\nabla\times\mathbf{F})\cdot d\mathbf{S}=2\cdot 4\pi=8\pi.
\]
(Parametric check: \(\mathbf{r}=(2\cos t,2\sin t)\), \(\mathbf{r}'=(-2\sin t,2\cos t)\), \(\mathbf{F}\cdot\mathbf{r}'=4\), integrate \(t:0\to 2\pi\) gives \(8\pi\).)

### Answer

\(\nabla\times\mathbf{F}=2\hat{z}\); circulation \(8\pi\)

## Q4

### Given

Coaxial potential \(V(\rho)=A\ln\rho+B\) for \(a<\rho<b\), with \(V(a)=V_0\), \(V(b)=0\). (Laplace in cylindrical 1-D, no \(z,\phi\) dependence.)

### Find

\(A\) and \(B\), and \(E_\rho=-dV/d\rho\) for \(a<\rho<b\).

### Solution

\(A\ln a+B=V_0\), \(A\ln b+B=0\). Subtract: \(A\ln(a/b)=V_0\), \(A=V_0/\ln(a/b)=V_0/\ln(a/b)\). Also \(A=-V_0/\ln(b/a)\).
\[
B=-A\ln b=\frac{V_0\ln b}{\ln(b/a)}.
\]
\[
E_\rho=-\frac{A}{\rho}=\frac{V_0}{\rho\ln(b/a)}.
\]
(\(a<b\) so \(\ln(b/a)>0\); field points \(+\hat{\rho}\) if \(V_0>0\), from inner to outer.)

### Answer

\(A=-V_0/\ln(b/a)\), \(B=V_0\ln b/\ln(b/a)\); \(E_\rho=V_0/(\rho\ln(b/a))\)

## Q5

### Given

\(\mathbf{E}=2x\hat{x}+z\hat{y}+y\hat{z}\) in a simply connected region of \(\mathbb{R}^3\).

### Find

Whether \(\mathbf{E}\) is conservative, and if so a potential \(V\) with \(\mathbf{E}=-\nabla V\) and \(V(0,0,0)=0\).

### Solution

\[
\nabla\times\mathbf{E}=\begin{vmatrix}\hat{x}&\hat{y}&\hat{z}\\\partial_x&\partial_y&\partial_z\\2x&z&y\end{vmatrix}=\hat{x}(1-1)-\hat{y}(0-0)+\hat{z}(0-0)=\mathbf{0}.
\]
Conservative. Integrate \(-E_x= -2x = \partial_x V\), so \(V=-x^2+f(y,z)\). Then \(\partial_y V=f_y=-E_y=-z\), so \(f=-yz+g(z)\). Then \(\partial_z V=-y+g'(z)=-E_z=-y\), so \(g'=0\). With \(V(0,0,0)=0\), \(g=0\).
\[
V=-x^2-yz.
\]

### Answer

Conservative; \(V=-x^2-yz\)
