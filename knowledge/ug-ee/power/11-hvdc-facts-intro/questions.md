# Questions — HVDC and FACTS at UG level

Original numbers.

## Q1

### Given

A 6-pulse LCC rectifier, line-to-line AC voltage at the converter transformer secondary \(166\ \mathrm{kV}\), firing angle \(\alpha=15^\circ\), neglect overlap.

### Find

No-load delayed DC voltage \(V_d=V_{d0}\cos\alpha\).

### Solution

\[
V_{d0}=\frac{3\sqrt{2}}{\pi}\times 166=\frac{4.243}{3.1416}\times 166=224.1\ \mathrm{kV},
\]
\[
V_d=224.1\cos 15^\circ=216.4\ \mathrm{kV}.
\]

### Answer

\(216.4\ \mathrm{kV}\)

## Q2

### Given

Two-terminal HVDC. Rectifier \(V_{d1}=500\ \mathrm{kV}\), inverter \(V_{d2}=490\ \mathrm{kV}\), line resistance \(8.0\ \Omega\) (total).

### Find

DC current and power delivered at the inverter.

### Solution

\[
I_d=\frac{500-490}{8}=1.25\ \mathrm{kA},\qquad P_2=490\times 1.25=612.5\ \mathrm{MW}.
\]

Rectifier power \(500\times 1.25=625\ \mathrm{MW}\); line loss \(I_d^2 R=12.5\ \mathrm{MW}\).

### Answer

\(I_d=1.25\ \mathrm{kA}\); \(P_{\mathrm{inv}}=612.5\ \mathrm{MW}\)

## Q3

### Given

Lossless AC line \(X=80\ \Omega\), \(V_s=V_r=220\ \mathrm{kV}\) line-to-line, \(\delta=20^\circ\). A series capacitor compensates 40% of \(X\).

### Find

Three-phase power before and after compensation.

### Solution

Uncompensated:

\[
P=\frac{V^2}{X}\sin\delta=\frac{220^2}{80}\sin 20^\circ=605\times 0.3420=206.9\ \mathrm{MW}.
\]

\(X_{\mathrm{net}}=80(1-0.40)=48\ \Omega\):

\[
P=\frac{220^2}{48}\sin 20^\circ=1008.3\times 0.3420=344.8\ \mathrm{MW}.
\]

(The \(V^2/X\) form is the three-phase power with line-to-line voltages.)

### Answer

\(206.9\ \mathrm{MW}\) uncompensated; \(344.8\ \mathrm{MW}\) compensated

## Q4

### Given

A STATCOM at a bus \(V=1.02\ \mathrm{pu}\) on \(100\ \mathrm{MVA}\), \(132\ \mathrm{kV}\) injects capacitive (var-generating) current \(0.15\ \mathrm{pu}\) (current base = \(S/(\sqrt{3}V)\)).

### Find

Three-phase Q in Mvar (generator convention at the STATCOM, positive Q supplied to the grid).

### Solution

\[
Q_{\mathrm{pu}}=V I_q=1.02\times 0.15=0.153\ \mathrm{pu}=15.3\ \mathrm{Mvar}.
\]

### Answer

\(15.3\ \mathrm{Mvar}\) supplied

## Q5

### Given

LCC terminal transferring \(800\ \mathrm{MW}\). Approximate reactive consumption \(0.55\) of P (both ends similar, use one terminal).

### Find

Reactive power drawn from the AC bus at that terminal, and a capacitor bank Mvar to fully compensate it at that operating point.

### Solution

\[
Q=0.55\times 800=440\ \mathrm{Mvar}.
\]

A shunt bank of \(440\ \mathrm{Mvar}\) at the actual bus voltage would cancel this snapshot; filters share some of that duty in a real yard.

### Answer

\(440\ \mathrm{Mvar}\) (bank \(440\ \mathrm{Mvar}\) at that voltage)

## Q6

### Given

Midpoint shunt compensation: two lossless halves of \(X/2=50\ \Omega\) each, sending and receiving and midpoint voltages all \(400\ \mathrm{kV}\) line-to-line, total angle \(\delta=30^\circ\).

### Find

Three-phase power using \(P=(2 V V_m/X)\sin(\delta/2)\) with \(X=100\ \Omega\), \(V=V_m=400\ \mathrm{kV}\).

### Solution

\[
P=\frac{2\times 400\times 400}{100}\sin 15^\circ=3200\times 0.2588=828.2\ \mathrm{MW}.
\]

Without midpoint support, \(P=(400^2/100)\sin 30^\circ=1600\times 0.5=800\ \mathrm{MW}\). The midpoint device raises P slightly at this modest angle and, more importantly, supports voltage.

### Answer

\(828.2\ \mathrm{MW}\)
