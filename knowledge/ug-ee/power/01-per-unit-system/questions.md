# Questions — Base change, single-line diagrams

Original numbers. Three-phase bases use line-to-line kV and three-phase MVA unless a problem states otherwise.

## Q1

### Given

A study base of \(100\ \mathrm{MVA}\) and \(132\ \mathrm{kV}\) (line-to-line). A feeder has series impedance \(4+j20\ \Omega\).

### Find

The per-unit series impedance on the study base.

### Solution

Impedance base:

\[
Z_\mathrm{base}=\frac{(132)^2}{100}=\frac{17424}{100}=174.24\ \Omega.
\]

Per-unit impedance:

\[
Z_\mathrm{pu}=\frac{4+j20}{174.24}=0.02296+j0.1148\ \mathrm{pu}.
\]

Rounded to four decimals on the imaginary part as usual for UG work: \(0.0230+j0.1148\ \mathrm{pu}\).

### Answer

\(0.0230+j0.1148\ \mathrm{pu}\)

## Q2

### Given

A transformer is nameplated \(40\ \mathrm{MVA}\), \(132/33\ \mathrm{kV}\), \(Z=8\%\). The system base is \(100\ \mathrm{MVA}\) with voltage bases \(132\ \mathrm{kV}\) and \(33\ \mathrm{kV}\) on the two sides (rated ratio).

### Find

Transformer leakage in per-unit on the system base.

### Solution

On nameplate, \(Z=0.08\ \mathrm{pu}\). Voltage bases match the ratings, so the \((V_\mathrm{old}/V_\mathrm{new})^2\) factor is 1. Change of MVA base:

\[
Z_\mathrm{pu,sys}=0.08\times\frac{100}{40}=0.20\ \mathrm{pu}.
\]

### Answer

\(0.20\ \mathrm{pu}\)

## Q3

### Given

A synchronous machine: \(50\ \mathrm{MVA}\), \(11\ \mathrm{kV}\), \(X''=0.18\ \mathrm{pu}\) on nameplate. System bases: \(100\ \mathrm{MVA}\) and \(11\ \mathrm{kV}\) at the machine terminals.

### Find

\(X''\) on the system base, and the corresponding ohmic reactance.

### Solution

Change of MVA base, voltage base unchanged:

\[
X''_\mathrm{sys}=0.18\times\frac{100}{50}=0.36\ \mathrm{pu}.
\]

Ohmic base at \(11\ \mathrm{kV}\), \(100\ \mathrm{MVA}\):

\[
Z_\mathrm{base}=\frac{11^2}{100}=1.21\ \Omega,\qquad X''_\Omega=0.36\times 1.21=0.4356\ \Omega.
\]

The same ohms follow from nameplate: \(Z_{\mathrm{base,name}}=11^2/50=2.42\ \Omega\), \(X''=0.18\times 2.42=0.4356\ \Omega\).

### Answer

\(0.36\ \mathrm{pu}\), \(0.4356\ \Omega\)

## Q4

### Given

A three-phase load absorbs \(36\ \mathrm{MW}\) at \(0.90\) lagging power factor from a \(33\ \mathrm{kV}\) bus. System base: \(100\ \mathrm{MVA}\), \(33\ \mathrm{kV}\) at that bus.

### Find

The load in per-unit as \(P+jQ\), and the line current in amperes if the bus voltage is \(1.02\ \mathrm{pu}\).

### Solution

Apparent power:

\[
S=\frac{36}{0.90}=40\ \mathrm{MVA},\qquad Q=S\sin\theta=40\sqrt{1-0.90^2}=17.436\ \mathrm{Mvar}.
\]

On \(100\ \mathrm{MVA}\):

\[
S_\mathrm{pu}=\frac{36+j17.436}{100}=0.36+j0.1744\ \mathrm{pu}.
\]

Actual bus voltage: \(V=1.02\times 33=33.66\ \mathrm{kV}\). Line current from three-phase power:

\[
I_L=\frac{S}{\sqrt{3}V}=\frac{40\times 10^6}{\sqrt{3}\times 33.66\times 10^3}=685.7\ \mathrm{A}.
\]

(Load \(S\) is specified as \(40\ \mathrm{MVA}\) at the given pf; using \(|S|=40\ \mathrm{MVA}\) with the actual voltage is the consistent “constant power” current at that operating voltage.)

### Answer

\(0.36+j0.1744\ \mathrm{pu}\); \(I_L=685.7\ \mathrm{A}\)

## Q5

### Given

Zones: generator \(13.8\ \mathrm{kV}\), then a \(13.8/69\ \mathrm{kV}\) transformer, then a line, then a \(69/13.8\ \mathrm{kV}\) transformer to a load bus. System \(S_\mathrm{base}=80\ \mathrm{MVA}\). Voltage base at the generator is chosen as \(13.8\ \mathrm{kV}\). Both transformers are rated at the voltages named.

### Find

Voltage bases in the three zones (generator, line, load) and \(Z_\mathrm{base}\) of the \(69\ \mathrm{kV}\) line zone.

### Solution

Generator zone: \(V_\mathrm{base}=13.8\ \mathrm{kV}\) as chosen. First transformer ratio \(13.8/69\), so line-zone base:

\[
V_{\mathrm{base,line}}=13.8\times\frac{69}{13.8}=69\ \mathrm{kV}.
\]

Second transformer \(69/13.8\), so load-zone base:

\[
V_{\mathrm{base,load}}=69\times\frac{13.8}{69}=13.8\ \mathrm{kV}.
\]

Line-zone impedance base:

\[
Z_\mathrm{base,line}=\frac{69^2}{80}=\frac{4761}{80}=59.5125\ \Omega.
\]

### Answer

\(13.8\ \mathrm{kV}\), \(69\ \mathrm{kV}\), \(13.8\ \mathrm{kV}\); \(Z_\mathrm{base}=59.51\ \Omega\)

## Q6

### Given

Prefault voltage \(1.0\ \mathrm{pu}\) at a bus. Positive-sequence Thevenin reactance to the bus on \(100\ \mathrm{MVA}\) is \(j0.25\ \mathrm{pu}\) (resistances neglected). Bolted three-phase fault at the bus.

### Find

Fault current in pu and in kA if the bus voltage base is \(33\ \mathrm{kV}\).

### Solution

\[
I_f=\frac{1.0}{j0.25}=-j4.0\ \mathrm{pu}.
\]

Base current:

\[
I_\mathrm{base}=\frac{100}{\sqrt{3}\times 33}=1.7493\ \mathrm{kA},\qquad |I_f|=4.0\times 1.7493=6.997\ \mathrm{kA}.
\]

### Answer

\(4.0\ \mathrm{pu}\) (\(6.997\ \mathrm{kA}\) rms line)
