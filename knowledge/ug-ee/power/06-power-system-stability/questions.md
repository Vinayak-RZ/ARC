# Questions — Swing equation, equal-area

Original numbers. Electrical radians in swing formulas; degrees allowed in statements if converted.

## Q1

### Given

Classical OMIB: \(E=1.10\ \mathrm{pu}\), \(V=1.00\ \mathrm{pu}\), \(X=0.40\ \mathrm{pu}\). Mechanical power \(P_m=1.20\ \mathrm{pu}\).

### Find

Prefault equilibrium angle \(\delta_0\) in degrees, and \(P_{\max}\).

### Solution

\[
P_{\max}=\frac{EV}{X}=\frac{1.10\times 1.00}{0.40}=2.75\ \mathrm{pu}.
\]
\[
\sin\delta_0=\frac{P_m}{P_{\max}}=\frac{1.20}{2.75}=0.4364,\qquad \delta_0=25.87^\circ.
\]

The supplementary angle \(154.13^\circ\) is the unstable equilibrium of the same prefault network, not the operating point.

### Answer

\(P_{\max}=2.75\ \mathrm{pu}\); \(\delta_0=25.87^\circ\)

## Q2

### Given

Machine \(H=5.0\ \mathrm{MJ/MVA}\) on its own base, \(f=50\ \mathrm{Hz}\). During a bolted terminal fault \(P_e=0\), \(P_m=0.80\ \mathrm{pu}\) on the same base. Rotor starts at rest relative to synchronous speed, \(\delta_0=20^\circ\).

### Find

Rotor angle at \(t=0.12\ \mathrm{s}\) after fault inception, in degrees.

### Solution

\(\omega_s=2\pi\times 50=314.16\ \mathrm{rad/s}\). \(\delta_0=20^\circ=0.3491\ \mathrm{rad}\).

\[
\delta(t)=\delta_0+\frac{\omega_s P_m}{4H}t^2=0.3491+\frac{314.16\times 0.80}{4\times 5.0}(0.12)^2.
\]
\[
\frac{\omega_s P_m}{4H}=\frac{251.33}{20}=12.566\ \mathrm{rad/s}^2,
\]
\[
\Delta\delta=12.566\times 0.0144=0.1810\ \mathrm{rad}=10.37^\circ.
\]
\[
\delta=20+10.37=30.37^\circ.
\]

### Answer

\(30.37^\circ\)

## Q3

### Given

Postfault \(P_{\max}=2.00\ \mathrm{pu}\), \(P_m=1.00\ \mathrm{pu}\).

### Find

The unstable equilibrium angle \(\delta_u\) in degrees.

### Solution

\[
\sin\delta_{\mathrm{eq}}=\frac{1.00}{2.00}=0.50,\qquad \delta_{\mathrm{stable}}=30^\circ,\qquad \delta_u=180^\circ-30^\circ=150^\circ.
\]

### Answer

\(150^\circ\)

## Q4

### Given

Prefault \(\delta_0=25^\circ\), during-fault \(P_e=0\), \(P_m=0.90\ \mathrm{pu}\), clearing angle \(\delta_c=50^\circ\). Postfault \(P_e=2.2\sin\delta\ \mathrm{pu}\). Unstable angle \(\delta_u=140^\circ\).

### Find

Accelerating area \(A_1\) and the available decelerating area from \(\delta_c\) to \(\delta_u\), both in pu·radian. State whether first-swing EAC predicts stability.

### Solution

Convert: \(\delta_0=0.4363\ \mathrm{rad}\), \(\delta_c=0.8727\ \mathrm{rad}\), \(\delta_u=2.4435\ \mathrm{rad}\).

\[
A_1=P_m(\delta_c-\delta_0)=0.90\times(0.8727-0.4363)=0.3928\ \mathrm{pu\cdot rad}.
\]

\[
A_2=\int_{\delta_c}^{\delta_u}(2.2\sin\delta-0.90)\,d\delta=2.2(\cos\delta_c-\cos\delta_u)-0.90(\delta_u-\delta_c).
\]
\[
\cos 50^\circ=0.6428,\quad\cos 140^\circ=-0.7660,
\]
\[
A_2=2.2(0.6428-(-0.7660))-0.90(2.4435-0.8727)=2.2(1.4088)-0.90(1.5708)=3.099-1.414=1.685\ \mathrm{pu\cdot rad}.
\]

\(A_2>A_1\), so the equal-area criterion predicts first-swing stability (neglecting damping).

### Answer

\(A_1=0.393\ \mathrm{pu\cdot rad}\); \(A_2=1.685\ \mathrm{pu\cdot rad}\); stable

## Q5

### Given

\(P_e=0\) during the fault, \(P_m=0.80\ \mathrm{pu}\), \(\delta_0=20^\circ=0.3491\ \mathrm{rad}\), \(\delta_u=130^\circ=2.2689\ \mathrm{rad}\), postfault \(P_{\max}=1.80\ \mathrm{pu}\).

### Find

Critical clearing angle \(\delta_{\mathrm{cr}}\) in degrees from \(A_1=A_{2,\mathrm{max}}\).

### Solution

\[
P_m(\delta_{\mathrm{cr}}-\delta_0)=\int_{\delta_{\mathrm{cr}}}^{\delta_u}(P_{\max}\sin\delta-P_m)\,d\delta
\]
\[
P_m(\delta_{\mathrm{cr}}-\delta_0)=P_{\max}(\cos\delta_{\mathrm{cr}}-\cos\delta_u)-P_m(\delta_u-\delta_{\mathrm{cr}}).
\]

Bring terms with \(\delta_{\mathrm{cr}}\) together:

\[
P_m(\delta_{\mathrm{cr}}-\delta_0)+P_m(\delta_u-\delta_{\mathrm{cr}})=P_{\max}(\cos\delta_{\mathrm{cr}}-\cos\delta_u)
\]
\[
P_m(\delta_u-\delta_0)=P_{\max}(\cos\delta_{\mathrm{cr}}-\cos\delta_u)
\]
\[
\cos\delta_{\mathrm{cr}}=\frac{P_m(\delta_u-\delta_0)}{P_{\max}}+\cos\delta_u=\frac{0.80(2.2689-0.3491)}{1.80}+\cos 130^\circ.
\]
\[
\cos\delta_{\mathrm{cr}}=\frac{0.80\times 1.9198}{1.80}-0.6428=0.8532-0.6428=0.2104,
\]
\[
\delta_{\mathrm{cr}}=\cos^{-1}(0.2104)=77.85^\circ
\]

(the root in \((\delta_0,\delta_u)\), not the negative cosine companion outside the swing).

### Answer

\(77.85^\circ\)

## Q6

### Given

Two machines on a common 100 MVA base: \(H_1=4.0\ \mathrm{s}\), \(H_2=6.0\ \mathrm{s}\). Relative-motion OMIB equivalent for the pair.

### Find

Equivalent inertia \(H_{\mathrm{eq}}\).

### Solution

\[
H_{\mathrm{eq}}=\frac{H_1 H_2}{H_1+H_2}=\frac{4\times 6}{10}=2.40\ \mathrm{s}
\]

on the same 100 MVA base.

### Answer

\(2.40\ \mathrm{s}\) (on 100 MVA)
