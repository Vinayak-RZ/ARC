# Questions — Feeders, radial vs ring, voltage drop

Original numbers. Balanced three-phase unless a DC distributor is stated.

## Q1

### Given

An 11 kV, 8 km three-phase feeder, \(r=0.22\ \Omega/\mathrm{km}\), \(x=0.38\ \Omega/\mathrm{km}\) per phase. Load at the far end \(4.0\ \mathrm{MW}\) at \(0.85\) lagging pf. Use rated voltage to compute current. Approximate line-to-line drop \(\sqrt{3}I(R\cos\phi+X\sin\phi)\).

### Find

Line current, voltage drop, and percent drop on 11 kV.

### Solution

\[
I=\frac{4.0\times 10^6}{\sqrt{3}\times 11\times 10^3\times 0.85}=247.4\ \mathrm{A}.
\]
\[
R=0.22\times 8=1.76\ \Omega,\qquad X=0.38\times 8=3.04\ \Omega,
\]
\[
\cos\phi=0.85,\quad\sin\phi=0.5268,
\]
\[
\Delta V_{LL}=\sqrt{3}\times 247.4\times(1.76\times 0.85+3.04\times 0.5268)=\sqrt{3}\times 247.4\times 3.097=1326\ \mathrm{V}.
\]
\[
\%\ \mathrm{drop}=\frac{1.326}{11}\times 100=12.05\%.
\]

### Answer

\(I=247.4\ \mathrm{A}\); \(\Delta V=1.326\ \mathrm{kV}\); \(12.05\%\)

## Q2

### Given

A DC two-wire distributor, one-way resistance \(R=0.40\ \Omega\), uniformly distributed load of total \(120\ \mathrm{A}\), fed from one end, \(X=0\).

### Find

Far-end voltage drop and total copper loss in both conductors. (Take the go-and-return resistance as \(2R\) for loss and drop if \(R\) is one-way per conductor; here interpret \(R=0.40\ \Omega\) as the one-way conductor resistance, go-and-return \(0.80\ \Omega\) for concentrated equivalent.)

### Solution

For a two-wire DC line, one-way conductor resistance \(R=0.40\ \Omega\), go-and-return \(R_{\mathrm{loop}}=0.80\ \Omega\). Uniform load, far-end drop \(=I R_{\mathrm{loop}}/2=120\times 0.80/2=48\ \mathrm{V}\).

Copper loss both conductors: each conductor sees the uniform-current profile, loss per conductor \(I^2 R/3\), two conductors:

\[
P_{\mathrm{cu}}=2\times\frac{120^2\times 0.40}{3}=3840\ \mathrm{W}=3.84\ \mathrm{kW}.
\]

Equivalently \(I^2 R_{\mathrm{loop}}/3=14400\times 0.80/3=3840\ \mathrm{W}\).

### Answer

\(48\ \mathrm{V}\); \(3.84\ \mathrm{kW}\)

## Q3

### Given

The same 11 kV feeder as Q1 but the 4.0 MW at 0.85 lag is uniformly distributed along the 8 km instead of concentrated at the end. Approximate drop as half of Q1’s concentrated drop (resistance-and-reactance analog of the \(IR/2\) rule, UG exam style).

### Find

Approximate percent voltage drop.

### Solution

Q1 drop was \(12.05\%\). Uniform-load far-end drop \(\approx 12.05/2=6.03\%\).

(The factor 1/2 is exact for the series impedance times the linearly tapering current when the receiving voltage is used as phase reference for all taps — a standard approximation.)

### Answer

\(6.03\%\)

## Q4

### Given

DC distributor 600 m, resistance \(0.05\ \Omega\) per 100 m per conductor (go-and-return therefore \(0.10\ \Omega\) per 100 m of route). Fed at both ends A and B at \(240\ \mathrm{V}\). A concentrated load \(80\ \mathrm{A}\) at 200 m from A (400 m from B). No other loads.

### Find

Currents from A and from B, and the voltage at the load.

### Solution

Route resistance A to load: \(2\times 0.05\times(200/100)=0.20\ \Omega\). B to load: \(2\times 0.05\times 4=0.40\ \Omega\).

Let \(I_A\) flow from A, \(I_B=80-I_A\) from B. Equal voltages at A and B imply \(I_A\times 0.20=I_B\times 0.40\):

\[
0.20 I_A=0.40(80-I_A),\qquad 0.20 I_A=32-0.40 I_A,\qquad 0.60 I_A=32,\qquad I_A=53.33\ \mathrm{A},
\]
\[
I_B=26.67\ \mathrm{A}.
\]
\[
V_{\mathrm{load}}=240-53.33\times 0.20=229.3\ \mathrm{V}.
\]

Check: \(240-26.67\times 0.40=229.3\ \mathrm{V}\).

### Answer

\(I_A=53.33\ \mathrm{A}\), \(I_B=26.67\ \mathrm{A}\); \(V=229.3\ \mathrm{V}\)

## Q5

### Given

Three-phase feeder current \(180\ \mathrm{A}\), per-phase resistance \(1.10\ \Omega\), load \(2.80\ \mathrm{MW}\).

### Find

Three-phase copper loss and percent loss.

### Solution

\[
P_{\mathrm{loss}}=3 I^2 R=3\times 180^2\times 1.10=106920\ \mathrm{W}=106.9\ \mathrm{kW}.
\]
\[
\%\ \mathrm{loss}=\frac{0.1069}{2.80}\times 100=3.82\%.
\]

### Answer

\(106.9\ \mathrm{kW}\); \(3.82\%\)

## Q6

### Given

Four consumers with peak demands 40, 60, 25, and 55 kW. The coincident peak on the feeder is 140 kW. Average feeder load over a day is 62 kW.

### Find

Diversity factor and load factor.

### Solution

\[
\mathrm{DF}=\frac{40+60+25+55}{140}=\frac{180}{140}=1.286,
\]
\[
\mathrm{LF}=\frac{62}{140}=0.443=44.3\%.
\]

### Answer

\(\mathrm{DF}=1.286\); \(\mathrm{LF}=0.443\)
