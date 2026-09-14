# Economic operation: incremental cost, B-coefficients, and penalty factors

A power system with several thermal plants must meet a load (plus losses) at minimum fuel cost while respecting generator limits. The undergraduate solution is equal incremental cost, modified by a penalty factor when transmission losses matter. This is not unit commitment (on/off, minimum up time) and not AC optimal power flow with voltage constraints. Those are later. Here: quadratic (or piecewise linear) cost curves, Lagrange multipliers for the power-balance constraint, coordination equations, B-matrix (Kron) loss formula, and a short statement of hydro-thermal coordination as a water-value multiplier.

## Concepts

A thermal unit \(i\) has a cost rate \(C_i(P_i)\) in ₹/h or $/h as a function of electrical power \(P_i\) in MW. A common UG fit is quadratic \(C_i=\alpha_i+\beta_i P_i+\gamma_i P_i^2\). Incremental cost (IC), also called incremental fuel cost or \(\mathrm{d}C_i/\mathrm{d}P_i\), is then \(\beta_i+2\gamma_i P_i\) in ₹/MWh. The units of \(\gamma\) are ₹/MW²h. Input-output curves in heat units (MBtu/h vs MW) times fuel price give \(C_i\). Valve-point ripple makes the curve nonconvex; UG ignores that and treats \(C_i\) as smooth convex, so a unique IC intersection exists.

Without losses, minimize \(\sum C_i(P_i)\) subject to \(\sum P_i=P_D\) and \(P_i^{\min}\le P_i\le P_i^{\max}\). Interior optimum: all units that are not at a limit have the same IC \(\lambda=\mathrm{d}C_i/\mathrm{d}P_i\). That common \(\lambda\) is the Lagrange multiplier of the power-balance constraint: the marginal cost of serving one more MW of load. Units at \(P_{\max}\) have IC \(\le\lambda\) (they already look cheap); units at \(P_{\min}\) have IC \(\ge\lambda\) (they look expensive but cannot back down). Economic dispatch (ED) is this calculation. It is not the same as scheduling which units are on (commitment).

With transmission losses \(P_L(P_1,\ldots,P_n)\), the constraint is \(\sum P_i=P_D+P_L\). Coordination equations become

\[
\frac{\mathrm{d}C_i}{\mathrm{d}P_i}\,L_i=\lambda,\qquad L_i=\frac{1}{1-\partial P_L/\partial P_i},
\]

where \(L_i\) is the penalty factor of plant \(i\). If increasing plant \(i\) increases losses (\(\partial P_L/\partial P_i>0\)), then \(L_i>1\) and that plant is penalized: it must have a lower IC to be equally attractive. A plant sitting electrically close to the load can have \(\partial P_L/\partial P_i<0\) (negative penalty, \(L_i<1\)): raising it actually reduces losses by displacing remote generation.

Kron’s loss formula (B-coefficients) is a quadratic approximation

\[
P_L=\sum_i\sum_j P_i B_{ij} P_j+\sum_i B_{i0} P_i+B_{00},
\]

often simplified in homework to \(P_L=\sum_i\sum_j P_i B_{ij} P_j\) with \(B_{ij}\) in MW⁻¹. Then \(\partial P_L/\partial P_i=2\sum_j B_{ij}P_j\) (plus \(B_{i0}\) if present). \(B\) coefficients are computed from a base-case load flow and assumed constant near that case. They are not valid across a radically different dispatch or topology. UG problems hand you \(B_{11},B_{12},B_{22}\).

Iterative solution: guess \(\lambda\), solve each \(P_i\) from \(\mathrm{IC}_i(P_i)L_i=\lambda\) (with \(L_i\) from current \(P\)), clip to limits, update \(P_L\), check \(\sum P_i-P_L=P_D\), raise or lower \(\lambda\). Without losses, a direct solve of the linear IC equations plus the balance is enough for quadratics.

Example of the no-loss linear solve: two units \(IC_1=2+0.02 P_1\), \(IC_2=1.5+0.03 P_2\), \(P_1+P_2=P_D\). Set ICs equal, solve. Always clip and re-dispatch if a limit binds: freeze that unit at the limit and equal-IC the others to the remaining load.

Incremental transmission loss (ITL) is \(\partial P_L/\partial P_i\). Penalty factor \(L_i=1/(1-\mathrm{ITL}_i)\). Some older notes write \(IC_i/(1-\mathrm{ITL}_i)=\lambda\), which is the same.

Hydro-thermal: a hydro plant has a water-usage rate \(q_i(P_i)\) and a limited reservoir (or a streamflow). The coordination uses \(\nu\,\mathrm{d}q_i/\mathrm{d}P_i\) in place of fuel IC, with \(\nu\) a water value (Lagrange multiplier of the water constraint) in ₹/m³ or ₹ per unit volume. On a one-day horizon with fixed volume, \(\nu\) is chosen so that the water is used. UG writes the equation; it does not run a full hydrothermal DP.

Network-constrained ED (DC OPF) adds line flow limits \(\lvert(\theta_i-\theta_k)/x_{ik}\rvert\le P_{ik}^{\max}\). Then \(\lambda\) becomes locational (LMP = energy \(\lambda\) plus congestion plus losses). That is a power-market overlay, not required for the core equal-IC exam. Mention LMP as “\(\lambda\) at a bus.”

Emissions dispatch and combined cost+emission are extra objectives; Pareto weights are not core UG.

Piecewise linear costs: equal incremental cost still holds inside a segment; the unit’s IC is a step function and the dispatcher fills the cheapest remaining MW (merit order). Quadratic IC is the smooth analog of merit order.

Why losses need a base-case: \(B_{ij}\) depend on the slack-bus choice and on voltage profile. Changing the slack in a B-coefficient set without recomputing is inconsistent. Exam B-matrices are given; do not rederive Kron unless asked.

A unit’s incremental cost is a local derivative, not the average cost \(C_i/P_i\). Average cost is used in some tariff arguments; it does not solve ED. Two units can have the same average cost at a point and different ICs; the cheaper IC unit should take the next MW. That is the entire justification of equal-IC. Heat rate (MBtu/MWh) times fuel price (₹/MBtu) is IC if the heat-rate curve is differentiated correctly: if \(H(P)=\alpha'+\beta'P+\gamma'P^2\) in MBtu/h, then \(\mathrm{IC}=(\beta'+2\gamma'P)\times\mathrm{price}\). Using average heat rate times price as if it were IC is a classic error.

When more than two units are free, the lossless quadratic case is a linear system: \(P_i=(\lambda-\beta_i)/(2\gamma_i)\) for each \(i\), \(\sum P_i=P_D\). Solve for \(\lambda\) in one line. Units with tiny \(\gamma_i\) (flat IC) take large \(\Delta P\) for a small \(\Delta\lambda\) — they are the swing plants of the dispatch. Units with steep \(\gamma_i\) barely move. If \(\gamma_i=0\), IC is constant and that unit is all-or-nothing at the constant IC relative to \(\lambda\) (fill it until a limit).

Loss formula units: if \(P\) is in MW, \(B_{ij}\) is in MW⁻¹ so that \(P B P\) is MW. If \(P\) is in pu on \(S_{\mathrm{base}}\), \(B\) is pu and \(P_L\) is pu. Converting \(B_{\mathrm{MW}}=B_{\mathrm{pu}}/S_{\mathrm{base,MW}}\). Mixing pu P with MW⁻¹ B produces nonsense.

Spinning reserve and ramp rates are operational constraints that the basic equal-IC statement ignores. A unit that is cheap but at \(P_{\max}\) cannot provide raise reserve; the dispatcher may back it off for reserve, which is no longer pure ED. UG exams usually ignore reserve unless a remaining-headroom sentence appears.

Penalty-factor intuition on a two-bus line: a remote plant sending power over a lossy line has \(\partial P_L/\partial P_{\mathrm{remote}}>0\), so \(L>1\), so its IC must be lower than the local plant’s IC at optimum. The local plant is dispatched harder than a lossless equal-IC would suggest. That is geographic discrimination, not a tax on fuel quality. If the B-coefficient matrix is symmetric and positive semidefinite (lossy network), \(P_L\) is nonnegative for the operating P vector; a negative computed \(P_L\) means a sign error in B or a P that includes loads as negative generation inconsistently.

Hydro coordination in one paragraph more: for a hydro plant with a daily water budget \(\int q(P)\,dt=Q_{\mathrm{day}}\), the constant \(\nu\) is chosen so the integral is met. If water is abundant, \(\nu\) is small and hydro looks cheap, so it runs high in the peak. If water is scarce, \(\nu\) is large and hydro is saved for the hours when thermal \(\lambda\) is highest. That is peak-shaving. Cascade reservoirs and delayed river travel are not UG ED.

Transmission-constrained ED without a full OPF: if a corridor limit binds, the two sides of the constraint have different \(\lambda\) (LMP jump). UG can illustrate with two areas and a tie \(P_{12}\le P_{\max}\): dispatch each area to its own load plus/minus the max tie, then \(\lambda_1\neq\lambda_2\). The difference is the congestion price. No B-coefficients are required for that sketch.

## Equations

Quadratic cost and IC:

\[
C_i=\alpha_i+\beta_i P_i+\gamma_i P_i^2,\qquad \mathrm{IC}_i=\beta_i+2\gamma_i P_i.
\]

Lossless coordination:

\[
\beta_i+2\gamma_i P_i=\lambda,\qquad \sum_i P_i=P_D,\qquad P_i\in[P_i^{\min},P_i^{\max}].
\]

Penalty factor:

\[
L_i=\frac{1}{1-\partial P_L/\partial P_i},\qquad \mathrm{IC}_i\,L_i=\lambda.
\]

Two-plant Kron (no linear terms):

\[
P_L=B_{11}P_1^2+2B_{12}P_1 P_2+B_{22}P_2^2,
\]
\[
\frac{\partial P_L}{\partial P_1}=2B_{11}P_1+2B_{12}P_2.
\]

Hydro coordination (schematic): \(\nu\,\mathrm{d}q_i/\mathrm{d}P_i=\lambda/L_i\) or as specified with the same \(\lambda\) as thermal IC.

## Methods

Lossless: set all free ICs equal to \(\lambda\), express \(P_i=(\lambda-\beta_i)/(2\gamma_i)\), sum to \(P_D\), solve \(\lambda\), clip limits, repeat with remaining load.

With losses: (1) start with lossless dispatch; (2) compute \(P_L\) and ITLs from B-coefficients; (3) compute \(L_i\); (4) solve \(\mathrm{IC}_i L_i=\lambda\) with \(\sum P_i=P_D+P_L\); (5) iterate. One iteration is a typical hand question.

Limit handling: if a computed \(P_i>P_{\max}\), set it to \(P_{\max}\) and remove it from the equal-IC set. Do not use a negative \(\gamma\) (nonconvex) in the closed-form solve.

Checks: \(\lambda\) between the cheapest IC at \(P_{\min}\) and the dearest at \(P_{\max}\); \(P_L\) a few percent of \(P_D\); \(L_i\) near 1.0 to 1.1 typically; sum of plants = load + losses.

## Mistakes

Setting \(C_i\) equal instead of \(\mathrm{d}C_i/\mathrm{d}P_i\). Using \(\mathrm{IC}=\beta+\gamma P\) (missing the 2). Forgetting to clip limits. Treating \(B_{12}\) as if \(P_L=B_{11}P_1^2+B_{12}P_1P_2+B_{22}P_2^2\) without the 2 on the cross term when taking \(\partial P_L/\partial P_1\). Using \(L_i=1+\partial P_L/\partial P_i\) instead of \(1/(1-\mathrm{ITL})\). Balancing \(\sum P_i=P_D\) while adding a nonzero \(P_L\). Dispatching a unit below minimum because IC matching wanted it. Mixing heat-rate incremental (MBtu/MWh) with ₹/MWh without the fuel price. Using penalty factors computed at a wildly different dispatch. Equalizing incremental costs when one unit is at a bound without checking the inequality. Writing \(P_L=\sum B_{ii}P_i\) (linear) and still using the quadratic derivative. Changing MVA bases of \(B_{ij}\) incorrectly (B scales as 1/S_base if P is in pu — in MW they are MW⁻¹; do not treat them as pu without converting).
