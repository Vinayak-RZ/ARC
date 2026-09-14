# Questions — Cables, string efficiency, grounding

Original numbers.

## Q1

### Given

A three-disc suspension string. Each disc capacitance \(C\), pin-to-earth capacitance \(0.20 C\) (so \(K=0.20\)). Tower-end disc voltage \(V_1=8.0\ \mathrm{kV}\).

### Find

Disc voltages \(V_2,V_3\), total string voltage, voltage across the line-end disc, and string efficiency.

### Solution

Using the \(n=3\) ladder:

\[
V_2=V_1(1+K)=8.0(1.20)=9.60\ \mathrm{kV},
\]
\[
V_3=V_1(1+3K+K^2)=8.0(1+0.60+0.04)=8.0\times 1.64=13.12\ \mathrm{kV}.
\]
\[
V_{\mathrm{string}}=8.0+9.60+13.12=30.72\ \mathrm{kV}.
\]
\[
\eta=\frac{30.72}{3\times 13.12}=\frac{30.72}{39.36}=0.7805=78.05\%.
\]

### Answer

\(V_2=9.60\ \mathrm{kV}\), \(V_3=13.12\ \mathrm{kV}\), \(V_{\mathrm{string}}=30.72\ \mathrm{kV}\), \(\eta=78.05\%\)

## Q2

### Given

A 33 kV three-phase screened cable, capacitance to earth \(0.28\ \mu\mathrm{F/km}\) per phase, length \(12\ \mathrm{km}\), \(f=50\ \mathrm{Hz}\), energized at rated line voltage.

### Find

Charging current per phase and three-phase charging Mvar.

### Solution

\[
C=0.28\times 12=3.36\ \mu\mathrm{F},\qquad X_c=\frac{1}{\omega C}=\frac{1}{314.16\times 3.36\times 10^{-6}}=947.4\ \Omega.
\]
\[
V_\phi=\frac{33}{\sqrt{3}}=19.053\ \mathrm{kV},\qquad I_c=\frac{V_\phi}{X_c}=\frac{19.053\times 10^3}{947.4}=20.11\ \mathrm{A}.
\]
\[
Q_{3\phi}=3 V_\phi I_c=3\times 19.053\times 10^3\times 20.11=1.150\times 10^6\ \mathrm{var}=1.150\ \mathrm{Mvar}.
\]

Equivalently \(Q=V_{LL}^2\omega C=33^2\times 314.16\times 3.36\times 10^{-6}=1.150\ \mathrm{Mvar}\).

### Answer

\(I_c=20.11\ \mathrm{A}\); \(Q=1.150\ \mathrm{Mvar}\)

## Q3

### Given

Single-core coaxial geometry: conductor radius \(r=1.2\ \mathrm{cm}\), inner radius of earthed screen \(R=2.8\ \mathrm{cm}\), XLPE \(\varepsilon_r=2.5\). Length \(1.0\ \mathrm{km}\).

### Find

Capacitance per kilometre.

### Solution

\[
C=\frac{2\pi\varepsilon}{\ln(R/r)}=\frac{2\pi\times 2.5\times 8.854\times 10^{-12}}{\ln(2.8/1.2)}=\frac{1.390\times 10^{-10}}{\ln(2.333)}=1.641\times 10^{-10}\ \mathrm{F/m}.
\]
\[
C=0.1641\ \mu\mathrm{F/km}.
\]

### Answer

\(0.164\ \mu\mathrm{F/km}\)

## Q4

### Given

A Petersen coil is to compensate earth-fault charging of an 11 kV cable network. Total per-phase capacitance to ground \(C_0=4.5\ \mu\mathrm{F}\), \(f=50\ \mathrm{Hz}\). Use \(L=1/(3\omega^2 C_0)\) for a coil in the transformer neutral.

### Find

The coil inductance.

### Solution

\[
\omega=314.16\ \mathrm{rad/s},\qquad \omega^2=9.870\times 10^4,
\]
\[
L=\frac{1}{3\times 9.870\times 10^4\times 4.5\times 10^{-6}}=\frac{1}{1.332}=0.751\ \mathrm{H}.
\]

### Answer

\(0.751\ \mathrm{H}\)

## Q5

### Given

Substation ground grid approximated as a circular plate of radius \(r=25\ \mathrm{m}\) on soil \(\rho=80\ \Omega\cdot\mathrm{m}\). Use \(R_g=\rho/(4r)\). A ground fault returns \(I_g=4.0\ \mathrm{kA}\) through the grid (shield-wire diversion already removed).

### Find

Grid resistance and ground potential rise \(I_g R_g\).

### Solution

\[
R_g=\frac{80}{4\times 25}=0.80\ \Omega,\qquad \mathrm{GPR}=4000\times 0.80=3200\ \mathrm{V}.
\]

This GPR is not the mesh touch voltage; it is an upper-scale figure.

### Answer

\(R_g=0.80\ \Omega\); \(\mathrm{GPR}=3.20\ \mathrm{kV}\)

## Q6

### Given

Neutral earthing resistor \(R_n=8.0\ \Omega\) at an 11 kV (line-to-line) transformer star point. Ignore network \(X_0\) besides this resistor (i.e. \(Z_0=3R_n\) in sequence with \(Z_1=Z_2=0\) as a crude bound). Prefault \(V_\phi=11/\sqrt{3}\ \mathrm{kV}\).

### Find

Bolted LG current at the station bus under that bound.

### Solution

Sequence: \(I_0=V_\phi/(Z_1+Z_2+Z_0)=V_\phi/(3R_n)\), \(I_a=3I_0=V_\phi/R_n\).

\[
V_\phi=6351\ \mathrm{V},\qquad I_a=\frac{6351}{8.0}=794\ \mathrm{A}.
\]

The resistor is sized so that LG current is hundreds of amperes, not kiloamperes.

### Answer

\(794\ \mathrm{A}\)
