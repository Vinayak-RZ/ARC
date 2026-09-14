# Magnetostatics: Biot–Savart, Ampère, vector potential

Magnetostatics is the dual of electrostatics for steady currents: \(\nabla\cdot\mathbf{B}=0\), \(\nabla\times\mathbf{H}=\mathbf{J}\). Biot–Savart is Coulomb’s law for currents; Ampère’s law is Gauss’s law for currents when symmetry cooperates. The vector potential \(\mathbf{A}\) with \(\mathbf{B}=\nabla\times\mathbf{A}\) exists because \(\mathbf{B}\) is solenoidal. Linear media \(\mathbf{B}=\mu\mathbf{H}\), boundary conditions on \(\mathbf{B}\) and \(\mathbf{H}\), and inductance as a preview of the next unit complete the picture. No displacement current yet (unit 06).

## Concepts

Biot–Savart for a current element: \(\mathrm{d}\mathbf{B}=\frac{\mu_0}{4\pi}\frac{I\mathrm{d}\mathbf{l}\times\mathbf{a}_R}{R^2}\). Superposition along a wire, or \(\mathbf{J}\,\mathrm{d}v\) for volume current. Direction: right-hand rule. Infinite straight wire: \( B=\mu_0 I/(2\pi\rho) \). Circular loop on axis: \( B_z=\mu_0 I a^2/2(a^2+z^2)^{3/2} \). Finite straight segment: \( B=(\mu_0 I/(4\pi\rho))(\sin\alpha_1+\sin\alpha_2) \).

Ampère: \(\oint\mathbf{H}\cdot\mathrm{d}\mathbf{l}=I_{\mathrm{enc,free}}\). Differential \(\nabla\times\mathbf{H}=\mathbf{J}_{\mathrm{free}}\). Use when \(\mathbf{H}\) is tangential and constant on a circle (infinite line, infinite coaxial, infinite solenoid, toroid). Infinite solenoid: \( H=nI \) inside, 0 outside (ideal). Toroid: \( H_\phi=NI/(2\pi\rho) \) inside the core, approximately \( NI/\ell_{\mathrm{mean}} \). Coax: \( H_\phi=I/(2\pi\rho) \) between conductors.

\(\nabla\cdot\mathbf{B}=0\): no magnetic charge, flux lines close. Integral \(\oint\mathbf{B}\cdot\mathrm{d}\mathbf{S}=0\) on any closed surface.

Vector potential: \(\mathbf{B}=\nabla\times\mathbf{A}\), Coulomb gauge \(\nabla\cdot\mathbf{A}=0\), then \(\nabla^2\mathbf{A}=-\mu\mathbf{J}\) (magnetostatic Poisson). Line current: \(\mathbf{A}=\frac{\mu_0 I}{4\pi}\int\mathrm{d}\mathbf{l}/R\) parallel to the current. \(\mathbf{A}\) is not unique (gauge); \(\mathbf{B}\) is. Faraday’s law in terms of \(\mathbf{A}\) is \(\mathbf{E}=-\nabla V-\partial\mathbf{A}/\partial t\) (next units).

Force: Lorentz \( \mathbf{F}=q(\mathbf{E}+\mathbf{v}\times\mathbf{B}) \), on a wire \( I\oint\mathrm{d}\mathbf{l}\times\mathbf{B} \). Two parallel wires: \( F/L=\mu_0 I_1 I_2/(2\pi d) \), attract if currents same direction (SI ampere historically). Torque on a magnetic dipole \(\mathbf{m}=I\mathbf{S}\) is \(\mathbf{m}\times\mathbf{B}\).

Materials: magnetization \(\mathbf{M}\), \(\mathbf{B}=\mu_0(\mathbf{H}+\mathbf{M})\), bound currents \(\mathbf{J}_b=\nabla\times\mathbf{M}\), \(\mathbf{K}_b=\mathbf{M}\times\mathbf{n}\). Linear \(\mathbf{B}=\mu\mathbf{H}\), \(\mu_r=1+\chi_m\). Diamagnetic \(\chi_m\) tiny negative, paramagnetic tiny positive, ferromagnetic huge and nonlinear (hysteresis, measurements pack unit 07). Inside a long solenoid filled with linear \(\mu\), \( B=\mu n I \), \( H=nI \) (from free current).

Boundary: \(\mathbf{n}\cdot(\mathbf{B}_1-\mathbf{B}_2)=0\) (normal \( B \) continuous). \(\mathbf{n}\times(\mathbf{H}_1-\mathbf{H}_2)=\mathbf{K}_{\mathrm{free}}\) (tangential \( H \) jumps by free surface current). At a high-\(\mu\) interface, \(\mathbf{B}\) is nearly normal in the air, like electrostatic \(\mathbf{E}\) near a conductor — magnetic circuit approximation (machines pack).

Magnetic circuits: \(\mathcal{F}=NI=\Phi\mathcal{R}\), \(\mathcal{R}=\ell/(\mu A)\). Leakage and fringing are the error terms. Not a substitute for \(\mathbf{B}\) in a gap when the gap is large.

## Equations

Biot–Savart:

\[
\mathbf{B}=\frac{\mu_0}{4\pi}\int\frac{I\mathrm{d}\mathbf{l}\times\mathbf{a}_R}{R^2}.
\]

Ampère:

\[
\oint\mathbf{H}\cdot\mathrm{d}\mathbf{l}=I_{\mathrm{enc}},\qquad \nabla\times\mathbf{H}=\mathbf{J}.
\]

Infinite line / solenoid / loop on axis:

\[
H_\phi=\frac{I}{2\pi\rho},\qquad H_z=nI\ \mathrm{(inside)},\qquad
B_z=\frac{\mu_0 I a^2}{2(a^2+z^2)^{3/2}}.
\]

\(\nabla\cdot\mathbf{B}=0\), \(\mathbf{B}=\nabla\times\mathbf{A}\).

Force per length, parallel wires:

\[
\frac{F}{L}=\frac{\mu_0 I_1 I_2}{2\pi d}.
\]

Linear media: \(\mathbf{B}=\mu\mathbf{H}\). Energy density \( \frac12\mathbf{B}\cdot\mathbf{H} \) (linear).

## Methods

Symmetry → Ampère. Otherwise Biot–Savart with a parameterized \(\mathrm{d}\mathbf{l}\). Check dimensions: \(\mu_0=4\pi\times 10^{-7}\), so \(\mu_0/(2\pi)=2\times 10^{-7}\), a 1 A wire at 1 m has \( B=2\times 10^{-7} \) T.

For \(\mathbf{A}\), integrate like the electric potential but a vector; then curl. For a straight wire along z, \(\mathbf{A}= -(\mu_0 I/(2\pi))\ln\rho\,\mathbf{a}_z \) (up to constants).

Magnetic circuit: series reluctances add; a gap \(\ell_g/(\mu_0 A)\) often dominates iron \(\ell_i/(\mu A)\).

## Mistakes

Ampère on a square loop of wire “by symmetry.”

Using \( B=\mu_0 I/(2\pi\rho) \) inside a wire without integrating enclosed current (uniform \( J \): \( B\propto\rho \) inside).

Confusing \( n \) turns per metre with \( N \) total on a toroid of length \( \ell \): \( H=NI/\ell=nI \).

\(\nabla\cdot\mathbf{H}=0\) always (false if \(\mathbf{M}\) has divergence; \(\nabla\cdot\mathbf{B}=0\) always).

Right-hand rule sign errors that reverse force (attraction vs repulsion).

Boundary: normal \( H \) continuous (no: normal \( B \)).

Solenoid \( B=\mu_0 NI \) with \( N \) total turns not per length.

A wire walk-through: 8.00 A, \(\rho=4.00\) cm, \( B=\mu_0 I/(2\pi\rho)=40.0 \) µT.

Solenoid: 800 turns/m, 0.50 A, air, \( B=\mu_0 n I=0.503 \) mT.

Toroid: \( N=400 \), \( I=2.0 \) A, mean \(\rho=8.0\) cm, \( H=400\times 2/(2\pi\times 0.08)=1592 \) A/m. If \(\mu_r=500 \), \( B=1.00 \) T.

Loop: \( a=10 \) cm, \( I=3 \) A, at centre \( B=\mu_0 I/(2a)=18.8 \) µT.

Parallel wires 10 cm apart, 5 A each, same direction: \( F/L=5.00\times 10^{-5} \) N/m attract.

Inside copper wire radius 2 mm, 10 A uniform: at 1 mm, \( I_{\mathrm{enc}}=2.5 \) A, \( B=\mu_0 2.5/(2\pi\times 0.001)=0.500 \) mT.

Vector potential check: curl of \( -\ln\rho\,\mathbf{a}_z \) in cylindrical is \( (1/\rho)\mathbf{a}_\phi \), matching the line field.

Finite segment: 90° at each end, \(\rho=5\) cm, \( I=12 \) A, \( B=\mu_0 I(\sin 90+\sin 90)/(4\pi\rho)=48.0 \) µT.


Ampère’s law, used properly, is a flux of \(\mathbf{J}\) through any surface spanning the loop. For a coaxial return, a circle of radius \(\rho\) between conductors encloses the inner current only. Outside the sheath, enclosed current is zero if the return is equal and opposite — \( H=0 \) outside an ideal coax, which is why coax does not make a large external magnetostatic field.

Solenoid corrections: a finite solenoid has \( B \) leaking at the ends; on axis \( B_z=(\mu_0 n I/2)(\cos\beta_1-\cos\beta_2) \) in the usual angle notation. At the end of a long solenoid, \( B\approx \frac12\mu_0 n I \). UG “infinite solenoid” is the interior of a long dense winding.

Biot–Savart for a square loop: four finite segments. At the centre, each side of length \( a \) at distance \( a/2 \) with 90°+90° gives \( B=8\mu_0 I/(4\pi a\sqrt{2})=2\sqrt{2}\mu_0 I/(\pi a) \). Do not treat a square as a circle of equal area unless the problem allows an approximation.

Magnetic scalar potential: in a current-free simply connected region, \(\mathbf{H}=-\nabla V_m \), Laplace for \( V_m \). A loop of current makes \( V_m \) multi-valued (the 4π steradian jump). Use \(\mathbf{A}\) or Biot–Savart instead around currents.

Bound currents: a uniformly magnetized bar has \(\mathbf{J}_b=0\), \(\mathbf{K}_b=\mathbf{M}\times\mathbf{n}\), equivalent to a solenoid of surface current \( M \). That is why \( B=\mu_0(H+M) \) inside and the exterior dipole field looks like a solenoid’s.

Magnetic circuits with an air gap: \(\Phi\) continues (approximately), \( H_i\ell_i+H_g\ell_g=NI \), \( B_g\approx B_i \) if no leakage and same area, \( H_g=B_g/\mu_0 \). Almost all ampere-turns drop across the gap. Fringing: use \( A_g>A_i \) as a crude correction, or ignore if the problem does.

Force between two coaxial loops (far): dipole–dipole. Near: numerical Biot–Savart. UG often wants only the parallel-wire force.

Vector potential of a spinning charged sphere or a solenoid: \(\mathbf{A}\) azimuthal. \(\mathbf{B}=\nabla\times\mathbf{A}\) recovers the interior uniform \( B \) of a long solenoid if you take the infinite limit.

Units drill: 1 tesla is a large laboratory iron-core field. Earth’s field ~50 µT. A 1 A wire at 1 cm is 20 µT. MRI is a few tesla. Never quote \( H \) in tesla.

Boundary at \(\mu\to\infty\) iron: \( H_t\approx 0 \) in the iron, so \(\mathbf{H}\) in the air gap meets the iron normally (like \(\mathbf{E}\) on a conductor). Magnetic field lines prefer high \(\mu\).

Steady current in a wire of finite conductivity: \(\mathbf{J}=\sigma\mathbf{E}\) inside, magnetostatics for \(\mathbf{B}\) from \(\mathbf{J}\), electrostatics for the surface charge that keeps \(\mathbf{J}\) along a bend. The surface charge is tiny and is not needed to compute \( B \) of a long straight wire.

Energy \(\frac12\int\mathbf{B}\cdot\mathbf{H}\,\mathrm{d}v\) in linear media equals \(\frac12 LI^2\). In a gapped inductor the energy is mostly in the gap (\( H \) huge, \(\mu_0\)). Pulling the gap closed releases energy (relay).

Ampère-Maxwell without displacement is this unit: do not put \(\varepsilon\partial E/\partial t\) into a DC coax problem.

Worked toroid with a gap: \( N=200 \), \( I=1 \) A, \(\ell_i=20\) cm, \(\ell_g=1\) mm, \( A=2 \) cm², \(\mu_r=800\). Reluctance iron \( \ell_i/(\mu A)=0.0995\times 10^7 \), gap \( \ell_g/(\mu_0 A)=3.98\times 10^6 \), gap dominates. \(\Phi=NI/\mathcal{R}\approx 5.0\times 10^{-5}\) Wb, \( B_g\approx 0.25 \) T.

Worked finite wire: from \(\alpha_1=30^\circ\) to \(\alpha_2=90^\circ\), \(\rho=4\) cm, \( I=20 \) A, \( B=\mu_0 I(\sin 30+\sin 90)/(4\pi\rho)=25+50=75 \) µT times \( 10^{-7}/0.04 \) wait: \(\mu_0/(4\pi)=10^{-7}\), \( 10^{-7}\times 20/0.04 \times 1.5=75 \) µT.

Worked loop pair: Helmholtz coils, two loops of radius \( a \), spacing \( a \), uniform-ish field at the centre \( B= (8\mu_0 N I)/(a\sqrt{125}) \). A lab formula; derive only if asked.

Right-hand rule for \(\mathbf{B}\) around a wire: thumb current, fingers \(\mathbf{B}\). Force \(\mathbf{I}\times\mathbf{B}\): a wire in a \(\mathbf{B}\) into the page, current right, force up. Motors are that, generators are Faraday (next unit).

If a problem gives \(\mathbf{A}\), compute \(\mathbf{B}=\nabla\times\mathbf{A}\) in the stated coordinates with scale factors. Example \(\mathbf{A}=k\rho\mathbf{a}_z\), cylindrical curl \( -k\mathbf{a}_\phi \). If they ask \(\nabla\cdot\mathbf{A}\) in Coulomb gauge, it should be 0; if not, a gauge transform can subtract \(\nabla\chi\).

Magnetostatics stops when \(\partial\mathbf{D}/\partial t\) matters or when \(\mathbf{B}\) changes and Faraday electric fields appear. A slowly ramped solenoid is still approximately magnetostatic if the displacement current and induced \( E \) are negligible compared with \( J \) and the intended \( B \).


One more Ampère loop that is not a circle: a rectangular path around a sheet current \(\mathbf{K}=K\mathbf{a}_x\) on the plane \( z=0 \). Tangential \( H \) jumps by \( K \), each side \( K/2 \) if the sheet is isolated and symmetric, analogous to the infinite charged sheet’s \( E=\rho_S/(2\varepsilon_0) \). A ground plane under a microstrip is the return; the fields are not exactly that simple, but the jump BC is exact.

Inductance preview from energy: \( L=2W/I^2 \) with \( W=\frac12\int B H\,\mathrm{d}v \). For a long solenoid this recovers \( L=\mu n^2 A\ell \). For a coax it recovers \( L'=(\mu/2\pi)\ln(b/a) \) plus internal inductance if you integrate inside the inner conductor. Energy is sometimes easier than flux linkage when the path of “the” current is ambiguous.

If iron saturates, \(\mu\) is not a constant, superposition fails, and \( B=\mu_0(H+M) \) with a nonlinear \( M(H) \) from a B–H loop (measurements unit 07). Magnetostatics in motors is that nonlinear world; this unit’s linear \(\mu_r\) is the exam default unless a loop is given.

List, before leaving: Biot–Savart, Ampère, \(\nabla\cdot B=0\), \(\mathbf{B}=\nabla\times\mathbf{A}\), parallel-wire force, solenoid and toroid \( H \), boundary jumps, linear \(\mu\). Faraday is next; do not induce an emf with a DC current at rest.
