# Questions — Displacement current, Maxwell set

Original pedagogical numbers.

## Q1

### Given

Parallel-plate capacitor \( C=80.0 \) pF, \( v=5.00\sin(2.00\times 10^4 t) \) V.

### Find

Displacement current \( i_d=C\mathrm{d}v/\mathrm{d}t \).

### Solution

\( i_d=80e-12\times 5\times 2e4\cos(2e4 t)=8.00\cos(2.00\times 10^4 t) \) µA.

### Answer

\( 8.00\cos(2.00\times 10^4 t) \) µA.

## Q2

### Given

Between plates, uniform \( E=4000 t \) V/m (t in seconds) for a short interval, \( A=25.0 \) cm², \(\varepsilon=\varepsilon_0\), no conduction current.

### Find

\( I_d \).

### Solution

\( \partial D/\partial t=\varepsilon_0\times 4000 \). \( I_d=A\partial D/\partial t=8.854e-12\times 4000\times 0.0025=88.5 \) nA.

### Answer

\( 88.5 \) nA.

## Q3

### Given

Copper \(\sigma=5.80\times 10^7\) S/m, \(\varepsilon=\varepsilon_0\), \( f=1.00 \) MHz.

### Find

Ratio \( |J|/|J_d|=\sigma/(\omega\varepsilon) \).

### Solution

\( \omega\varepsilon=2\pi\times 10^6\times 8.854e-12=5.56\times 10^{-5} \). Ratio \( 5.80e7/5.56e-5=1.04\times 10^{12} \).

### Answer

\( 1.04\times 10^{12} \) (conduction dominates).

## Q4

### Given

Phasor Faraday, \(\tilde{\mathbf{B}}=0.010\,e^{-j2x}\mathbf{a}_z\) T, \(\omega=6.00\times 10^8\) rad/s, \(\mu=\mu_0\).

### Find

The phasor \(\nabla\times\tilde{\mathbf{E}}\) from Faraday’s law.

### Solution

\(\nabla\times\tilde{\mathbf{E}}=-j\omega\tilde{\mathbf{B}}=-j\times 6e8\times 0.010 e^{-j2x}\mathbf{a}_z=-j6.00e6\,e^{-j2x}\mathbf{a}_z\).

### Answer

\( -j 6.00\times 10^{6}\,e^{-j2x}\mathbf{a}_z \) V/m².

## Q5

### Given

Free-space \( c=1/\sqrt{\mu_0\varepsilon_0} \) and \(\eta_0=\sqrt{\mu_0/\varepsilon_0}\).

### Find

Numerical \( c \) and \(\eta_0\) using \(\mu_0=4\pi\times 10^{-7}\), \(\varepsilon_0=8.854\times 10^{-12}\).

### Solution

\( c=2.998\times 10^8 \) m/s. \(\eta_0=376.7\,\Omega\).

### Answer

\( 3.00\times 10^8 \) m/s; \( 377\,\Omega \).

## Q6

### Given

A wire carries 3.00 A DC into a capacitor plate. A loop encircles the wire. A second surface bounded by the same loop passes between the plates.

### Find

\(\oint\mathbf{H}\cdot\mathrm{d}\mathbf{l}\) for both surfaces.

### Solution

Steady DC after the capacitor is charged: \( I=0 \), \( I_d=0 \), both integrals 0. During charging, both equal the instantaneous 3.00 A (conduction on the wire surface, displacement on the plate surface). The intended UG charging instant: both 3.00 A.

### Answer

During charging, both \( 3.00 \) A; in true DC steady state, both \( 0 \).
