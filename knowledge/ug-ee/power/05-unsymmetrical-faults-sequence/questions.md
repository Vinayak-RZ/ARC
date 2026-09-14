# Questions — Sequence networks, LG/LL/LLG

Original numbers. Unloaded prefault \(E_1=1.0\angle 0^\circ\ \mathrm{pu}\) unless stated. Bolted faults unless \(Z_f\) is given.

## Q1

### Given

At a bus, \(Z_1=j0.20\ \mathrm{pu}\), \(Z_2=j0.20\ \mathrm{pu}\), \(Z_0=j0.10\ \mathrm{pu}\). Solid LG fault, phase a to ground.

### Find

Sequence currents \(I_0=I_1=I_2\) and phase current \(I_a\) in pu.

### Solution

Series connection:

\[
I_1=\frac{1.0}{j0.20+j0.20+j0.10}=\frac{1}{j0.50}=-j2.0\ \mathrm{pu}.
\]
\[
I_0=I_2=I_1=-j2.0\ \mathrm{pu},\qquad I_a=3I_1=-j6.0\ \mathrm{pu}.
\]

### Answer

\(I_0=I_1=I_2=-j2.0\ \mathrm{pu}\); \(I_a=-j6.0\ \mathrm{pu}\)

## Q2

### Given

Same Thevenin impedances as Q1. Bolted three-phase fault.

### Find

Fault current \(I_a\) in pu, and the ratio \(|I_{a,\mathrm{LG}}|/|I_{a,3\phi}|\) using Q1.

### Solution

\[
I_{a,3\phi}=\frac{1}{Z_1}=-j5.0\ \mathrm{pu}.
\]

From Q1, \(|I_{a,\mathrm{LG}}|=6.0\). Ratio \(6.0/5.0=1.20\). LG is more severe here because \(Z_0<Z_1\).

### Answer

\(-j5.0\ \mathrm{pu}\); ratio \(1.20\)

## Q3

### Given

Same \(Z_1=Z_2=j0.20\ \mathrm{pu}\). Bolted LL fault on phases b and c.

### Find

\(|I_b|\) in pu.

### Solution

\[
I_1=\frac{1}{Z_1+Z_2}=\frac{1}{j0.40}=-j2.5\ \mathrm{pu},\qquad I_2=-I_1=j2.5\ \mathrm{pu},\quad I_0=0.
\]
\[
I_b=I_0+a^2 I_1+a I_2=a^2(-j2.5)+a(j2.5)=(a-a^2)(j2.5).
\]

\(a-a^2=j\sqrt{3}\), so \(I_b=(j\sqrt{3})(j2.5)=-\sqrt{3}\times 2.5=-4.330\ \mathrm{pu}\). Magnitude \(4.330\ \mathrm{pu}\).

Equivalently \(|I_b|=\sqrt{3}|I_1|=\sqrt{3}\times 2.5=4.330\ \mathrm{pu}\).

### Answer

\(4.330\ \mathrm{pu}\)

## Q4

### Given

LG fault through \(Z_f=j0.05\ \mathrm{pu}\). \(Z_1=j0.15\), \(Z_2=j0.15\), \(Z_0=j0.25\ \mathrm{pu}\). \(E_1=1.0\ \mathrm{pu}\).

### Find

\(I_a\) in pu.

### Solution

\[
I_1=\frac{1}{Z_1+Z_2+Z_0+3Z_f}=\frac{1}{j(0.15+0.15+0.25+0.15)}=\frac{1}{j0.70}=-j1.429\ \mathrm{pu}.
\]
\[
I_a=3I_1=-j4.286\ \mathrm{pu}.
\]

### Answer

\(-j4.286\ \mathrm{pu}\)

## Q5

### Given

Bolted LLG on phases b-c-g. \(Z_1=j0.25\), \(Z_2=j0.25\), \(Z_0=j0.40\ \mathrm{pu}\). \(E_1=1.0\ \mathrm{pu}\).

### Find

Sequence currents \(I_1,I_2,I_0\) in pu.

### Solution

Parallel of \(Z_2\) and \(Z_0\):

\[
Z_2\parallel Z_0=j\frac{0.25\times 0.40}{0.25+0.40}=j\frac{0.10}{0.65}=j0.15385\ \mathrm{pu}.
\]
\[
I_1=\frac{1}{Z_1+Z_2\parallel Z_0}=\frac{1}{j0.25+j0.15385}=-j2.476\ \mathrm{pu}.
\]
\[
I_2=-I_1\frac{Z_0}{Z_2+Z_0}=-(-j2.476)\frac{0.40}{0.65}=j2.476\times 0.6154=j1.524\ \mathrm{pu}.
\]
\[
I_0=-I_1\frac{Z_2}{Z_2+Z_0}=j2.476\times\frac{0.25}{0.65}=j0.952\ \mathrm{pu}.
\]

Check: \(I_2+I_0=-(-I_1)=j2.476\), and \(j1.524+j0.952=j2.476\).

### Answer

\(I_1=-j2.476\ \mathrm{pu}\), \(I_2=j1.524\ \mathrm{pu}\), \(I_0=j0.952\ \mathrm{pu}\)

## Q6

### Given

A grounded-Y / delta transformer, leakage \(X=0.10\ \mathrm{pu}\) on the study base, sits between an HV bus (Y-grounded, \(Z_g=0\)) and a delta MV bus. Positive-sequence Thevenin at the HV bus from the rest of the HV system (excluding this transformer) is \(Z_1^{\mathrm{HV}}=j0.12\ \mathrm{pu}\). The MV delta system is open (no other sources). Fault is LG on the HV bus.

### Find

\(Z_1,Z_2,Z_0\) at the HV fault bus, and \(I_a\) for bolted LG. Take \(Z_2=Z_1\) for the HV Thevenin and the transformer. Zero-sequence: transformer provides a path \(j0.10\) to reference on the HV side; HV system \(Z_0^{\mathrm{HV}}=\infty\) (ungrounded sources). \(E_1=1.0\ \mathrm{pu}\).

### Solution

Positive sequence: transformer MV open means the transformer does not shunt \(Z_1\) (no MV load/source). So \(Z_1=Z_1^{\mathrm{HV}}=j0.12\ \mathrm{pu}\). Likewise \(Z_2=j0.12\ \mathrm{pu}\).

Zero sequence: HV network open (\(Z_0^{\mathrm{HV}}=\infty\)), but the grounded-Y/Δ transformer is a shunt \(jX_t=j0.10\) at the HV bus. \(Z_0=j0.10\ \mathrm{pu}\).

\[
I_1=\frac{1}{j0.12+j0.12+j0.10}=-j2.941\ \mathrm{pu},\qquad I_a=-j8.824\ \mathrm{pu}.
\]

### Answer

\(Z_1=Z_2=j0.12\ \mathrm{pu}\), \(Z_0=j0.10\ \mathrm{pu}\); \(I_a=-j8.82\ \mathrm{pu}\)
