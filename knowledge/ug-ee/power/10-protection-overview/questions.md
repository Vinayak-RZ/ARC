# Questions — Zones, CTs/VTs, overcurrent intro

Original numbers.

## Q1

### Given

A CT, ratio \(400/5\), ideal. Primary fault current \(6.4\ \mathrm{kA}\) RMS.

### Find

Secondary current.

### Solution

\[
n=\frac{400}{5}=80,\qquad I_s=\frac{6400}{80}=80\ \mathrm{A}.
\]

### Answer

\(80\ \mathrm{A}\)

## Q2

### Given

IEC standard inverse: \(\alpha=0.02\), \(\beta=0.14\), pickup \(I_s=5.0\ \mathrm{A}\) secondary, \(\mathrm{TMS}=0.25\). Fault current \(20\ \mathrm{A}\) secondary.

### Find

Operating time.

### Solution

\[
\frac{I}{I_s}=4.0,\qquad t=0.25\times\frac{0.14}{4^{0.02}-1}.
\]
\[
4^{0.02}=e^{0.02\ln 4}=e^{0.02773}=1.0281,
\]
\[
t=0.25\times\frac{0.14}{0.0281}=0.25\times 4.982=1.246\ \mathrm{s}.
\]

### Answer

\(1.25\ \mathrm{s}\)

## Q3

### Given

A radial 66 kV line, positive-sequence \(Z_L=4+j20\ \Omega\). Bolted three-phase fault at 70% of the line length. Relay at the sending end; source behind the relay is strong enough that the line impedance dominates the apparent impedance (neglect source \(Z\) only if using \(Z_{\mathrm{app}}=m Z_L\) as instructed — here include nothing but the line, as in the homogeneous-line distance sketch).

### Find

Primary apparent impedance seen by a phase-distance element.

### Solution

\[
Z_{\mathrm{app}}=0.70(4+j20)=2.8+j14\ \Omega.
\]

### Answer

\(2.8+j14\ \Omega\)

## Q4

### Given

CT \(200/5\), VT \(33\,\mathrm{kV}/110\,\mathrm{V}\) (line-to-line ratios). Primary apparent impedance \(12.0\ \Omega\).

### Find

Secondary ohms for the distance relay, \(Z_{\mathrm{sec}}=Z_{\mathrm{pri}}\times(\mathrm{CTR}/\mathrm{VTR})\).

### Solution

\[
\mathrm{CTR}=\frac{200}{5}=40,\qquad \mathrm{VTR}=\frac{33000}{110}=300,
\]
\[
Z_{\mathrm{sec}}=12.0\times\frac{40}{300}=1.60\ \Omega.
\]

### Answer

\(1.60\ \Omega\) secondary

## Q5

### Given

Downstream inverse relay operates in \(0.35\ \mathrm{s}\) at a through-fault current. Breaker interrupting time \(0.08\ \mathrm{s}\). Desired coordination time interval margin \(0.25\ \mathrm{s}\) (relay errors and safety).

### Find

The minimum upstream relay operating time at the same current.

### Solution

\[
t_{\mathrm{up}}\ge 0.35+0.08+0.25=0.68\ \mathrm{s}.
\]

### Answer

\(0.68\ \mathrm{s}\)

## Q6

### Given

Simple two-terminal differential with currents into the zone \(\mathbf{I}_1=4.0\angle 0^\circ\ \mathrm{A}\), \(\mathbf{I}_2=3.8\angle 178^\circ\ \mathrm{A}\) secondary (external-fault-like, CT mismatch). Operate \(I_{\mathrm{op}}=|\mathbf{I}_1+\mathbf{I}_2|\), restrain \(I_{\mathrm{res}}=(|I_1|+|I_2|)/2\). Slope \(k=0.30\), pickup \(0.20\ \mathrm{A}\). Trip if \(I_{\mathrm{op}}>k I_{\mathrm{res}}+0.20\).

### Find

Whether the relay trips.

### Solution

\[
\mathbf{I}_2=3.8(\cos 178+j\sin 178)=-3.798+j0.133,
\]
\[
\mathbf{I}_1+\mathbf{I}_2=0.202+j0.133,\qquad I_{\mathrm{op}}=0.242\ \mathrm{A}.
\]
\[
I_{\mathrm{res}}=\frac{4.0+3.8}{2}=3.90\ \mathrm{A},\qquad k I_{\mathrm{res}}+0.20=1.17+0.20=1.37\ \mathrm{A}.
\]

\(0.242<1.37\), no trip (through-fault restraint holds).

### Answer

No trip (\(I_{\mathrm{op}}=0.24\ \mathrm{A}<1.37\ \mathrm{A}\))
