# Worked questions — cycloconverters and dual converters

## Q1
### Given
A three-phase dual converter in circulating-current mode, \(V_{LL}=400\,\mathrm{V}\), so \(V_{do}=1.35\times 400=540\,\mathrm{V}\). Desired DC voltage \(V_t=+220\,\mathrm{V}\).
### Find
Firing angles \(\alpha_P\) and \(\alpha_N\).
### Solution
\(\cos\alpha_P=220/540=0.4074\), \(\alpha_P=66.0^\circ\). \(\alpha_N=180-66.0=114.0^\circ\). Check: \(\cos 114^\circ=-0.407\), \(V_N=540\times(-0.407)=-220\,\mathrm{V}\), means match in magnitude with opposite bridge polarity as drawn.
### Answer
\(\alpha_P=66.0^\circ\), \(\alpha_N=114^\circ\)

## Q2
### Given
Cycloconverter modulation \(m=0.75\), \(V_{do}=250\,\mathrm{V}\). At an instant \(\omega_o t=90^\circ\).
### Find
The required \(\alpha\) of the active group and the instantaneous mean output voltage.
### Solution
\(\cos\alpha=m\sin 90^\circ=0.75\), \(\alpha=41.4^\circ\). \(v=250\times 0.75=188\,\mathrm{V}\).
### Answer
\(\alpha=41.4^\circ\), \(v=188\,\mathrm{V}\)

## Q3
### Given
50 Hz supply, cycloconverter rule \(f_o\le f_i/3\).
### Find
Maximum \(f_o\) and the output period.
### Solution
\(f_o\le 16.67\,\mathrm{Hz}\). \(T_o\ge 60\,\mathrm{ms}\).
### Answer
\(f_o\le 16.7\,\mathrm{Hz}\), \(T_o\ge 60\,\mathrm{ms}\)

## Q4
### Given
Non-circulating dual converter feeding \(R_a=0.60\,\Omega\), \(E_a=+80\,\mathrm{V}\) (forward rotation). Bridge P is live with \(\alpha_P=50^\circ\), \(V_{do}=200\,\mathrm{V}\). Continuous current.
### Find
\(V_t\), \(I_a\), and the quadrant.
### Solution
\(V_t=200\cos 50^\circ=128.6\,\mathrm{V}\). \(I_a=(128.6-80)/0.60=81.0\,\mathrm{A}\). Both \(V\) and \(I\) positive: Q1 motoring.
### Answer
\(V_t=129\,\mathrm{V}\), \(I_a=81.0\,\mathrm{A}\), Q1

## Q5
### Given
Circulating-current dual converter, \(V_{do}=200\,\mathrm{V}\), \(E_a=+80\,\mathrm{V}\), \(R_a=0.60\,\Omega\), regenerative current \(I_a=-40\,\mathrm{A}\) (Q2). Means still match via \(\alpha_N=180^\circ-\alpha_P\).
### Find
Required \(V_t\), \(\alpha_P\), and \(\alpha_N\).
### Solution
\(V_t=E_a+I_a R_a=80+(-40)(0.60)=56.0\,\mathrm{V}\). \(\cos\alpha_P=56/200=0.280\), \(\alpha_P=73.7^\circ\). \(\alpha_N=180-73.7=106.3^\circ\). Both bridges remain gated; load current is negative while \(V_t\) stays positive (regeneration).
### Answer
\(V_t=56.0\,\mathrm{V}\), \(\alpha_P=73.7^\circ\), \(\alpha_N=106.3^\circ\)

## Q6
### Given
A circulating dual converter has a reactor \(L=40\,\mathrm{mH}\). Approximate the voltage difference as a square of amplitude 30 V and period 3.33 ms (six-pulse ripple at 50 Hz, 300 Hz). Treat \(v_L=30\,\mathrm{V}\) for half of that period.
### Find
Peak-to-peak circulating current swing \(\Delta i=v\Delta t/L\).
### Solution
Half-period \(1.667\,\mathrm{ms}\). \(\Delta i=30\times 1.667\times 10^{-3}/0.040=1.25\,\mathrm{A}\) peak-to-peak.
### Answer
\(\Delta i=1.25\,\mathrm{A}\) pp
