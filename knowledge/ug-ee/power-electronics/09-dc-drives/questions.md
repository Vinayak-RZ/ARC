# Worked questions — DC drives

## Q1
### Given
A separately excited DC motor, \(K\phi=1.8\,\mathrm{V\cdot s/rad}\), \(R_a=0.45\,\Omega\), is fed from a three-phase fully controlled rectifier, \(V_{LL}=415\,\mathrm{V}\), \(\alpha=25^\circ\), continuous \(I_a=40\,\mathrm{A}\). Overlap drop \(3\omega L_s I_a/\pi=6\,\mathrm{V}\).
### Find
Armature terminal voltage, back-emf, and speed in rad/s and r/min.
### Solution
\(V_t=1.3505\times 415\times\cos 25^\circ-6=507.7-6=501.7\,\mathrm{V}\). \(E_a=501.7-40\times 0.45=483.7\,\mathrm{V}\). \(\omega=483.7/1.8=268.7\,\mathrm{rad/s}=2566\,\mathrm{r/min}\).
### Answer
\(V_t=502\,\mathrm{V}\), \(E_a=484\,\mathrm{V}\), \(\omega=269\,\mathrm{rad/s}\) (\(2566\,\mathrm{r/min}\))

## Q2
### Given
Buck chopper DC drive, \(V_{bus}=180\,\mathrm{V}\), \(E_a=110\,\mathrm{V}\), \(R_a=0.50\,\Omega\), \(I_a=30\,\mathrm{A}\) motoring, CCM.
### Find
Duty ratio \(D\) and armature terminal voltage \(V_t\).
### Solution
\(V_t=110+30\times 0.50=125\,\mathrm{V}\). \(D=125/180=0.694\).
### Answer
\(V_t=125\,\mathrm{V}\), \(D=0.694\)

## Q3
### Given
The motor of Q2 at the same speed (\(E_a=110\,\mathrm{V}\)) must regenerate 30 A into the 180 V bus using a second-quadrant (boost) chopper. Ideal CCM, \(V_{bus}=E_a/(1-D)\).
### Find
Duty \(D\) of the boost switch (the switch that shorts the armature through the chopper inductor).
### Solution
\(1-D=E_a/V_{bus}=110/180=0.611\), \(D=0.389\). (Armature current is reversed relative to motoring; the bus absorbs \(P\approx 180\times 30\times\eta\).)
### Answer
\(D=0.389\)

## Q4
### Given
Starting: \(E_a=0\), \(V_t=220\,\mathrm{V}\), \(R_a=0.30\,\Omega\), rated \(I_a=80\,\mathrm{A}\).
### Find
Unprotected start current and the extra series resistance needed to hold \(I_a=80\,\mathrm{A}\) at start.
### Solution
Naked \(I=220/0.30=733\,\mathrm{A}\). Need \(R_{\mathrm{tot}}=220/80=2.75\,\Omega\), so \(R_{\mathrm{extra}}=2.45\,\Omega\).
### Answer
\(733\,\mathrm{A}\) unprotected; \(R_{\mathrm{st}}=2.45\,\Omega\)

## Q5
### Given
Dynamic braking: \(E_a=160\,\mathrm{V}\), \(R_a=0.40\,\Omega\), brake resistor \(R_b=1.60\,\Omega\), \(K\phi=2.0\,\mathrm{V\cdot s/rad}\).
### Find
Braking current, electromagnetic torque, and mechanical power dumped.
### Solution
\(I_a=160/(0.40+1.60)=80.0\,\mathrm{A}\). \(T=2.0\times 80=160\,\mathrm{N\cdot m}\). \(P_{\mathrm{mech}}=E_a I_a=12.8\,\mathrm{kW}\).
### Answer
\(I_a=80.0\,\mathrm{A}\), \(T=160\,\mathrm{N\cdot m}\), \(P=12.8\,\mathrm{kW}\)

## Q6
### Given
Field weakening: rated \(V_t=400\,\mathrm{V}\), rated \(\phi\) such that \(K\phi=3.0\,\mathrm{V\cdot s/rad}\), \(I_a=20\,\mathrm{A}\), \(R_a=0.50\,\Omega\). Flux reduced to 0.70 of rated, \(V_t\) still 400 V.
### Find
Speed at rated flux and at 0.70 flux (same \(I_a\)).
### Solution
Rated: \(E_a=400-10=390\,\mathrm{V}\), \(\omega=390/3.0=130\,\mathrm{rad/s}\). Weakened: \(K\phi=2.1\), \(\omega=390/2.1=185.7\,\mathrm{rad/s}\).
### Answer
\(130\,\mathrm{rad/s}\) rated flux; \(186\,\mathrm{rad/s}\) at \(0.70\phi\)
