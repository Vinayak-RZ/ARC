# Questions — OC/SC, regulation, three-phase connections

Original numbers. Q1–Q2 are transformer open-circuit and short-circuit numericals.

## Q1

### Given

A 50 kVA, 11 kV / 400 V, 50 Hz single-phase transformer. Open-circuit test on the LV side: \(V_\mathrm{OC}=400\ \mathrm{V}\), \(I_\mathrm{OC}=5.50\ \mathrm{A}\), \(P_\mathrm{OC}=420\ \mathrm{W}\).

### Find

Shunt parameters \(R_c\) and \(X_m\) referred to the LV side, and the no-load power factor.

### Solution

\[
R_c = \frac{V_\mathrm{OC}^2}{P_\mathrm{OC}} = \frac{400^2}{420} = 381.0\ \Omega.
\]

\[
\cos\phi_0 = \frac{P_\mathrm{OC}}{V_\mathrm{OC} I_\mathrm{OC}} = \frac{420}{400\times 5.50} = 0.1909\ \text{(leading from the source view: magnetizing lag, so current lags; pf lagging)}.
\]

No-load pf = 0.191 lagging.

\[
I_c = \frac{P_\mathrm{OC}}{V_\mathrm{OC}} = \frac{420}{400} = 1.050\ \mathrm{A},\qquad I_m = \sqrt{5.50^2-1.050^2} = 5.399\ \mathrm{A}.
\]

\[
X_m = \frac{V_\mathrm{OC}}{I_m} = \frac{400}{5.399} = 74.09\ \Omega.
\]

Check: \(Q=\sqrt{(400\times 5.50)^2-420^2}=\sqrt{2200^2-420^2}=2159.6\ \mathrm{VAR}\), \(X_m=V^2/Q=160000/2159.6=74.09\ \Omega\).

### Answer

\(R_c=381\ \Omega\), \(X_m=74.1\ \Omega\) (LV), \(\mathrm{pf}_0=0.191\) lag

## Q2

### Given

Same transformer as Q1. Short-circuit test on the HV side: \(V_\mathrm{SC}=480\ \mathrm{V}\), \(I_\mathrm{SC}=4.55\ \mathrm{A}\) (approximately rated HV current), \(P_\mathrm{SC}=650\ \mathrm{W}\).

### Find

\(R_\mathrm{eq}\), \(X_\mathrm{eq}\), and \(Z_{\%}\) referred to the HV side. Rated HV current is \(50000/11000=4.545\ \mathrm{A}\).

### Solution

\[
R_\mathrm{eq,H} = \frac{P_\mathrm{SC}}{I_\mathrm{SC}^2} = \frac{650}{4.55^2} = 31.41\ \Omega.
\]

\[
Z_\mathrm{eq,H} = \frac{V_\mathrm{SC}}{I_\mathrm{SC}} = \frac{480}{4.55} = 105.5\ \Omega.
\]

\[
X_\mathrm{eq,H} = \sqrt{105.5^2-31.41^2} = 100.7\ \Omega.
\]

Percent impedance at this current:

\[
Z_{\%} = \frac{480}{11000}\times 100 = 4.36\%.
\]

(Using exact rated 4.545 A would scale \(Z\) slightly; the measured \(I_\mathrm{SC}\) is already rated to three figures.)

### Answer

\(R_\mathrm{eq}=31.4\ \Omega\), \(X_\mathrm{eq}=101\ \Omega\) (HV), \(Z_{\%}=4.36\%\)

## Q3

### Given

The transformer of Q1–Q2 supplies rated 50 kVA at 0.80 lagging PF, secondary voltage 400 V. Use HV \(Z_\mathrm{eq}\) from Q2. Neglect the magnetizing branch for regulation.

### Find

Voltage regulation and full-load efficiency.

### Solution

Rated HV current \(I=4.545\ \mathrm{A}\). Approximate drop at lagging 0.8:

\[
\Delta V = I(R\cos\theta+X\sin\theta)=4.545(31.41\times 0.8+100.7\times 0.6)
\]

\[
=4.545(25.13+60.42)=4.545\times 85.55=388.8\ \mathrm{V}.
\]

\[
\mathrm{reg}=\frac{388.8}{11000}=0.0353=3.53\%.
\]

Full-load output \(P=50\times 10^3\times 0.8=40\ \mathrm{kW}\). Losses \(P_\mathrm{OC}+P_\mathrm{SC}=420+650=1070\ \mathrm{W}\).

\[
\eta=\frac{40000}{41070}=0.9739=97.4\%.
\]

### Answer

Regulation \(3.53\%\), \(\eta=97.4\%\)

## Q4

### Given

Three identical 11 kV / 415 V, 100 kVA single-phase transformers are connected as a three-phase Δ–Y bank (HV delta, LV wye). A balanced three-phase load takes 250 kW at 0.85 lagging PF at 415 V line-to-line.

### Find

The HV line voltage (ideal transformers), the HV line current, and the load current in each LV winding (wye phase current).

### Solution

LV line 415 V wye: phase voltage \(415/\sqrt{3}=239.6\ \mathrm{V}\). Turns ratio per phase \(a=V_{H\mathrm{ph}}/V_{L\mathrm{ph}}\). HV is delta, so HV phase voltage = HV line voltage. For the ideal 11 kV / 415 V nameplate as line-to-line on both sides of the bank: HV line = 11 kV, LV line = 415 V.

HV phase voltage (delta) = 11 kV. LV phase voltage (wye) = 239.6 V. Phase turns ratio \(N_H/N_L=11000/239.6=45.91\).

Three-phase load current (LV line, also LV phase in wye):

\[
S = \frac{250}{0.85}=294.1\ \mathrm{kVA},\qquad I_{L,\mathrm{LV}}=\frac{294.1\times 10^3}{\sqrt{3}\times 415}=409.0\ \mathrm{A}.
\]

Each LV winding current is 409 A.

Ideal per-phase VA: \(294.1/3=98.04\ \mathrm{kVA}\) per transformer (within 100 kVA). HV winding (delta) current \(I_{H\mathrm{ph}}=98040/11000=8.913\ \mathrm{A}\). HV line current \(I_{L,\mathrm{HV}}=\sqrt{3}\times 8.913=15.44\ \mathrm{A}\).

HV line voltage remains 11 kV in the ideal model.

### Answer

\(V_{L,\mathrm{HV}}=11\ \mathrm{kV}\), \(I_{L,\mathrm{HV}}=15.4\ \mathrm{A}\), \(I_{L\mathrm{winding}}=409\ \mathrm{A}\)

## Q5

### Given

Two identical single-phase transformers, each 50 kVA, are connected open-delta (V–V) on a 400 V three-phase bus.

### Find

The maximum balanced three-phase load VA the bank can supply without exceeding either transformer rating, and that load as a fraction of a closed-delta bank of three such units.

### Solution

Each unit can carry 50 kVA (its winding rating). Open-delta three-phase throughput:

\[
S_\mathrm{V}=\sqrt{3}\times 50=86.60\ \mathrm{kVA}.
\]

Three-unit closed delta: 150 kVA. Fraction \(86.60/150=0.577=1/\sqrt{3}\).

Not \(2/3\times 150=100\ \mathrm{kVA}\).

### Answer

\(86.6\ \mathrm{kVA}\) (\(57.7\%\) of a 150 kVA closed-delta bank)

## Q6

### Given

OC and SC results of Q1–Q2. Load fraction \(x\) at unity PF.

### Find

Load fraction \(x^*\) at which efficiency is maximum (unity PF), and that maximum efficiency.

### Solution

Maximum \(\eta\) when copper loss equals core loss: \(x^2 P_\mathrm{SC}=P_\mathrm{OC}\).

\[
x^*=\sqrt{420/650}=0.8039.
\]

Output at that point, unity PF: \(x^* S_r=0.8039\times 50=40.19\ \mathrm{kW}\). Losses \(2\times 420=840\ \mathrm{W}\).

\[
\eta_\mathrm{max}=\frac{40190}{40190+840}=0.9795=98.0\%.
\]

### Answer

\(x^*=0.804\), \(\eta_\mathrm{max}=98.0\%\) (unity PF)
