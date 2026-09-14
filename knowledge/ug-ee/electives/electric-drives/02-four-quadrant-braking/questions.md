# Questions — Plugging, regenerative, dynamic braking

Original numbers.

## Q1

### Given

Separately excited DC machine, \(K\phi=1.60\,\mathrm{V\cdot s/rad}\), \(R_a=0.40\,\Omega\), \(\omega=120\,\mathrm{rad/s}\). Dynamic brake resistor \(R_b=1.20\,\Omega\), field unchanged.

### Find

\(E_a\), braking current, torque, and mechanical power.

### Solution

\[
E_a=1.60\times 120=192\,\mathrm{V},\qquad I_a=192/(0.40+1.20)=120\,\mathrm{A},
\]
\[
T=1.60\times 120=192\,\mathrm{N\cdot m},\qquad P_{\mathrm{mech}}=E_a I_a=23.04\,\mathrm{kW}.
\]

### Answer

\(E_a=192\,\mathrm{V}\), \(I_a=120\,\mathrm{A}\), \(T=192\,\mathrm{N\cdot m}\), \(P=23.0\,\mathrm{kW}\)

## Q2

### Given

Same machine and speed as Q1. Regenerative braking into \(V_t=160\,\mathrm{V}\) (current reversed).

### Find

Generating current and braking torque.

### Solution

\[
I_a=(E_a-V_t)/R_a=(192-160)/0.40=80.0\,\mathrm{A},\qquad T=1.60\times 80=128\,\mathrm{N\cdot m}.
\]

### Answer

\(I_a=80.0\,\mathrm{A}\), \(T=128\,\mathrm{N\cdot m}\)

## Q3

### Given

Same \(E_a=192\,\mathrm{V}\), \(V_t=220\,\mathrm{V}\), \(R_a=0.40\,\Omega\). Plugging with extra \(R_{\mathrm{ext}}=2.00\,\Omega\).

### Find

Plugging current. Also the unprotected plugging current if \(R_{\mathrm{ext}}=0\).

### Solution

\[
I=\frac{220+192}{0.40+2.00}=\frac{412}{2.40}=171.7\,\mathrm{A},\qquad I_{\mathrm{naked}}=\frac{412}{0.40}=1030\,\mathrm{A}.
\]

### Answer

\(172\,\mathrm{A}\) with \(R_{\mathrm{ext}}\); \(1.03\,\mathrm{kA}\) unprotected

## Q4

### Given

Inertia \(J=8.0\,\mathrm{kg\cdot m}^2\), \(\omega=120\,\mathrm{rad/s}\), dynamic braking as in Q1 with constant \(T=192\,\mathrm{N\cdot m}\) (approximate, actually \(T\propto\omega\)). Use the constant-torque estimate for time to rest \(t=J\omega/T\), and the exact kinetic energy \(\tfrac12 J\omega^2\).

### Find

Kinetic energy and constant-torque stopping time.

### Solution

\[
W=0.5\times 8.0\times 14400=57.6\,\mathrm{kJ},\qquad t=8.0\times 120/192=5.00\,\mathrm{s}.
\]

(True dynamic brake with \(T\propto\omega\) is exponential, longer to the last few r/min.)

### Answer

\(57.6\,\mathrm{kJ}\); \(5.00\,\mathrm{s}\) (constant-\(T\) estimate)

## Q5

### Given

4-pole induction motor, 50 Hz, running at \(1440\,\mathrm{r/min}\). Two stator leads reversed (plugging). Synchronous speed \(n_s=1500\,\mathrm{r/min}\).

### Find

Slip immediately after reversal.

### Solution

After reversal the field rotates at \(-1500\,\mathrm{r/min}\). Rotor still \(+1440\,\mathrm{r/min}\).

\[
s=\frac{-1500-1440}{-1500}=\frac{-2940}{-1500}=1.96.
\]

### Answer

\(s=1.96\)

## Q6

### Given

VSI DC bus \(C=4000\,\mu\mathrm{F}\), \(V_{\mathrm{dc}}=650\,\mathrm{V}\). A stop dumps \(\Delta E=800\,\mathrm{J}\) into the capacitor (no chopper). \(\Delta V\approx\Delta E/(C V_{\mathrm{dc}})\).

### Find

Approximate bus voltage rise.

### Solution

\[
\Delta V=\frac{800}{4000\times 10^{-6}\times 650}=\frac{800}{2.60}=308\,\mathrm{V}.
\]

New voltage \(\approx 958\,\mathrm{V}\) (trip territory; a brake chopper is required).

### Answer

\(\Delta V=308\,\mathrm{V}\) (bus \(\approx 958\,\mathrm{V}\))
