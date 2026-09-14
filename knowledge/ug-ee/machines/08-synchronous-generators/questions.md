# Questions — Pitch, winding factor, OCC/SCC, regulation

Original numbers.

## Q1

### Given

A 3-phase, 4-pole, 50 Hz alternator. Stator: 36 slots, double-layer, 8 conductors per slot, coil pitch 8 slots. Flux per pole 0.045 Wb (fundamental). Y-connected.

### Find

\(k_p\), \(k_d\), \(k_w\), phase EMF, and line EMF.

### Solution

Slots/pole \(=36/4=9\). Slot angle \(\alpha=180^\circ/9=20^\circ\) electrical. Slots/pole/phase \(n=9/3=3\).

Coil pitch 8 slots: \(\gamma=8\times 20^\circ=160^\circ\).

\[
k_p=\sin(160^\circ/2)=\sin 80^\circ=0.9848.
\]

\[
k_d=\frac{\sin(3\times 20^\circ/2)}{3\sin(10^\circ)}=\frac{\sin 30^\circ}{3\sin 10^\circ}=\frac{0.5}{3\times 0.1736}=0.9598.
\]

\[
k_w=0.9848\times 0.9598=0.9452.
\]

Conductors total \(Z=36\times 8=288\). Turns/phase \(N_\mathrm{ph}=Z/(2\times 3)=48\).

\[
E_\mathrm{ph}=4.44 k_w f N_\mathrm{ph}\Phi=4.44\times 0.9452\times 50\times 48\times 0.045=453.0\ \mathrm{V}.
\]

\[
E_L=\sqrt{3}\times 453.0=784.6\ \mathrm{V}.
\]

### Answer

\(k_w=0.945\), \(E_\mathrm{ph}=453\ \mathrm{V}\), \(E_L=785\ \mathrm{V}\)

## Q2

### Given

OCC at rated speed: \(E_\mathrm{ph}=400\ \mathrm{V}\) (line 693 V if Y) at \(I_f=4.0\ \mathrm{A}\) on the air-gap line? Use: at \(I_f=5.0\ \mathrm{A}\), OCC gives \(E_\mathrm{ph}=280\ \mathrm{V}\) and SCC gives \(I_\mathrm{sc}=40\ \mathrm{A}\). \(R_a=0.20\ \Omega\) per phase.

### Find

Synchronous impedance and reactance per phase at this field current.

### Solution

\[
Z_s=\frac{280}{40}=7.00\ \Omega,\qquad X_s=\sqrt{7.00^2-0.20^2}=6.997\approx 7.00\ \Omega.
\]

\(R_a\) is negligible in \(Z_s\) here.

### Answer

\(Z_s=7.00\ \Omega\), \(X_s=7.00\ \Omega\)

## Q3

### Given

Cylindrical-rotor generator, \(V_\phi=240\ \mathrm{V}\), \(R_a=0.25\ \Omega\), \(X_s=6.0\ \Omega\), \(I_a=20\ \mathrm{A}\) at 0.80 lagging PF, stand-alone.

### Find

\(|E_a|\) and voltage regulation by the EMF method, \(\mathrm{reg}=(|E_a|-V)/V\).

### Solution

\(\mathbf{V}=240\angle 0^\circ\), \(\mathbf{I}=20\angle -36.87^\circ=16-j12\ \mathrm{A}\).

\[
\mathbf{I}R_a=5-j3\ \mathrm{V},\qquad jX_s\mathbf{I}=j6(16-j12)=72+j96\ \mathrm{V}.
\]

\[
\mathbf{E}_a=240+5-j3+72+j96=317+j93,\qquad |E_a|=330.4\ \mathrm{V}.
\]

\[
\mathrm{reg}=(330.4-240)/240=0.3765=37.7\%.
\]

Approximate: \(IR\cos\theta+IX\sin\theta=20(0.25\times 0.8+6\times 0.6)=20(0.2+3.6)=76\ \mathrm{V}\), \(|E|\approx 240+76=316\ \mathrm{V}\) (underestimates the quadrature remainder).

### Answer

\(|E_a|=330\ \mathrm{V}\), \(\mathrm{reg}=37.7\%\)

## Q4

### Given

The same machine as Q3, same \(I_a=20\ \mathrm{A}\), 0.80 leading PF.

### Find

\(|E_a|\) and regulation.

### Solution

\(\mathbf{I}=20\angle +36.87^\circ=16+j12\ \mathrm{A}\).

\[
\mathbf{I}R=4+j3,\qquad jX\mathbf{I}=j6(16+j12)=-72+j96.
\]

\[
\mathbf{E}_a=240+4+j3-72+j96=172+j99,\qquad |E_a|=198.5\ \mathrm{V}.
\]

\[
\mathrm{reg}=(198.5-240)/240=-0.173=-17.3\%.
\]

Leading load, negative regulation: no-load voltage would be lower than the loaded 240 V if \(E_a\) were held (stand-alone interpretation: excitation was raised under load).

### Answer

\(|E_a|=198\ \mathrm{V}\), \(\mathrm{reg}=-17.3\%\)

## Q5

### Given

Y-connected 11 kV, 50 MVA, 50 Hz generator. Unsaturated \(X_s=1.25\ \mathrm{pu}\). \(R_a\) neglected. Infinite bus 11 kV. Delivers 40 MW at unity PF.

### Find

\(E_a\) in pu and kV line-to-line, and the load angle \(\delta\).

### Solution

\(S_b=50\ \mathrm{MVA}\), \(P=40/50=0.80\ \mathrm{pu}\). Unity PF: \(Q=0\), \(S=0.80\ \mathrm{pu}\), \(I=0.80\ \mathrm{pu}\) in phase with \(V=1\angle 0^\circ\).

\[
E_a\angle\delta = V + j X_s I = 1 + j 1.25\times 0.80 = 1 + j 1.00.
\]

\[
|E_a|=\sqrt{2}=1.414\ \mathrm{pu},\qquad \delta=\tan^{-1}(1/1)=45.0^\circ.
\]

Line voltage corresponding to \(|E_a|\): \(1.414\times 11=15.56\ \mathrm{kV}\).

Check: \(P=V E_a\sin\delta / X_s = 1\times 1.414\times \sin 45^\circ / 1.25=1.414\times 0.7071/1.25=0.800\ \mathrm{pu}\).

### Answer

\(|E_a|=1.41\ \mathrm{pu}\) (\(15.6\ \mathrm{kV}\) line), \(\delta=45^\circ\)
