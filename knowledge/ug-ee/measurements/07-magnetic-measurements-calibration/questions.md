# Questions — Fluxmeter, B–H, calibration chain

Original pedagogical numbers.

## Q1

### Given

Search coil \( N=80 \) turns, closed through resistance \( 150\,\Omega \). A flux change produces a charge \( 0.400\,\mu\mathrm{C} \) through a ballistic galvanometer.

### Find

\( \Delta\Phi \).

### Solution

\( Q=N\Delta\Phi/R\Rightarrow \Delta\Phi=QR/N=0.400\times 10^{-6}\times 150/80=0.750\,\mu\mathrm{Wb} \).

### Answer

\( 0.750\,\mu\mathrm{Wb} \).

## Q2

### Given

Ring mean length 0.250 m, 120 magnetizing turns, current 2.00 A. Cross-section \( 5.00 \) cm². A reverse of current (from \( +2 \) A to \( -2 \) A) gives \( \Delta\Phi=1.80\times 10^{-4} \) Wb in the core (from the search coil, already divided by its \( N \)).

### Find

\( H \) before reversal and \( \Delta B \). If the specimen was at \( +B \) and goes to \( -B \) with a symmetric loop, estimate \( B \).

### Solution

\( H=NI/\ell=120\times 2/0.250=960 \) A/m. \( \Delta B=\Delta\Phi/A=1.80\times 10^{-4}/5.00\times 10^{-4}=0.360 \) T. Symmetric reverse of \( I \) gives \( \Delta B=2B \), so \( B=0.180 \) T.

### Answer

\( H=960 \) A/m; \( \Delta B=0.360 \) T; \( B=0.180 \) T if symmetric.

## Q3

### Given

Mutual inductor \( M=25.0 \) mH. Primary current steps by \( 0.800 \) A.

### Find

The volt-second integral at the secondary, \( \int v\,\mathrm{d}t \).

### Solution

\( \int v\,\mathrm{d}t=M\Delta I=0.025\times 0.800=0.0200 \) V·s.

### Answer

\( 0.0200 \) V·s.

## Q4

### Given

Hall probe \( V_H=k_H I B \) with \( k_H=0.80 \) V/(A·T), control current 50.0 mA, \( V_H=6.00 \) mV.

### Find

\( B \).

### Solution

\( B=V_H/(k_H I)=0.006/(0.80\times 0.050)=0.150 \) T.

### Answer

\( 0.150 \) T.

## Q5

### Given

Meter constant of a fluxmeter is calibrated 4.00% high (it reads 1.040 times true \( \int v\,\mathrm{d}t \)). A subsequent \( \Delta\Phi \) measurement with \( N=40 \) uses that meter reading 2.00 mV·s without correction.

### Find

The reported \( \Delta\Phi \) and the true \( \Delta\Phi \).

### Solution

Reported \( \Delta\Phi=\int v_{\mathrm{read}}/N=0.002/40=50.0\,\mu\mathrm{Wb} \). True integral \( =2.00/1.040=1.923 \) mV·s. True \( \Delta\Phi=48.1\,\mu\mathrm{Wb} \).

### Answer

Reported \( 50.0\,\mu\mathrm{Wb} \); true \( 48.1\,\mu\mathrm{Wb} \).

## Q6

### Given

A working voltmeter’s Type B spec is 0.20% of reading. The laboratory standard used to calibrate it has 0.05% expanded uncertainty (\( k=2 \)), so standard uncertainty 0.025%. Combine as RSS standard uncertainties, treating the 0.20% spec as a rectangular half-width → \( u=0.20\%/\sqrt{3} \).

### Find

Combined standard uncertainty of a calibrated reading still using the working meter’s spec as the dominant Type B (as-left, no adjustment).

### Solution

\( u_{\mathrm{meter}}=0.20/\sqrt{3}=0.1155\% \). \( u_{\mathrm{std}}=0.025\% \). \( u_c=\sqrt{0.1155^2+0.025^2}=0.118\% \).

### Answer

\( u_c\approx 0.12\% \) of reading.
