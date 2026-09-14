# Questions — Wheatstone, Kelvin, Maxwell, Schering, Wien

Original pedagogical numbers.

## Q1

### Given

Wheatstone arms \( P=1000.0\,\Omega \), \( Q=100.0\,\Omega \), \( R=246.8\,\Omega \) at balance. The unknown is \( S \) in the arm opposite the product sense \( S=RP/Q \).

### Find

\( S \) and, if each of \( P,Q,R \) has 0.05% limiting error, the relative limiting error of \( S \).

### Solution

\( S=246.8\times 1000/100=2468\,\Omega \). Relative limiting error of a product/quotient is the sum of relatives: \( 0.15\% \). Absolute \( \Delta S=3.70\,\Omega \).

### Answer

\( 2468\,\Omega \pm 3.70\,\Omega \) (\( 0.15\% \)).

## Q2

### Given

Kelvin double bridge with matched ratios \( p/q=p'/q'=0.01000 \) and standard \( R_s=0.10000\,\Omega \). The yoke resistance is \( 0.002\,\Omega \) but the ratios are equal.

### Find

\( R_x \).

### Solution

Matched ratios cancel the yoke: \( R_x=R_s p/q=0.0010000\,\Omega \).

### Answer

\( 1.0000\,\mathrm{m}\Omega \).

## Q3

### Given

Maxwell inductance-capacitance bridge: \( R_2=250\,\Omega \), \( R_4=400\,\Omega \), \( C_3=0.400\,\mu\mathrm{F} \), \( R_3=8.00\,\mathrm{k}\Omega \), using \( L_x=R_2 R_4 C_3 \) and \( R_x=R_2 R_4/R_3 \). Frequency 800 Hz.

### Find

\( L_x \), \( R_x \), and \( Q=\omega L_x/R_x \).

### Solution

\( L_x=250\times 400\times 0.400\times 10^{-6}=0.0400 \) H. \( R_x=250\times 400/8000=12.5\,\Omega \). \( \omega=2\pi\times 800=5027 \) rad/s. \( Q=5027\times 0.0400/12.5=16.1 \).

### Answer

\( L_x=40.0 \) mH, \( R_x=12.5\,\Omega \), \( Q=16.1 \).

## Q4

### Given

Schering bridge: \( C_s=50.0 \) pF, \( R_3=2000\,\Omega \), \( R_4=318.3\,\Omega \), \( C_4=1.00 \) nF, \( f=50.0 \) Hz. Labelling \( C_x=C_s R_4/R_3 \), \( D=\omega C_4 R_4 \).

### Find

\( C_x \) and dissipation factor \( D \).

### Solution

\( C_x=50.0\times 318.3/2000=7.958 \) pF. \( D=2\pi\times 50\times 1.00\times 10^{-9}\times 318.3=1.000\times 10^{-4} \).

### Answer

\( C_x=7.96 \) pF; \( D=1.00\times 10^{-4} \).

## Q5

### Given

Equal-component Wien network \( R_1=R_2=5.00\,\mathrm{k}\Omega \), \( C_1=C_2=31.8 \) nF, ratio arm set to \( R_3/R_4=2 \) at balance.

### Find

The balance frequency.

### Solution

\( f=1/(2\pi RC)=1/(2\pi\times 5000\times 31.8\times 10^{-9})=1000 \) Hz.

### Answer

\( 1.00 \) kHz.

## Q6

### Given

Hay-bridge approximation for high Q: \( R_2=1000\,\Omega \), \( R_4=1000\,\Omega \), \( C=400 \) pF, and \( \omega^2 r^2 C^2 \ll 1 \).

### Find

Approximate \( L_x \).

### Solution

\( L_x\approx R_2 R_4 C=1000\times 1000\times 400\times 10^{-12}=0.400 \) mH.

### Answer

\( 0.400 \) mH.
