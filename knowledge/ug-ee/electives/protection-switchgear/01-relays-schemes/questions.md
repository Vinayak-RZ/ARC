# Questions — Overcurrent, differential, distance schemes

Original numbers.

## Q1

### Given

IEC standard inverse: \(\alpha=0.02\), \(\beta=0.14\), pickup \(I_s=4.0\,\mathrm{A}\) secondary, \(\mathrm{TMS}=0.30\). Fault current \(16.0\,\mathrm{A}\) secondary.

### Find

Relay operating time.

### Solution

\[
\frac{I}{I_s}=4.0,\qquad 4^{0.02}=e^{0.02\ln 4}=e^{0.027725}=1.02811,
\]
\[
t=0.30\times\frac{0.14}{1.02811-1}=0.30\times\frac{0.14}{0.02811}=0.30\times 4.980=1.494\,\mathrm{s}.
\]

### Answer

\(1.49\,\mathrm{s}\)

## Q2

### Given

A 132 kV line, positive-sequence \(Z_L=8.0+j40.0\,\Omega\). Zone-1 reach 80% of the line. CT \(600/5\), VT \(132\,\mathrm{kV}/110\,\mathrm{V}\) (line-to-line ratios).

### Find

Zone-1 primary ohms and secondary ohms (magnitude of \(Z_L\) used for a mho diameter along the line; report the complex reach \(0.80 Z_L\) in primary and secondary).

### Solution

\[
Z_{1,\mathrm{pri}}=0.80(8+j40)=6.40+j32.0\,\Omega.
\]
\[
\mathrm{CTR}=600/5=120,\qquad\mathrm{VTR}=132000/110=1200,
\]
\[
Z_{1,\mathrm{sec}}=(6.40+j32.0)\times\frac{120}{1200}=0.640+j3.20\,\Omega.
\]

### Answer

Primary \(6.40+j32.0\,\Omega\); secondary \(0.640+j3.20\,\Omega\)

## Q3

### Given

Two-terminal differential, currents into the zone \(\mathbf{I}_1=6.0\angle 0^\circ\,\mathrm{A}\), \(\mathbf{I}_2=5.7\angle 175^\circ\,\mathrm{A}\) secondary. Slope \(k=0.40\), pickup \(0.25\,\mathrm{A}\). Trip if \(I_{\mathrm{op}}>k I_{\mathrm{res}}+0.25\) with \(I_{\mathrm{op}}=|\mathbf{I}_1+\mathbf{I}_2|\) and \(I_{\mathrm{res}}=(|I_1|+|I_2|)/2\).

### Find

Operate current, restrain current, threshold, and whether the relay trips.

### Solution

\[
\mathbf{I}_2=5.7(\cos 175^\circ+j\sin 175^\circ)=-5.678+j0.497,
\]
\[
\mathbf{I}_1+\mathbf{I}_2=0.322+j0.497,\qquad I_{\mathrm{op}}=\sqrt{0.322^2+0.497^2}=0.592\,\mathrm{A}.
\]
\[
I_{\mathrm{res}}=(6.0+5.7)/2=5.85\,\mathrm{A},\qquad k I_{\mathrm{res}}+0.25=2.34+0.25=2.59\,\mathrm{A}.
\]

\(0.592<2.59\): no trip (through-fault restraint).

### Answer

\(I_{\mathrm{op}}=0.592\,\mathrm{A}\), \(I_{\mathrm{res}}=5.85\,\mathrm{A}\), threshold \(2.59\,\mathrm{A}\), no trip

## Q4

### Given

Downstream 51 operates in \(0.42\,\mathrm{s}\) at a through-fault. Breaker interrupting time \(0.06\,\mathrm{s}\). Desired margin \(0.28\,\mathrm{s}\). Upstream IEC SI, \(I_s=5.0\,\mathrm{A}\), fault \(25.0\,\mathrm{A}\) secondary (\(\alpha=0.02\), \(\beta=0.14\)).

### Find

Minimum upstream TMS so that \(t_{\mathrm{up}}\ge 0.42+0.06+0.28\).

### Solution

\[
t_{\mathrm{up,min}}=0.76\,\mathrm{s},\qquad I/I_s=5,\qquad 5^{0.02}=e^{0.02\ln 5}=1.0327,
\]
\[
\frac{0.14}{0.0327}=4.281,\qquad\mathrm{TMS}_{\min}=\frac{0.76}{4.281}=0.178.
\]

### Answer

\(\mathrm{TMS}\ge 0.178\) (use \(0.20\) if the tap is in steps of \(0.05\))

## Q5

### Given

Homogeneous 66 kV line \(Z_L=3+j15\,\Omega\). Bolted three-phase fault at 55% of the line. Relay at the sending end; apparent impedance \(Z_{\mathrm{app}}=m Z_L\). Residual compensation is not required (three-phase).

### Find

Primary apparent impedance.

### Solution

\[
Z_{\mathrm{app}}=0.55(3+j15)=1.65+j8.25\,\Omega.
\]

### Answer

\(1.65+j8.25\,\Omega\)

## Q6

### Given

Earth-fault distance: \(Z_1=0.25+j1.20\,\Omega/\mathrm{km}\), \(Z_0=0.70+j3.60\,\Omega/\mathrm{km}\). Line length 40 km. Relay uses \(k_0=(Z_0-Z_1)/(3Z_1)\).

### Find

Complex \(k_0\) and zone-1 reach in primary ohms if zone 1 is \(0.80\times Z_1\ell\) (phase–earth element set on positive-sequence line impedance, compensation applied in the current path).

### Solution

\[
Z_0-Z_1=0.45+j2.40,\qquad 3Z_1=0.75+j3.60,
\]
\[
k_0=\frac{0.45+j2.40}{0.75+j3.60}=\frac{(0.45+j2.40)(0.75-j3.60)}{0.75^2+3.60^2}=\frac{8.978+j0.180}{13.5225}=0.664+j0.0133.
\]
\[
Z_{1,\mathrm{reach}}=0.80\times 40\times(0.25+j1.20)=8.00+j38.4\,\Omega.
\]

### Answer

\(k_0\approx 0.664+j0.013\); zone-1 \(8.00+j38.4\,\Omega\) primary
