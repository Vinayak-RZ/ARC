# Linear ODEs and constant-coefficient systems

Every lumped linear circuit, every linearized machine, and every classical plant model in a first control course is a linear ordinary differential equation with constant coefficients, or a first-order vector system \(\dot{x}=Ax+Bu\) that is equivalent to one. This unit is the solution methods used in those courses: characteristic equations, undetermined coefficients, variation of parameters in the single-equation case, and the matrix exponential for constant \(A\). Partial differential equations (transmission-line telegrapher equations in space and time) are not solved here. Nonlinear machine torque-speed curves are linearized only as far as “the Jacobian is an \(A\) matrix.”

The independent variable is almost always time \(t\ge 0\). Initial conditions are capacitor voltages and inductor currents, or state variables of a mechanical analog. Forcing functions in UG EE are constants (DC sources switched in), steps, ramps, exponentials, and sinusoids. The Laplace transform (unit 03) is the industrial method for the same ODEs; this unit keeps the time-domain story so that the transform is not a black box.

## Concepts

A linear ODE of order \(n\) has the form
\[
a_n(t)y^{(n)}+\cdots+a_1(t)y'+a_0(t)y = g(t).
\]
Constant coefficients means each \(a_k\) is a number, not a function of \(t\). The equation is homogeneous when \(g\equiv 0\). Superposition holds: if \(y_1\) and \(y_2\) solve the homogeneous equation, so does \(c_1 y_1+c_2 y_2\). If \(y_p\) is any particular solution of the nonhomogeneous equation and \(y_h\) is the general homogeneous solution, then \(y=y_h+y_p\) is the general solution of the forced equation. The \(n\) free constants in \(y_h\) are fixed by \(n\) initial (or boundary) conditions.

The characteristic polynomial of a constant-coefficient homogeneous equation
\[
a_n r^n + \cdots + a_1 r + a_0 = 0
\]
is obtained by substituting \(y=e^{rt}\). Each distinct real root \(r\) gives a term \(ce^{rt}\). A repeated real root of multiplicity \(m\) gives \(e^{rt}(c_0 + c_1 t + \cdots + c_{m-1}t^{m-1})\). A complex conjugate pair \(\alpha\pm j\omega\) (coefficients real) gives \(e^{\alpha t}(A\cos\omega t + B\sin\omega t)\), equivalently \(Ce^{\alpha t}\cos(\omega t-\phi)\). Electrical engineers prefer the damped-sinusoid form because it matches oscilloscope traces of underdamped RLC transients.

Classification of second-order circuits is the same classification as second-order characteristic roots. For \(\ddot{y}+2\zeta\omega_n\dot{y}+\omega_n^2 y = 0\), the damping ratio \(\zeta\) decides overdamped (\(\zeta>1\), two negative real roots if \(\omega_n>0\) and the linear term has the stable sign), critically damped (\(\zeta=1\), repeated root), or underdamped (\(0\le\zeta<1\), complex pair). Undamped (\(\zeta=0\)) is the LC loop with no R. The same \(\zeta,\omega_n\) language is reused in control time-response. Stability for these constant-coefficient equations, with no delayed terms, is “all characteristic roots have negative real parts.” A root on the imaginary axis gives a sustained sinusoid (marginal in the BIBO sense if it is simple and not forced at that frequency in a way that resonates). A positive real part is exponential growth: an unstable linearized model, or a negative-resistance oscillator viewed as a linear ODE with the wrong sign on damping.

A first-order linear state system \(\dot{x}=Ax+Bu\), \(x(t)\in\mathbb{R}^n\), is the form used in modern UG control. If \(A\) is diagonalizable, \(A=P\Lambda P^{-1}\) with \(\Lambda=\operatorname{diag}(\lambda_i)\), the homogeneous solution is \(x(t)=P e^{\Lambda t} P^{-1} x(0)\) with \(e^{\Lambda t}=\operatorname{diag}(e^{\lambda_i t})\). If \(A\) is not diagonalizable, a Jordan block of size two for eigenvalue \(\lambda\) produces a factor \(t e^{\lambda t}\), the same repeated-root phenomenon. The matrix exponential \(e^{At}=\sum_{k\ge 0}(At)^k/k!\) always exists; computing it by the series is rarely the exam method. Laplace methods, Cayley–Hamilton, and diagonalization are.

Existence and uniqueness for linear ODEs with continuous coefficients on an interval are guaranteed for an initial-value problem. In circuits this means: specify every capacitor voltage and inductor current at \(t=0^+\), and the unique forward solution exists. Discontinuous sources (steps) are allowed as forcing; the state itself does not jump unless an impulse of current hits a capacitor or an impulse of voltage hits an inductor. Impulse forcing is the Dirac delta, treated distributionally: integrate the ODE across \(t=0\) to obtain the jump.

The homogeneous solution is called the natural response in circuits; the particular solution for a sustained source is the forced response. In sinusoidal steady state the particular solution is the phasor solution of unit 01. Transient analysis is the homogeneous piece decaying from the mismatch between initial state and that particular solution. Switching a DC source onto an RC circuit is first-order: \(y(t)=y(\infty)+(y(0^+)-y(\infty))e^{-t/\tau}\) with \(\tau=RC\) or \(L/R\). That formula is the general solution of \(\tau\dot{y}+y=y(\infty)\) with constant right-hand side, not a new theory.

Coupled first-order equations appear as a mesh pair with two inductors, or as a state model. Elimination can produce one second-order equation in one unknown; the characteristic polynomial is \(\det(sI-A)=0\) after Laplace or \(\det(\lambda I-A)=0\) in the time domain. Do not compute eigenvalues of \(A\) and then forget that the eigenvectors are needed to match initial conditions. The modal matrix \(P\) is part of the solution, not decoration.

Green’s functions and impulse responses are the same idea: the particular solution for \(g=\delta(t)\) with rest initial conditions is \(h(t)\), and convolution \(h*g\) solves general forcing. Unit 03 and the signals pack develop this. Here it is enough to know that undetermined coefficients is a shortcut when \(g\) is a polynomial, exponential, sinusoid, or a product of those (the DC, step, exponential, and AC sources of circuit books). If \(g\) is a term already in the homogeneous solution, multiply the trial particular solution by \(t\) (or \(t^s\) for multiplicity \(s\)).

Variation of parameters always works for a fundamental set \(y_1,y_2\) of a second-order equation, at the cost of integrals. For constant-coefficient UG problems, undetermined coefficients is shorter. Use variation of parameters when \(g(t)=1/t\), \(\tan t\), or another function outside the exponential-polynomial family.

Dimensional consistency is part of the mathematics in this department. If \(y\) is volts, each term in the ODE must be volts (or volts per second, consistently). The characteristic root \(r\) has units of inverse seconds. Writing \(\ddot{v}+3v=0\) without a coefficient that carries \(s^{-2}\) is a modelling error, even if the algebra of the numbers is fine.

Boundary-value problems (two-point conditions, Sturm–Liouville) appear in some engineering-maths modules and in electrostatics in one dimension. They are not the default circuit problem, which is an initial-value problem. Eigenvalue problems for \(X''+\lambda X=0\) with \(X(0)=X(L)=0\) produce Fourier sine series; that is unit 04, not this one.

## Equations

Standard constant-coefficient form:

\[
a_n y^{(n)}+\cdots+a_1 y'+a_0 y = g(t),\qquad a_n\neq 0.
\]

Characteristic equation:

\[
a_n r^n + \cdots + a_1 r + a_0 = 0.
\]

Second-order prototype (control/circuits):

\[
\ddot{y} + 2\zeta\omega_n \dot{y} + \omega_n^2 y = \omega_n^2 u(t).
\]

Underdamped homogeneous solution (\(\zeta<1\)):

\[
y_h(t) = e^{-\zeta\omega_n t}\big(A\cos\omega_d t + B\sin\omega_d t\big),\qquad \omega_d = \omega_n\sqrt{1-\zeta^2}.
\]

First-order linear circuit with constant target:

\[
y(t) = y(\infty) + \big(y(0^+)-y(\infty)\big)e^{-t/\tau}.
\]

State equation and solution (constant \(A,B\), integrable \(u\)):

\[
\dot{x}=Ax+Bu,\qquad x(t)=e^{At}x(0)+\int_0^t e^{A(t-\sigma)}Bu(\sigma)\,d\sigma.
\]

Cayley–Hamilton (for computing \(e^{At}\) as a polynomial in \(A\)):

\[
\chi_A(A)=0,\qquad \chi_A(\lambda)=\det(\lambda I-A).
\]

Wronskian for two solutions of a second-order homogeneous equation:

\[
W(y_1,y_2)=y_1 y_2' - y_2 y_1'.
\]
If \(W\neq 0\) on the interval, the pair is a fundamental set.

Undetermined-coefficient trials (real coefficients): for \(g=p_k(t)e^{\alpha t}\), try \(t^s q_k(t)e^{\alpha t}\) with \(s=0\) unless \(\alpha\) is already a root of multiplicity \(s\). For \(g=p_k(t)e^{\alpha t}\cos\beta t\) or \(\sin\beta t\), include both sine and cosine in the trial, times \(t^s\) if \(\alpha\pm j\beta\) are roots.

## Methods

Write the ODE with the highest derivative alone, identify order, and confirm constant coefficients. Form the characteristic polynomial. Factor it; for quadratics use the discriminant. Classify each root (real distinct, repeated, complex pair). Write \(y_h\) with the matching template and the correct number of arbitrary constants.

For a step or DC forcing, a constant particular solution \(y_p=K\) usually works: plug in, solve \(a_0 K = g\). If \(a_0=0\) (a root at the origin, pure integrators, series capacitors already accounted as state), use \(K t\) or a higher power of \(t\). For sinusoidal forcing at frequency \(\omega\), use \(y_p=A\cos\omega t+B\sin\omega t\), or switch to phasors and take the real part — that is undetermined coefficients in polar clothing.

Apply initial conditions to the full \(y=y_h+y_p\), never to \(y_h\) alone, unless the particular solution happens to be zero at the initial instant and all required derivatives match, which you must check. In circuits, \(t=0^-\) and \(t=0^+\) differ when a switch changes the topology; capacitor voltage and inductor current are continuous unless impulses occur. Resistive voltages may jump.

For a \(2\times 2\) system \(\dot{x}=Ax\), compute eigenvalues from \(\det(A-\lambda I)=0\) (or \(\det(\lambda I-A)=0\), consistently). For each eigenvalue, solve \((A-\lambda I)v=0\) for an eigenvector. If two independent eigenvectors exist, \(x(t)=c_1 v_1 e^{\lambda_1 t}+c_2 v_2 e^{\lambda_2 t}\). Fit \(c_1,c_2\) from \(x(0)\). If there is only one independent eigenvector, find a generalized eigenvector \(w\) with \((A-\lambda I)w=v\), and include the \(t e^{\lambda t}\) term.

Reduction of order: if one homogeneous solution \(y_1\) is known, set \(y=v(t)y_1\) and obtain a first-order equation in \(v'\). This is useful when a root is obvious by inspection (for example a rigid-body mode \(r=0\)).

Check a finished solution by differentiating and substituting back into the ODE, and by plugging the initial time into \(y\) and \(y'\). A solution that satisfies initial conditions but not the ODE is wrong; a solution that satisfies the ODE but not the initial conditions is the wrong member of the family.

When the forcing starts at \(t=0\) and is zero before, treat the problem as causal: homogeneous solution for the coefficients of \(e^{rt}\) is determined by \(0^+\) data. If you use two-sided functions (\(\cos\omega t\) for all \(t\)), you are solving a different problem (no switch).

## Mistakes

Using \(y_p = A\cos\omega t\) without a sine term when the ODE has a first-derivative (damping) term. Both quadratures are required unless you work in complex exponentials and take the real part at the end.

Matching initial conditions to \(y_h\) only, then adding \(y_p\). The constants come out wrong by exactly the particular solution’s initial value.

Writing the underdamped frequency as \(\omega_n\) instead of \(\omega_d=\omega_n\sqrt{1-\zeta^2}\). Oscilloscope period is \(2\pi/\omega_d\).

Taking \(\sqrt{\zeta^2-1}\) when \(\zeta<1\), or using real exponentials for an underdamped circuit. Check the discriminant of \(r^2+2\zeta\omega_n r+\omega_n^2=0\).

Forgetting multiplicity: a repeated root \(r\) needs \(c_1 e^{rt}+c_2 t e^{rt}\). Critical damping is this case. Writing only \(ce^{-t/\tau}\) for a series RLC at \(\zeta=1\) cannot match two initial conditions.

Sign error in the state matrix from KCL/KVL, producing a right-half-plane eigenvalue in a passive RLC network. Passive linear RLC with positive elements cannot be unstable; the characteristic roots must lie in the closed left half-plane. Use that as a modelling check.

Adding particular solutions for two frequencies and then using a single phasor. Superposition is in the time domain; each frequency gets its own particular solution.

Treating a step as an impulse, or integrating across a switch without checking for impulses. A finite voltage step on a capacitor current is an impulse of current only in the ideal model if you differentiate a jump; capacitor voltage itself does not jump.

Dimensionless mixing: adding \(\ddot{v}\) to \(v\) without coefficients. In a real circuit the coefficients are \(LC\), \(RC\), and so on.

Computing \(e^{At}\) as the elementwise exponential of the matrix \(A\). The exponential is defined by the power series in the matrix product, not elementwise, except in the special case that \(A\) is diagonal.

Dropping the convolution integral and writing \(x(t)=e^{At}x(0)+Bu(t)\) for a forced system. That formula is false unless \(A=0\) or \(u\) is an impulse in a carefully interpreted sense.

Complex characteristic roots kept as \(e^{(\alpha+j\omega)t}\) without combining conjugates into a real sinusoid when \(y\) is a real voltage. The physical waveform is real.
