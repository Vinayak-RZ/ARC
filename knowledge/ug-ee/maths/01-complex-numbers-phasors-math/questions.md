# Questions — Complex arithmetic and Euler

Original numbers. Peak/RMS convention is stated in each item.

## Q1

### Given

The impedance \(Z = -8 + j6\ \Omega\).

### Find

Magnitude \(|Z|\) in ohms and principal argument \(\arg Z\) in degrees in \((-180^\circ,180^\circ]\).

### Solution

Magnitude:
\[
|Z| = \sqrt{(-8)^2 + 6^2} = \sqrt{64+36} = \sqrt{100} = 10\ \Omega.
\]
The point is in the second quadrant (\(x<0\), \(y>0\)). Reference angle:
\[
\alpha = \arctan(6/8) = \arctan(0.75) = 36.87^\circ.
\]
Principal argument:
\[
\arg Z = 180^\circ - 36.87^\circ = 143.13^\circ.
\]
Polar form is \(10\angle 143.13^\circ\ \Omega\).

### Answer

\(|Z|=10\ \Omega\), \(\arg Z = 143.13^\circ\)

## Q2

### Given

\(Z_1 = 3+j4\ \Omega\) and \(Z_2 = 2-j2\ \Omega\), series connection, RMS source \(\mathbf{V} = 20\angle 0^\circ\ \mathrm{V}\).

### Find

The current \(\mathbf{I} = \mathbf{V}/(Z_1+Z_2)\) in rectangular form (amperes).

### Solution

Series impedance:
\[
Z = Z_1+Z_2 = (3+2)+j(4-2) = 5+j2\ \Omega.
\]
Current:
\[
\mathbf{I} = \frac{20}{5+j2}\cdot\frac{5-j2}{5-j2} = \frac{20(5-j2)}{25+4} = \frac{100-j40}{29} = 3.448 - j1.379\ \mathrm{A}.
\]

### Answer

\(\mathbf{I} = 3.448 - j1.379\ \mathrm{A}\)

## Q3

### Given

A cosine source \(v(t) = 10\cos(1000t + 30^\circ)\ \mathrm{V}\) (peak form) drives \(R=4\ \Omega\) in series with \(L=2\ \mathrm{mH}\) and \(C=500\ \mu\mathrm{F}\).

### Find

The steady-state current \(i(t)\) in the form \(I_m\cos(1000t+\phi)\).

### Solution

Angular frequency \(\omega=1000\ \mathrm{rad/s}\). Device impedances:
\[
j\omega L = j(1000)(0.002) = j2\ \Omega, \qquad \frac{1}{j\omega C} = \frac{1}{j(1000)(5\times 10^{-4})} = \frac{1}{j0.5} = -j2\ \Omega.
\]
\[
Z = 4 + j2 - j2 = 4\ \Omega.
\]
Peak phasor of voltage is \(10\angle 30^\circ\ \mathrm{V}\). Current peak phasor:
\[
\mathbf{I} = \frac{10\angle 30^\circ}{4} = 2.5\angle 30^\circ\ \mathrm{A}.
\]
Restore the cosine:
\[
i(t) = 2.5\cos(1000t + 30^\circ)\ \mathrm{A}.
\]
The LC pair cancels at this particular \(\omega\) (series resonance), so the current is in phase with the voltage.

### Answer

\(i(t)=2.5\cos(1000t+30^\circ)\ \mathrm{A}\)

## Q4

### Given

\(z = 16\angle 120^\circ\) (degrees).

### Find

All distinct fourth roots in polar form with principal angles in \((-180^\circ,180^\circ]\), magnitudes exact.

### Solution

Magnitude of each root: \(16^{1/4} = 2\). Arguments:
\[
\theta_k = \frac{120^\circ + k\cdot 360^\circ}{4} = 30^\circ + k\cdot 90^\circ,\qquad k=0,1,2,3.
\]
\[
k=0:\ 30^\circ,\quad k=1:\ 120^\circ,\quad k=2:\ 210^\circ \equiv -150^\circ,\quad k=3:\ 300^\circ \equiv -60^\circ.
\]
The four roots are \(2\angle 30^\circ\), \(2\angle 120^\circ\), \(2\angle -150^\circ\), \(2\angle -60^\circ\).

### Answer

\(2\angle 30^\circ,\ 2\angle 120^\circ,\ 2\angle -150^\circ,\ 2\angle -60^\circ\)

## Q5

### Given

RMS phasors \(\mathbf{V} = 100\angle 0^\circ\ \mathrm{V}\) and \(\mathbf{I} = 5\angle -36.87^\circ\ \mathrm{A}\).

### Find

Complex power \(S=\mathbf{V}\mathbf{I}^*\) in rectangular form, and the power factor lagging or leading.

### Solution

\[
\mathbf{I}^* = 5\angle +36.87^\circ\ \mathrm{A}.
\]
\[
S = (100\angle 0^\circ)(5\angle 36.87^\circ) = 500\angle 36.87^\circ = 500(\cos 36.87^\circ + j\sin 36.87^\circ).
\]
\[
\cos 36.87^\circ = 0.8,\quad \sin 36.87^\circ = 0.6,
\]
so \(S = 400 + j300\ \mathrm{VA}\). Real power \(P=400\ \mathrm{W}\), reactive power \(Q=300\ \mathrm{VAR}\) (positive, inductive). Power factor:
\[
\mathrm{pf} = \cos 36.87^\circ = 0.8\ \text{lagging}.
\]

### Answer

\(S=400+j300\ \mathrm{VA}\), pf \(=0.8\) lagging

## Q6

### Given

The three-phase operator \(a=e^{j2\pi/3}\) and the a-phase RMS phasor \(\mathbf{V}_a = 230\angle 0^\circ\ \mathrm{V}\) (ABC sequence, \(\mathbf{V}_b = a^2\mathbf{V}_a\), \(\mathbf{V}_c = a\mathbf{V}_a\)).

### Find

\(\mathbf{V}_b\) in rectangular form (volts), using \(a^2 = -1/2 - j\sqrt{3}/2\).

### Solution

\[
\mathbf{V}_b = a^2\cdot 230 = 230\left(-\frac12 - j\frac{\sqrt{3}}{2}\right) = -115 - j115\sqrt{3}.
\]
Numerically \(\sqrt{3}\approx 1.73205\), so \(115\sqrt{3}\approx 199.186\) and
\[
\mathbf{V}_b \approx -115 - j199.19\ \mathrm{V}.
\]
Check: magnitude \(\sqrt{115^2+(115\sqrt{3})^2} = 115\sqrt{1+3} = 115\cdot 2 = 230\ \mathrm{V}\), angle \(-120^\circ\).

### Answer

\(\mathbf{V}_b = -115 - j115\sqrt{3}\ \mathrm{V}\) \(\approx -115-j199.19\ \mathrm{V}\)
