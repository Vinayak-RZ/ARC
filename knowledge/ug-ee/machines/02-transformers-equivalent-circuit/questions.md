# Questions — Ideal and practical single-phase transformer

Original numbers.

## Q1

### Given

Ideal transformer, \(N_1=1200\) turns, \(N_2=120\) turns. Primary voltage \(v_1=230\sqrt{2}\sin(2\pi 50 t)\ \mathrm{V}\). Load on the secondary is \(Z_L=4+j3\ \Omega\).

### Find

Turns ratio \(a=N_1/N_2\), secondary voltage RMS, secondary current RMS, and primary current RMS.

### Solution

\(a=10\). Primary RMS \(V_1=230\ \mathrm{V}\). Secondary RMS \(V_2=V_1/a=23.0\ \mathrm{V}\).

\[
|Z_L|=\sqrt{4^2+3^2}=5\ \Omega,\qquad I_2=23/5=4.60\ \mathrm{A}.
\]

Ideal current \(I_1=I_2/a=0.460\ \mathrm{A}\). Check: \(Z_\mathrm{in}=a^2 Z_L=100(4+j3)=400+j300\ \Omega\), \(|Z_\mathrm{in}|=500\ \Omega\), \(I_1=230/500=0.460\ \mathrm{A}\).

### Answer

\(a=10\), \(V_2=23.0\ \mathrm{V}\), \(I_2=4.60\ \mathrm{A}\), \(I_1=0.460\ \mathrm{A}\)

## Q2

### Given

A 50 Hz, 230/115 V transformer has core net area \(A_c=25\times 10^{-4}\ \mathrm{m}^2\) and \(N_1=200\) turns on the 230 V winding.

### Find

Peak flux density \(B_\mathrm{max}\) in tesla.

### Solution

No-load Faraday (sinusoidal): \(V_1 \approx 4.44 f N_1 B_\mathrm{max} A_c\).

\[
4.44\times 50\times 200\times 25\times 10^{-4} = 111.0,
\]

\[
B_\mathrm{max} = \frac{230}{111.0} = 2.072\ \mathrm{T}.
\]

That flux density is above a typical 50 Hz silicon-steel knee; the algebra is still Faraday’s law for the given area.

### Answer

\(B_\mathrm{max}=2.07\ \mathrm{T}\)

## Q3

### Given

Single-phase transformer 11 kV / 220 V, 50 kVA. Parameters referred to primary: \(R_\mathrm{eq}=12.0\ \Omega\), \(X_\mathrm{eq}=40.0\ \Omega\). Magnetizing branch neglected. Load is rated 50 kVA at 0.80 lagging PF with secondary voltage held at 220 V.

### Find

Primary voltage magnitude required, and percent regulation \((V_{1,\mathrm{needed}}-V_{1,\mathrm{ideal}})/V_{1,\mathrm{ideal}}\) where \(V_{1,\mathrm{ideal}}=11\ \mathrm{kV}\) (i.e. drop relative to rated primary).

### Solution

\(a=11000/220=50\). Rated primary current \(I_1=50000/11000=4.545\ \mathrm{A}\). Secondary rated current \(I_2=50000/220=227.3\ \mathrm{A}\), and \(I_2'=I_2/a=4.545\ \mathrm{A}\).

\(\mathbf{V}_2'=a\times 220=11000\ \mathrm{V}\). Take \(\mathbf{V}_2'=11000\angle 0^\circ\). Lagging PF 0.8: \(\theta=\cos^{-1}0.8=36.87^\circ\), \(\mathbf{I}_2'=4.545\angle -36.87^\circ\ \mathrm{A}\).

\[
\mathbf{I}Z_\mathrm{eq}=(4.545\angle -36.87^\circ)(12+j40).
\]

\(12+j40=41.76\angle 73.30^\circ\). Product: \(4.545\times 41.76=189.8\ \mathrm{V}\) at angle \(73.30-36.87=36.43^\circ\).

\[
\mathbf{I}Z = 189.8(\cos 36.43^\circ + j\sin 36.43^\circ) = 152.8 + j112.7\ \mathrm{V}.
\]

\[
\mathbf{V}_1 = 11000 + 152.8 + j112.7 = 11152.8 + j112.7,\qquad |V_1|=11153\ \mathrm{V}.
\]

Regulation vs 11 kV: \((11153-11000)/11000=1.39\%\).

Approximate formula: \(\Delta V \approx I(R\cos\theta+X\sin\theta)=4.545(12\times 0.8+40\times 0.6)=4.545(9.6+24)=152.7\ \mathrm{V}\), \(|V_1|\approx 11000+152.7=11153\ \mathrm{V}\) (the quadrature remainder is small).

### Answer

\(|V_1|=11.15\ \mathrm{kV}\), regulation \(1.39\%\)

## Q4

### Given

Same transformer as Q3. Core loss 400 W (constant). Full-load copper loss \(I_{1,\mathrm{rated}}^2 R_\mathrm{eq}=(4.545)^2(12)=248\ \mathrm{W}\). Load 0.80 lagging.

### Find

Efficiency at full load and at half load (half VA, same PF, same voltage).

### Solution

Full load output \(P=50\times 10^3\times 0.8=40\ \mathrm{kW}\). Losses \(400+248=648\ \mathrm{W}\).

\[
\eta_\mathrm{fl} = \frac{40000}{40000+648}=0.9841=98.41\%.
\]

Half load: output 20 kW, copper loss \(0.25\times 248=62\ \mathrm{W}\), core 400 W.

\[
\eta_{1/2} = \frac{20000}{20000+462}=0.9774=97.74\%.
\]

### Answer

\(\eta_\mathrm{fl}=98.4\%\), \(\eta_{1/2}=97.7\%\)

## Q5

### Given

A 230/115 V two-winding transformer rated 5 kVA is reconnected as a step-up autotransformer from 230 V to 345 V (additive: 230 V winding as common, 115 V winding in series).

### Find

Maximum throughput VA in this auto connection, and the inductive (transformed) VA.

### Solution

Winding current ratings: 230 V winding \(I_H=5000/230=21.74\ \mathrm{A}\); 115 V winding \(I_L=5000/115=43.48\ \mathrm{A}\).

Additive 345 V output: series winding is the 115 V winding, current limited to 43.48 A. Common winding (230 V) carries the difference between source and load current.

Throughput \(S=V_\mathrm{high} I_\mathrm{series}=345\times 43.48=15.0\ \mathrm{kVA}\).

(Alternatively \(S_\mathrm{auto}=S_\mathrm{two}\times V_H/(V_H-V_L)=5\times 345/115=15\ \mathrm{kVA}\).)

Inductive VA remains 5 kVA. Conductively transferred: \(15-5=10\ \mathrm{kVA}\).

Check common-winding current: load at 345 V, 43.48 A is 15 kVA; source at 230 V would supply \(15000/230=65.22\ \mathrm{A}\); common winding current \(65.22-43.48=21.74\ \mathrm{A}\), exactly the 230 V winding rating.

### Answer

Throughput \(15.0\ \mathrm{kVA}\); inductive \(5.0\ \mathrm{kVA}\)
