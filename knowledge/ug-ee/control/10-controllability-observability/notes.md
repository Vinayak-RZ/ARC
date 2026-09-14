# Controllability, observability, PBH, canonical forms

Pole placement and observers are possible only when the pair \((A,B)\) is controllable and \((A,C)\) is observable. UG tests are rank tests, the Popov–Belevitch–Hautus (PBH) eigenvalue test, and the standard canonical realizations that make those properties obvious. This unit is those tests, what a loss of controllability means in a cancellation, and the controllable/observable/Jordan forms at exam depth — not LQR or Kalman filters.

## Concepts

Controllability: there exists a finite-time input driving \(x(0)\) to any \(x(T)\) in \(\mathbb{R}^n\). For linear time-invariant systems this is equivalent to the controllability matrix
\[
\mathcal{C}=\begin{bmatrix}B&AB&\cdots&A^{n-1}B\end{bmatrix}
\]
having rank \(n\). SISO: \(\mathcal{C}\) is square; controllability iff \(\det\mathcal{C}\neq 0\). MIMO: \(B\) has \(m\) columns, \(\mathcal{C}\) is \(n\times nm\), rank \(n\) is enough. Controllability is about the pair \((A,B)\), not about \(C\).

Observability: the free output \(y(t)=C e^{At}x_0\) on a finite interval determines \(x_0\) uniquely. Rank test:
\[
\mathcal{O}=\begin{bmatrix}C\\CA\\\vdots\\CA^{n-1}\end{bmatrix}
\]
has rank \(n\). Duality: \((A,C)\) observable iff \((A^\top,C^\top)\) controllable.

PBH controllability: \((A,B)\) is controllable iff
\[
\mathrm{rank}\begin{bmatrix}\lambda I-A& B\end{bmatrix}=n
\]
for every eigenvalue \(\lambda\) of \(A\) (equivalently for every complex \(\lambda\)). Failure at \(\lambda_0\) means that mode is uncontrollable: some left eigenvector \(w^\top A=\lambda_0 w^\top\) also satisfies \(w^\top B=0\). PBH observability: \(\mathrm{rank}\begin{bmatrix}\lambda I-A\\ C\end{bmatrix}=n\) for every eigenvalue.

A pole–zero cancellation in \(G(s)=C(sI-A)^{-1}B\) is an uncontrollable or unobservable mode (or both). If the cancelled pole is in the RHP, the realization is internally unstable even if \(G\) is Hurwitz. Minimal realizations are those that are both controllable and observable; their order equals the degree of the reduced \(G\).

Controllable canonical form (CCF) for SISO:
\[
A_c=\begin{bmatrix}0&1&0&\cdots\\0&0&1&\cdots\\-a_n&\cdots&\cdots&-a_1\end{bmatrix},\quad
B_c=\begin{bmatrix}0\\\vdots\\1\end{bmatrix},\quad
C_c=\begin{bmatrix}b_n&\cdots&b_1\end{bmatrix}.
\]
\(\mathcal{C}\) is triangular-ish and obviously full rank. Pole placement \(u=-Kx\) becomes matching the last row of \(A-BK\) to the desired characteristic polynomial (Ackermann):
\[
K=e_n^\top\mathcal{C}^{-1}\chi_{\mathrm{des}}(A)
\]
in one common convention. UG should be able to place poles on a 2×2 by solving \(A-BK\) entries, not only by quoting Ackermann.

Observable canonical form is the transpose dual: \(A_o=A_c^\top\), \(C_o=B_c^\top\), \(B_o=C_c^\top\) for the same \(G\) (signs and companion orientation matching the course). Observer gain \(L\) places eigenvalues of \(A-LC\).

Jordan (modal) form: a mode is controllable if the corresponding input component (the row of \(P^{-1}B\)) is nonzero; observable if the corresponding column of \(CP\) is nonzero. A zero in that slot is PBH made visible.

Stabilizability: every uncontrollable mode is already Hurwitz. Detectability: every unobservable mode is Hurwitz. You can still close a stable loop if the junk you cannot move is stable. You cannot stabilize an unstable uncontrollable mode.

Kalman decomposition (UG statement): a similarity splits the state into four parts: co, c\(\bar{\mathrm{o}}\), \(\bar{\mathrm{c}}\)o, \(\bar{\mathrm{c}}\bar{\mathrm{o}}\). Only the co part appears in \(G(s)\).

PBH is often faster than forming \(\mathcal{C}\) when \(A\) is diagonal or 2×2 with an obvious eigenvector.

Inputs that are not the actuator (disturbances) have their own \(B_d\); controllability from \(u\) does not mean controllability from \(d\).

## Equations

Rank tests: \(\mathrm{rank}\,\mathcal{C}=n\), \(\mathrm{rank}\,\mathcal{O}=n\).

PBH:
\[
\mathrm{rank}[\lambda I-A,\ B]=n,\qquad
\mathrm{rank}\begin{bmatrix}\lambda I-A\\C\end{bmatrix}=n
\quad\forall\lambda\in\sigma(A).
\]

Ackermann (SISO, one convention):
\[
K=\begin{bmatrix}0&\cdots&0&1\end{bmatrix}\mathcal{C}^{-1}\phi(A),
\]
\(\phi\) the desired characteristic polynomial.

Bass–Gura / last-row: in CCF, \(K=(\alpha_{\mathrm{des}}-\alpha_{\mathrm{open}})\) aligned with the companion last row.

Popov: the uncontrollable subspace is the largest \(A\)-invariant subspace in \(\ker\) of the map involving \(B\) — skip at UG beyond “left eigenvector ⊥ columns of \(B\)”.

## Methods

To test controllability of a numerical 2×2: form \(B,AB\), check whether they are linearly independent (\(\det[B,AB]\neq 0\)). Same for \(\mathcal{O}\). If \(A\) is diagonal, PBH: look at each \(B\) component; a zero component next to a distinct eigenvalue is uncontrollability of that mode.

To build CCF from \(G(s)\): read coefficients of the monic denominator into the last row, numerator into \(C\). Verify \(C(sI-A)^{-1}B=G\).

To place poles of a controllable 2×2: let \(K=[k_1,k_2]\), form \(\det(sI-A+BK)\), equate to \(s^2+2\zeta\omega_n s+\omega_n^2\), solve the two equations. Check the closed-loop Routh as a sanity pass.

If rank \(\mathcal{C}=n-1\), find the left null vector \(w^\top\mathcal{C}=0\); then \(w^\top B=0\) and \(w\) identifies the uncontrollable direction. Projecting the dynamics onto \(w\) gives the uncontrollable eigenvalue \(w^\top A\) relative to \(w\).

Do not try to place poles of an uncontrollable pair. The algebra will be inconsistent (or will appear to work if you only match the characteristic polynomial of a non-minimal realization you already cancelled).

Observer duality: copy the controllable design on \((A^\top,C^\top)\), then transpose the gain.

Worked PBH versus \(\mathcal{C}\) on a nondiagonal pair. \(A=\begin{bmatrix}0&1\\-2&-3\end{bmatrix}\), \(B=\begin{bmatrix}1\\-1\end{bmatrix}\). Eigenvalues \(-1,-2\). \(AB=\begin{bmatrix}-1\\1\end{bmatrix}=-B\), so \(\mathcal{C}=[B,AB]\) has rank 1: uncontrollable. PBH at \(\lambda=-1\): \(\lambda I-A=\begin{bmatrix}-1&-1\\2&2\end{bmatrix}\), adjacent to \(B=\begin{bmatrix}1\\-1\end{bmatrix}\). Rows are dependent if the stacked matrix drops rank: first row \((-1,-1,1)\), second \((2,2,-1)\) — wait second is not −2 times the first because of the \(B\) column (\(1\) vs \(-1\)). Rank of \([\lambda I-A,\ B]\) at \(-1\): \(\lambda I-A\) already has rank 1 (repeated rows up to sign). The extra column \(B=[1,-1]^\top\) is not in the column space of \(\lambda I-A=\begin{bmatrix}-1&-1\\2&2\end{bmatrix}\) whose columns are multiples of \([-1,2]^\top\). Is \([1,-1]^\top\) a multiple of \([-1,2]^\top\)? No. So rank is 2 at \(\lambda=-1\). At \(\lambda=-2\): \(\lambda I-A=\begin{bmatrix}-2&-1\\2&1\end{bmatrix}\), columns multiples of \([-2,2]^\top\). \(B=[1,-1]^\top=-0.5[-2,2]^\top\), in that span, so \([\lambda I-A,\ B]\) still rank 1. Uncontrollable mode is \(-2\), not \(-1\). The lesson: \(\mathcal{C}\) rank tells you a loss exists; PBH tells you which eigenvalue.

After finding that mode, a left eigenvector \(w^\top(A+2I)=0\) with \(w^\top B=0\) is \(w^\top\propto [1,1]\) because \((A+2I)=\begin{bmatrix}2&1\\-2&-1\end{bmatrix}\) has rows multiples of \([2,1]\), so left kernel is orthogonal to \([2,1]\) in the row sense... actually left eigenvectors satisfy \(w^\top A=\lambda w^\top\). For \(\lambda=-2\), \(w^\top(A+2I)=0\). \(A+2I=\begin{bmatrix}2&1\\-2&-1\end{bmatrix}\), rows parallel, \(w^\top\) must kill both columns: columns are multiples of \([1,-1]^\top\), so \(w^\top[1,-1]^\top=0\) ⇒ \(w_1=w_2\), \(w=[1,1]^\top\). And \(w^\top B=1-1=0\), confirming PBH. The uncontrollable state combination is \(w^\top x=x_1+x_2\), which evolves as \(\frac{d}{dt}(x_1+x_2)=-2(x_1+x_2)\) with no \(u\).

## Mistakes

Testing rank of \(B\) only (that is “instantaneous reach of \(n\) directions,” false for \(m<n\)).

Using \(\mathcal{C}\) with the wrong number of columns (stopping at \(A^{n-2}B\)).

Declaring a system uncontrollable because \(G(s)\) has degree less than \(n\) without checking that the realization is non-minimal — that is the definition of a cancellation, which is exactly lost c/o.

Applying Ackermann to a MIMO \(B\) with two columns without the extra structure.

PBH at a value \(\lambda\) that is not an eigenvalue and concluding uncontrollability from a rank drop that does not happen — PBH only constrains eigenvalues. (For \(\lambda\) not an eigenvalue, \(\lambda I-A\) is already rank \(n\).)

Placing observer poles slower than controller poles and then blaming controllability for a slow estimate. Observer poles should be somewhat faster (rule of thumb 2–5×), not slower.

Forgetting that similarity \(T\) requires \(\bar{B}=TB\), \(\bar{C}=CT^{-1}\) when transforming to CCF. Using \(C\) untransformed with \(A_c\) gives the wrong \(G\).

Stabilizing by cancelling a RHP plant pole with a controller zero: the closed-loop TF looks fine; the uncontrollable/unobservable cancelled mode is still there if it was in the plant.

Checking \(\det A\neq 0\) as a controllability test. Invertibility of \(A\) is about type number / equilibrium uniqueness, not controllability.

A 2×2 numerical that should be computed every semester. \(A=\begin{bmatrix}-2&0\\1&-3\end{bmatrix}\), \(B=\begin{bmatrix}1\\0\end{bmatrix}\), \(C=\begin{bmatrix}0&1\end{bmatrix}\). Then \(AB=\begin{bmatrix}-2\\1\end{bmatrix}\), \(\mathcal{C}=\begin{bmatrix}1&-2\\0&1\end{bmatrix}\), \(\det=1\neq 0\), controllable. \(\mathcal{O}=\begin{bmatrix}0&1\\1&-3\end{bmatrix}\), \(\det=-1\neq 0\), observable. \(G(s)=1/[(s+2)(s+3)]\), degree 2, minimal. If instead \(B=\begin{bmatrix}0\\1\end{bmatrix}\), \(AB=\begin{bmatrix}0\\-3\end{bmatrix}\), \(\mathcal{C}\) has both columns in \(\mathrm{span}\{e_2\}\), rank 1: the first state (mode \(-2\)) is not fed by \(u\). PBH at \(\lambda=-2\): \([\lambda I-A,\ B]=\begin{bmatrix}0&0&0\\-1&1&1\end{bmatrix}\), rank 1. That is the picture of an uncontrollable stable mode: you can still have a nice \(G(s)=1/(s+3)\) and a hidden \(e^{-2t}\) that initial conditions can excite.

Pole placement on a controllable companion pair is matching the last row. Open-loop last row of \(A\) is \([-a_0,-a_1]\) for the monic polynomial \(s^2+a_1 s+a_0\). Feedback \(K=[k_0,k_1]\) replaces it by \([-a_0-k_0,-a_1-k_1]\). Desired \(s^2+\alpha_1 s+\alpha_0\) needs \(k_0=\alpha_0-a_0\), \(k_1=\alpha_1-a_1\). If the realization is not already companion, either transform with the controllability matrix (the map to CCF uses \(\mathcal{C}\) and the companion \(\mathcal{C}_c\)) or expand \(\det(sI-A+BK)\) in the original coordinates, which is two scalar equations in two unknowns for \(n=2\). For \(n=3\), three unknowns in \(K\), still doable by equating coefficients; beyond that, Ackermann or a named algorithm.

Observer placement is the same arithmetic on \(A-LC\). Separation principle (UG statement): if \(u=-K\hat{x}\) and \(\dot{\hat{x}}=A\hat{x}+Bu+L(y-C\hat{x})\), the closed-loop eigenvalues are the union of those of \(A-BK\) and those of \(A-LC\). You may place them independently *provided* the pair is controllable and observable. You may not place an uncontrollable eigenvalue, and you may not observe an unobservable one. A common lab: place controller poles at \(-2\pm j2\), observer poles at \(-6\pm j6\), then watch that the step of \(y\) looks like the slower controller pair once the observer transient dies.

PBH for a 3×3 diagonal \(A=\mathrm{diag}(-1,-2,-5)\), \(B=[1,1,0]^\top\): the third channel of \(B\) is zero, so \(\lambda=-5\) fails PBH. Adding even a tiny \(B_3=\varepsilon\) restores rank; controllability is a yes/no that is structurally fragile when a coupling is “almost” zero. In a physical schematic, that “almost” is a missing actuator on that energy storage.

Kalman split in one picture: take a 3rd-order realization of a 1st-order \(G\). Two eigenvalues are cancelled. One cancelled eigenvalue might be uncontrollable (a motor winding you cannot reach), the other unobservable (a sensor that cannot see a vibration mode). \(G(s)\) is the co part only. Internal stability needs all four blocks Hurwitz, not just co.

When forming \(\mathcal{C}\) for MIMO, two columns of \(B\) at a time: rank can be \(n\) even if each column alone is not a cyclic generator. A satellite with two thrusters may be controllable with both and uncontrollable with one. Do not test a single column and declare the pair uncontrollable unless \(m=1\).
