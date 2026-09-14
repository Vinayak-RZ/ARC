# Questions — Load torque, stability of equilibrium

Original numbers.

## Q1

### Given

Motor inertia \(J_m=0.30\,\mathrm{kg\cdot m}^2\), load inertia \(J_L=12.0\,\mathrm{kg\cdot m}^2\) on a gearbox with \(n=\omega_m/\omega_L=10\), ideal.

### Find

Equivalent inertia at the motor shaft.

### Solution

\[
J_{\mathrm{eq}}=0.30+\frac{12.0}{10^2}=0.30+0.12=0.42\,\mathrm{kg\cdot m}^2.
\]

### Answer

\(0.42\,\mathrm{kg\cdot m}^2\)

## Q2

### Given

\(J=0.42\,\mathrm{kg\cdot m}^2\), constant \(T_m=25\,\mathrm{N\cdot m}\), constant \(T_\ell=10\,\mathrm{N\cdot m}\). Start from rest to \(1200\,\mathrm{r/min}\).

### Find

Time.

### Solution

\[
\omega=1200\times\frac{2\pi}{60}=125.66\,\mathrm{rad/s},\qquad T_{\mathrm{net}}=15\,\mathrm{N\cdot m},
\]
\[
t=\frac{J\omega}{T_{\mathrm{net}}}=\frac{0.42\times 125.66}{15}=3.52\,\mathrm{s}.
\]

### Answer

\(3.52\,\mathrm{s}\)

## Q3

### Given

Separately excited DC: \(T_m=50-1.25\omega\) N·m (\(\omega\) in rad/s). Fan \(T_\ell=0.050\omega^2\).

### Find

Positive-speed equilibrium and whether it is stable (slope test).

### Solution

\[
50-1.25\omega=0.050\omega^2\qquad\Rightarrow\qquad \omega^2+25\omega-1000=0,
\]
\[
\omega=\frac{-25+\sqrt{625+4000}}{2}=\frac{-25+\sqrt{4625}}{2}=\frac{-25+68.01}{2}=21.51\,\mathrm{rad/s}.
\]
\[
\frac{\mathrm{d}T_m}{\mathrm{d}\omega}=-1.25,\qquad\frac{\mathrm{d}T_\ell}{\mathrm{d}\omega}=0.10\omega=2.15.
\]

\(-1.25<2.15\): stable.

### Answer

\(\omega=21.5\,\mathrm{rad/s}\), stable

## Q4

### Given

Translational mass \(m=800\,\mathrm{kg}\) on a drum \(r=0.25\,\mathrm{m}\), motor inertia \(0.50\,\mathrm{kg\cdot m}^2\), no gearbox. Level rail, neglect drum mass.

### Find

Total \(J\) at the motor/drum shaft.

### Solution

\[
J=0.50+800\times 0.25^2=0.50+50.0=50.5\,\mathrm{kg\cdot m}^2.
\]

### Answer

\(50.5\,\mathrm{kg\cdot m}^2\)

## Q5

### Given

Duty: \(40\,\mathrm{N\cdot m}\) for \(8\,\mathrm{s}\), \(10\,\mathrm{N\cdot m}\) for \(12\,\mathrm{s}\), cycle \(20\,\mathrm{s}\). Rated torque must cover \(T_{\mathrm{rms}}\).

### Find

RMS torque.

### Solution

\[
T_{\mathrm{rms}}=\sqrt{\frac{40^2\times 8+10^2\times 12}{20}}=\sqrt{\frac{12800+1200}{20}}=\sqrt{700}=26.46\,\mathrm{N\cdot m}.
\]

### Answer

\(26.5\,\mathrm{N\cdot m}\)

## Q6

### Given

Induction-motor breakdown at slip \(0.18\), \(T_{\max}=180\,\mathrm{N\cdot m}\). Constant load \(T_\ell=70\,\mathrm{N\cdot m}\). Standstill torque \(T(s=1)=90\,\mathrm{N\cdot m}\).

### Find

Whether the motor starts against this load, and which intersection is the intended running point (low-slip vs high-slip).

### Solution

At start \(T_m=90>70\): starts. Two intersections of a typical induction curve with a horizontal \(T_\ell=70\): one at \(s<0.18\) (stable) and one at \(s>0.18\) (unstable). The intended running point is the low-slip intersection.

### Answer

Starts (\(90>70\)); run at the low-slip intersection (stable)
