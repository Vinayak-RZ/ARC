# Routh array and parameter range

Hurwitz stability of a linear time-invariant system is “every root of the characteristic polynomial lies in the open left half-plane.” Computing those roots is unnecessary for the yes/no and for a gain range: the Routh array turns coefficient conditions into a table whose first-column signs count RHP roots. This unit is construction of the array, the two degeneracies (zero in the first column, entire zero row), auxiliary polynomials for \(j\omega\) roots, and the standard UG task of finding \(K\) such that \(1+KG(s)=0\) is stable.

## Concepts

A polynomial \(p(s)=a_n s^n+\cdots+a_0\) with real coefficients has Hurwitz stability if and only if every root satisfies \(\mathrm{Re}\,s<0\). Necessary conditions (not sufficient): every \(a_k>0\) or every \(a_k<0\) (we normalize \(a_n>0\) and then require all \(a_k>0\)); no missing powers unless a root at 0 is intended (a root at 0 is not strictly Hurwitz). A quadratic \(s^2+a s+b\) is Hurwitz iff \(a>0\) and \(b>0\). A cubic \(s^3+a s^2+b s+c\) needs \(a,b,c>0\) and \(ab>c\). Higher degrees need Routh or an equivalent Hurwitz determinant test.

The Routh array has \(n+1\) rows labelled \(s^n,s^{n-1},\ldots,s^0\). Row \(s^n\) is \(a_n, a_{n-2}, a_{n-4},\ldots\). Row \(s^{n-1}\) is \(a_{n-1}, a_{n-3},\ldots\). Each following row is formed from the two rows above by 2×2 determinants. If the first-column entry of the row above is \(c\), the new row’s first entry is \(-\frac{1}{c}\det\begin{bmatrix}r_{11}&r_{12}\\r_{21}&r_{22}\end{bmatrix}\) using the first two columns of those two rows, and similarly shifting columns. Many textbooks write the same thing as
\[
b_1=\frac{c_1 d_2-c_2 d_1}{c_1}
\]
with a sign convention that already includes the minus. Compute one 2×2 slowly on every exam until the pattern is muscle memory. The last row \(s^0\) is a single entry equal to \(a_0\) (or a multiple of it).

The number of sign changes in the first column equals the number of RHP roots (Routh–Hurwitz). LHP roots do not produce sign changes. Simple \(j\omega\) roots are a marginal case handled by a zero row, not by a sign change.

Degeneracy A: a zero in the first column but the rest of that row not all zero. Replace the zero by a small \(\varepsilon>0\) (or \(\varepsilon\) with unknown sign), continue, and let \(\varepsilon\to 0^+\). Sign changes that depend on \(\varepsilon\) are counted in the limit. An equivalent method replaces the zero by a tiny number and uses a computer; by hand, \(\varepsilon\) is cleaner. Another equivalent: substitute \(s=1/z\) and reverse coefficients, which often moves the zero (the reversed polynomial’s roots are reciprocals).

Degeneracy B: an entire row of zeros. This signals roots that are symmetric across the origin (pairs \(\pm r\), \(\pm j\omega\), or quadrants). The row above the zero row is used to form an auxiliary polynomial \(A(s)\), even powers (or odd, matching that row’s degree). Replace the zero row by the coefficients of \(dA/ds\). Continue. The auxiliary polynomial is a factor of \(p(s)\); its roots include the \(j\omega\) pair if the system is marginally stable. To test marginal stability, factor \(A(s)\) and check that those roots are simple on the \(j\omega\) axis and that the rest of the array has no sign change.

Parameter ranges. Characteristic equation \(s^n+\cdots+K=0\) or \(1+K G(s)=0\) produces some first-column entries that are affine in \(K\). Demand every first-column entry positive (given \(a_n>0\)) and solve the inequalities. Intersect with \(K>0\) if the gain is physically positive. Boundary values that make a first-column entry zero are the onset of \(j\omega\) crossing or a root through infinity; they are not interior to the strict Hurwitz set. At a zero first-column entry caused by \(K=K_u\), form the auxiliary polynomial from the previous row to get \(\omega_u\) for Ziegler–Nichols (unit 08).

Relative stability: replacing \(s\) by \(s+\alpha\) and applying Routh tests whether all roots satisfy \(\mathrm{Re}\,s<-\alpha\). Useful as a settling-time constraint \(\zeta\omega_n>\alpha\) for a dominant pair, applied to the whole polynomial (conservative if other poles are slower).

Discrete-time Jury test is not Routh; do not apply Routh to \(z\)-polynomials without the bilinear map. After \(z=(1+w)/(1-w)\), Routh on \(w\) is a possible UG method for digital characteristic polynomials (unit 11).

Routh does not give root locations beyond the RHP count and the auxiliary \(j\omega\) roots. For damping, use root locus or compute roots.

A pole–zero cancelled unstable mode in a TF does not appear in a cancelled characteristic polynomial. Apply Routh to \(\det(sI-A)\) or to \(1+L\) *before* cancelling RHP factors.

## Equations

Polynomial:
\[
p(s)=a_n s^n+a_{n-1}s^{n-1}+\cdots+a_0,\qquad a_n>0.
\]
Necessary: \(a_k>0\) for all \(k\).

Routh row construction (rows \(R_{i-2}\), \(R_{i-1}\) → \(R_i\)), first-column pivot \(p=R_{i-1,1}\):
\[
R_{i,j}=-\frac{1}{p}\det\begin{bmatrix}R_{i-2,1}&R_{i-2,j+1}\\R_{i-1,1}&R_{i-1,j+1}\end{bmatrix}.
\]

Cubic necessary and sufficient (\(s^3+a s^2+b s+c\), \(a>0\)):
\[
a>0,\; b>0,\; c>0,\; ab>c.
\]

Auxiliary polynomial from the \(s^{k}\) row \((c_0,c_1,c_2,\ldots)\):
\[
A(s)=c_0 s^{k}+c_1 s^{k-2}+c_2 s^{k-4}+\cdots.
\]
Zero-row replacement: coefficients of \(A'(s)\).

Closed-loop characteristic polynomial of unity negative feedback:
\[
p(s)=\mathrm{den}(L)+\mathrm{num}(L).
\]

Relative stability shift:
\[
p(s+\alpha)\ \text{Hurwitz}\iff \text{all roots of }p\text{ have }\mathrm{Re}<-\alpha.
\]

## Methods

Write \(p(s)\) with \(a_n>0\). If any coefficient is zero or negative, it is already not strictly Hurwitz (except the zero-row case after you still build the array to count RHP roots). Build two starter rows. Compute downward. Count first-column sign changes. Report that number as RHP roots.

For a parameter \(K\), keep \(K\) symbolic in the array. Each first-column entry \(>0\) is an inequality. Sketch the intersection on a \(K\)-line. Test a point inside the interval by plugging a number if the inequalities are messy.

When a first-column zero appears at a specific \(K\), that \(K\) is a boundary. Form \(A(s)\) from the row above, set \(A(j\omega)=0\), get \(\omega\). Those are the crossing frequencies of the root locus or the Nyquist \(-1\) hit.

Zero in first column only: replace by \(\varepsilon\), or multiply \(p(s)\) by \((s+1)\) to bump coefficients (a legal trick that adds a known LHP root and can remove a first-column zero). Reverse polynomial if that is shorter.

Always cross-check a cubic with \(ab>c\). Always cross-check a quadratic with both coefficients positive. If Routh disagrees, an arithmetic error in a determinant is almost certain.

For \(1+KG(s)=0\) with \(G=n/d\), \(p=d+K n\). Do not Routh on \(d\) (open-loop) when the question is closed-loop.

Document every 2×2. The standard slip is to use the wrong column pair or to drop the minus, which flips every even row and can flip the sign-change count.

If the question asks “number of roots in the RHP” and the array has a zero row, complete the auxiliary procedure first; some roots may be on \(j\omega\) (not RHP). Simple \(j\omega\) roots are not RHP.

## Mistakes

Declaring stability from all coefficients positive on a quartic or higher. Counterexample: \(s^4+s^3+s^2+s+1\) needs an array (this one is actually stable, but \(s^4+s^3+s^2+s+2\) is not — check before quoting). The cubic extra condition \(ab>c\) is the warning that positivity is not enough.

Counting a \(j\omega\) pair as two RHP roots because a first-column entry was zero. Zero row: on the axis, not RHP, if simple.

Using Routh on the numerator of \(G\), or on the open-loop denominator only.

Forgetting that \(K<0\) can still make first-column entries positive in some problems; if \(K\) is a physical gain, intersect with \(K>0\) only after the problem says so.

Replacing a whole zero row by \(\varepsilon\) instead of forming \(A'(s)\). Different degeneracies, different fixes.

Sign error in the determinant formula, especially the leading minus.

Applying the final-value theorem or \(K_v\) formulas without a Routh check.

Cancelling \((s-2)\) in \(1+L\) and Routhing the reduced polynomial when the plant still has a pole at \(+2\).

Shifting by \(\alpha\) but substituting \(s-\alpha\) instead of \(s+\alpha\) for the left-shift test.

Reporting the range as closed (\(K\ge 0\)) for strict Hurwitz. Equality is the stability boundary, usually not allowed if the spec is asymptotic stability.

A fully numerical cubic walkthrough, of the kind that appears on every midterm: \(p(s)=s^3+5s^2+6s+K\). Array rows \(s^3:\ (1,\ 6)\), \(s^2:\ (5,\ K)\), \(s^1:\ (30-K)/5\), \(s^0:\ K\). First-column positivity: \(K>0\) and \(K<30\). At \(K=30\) the \(s^1\) row vanishes; auxiliary from \(s^2\) is \(5s^2+30=0\), \(\omega=\sqrt{6}\). Factor at the boundary: \(p(s)=(s+5)(s^2+6)\) when \(K=30\), which matches the trace of the \(s^2\) row (the coefficient 5 is the leftover first-order factor). For \(K=12\) (interior), first column \(1,5,18/5,12\), no sign change, three LHP roots. For \(K=40\), \(s^1\) entry negative: two sign changes (\(+\to-\) then \(-\to+\)), two RHP roots and one LHP. That pattern — two RHP at once when a quadratic factor crosses — is what a conjugate pair does; Routh never moves a single real root through \(+j0\) except via \(s=0\) (the \(s^0\) entry). A real root through the origin is \(a_0=0\); a conjugate pair through \(\pm j\omega\) is a zero row or a first-column zero with an auxiliary polynomial of even degree.

Quartic practice: \(s^4+3s^3+4s^2+2s+K\). Compute \(s^2\) first entry \((12-2)/3=10/3\), second entry \(K\). Then \(s^1\) first entry \(\frac{(10/3)\cdot 2-3K}{10/3}=(20/3-3K)\cdot 3/10=(20-9K)/10\). Conditions \(K>0\) and \(20-9K>0\) so \(K<20/9\), and \(10/3>0\) automatically. The upper bound \(K=20/9\) is a \(j\omega\) crossing; auxiliary \( (10/3)s^2+20/9=0\) gives \(\omega^2=(20/9)/(10/3)=2/3\). Use this as a template whenever a problem says “find \(K\) and the frequency of oscillation.”

Routh on \(1+L=0\) when \(L\) is not monic: if \(L=N/D\) with \(\deg D=n\) and \(\deg N<n\), then \(p=D+N\) is still degree \(n\). If \(\deg N=\deg D\) (biproper loop), \(p=(1+D_{\infty})s^n+\cdots\) and the leading coefficient depends on high-frequency loop gain; well-posedness failed if that leading coefficient is zero (\(L(\infty)=-1\)). If \(\deg N>\deg D\), the closed-loop polynomial has degree equal to \(\deg N\) and the “plant” is improper; Routh still applies to whatever polynomial you wrote, but the model is not a lumped causal loop.

When an exam gives a polynomial with a parameter in two coefficients, do not assume the inequalities factor independently without drawing the \(K\)-line. Example: \(s^3+(2+K)s^2+(3)s+(1+K)\). Coefficient positivity already ties \(K>-2\) and \(K>-1\); the cubic product condition \((2+K)\cdot 3>1+K\) is \(6+3K>1+K\) ⇒ \(K>-2.5\), which is weaker than \(K>-1\). The binding range is \(K>-1\). Always list every inequality, then intersect. A number line with open circles at the binding edges is the answer format that survives a sign error in one of the unused inequalities.
