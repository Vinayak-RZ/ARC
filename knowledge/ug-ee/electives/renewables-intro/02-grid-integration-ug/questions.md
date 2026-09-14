# Questions — Inverter interface, islanding intro

Original numbers.

## Q1

### Given

Three-phase inverter at \(415\,\mathrm{V}\) line-to-line, current \(80.0\,\mathrm{A}\) (line RMS), \(\cos\phi=0.920\) exporting (lagging current, \(Q>0\) into the grid). \(P=\sqrt{3} V I\cos\phi\), \(Q=\sqrt{3} V I\sin\phi\).

### Find

\(P\), \(Q\), and \(S\).

### Solution

\[
S=\sqrt{3}\times 415\times 80.0=57.50\,\mathrm{kVA},
\]
\[
P=57.50\times 0.920=52.90\,\mathrm{kW},\qquad\sin\phi=\sqrt{1-0.920^2}=0.3919,\qquad Q=22.54\,\mathrm{kvar}.
\]

### Answer

\(P=52.9\,\mathrm{kW}\), \(Q=22.5\,\mathrm{kvar}\), \(S=57.5\,\mathrm{kVA}\)

## Q2

### Given

Inverter \(S_{\mathrm{rated}}=50.0\,\mathrm{kVA}\). MPPT offers \(42.0\,\mathrm{kW}\).

### Find

Maximum \(|Q|\) that still respects the apparent-power disk.

### Solution

\[
|Q|\le\sqrt{50.0^2-42.0^2}=\sqrt{736}=27.1\,\mathrm{kvar}.
\]

### Answer

\(27.1\,\mathrm{kvar}\)

## Q3

### Given

Grid-following inverter rated \(I=60\,\mathrm{A}\) RMS. During a sag, current limit \(1.20\times\) rated.

### Find

Maximum RMS current the inverter will contribute to a nearby fault (UG current-limited model).

### Solution

\[
I_{\mathrm{fault}}=1.20\times 60=72.0\,\mathrm{A}.
\]

### Answer

\(72.0\,\mathrm{A}\)

## Q4

### Given

PV inverter 30.0 kW at unity pf. Local island load 30.0 kW + 1.5 kvar inductive. Passive 27/59/81 only.

### Find

\(\Delta P\), \(\Delta Q\), and whether a matched-power non-detection zone is a concern.

### Solution

\[
\Delta P=30.0-30.0=0,\qquad\Delta Q=0-1.5=-1.5\,\mathrm{kvar}.
\]

Power is matched; reactive mismatch is small. Voltage and frequency may remain inside 27/59/81 windows: NDZ concern. Active islanding or transfer trip is required for a reliable cease-to-energize.

### Answer

\(\Delta P=0\), \(\Delta Q=-1.5\,\mathrm{kvar}\); yes, NDZ concern

## Q5

### Given

Current harmonics at the PCC: \(I_1=40.0\,\mathrm{A}\), \(I_5=2.40\,\mathrm{A}\), \(I_7=1.60\,\mathrm{A}\), other harmonics negligible.

### Find

\(I_{\mathrm{THD}}\).

### Solution

\[
I_{\mathrm{THD}}=\frac{\sqrt{2.40^2+1.60^2}}{40.0}=\frac{\sqrt{5.76+2.56}}{40.0}=\frac{2.887}{40.0}=0.0722\quad(7.22\%).
\]

### Answer

\(7.22\%\)

## Q6

### Given

Grid-forming droop \(m_p=0.4\,\mathrm{Hz/MW}\), \(P_0=0\), \(f_0=50.00\,\mathrm{Hz}\). Island load \(P=1.25\,\mathrm{MW}\). \(\omega=2\pi f\), but report frequency: \(f=f_0-m_p P\).

### Find

Steady island frequency.

### Solution

\[
f=50.00-0.4\times 1.25=49.50\,\mathrm{Hz}.
\]

### Answer

\(49.50\,\mathrm{Hz}\)
