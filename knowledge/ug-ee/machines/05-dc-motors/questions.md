# Questions — Torque, speed control, starters

Original numbers.

## Q1

### Given

A 220 V shunt motor, \(R_a=0.25\ \Omega\), \(R_f=110\ \Omega\), \(I_L=40\ \mathrm{A}\) at a certain load. Rotational losses 600 W.

### Find

Back emf \(E\), converted power, shaft power, and shaft torque if speed is 1200 r/min.

### Solution

\(I_f=220/110=2.00\ \mathrm{A}\), \(I_a=40-2=38.0\ \mathrm{A}\).

\[
E=V-I_a R_a=220-38\times 0.25=210.5\ \mathrm{V}.
\]

\[
P_\mathrm{conv}=E I_a=210.5\times 38=7999\ \mathrm{W},\qquad P_\mathrm{sh}=7999-600=7399\ \mathrm{W}.
\]

\[
\omega=1200\times 2\pi/60=125.66\ \mathrm{rad/s},\qquad T=P_\mathrm{sh}/\omega=7399/125.66=58.88\ \mathrm{N\cdot m}.
\]

### Answer

\(E=210.5\ \mathrm{V}\), \(P_\mathrm{conv}=8.00\ \mathrm{kW}\), \(P_\mathrm{sh}=7.40\ \mathrm{kW}\), \(T=58.9\ \mathrm{N\cdot m}\)

## Q2

### Given

The motor of Q1 at standstill, no starter, field fully excited.

### Find

Starting armature current if the armature were thrown directly on 220 V.

### Solution

\(E=0\), \(I_a=V/R_a=220/0.25=880\ \mathrm{A}\), about 23 times the 38 A running value in Q1.

### Answer

\(I_{a,\mathrm{st}}=880\ \mathrm{A}\)

## Q3

### Given

220 V series motor, \(R_a+R_\mathrm{se}=0.50\ \Omega\). At 40 A it runs at 800 r/min. Assume unsaturated \(\phi\propto I_a\) and neglect armature reaction.

### Find

Speed at 25 A, same terminal voltage, load whatever produces that current.

### Solution

At 40 A: \(E_1=220-40\times 0.50=200\ \mathrm{V}\). At 25 A: \(E_2=220-25\times 0.50=207.5\ \mathrm{V}\).

\[
\frac{E}{\phi N}=\mathrm{const},\qquad \frac{\phi_2}{\phi_1}=\frac{25}{40}=0.625.
\]

\[
\frac{E_2}{E_1}=\frac{\phi_2 N_2}{\phi_1 N_1}\implies N_2=N_1\frac{E_2}{E_1}\frac{\phi_1}{\phi_2}=800\times\frac{207.5}{200}\times\frac{1}{0.625}=1328\ \mathrm{r/min}.
\]

### Answer

\(N=1330\ \mathrm{r/min}\)

## Q4

### Given

Shunt motor, 220 V, \(R_a=0.20\ \Omega\), rated \(I_a=50\ \mathrm{A}\), rated speed 1000 r/min at full field. Field weakening to \(\phi'=0.80\phi\) with the same \(I_a=50\ \mathrm{A}\) and same \(V\).

### Find

New speed and the ratio of available torque to rated torque (constant \(\phi\) rated).

### Solution

Rated: \(E=220-50\times 0.20=210\ \mathrm{V}\), \(E=k\phi\omega\) so \(k\phi \propto 210/1000\).

New: \(E'=220-50\times 0.20=210\ \mathrm{V}\) still (same \(I_a R_a\)).

\[
\frac{E'}{E}=\frac{\phi'\ n'}{\phi\ n}\implies n'=1000\times\frac{210}{210}\times\frac{\phi}{\phi'}=1250\ \mathrm{r/min}.
\]

Torque \(T\propto \phi I_a\): \(T'/T=0.80\).

### Answer

\(n=1250\ \mathrm{r/min}\), \(T'/T=0.80\)

## Q5

### Given

220 V shunt motor, \(R_a=0.30\ \Omega\), rated \(I_a=40\ \mathrm{A}\). A starter must limit the first-notch current to 80 A. Four-point starter, field already on the supply.

### Find

External starter resistance on the first notch, and the back emf at which that resistance may be cut out if the current is allowed to fall to 40 A before the next notch (still with the first-notch resistance in).

### Solution

First notch, \(E=0\): \(R_\mathrm{st}+R_a=V/I_1=220/80=2.75\ \Omega\), so \(R_\mathrm{st}=2.75-0.30=2.45\ \Omega\).

With that resistance still in, current 40 A:

\[
E=V-I(R_a+R_\mathrm{st})=220-40\times 2.75=110\ \mathrm{V}.
\]

### Answer

\(R_\mathrm{st}=2.45\ \Omega\), \(E=110\ \mathrm{V}\) at 40 A on the first notch
