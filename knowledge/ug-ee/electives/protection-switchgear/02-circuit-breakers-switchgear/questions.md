# Questions — Arc interruption, CB types, GIS intro

Original numbers.

## Q1

### Given

A 145 kV breaker, three-phase bolted fault current \(31.5\,\mathrm{kA}\) RMS AC. Use the IEC-style making factor \(2.5\).

### Find

Rated making current the breaker must meet, and the legacy three-phase short-circuit MVA at 145 kV.

### Solution

\[
i_{\mathrm{make}}=2.5\times 31.5=78.75\,\mathrm{kA\ peak},
\]
\[
S_{\mathrm{sc}}=\sqrt{3}\times 145\,\mathrm{kV}\times 31.5\,\mathrm{kA}=7912\,\mathrm{MVA}.
\]

### Answer

\(78.8\,\mathrm{kA}\) peak making; \(7.91\,\mathrm{GVA}\)

## Q2

### Given

Current chopping \(i_{\mathrm{ch}}=5.0\,\mathrm{A}\), load inductance \(L=0.25\,\mathrm{H}\), stray capacitance \(C=10\,\mathrm{nF}\). Undamped chopping overvoltage \(V_{\mathrm{ch}}=i_{\mathrm{ch}}\sqrt{L/C}\).

### Find

Chopping overvoltage.

### Solution

\[
\frac{L}{C}=\frac{0.25}{10\times 10^{-9}}=2.50\times 10^{7},\qquad\sqrt{L/C}=5.00\times 10^{3},
\]
\[
V_{\mathrm{ch}}=5.0\times 5.00\times 10^{3}=25.0\,\mathrm{kV}.
\]

### Answer

\(25.0\,\mathrm{kV}\)

## Q3

### Given

Simple TRV: equivalent \(L=8.0\,\mathrm{mH}\), \(C=12.0\,\mathrm{nF}\), TRV peak envelope \(V_p=1.5\times (145\sqrt{2}/\sqrt{3})=178\,\mathrm{kV}\) (use \(V_p=178\,\mathrm{kV}\) as given). \(v=V_p(1-\cos\omega_0 t)\) with \(\omega_0=1/\sqrt{LC}\).

### Find

Natural frequency \(f_0\) and the initial RRRV approximated as \(V_p\omega_0\) (peak slope of \(V_p\sin\omega_0 t\) at \(t=0^+\) is \(V_p\omega_0\)).

### Solution

\[
LC=8.0\times 10^{-3}\times 12.0\times 10^{-9}=9.60\times 10^{-11},\qquad \omega_0=1/\sqrt{LC}=1.021\times 10^{5}\,\mathrm{rad/s},
\]
\[
f_0=\omega_0/(2\pi)=16.2\,\mathrm{kHz},\qquad\mathrm{RRRV}=178\times 10^{3}\times 1.021\times 10^{5}=1.82\times 10^{10}\,\mathrm{V/s}=18.2\,\mathrm{kV/\mu s}.
\]

### Answer

\(f_0=16.2\,\mathrm{kHz}\), \(\mathrm{RRRV}=18.2\,\mathrm{kV/\mu s}\)

## Q4

### Given

Thevenin \(X/R=14\) at 50 Hz. Fault AC RMS \(I_{\mathrm{ac}}=20.0\,\mathrm{kA}\). Contact separation at \(t=45\,\mathrm{ms}\) after fault inception. DC offset at \(t=0\) is fully offset, \(I_{\mathrm{dc}}(0)=I_{\mathrm{ac}}\sqrt{2}\). Time constant \(\tau=L/R=(X/R)/\omega\).

### Find

DC component at contact separation and the asymmetrical RMS breaking current \(\sqrt{I_{\mathrm{ac}}^2+I_{\mathrm{dc}}^2}\).

### Solution

\[
\omega=2\pi\times 50=314.16\,\mathrm{rad/s},\qquad\tau=14/314.16=0.0446\,\mathrm{s},
\]
\[
I_{\mathrm{dc}}(0.045)=20.0\sqrt{2}\,e^{-0.045/0.0446}=28.28\,e^{-1.009}=10.31\,\mathrm{kA},
\]
\[
I_{\mathrm{asym}}=\sqrt{20.0^2+10.31^2}=22.50\,\mathrm{kA}.
\]

### Answer

\(I_{\mathrm{dc}}=10.3\,\mathrm{kA}\), \(I_{\mathrm{asym}}=22.5\,\mathrm{kA}\)

## Q5

### Given

A 33 kV indoor board, prospective fault \(25\,\mathrm{kA}\), continuous load \(800\,\mathrm{A}\). Choose among: (A) 12 kV vacuum 25 kA 630 A; (B) 36 kV vacuum 25 kA 1250 A; (C) 36 kV vacuum 16 kA 1250 A; (D) isolator 36 kV 1250 A.

### Find

Which device is an acceptable circuit breaker for this board, and why the others fail.

### Solution

Voltage must be \(\ge 33\,\mathrm{kV}\) (36 kV class). Breaking \(\ge 25\,\mathrm{kA}\). Normal current \(\ge 800\,\mathrm{A}\). (A) is 12 kV. (C) is only 16 kA. (D) is not a breaker. (B) meets 36 kV, 25 kA, 1250 A.

### Answer

(B) 36 kV vacuum, 25 kA, 1250 A

## Q6

### Given

Breaker-and-a-half diameter: breakers A (bus 1), B (tie), C (bus 2). Line 1 between A and B, line 2 between B and C. Fault on line 1.

### Find

Which breakers must open to isolate line 1, and whether line 2 can stay in service.

### Solution

Line 1 is isolated by opening A and B. Breaker C stays closed; line 2 remains connected to bus 2. Bus 1 and bus 2 stay tied through C only after B opens, so the diameter is split: line 2 still has bus 2 (and, if C is closed, not bus 1). Line 2 remains in service.

### Answer

Open A and B; line 2 stays in service via C
