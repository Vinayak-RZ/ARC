# Short, medium, and long transmission-line models and ABCD parameters

A transmission line is a distributed R, L, G, C circuit. At power frequency the wavelength at \(50\ \mathrm{Hz}\) is \(6000\ \mathrm{km}\) in free space and still several thousand kilometres on an overhead line, so a \(50\ \mathrm{km}\) feeder is electrically short and a \(400\ \mathrm{km}\) EHV line is not. Undergraduate T&D courses classify lines as short, medium, or long, replace the distributed circuit by a lumped equivalent, and describe the two-port by ABCD (transmission) parameters. This unit is those models, voltage regulation, Ferranti rise, SIL, and the algebra that later load-flow \(\pi\) branches reuse.

## Concepts

Per-phase series impedance density \(z=r+j\omega\ell\) in \(\Omega/\mathrm{km}\) and shunt admittance density \(y=g+j\omega c\) in S/km define a uniform line. Conductance \(g\) is often neglected on overhead lines (small leakage). Capacitance is not negligible on EHV because \(\omega c\) times hundreds of kilometres is millisiemens, comparable to the reactive demand of the series inductance.

Length classification (typical UG, \(50/60\ \mathrm{Hz}\) overhead):

- Short: roughly under \(80\ \mathrm{km}\). Shunt capacitance ignored. Series \(Z=z\ell\) only.
- Medium: roughly \(80\)–\(240\ \mathrm{km}\). Shunt charging lumped. Nominal \(\pi\) (half \(Y=y\ell\) at each end, \(Z\) in the middle) is the default. Nominal T (half \(Z\) on each side, \(Y\) in the middle) is equivalent for exams but less convenient for \(Y_\mathrm{bus}\).
- Long: beyond about \(240\ \mathrm{km}\), or whenever you need accuracy on charging and angle. Use hyperbolic (distributed) parameters, then an equivalent \(\pi\) whose series arm is \(Z\sinh\gamma\ell/\gamma\ell\) rather than \(z\ell\).

These kilometre numbers are rules of thumb, not physics. A cable has far more \(c\) per kilometre; a \(20\ \mathrm{km}\) cable may need a medium-line model. Always think in electrical length \(\gamma\ell\), not only in km.

ABCD parameters treat the line as a two-port with sending voltage and current \((V_S,I_S)\) and receiving \((V_R,I_R)\), all per-phase RMS phasors:

\[
V_S=AV_R+BI_R,\qquad I_S=CV_R+DI_R.
\]

Reciprocal networks satisfy \(AD-BC=1\). A symmetric line has \(A=D\). Short line: \(A=D=1\), \(B=Z\), \(C=0\). Medium nominal \(\pi\): \(A=D=1+YZ/2\), \(B=Z\), \(C=Y(1+YZ/4)\). Long line: \(A=D=\cosh\gamma\ell\), \(B=Z_c\sinh\gamma\ell\), \(C=(1/Z_c)\sinh\gamma\ell\), with propagation constant \(\gamma=\sqrt{zy}\) and characteristic impedance \(Z_c=\sqrt{z/y}\).

Voltage regulation is \((|V_{R,\mathrm{nl}}|-|V_{R,\mathrm{fl}}|)/|V_{R,\mathrm{fl}}|\) with sending voltage held fixed. For a short line with lagging load, regulation is positive (voltage drops with load). For a long lightly loaded line, Ferranti effect can make \(|V_R|>|V_S|\) at no-load, so “regulation” needs a signed definition; say what you computed.

Surge impedance loading (SIL) is \(P_\mathrm{SIL}=|V|^2/Z_c\) three-phase if \(V\) is line-to-line and \(Z_c\) is the positive-sequence characteristic impedance (real part when \(r=g=0\): \(Z_c=\sqrt{\ell/c}\)). At SIL a lossless line has flat voltage profile: series inductive vars cancel shunt capacitive vars. Below SIL the line is a net var generator (charging dominates); above SIL it is a net var absorber. That is the physical reason EHV lines need shunt reactors at light load and may need capacitors or generation support at heavy load.

Power transfer on a lossless short line \(X\), with angle \(\delta\) between sending and receiving voltages of magnitudes \(V_S,V_R\):

\[
P=\frac{V_S V_R}{X}\sin\delta,\qquad Q_R=\frac{V_R}{X}(V_S\cos\delta-V_R).
\]

The \(P\)–\(\delta\) sinusoid is the same curve that unit 06 uses for equal-area stability. The \(Q\)–\(V\) relation is the same idea as unit 12: raising \(V_S\) or adding receiving-end capacitors raises \(V_R\).

Nominal \(\pi\) versus equivalent \(\pi\): the nominal \(\pi\) uses \(Z=z\ell\) and \(Y=y\ell\). The equivalent \(\pi\) uses \(Z'=Z_c\sinh\gamma\ell\) and \(Y'/2=(1/Z_c)\tanh(\gamma\ell/2)\). For a \(100\ \mathrm{km}\) overhead line the difference is small; for \(400\ \mathrm{km}\) it is not. UG numericals often hand you \(A,B\) or \(z,y,\ell\) and expect hyperbolic functions or a “use nominal \(\pi\)” instruction. Follow the instruction.

Ferranti effect: open receiving end, \(I_R=0\), so \(V_S=AV_R\) and \(V_R=V_S/A\). For a long line \(|A|<1\) at no-load (A is \(\cosh\gamma\ell\approx 1-(\omega^2\ell c)\ell^2/2\) which is slightly less than 1 in magnitude after the imaginary parts are included — more simply, charging current through series inductance produces a voltage rise toward the open end). Shunt reactors at the receiving end or at line sections mitigate Ferranti and overvoltage during load rejection.

Corona, skin effect, and bundled conductors change the effective \(r\), \(\ell\), and \(c\). Bundling raises GMD for inductance (lowers \(\ell\)) and raises capacitance, lowering \(Z_c\) and raising SIL — which is why 400 kV+ lines bundle. This unit uses given \(z,y\); GMD/GMR geometry belongs with line-parameter calculation in T&D, not with ABCD algebra. If a problem gives GMD, GMR, and \(\varepsilon\), compute \(\ell=2\times 10^{-7}\ln(\mathrm{GMD}/\mathrm{GMR})\) H/m per phase (approximate, transposition assumed) and \(c=2\pi\varepsilon/\ln(\mathrm{GMD}/r_\mathrm{eq})\).

Transposition averages the three sequence couplings so that a balanced line can be represented by one positive-sequence \(z,y\). Untransposed lines have small negative- and zero-sequence coupling to positive sequence; UG load flow ignores that.

ABCD of cascaded lines: if two two-ports are in cascade, the overall matrix is the product \(A_1 A_2\) in the usual \(2\times 2\) block sense:

\[
\begin{pmatrix}A&B\\C&D\end{pmatrix}
=
\begin{pmatrix}A_1&B_1\\C_1&D_1\end{pmatrix}
\begin{pmatrix}A_2&B_2\\C_2&D_2\end{pmatrix}.
\]

Order matters: the sending-end network is on the left. A transformer can be inserted as a two-port \(A=t\), \(B=0\), \(C=0\), \(D=1/t\) (ideal, voltage ratio \(t=V_S/V_R\) for step) plus a series leakage in \(B\).

Efficiency \(\eta=P_R/P_S\). Losses are \(I^2R\) in the series resistance plus dielectric loss if \(g\neq 0\). Medium-line charging does not dissipate real power if \(g=0\), but it changes the current profile so sending and receiving currents differ; \(I_S\neq I_R\). Using \(I_R\) in \(I^2R\) with \(R=r\ell\) underestimates or overestimates depending on the current distribution; the rigorous loss is \(P_S-P_R\).

Short-line regulation formula with \(V_R\) as phasor reference: \(V_S=V_R+I_R(R+jX)\). Approximate magnitude: \(\Delta V\approx I_R(R\cos\phi+X\sin\phi)\) for lagging \(\phi\), which is the “kVA drop” mnemonic. It fails when \(\phi\) is leading (Ferranti-like rise) because the \(X\sin\phi\) term changes sign.

Compensation belongs in unit 12 but is previewed here: series capacitors cancel part of \(X\) (raise \(P_\mathrm{max}\)); shunt capacitors at R raise \(V_R\) and supply load vars; shunt reactors absorb Ferranti vars.

A cable \(\pi\) has large \(Y\) and small \(X\). Voltage drop is more resistive; charging Mvar is large even at tens of kilometres. Never apply overhead short-line neglect of \(B\) to a submarine cable.

ABCD parameters are two-port transmission parameters, not chain parameters of a different name: the same \(A,B,C,D\) appear in network theory as \(T\) parameters. Power-system convention puts receiving quantities on the right-hand side, so \(B\) has the dimension of ohms and \(C\) of siemens. A unit check on a numerical \(A,B,C,D\) set catches swapped \(B\) and \(C\). Reciprocity \(AD-BC=1\) is a numerical checksum after hyperbolic evaluation; if it is 0.97 or 1.04, rounding of \(\gamma\ell\) is the usual culprit, not a new physics.

Voltage and current along a long line, with \(x=0\) at the receiving end, are \(V(x)=V_R\cosh\gamma x+Z_c I_R\sinh\gamma x\) and \(I(x)=I_R\cosh\gamma x+V_R\sinh\gamma x/Z_c\). At \(x=\ell\) this is exactly the ABCD pair. Standing-wave language from RF lines is valid but rarely helpful at 50 Hz except on very long lines and on some open-ended Ferranti plots. SIL is the matched-load power; a line terminated in \(Z_c\) has \(V_S/I_S=Z_c\) and a flat \(|V|\) if lossless. Real lines are not operated as matched RF lines: the load is a grid, not \(Z_c\). SIL remains a var-balance benchmark, not a thermal rating. Thermal rating is ampacity and sag, a different number, often above SIL on EHV and below SIL on long cables.

When a problem gives only percent voltage regulation and a lagging pf, recover \(V_S\) from the short-line phasor diagram: the “desiring” construction with \(IR\) in phase with \(I\) and \(IX\) leading \(I\) by 90° relative to the \(V_R\) reference. The same diagram with a leading pf shows why regulation can be negative. Medium-line regulation must include the sending-end current that supplies charging: compute \(I_S=C V_R+D I_R\) and then \(P_S=\mathrm{Re}(V_S I_S^*)\). Efficiency is \(P_R/P_S\), not \(|V_R|/|V_S|\).

## Equations

Propagation and characteristic impedance:

\[
\gamma=\sqrt{zy},\qquad Z_c=\sqrt{\frac{z}{y}}.
\]

Long-line ABCD:

\[
A=D=\cosh(\gamma\ell),\quad B=Z_c\sinh(\gamma\ell),\quad C=\frac{\sinh(\gamma\ell)}{Z_c}.
\]

Equivalent \(\pi\):

\[
Z'=Z_c\sinh(\gamma\ell),\qquad \frac{Y'}{2}=\frac{1}{Z_c}\tanh\frac{\gamma\ell}{2}.
\]

Short line:

\[
A=D=1,\quad B=Z=z\ell,\quad C=0.
\]

Nominal \(\pi\):

\[
A=D=1+\frac{YZ}{2},\quad B=Z,\quad C=Y\left(1+\frac{YZ}{4}\right),\quad Y=y\ell.
\]

Lossless power:

\[
P=\frac{|V_S||V_R|}{X}\sin\delta.
\]

SIL (lossless, \(V\) line-to-line, three-phase):

\[
P_\mathrm{SIL}=\frac{|V|^2}{Z_c},\qquad Z_c=\sqrt{\frac{\ell}{c}}.
\]

No-load receiving voltage (Ferranti): \(V_R=V_S/A\) with \(I_R=0\).

## Methods

Classify by length and by whether \(y\ell\) is given. If only \(R,X\) appear, use short-line. If \(B\) or \(C\) per km appears, use nominal \(\pi\) unless told to use hyperbolic functions.

Work per-phase: \(V\) is phase-to-neutral unless the problem uses a balanced three-phase ABCD with line voltages consistently — UG almost always uses per-phase phasors. Convert \(\Delta\) loads to Y.

To find \(V_S\) given load at R: compute \(I_R=S_R^*/V_R^*\) (per-phase), then apply ABCD. Regulation: recompute \(|V_R|\) at \(I_R=0\) with the same \(|V_S|\), or equivalently \(|V_R|=|V_S/A|\).

To build a load-flow branch: convert the equivalent \(\pi\) into series \(z_{ik}\) and shunt \(j b/2\) at each end. That is unit 03’s line data.

Checks: \(AD-BC=1\) within rounding; \(|A|\) slightly less than 1 for a typical long line; \(P_S-P_R=I^2R\) roughly; at no-load \(I_S=C V_R= (A-1)/B\cdot V_S\) consistent with charging.

For a numerical hyperbolic evaluation, if \(\gamma\ell=x+jy\) with \(x\) small, \(\cosh(x+jy)=\cosh x\cos y+j\sinh x\sin y\). Series expansions \(A\approx 1+zy\ell^2/2\), \(B\approx z\ell(1+zy\ell^2/6)\) recover the equivalent \(\pi\) without naming hyperbolic functions.

## Mistakes

Using line-to-line voltage as \(V_R\) in \(I_R=S/(3V_R)\) mixed with a per-phase \(Z\) (use phase voltage or be consistent with three-phase ABCD). Ignoring charging on a 200 km 400 kV line. Using nominal \(\pi\) \(Z=z\ell\) on a 400 km line when the problem asked for long-line. Setting \(C=0\) on a medium line (that is the short-line model). Computing SIL with phase voltage and then calling it three-phase. Taking regulation as \((V_S-V_R)/V_S\) with phasors not magnitudes, or with a loaded \(V_S\) that was never held constant. Forgetting \(\sqrt{3}\) when converting three-phase MW to per-phase VA. Cascading ABCD in the wrong order. Treating \(Z_c\) as the series impedance \(z\ell\). Using \(P=V^2/X\) without \(\sin\delta\). Applying overhead length breakpoints to cables. Dropping the factor \(1/2\) on shunt \(Y\) in the nominal \(\pi\) (putting all charging at one end). Using \(A=1+YZ\) instead of \(1+YZ/2\). Reporting Ferranti as a current when the question asked voltage rise.
