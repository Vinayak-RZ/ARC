# Questions — V-curves, hunting, starting

Original numbers. Cylindrical rotor, \(R_a=0\) unless stated.

## Q1

### Given

3-phase, 400 V, Y-connected synchronous motor, \(X_s=4.0\ \Omega\) per phase. Shaft input electrical (converted) \(P=12.0\ \mathrm{kW}\) at unity PF. Infinite bus 400 V.

### Find

\(E_a\) (phase), load angle \(\delta\), and armature current.

### Solution

\(V_\phi=400/\sqrt{3}=230.9\ \mathrm{V}\). Unity PF, \(Q=0\). \(I_L=P/(\sqrt{3} V_L \mathrm{pf})=12000/(\sqrt{3}\times 400)=17.32\ \mathrm{A}\). Phase current same in Y.

\(\mathbf{I}=17.32\angle 0^\circ\) if \(\mathbf{V}=230.9\angle 0^\circ\). Motor: \(\mathbf{E}_a=\mathbf{V}-j X_s\mathbf{I}=230.9-j4.0\times 17.32=230.9-j69.28\).

\[
|E_a|=241.1\ \mathrm{V},\qquad \delta=\tan^{-1}(69.28/230.9)=16.7^\circ
\]

(behind the terminal voltage). Check \(P=3 V E_a\sin\delta / X_s=3\times 230.9\times 241.1\times\sin 16.7^\circ / 4.0=12.00\ \mathrm{kW}\).

### Answer

\(E_a=241\ \mathrm{V}\) (phase), \(\delta=16.7^\circ\), \(I=17.3\ \mathrm{A}\)

## Q2

### Given

Same motor and bus as Q1. Same \(P=12\ \mathrm{kW}\), now 0.80 leading PF (overexcited).

### Find

Armature current, \(Q\) (three-phase, motor supplying vars if \(Q>0\)), and \(|E_a|\).

### Solution

\(S=P/\mathrm{pf}=12/0.8=15\ \mathrm{kVA}\), \(I=15000/(\sqrt{3}\times 400)=21.65\ \mathrm{A}\). Leading: \(\mathbf{I}=21.65\angle +36.87^\circ\).

\(Q=15\sin 36.87^\circ=9.00\ \mathrm{kVAR}\) supplied.

\[
\mathbf{I}=21.65(0.8+j0.6)=17.32+j12.99\ \mathrm{A},
\]

\[
jX_s\mathbf{I}=j4(17.32+j12.99)=-51.96+j69.28,
\]

\[
\mathbf{E}_a=\mathbf{V}-jX_s\mathbf{I}=230.9-(-51.96+j69.28)=282.9-j69.28,
\]

\[
|E_a|=291.2\ \mathrm{V}.
\]

### Answer

\(I=21.7\ \mathrm{A}\), \(Q=9.00\ \mathrm{kVAR}\) (leading), \(|E_a|=291\ \mathrm{V}\)

## Q3

### Given

Synchronous condenser, 11 kV, \(X_s=8.0\ \Omega\) per phase, Y-connected, \(P=0\), lossless. Field set so \(E_a=7.5\ \mathrm{kV}\) phase.

### Find

Line current and three-phase reactive power. Phase voltage \(11/\sqrt{3}=6.351\ \mathrm{kV}\).

### Solution

\(\delta=0\), \(I=(E_a-V)/X_s=(7500-6351)/8.0=143.6\ \mathrm{A}\) (leading, overexcited).

\[
Q=3 V I=3\times 6351\times 143.6=2.735\ \mathrm{MVAR}
\]

(supplied). Alternatively \(Q=3(E_a-V)V/X_s=3(7500-6351)(6351)/8.0=2.735\ \mathrm{MVAR}\).

### Answer

\(I_L=144\ \mathrm{A}\) leading, \(Q=2.74\ \mathrm{MVAR}\) supplied

## Q4

### Given

Cylindrical motor, \(V_\phi=1.0\ \mathrm{pu}\), \(X_s=0.80\ \mathrm{pu}\), \(E_a=1.20\ \mathrm{pu}\), \(P=0.90\ \mathrm{pu}\). Inertia constant \(H=5.0\ \mathrm{s}\), \(\omega_s=314\ \mathrm{rad/s}\) (electrical, 50 Hz). Neglect damping.

### Find

Load angle \(\delta\), synchronizing power \(P_\mathrm{syn}=\mathrm{d}P/\mathrm{d}\delta\) in pu/rad, and small-signal hunting frequency in hertz.

### Solution

\[
P=\frac{V E_a}{X_s}\sin\delta \implies 0.90=\frac{1.20}{0.80}\sin\delta=1.50\sin\delta,
\]

\[
\sin\delta=0.60,\qquad \delta=36.87^\circ=0.6435\ \mathrm{rad}.
\]

\[
P_\mathrm{syn}=\frac{V E_a}{X_s}\cos\delta=1.50\times 0.80=1.20\ \mathrm{pu/rad}.
\]

Swing: \(\frac{2H}{\omega_s}\ddot{\delta}+P_\mathrm{syn}\delta=0\) for small \(\Delta\delta\), \(\omega_n=\sqrt{\omega_s P_\mathrm{syn}/(2H)}=\sqrt{314\times 1.20/10}=\sqrt{37.68}=6.138\ \mathrm{rad/s}\).

\[
f_n=6.138/(2\pi)=0.977\ \mathrm{Hz}.
\]

### Answer

\(\delta=36.9^\circ\), \(P_\mathrm{syn}=1.20\ \mathrm{pu/rad}\), \(f_n=0.98\ \mathrm{Hz}\)

## Q5

### Given

A 50 Hz, 8-pole synchronous motor is to be induction-started on dampers. Rated field voltage 110 V DC. During start the field is closed through a 20 Ω discharge resistor; field winding resistance 2.0 Ω. Approximate open-circuit induced field voltage at \(s=1\) (standstill, rated stator voltage) as 900 V RMS.

### Find

RMS current in the field discharge circuit at the instant of start, and the mechanical synchronous speed.

### Solution

Discharge loop \(Z\approx R_f+R_d=22\ \Omega\) if inductance is ignored for a UG magnitude estimate (actual current is also limited by field inductance at 50 Hz). \(I_\mathrm{rms}\approx 900/22=40.9\ \mathrm{A}\).

If \(L_f\) were given, \(I=900/\sqrt{22^2+(2\pi 50 L_f)^2}\). Without \(L_f\), 40.9 A is the resistive upper bound.

\[
n_s=120\times 50/8=750\ \mathrm{r/min}.
\]

### Answer

\(I_\mathrm{f,start}\lesssim 40.9\ \mathrm{A}\) RMS (resistive bound), \(n_s=750\ \mathrm{r/min}\)
