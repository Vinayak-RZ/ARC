# Questions — Gaseous/liquid/solid breakdown, HV testing

Original numbers.

## Q1

### Given

Uniform air gap, relative density \(\delta=0.95\), gap \(d=1.20\,\mathrm{cm}\). Use \(V_b=24.2\,\delta d+6.08\sqrt{\delta d}\) kV (peak).

### Find

Breakdown voltage.

### Solution

\[
\delta d=1.14,\qquad \sqrt{\delta d}=1.068,\qquad V_b=24.2\times 1.14+6.08\times 1.068=27.59+6.49=34.08\,\mathrm{kV}.
\]

### Answer

\(34.1\,\mathrm{kV}\) peak

## Q2

### Given

Cockcroft–Walton, \(n=8\) stages, transformer peak \(V_m=50\,\mathrm{kV}\), no-load. Then load current \(I=4.0\,\mathrm{mA}\), \(f=50\,\mathrm{Hz}\), stage \(C=0.050\,\mu\mathrm{F}\). Ripple \(\delta V=I n(n+1)/(2 f C)\).

### Find

No-load DC voltage and peak-to-peak ripple under load.

### Solution

\[
V_{\mathrm{DC}}=2\times 8\times 50=800\,\mathrm{kV}.
\]
\[
\delta V=\frac{4.0\times 10^{-3}\times 8\times 9}{2\times 50\times 0.050\times 10^{-6}}=\frac{0.288}{5.0\times 10^{-6}}=57.6\,\mathrm{kV}.
\]

### Answer

\(800\,\mathrm{kV}\) no-load; ripple \(57.6\,\mathrm{kV}\)

## Q3

### Given

Marx generator, 10 stages, each charged to \(V_0=95\,\mathrm{kV}\). Wave-shaping delivers 88% of the ideal series voltage to the test object.

### Find

Peak lightning-impulse voltage at the object.

### Solution

\[
V=0.88\times 10\times 95=836\,\mathrm{kV}.
\]

### Answer

\(836\,\mathrm{kV}\)

## Q4

### Given

Capacitive divider \(C_1=50\,\mathrm{pF}\) (HV arm), \(C_2=100\,\mathrm{nF}\) (LV arm). Peak HV \(800\,\mathrm{kV}\).

### Find

LV arm peak voltage.

### Solution

\[
V_{\mathrm{low}}=800\times\frac{50\times 10^{-12}}{50\times 10^{-12}+100\times 10^{-9}}=800\times\frac{50}{100050}=0.400\,\mathrm{kV}=400\,\mathrm{V}.
\]

### Answer

\(400\,\mathrm{V}\) peak

## Q5

### Given

Schering bridge at \(50\,\mathrm{Hz}\): \(C_s=100\,\mathrm{pF}\), \(R_3=200\,\Omega\), \(R_4=318\,\Omega\), \(C_4=0.50\,\mu\mathrm{F}\). Balance \(C_x=C_s R_4/R_3\), \(\tan\delta=\omega C_4 R_4\).

### Find

Specimen \(C_x\) and \(\tan\delta\).

### Solution

\[
C_x=100\times\frac{318}{200}=159\,\mathrm{pF},
\]
\[
\omega=314.16,\qquad\tan\delta=314.16\times 0.50\times 10^{-6}\times 318=0.0499.
\]

### Answer

\(C_x=159\,\mathrm{pF}\), \(\tan\delta=0.0499\)

## Q6

### Given

Peek corona onset, overhead wire \(r=1.00\,\mathrm{cm}\), \(\delta=1.00\), surface factor \(m=0.85\). \(E_c=m\delta(30+9/\sqrt{\delta r})\) kVpeak/cm.

### Find

Onset gradient.

### Solution

\[
\sqrt{\delta r}=1.00,\qquad E_c=0.85\times 1.00\times(30+9)=0.85\times 39=33.15\,\mathrm{kV_{peak}/cm}.
\]

### Answer

\(33.2\,\mathrm{kV_{peak}/cm}\)
