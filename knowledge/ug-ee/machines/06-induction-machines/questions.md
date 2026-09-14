# Questions — Equivalent circuit, torque-slip

Original numbers. Per-phase quantities unless noted. Y-connected machines.

## Q1

### Given

A 4-pole, 50 Hz, three-phase induction motor runs at 1440 r/min.

### Find

Synchronous speed, slip, and rotor frequency.

### Solution

\[
n_s=120\times 50/4=1500\ \mathrm{r/min},\qquad s=(1500-1440)/1500=0.040,
\]

\[
f_2=s f=2.00\ \mathrm{Hz}.
\]

### Answer

\(n_s=1500\ \mathrm{r/min}\), \(s=0.040\), \(f_2=2.00\ \mathrm{Hz}\)

## Q2

### Given

The motor of Q1 has air-gap power \(P_g=12.0\ \mathrm{kW}\) at that slip. Rotational losses 400 W.

### Find

Rotor copper loss, converted power, shaft power, and electromagnetic torque.

### Solution

\[
P_\mathrm{cu2}=s P_g=0.040\times 12000=480\ \mathrm{W},\qquad P_\mathrm{mech}=(1-s)P_g=11520\ \mathrm{W}.
\]

\[
P_\mathrm{sh}=11520-400=11120\ \mathrm{W}.
\]

\[
\omega_s=2\pi\times 1500/60=157.08\ \mathrm{rad/s},\qquad T=P_g/\omega_s=12000/157.08=76.39\ \mathrm{N\cdot m}.
\]

### Answer

\(P_\mathrm{cu2}=480\ \mathrm{W}\), \(P_\mathrm{mech}=11.52\ \mathrm{kW}\), \(P_\mathrm{sh}=11.12\ \mathrm{kW}\), \(T=76.4\ \mathrm{N\cdot m}\)

## Q3

### Given

400 V, 50 Hz, 4-pole, Y-connected, three-phase IM. Per-phase: \(R_1=0.40\ \Omega\), \(R_2'=0.50\ \Omega\), \(X_1=X_2'=1.20\ \Omega\). Magnetizing branch neglected. Slip 0.05.

### Find

Per-phase current \(I_2'\), input power (three-phase), and electromagnetic torque. Stator copper is included in the input.

### Solution

Phase voltage \(V=400/\sqrt{3}=230.9\ \mathrm{V}\).

\[
Z=R_1+R_2'/s+j(X_1+X_2')=0.40+0.50/0.05+j2.40=10.40+j2.40\ \Omega,
\]

\[
|Z|=10.67\ \Omega,\qquad I_2'=230.9/10.67=21.64\ \mathrm{A}.
\]

\[
P_\mathrm{in}=3 I^2 (R_1+R_2'/s)=3(21.64)^2(10.40)=14610\ \mathrm{W}.
\]

\[
P_g=3 I^2 (R_2'/s)=3(21.64)^2(10.0)=14050\ \mathrm{W},
\]

\[
T=P_g/\omega_s=14050/157.08=89.44\ \mathrm{N\cdot m}.
\]

### Answer

\(I_2'=21.6\ \mathrm{A}\), \(P_\mathrm{in}=14.6\ \mathrm{kW}\), \(T=89.4\ \mathrm{N\cdot m}\)

## Q4

### Given

Parameters of Q3. Approximate breakdown using \(s_m=R_2'/\sqrt{R_1^2+(X_1+X_2')^2}\).

### Find

Breakdown slip and maximum electromagnetic torque.

### Solution

\[
s_m=\frac{0.50}{\sqrt{0.40^2+2.40^2}}=\frac{0.50}{2.433}=0.2055.
\]

At \(s_m\):

\[
R_2'/s_m=0.50/0.2055=2.433\ \Omega,
\]

\[
Z=0.40+2.433+j2.40=2.833+j2.40,\quad |Z|=3.713\ \Omega,
\]

\[
I=230.9/3.713=62.19\ \mathrm{A},\qquad P_g=3(62.19)^2(2.433)=28230\ \mathrm{W},
\]

\[
T_\mathrm{max}=28230/157.08=179.7\ \mathrm{N\cdot m}.
\]

Closed form (approx.): \(T_\mathrm{max}=\frac{3}{2\omega_s}\frac{V^2}{R_1+\sqrt{R_1^2+X^2}}=\frac{3}{2\times 157.08}\frac{230.9^2}{0.40+2.433}=179.7\ \mathrm{N\cdot m}\).

### Answer

\(s_m=0.206\), \(T_\mathrm{max}=180\ \mathrm{N\cdot m}\)

## Q5

### Given

A wound-rotor motor has \(R_2'=0.40\ \Omega\) and \(X=X_1+X_2'=2.00\ \Omega\). \(R_1\) neglected for a starting-torque estimate. Rated \(V_\mathrm{ph}=230\ \mathrm{V}\), \(\omega_s=157.1\ \mathrm{rad/s}\).

### Find

External referred resistance \(R_\mathrm{ext}'\) to be added to the rotor to maximize starting torque, and that starting torque.

### Solution

Maximum torque at start needs \(s_m=1\), i.e. \(R_2'+R_\mathrm{ext}'=X=2.00\ \Omega\) when \(R_1=0\). So \(R_\mathrm{ext}'=1.60\ \Omega\).

Then \(T_\mathrm{st}=T_\mathrm{max}=\frac{3}{2\omega_s}\frac{V^2}{X}=\frac{3}{2\times 157.1}\frac{230^2}{2.00}=253.0\ \mathrm{N\cdot m}\).

Without extra \(R\), \(s=1\): \(T=\frac{3}{\omega_s}\frac{V^2 R_2'}{R_2'^2+X^2}=\frac{3}{157.1}\frac{230^2\times 0.40}{0.16+4}=87.3\ \mathrm{N\cdot m}\).

### Answer

\(R_\mathrm{ext}'=1.60\ \Omega\), \(T_\mathrm{st,max}=253\ \mathrm{N\cdot m}\)
