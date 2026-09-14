# TF, SS, linearization

A control problem starts with a plant model, not with a Bode plot. The undergraduate toolkit is three equivalent languages for the same linear lumped physics: an ordinary differential equation, a transfer function \(G(s)=Y(s)/U(s)\) at zero initial conditions, and a state-space quadruple \((A,B,C,D)\). Nonlinear plants that UG courses actually assign (a pendulum, a DC motor with Coulomb friction, a tank with square-root outflow) are linearized about an operating point so that those three languages apply in a neighbourhood. This unit is how those models are written, how they convert, and where they lie.

## Concepts

A lumped electrical, mechanical, thermal, or hydraulic plant with energy storage yields first-order equations in a chosen set of states. Capacitor voltages and inductor currents, masses’ velocities and spring deflections, tank heights, and thermal capacitances are the usual choices because they are the energy variables and they cannot jump under finite power. Collecting them as a column \(x\in\mathbb{R}^n\) and writing Kirchhoff, Newton, or conservation gives
\[
\dot{x}=f(x,u),\qquad y=h(x,u)
\]
in general. If \(f\) and \(h\) are linear (or affine with the affine piece absorbed into the input), this is already
\[
\dot{x}=Ax+Bu,\qquad y=Cx+Du.
\]
The matrix \(A\) is \(n\times n\), \(B\) is \(n\times m\), \(C\) is \(p\times n\), \(D\) is \(p\times m\). Single-input single-output (SISO) undergraduate problems have \(m=p=1\), so \(B\) is a column and \(C\) a row. The feedthrough \(D\) is zero whenever the output cannot respond instantaneously to the input: no algebraic path from \(u\) to \(y\). A voltage divider has \(D\neq 0\); a DC-motor speed has \(D=0\).

The transfer function of a linear state model with zero initial state is
\[
G(s)=C(sI-A)^{-1}B+D.
\]
Poles of \(G\) are eigenvalues of \(A\) unless a cancellation with a zero occurs. Zeros are the values of \(s\) that make the system matrix
\[
\begin{bmatrix}sI-A&-B\\C&D\end{bmatrix}
\]
drop rank (Rosenbrock). A pole–zero cancellation in \(G(s)\) means that mode is uncontrollable, unobservable, or both; the cancelled pole still lives in \(A\) and can still be unstable. Writing only \(G(s)\) hides that mode. That is why state-space is not optional decoration for stability arguments on realizations.

Properness: \(G(s)\) is strictly proper if \(\deg(\text{den})>\deg(\text{num})\), equivalently \(D=0\) and the high-frequency gain vanishes. It is biproper if degrees match (\(D\neq 0\)). It is improper if the numerator degree is larger: that model is not causal as a lumped ODE and does not arise from a well-posed state realization without differentiators. UG plants (motors, RLC, two-mass, tanks) are strictly proper. PID controllers are improper if written as \(K_p+K_is^{-1}+K_ds\); they need a high-frequency pole on the derivative term to be realizable.

Linearization. Let \(u_e,x_e\) be an equilibrium: \(f(x_e,u_e)=0\). Small deviations \(\tilde{x}=x-x_e\), \(\tilde{u}=u-u_e\) satisfy
\[
\dot{\tilde{x}}=A\tilde{x}+B\tilde{u},\qquad A=\frac{\partial f}{\partial x}\Big|_{e},\quad B=\frac{\partial f}{\partial u}\Big|_{e}
\]
to first order, and \(C=\partial h/\partial x\), \(D=\partial h/\partial u\) at the same point. The Jacobian is taken with every other variable held at the equilibrium, including constant gravity and constant load torque. A pendulum \(\ddot{\theta}+(g/\ell)\sin\theta=u\) linearizes to \(\ddot{\theta}+(g/\ell)\theta=u\) about hanging \(\theta=0\), and to \(\ddot{\theta}-(g/\ell)\theta=u\) about inverted \(\theta=\pi\) after a shift. Same nonlinear ODE, two different \(A\) matrices, one stable open loop and one not. Operating point is part of the model, not a footnote.

From ODE to TF: take Laplace of a linear constant-coefficient ODE, set initial conditions to zero (they are the zero-input response, superposed later), and form \(Y(s)/U(s)\). From TF to ODE: \(G(s)=b(s)/a(s)\) with monic \(a\) means \(a(D)y=b(D)u\) where \(D=d/dt\). From TF to state-space: any realization, typically controllable canonical form if the task is pole placement, or observable canonical form if the task is an observer. From SS to TF: the resolvent formula above, or Cramer on \((sI-A)X=BU\). Different realizations of the same \(G\) differ by similarity on the controllable-and-observable part; they are interchangeable for input–output behaviour and not interchangeable for hidden modes.

DC motor armature-controlled: states \(i_a,\omega\). Electrical: \(L\dot{i}_a=-Ri_a-k_b\omega+v_a\). Mechanical: \(J\dot{\omega}=k_t i_a-b\omega-T_L\). Output speed: \(C=[0,1]\), \(D=0\). Transfer \( \Omega(s)/V_a(s) \) is second order if \(L\) is kept, first order if \(L\approx 0\) (the usual UG reduction). Load torque is a disturbance input, a second column of \(B\), not a change of \(A\).

Translational mechanics: mass–spring–damper \(m\ddot{x}+c\dot{x}+kx=f\) is already linear. Two-mass with a shaft spring is fourth order if both positions and both velocities are states, or third if one position is measured relative. Rotational copies replace \(m\) by \(J\) and \(x\) by \(\theta\). Thermal: \(\dot{T}=(1/C_{th})(u-T/R_{th})\), first order. Tank: \(A_c\dot{h}=q_{\mathrm{in}}-a\sqrt{2gh}\) is nonlinear; the linearized outflow gain is \(a\sqrt{2g}/(2\sqrt{h_e})\) and depends on the steady height.

Relative degree: the excess of den over num poles, equal to how many times one must differentiate \(y\) before \(u\) appears. For SISO linear plants it is also the first Markov parameter \(CA^{r-1}B\neq 0\). Relative degree one plants can be inverted with a proper inverse; relative degree two (motor position from voltage, if inductance is neglected) cannot. UG design rarely inverts; it does need to know that a double integrator \(1/s^2\) is not a first-order lag.

Units and scaling. Write \(A\) in 1/s, \(B\) in (state unit)/(input unit)/s. A numerical \(A\) with entries of \(10^6\) next to \(10^{-3}\) is a stiff electrical/mechanical pair (armature inductance versus inertia). Nondimensionalize or use SI consistently. Transfer-function coefficients inherit the same units: a plant \(10/(s(0.2s+1))\) has a free integrator (type 1) and a time constant 0.2 s.

Time delay \(e^{-sT}\) is transcendental, not a rational TF. Padé approximations of delay are used later for Bode/Nyquist sketches; they add RHP zeros (non-minimum phase) in the odd-order Padé. Do not linearize a delay by \(1-sT\) except as a low-frequency phase sketch.

MIMO is the same algebra with matrices. UG classical control is SISO; the state-space notes in later units keep MIMO dimensionally honest even when every numerical is SISO.

## Equations

Linear state model:
\[
\dot{x}=Ax+Bu,\qquad y=Cx+Du.
\]
Transfer function:
\[
G(s)=C(sI-A)^{-1}B+D=\frac{b_ms^m+\cdots+b_0}{s^n+a_{n-1}s^{n-1}+\cdots+a_0}.
\]
Characteristic polynomial:
\[
\chi(s)=\det(sI-A)=s^n+a_{n-1}s^{n-1}+\cdots+a_0.
\]
Cayley–Hamilton: \(\chi(A)=0\).

Linearization Jacobians:
\[
A_{ij}=\frac{\partial f_i}{\partial x_j}\Big|_{x_e,u_e},\qquad B_{ik}=\frac{\partial f_i}{\partial u_k}\Big|_{x_e,u_e}.
\]
Equilibrium: \(f(x_e,u_e)=0\). For a constant output \(y_e=h(x_e,u_e)\).

Controllable canonical realization of
\[
G(s)=\frac{b_1 s^{n-1}+\cdots+b_n}{s^n+a_1 s^{n-1}+\cdots+a_n}
\]
(with \(D=0\)):
\[
A=\begin{bmatrix}0&1&0&\cdots\\0&0&1&\cdots\\\vdots&&&\ddots\\-a_n&-a_{n-1}&\cdots&-a_1\end{bmatrix},\quad
B=\begin{bmatrix}0\\\vdots\\0\\1\end{bmatrix},\quad
C=\begin{bmatrix}b_n&\cdots&b_1\end{bmatrix}.
\]
(The companion indexing follows the monic denominator; match the course’s row/column convention before copying a matrix.)

Similarity: \(\bar{x}=Tx\) gives \(\bar{A}=TAT^{-1}\), \(\bar{B}=TB\), \(\bar{C}=CT^{-1}\), \(\bar{D}=D\), same \(G(s)\).

DC motor (armature):
\[
\begin{bmatrix}\dot{i}\\\dot{\omega}\end{bmatrix}
=\begin{bmatrix}-R/L&-k_b/L\\k_t/J&-b/J\end{bmatrix}
\begin{bmatrix}i\\\omega\end{bmatrix}
+\begin{bmatrix}1/L\\0\end{bmatrix}v_a
+\begin{bmatrix}0\\-1/J\end{bmatrix}T_L.
\]

Mass–spring–damper:
\[
\begin{bmatrix}\dot{x}\\\dot{v}\end{bmatrix}
=\begin{bmatrix}0&1\\-k/m&-c/m\end{bmatrix}
\begin{bmatrix}x\\v\end{bmatrix}
+\begin{bmatrix}0\\1/m\end{bmatrix}f.
\]

Pendulum linearizations:
\[
\ddot{\theta}+\frac{g}{\ell}\theta=u\quad(\text{down}),\qquad
\ddot{\theta}-\frac{g}{\ell}\theta=u\quad(\text{up}).
\]

## Methods

Start from physics, not from a guessed \(G(s)\). Name the states as energy variables. Write one first-order equation per state. Identify inputs (commands and disturbances) and the measured output. If the equations are linear, read off \((A,B,C,D)\). If not, find the equilibrium of interest by setting \(\dot{x}=0\) with the intended steady input, then form Jacobians. Report the operating point with the matrices; a linearized tank at \(h_e=1\,\mathrm{m}\) is a different plant from the same tank at \(h_e=4\,\mathrm{m}\).

To get a transfer function from an ODE, Laplace with zero ICs. Solve algebraically for \(Y/U\). Factor and cancel only after checking that the cancelled root is not a plant pole you still care about (RHP cancellations are forbidden as design moves; they are modelling bugs if they appear in the physics). State the DC gain \(G(0)\) and the relative degree.

To realize a given proper \(G(s)\), pick controllable canonical form unless the problem names another. Verify by computing \(C(sI-A)^{-1}B\) on a numerical example (2×2 is enough). If \(D\neq 0\), split \(G(s)=G_{\mathrm{sp}}(s)+D\) and realize the strictly proper part.

To convert SS to TF by hand, form \(sI-A\), invert by adjugate over determinant, then sandwich with \(C\) and \(B\). The determinant is the characteristic polynomial; it must match Routh later. For 2×2,
\[
(sI-A)^{-1}=\frac{1}{s^2-(\mathrm{tr}A)s+\det A}\begin{bmatrix}s-a_{22}&a_{12}\\a_{21}&s-a_{11}\end{bmatrix}.
\]

Check a model: (1) dimensions and SI units; (2) open-circuit / free-response poles in the closed LHP for a passive plant; (3) step response of \(G\) has the right DC value \(G(0)\); (4) relative degree matches how many integrators sit before the input appears in \(y\); (5) linearization Jacobian signs (restoring gravity versus inverted).

When a problem gives a block diagram already in transfer functions, the modelling step is done; still write the loop’s plant as one \(G\) only after reducing (next unit). When a problem gives a schematic, do not skip to a memorized motor TF with the wrong sign on back-emf.

For small-signal electronic plants (op-amp, linearized MOSFET), the same Jacobian story applies: bias point first, hybrid-π second, then TF. Control courses inherit the electronics small-signal model as \(G(s)\) and do not re-derive Shockley equations in the exam; they do require that the student know a linearized \(g_m\) is valid only near that bias.

Delay and saturation are not linear. Keep them out of \(A\) or treat delay as \(e^{-sT}\) in the TF and saturation as a later describing-function or describing-free simulation. Linearizing saturation at the origin of a relay gives gain 0 or \(\infty\) depending on the slope; that is a warning, not a model.

## Mistakes

Writing \(G(s)\) from an ODE but keeping initial conditions in the numerator, then calling the ratio a transfer function. TF is zero-state. Initial conditions belong in the zero-input response.

Cancelling an unstable pole against a zero and declaring the system stable because the reduced \(G\) is. The hidden mode is still in \(A\).

Linearizing \(\sin\theta\) as \(\theta\) about \(\theta=\pi\). Shift first: let \(\phi=\theta-\pi\), then \(\sin\theta=\sin(\phi+\pi)=-\sin\phi\approx-\phi\), which flips the stiffness sign.

Using \(D\neq 0\) for a motor speed or a tank height. Those outputs cannot jump with a finite input.

Treating load torque as a change of \(A\) instead of a second input. A constant load shifts the equilibrium; a time-varying load is \(B_d T_L\).

Elementwise inversion of \(sI-A\), or inverting each entry. The resolvent is a matrix inverse.

Writing companion form with the \(a_i\) on the wrong row or with a sign error, then trusting pole placement on that \(A\). Always recompute \(\det(sI-A)\) and match the intended denominator.

Mixing degrees: \(m\ddot{x}+c\dot{x}+kx=f\) implemented as \(A\) with \(k\) in the (2,1) entry without dividing by \(m\).

Calling a Padé delay a plant pole. Padé poles are artefacts of the approximation; the delay is all-pass in magnitude.

Using small-angle \(\sin\theta\approx\theta\) when the problem states 40° and asks for a simulation number. Linearization is a local model; quote the operating point or simulate the nonlinear ODE.

Forgetting units on \(G(0)\): a plant \(8/(s+2)\) has DC gain 4 in output-per-input units, not 8.

Building a realization of an improper TF (PID without a filter) as a state model. There is no finite-dimensional proper realization; add the missing pole or keep the PID in the controller slot of a block diagram rather than as a plant.
