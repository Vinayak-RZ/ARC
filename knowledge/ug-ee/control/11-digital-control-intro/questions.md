# Questions — Sampling, hold, discrete equivalents

Original pedagogical numbers.

## Q1

### Given

\(G(s)=5/(s+5)\), ZOH sampling period \(T=0.2\,\mathrm{s}\).

### Find

\(G_d(z)\) and the discrete pole.

### Solution

\(e^{-aT}=e^{-1}=0.3679\). \(G_d=(1-e^{-aT})/(z-e^{-aT})=0.6321/(z-0.3679)\). Discrete pole \(z=0.368\). DC: \(G_d(1)=0.6321/0.6321=1=G(0)\).

### Answer

\(G_d(z)=0.632/(z-0.368)\); pole at \(0.368\).

## Q2

### Given

Closed-loop discrete polynomial \(z^2-0.5z+0.4=0\).

### Find

Whether both roots lie in the open unit disk, using the quadratic Jury conditions.

### Solution

\(a=-0.5\), \(b=0.4\). \(|b|=0.4<1\). \(1+a+b=1-0.5+0.4=0.9>0\). \(1-a+b=1+0.5+0.4=1.9>0\). All hold: stable. (Roots of \(z^2-0.5z+0.4=0\): \(0.25\pm j\sqrt{0.4-0.0625}=0.25\pm j0.581\), modulus \(\sqrt{0.4}=0.632<1\).)

### Answer

Yes, both roots inside \(|z|<1\).

## Q3

### Given

Analog \(C(s)=4/(s+4)\), Tustin with \(T=0.1\,\mathrm{s}\), no prewarp.

### Find

\(C(z)\).

### Solution

\(s=20(z-1)/(z+1)\). \(C=4/[20(z-1)/(z+1)+4]=4(z+1)/[20(z-1)+4(z+1)]=4(z+1)/(24z-16)=(z+1)/(6z-4)\).

### Answer

\(C(z)=(z+1)/(6z-4)\).

## Q4

### Given

A continuous pole at \(s=-3\pm j4\), sampled at \(T=0.2\,\mathrm{s}\).

### Find

The corresponding discrete poles \(z=e^{sT}\).

### Solution

\(sT=-0.6\pm j0.8\). \(z=e^{-0.6}e^{\pm j0.8}=0.5488(\cos 0.8\pm j\sin 0.8)=0.5488(0.6967\pm j0.7174)=0.382\pm j0.394\). \(|z|=e^{-0.6}=0.549\).

### Answer

\(z=0.382\pm j0.394\) (\(|z|=0.549\)).

## Q5

### Given

Forward Euler \(s=(z-1)/T\) applied to a stable analog pole \(s=-a\), \(a>0\).

### Find

The discrete pole and the largest \(T\) for which \(|z|<1\).

### Solution

\(-a=(z-1)/T\) ⇒ \(z=1-aT\). \(|1-aT|<1\). For \(T>0\), \(1-aT>-1\) ⇒ \(aT<2\) ⇒ \(T<2/a\), and \(1-aT<1\) always. At \(T=2/a\), \(z=-1\) (marginally).

### Answer

\(z=1-aT\); need \(0<T<2/a\).
