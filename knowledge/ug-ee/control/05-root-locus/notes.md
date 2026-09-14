# Root locus: rules, departure, design sketch

The Evans root locus is the path of closed-loop poles as a real gain \(K\) varies from 0 to \(\infty\) in \(1+K G_{\mathrm{ol}}(s)=0\), or equivalently \(G_{\mathrm{ol}}(s)=-1/K\). For UG design it is a sketching tool: enough geometry to place a dominant pair, to see a breakaway, and to read a \(j\omega\) crossing without computing every point. This unit is the angle and magnitude conditions, the standard construction rules, angles of departure and arrival, and the one-parameter design sketch (gain from a point, not a lead compensator — that is unit 08).

## Concepts

Write the characteristic equation as
\[
1+K\frac{n(s)}{d(s)}=0\qquad\Leftrightarrow\qquad d(s)+K n(s)=0
\]
with \(K\ge 0\) the usual Evans parameter. The open-loop poles are the roots of \(d\); the open-loop zeros are the roots of \(n\). On the locus,
\[
\angle G_{\mathrm{ol}}(s)=(2q+1)180^\circ,\qquad |K|=1/|G_{\mathrm{ol}}(s)|
\]
(the odd-multiple of 180° is the negative-real mapping). The complementary 0° locus (\(K\le 0\)) exists but is a different sketch; exams mean the 180° locus unless they say otherwise.

Number of branches equals the number of open-loop poles \(n\) (finite zeros \(m\le n\)). As \(K\to 0\), branches start at open-loop poles. As \(K\to\infty\), \(m\) branches end at finite zeros and \(n-m\) branches go to infinity along asymptotes.

Asymptotes: centroid
\[
\sigma_a=\frac{\sum p_i-\sum z_j}{n-m},
\]
angles
\[
\phi_q=\frac{(2q+1)180^\circ}{n-m},\qquad q=0,\ldots,n-m-1.
\]
For \(n-m=1\), one asymptote at 180° (the negative real axis). For \(n-m=2\), \(\pm 90^\circ\) (vertical). For \(n-m=3\), \(60^\circ,180^\circ,300^\circ\).

Real-axis rule: a point on the real axis is on the 180° locus iff the total number of real poles and zeros to its right is odd. Complex pairs do not affect the real-axis occupancy (they come in conjugates). This rule is the fastest part of the sketch and the most graded.

Breakaway / break-in: points where two real branches meet and split (or join). They satisfy \(dK/ds=0\) with \(K=-1/G_{\mathrm{ol}}(s)\) along the real axis, equivalently
\[
\sum\frac{1}{\sigma+p_i}=\sum\frac{1}{\sigma+z_j}
\]
at a real \(\sigma\) that already lies on the locus. For two poles at 0 and \(-a\) and no zero, breakaway at \(-a/2\). Always check that the candidate is on the real-axis locus; extra roots of \(dK/ds=0\) can be off-axis or off-locus.

Imaginary crossing: substitute \(s=j\omega\) into \(1+K G_{\mathrm{ol}}=0\) and separate real/imaginary, or Routh: the \(K_u\) that zeros a first-column entry, then the auxiliary polynomial gives \(\omega_u\). Mark \(\pm j\omega_u\) and the gain \(K_u\). If there is no crossing, the locus may stay in the LHP for all \(K>0\) (as in \(K/(s(s+2)(s+8))\) wait — that one does cross; \(K/(s(s+2))\) does not).

Angle of departure from a complex open-loop pole: \(180^\circ\) minus the net angle of the vectors from all other poles and zeros to that pole (zeros contribute \(+\), poles \(-\), then the departure is the leftover to make the total odd-π). Angle of arrival at a complex zero is analogous with the roles swapped. These angles set how the branch leaves a lightly damped plant pair.

A test point \(s_0\) is on the locus iff the angle condition holds; then \(K=1/|G_{\mathrm{ol}}(s_0)|\). Design sketch: draw the \(\zeta\) rays (lines at \(\cos^{-1}\zeta\) from the negative real axis) and the vertical settle line \(\mathrm{Re}=-\sigma\). A point on both the locus and those constraints is a candidate dominant pair; read \(K\) from the magnitude condition. If the locus never meets the \(\zeta\) ray, proportional gain cannot meet that damping — use lead (unit 08).

Zeros pull; poles push. Adding a zero (PD, lead) bends branches left. Adding a pole (PI, lag) bends them right. A dipole (lag) near the origin barely changes the high-frequency locus but raises \(K_v\).

Multiplicity: a double pole on the real axis has two 180° departures, typically ±90° from the axis if the local neighbourhood is two coinciding poles and the rest of the angle is 180°. Compute if needed; do not guess.

The locus of \(1+K G=0\) is not the locus of closed-loop zeros. Closed-loop zeros of \(T=KG/(1+KG)\) in unity feedback are the zeros of \(G\) (and poles of the complementary sensitivity are the closed-loop poles). Do not mark open-loop zeros as closed-loop poles.

## Equations

Angle / magnitude:
\[
\angle G_{\mathrm{ol}}(s)=\pi\pmod{2\pi},\qquad K=\frac{1}{|G_{\mathrm{ol}}(s)|}.
\]

Asymptote centroid and angles: as above.

Breakaway on the real axis: \(\frac{dK}{ds}=0\) with \(K=-d(s)/n(s)\).

Routh crossing: \(p(s)=d(s)+K n(s)\); \(K_u\) from a vanishing Routh entry; \(\omega_u\) from \(A(j\omega)=0\).

Departure from pole \(p_k\):
\[
\theta_{\mathrm{dep}}=\sum_j\angle(p_k-z_j)-\sum_{i\neq k}\angle(p_k-p_i)-180^\circ
\]
(mod 360°, and the 180° is one odd multiple; if several branches, other odd multiples).

Damping ray: \(\zeta=\cos\theta\) where \(\theta\) is the angle from the negative real axis to the pole.

## Methods

Construction order that graders expect: (1) plot finite poles (×) and zeros (○); (2) real-axis segments; (3) \(n,m\), centroid, asymptotes; (4) breakaway by \(dK/ds=0\) or by inspection; (5) \(j\omega\) crossing by Routh; (6) departure angles if complex poles exist; (7) light sketch of branches consistent with all of the above; (8) if a design point is named, check the angle condition and compute \(K\).

To compute \(K\) at a point \(s_0\), use pole-zero distances: \(K=\prod |s_0-p_i|/\prod |s_0-z_j|\) for \(G_{\mathrm{ol}}=n/d\) monic in both (adjust leading-coefficient \(\beta\) if \(G_{\mathrm{ol}}=\beta n/d\)). Include \(\beta\) in \(K_{\mathrm{true}}=\beta K_{\mathrm{Evans}}\) according to how the problem defined \(K\).

Routh for crossing is usually faster than substituting \(s=j\omega\) into a cubic or quartic, and it double-counts as a stability-range problem.

For a design sketch with specified \(\zeta\) and \(\omega_n\), the target point is determined even before the locus: if that point is not on the uncompensated locus, proportional control fails. Measure the angle defect; that defect is what a lead zero-pole pair must supply (unit 08). This unit stops at “is the point on the locus?” and “what \(K\)?”.

When \(G_{\mathrm{ol}}\) has a parameter that is not \(K\) (a plant time constant), the locus in that parameter is not Evans unless you rewrite \(1+\alpha G_1=0\). Force the Evans form before applying rules.

Check a finished sketch: branches are conjugate-symmetric; they start at poles; they do not cross each other except at breakaways (in the simple UG pictures); they go to zeros or asymptotes; real-axis occupancy matches the odd-count rule.

## Mistakes

Using even multiples of 180° (the 0° locus) while quoting \(K>0\).

Centroid as \((\sum z-\sum p)/(n-m)\) with the sums reversed, or dividing by \(n\) instead of \(n-m\).

Putting a real-axis segment to the left of an even number of real singularities.

Breakaway at the midpoint between a pole and a zero (that is a break-in/breakaway only in special cases; use \(dK/ds=0\)).

Forgetting the leading constant of \(G_{\mathrm{ol}}\) when computing \(K\) from lengths.

Marking asymptotes from the origin instead of from \(\sigma_a\).

Applying departure-angle arithmetic with the wrong 180° sign, so the branch is drawn into the RHP when it actually leaves leftward (or vice versa).

Treating closed-loop zeros as moving on the locus.

Using the locus of \(1+K G H=0\) but omitting \(H\) when \(H\neq 1\).

Reading stability as “all branches in the LHP at this \(K\)” from a sloppy sketch that missed a real-axis branch in the RHP (type 0 with a RHP pole, etc.). Confirm with Routh at that \(K\).

Declaring that adding a pole at the origin (PI) “does not change the locus much.” It adds a branch and moves the centroid right, often destroying damping of the former pair.

A complete sketch of \(1+K/[s(s+3)(s+6)]=0\) is the canonical three-pole drill. Poles at \(0,-3,-6\); \(n-m=3\); centroid \((-0-3-6)/3=-3\); asymptotes \(60^\circ,180^\circ,300^\circ\) through \(-3\). Real-axis occupancy: \([-3,0]\) and \((-\infty,-6]\). Breakaway between \(-3\) and \(0\): \(K=-s(s+3)(s+6)\), set \(dK/ds=0\), or \(\frac{1}{\sigma}+\frac{1}{\sigma+3}+\frac{1}{\sigma+6}=0\). A reasonable numerical root is \(\sigma\approx -1.27\) (and a second critical point left of \(-6\) that is not a breakaway on the two-pole-plus-infinity picture in the same way — check occupancy). Routh on \(s^3+9s^2+18s+K\): \(s^1\) entry \((162-K)/9\), so \(K_u=162\), \(\omega_u=\sqrt{18}=4.24\). Branches: one stays on the negative real axis toward \(-\infty\) along the 180° asymptote after the far breakaway region; two leave the \([-3,0]\) breakaway, cross \(\pm j4.24\) at \(K=162\), and go to the \(\pm 60^\circ\) asymptotes. For a design with \(\zeta=0.5\), the ray from 0 at \(60^\circ\) from the negative real axis (i.e. \(120^\circ\) from the positive real axis) may or may not hit the locus in the LHP before the \(j\omega\) crossing; if it does, read \(K\) from the product of distances to the three poles. If the ray misses, proportional gain cannot meet \(\zeta=0.5\) and a lead zero is required.

Angles of departure, computed once slowly: plant poles at \(0\) and \(-1\pm j2\). At \(-1+j2\), the vector from 0 is \(-1+j2\) at \(116.6^\circ\); the vector from the conjugate is \(+j4\) at \(90^\circ\); no zeros. Sum of pole angles \(206.6^\circ\). Departure \(180^\circ-206.6^\circ=-26.6^\circ\) measured from the positive-real direction attached to that pole. Draw a small arrow at \(-26.6^\circ\); the branch dives slightly downward as it leaves, which in this geometry typically heads toward the \(j\omega\) axis. A sign error of \(180^\circ\) here is the difference between “needs a notch” and “gain is enough.”

Magnitude condition with a non-monic numerator: \(G_{\mathrm{ol}}=\beta (s+z)/[s(s+p)]\). Then \(K_{\mathrm{Evans}}\) in \(1+K_{\mathrm{Evans}} n/d=0\) is not the physical gain. Either absorb \(\beta\) into \(K\) from the start or compute \(K_{\mathrm{physical}}=K_{\mathrm{Evans}}/\beta\) after measuring lengths on the monic \(n/d\). Exam keys split on this; write the characteristic equation you used in one line before the arithmetic.

Repeated open-loop poles: two poles at \(-a\) contribute \(360^\circ\) of angle as a test point circles them, and the real-axis rule counts two singularities. Breakaway from a double pole along directions that split the local \(180^\circ\) condition; for a double pole on the real axis with the rest of the plane empty, branches leave at \(\pm 90^\circ\). If there is also a zero, those angles rotate by half the zero’s contribution. Compute; do not memorize a single picture.
