# Questions — Root locus

Original pedagogical numbers.

## Q1

### Given

\(1+K\frac{1}{s(s+2)(s+8)}=0\), \(K\ge 0\).

### Find

Asymptote centroid and angles, and the real-axis portions of the locus.

### Solution

Poles at \(0,-2,-8\); \(n=3,m=0\). \(\sigma_a=(-0-2-8)/3=-10/3=-3.333\). Angles \(60^\circ,180^\circ,300^\circ\). Real axis: odd count to the right ⇒ segments \((-\infty,-8]\) wait: to the right of \(s=-9\): three poles, odd, yes; between \(-8\) and \(-2\): two poles to the right (0 and -2), even, off; between \(-2\) and \(0\): one pole to the right, on; \(s>0\): zero poles to the right, off. So \((-\infty,-8]\cup[-2,0]\).

### Answer

Centroid \(-10/3\); angles \(60^\circ,180^\circ,300^\circ\); real locus \((-\infty,-8]\cup[-2,0]\).

## Q2

### Given

Same \(L=K/[s(s+2)(s+8)]\) as Q1.

### Find

The Routh gain \(K_u\) and frequency \(\omega_u\) at the \(j\omega\) crossing.

### Solution

\(p=s^3+10s^2+16s+K\). Routh: \(s^3:\ 1,16\); \(s^2:\ 10,K\); \(s^1:\ (160-K)/10\); \(s^0:\ K\). Crossing \(K_u=160\). Auxiliary \(10s^2+160=0\) ⇒ \(s^2=-16\) ⇒ \(\omega_u=4\).

### Answer

\(K_u=160\), \(\omega_u=4\,\mathrm{rad/s}\).

## Q3

### Given

\(G_{\mathrm{ol}}=(s+3)/[s(s+1)]\), Evans \(K\ge 0\).

### Find

The real-axis break-in or breakaway point(s).

### Solution

\(K=-s(s+1)/(s+3)\). Set \(dK/ds=0\). Alternatively \(\frac{1}{\sigma}+\frac{1}{\sigma+1}=\frac{1}{\sigma+3}\). Multiply: \((\sigma+1+\sigma)/[\sigma(\sigma+1)]=1/(\sigma+3)\) ⇒ \((2\sigma+1)(\sigma+3)=\sigma(\sigma+1)\) ⇒ \(2\sigma^2+6\sigma+\sigma+3=\sigma^2+\sigma\) ⇒ \(\sigma^2+6\sigma+3=0\) ⇒ \(\sigma=-3\pm\sqrt{6}\). \(\sigma=-3+2.449=-0.551\) lies in \((-1,0)\)? Poles 0,-1 zero -3. Real locus: \((-\infty,-3]\cup[-1,0]\). \(-3-\sqrt{6}=-5.449\) is on \((-\infty,-3]\) (breakaway of the two left branches toward the zero and \(-\infty\)). \(-0.551\) is on \([-1,0]\) (break-in from the complex pair, or breakaway between 0 and -1). For this zero-pole pattern the segment \([-1,0]\) is on the locus and \(-0.551\) is the breakaway between the two real poles, after which branches go complex and later break in at \(-5.449\) toward the zero and the infinite zero? \(n-m=1\), one asymptote at 180°, so one branch to \(-\infty\) along the real axis; the other ends at the zero. So \(-5.449\) is break-in (complex pair arrives on the real axis), \(-0.551\) is breakaway.

### Answer

Breakaway \(\sigma=-3+\sqrt{6}\approx-0.551\); break-in \(\sigma=-3-\sqrt{6}\approx-5.45\).

## Q4

### Given

Open-loop poles at \(-1\pm j2\) and at \(0\); no finite zeros; \(K\ge 0\).

### Find

The angle of departure from the pole at \(-1+j2\).

### Solution

Vectors to \(-1+j2\): from pole at 0: angle \(\angle(-1+j2)=116.57^\circ\). From conjugate \(-1-j2\): vertical, \(90^\circ\). From itself: excluded. No zeros. Net pole angles \(116.57+90=206.57^\circ\). \(\theta_{\mathrm{dep}}=180-206.57=-26.57^\circ\) relative to the positive real direction through the pole, i.e. the branch leaves 26.6° below the \(+\) real-parallel, toward the left half (the usual drawing: slightly downward of the negative-horizontal). Equivalently \(\theta_{\mathrm{dep}}=180^\circ-\sum\angle_{\mathrm{poles}}+\sum\angle_{\mathrm{zeros}}=-26.6^\circ\).

### Answer

Departure angle \(-26.6^\circ\) (from the \(+\) real direction at that pole).

## Q5

### Given

A point \(s=-2+j2\) is known to lie on the locus of \(1+K/(s(s+4))=0\).

### Find

The gain \(K\) at that point, and \(\zeta\) of that closed-loop pair.

### Solution

\(|G_{\mathrm{ol}}|=1/(|s||s+4|)\). \(|s|=\sqrt{8}=2\sqrt{2}\). \(|s+4|=|-2+j2+4|=|2+j2|=2\sqrt{2}\). \(K=|s||s+4|=8\). \(\zeta=\cos\theta\) with \(\theta=\angle\) from negative real: the pole is at angle \(135^\circ\) from \(+\) real, so \(45^\circ\) from \(-\) real, \(\zeta=\cos 45^\circ=0.707\). Check angle: \(\angle 1/(s(s+4))=-(\angle s+\angle(s+4))=- (135^\circ+45^\circ)=-180^\circ\), on the locus. Characteristic \(s^2+4s+K=s^2+4s+8=(s+2)^2+4\), poles \(-2\pm j2\), yes.

### Answer

\(K=8\); \(\zeta=0.707\).
