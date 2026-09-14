# Questions — PV I–V, wind Cp, DG

Original numbers.

## Q1

### Given

PV module \(V_{oc}=36.0\,\mathrm{V}\), \(I_{sc}=8.50\,\mathrm{A}\), \(\mathrm{FF}=0.760\) at STC. Irradiance \(G=700\,\mathrm{W/m}^2\). Scale \(I_{sc}\propto G\), hold \(V_{oc}\) and FF.

### Find

\(I_{sc}\) and \(P_{\max}\) at 700 W/m².

### Solution

\[
I_{sc}=8.50\times 0.700=5.95\,\mathrm{A},\qquad P_{\max}=0.760\times 36.0\times 5.95=163\,\mathrm{W}.
\]

### Answer

\(I_{sc}=5.95\,\mathrm{A}\), \(P_{\max}=163\,\mathrm{W}\)

## Q2

### Given

Array: 18 modules in series, 4 strings in parallel. Each module \(V_{mp}=30.0\,\mathrm{V}\), \(I_{mp}=7.80\,\mathrm{A}\) (identical, uniform sun).

### Find

Array MPP voltage, current, and power.

### Solution

\[
V=18\times 30.0=540\,\mathrm{V},\qquad I=4\times 7.80=31.2\,\mathrm{A},\qquad P=16.8\,\mathrm{kW}.
\]

### Answer

\(540\,\mathrm{V}\), \(31.2\,\mathrm{A}\), \(16.8\,\mathrm{kW}\)

## Q3

### Given

Wind turbine radius \(R=35.0\,\mathrm{m}\), \(v=12.0\,\mathrm{m/s}\), \(\rho=1.225\,\mathrm{kg/m}^3\), \(C_p=0.420\).

### Find

Air power and mechanical shaft power. Also Betz-limit power at this \(v\).

### Solution

\[
A=\pi\times 35^2=3848\,\mathrm{m}^2,\qquad\tfrac12\rho A v^3=0.5\times 1.225\times 3848\times 1728=4.072\times 10^{6}\,\mathrm{W},
\]
\[
P=0.420\times 4.072=1.71\,\mathrm{MW},\qquad P_{\mathrm{Betz}}=(16/27)\times 4.072=2.41\,\mathrm{MW}.
\]

### Answer

\(P_{\mathrm{air}}=4.07\,\mathrm{MW}\), \(P=1.71\,\mathrm{MW}\), \(P_{\mathrm{Betz}}=2.41\,\mathrm{MW}\)

## Q4

### Given

Rotor 18 r/min, \(R=35.0\,\mathrm{m}\), \(v=12.0\,\mathrm{m/s}\). \(\lambda=\omega R/v\).

### Find

Tip-speed ratio.

### Solution

\[
\omega=18\times\frac{2\pi}{60}=1.885\,\mathrm{rad/s},\qquad\lambda=\frac{1.885\times 35}{12}=5.50.
\]

### Answer

\(\lambda=5.50\)

## Q5

### Given

Turbine rated \(2.50\,\mathrm{MW}\). Annual energy \(7.20\,\mathrm{GWh}\).

### Find

Capacity factor.

### Solution

\[
\mathrm{CF}=\frac{7.20\times 10^{6}\,\mathrm{kWh}}{2500\,\mathrm{kW}\times 8760\,\mathrm{h}}=\frac{7.20\times 10^{6}}{2.190\times 10^{7}}=0.329.
\]

### Answer

\(0.329\) (\(32.9\%\))

## Q6

### Given

Simple feeder \(R=1.20\,\Omega\), \(X=1.60\,\Omega\), \(V=11.0\,\mathrm{kV}\) line-to-line (use \(V_{\phi}=11/\sqrt{3}=6.35\,\mathrm{kV}\) in \(\Delta V\approx (RP+XQ)/V_{\phi}\) per-phase with per-phase \(P/3\)). Export \(P=1.50\,\mathrm{MW}\), \(Q=0\) at the DG bus, no local load. Per-phase \(P=0.50\,\mathrm{MW}\).

### Find

Approximate phase-to-neutral voltage rise.

### Solution

\[
\Delta V=\frac{1.20\times 0.50\times 10^{6}+1.60\times 0}{6350}=94.5\,\mathrm{V}.
\]

### Answer

\(94.5\,\mathrm{V}\) (about \(1.5\%\) of \(V_{\phi}\))
