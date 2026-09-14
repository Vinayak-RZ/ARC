# Questions — Gross/systematic/random, limiting error

Original pedagogical numbers.

## Q1

### Given

Two resistors \( R_1 = 120.0\,\Omega \) with limiting error \( 0.4\% \) and \( R_2 = 180.0\,\Omega \) with limiting error \( 0.6\% \) are connected in series.

### Find

The series equivalent and its absolute and relative limiting errors.

### Solution

\( R = R_1+R_2 = 300.0\,\Omega \). Absolute limiting errors: \( \Delta R_1 = 0.004\times 120 = 0.48\,\Omega \), \( \Delta R_2 = 0.006\times 180 = 1.08\,\Omega \). For a sum, absolute errors add: \( \Delta R = 1.56\,\Omega \). Relative: \( 1.56/300 = 0.0052 = 0.52\% \).

### Answer

\( 300.0\,\Omega \pm 1.56\,\Omega \) (\( 0.52\% \)).

## Q2

### Given

A moving-coil voltmeter is 0–150 V, class index 0.5. It reads 120.0 V.

### Find

Absolute limiting error and relative limiting error of this reading.

### Solution

Limiting error is \( 0.5\% \) of FSD: \( \Delta V = 0.005\times 150 = 0.75 \) V. Relative to the reading: \( 0.75/120 = 0.00625 = 0.625\% \).

### Answer

\( 0.75 \) V; \( 0.625\% \) of reading.

## Q3

### Given

Power \( P=VI \) with \( V=200.0 \) V, limiting error \( 0.8 \) V, and \( I=4.00 \) A, limiting error \( 0.05 \) A.

### Find

\( P \) and its relative limiting error.

### Solution

\( P = 800 \) W. \( \Delta P/P = \Delta V/V+\Delta I/I = 0.8/200 + 0.05/4 = 0.004 + 0.0125 = 0.0165 = 1.65\% \). \( \Delta P = 13.2 \) W.

### Answer

\( 800 \) W \( \pm 13.2 \) W (\( 1.65\% \)).

## Q4

### Given

Five independent current readings (A): \( 2.12,\ 2.09,\ 2.15,\ 2.11,\ 2.13 \).

### Find

Sample mean, sample standard deviation \( s \), and the standard uncertainty of the mean \( s/\sqrt{n} \).

### Solution

Sum \( = 10.60 \), \( \bar I = 2.120 \) A. Deviations: \( 0.000,\ -0.030,\ +0.030,\ -0.010,\ +0.010 \). Sum of squares \( = 0.00200 \). \( s = \sqrt{0.00200/4} = \sqrt{5\times 10^{-4}} = 0.02236 \) A. \( u_A = s/\sqrt{5} = 0.0100 \) A.

### Answer

Mean \( 2.120 \) A; \( s=0.0224 \) A; \( u_A=0.0100 \) A.

## Q5

### Given

A node with Thevenin equivalent \( 12.00 \) V in series with \( 8.00\,\mathrm{k}\Omega \) is measured by a voltmeter of \( 20\,\mathrm{k}\Omega/\mathrm{V} \) on the 10 V range (so \( R_m = 200\,\mathrm{k}\Omega \)). The open-circuit voltage is the quantity of interest.

### Find

The voltmeter reading and the relative loading error versus the true open-circuit voltage.

### Solution

\( V_{\mathrm{read}} = 12\times 200/(8+200) = 12\times 200/208 = 11.538 \) V. Relative error \( (11.538-12)/12 = -0.0385 = -3.85\% \). First-order check: \( -R_{th}/R_m = -8/200 = -4.00\% \).

### Answer

\( 11.54 \) V; loading error \( -3.85\% \) (about \( -4\% \) to first order).

## Q6

### Given

\( y = k\,x^{2}/z \) with relative limiting errors \( 0.3\% \) in \( x \) and \( 0.5\% \) in \( z \). The constant \( k \) is exact.

### Find

Relative limiting error of \( y \).

### Solution

\( \mathrm{d}y/y = 2\,\mathrm{d}x/x - \mathrm{d}z/z \), so limiting \( \Delta y/y = 2\times 0.3\% + 0.5\% = 1.1\% \).

### Answer

\( 1.1\% \).
