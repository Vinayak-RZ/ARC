# Questions — Zbus, bolted three-phase faults

Original numbers. Resistances neglected unless stated. Unloaded prefault \(V=1.0\ \mathrm{pu}\) unless a prefault voltage is given.

## Q1

### Given

Generator \(G\): \(100\ \mathrm{MVA}\), \(X''=0.20\ \mathrm{pu}\) on nameplate. Transformer \(T\): \(100\ \mathrm{MVA}\), \(X=0.10\ \mathrm{pu}\). Solid three-phase fault on the transformer HV bus. System base \(100\ \mathrm{MVA}\). Prefault voltage \(1.0\ \mathrm{pu}\).

### Find

Fault current in pu on \(100\ \mathrm{MVA}\).

### Solution

Same MVA base. Thevenin reactance \(X_{\mathrm{th}}=X''+X_T=0.20+0.10=0.30\ \mathrm{pu}\).

\[
I_f=\frac{1.0}{j0.30}=-j3.333\ \mathrm{pu}.
\]

### Answer

\(3.333\ \mathrm{pu}\)

## Q2

### Given

The HV bus of Q1 is \(220\ \mathrm{kV}\). Base \(100\ \mathrm{MVA}\).

### Find

RMS line current in kA and three-phase fault MVA.

### Solution

\[
I_\mathrm{base}=\frac{100}{\sqrt{3}\times 220}=0.2624\ \mathrm{kA},
\]
\[
I_f=3.333\times 0.2624=0.8747\ \mathrm{kA}.
\]
\[
S_{\mathrm{sc}}=\frac{100}{0.30}=333.3\ \mathrm{MVA}.
\]

Check: \(\sqrt{3}\times 220\times 0.8747\approx 333\ \mathrm{MVA}\).

### Answer

\(0.875\ \mathrm{kA}\); \(333.3\ \mathrm{MVA}\)

## Q3

### Given

Two generators, each \(50\ \mathrm{MVA}\), \(X''=0.16\ \mathrm{pu}\) on their own ratings, connected in parallel through identical transformers \(X=0.08\ \mathrm{pu}\) on \(50\ \mathrm{MVA}\) to a common 11 kV bus, which is then faulted (three-phase bolted). Study base \(100\ \mathrm{MVA}\). Prefault \(1.0\ \mathrm{pu}\).

### Find

\(I_f\) in pu on \(100\ \mathrm{MVA}\).

### Solution

Each machine \(X''\) on 100 MVA: \(0.16\times 100/50=0.32\ \mathrm{pu}\). Each transformer: \(0.08\times 100/50=0.16\ \mathrm{pu}\). Each path: \(0.32+0.16=0.48\ \mathrm{pu}\). Two parallel paths:

\[
X_{\mathrm{th}}=\frac{0.48}{2}=0.24\ \mathrm{pu},\qquad I_f=\frac{1}{0.24}=4.167\ \mathrm{pu}.
\]

### Answer

\(4.167\ \mathrm{pu}\)

## Q4

### Given

Bus impedance matrix on 100 MVA (reactances, pu):

\[
Z_\mathrm{bus}=j\begin{pmatrix}0.20&0.08\\0.08&0.16\end{pmatrix}.
\]

Prefault voltages \(V_1(0)=1.02\ \mathrm{pu}\), \(V_2(0)=0.98\ \mathrm{pu}\). Bolted three-phase fault at bus 2.

### Find

Fault current \(I_f\) and postfault voltage at bus 1.

### Solution

\[
I_f=\frac{V_2(0)}{Z_{22}}=\frac{0.98}{j0.16}=-j6.125\ \mathrm{pu}.
\]
\[
V_1^{\mathrm{post}}=V_1(0)-Z_{12}I_f=1.02-(j0.08)(-j6.125)=1.02-0.490=0.530\ \mathrm{pu}.
\]

(The product \(j\times(-j)=1\), so \(Z_{12}I_f=+0.490\).)

### Answer

\(I_f=-j6.125\ \mathrm{pu}\); \(V_1=0.530\ \mathrm{pu}\)

## Q5

### Given

An infinite bus with short-circuit level \(2500\ \mathrm{MVA}\) at \(132\ \mathrm{kV}\), connected through a line \(X=0.12\ \mathrm{pu}\) on \(100\ \mathrm{MVA}\) to bus F. Bolted three-phase fault at F. Prefault voltage \(1.0\ \mathrm{pu}\) on \(100\ \mathrm{MVA}\).

### Find

Thevenin reactance at F and \(I_f\) in pu on \(100\ \mathrm{MVA}\).

### Solution

Infinite-bus reactance on 100 MVA:

\[
X_\infty=\frac{S_\mathrm{base}}{S_{\mathrm{sc}}}=\frac{100}{2500}=0.04\ \mathrm{pu}.
\]
\[
X_{\mathrm{th}}=0.04+0.12=0.16\ \mathrm{pu},\qquad I_f=\frac{1}{0.16}=6.25\ \mathrm{pu}.
\]

### Answer

\(X_{\mathrm{th}}=0.16\ \mathrm{pu}\); \(I_f=6.25\ \mathrm{pu}\)

## Q6

### Given

Positive-sequence \(Y_\mathrm{bus}\) including generator subtransient shunts (pu, purely imaginary): \(Y_{11}=-j8.0\), \(Y_{12}=Y_{21}=j3.0\), \(Y_{22}=-j6.0\) for a two-bus network. Prefault \(V=1.0\ \mathrm{pu}\) everywhere. Bolted fault at bus 1.

### Find

\(Z_{11}\) and \(I_f\).

### Solution

\[
\det Y=Y_{11}Y_{22}-Y_{12}^2=(-j8)(-j6)-(j3)^2=-48-(-9)=-39.
\]

\((-j8)(-j6)=j^2 48=-48\) and \((j3)^2=j^2 9=-9\). For a \(2\times 2\),

\[
Z_{11}=\frac{Y_{22}}{\det Y}=\frac{-j6}{-39}=j\frac{6}{39}=j0.15385\ \mathrm{pu}.
\]

\[
I_f=\frac{1}{Z_{11}}=-j6.50\ \mathrm{pu}.
\]

### Answer

\(Z_{11}=j0.1538\ \mathrm{pu}\); \(I_f=6.50\ \mathrm{pu}\)
