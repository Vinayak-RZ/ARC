# Questions — Q–V, shunt/series compensation

Original numbers. Three-phase where voltages are line-to-line.

## Q1

### Given

A 11 kV bus supplies \(2.4\ \mathrm{MW}\) at \(0.75\) lagging pf. Capacitors raise the pf to \(0.95\) lagging. Voltage held at \(11\ \mathrm{kV}\), \(f=50\ \mathrm{Hz}\). Wye-connected bank.

### Find

Capacitor Mvar, and per-phase capacitance.

### Solution

\[
Q_1=P\tan\phi_1=2.4\tan(\cos^{-1}0.75)=2.4\times 0.8819=2.117\ \mathrm{Mvar},
\]
\[
Q_2=2.4\tan(\cos^{-1}0.95)=2.4\times 0.3287=0.789\ \mathrm{Mvar},
\]
\[
Q_C=2.117-0.789=1.328\ \mathrm{Mvar}.
\]
\[
C_{\mathrm{phase}}=\frac{Q_C}{3\omega V_\phi^2}=\frac{Q_C}{\omega V_{LL}^2}=\frac{1.328\times 10^6}{314.16\times 11^2\times 10^6}=34.95\ \mu\mathrm{F}.
\]

### Answer

\(Q_C=1.328\ \mathrm{Mvar}\); \(C=34.95\ \mu\mathrm{F}\) per phase (wye)

## Q2

### Given

Radial lossless line \(X=0.40\ \mathrm{pu}\), sending \(E=1.00\ \mathrm{pu}\) held. Load \(Q=0\), constant P. Voltage-limited transfer.

### Find

\(P_{\max}\) in pu and receiving \(V\) at the nose.

### Solution

\[
P_{\max}=\frac{E^2}{2X}=\frac{1}{0.80}=1.25\ \mathrm{pu},\qquad V=\frac{E}{\sqrt{2}}=0.707\ \mathrm{pu}.
\]

### Answer

\(P_{\max}=1.25\ \mathrm{pu}\); \(V=0.707\ \mathrm{pu}\)

## Q3

### Given

Same \(E=1.00\ \mathrm{pu}\), \(X=0.40\ \mathrm{pu}\), but both ends held at \(1.00\ \mathrm{pu}\) (angle-limited).

### Find

\(P_{\max}\).

### Solution

\[
P_{\max}=\frac{E V}{X}=\frac{1}{0.40}=2.50\ \mathrm{pu}
\]

at \(\delta=90^\circ\). This is twice Q2’s voltage-limited nose, as expected.

### Answer

\(2.50\ \mathrm{pu}\)

## Q4

### Given

Approximate drop \(\Delta V=(RP+XQ)/V\). \(R=0.05\ \mathrm{pu}\), \(X=0.25\ \mathrm{pu}\), \(P=0.80\ \mathrm{pu}\), \(Q=0.40\ \mathrm{pu}\), receiving \(V=0.98\ \mathrm{pu}\). Sending magnitude estimate \(V_S\approx V+\Delta V\).

### Find

\(\Delta V\) and \(V_S\).

### Solution

\[
\Delta V=\frac{0.05\times 0.80+0.25\times 0.40}{0.98}=\frac{0.04+0.10}{0.98}=0.1429\ \mathrm{pu}.
\]
\[
V_S\approx 0.98+0.143=1.123\ \mathrm{pu}.
\]

(The approximation is crude at 14% drop; a phasor calculation would be better in a design, but the formula is what the question asked.)

### Answer

\(\Delta V=0.143\ \mathrm{pu}\); \(V_S\approx 1.123\ \mathrm{pu}\)

## Q5

### Given

A 250 Mvar shunt bank rated at \(400\ \mathrm{kV}\). Operating voltage \(380\ \mathrm{kV}\).

### Find

Reactive output at 380 kV.

### Solution

\[
Q=Q_{\mathrm{rated}}\left(\frac{V}{V_{\mathrm{rated}}}\right)^2=250\left(\frac{380}{400}\right)^2=250\times 0.9025=225.6\ \mathrm{Mvar}.
\]

### Answer

\(225.6\ \mathrm{Mvar}\)

## Q6

### Given

Line \(X=100\ \Omega\), series capacitor \(X_C=35\ \Omega\), \(V_s=V_r=220\ \mathrm{kV}\), \(\delta=18^\circ\).

### Find

Compensation degree and three-phase power.

### Solution

\[
k=\frac{35}{100}=0.35,\qquad X_{\mathrm{net}}=65\ \Omega,
\]
\[
P=\frac{220^2}{65}\sin 18^\circ=744.62\times 0.3090=230.1\ \mathrm{MW}.
\]

### Answer

\(k=0.35\); \(P=230.1\ \mathrm{MW}\)
