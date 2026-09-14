# Questions — Nyquist stability

Original pedagogical numbers.

## Q1

### Given

Open-loop \(L(s)=2/(s+2)\), which is stable. Unity negative feedback.

### Find

\(P\), whether \(L(j\omega)\) encircles \(-1\), and \(Z\).

### Solution

One OL pole at \(-2\), \(P=0\). \(L(j\omega)=2/(2+j\omega)\), a circle of diameter 1 (from 0 to 1 on the real axis), entirely in \(\mathrm{Re}\ge 0\). Does not encircle \(-1\). \(N=0\), \(Z=0\). Closed-loop pole at \(s+4=0\), \(s=-4\), agrees.

### Answer

\(P=0\), \(N=0\), \(Z=0\) (stable).

## Q2

### Given

\(L(s)=K/[s(s+1)(s+2)]\), \(K=8\). Open-loop poles are in the closed LHP (one at 0).

### Find

\(P\) for the D-contour that indents around the origin, the Routh \(j\omega\) crossing gain, and whether \(K=8\) is stable.

### Solution

Indentation puts \(s=0\) outside \(\Gamma\), so \(P=0\). Characteristic \(s^3+3s^2+2s+K\). Routh: stable for \(0<K<6\) (unit 04 style). \(K=8>6\) is unstable, \(Z=2\). Thus \(N=Z-P=2\) clockwise encirclements of \(-1\). At \(K=6\), the plot passes through \(-1\) at \(\omega=\sqrt{2}\).

### Answer

\(P=0\); \(K_u=6\); \(K=8\) unstable with \(N=2\), \(Z=2\).

## Q3

### Given

\(L(s)=4(s+2)/(s-1)\). Unity negative feedback.

### Find

\(P\), closed-loop characteristic polynomial, \(Z\), and the required \(N\).

### Solution

OL pole at \(+1\), \(P=1\). \(1+L=(s-1+4s+8)/(s-1)=(5s+7)/(s-1)\). Closed-loop pole \(s=-7/5=-1.4\), \(Z=0\). Need \(N=Z-P=-1\), i.e. one counterclockwise encirclement of \(-1\). (The plot of \(L(j\omega)\) is a circle that does enclose \(-1\) in the ccw sense as \(\omega\) goes \(-\infty\to\infty\).)

### Answer

\(P=1\), \(Z=0\), \(N=-1\) (one ccw encirclement); stable.

## Q4

### Given

Type-1 \(L\sim K_v/s\) near \(s=0\) with \(K_v>0\). Small RHP indentation \(s=\varepsilon e^{j\theta}\), \(\theta\) from \(-\pi/2\) to \(+\pi/2\).

### Find

The angle traversed by \(L(s)\) on that indentation, and the sense.

### Solution

\(L\approx K_v/s=(K_v/\varepsilon)e^{-j\theta}\). As \(\theta\) goes from \(-\pi/2\) to \(+\pi/2\) (RHP indent, D-contour going up), \(-\theta\) goes from \(+\pi/2\) to \(-\pi/2\), a clockwise half-turn of the large-radius image. Angle change \(-180^\circ\), clockwise.

### Answer

Large clockwise semicircle (\(-180^\circ\)) connecting \(L(j0^-)\) to \(L(j0^+)\).

## Q5

### Given

A polar plot of a stable open-loop strictly proper \(L\) (\(P=0\)) crosses the negative real axis at \(-0.4\) once and intersects the unit circle at an angle of \(-115^\circ\) (phase of \(L\)).

### Find

GM in dB, PM, \(N\), and \(Z\).

### Solution

Crossing at \(-0.4\): \(|L|=0.4\), \(\mathrm{GM}=1/0.4=2.5=8.0\,\mathrm{dB}\). \(\mathrm{PM}=-115+180=65^\circ\). The plot does not reach \(-1\), so with the conjugate mirror and \(L(\infty)=0\), \(N=0\). \(Z=0\).

### Answer

\(\mathrm{GM}=8.0\,\mathrm{dB}\); \(\mathrm{PM}=65^\circ\); \(N=0\); \(Z=0\).
