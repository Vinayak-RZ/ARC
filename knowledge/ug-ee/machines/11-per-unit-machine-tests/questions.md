# Questions — Per-unit machines and standard tests

Original numbers.

## Q1

### Given

A 50 kVA, 11 kV / 400 V, 50 Hz single-phase transformer. SC test on HV: \(V_\mathrm{SC}=480\ \mathrm{V}\), \(I_\mathrm{SC}=4.55\ \mathrm{A}\), \(P_\mathrm{SC}=650\ \mathrm{W}\) (same numbers as the pack’s transformer OC/SC unit).

### Find

\(R_\mathrm{eq}\), \(X_\mathrm{eq}\) in ohms on the HV side, and \(Z,R,X\) in pu on the 50 kVA, 11 kV base.

### Solution

HV base: \(I_b=50000/11000=4.545\ \mathrm{A}\), \(Z_b=11000^2/50000=2420\ \Omega\).

\[
R_\mathrm{eq}=\frac{650}{4.55^2}=31.41\ \Omega,\qquad Z_\mathrm{eq}=480/4.55=105.5\ \Omega,
\]

\[
X_\mathrm{eq}=\sqrt{105.5^2-31.41^2}=100.7\ \Omega.
\]

\[
R_\mathrm{pu}=31.41/2420=0.0130,\qquad X_\mathrm{pu}=100.7/2420=0.0416,\qquad Z_\mathrm{pu}=105.5/2420=0.0436.
\]

Check: \(Z_\mathrm{pu}\approx V_\mathrm{SC}/V_r=480/11000=0.0436\).

### Answer

\(R_\mathrm{eq}=31.4\ \Omega\), \(X_\mathrm{eq}=101\ \Omega\); \(R=0.0130\ \mathrm{pu}\), \(X=0.0416\ \mathrm{pu}\), \(Z=0.0436\ \mathrm{pu}\)

## Q2

### Given

The transformer of Q1 is used on a 100 kVA, 11 kV study base.

### Find

\(Z_\mathrm{pu}\) on the new base.

### Solution

Same voltage, \(S_{b2}/S_{b1}=2\),

\[
Z_{\mathrm{pu,new}}=0.0436\times 2=0.0872\ \mathrm{pu}.
\]

### Answer

\(0.0872\ \mathrm{pu}\) on 100 kVA, 11 kV

## Q3

### Given

400 V, 50 Hz, 7.5 kW, 4-pole, Y-connected IM, rated PF 0.85, rated \(\eta=0.88\). No-load: \(V=400\ \mathrm{V}\), \(I_0=6.0\ \mathrm{A}\), \(P_0=420\ \mathrm{W}\). DC stator resistance 1.20 Ω per phase (use 1.20 Ω as AC \(R_1\)).

### Find

Rated VA and rated current (from kW, PF, \(\eta\)), and an approximate \(X_m\) per phase treating no-load current as magnetizing after removing \(I_c\) from \(P_0-3I_0^2 R_1\).

### Solution

Shaft 7500 W, input \(P_\mathrm{in}=7500/0.88=8523\ \mathrm{W}\). Rated VA \(S=P_\mathrm{in}/\mathrm{pf}=8523/0.85=10027\ \mathrm{VA}\).

\[
I_r=10027/(\sqrt{3}\times 400)=14.47\ \mathrm{A}.
\]

No-load stator Cu \(3 I_0^2 R_1=3(36)(1.20)=129.6\ \mathrm{W}\). Core+rot \(P_\phi=420-129.6=290.4\ \mathrm{W}\).

Per-phase \(V=230.9\ \mathrm{V}\). \(I_c=P_\phi/(3V)=290.4/(3\times 230.9)=0.419\ \mathrm{A}\).

\[
I_m=\sqrt{6.0^2-0.419^2}=5.985\ \mathrm{A},\qquad X_m=230.9/5.985=38.6\ \Omega.
\]

### Answer

\(S_r=10.03\ \mathrm{kVA}\), \(I_r=14.5\ \mathrm{A}\), \(X_m=38.6\ \Omega\)

## Q4

### Given

Blocked-rotor on the motor of Q3: \(V_{L,\mathrm{br}}=90\ \mathrm{V}\), \(I_L=14.5\ \mathrm{A}\), \(P=980\ \mathrm{W}\). \(R_1=1.20\ \Omega\). Split leakage equally.

### Find

\(R_2'\), \(X_1\), \(X_2'\) per phase, and \(Z_\mathrm{br}\) in pu on rated VA and 400 V.

### Solution

\(V_\mathrm{ph}=90/\sqrt{3}=51.96\ \mathrm{V}\), \(I_\mathrm{ph}=14.5\ \mathrm{A}\).

\[
Z_\mathrm{br}=51.96/14.5=3.583\ \Omega,\qquad R_\mathrm{br}=980/(3\times 14.5^2)=1.553\ \Omega,
\]

\[
X_\mathrm{br}=\sqrt{3.583^2-1.553^2}=3.227\ \Omega.
\]

\[
R_2'=1.553-1.20=0.353\ \Omega,\qquad X_1=X_2'=1.614\ \Omega.
\]

\(Z_b=V_L^2/S=400^2/10027=15.96\ \Omega\). \(Z_\mathrm{br,pu}=3.583/15.96=0.224\).

(Blocked impedance 0.22 pu implies starting current about \(1/0.22\approx 4.5\ \mathrm{pu}\) at rated volts if the circuit stayed linear — a modest cage.)

### Answer

\(R_2'=0.353\ \Omega\), \(X_1=X_2'=1.61\ \Omega\), \(Z_\mathrm{br}=0.224\ \mathrm{pu}\)

## Q5

### Given

11 kV, 50 MVA, Y-connected generator. OCC at rated speed: 11 kV line at \(I_f=180\ \mathrm{A}\). SCC: rated current at \(I_f=150\ \mathrm{A}\). \(R_a\) neglected.

### Find

SCR, unsaturated \(X_{s,\mathrm{pu}}\) using air-gap / SCC ratio as \(X_{s,\mathrm{pu}}\approx 1/\mathrm{SCR}\) if the OCC point is on the air-gap line, and \(I_{a,\mathrm{rated}}\).

### Solution

Rated current \(I_b=50\times 10^6/(\sqrt{3}\times 11000)=2624\ \mathrm{A}\).

SCR \(= I_{f,\mathrm{OCC}(V_r)}/I_{f,\mathrm{SCC}(I_r)}=180/150=1.20\).

If that OCC point is unsaturated (air-gap), \(X_{s,\mathrm{pu}}=1/\mathrm{SCR}=0.833\).

(If the OCC is saturated at rated voltage, this \(1/\mathrm{SCR}\) is still the definition-related unsaturated estimate used in UG: SCR is defined from those two field currents, and \(X_{s,\mathrm{unsat}}\approx 1/\mathrm{SCR}\).)

### Answer

SCR \(=1.20\), \(X_{s,\mathrm{pu}}\approx 0.833\), \(I_r=2.62\ \mathrm{kA}\)

## Q6

### Given

Retardation on a DC machine: \(J=25\ \mathrm{kg\cdot m}^2\). At \(n=1000\ \mathrm{r/min}\) the slope is \(\mathrm{d}n/\mathrm{d}t=-40\ \mathrm{r/min/s}\) (free deceleration).

### Find

Rotational loss power at that speed.

### Solution

\(\omega=1000\times 2\pi/60=104.72\ \mathrm{rad/s}\).

\(\mathrm{d}\omega/\mathrm{d}t=-40\times 2\pi/60=-4.189\ \mathrm{rad/s}^2\).

\[
P_\mathrm{rot}=-J\omega\frac{\mathrm{d}\omega}{\mathrm{d}t}=-25\times 104.72\times(-4.189)=10970\ \mathrm{W}.
\]

### Answer

\(P_\mathrm{rot}=11.0\ \mathrm{kW}\)
