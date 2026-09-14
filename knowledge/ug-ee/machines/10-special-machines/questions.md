# Questions — Stepper, BLDC, reluctance, servo intro

Original numbers.

## Q1

### Given

A hybrid stepper, 1.8° full step, 200 full steps per revolution. Microstepping 16 microsteps per full step.

### Find

Microstep angle, and the number of microsteps for 2.5 shaft revolutions.

### Solution

\[
\theta_\mu=1.8^\circ/16=0.1125^\circ.
\]

Microsteps/rev \(=200\times 16=3200\). For 2.5 rev: \(2.5\times 3200=8000\) microsteps.

### Answer

\(0.1125^\circ/\mu\mathrm{step}\), 8000 microsteps

## Q2

### Given

Two-phase hybrid stepper. Full-step holding torque (two phases on, \(i_A=i_B=I_m\)) is 0.80 N·m. Assume \(T\propto i_A\cos p\theta + i_B\sin p\theta\) in the linear model, and holding is the maximum of that.

### Find

Holding torque with one phase on at \(I_m\), and the microstep torque amplitude if \(i_A=I_m\cos\alpha\), \(i_B=I_m\sin\alpha\) (constant-magnitude microstepping).

### Solution

Two-phase-on: \(i_A=i_B=I_m\), the current vector magnitude is \(I_m\sqrt{2}\), torque amplitude \(k I_m\sqrt{2}=0.80\ \mathrm{N\cdot m}\).

One phase on: magnitude \(I_m\), torque amplitude \(0.80/\sqrt{2}=0.566\ \mathrm{N\cdot m}\).

Constant-magnitude microstepping: \(|i|=I_m\) for all \(\alpha\), same as one-phase amplitude if the model is \(T=k|i|\). Many drives keep \(|i|=I_m\sqrt{2}\) to preserve two-phase holding; if they instead keep \(|i|=I_m\), holding is 0.566 N·m. The problem’s sinusoidal pair at \(I_m\) is the \(|i|=I_m\) case: amplitude \(0.566\ \mathrm{N\cdot m}\).

### Answer

One-phase hold \(0.566\ \mathrm{N\cdot m}\); \(|i|=I_m\) microstep amplitude \(0.566\ \mathrm{N\cdot m}\)

## Q3

### Given

BLDC, six-step, two phases on. \(k_e=0.12\ \mathrm{V\cdot s/rad}\) (line-to-line trapezoid plateau), \(R_\mathrm{ph}=0.40\ \Omega\), \(L\) neglected (average). DC link 48 V, PWM duty \(\delta=0.75\). No-load except a small current. Load current (DC link average) 8.0 A.

### Find

Approximate steady speed at this duty and current, using \(V_\mathrm{avg}=\delta V_\mathrm{dc}=E+I(2R_\mathrm{ph})\).

### Solution

\[
V_\mathrm{avg}=0.75\times 48=36.0\ \mathrm{V},\qquad 2R=0.80\ \Omega,
\]

\[
E=36.0-8.0\times 0.80=29.6\ \mathrm{V},\qquad \omega=E/k_e=29.6/0.12=246.7\ \mathrm{rad/s}.
\]

\[
n=246.7\times 60/(2\pi)=2355\ \mathrm{r/min}.
\]

SI: \(k_t=k_e=0.12\ \mathrm{N\cdot m/A}\), \(T=k_t I=0.96\ \mathrm{N\cdot m}\) (if \(I\) is the plateau phase current; here the 8 A is used as that current in the two-phase-on model).

### Answer

\(\omega=247\ \mathrm{rad/s}\) (\(2350\ \mathrm{r/min}\))

## Q4

### Given

A singly excited reluctance actuator (rotary), linear \(L(\theta)=L_0+L_1\cos 2\theta\) with \(L_0=12\ \mathrm{mH}\), \(L_1=8\ \mathrm{mH}\), \(i=6.0\ \mathrm{A}\) constant, \(\theta=20^\circ\).

### Find

Torque \(T=\tfrac12 i^2 \mathrm{d}L/\mathrm{d}\theta\) (SI, \(\theta\) in radians in the derivative).

### Solution

\[
\frac{\mathrm{d}L}{\mathrm{d}\theta}=-2 L_1\sin 2\theta=-2(0.008)\sin 40^\circ=-0.016\times 0.6428=-0.01028\ \mathrm{H/rad}.
\]

\[
T=\tfrac12 (36)(-0.01028)=-0.1851\ \mathrm{N\cdot m}.
\]

The negative sign means torque toward decreasing \(\theta\) at this position (toward alignment at \(\theta=0\) where \(L\) is max if \(\cos 2\theta\) is max).

### Answer

\(T=-0.185\ \mathrm{N\cdot m}\)

## Q5

### Given

Servo axis: motor \(J_m=2.0\times 10^{-4}\ \mathrm{kg\cdot m}^2\), load \(J_L=1.8\times 10^{-3}\) at the shaft (direct drive), friction neglected. Required \(\alpha=400\ \mathrm{rad/s}^2\). Load torque 0.15 N·m. Motor \(k_t=0.25\ \mathrm{N\cdot m/A}\).

### Find

Motor current needed (average) during this acceleration.

### Solution

\[
J_\mathrm{tot}=2.0\times 10^{-4}+1.8\times 10^{-3}=2.0\times 10^{-3}\ \mathrm{kg\cdot m}^2,
\]

\[
T=J\alpha+T_L=2.0\times 10^{-3}\times 400+0.15=0.80+0.15=0.95\ \mathrm{N\cdot m},
\]

\[
I=T/k_t=0.95/0.25=3.80\ \mathrm{A}.
\]

### Answer

\(I=3.80\ \mathrm{A}\)
