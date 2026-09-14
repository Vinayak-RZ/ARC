# Questions — Generated emf, types, characteristics

Original numbers.

## Q1

### Given

A 4-pole lap-wound DC generator, 600 conductors, flux 0.024 Wb/pole, speed 1200 r/min.

### Find

Generated emf \(E\).

### Solution

Lap winding: \(A=P=4\).

\[
E = \frac{\Phi Z N P}{60 A} = \frac{0.024\times 600\times 1200\times 4}{60\times 4} = \frac{0.024\times 600\times 1200}{60} = 288\ \mathrm{V}.
\]

### Answer

\(E=288\ \mathrm{V}\)

## Q2

### Given

The machine of Q1 runs as a shunt generator. \(R_a=0.18\ \Omega\), \(R_f=180\ \Omega\), brush drop neglected. Terminal voltage 270 V.

### Find

Load current \(I_L\) and output power.

### Solution

\(I_f=270/180=1.50\ \mathrm{A}\). Generator KVL: \(E=V+I_a R_a\), so \(288=270+I_a(0.18)\), \(I_a=18/0.18=100\ \mathrm{A}\).

\[
I_L=I_a-I_f=98.5\ \mathrm{A},\qquad P=V I_L=270\times 98.5=26.60\ \mathrm{kW}.
\]

### Answer

\(I_L=98.5\ \mathrm{A}\), \(P=26.6\ \mathrm{kW}\)

## Q3

### Given

Separately excited DC generator. OCC at 1000 r/min: \(E_0=120\ \mathrm{V}\) at \(I_f=1.2\ \mathrm{A}\) (unsaturated, residual neglected). Field resistance not involved. Speed 1200 r/min, same \(I_f\). \(R_a=0.40\ \Omega\), \(I_a=40\ \mathrm{A}\), no armature reaction.

### Find

Terminal voltage \(V\).

### Solution

Scale OCC with speed: \(E=120\times(1200/1000)=144\ \mathrm{V}\).

\[
V=E-I_a R_a=144-40\times 0.40=128\ \mathrm{V}.
\]

### Answer

\(V=128\ \mathrm{V}\)

## Q4

### Given

A shunt generator fails to build up. Field-circuit resistance \(R_f=220\ \Omega\). Air-gap line of the OCC at the running speed is \(E=180 I_f\) with \(E\) in volts and \(I_f\) in amperes. Residual voltage 5 V.

### Find

The critical field-circuit resistance and whether build-up occurs at \(R_f=220\ \Omega\).

### Solution

The air-gap line slope is \(E/I_f=180\ \mathrm{V/A}\), so \(R_\mathrm{crit}=180\ \Omega\).

The field-resistance line is \(E=220 I_f\), steeper than the air-gap line. The only intersection with the OCC family in the linear region is at the origin. Residual 5 V does not create a stable high-voltage operating point when \(R_f>R_\mathrm{crit}\). Build-up does not occur.

### Answer

\(R_\mathrm{crit}=180\ \Omega\); no build-up

## Q5

### Given

Cumulative compound generator, long shunt. \(R_a=0.12\ \Omega\), \(R_\mathrm{se}=0.04\ \Omega\), \(R_f=100\ \Omega\). \(I_L=80\ \mathrm{A}\), \(V=240\ \mathrm{V}\). Generated \(E\) includes series-field flux already.

### Find

Armature current and generated emf \(E\).

### Solution

Long shunt: shunt field across the combination of armature and series field, so \(I_f=V/R_f=240/100=2.40\ \mathrm{A}\).

\[
I_a=I_L+I_f=82.4\ \mathrm{A}.
\]

\[
E=V+I_a R_a+I_a R_\mathrm{se}=240+82.4(0.12+0.04)=240+13.18=253.2\ \mathrm{V}.
\]

### Answer

\(I_a=82.4\ \mathrm{A}\), \(E=253\ \mathrm{V}\)
