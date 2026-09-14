# Questions — Coordinate systems, vector identities

Original pedagogical numbers.

## Q1

### Given

Point \( P \) with Cartesian coordinates \( (3,4,12) \) m.

### Find

Spherical coordinates \( (r,\theta,\phi) \).

### Solution

\( r=\sqrt{9+16+144}=13 \) m. \( \theta=\cos^{-1}(z/r)=\cos^{-1}(12/13)=22.62^\circ \). \( \phi=\mathrm{atan2}(4,3)=53.13^\circ \).

### Answer

\( (13\,\mathrm{m},\ 22.6^\circ,\ 53.1^\circ) \).

## Q2

### Given

\(\mathbf{A}=2\rho\mathbf{a}_\rho-3z\mathbf{a}_z\) in cylindrical coordinates.

### Find

\(\nabla\cdot\mathbf{A}\).

### Solution

\(\nabla\cdot\mathbf{A}=\frac{1}{\rho}\partial(\rho\cdot 2\rho)/\partial\rho+\partial(-3z)/\partial z=4-3=1\).

### Answer

\( 1 \).

## Q3

### Given

Scalar \( f=x^2 y \).

### Find

\(\nabla f\) at \( (1,2,0) \) and \(\nabla\times(\nabla f)\).

### Solution

\(\nabla f=2xy\mathbf{a}_x+x^2\mathbf{a}_y\). At \( (1,2,0) \): \( 4\mathbf{a}_x+\mathbf{a}_y \). Curl of gradient is \(\mathbf{0}\).

### Answer

\( 4\mathbf{a}_x+\mathbf{a}_y \); \(\mathbf{0}\).

## Q4

### Given

A circle \( \rho=2 \) m, \( z=0 \), traversed in \( +\phi \). Field \(\mathbf{F}=\rho\mathbf{a}_\phi\).

### Find

\(\oint\mathbf{F}\cdot\mathrm{d}\mathbf{l}\).

### Solution

\(\mathrm{d}\mathbf{l}=\rho\mathrm{d}\phi\mathbf{a}_\phi=2\mathrm{d}\phi\mathbf{a}_\phi\), \(\mathbf{F}=2\mathbf{a}_\phi\), integrand \( 4\,\mathrm{d}\phi \), integral \( 8\pi \).

### Answer

\( 8\pi \) (units of \( F \) times metres).

## Q5

### Given

Cylindrical volume \( 0\le\rho\le 1 \), \( 0\le\phi\le 2\pi \), \( 0\le z\le 2 \), and \(\mathbf{A}=\rho^2\mathbf{a}_\rho\).

### Find

Flux \(\oint\mathbf{A}\cdot\mathrm{d}\mathbf{S}\) using the divergence theorem.

### Solution

\(\nabla\cdot\mathbf{A}=\frac{1}{\rho}\partial(\rho^3)/\partial\rho=3\rho\). \(\int 3\rho\cdot\rho\,\mathrm{d}\rho\mathrm{d}\phi\mathrm{d}z=\int_0^2\int_0^{2\pi}\int_0^1 3\rho^2\mathrm{d}\rho\mathrm{d}\phi\mathrm{d}z=3\cdot(1/3)\cdot 2\pi\cdot 2=4\pi\).

### Answer

\( 4\pi \).

## Q6

### Given

Identity check: \(\mathbf{A}=y\mathbf{a}_x\).

### Find

\(\nabla\times\mathbf{A}\) and \(\nabla\cdot(\nabla\times\mathbf{A})\).

### Solution

\(\nabla\times\mathbf{A}=-\mathbf{a}_z\). Divergence of that is 0.

### Answer

\( -\mathbf{a}_z \); \( 0 \).
