# B-H, reluctance, inductance from energy

Electrical machines are magnetic devices first. A transformer, a DC machine, and an induction motor all convert energy by linking current to flux in a ferromagnetic core with one or more air gaps. Before equivalent circuits, the working model is the magnetic circuit: magnetomotive force (MMF) drives flux through reluctances the way voltage drives current through resistances. This unit installs that analogy, the B-H curve that makes it nonlinear, and the energy/coenergy identities that later give inductance and electromagnetic force. It is not a fields course. Maxwell’s equations stay in the background; Ampere’s law and Faraday’s law appear as circuit statements.

The payoff is practical. Saturation, leakage, fringing, hysteresis, and eddy currents are not decorations. They explain why magnetizing current is not sinusoidal, why an air-gap length of a millimetre dominates a steel path of a metre, and why inductance is defined from stored energy rather than from a naive \(N\Phi/i\) when the B-H curve is nonlinear. Every later machines unit assumes this vocabulary.

## Concepts

Ampere’s law around a closed path states that the line integral of \(\mathbf{H}\) equals the enclosed current (SI: ampere-turns). In a magnetic circuit with \(N\) turns carrying current \(i\), the MMF is \(\mathcal{F} = Ni\). That MMF is spent as \(\int H\,dl\) along the flux path. If the path splits into segments of roughly uniform \(H\), the sum \(H_c \ell_c + H_g \ell_g + \cdots\) equals \(Ni\). Steel has large \(\mu\), so \(H_c = B/\mu\) is small even when \(\ell_c\) is long. Air has \(\mu_0\), so a short gap \(\ell_g\) can consume most of the MMF. That is why air-gap design is the first numerical skill in machines.

Flux \(\Phi\) is the surface integral of \(\mathbf{B}\). In a core of cross-section \(A_c\) with approximately uniform \(B\), \(\Phi = B A_c\). Continuity of flux (no magnetic monopoles) makes \(\Phi\) the same in series elements if leakage is neglected. Parallel branches split flux the way parallel resistors split current. Reluctance \(\mathcal{R} = \ell/(\mu A)\) is defined so that \(\mathcal{F} = \mathcal{R}\Phi\), analogous to \(V=RI\). Permeance \(\mathcal{P}=1/\mathcal{R}\) is often nicer for parallel air-gap combinations. The analogy is not perfect: magnetic circuits leak, \(B\) is not uniform near corners, and \(\mu\) depends on \(B\). Use the analogy, then correct it.

The B-H curve of a ferromagnetic material is the constitutive relation. For air, \(B=\mu_0 H\) is a straight line through the origin. For silicon steel, \(B=\mu(H)H\) saturates: incremental permeability \(\mathrm{d}B/\mathrm{d}H\) falls as \(B\) approaches 1.5–2 T. A virgin curve, a hysteresis loop, and a DC magnetization curve are different objects. The hysteresis loop encloses an energy per cycle \(\oint H\,\mathrm{d}B\) (volume density). That area is hysteresis loss. Eddy-current loss is a separate ohmic loss from Faraday-induced currents in the core; laminations cut the eddy paths. The Steinmetz and classical eddy formulas appear in Methods; conceptually, core loss is why transformers hum and why magnetizing branches have a resistor.

Leakage flux is flux that does not follow the intended path. In a transformer, leakage is the flux of one winding that does not link the other. In a rotating machine, leakage includes slot, end-winding, and zig-zag components. Fringing is the spreading of flux at an air gap so that the effective gap area is larger than the core area. A first correction is \(A_g \approx (a+\ell_g)(b+\ell_g)\) for a rectangular pole face \(a\times b\). Ignoring fringing overestimates gap reluctance; ignoring leakage underestimates the MMF needed for a given useful flux.

Inductance from flux linkage is \(L = \lambda/i = N\Phi/i\) when the relationship is linear and passes through the origin. Equivalently \(L = N^2/\mathcal{R}\) or \(L = N^2\mathcal{P}\). When the core saturates, \(\lambda(i)\) is a curve, not a line. Incremental inductance \(L_\mathrm{inc}=\mathrm{d}\lambda/\mathrm{d}i\) and apparent inductance \(\lambda/i\) then differ. Energy stored in a magnetic field for a lossless inductor is \(W = \int i\,\mathrm{d}\lambda\). Coenergy is \(W' = \int \lambda\,\mathrm{d}i\). For a linear inductor \(W=W'=\tfrac12 Li^2\). For a saturating inductor \(W' > W\) on the usual B-H shape. Electromagnetic force or torque in a singly excited system is obtained from coenergy at constant current, \(f_e = \partial W'(i,x)/\partial x\), or from energy at constant flux linkage, \(f_e = -\partial W(\lambda,x)/\partial x\). That identity is the origin of reluctance torque and of the virtual-work derivation of \(T = \tfrac12 i^2 \mathrm{d}L/\mathrm{d}\theta\).

A linear magnetic circuit is a teaching device. Real machines run near the knee of the B-H curve because that is where you get the most flux per kilogram of steel. Designers pick a peak \(B\) (often 1.2–1.7 T in 50 Hz silicon steel) and then size the gap and the ampere-turns. The magnetic circuit of a rotating machine also has a rotating MMF from distributed windings; that is later units. Here the geometry is static: a toroid, a U-core with an armature, a simple two-pole DC yoke.

Boundary conditions matter at steel–air interfaces. The normal component of \(\mathbf{B}\) is continuous if no surface current of the magnetic kind is invented; the tangential component of \(\mathbf{H}\) jumps with surface current. In an air gap between two pole faces, \(B_g \approx B_c\) if leakage is small, but \(H_g = B_g/\mu_0\) is huge compared with \(H_c\). Students who write \(B=\mu_0 \mu_r H\) in the gap with \(\mu_r\) of steel have inverted the material.

Stacking factor \(k_s\) accounts for insulation between laminations: net iron area is \(k_s A_\mathrm{gross}\), typically 0.9–0.97. Flux uses net iron; gap area uses the physical pole face (plus fringing). Mixing those areas is a standard numerical trap.

Units: \(B\) in tesla, \(H\) in A/m, \(\Phi\) in weber, \(\mathcal{R}\) in A/Wb (or H\(^{-1}\)), \(\lambda\) in weber-turns, \(L\) in henry. MMF \(Ni\) is ampere-turns; the “turns” are dimensionless. Do not invent an extra \(4\pi\) in SI. Older CGS formulas (gilberts, oersteds) do not belong in this handbook.

A last conceptual split: magnetizing inductance of a transformer is the inductance seen when the secondary is open, corresponding to the useful flux path. Leakage inductance corresponds to leakage permeance. Energy in the gap of a rotating machine is the coenergy reservoir that produces torque. Those three sentences are the bridge from this unit to transformers and to electromechanical conversion.

Permanent magnets appear as MMF sources in some UG electives. A linear PM model is a recoil line \(B = B_r + \mu_\mathrm{rec} H\) with \(H<0\) in the second quadrant. Load line of the gap intersects that recoil line. This pack’s later special-machines unit uses that picture for BLDC and PMAC; here it is enough to know that a magnet is not a constant-flux source independent of gap, nor a constant-MMF source independent of recoil permeability.

## Equations

Ampere (lumped segments):

\[
Ni = \sum_k H_k \ell_k.
\]

Constitutive (linear segment):

\[
B = \mu H = \mu_0 \mu_r H,\qquad \Phi = B A,\qquad \mathcal{R} = \frac{\ell}{\mu A},\qquad Ni = \mathcal{R}\Phi.
\]

Series and parallel:

\[
\mathcal{R}_\mathrm{series} = \sum \mathcal{R}_k,\qquad \mathcal{P}_\mathrm{parallel} = \sum \mathcal{P}_k.
\]

Air gap (no fringing):

\[
\mathcal{R}_g = \frac{\ell_g}{\mu_0 A_g},\qquad H_g = \frac{B_g}{\mu_0}.
\]

Inductance (linear, origin-passing):

\[
L = \frac{N\Phi}{i} = \frac{N^2}{\mathcal{R}} = N^2 \mathcal{P}.
\]

Energy and coenergy (singly excited):

\[
W(\lambda) = \int_0^\lambda i(\lambda')\,\mathrm{d}\lambda',\qquad W'(i) = \int_0^i \lambda(i')\,\mathrm{d}i',\qquad W+W' = \lambda i.
\]

Linear lossless inductor:

\[
W = W' = \tfrac12 L i^2 = \tfrac12 \frac{\lambda^2}{L}.
\]

Force (virtual work):

\[
f_e = \left.\frac{\partial W'}{\partial x}\right|_{i=\mathrm{const}} = -\left.\frac{\partial W}{\partial x}\right|_{\lambda=\mathrm{const}}.
\]

Reluctance torque (linear \(L(\theta)\)):

\[
T_e = \tfrac12 i^2 \frac{\mathrm{d}L}{\mathrm{d}\theta}.
\]

Field energy density (linear media):

\[
w = \tfrac12 \mathbf{B}\cdot\mathbf{H} = \frac{B^2}{2\mu}.
\]

Core-loss sketches (order-of-magnitude, not a design code):

\[
p_h \propto f\, B_m^\alpha,\qquad p_e \propto f^2 t^2 B_m^2,
\]

with \(t\) the lamination thickness and \(\alpha\) often near 1.6–2 for the Steinmetz exponent on a limited \(B\) range.

## Methods

Draw the flux path before writing equations. Mark core segments, gaps, and any parallel branches. Assign a single \(\Phi\) in a series loop, or split \(\Phi\) at a junction. Convert the drawing into reluctances. If the steel is assumed infinite-\(\mu\), drop \(\mathcal{R}_c\) and put all MMF on the gaps. If not, iterate: guess \(B_c\), read \(H_c\) from the B-H curve, compute \(Ni\) required, compare with available ampere-turns, adjust \(B_c\).

For a toroid of mean length \(\ell_c\), area \(A_c\), \(N\) turns, and no gap, \(H = Ni/\ell_c\) and \(B=\mu H\) if linear. With a saw-cut gap \(\ell_g\), write \(Ni = H_c \ell_c + H_g \ell_g\) and \(\Phi = B_c A_c = B_g A_g\). If fringing is neglected, \(A_g=A_c\) so \(B_g=B_c\). Then \(H_g=B_c/\mu_0\). The gap term usually dominates. A numerical check: \(\ell_g/(\mu_0 A)\) versus \(\ell_c/(\mu A_c)\). If \(\mu_r=4000\), one millimetre of gap equals four metres of steel of the same area.

To include stacking factor, use \(A_c = k_s A_\mathrm{gross}\) in the iron and \(A_g = A_\mathrm{gross}\) (plus fringing) in the gap. Flux \(\Phi\) is the same; \(B_c = \Phi/A_c\) is therefore higher than \(B_g=\Phi/A_g\).

Inductance from geometry: compute \(\mathcal{R}_\mathrm{eq}\) as seen by the winding (series/parallel combination of the paths that the winding’s flux actually takes), then \(L=N^2/\mathcal{R}_\mathrm{eq}\). For two windings on the same core, magnetizing inductance uses the mutual permeance; leakage uses the leakage permeance. Do not add leakage and magnetizing reluctances as if they were the same loop.

Energy method for force: express \(W'(i,x)\) or \(W(\lambda,x)\). For a linear plunger, \(L(x) \approx N^2 \mu_0 A / x\) if the gap \(x\) dominates. Then \(W'=\tfrac12 L(x) i^2\) and \(f_e = \tfrac12 i^2 \mathrm{d}L/\mathrm{d}x\), which is attractive (negative \(x\) direction as gap decreases). The same algebra produces aligning reluctance torque in a rotary device.

Graphical load line: plot the steel’s \(B\)-\(H\) or \(\Phi\)-\(\mathcal{F}\) curve. The gap is a straight line through the origin on the \(\Phi\)-\(\mathcal{F}\) plane with slope \(1/\mathcal{R}_g\). Intersection is the operating point. Permanent-magnet problems use a second-quadrant recoil line instead of a first-quadrant steel curve.

When the excitation is AC, peak \(B\) is set by Faraday: \(E_\mathrm{rms} = 4.44 f N \Phi_\mathrm{max}\) for a sinusoidal flux. That formula is derived in the transformer unit; magnetically it means you cannot pick \(B\) and \(N\) independently at a given voltage and frequency. Magnetic-circuit sizing and electrical voltage equations are coupled.

Loss bookkeeping: hysteresis from loop area times frequency times volume; eddy from lamination thickness and \(B_m^2 f^2\). For equivalent-circuit work, lump both into a core-loss resistor placed across the magnetizing branch. Do not put that resistor in series with leakage; that would dissipate load current as if it were magnetizing loss.

A measurement habit: never extract \(\mu_r\) from a single \(B/H\) ratio on a loop that has remanence. Incremental permeability about a bias point is \(\Delta B/\Delta H\) on the local minor loop. Apparent permeability \(\lambda/(N^2 i)\) from a 50 Hz volt-ampere test includes core loss and is not \(\mu\).

## Mistakes

Using \(\mu_r\) of steel in the air gap. The gap is air. \(B_g=\mu_0 H_g\).

Equating \(B_c\) and \(B_g\) after applying stacking factor to both areas the same way. Iron area and gap area differ.

Treating reluctance like resistance for power. Magnetic “Ohm’s law” does not dissipate \(I^2R\) in the reluctance; dissipation is in winding copper and in core hysteresis/eddy.

Writing \(L=N\Phi/i\) on a saturated curve and then using \(\tfrac12 L i^2\) as if \(L\) were constant. Energy is the integral, not the triangle, unless linearity holds.

Forgetting that force from energy at constant \(\lambda\) has a minus sign. The plunger is pulled to increase inductance (decrease reluctance) at constant current.

Ignoring leakage on a heavily gapped core. Not all flux in the window is useful. A magnetizing-inductance calculation that uses only the gap under the pole overstates \(L_m\).

Mixing SI and CGS. \(B=\mu_0 H\) with \(\mu_0=4\pi\times 10^{-7}\) is SI. There is no extra \(4\pi\) on \(Ni=H\ell\) in SI.

Using mean length of the whole yoke when two limbs carry different flux. Parallel paths need a junction and two reluctances.

Taking the B-H curve as single-valued under AC. Hysteresis means \(B(H)\) is a loop; the magnetizing current has a third-harmonic component even if \(B\) is forced sinusoidal by the voltage.

Dropping turns in MMF: \(\mathcal{F}=Ni\), not \(i\). A 200-turn coil at 2 A is 400 AT, not 2 AT.

Computing fringing as an increase in gap length instead of area. Fringing increases effective area and decreases \(\mathcal{R}_g\).

Using peak and RMS flux densities interchangeably in loss formulas. State which. Faraday’s 4.44 uses \(\Phi_\mathrm{max}\).

Treating coenergy and energy as interchangeable in a saturating actuator, then wondering why the force predicted from \(\tfrac12 i^2 \mathrm{d}L/\mathrm{d}x\) disagrees with a finite-element coenergy difference. The linear formula assumes \(L\) independent of \(i\).
