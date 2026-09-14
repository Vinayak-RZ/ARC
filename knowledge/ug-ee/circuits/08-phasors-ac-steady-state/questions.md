# Questions — Phasors and AC steady state

Original pedagogical numbers.

## Q1

### Given

\( v_s(t) = 18.0\cos(400 t + 30^\circ)\,\mathrm{V} \) in series with \( R = 30\,\Omega \) and \( L = 50\,\mathrm{mH} \). Peak phasors.

### Find

Current \( i(t) \) and the voltage across the inductor.

### Solution

\( Z_L = j 400 \times 0.050 = j20\,\Omega \). \( Z = 30 + j20 = 36.06\angle 33.69^\circ\,\Omega \). \( \mathbf{V}_s = 18\angle 30^\circ \). \( \mathbf{I} = 18\angle 30 / 36.06\angle 33.69 = 0.499\angle -3.69^\circ\,\mathrm{A} \). \( \mathbf{V}_L = \mathbf{I}(j20) = 0.499\angle -3.69 \times 20\angle 90 = 9.98\angle 86.31^\circ\,\mathrm{V} \). So \( i(t) = 0.499\cos(400 t - 3.69^\circ)\,\mathrm{A} \), \( v_L(t) = 9.98\cos(400 t + 86.31^\circ)\,\mathrm{V} \).

### Answer

\( i(t) = 0.499\cos(400t-3.69^\circ)\,\mathrm{A} \); \( v_L = 9.98\cos(400t+86.3^\circ)\,\mathrm{V} \).

## Q2

### Given

Two impedances in parallel: \( Z_1 = 40\,\Omega \), \( Z_2 = -j30\,\Omega \), driven by RMS phasor \( \mathbf{I} = 2.0\angle 0^\circ\,\mathrm{A} \).

### Find

Derive the equivalent impedance and the branch currents.

### Solution

\( Z_\mathrm{eq} = 40 \parallel (-j30) = \frac{40(-j30)}{40-j30} = \frac{-j1200}{50\angle -36.87^\circ} = 24.0\angle -53.13^\circ\,\Omega = 14.4 - j19.2\,\Omega \). Voltage \( \mathbf{V} = \mathbf{I} Z_\mathrm{eq} = 48.0\angle -53.13^\circ\,\mathrm{V} \). \( \mathbf{I}_1 = \mathbf{V}/40 = 1.200\angle -53.13^\circ\,\mathrm{A} \). \( \mathbf{I}_2 = \mathbf{V}/(-j30) = 1.600\angle 36.87^\circ\,\mathrm{A} \). Sum \( 1.2\cos(-53.13) + j1.2\sin + 1.6\cos 36.87 + j1.6\sin = 0.720-j0.960+1.280+j0.960 = 2.0 \), checks.

### Answer

\( Z_\mathrm{eq} = 14.4-j19.2\,\Omega \); \( \mathbf{I}_1 = 1.20\angle -53.1^\circ\,\mathrm{A} \), \( \mathbf{I}_2 = 1.60\angle 36.9^\circ\,\mathrm{A} \).

## Q3

### Given

Design a series RC so that at 1.00 kHz the impedance angle is \( -35^\circ \) and \( |Z| = 2.2\,\mathrm{k}\Omega \).

### Find

R and C.

### Solution

\( Z = 2200\angle -35^\circ = 1802 - j1262\,\Omega \). So \( R = 1.802\,\mathrm{k}\Omega \), \( 1/(\omega C) = 1262 \), \( \omega = 2000\pi \). \( C = 1/(2000\pi \times 1262) = 126.1\,\mathrm{nF} \).

### Answer

\( R = 1.80\,\mathrm{k}\Omega \), \( C = 126\,\mathrm{nF} \).

## Q4

### Given

A student adds 10 V RMS across R and 10 V RMS across L in series and reports 20 V RMS at the source.

### Find

Explain the error and the true source RMS if the current is the same and the voltages are 90° apart.

### Solution

Phasors are orthogonal: \( \mathbf{V}_s = \mathbf{V}_R + \mathbf{V}_L \) as vectors, \( |V_s| = \sqrt{10^2+10^2} = 14.14\,\mathrm{V} \) RMS, not 20 V. Instantaneous peaks can still reach about 20 V at some instants, which is why peak ratings differ from RMS addition.

### Answer

Cannot add RMS scalars 90° apart; \( V_s = 14.14\,\mathrm{V} \) RMS.

## Q5

### Given

Nodal: ground, node A with \( Y = 0.010 - j0.020\,\mathrm{S} \) to ground, and a current source \( 0.50\angle 90^\circ\,\mathrm{A} \) into A. Peak phasors.

### Find

\( \mathbf{V}_A \) and \( v_A(t) \) if \( \omega = 300 \).

### Solution

\( \mathbf{V}_A = \mathbf{I}/Y = 0.50\angle 90 / (0.02236\angle -63.43) = 22.36\angle 153.43^\circ\,\mathrm{V} \). \( v_A(t) = 22.36\cos(300 t + 153.43^\circ)\,\mathrm{V} \).

### Answer

\( \mathbf{V}_A = 22.4\angle 153^\circ\,\mathrm{V} \); \( v_A(t) = 22.4\cos(300t+153^\circ)\,\mathrm{V} \).
