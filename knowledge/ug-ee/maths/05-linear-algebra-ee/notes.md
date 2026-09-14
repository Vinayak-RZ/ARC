# Matrices, eigenvalues, and quadratic forms for EE

Linear algebra in a UG EE programme is the language of nodal admittance matrices, state-space models, three-phase transformations, least-squares parameter fits, and small-signal Jacobians. This unit is that language: matrix arithmetic, linear systems \(Ax=b\), rank and invertibility, eigenvalues and eigenvectors, diagonalization, quadratic forms and energy, and the SVD at the level needed to understand condition numbers and least squares. Abstract vector-space axiomatics beyond \(\mathbb{R}^n\) and \(\mathbb{C}^n\) are kept short. Infinite-dimensional operator theory is out of scope.

Numbers in this course are real or complex. Circuit matrices at DC are real; phasor nodal matrices \(Y(j\omega)\) are complex symmetric (not Hermitian) for reciprocal networks, and Hermitian only in special lossless cases after a \(j\) factor. State matrices \(A\) of passive linear RLC models are not symmetric in physical coordinates, but an energy inner product can make them dissipative. Those distinctions matter when a theorem assumes symmetry.

## Concepts

A matrix \(A\in\mathbb{C}^{m\times n}\) maps \(x\in\mathbb{C}^n\) to \(Ax\in\mathbb{C}^m\). Composition of maps is matrix multiplication, which is not commutative: \(AB\neq BA\) in general, even when both products exist. The identity \(I\) satisfies \(AI=IA=A\). The inverse \(A^{-1}\) exists for square \(A\) if and only if \(\det A\neq 0\), equivalently all eigenvalues nonzero, equivalently \(\operatorname{rank} A=n\), equivalently \(Ax=0\) implies \(x=0\). Solving \(Ax=b\) then has the unique solution \(x=A^{-1}b\). Never compute the inverse to solve one right-hand side; factor \(A\) (LU, Cholesky if SPD) and apply the factors. The inverse is a theoretical object and a formula in \(2\times 2\) exams.

Rank is the dimension of the column space, equal to the dimension of the row space. Rank-deficient circuit matrices appear when a loop of voltage sources or a cutset of current sources is written without a gauge (ground) condition, or when two floating subcircuits are not joined. The linear dependence is physical: KCL at all nodes including the reference is redundant. Dropping one KCL equation, or adding a ground, restores full rank.

The transpose \(A^T\) and conjugate transpose (Hermitian adjoint) \(A^H=\overline{A}^T\) swap roles of rows and columns. For real matrices they coincide. A real symmetric matrix \(A^T=A\) has real eigenvalues and an orthonormal basis of eigenvectors: \(A=Q\Lambda Q^T\) with \(Q^T Q=I\). A complex Hermitian matrix \(A^H=A\) has the same property with \(Q^H Q=I\). A real nonsymmetric matrix may have complex eigenvalues (the underdamped \(2\times 2\) companion matrix of an RLC circuit). Orthogonal diagonalization is then impossible over the reals; real canonical form uses \(2\times 2\) rotation-scaling blocks.

Eigenvalues solve \(\det(A-\lambda I)=0\) (or \(\det(\lambda I-A)=0\); pick one and stay with it). Eigenvectors satisfy \(Av=\lambda v\), \(v\neq 0\). They are defined only up to scale; for modal analysis, normalise as convenient (\(\|v\|_2=1\), or first component 1). Distinct eigenvalues of a symmetric matrix give orthogonal eigenvectors automatically. Defective matrices (Jordan blocks) appear in critically damped repeated-root systems written in some coordinates; they are the linear-algebra name of the \(t e^{\lambda t}\) term in unit 02.

The matrix exponential \(e^{At}\) of unit 02 is computed from the eigenstructure when \(A\) is diagonalizable: \(e^{At}=P e^{\Lambda t} P^{-1}\). Cayley–Hamilton says \(A\) satisfies its own characteristic polynomial, so high powers of \(A\) reduce to a basis \(\{I,A,\ldots,A^{n-1}\}\) and \(e^{At}\) is a polynomial in \(A\) with scalar coefficients that solve a linear system from the scalar exponential interpolating the eigenvalues (and derivatives at repeats).

Quadratic forms \(x^T A x\) with real symmetric \(A\) are the energy expressions: magnetic energy \(\tfrac12 i^T L i\) for a positive definite inductance matrix, electric energy \(\tfrac12 v^T C v\), dissipation \(i^T R i\). Positive definite means \(x^T A x>0\) for all \(x\neq 0\), equivalently all eigenvalues positive, equivalently all leading principal minors positive (Sylvester). Positive semidefinite allows a kernel: a loop of inductors with no resistance can store energy that is invariant along a circulating combination. Completing the square and congruence \(A=R^T R\) (Cholesky) are the computational tests used in numerical methods (unit 08).

Least squares: when \(Ax=b\) is overdetermined (\(m>n\), full column rank), the minimizer of \(\|Ax-b\|_2\) solves the normal equations \(A^T A \hat{x}=A^T b\). The residual \(b-A\hat{x}\) is orthogonal to the column space. Ill-conditioning of \(A^T A\) (condition number squared relative to \(A\)) is why QR or SVD is preferred numerically. In EE this is fitting a Thévenin model to measurements, or estimating phasor amplitude and phase from samples.

The singular value decomposition \(A=U\Sigma V^T\) (real case) exists for every matrix. Singular values are the square roots of the eigenvalues of \(A^T A\). The largest over the smallest is the 2-norm condition number of a square invertible matrix, \(\kappa_2(A)=\sigma_{\max}/\sigma_{\min}\). A nodal matrix with widely spread time constants is often ill-conditioned; that is a warning about Gaussian elimination without pivoting or about interpreting tiny pivot as “the network is singular.”

Change of basis \(x=P z\) converts \(A\) into \(P^{-1}AP\). Similarity preserves eigenvalues, trace, determinant, and characteristic polynomial. It does not preserve symmetry unless \(P\) is orthogonal (or \(A\) is transformed by congruence \(P^T A P\) for quadratic forms). Mixing similarity and congruence is a common error when diagonalizing an inductance matrix: energy coordinates use congruence, modal coordinates of a state matrix use similarity.

The trace \(\operatorname{tr}A=\sum a_{ii}=\sum\lambda_i\) and \(\det A=\prod\lambda_i\) give quick checks. For a \(2\times 2\) companion matrix \(\begin{pmatrix}0&1\\-b&-a\end{pmatrix}\), trace \(-a\) is minus the damping coefficient and det \(b\) is \(\omega_n^2\).

Kronecker products and large multi-machine systems are postgraduate. Three-phase symmetrical-component transforms are \(3\times 3\) (or \(6\times 6\) with inverses) unitary or nearly unitary matrices; they diagonalize balanced circulant impedance matrices. That is eigenvalues of a circulant: the DFT matrix. The same idea reappears as the DFT in signals.

Inner products \(\langle x,y\rangle=y^H x\) (maths convention varies on which argument is conjugated; EE often writes \(x^H y\)) define orthogonality and orthogonal projections. Fourier series of unit 04 is an infinite-dimensional inner-product expansion. Finite least squares is the same geometry in \(\mathbb{R}^m\).

## Equations

Linear system and inverse (\(2\times 2\)):

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\quad \det A=ad-bc,\quad A^{-1}=\frac{1}{\det A}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}\ (\det A\neq 0).
\]

Eigenvalue problem:

\[
Av=\lambda v,\quad \det(A-\lambda I)=0.
\]

Diagonalization (when \(P=[v_1\ \cdots\ v_n]\) invertible):

\[
A=P\Lambda P^{-1},\qquad e^{At}=P\operatorname{diag}(e^{\lambda_i t})P^{-1}.
\]

Cayley–Hamilton: if \(\chi(\lambda)=\det(\lambda I-A)=\lambda^n+\cdots+a_0\), then \(\chi(A)=0\).

Quadratic form, real symmetric \(A\):

\[
q(x)=x^T A x,\qquad A \succ 0\ \iff\ \text{all }\lambda_i(A)>0.
\]

Normal equations (full column rank \(A\)):

\[
A^T A\hat{x}=A^T b,\qquad \hat{x}=(A^T A)^{-1}A^T b.
\]

SVD and 2-norm:

\[
A=U\Sigma V^T,\qquad \|A\|_2=\sigma_{\max},\qquad \kappa_2(A)=\frac{\sigma_{\max}}{\sigma_{\min}}\ (A\text{ invertible}).
\]

Trace and determinant:

\[
\operatorname{tr}A=\sum_i\lambda_i,\qquad \det A=\prod_i\lambda_i.
\]

Orthogonal projector onto the column space of full-rank \(A\):

\[
P_A=A(A^T A)^{-1}A^T.
\]

## Methods

To solve \(Ax=b\) by hand for \(n\le 3\), use elimination and keep a clear augmented matrix. Record the determinant as a check: if it is tiny compared with the entries, treat the answer as sensitive. For a \(2\times 2\) symbolic impedance matrix, use the inverse formula and simplify before substituting numbers.

To find eigenvalues of \(2\times 2\), solve \(\lambda^2-(\operatorname{tr}A)\lambda+\det A=0\). For \(3\times 3\), expand \(\det(A-\lambda I)\) along a convenient row, or use known structure (triangular matrices have eigenvalues on the diagonal; companion matrices have characteristic polynomial read from the last row).

To find an eigenvector, row-reduce \(A-\lambda I\) and read the nullspace. Do not be surprised if one row becomes zero: that is the dependence \(\det=0\). If both rows vanish, the whole space is eigenspace (multiple of \(I\)).

To test positive definiteness of a real symmetric \(2\times 2\), check \(a_{11}>0\) and \(\det A>0\). For larger matrices, eigenvalues or Cholesky (failure of Cholesky means not SPD). Energy matrices \(L,C,R\) assembled from passive elements should pass; if they do not, the stamp is wrong.

For least squares with two columns (fit \(y\approx \alpha+\beta u\)), form \(A=[1\ u]\) (column of ones and the samples of \(u\)), compute \(A^T A\) (Gram matrix of sums), and solve the \(2\times 2\) normal system. Plot residuals if the context is a lab fit; a systematic sinusoid in the residual means a missing harmonic column.

To compute \(e^{At}\) for diagonalizable \(2\times 2\), find \(P,\Lambda\), invert \(P\) (adjugate over det), multiply. Check \(e^{A\cdot 0}=I\) and \(\frac{d}{dt}e^{At}|_{0}=A\).

When a problem gives a change of coordinates for a three-phase set (Clarke, Park, Fortescue), identify whether the transform is unitary (\(T^{-1}=T^H\)) or scaled for power invariance. Power-invariant forms preserve \(v^T i\). Mixing amplitude-invariant Clarke with a power-invariant inverse drops a factor of \(3/2\).

Use \(\|Ax\|\le \|A\|_2\|x\|\) only as a bound. Equality holds along the top right singular vector. For a quick exam bound without SVD, the Frobenius norm \(\|A\|_F=\sqrt{\sum a_{ij}^2}\) satisfies \(\|A\|_2\le\|A\|_F\).

## Mistakes

Writing \(A^{-1}=1/A\) or inverting elementwise. Elementwise reciprocal is not the inverse except for \(1\times 1\) and some diagonal cases.

Assuming every matrix with real entries has real eigenvalues. Rotation \(\begin{pmatrix}0&-1\\1&0\end{pmatrix}\) has \(\pm j\).

Assuming every matrix is diagonalizable. A single Jordan block of size 2 is not.

Using \(P^T A P\) when the problem is a similarity of a state matrix, or \(P^{-1}AP\) when the problem is a quadratic-form change of basis for energy. The second does not preserve eigenvalues in general.

Solving least squares by dropping equations until \(A\) is square. That discards data; use normal equations or QR.

Forgetting to conjugate-transpose when the matrix is complex: power in a phasor network is \(v^H i\) with RMS phasors in some conventions, or \(\operatorname{Re}(v^H i)\). Using \(v^T i\) on complex vectors misses conjugation.

Checking \(\det A\neq 0\) numerically with a noisy matrix of condition \(10^{12}\) and declaring invertibility because the computed det was \(10^{-8}\) in float. Look at \(\kappa\) or the smallest singular value relative to the largest.

Normalising eigenvectors inconsistently between \(P\) and \(P^{-1}\) in a numerical example and then reporting \(P P^{-1}\neq I\) as a mystery.

Taking \(\sqrt{A}\) elementwise for a covariance or an inductance. A SPD square root is \(Q\sqrt{\Lambda}Q^T\).

Writing the characteristic polynomial as \(\det(A-\lambda I)\) in one line and \(\det(\lambda I-A)\) in the next, flipping the sign of odd-powered terms, then reading Routh signs wrong in a later control course.

Stamping a nodal matrix with the reference node still included so that \(Y\mathbf{1}=0\), then asking for \(Y^{-1}\). The all-ones kernel is the floating potential; ground a node first.
