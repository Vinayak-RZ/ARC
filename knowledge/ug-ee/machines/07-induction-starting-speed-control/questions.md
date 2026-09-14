# Questions — Starting, cascade, V/f intro

Original numbers.

## Q1

### Given

A 415 V, 50 Hz, three-phase cage motor. DOL starting line current 360 A, DOL starting torque 180 N·m. Star-delta starter.

### Find

Line current and starting torque during the star run-up.

### Solution

\[
I_{\mathrm{st,Y}}=\frac{1}{3}\times 360=120\ \mathrm{A},\qquad T_{\mathrm{st,Y}}=\frac{1}{3}\times 180=60\ \mathrm{N\cdot m}.
\]

Phase voltage in star is \(415/\sqrt{3}\) versus 415 V in delta, ratio \(1/\sqrt{3}\). Torque \(\propto V^2\) gives 1/3. Line current in star equals phase current, which is \(1/\sqrt{3}\) of DOL phase current; DOL line current was \(\sqrt{3}\) times DOL phase, so the line-current ratio is 1/3.

### Answer

\(I_\mathrm{st}=120\ \mathrm{A}\), \(T_\mathrm{st}=60\ \mathrm{N\cdot m}\)

## Q2

### Given

Same DOL numbers as Q1. Autotransformer tap 70% (\(x=0.70\)).

### Find

Motor current, line current, and starting torque during autotransformer start (neglect magnetizing of the autotransformer).

### Solution

\[
I_\mathrm{motor}=0.70\times 360=252\ \mathrm{A},\qquad I_\mathrm{line}=(0.70)^2\times 360=176.4\ \mathrm{A},
\]

\[
T_\mathrm{st}=(0.70)^2\times 180=88.2\ \mathrm{N\cdot m}.
\]

### Answer

\(I_\mathrm{motor}=252\ \mathrm{A}\), \(I_\mathrm{line}=176\ \mathrm{A}\), \(T_\mathrm{st}=88.2\ \mathrm{N\cdot m}\)

## Q3

### Given

Wound-rotor motor, Thevenin per phase \(V_\mathrm{Th}=210\ \mathrm{V}\), \(R_\mathrm{Th}=0.35\ \Omega\), \(X_\mathrm{Th}+X_2'=1.80\ \Omega\), \(R_2'=0.30\ \Omega\), \(\omega_s=157.1\ \mathrm{rad/s}\).

### Find

External referred resistance for maximum starting torque, and \(T_\mathrm{st}\) with that resistance.

### Solution

Need \(s_m=1\): \(R_2'+R_\mathrm{ext}'=\sqrt{R_\mathrm{Th}^2+(X_\mathrm{Th}+X_2')^2}=\sqrt{0.35^2+1.80^2}=1.834\ \Omega\).

\[
R_\mathrm{ext}'=1.834-0.30=1.534\ \Omega.
\]

At \(s=1\) with that total \(R_2\):

\[
T=\frac{3}{\omega_s}\frac{V_\mathrm{Th}^2 R}{(R_\mathrm{Th}+R)^2+(X)^2}=\frac{3}{157.1}\frac{210^2\times 1.834}{(0.35+1.834)^2+1.80^2}.
\]

Denominator: \(2.184^2+1.80^2=4.770+3.240=8.010\). Numerator: \(44100\times 1.834=80880\).

\[
T=\frac{3}{157.1}\times\frac{80880}{8.010}=192.7\ \mathrm{N\cdot m}.
\]

### Answer

\(R_\mathrm{ext}'=1.53\ \Omega\), \(T_\mathrm{st}=193\ \mathrm{N\cdot m}\)

## Q4

### Given

Two slip-ring motors, 6-pole and 4-pole, 50 Hz, shafts rigidly coupled, cumulative cascade, small slip.

### Find

Approximate no-load cascade speed.

### Solution

\[
n_{s,\mathrm{cas}}=\frac{120\times 50}{6+4}=600\ \mathrm{r/min}.
\]

### Answer

\(600\ \mathrm{r/min}\)

## Q5

### Given

A 4-pole IM, rated 400 V, 50 Hz. Constant V/f (no boost) to 25 Hz. Approximate circuit at 50 Hz: \(R_1=0.50\ \Omega\), \(R_2'=0.40\ \Omega\), \(X_1+X_2'=2.00\ \Omega\) at 50 Hz. Magnetizing neglected. Mechanical speed 720 r/min at 25 Hz.

### Find

Phase current and electromagnetic torque. Line 400 V at 50 Hz corresponds to phase \(230.9\ \mathrm{V}\) Y; at 25 Hz, \(V_\mathrm{ph}=115.5\ \mathrm{V}\). \(\omega_s(25\ \mathrm{Hz})=78.54\ \mathrm{rad/s}\).

### Solution

Reactance at 25 Hz: \(X=1.00\ \Omega\). \(n_s=120\times 25/4=750\ \mathrm{r/min}\). Slip \(s=(750-720)/750=0.040\).

\[
Z=0.50+0.40/0.040+j1.00=10.50+j1.00,\quad |Z|=10.55\ \Omega,
\]

\[
I=115.5/10.55=10.95\ \mathrm{A}.
\]

\[
P_g=3 I^2 (R_2'/s)=3(10.95)^2(10.0)=3597\ \mathrm{W},\qquad T=P_g/\omega_s=3597/78.54=45.80\ \mathrm{N\cdot m}.
\]

### Answer

\(I=11.0\ \mathrm{A}\), \(T=45.8\ \mathrm{N\cdot m}\)
