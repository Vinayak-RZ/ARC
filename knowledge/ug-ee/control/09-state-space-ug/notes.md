# State space at UG: diagonalization and \(\dot{x}=Ax\)

Once a plant is written as \(\dot{x}=Ax+Bu\), \(y=Cx+Du\), the first analysis question is the free motion \(\dot{x}=Ax\). Diagonalization (when it exists) turns that vector ODE into decoupled scalars. The matrix exponential packages the same story for forced responses. This unit is eigenvalues, eigenvectors, \(e^{At}\), the variation-of-constants formula, and what Jordan blocks do when \(A\) is not diagonalizable — at the depth of a first UG control course, not a graduate linear-systems course.

## Concepts

The homogeneous solution of \(\dot{x}=Ax\) is \(x(t)=e^{At}x(0)\), where
\[
e^{At}=I+At+\frac{(At)^2}{2!}+\cdots
\]
always converges. If \(A=P\Lambda P^{-1}\) with \(\Lambda=\mathrm{diag}(\lambda_i)\), then \(e^{At}=P e^{\Lambda t}P^{-1}\) and \(e^{\Lambda t}=\mathrm{diag}(e^{\lambda_i t})\). The columns of \(P\) are independent eigenvectors. Each modal coordinate \(z=P^{-1}x\) satisfies \(\dot{z}_i=\lambda_i z_i\). Real \(A\) with a complex pair \(\alpha\pm j\omega\) gives a 2×2 real block; the corresponding motion is \(e^{\alpha t}(\cos\omega t,\sin\omega t)\) in a plane. Do not leave the physical state in complex form on an exam that asked for \(x(t)\).

If \(A\) is not diagonalizable, a Jordan block of size 2 for eigenvalue \(\lambda\) produces \(e^{\lambda t}\) and \(t e^{\lambda t}\). Size 3 adds \(t^2 e^{\lambda t}/2\). Repeated eigenvalues do *not* automatically mean Jordan: \(\lambda I\) is diagonalizable. Check geometric multiplicity (number of independent eigenvectors) against algebraic multiplicity.

Stability of \(\dot{x}=Ax\): the origin is asymptotically stable iff every eigenvalue has negative real part (and for \(j\omega\) eigenvalues, Jordan blocks must be 1×1 for Lyapunov stability, and even then it is not asymptotic). This is the same as Hurwitz of \(\det(sI-A)\). Routh applies to that polynomial. Internal stability is about \(A\), not about a cancelled \(G(s)\).

Forced equation \(\dot{x}=Ax+Bu(t)\):
\[
x(t)=e^{At}x(0)+\int_0^t e^{A(t-\tau)}B u(\tau)\,d\tau.
\]
Laplace: \(X(s)=(sI-A)^{-1}x(0)+(sI-A)^{-1}B U(s)\). A constant input \(u\equiv \bar{u}\) with invertible \(A\) yields a particular solution \(x_{ss}=-A^{-1}B\bar{u}\) (equilibrium of \(0=Ax+B\bar{u}\)). If \(A\) has a zero eigenvalue, a constant input may ramp the state (type 1 plant).

Similarity \(\bar{x}=Tx\) does not change eigenvalues, \(G(s)\), or controllability/observability ranks (those ranks are similarity invariants). It does change the numerical entries of \(B,C\). Diagonal form is the modal coordinates; controllable canonical form is for pole placement (next unit).

Cayley–Hamilton: \(A^n\) is a linear combination of \(I,A,\ldots,A^{n-1}\), so \(e^{At}\) is a polynomial in \(A\) of degree at most \(n-1\) with scalar functions of \(t\) as coefficients. For 2×2 that is \(e^{At}=\alpha_0(t)I+\alpha_1(t)A\), with \(\alpha_i\) solved on each eigenvalue (the inverse Laplace of the resolvent is the other hand method).

Trace and det: \(\chi(s)=s^2-(\mathrm{tr}A)s+\det A\) for 2×2. \(\mathrm{tr}A=\sum\lambda_i\), \(\det A=\prod\lambda_i\). A 2×2 Hurwitz test is \(\mathrm{tr}A<0\) and \(\det A>0\).

Impulse response of SISO with \(D=0\): \(g(t)=C e^{At}B\), \(t\ge 0\), and \(G(s)=\mathcal{L}\{g\}\). Markov parameters \(CB, CAB, CA^2B,\ldots\) are the Taylor coefficients of \(g\) at \(0^+\).

Coordinate choice: physical states (current, speed) are best for linearization and for reading units. Modal states are best for seeing which mode is slow. Controller-canonical states may have no physical meaning. Convert back before plotting “armature current.”

Discrete-time cousin \(x[k+1]=F x[k]\) has \(F=e^{AH}\) for a sampled continuous plant with period \(H\) and zero input during the period. That is unit 11. Do not replace \(A\) by \(I+AH\) except as a crude Euler step, which can map a stable \(A\) to an unstable \(F\) if \(H\) is large.

## Equations

\[
x(t)=e^{At}x_0+\int_0^t e^{A(t-\tau)}Bu(\tau)\,d\tau,\qquad
y=Cx+Du.
\]
\[
e^{At}=P\mathrm{diag}(e^{\lambda_i t})P^{-1}\quad(A\text{ diagonalizable}).
\]
Resolvent:
\[
(sI-A)^{-1}=\frac{\mathrm{adj}(sI-A)}{\det(sI-A)}.
\]
2×2 inverse:
\[
(sI-A)^{-1}=\frac{1}{s^2-(\mathrm{tr}A)s+\det A}\begin{bmatrix}s-a_{22}&a_{12}\\a_{21}&s-a_{11}\end{bmatrix}.
\]
Jordan 2-block:
\[
\exp\begin{bmatrix}\lambda&1\\0&\lambda\end{bmatrix}t
=e^{\lambda t}\begin{bmatrix}1&t\\0&1\end{bmatrix}.
\]
Equilibrium under constant \(u\): \(Ax_{ss}+B\bar{u}=0\).

## Methods

To solve \(\dot{x}=Ax\) by hand: compute \(\chi(\lambda)=\det(\lambda I-A)\), find eigenvalues, find eigenvectors, form \(P\), invert \(P\) (2×2: \((1/\det)\begin{bmatrix}d&-b\\-c&a\end{bmatrix}\)), write \(x(t)=P e^{\Lambda t}P^{-1}x_0\). Expand into real sinusoids if needed. Check \(t=0\) recovers \(x_0\) and check \(\dot{x}(0)=A x_0\).

If a repeated eigenvalue has only one eigenvector, find a generalized eigenvector \((A-\lambda I)w=v\), and use the \(t e^{\lambda t}\) template.

For a step input, split \(x=x_h+x_{ss}\) with \(x_{ss}=-A^{-1}B\) if \(A\) is invertible, then choose \(x_h(0)=x_0-x_{ss}\).

To get \(e^{At}\) via Laplace: inverse Laplace of \((sI-A)^{-1}\), entrywise, using partial fractions.

Numerical hygiene: a stiff \(A\) (eigenvalues at \(-1\) and \(-10^6\)) makes \(e^{At}\) a bad thing to form as a power series at large \(t\); the slow mode is \(e^{-t}\) and the fast mode is underflow. Modal coordinates or scaling first.

When the problem gives \(A\) and asks “stable?”, Routh on \(\chi(s)\) is faster than eigenvalues if \(n=3\) or 4. For \(n=2\), trace/det.

Do not diagonalize to compute \(G(s)\) unless it helps; \(C(sI-A)^{-1}B\) on the original matrices is fine at 2×2.

Complex-pair recipe, written as a real 2×2. If \(A\) has eigenvalues \(\alpha\pm j\omega\) and a complex eigenvector \(v=p+jq\), a real modal plane uses columns \(p\) and \(q\): in those coordinates the block is \(\begin{bmatrix}\alpha&-\omega\\\omega&\alpha\end{bmatrix}\) or the transpose, depending on order. Then
\[
\exp\begin{bmatrix}\alpha&-\omega\\\omega&\alpha\end{bmatrix}t
=e^{\alpha t}\begin{bmatrix}\cos\omega t&-\sin\omega t\\\sin\omega t&\cos\omega t\end{bmatrix}.
\]
Match \(x(0)\) in the original basis. This is the underdamped second-order plant in state form: the same \(\zeta\omega_n=-\alpha\), \(\omega_d=\omega\). Never report \(x(t)\) as \(c\,e^{(\alpha+j\omega)t}v\) plus “take real part” unless you also write the conjugate term; a real \(x_0\) already determines both.

Reachability integral as a check of the forced formula: for a scalar input on \(0\le t\le T\), \(x(T)=e^{AT}x_0+\int_0^T e^{A(T-\tau)}B u(\tau)\,d\tau\). If \(u\) is a unit impulse at \(0\), \(x(T^+)=e^{AT}x_0+B\) in the distributional sense for a plant with \(D=0\) and the impulse on \(\dot{x}\). If \(u\) is a unit step and \(A\) is Hurwitz, \(x(\infty)=-A^{-1}B\). Those two checks (impulse adds \(B\), step settles at the equilibrium) catch a missing \(B\) or a sign error in \(A^{-1}\).

Similarity invariance: eigenvalues, characteristic polynomial, \(G(s)\), and the ranks of \(\mathcal{C}\) and \(\mathcal{O}\) do not change under \(\bar{x}=Tx\). The matrix \(e^{At}\) does change representation: \(\overline{e^{At}}=T e^{At} T^{-1}\). Computing \(e^{\bar{A}t}\) in diagonal coordinates and mapping back is the practical algorithm. Computing \(e^{At}\) in a badly scaled physical basis is how floating-point `expm` still works and how hand series fail.

If the exam asks only for \(y(t)=C e^{At}x_0\), you may never need every entry of \(e^{At}\): compute the scalar resolvent entry \(C(sI-A)^{-1}x_0\) and inverse-Laplace that one function. For 2×2 that is one partial-fraction job instead of four. On a 3×3 with a known eigenvector already given, projecting \(x_0\) onto that mode is faster than inverting a full \(P\).

## Mistakes

Elementwise exponential: \(e^{A}\) is not \((e^{a_{ij}})\).

Writing \(x(t)=e^{At}x_0+B u(t)\) without the convolution.

Using \(A=P\Lambda P^{-1}\) with columns of \(P\) that are not actual eigenvectors (failed \((A-\lambda I)v=0\)).

Treating a defective repeated eigenvalue as if two independent modes \(c_1 e^{\lambda t}+c_2 e^{\lambda t}\) could match two independent initial conditions in different directions — they cannot; you need \(t e^{\lambda t}\).

Sign of \(\chi\): \(\det(A-\lambda I)\) versus \(\det(\lambda I-A)\) flips odd \(n\). Be consistent; eigenvalues are the same set.

Inverting \(A\) to find \(x_{ss}\) when \(0\) is an eigenvalue (a free body, a type-1 plant). The inverse does not exist; the particular solution may be a ramp.

Reporting complex \(x(t)\) for a real initial condition.

Confusing Hurwitz stability of \(A\) with BIBO stability of \((A,B,C)\): an unstable unobservable mode is internally unstable but can be BIBO-stable. UG answers should say which.

Euler \(I+AH\) as “the” discrete plant for a large \(H\).

Mixing seconds and milliseconds in \(e^{-3t}\) so that a plot looks like a step.

A 2×2 walk-through that should be muscle memory. \(A=\begin{bmatrix}0&1\\-2&-3\end{bmatrix}\), \(x(0)=\begin{bmatrix}1\\0\end{bmatrix}\). Characteristic \(s^2+3s+2=(s+1)(s+2)\). Eigenvectors: \(\lambda=-1\), \((A+I)v=0\), \(A+I=\begin{bmatrix}1&1\\-2&-2\end{bmatrix}\), \(v_1=\begin{bmatrix}1\\-1\end{bmatrix}\). \(\lambda=-2\), \(A+2I=\begin{bmatrix}2&1\\-2&-1\end{bmatrix}\), \(v_2=\begin{bmatrix}1\\-2\end{bmatrix}\). \(P=\begin{bmatrix}1&1\\-1&-2\end{bmatrix}\), \(\det P=-1\), \(P^{-1}=\begin{bmatrix}2&1\\-1&-1\end{bmatrix}\). Then \(P^{-1}x_0=\begin{bmatrix}2\\-1\end{bmatrix}\), so \(z(t)=\begin{bmatrix}2e^{-t}\\-e^{-2t}\end{bmatrix}\), \(x(t)=P z= \begin{bmatrix}2e^{-t}-e^{-2t}\\ -2e^{-t}+2e^{-2t}\end{bmatrix}\). Check \(x(0)=\begin{bmatrix}1\\0\end{bmatrix}\) and \(\dot{x}(0)=A x_0=\begin{bmatrix}0\\-2\end{bmatrix}\): derivative at 0 is \(\begin{bmatrix}-2+2\\ 2-4\end{bmatrix}=\begin{bmatrix}0\\-2\end{bmatrix}\). That check catches 90% of modal-algebra bugs.

Cayley–Hamilton computation of \(e^{At}\) for the same \(A\): \(e^{At}=\alpha_0 I+\alpha_1 A\). On eigenvalues, \(e^{\lambda t}=\alpha_0+\alpha_1\lambda\). So \(e^{-t}=\alpha_0-\alpha_1\), \(e^{-2t}=\alpha_0-2\alpha_1\). Solve \(\alpha_0=2e^{-t}-e^{-2t}\), \(\alpha_1=e^{-t}-e^{-2t}\). Then \(e^{At}=(2e^{-t}-e^{-2t})I+(e^{-t}-e^{-2t})A\). Multiply by \(x_0\) and recover the same \(x(t)\). For a repeated eigenvalue with a Jordan block, the scalar system \(\dot{\alpha}=M\alpha\) uses \(e^{\lambda t}\) and \(t e^{\lambda t}\) as the two conditions (value and derivative of the interpolant).

Forced step with this \(A\), \(B=\begin{bmatrix}0\\1\end{bmatrix}\), \(u=1\), \(x(0)=0\): \(x_{ss}=-A^{-1}B\). \(A^{-1}=\frac{1}{2}\begin{bmatrix}-3&-1\\2&0\end{bmatrix}\), \(A^{-1}B=\frac{1}{2}\begin{bmatrix}-1\\0\end{bmatrix}\), \(x_{ss}=\begin{bmatrix}1/2\\0\end{bmatrix}\). Transient \(x_h(0)=-x_{ss}\), so \(x(t)=x_{ss}+e^{At}(-x_{ss})\). Output position \(y=x_1\) steps from 0 to 1/2 without overshoot here (overdamped). DC gain of \(G(s)=C(sI-A)^{-1}B\) with \(C=[1,0]\) is \(G(0)=1/2\), matching \(y_{ss}\).

When \(A\) has a zero eigenvalue, say a rigid-body integrator \(A=\begin{bmatrix}0&1\\0&0\end{bmatrix}\), \(e^{At}=\begin{bmatrix}1&t\\0&1\end{bmatrix}\) (the Jordan block at 0). A constant force \(B=\begin{bmatrix}0\\1\end{bmatrix}u\) produces a ramp in velocity and a parabola in position: the convolution integral, not \(A^{-1}\). This is the state-space form of a type-2 plant. Students who invert \(A\) here have already left the problem.

Numerical evaluation: for \(t=0.1\) and \(\|A\|\sim 1\), four terms of the series for \(e^{At}\) are plenty. For \(t=10\) and \(\|A\|\sim 1\), the series is the wrong tool; use diagonalization or a scaling-and-squaring algorithm (what `expm` does). In a hand exam, never sum the series beyond a 2×2 illustration at small \(t\).

Change of basis to modal coordinates is optional for \(G(s)\) but useful for model reduction: drop a column of \(P\) whose \(|\lambda|\) is huge and whose residue \(C v\cdot w^\top B\) is tiny, and call the rest a reduced plant. Residualization (set \(\dot{x}_{\mathrm{fast}}=0\)) is more accurate at DC than truncation (delete the state). UG control labs that reduce a 4th-order motor-plus-flexure to a 2nd-order dominant pair are doing this, often without writing \(P\).
