# Electrostatics: Coulomb, Gauss, potential, Poisson

Electrostatics is Maxwell with no time variation and no magnetic field: \(\nabla\cdot\mathbf{D}=\rho_v\), \(\nabla\times\mathbf{E}=0\). The two working tools are Coulomb’s law (superposition of point charges) and Gauss’s law (symmetry). Potential \( V \) turns a conservative \(\mathbf{E}\) into a scalar problem, and Poisson’s equation \(\nabla^2 V=-\rho_v/\varepsilon\) is that scalar problem in a linear dielectric. This unit stays in free space or a uniform \(\varepsilon\); conductors, interfaces, and capacitors are the next unit.

## Concepts

Coulomb: two point charges in free space, force on \( q_1 \) due to \( q_2 \) is \( \mathbf{F}_{12}=\frac{1}{4\pi\varepsilon_0} \frac{q_1 q_2}{R^2}\mathbf{a}_{R} \) with \(\mathbf{R}=\mathbf{r}_1-\mathbf{r}_2\). Electric field \(\mathbf{E}=\mathbf{F}/q\) on a test charge. Superposition holds because Maxwell is linear in free space. Continuous distributions: line \(\rho_L\), surface \(\rho_S\), volume \(\rho_v\), with \(\mathrm{d}q=\rho_L\mathrm{d}\ell=\rho_S\mathrm{d}S=\rho_v\mathrm{d}v\). The field integral is \(\mathbf{E}(\mathbf{r})=\frac{1}{4\pi\varepsilon_0}\int\frac{\mathrm{d}q}{R^2}\mathbf{a}_R\). You almost never want to do this in Cartesian for a sphere; use Gauss or potential.

Gauss’s law: \(\oint\mathbf{D}\cdot\mathrm{d}\mathbf{S}=Q_{\mathrm{enc}}\) with \(\mathbf{D}=\varepsilon_0\mathbf{E}\) in free space. Differential form \(\nabla\cdot\mathbf{D}=\rho_v\). Useful Gauss surfaces exist when \(\mathbf{D}\) is constant on pieces of a closed surface by symmetry: infinite plane, infinite line, sphere of spherical charge, infinite cylinder of cylindrical charge. If the symmetry is not there, Gauss is still true and still useless as a computational shortcut.

Potential: \(\mathbf{E}=-\nabla V\) because \(\nabla\times\mathbf{E}=0\). \( V(\mathbf{r})-V(\mathbf{r}_0)=-\int_{\mathbf{r}_0}^{\mathbf{r}}\mathbf{E}\cdot\mathrm{d}\mathbf{l} \). Reference: infinity for localized charges, so \( V=\frac{1}{4\pi\varepsilon_0}\int\mathrm{d}q/R \). For infinite line or plane, infinity is not a usable zero (potential diverges); set \( V=0 \) on a convenient cylinder or plane. Absolute \( V \) is conventional; differences are physical (work per unit charge). Equipotential surfaces, field lines perpendicular to them. A conductor in electrostatics is an equipotential (next unit).

Energy: assembling charges, \( W=\frac12\int\rho_v V\mathrm{d}v=\frac{\varepsilon_0}{2}\int E^2\mathrm{d}v \) (free space, including the field in all space). The factor \( 1/2 \) is not optional; it avoids double-counting. Force on a conductor can be found from \(\mathrm{d}W\) at constant \( Q \) or constant \( V \).

Dipole: \( \mathbf{p}=q\mathbf{d} \) from \( -q \) to \( +q \). Far field \( V=\frac{1}{4\pi\varepsilon_0}\frac{\mathbf{p}\cdot\mathbf{a}_r}{r^2} \), \( \mathbf{E} \) falls as \( 1/r^3 \). Polarization of materials is a density of dipoles (unit 03).

Poisson and Laplace: \(\nabla\cdot(\varepsilon\nabla V)=-\rho_v\), so Laplace \(\nabla^2 V=0\) in charge-free linear uniform media. Uniqueness: with \( V \) specified on the entire boundary (Dirichlet), or the normal derivative (Neumann) up to a constant, the solution is unique. That is why you may guess a potential that satisfies Laplace and the BCs and stop. Separation of variables in Cartesian (parallel-plate with a variation), cylindrical (coax, corner), spherical (conducting sphere in a uniform field) is the UG PDE toolkit. Method of images is uniqueness in disguise: replace a conductor by charges that enforce \( V=\mathrm{const} \) on the surface, solve in the region of interest only.

Infinite line: \( \mathbf{E}=\frac{\rho_L}{2\pi\varepsilon_0\rho}\mathbf{a}_\rho \). Infinite sheet: \( \mathbf{E}=\frac{\rho_S}{2\varepsilon_0}\mathbf{a}_n \) (each side, pointing away if \(\rho_S>0\)). Point: Coulomb. Sphere of uniform \(\rho_v\): inside \( E\propto r \), outside as a point charge at the centre.

Electric flux density \(\mathbf{D}\) is the convenient Gauss vector when \(\varepsilon\) is piecewise constant. In free space \(\mathbf{D}=\varepsilon_0\mathbf{E}\). Units: C/m² versus V/m.

Work and path: moving \( q \) in a static \(\mathbf{E}\) is path-independent. A closed loop of electrostatic field does no net work. (Faraday will break that for time-varying \(\mathbf{B}\).)

## Equations

Coulomb field of a point charge at the origin:

\[
\mathbf{E}=\frac{q}{4\pi\varepsilon_0 r^2}\mathbf{a}_r.
\]

Gauss:

\[
\oint_S\mathbf{D}\cdot\mathrm{d}\mathbf{S}=Q_{\mathrm{enc}}=\int_V\rho_v\mathrm{d}v,\qquad \nabla\cdot\mathbf{D}=\rho_v.
\]

Potential:

\[
\mathbf{E}=-\nabla V,\qquad V=\frac{1}{4\pi\varepsilon_0}\int\frac{\mathrm{d}q}{R}\quad(\text{ref. at }\infty).
\]

Poisson / Laplace:

\[
\nabla^2 V=-\frac{\rho_v}{\varepsilon},\qquad \nabla^2 V=0.
\]

Energy:

\[
W=\frac{\varepsilon}{2}\int_V E^2\mathrm{d}v.
\]

Infinite line / sheet:

\[
E_\rho=\frac{\rho_L}{2\pi\varepsilon\rho},\qquad E_n=\frac{\rho_S}{2\varepsilon}.
\]

Uniform sphere radius \( a \), total \( Q \):

\[
E(r)=\frac{Q r}{4\pi\varepsilon a^3}\ (r<a),\qquad \frac{Q}{4\pi\varepsilon r^2}\ (r>a).
\]

Image of \( q \) at height \( d \) above a grounded plane \( z=0 \): \( -q \) at \( z=-d \), valid for \( z>0 \). Force on \( q \): attraction \( \frac{1}{4\pi\varepsilon_0}\frac{q^2}{(2d)^2} \).

Dipole far potential: \( V=\frac{p\cos\theta}{4\pi\varepsilon_0 r^2} \).

## Methods

Always ask: is there a Gauss surface? If yes, sketch \(\mathbf{D}\) direction from symmetry, evaluate \( Q_{\mathrm{enc}} \), solve. If no, write Coulomb or potential integrals, or Laplace + BC.

Potential first when the distribution is given and you need \(\mathbf{E}\) with a messy direction: scalar integral, then gradient. Field first when Gauss applies.

Images: grounded plane, grounded sphere (Kelvin image), line parallel to a cylinder, dielectric half-space (harder). Never put the image charge in the region where you want the field.

Laplace in 1D: parallel plates \( V=V_0 x/d \), \( E=V_0/d \). Coax \( V=A\ln\rho+B \). Spherical shells \( V=A/r+B \). Fit two constants to two electrodes.

Check units: \(\varepsilon_0=8.854\times 10^{-12}\) F/m, \( 1/(4\pi\varepsilon_0)=9\times 10^9 \). A nC at 1 m is 9 V, not 9 kV.

## Mistakes

Gauss on a cube of charge “because Gauss’s law is always true” and assuming \( E \) constant on the cube.

Using \(\mathbf{E}=\sigma/(2\varepsilon_0)\) just outside a conductor (that is \(\sigma/\varepsilon_0\) for the conductor surface; \( 2\varepsilon_0 \) is the infinite sheet in free space).

Reference at infinity for an infinite line.

Forgetting superposition of two sheets.

Poisson with \(\nabla^2 V=+\rho/\varepsilon\) (sign).

Image charge used on both sides of a grounded plane.

Integrating Coulomb with \(\mathbf{a}_R\) treated as constant when it is not.

Energy \(\int\varepsilon E^2\) without \( 1/2 \).

A line-charge walk-through: \(\rho_L=20\) nC/m on the z-axis. At \(\rho=0.5\) m, \( E=20\times 10^{-9}/(2\pi\varepsilon_0\times 0.5)=720 \) V/m radial.

Sheet: \(\rho_S=2\) nC/m², \( E=\rho_S/(2\varepsilon_0)=113 \) V/m each side.

Sphere: \( Q=4 \) nC uniform in \( a=2 \) cm. Outside at 5 cm, \( E=9e9\times 4e-9/0.05^2=14.4 \) kV/m. Inside at 1 cm, \( E_{\mathrm{in}}=E_{\mathrm{out,surface}}\times r/a \) wait: surface \( E(a)=9e9\times 4e-9/0.02^2=90 \) kV/m, inside \( 90\times(0.01/0.02)=45 \) kV/m.

Potential of a point 5 nC at 30 cm: \( V=9e9\times 5e-9/0.3=150 \) V.

Image: \( q=8 \) nC, \( d=4 \) cm above ground. Force \( 9e9\times 64\times 10^{-18}/0.08^2=90 \) µN toward the plane.

Laplace coax: \( a=1 \) cm, \( b=3 \) cm, \( V(a)=50 \) V, \( V(b)=0 \). \( V(\rho)=50\ln(b/\rho)/\ln(b/a) \). \( E=50/(\rho\ln 3) \). At \(\rho=2\) cm, \( E=2.28 \) kV/m.

Energy of a isolated sphere: \( W=Q^2/(8\pi\varepsilon a) \), same as \( \frac12 QV \) with \( V=Q/(4\pi\varepsilon a) \).

Dipole \( p=2\times 10^{-12} \) C·m, \( r=10 \) cm, \(\theta=0\): \( V=9e9\times 2e-12/0.01=1.8 \) V.

Uniqueness reminder: two different-looking image sets that both keep a sphere at \( V=0 \) and match the exterior charges must give the same exterior field. If they do not, one of them is wrong, not uniqueness.


More Gauss surfaces that actually work. Infinite cylindrical shell of radius \(a\), surface charge \(\rho_S\): outside like a line \(\rho_L=2\pi a\rho_S\), inside \(E=0\) (no enclosed charge for \(\rho<a\)). Two parallel sheets \(\pm\rho_S\): field between \( \rho_S/\varepsilon_0 \) (the conductor-pair analog), outside 0 if they are equal-and-opposite. A uniformly charged infinite slab of thickness \(2d\) and volume density \(\rho_v\): inside, \( E_x=\rho_v x/\varepsilon_0 \) if \( x=0 \) is the midplane; outside, like a sheet of \(\rho_S=2\rho_v d\).

Potential of a ring of charge \(Q\), radius \(a\), on the axis: \( V=Q/(4\pi\varepsilon_0\sqrt{z^2+a^2}) \), then \( E_z=-\mathrm{d}V/\mathrm{d}z \). At the centre \( E=0 \) by symmetry but \( V \) is not zero. Never infer \( E=0 \) from a statement that someone chose \( V=0 \) at that point; \( V=0 \) is a reference, \( E=0 \) is a field.

Poisson 1-D between plates with a volume charge: \(\mathrm{d}^2V/\mathrm{d}x^2=-\rho/\varepsilon\), integrate twice, two BCs. Linear \( E \) if \(\rho\) uniform. Space-charge-limited diodes are this story with \(\rho\) related to current; UG electrostatics stops at prescribed \(\rho_v\).

Energy of a collection of point charges \( W=\frac12\sum q_i V_i \) with \( V_i \) the potential due to all others (or all including a self-energy debate: omit self for point charges, include \(\frac{\varepsilon}{2}\int E^2\) for continuous). Isolated sphere \( W=Q^2/(8\pi\varepsilon a) \) is the self-energy of a continuous surface charge.

Images: line charge \(\rho_L\) parallel to a grounded cylinder, or a point and a grounded sphere \( q'=-qa/d \), \( d'=a^2/d \). The sphere image is worth one derivation: it makes \( V=0 \) on \( r=a \). Force on \( q \) is the force toward \( q' \), not the field of the sphere’s actual induced \(\rho_S\) computed the hard way — but that force is equal.

Laplace uniqueness implies that if you have already satisfied the BCs, extra image charges outside the region of interest are not to be used inside. Students sometimes add the image and then also keep a surface charge integral in the same region, double-counting.

Dielectric sphere in a uniform field (preview of unit 03): induced dipole, field inside uniform. Mention only; the BC matching is the next unit’s method.

A numerical Coulomb sum: three 2 nC charges at \((0,0,0)\), \((1,0,0)\), \((0,1,0)\) metres. Potential at \((0,0,1)\) is \( 9e9\times 2e-9\times(1+1/\sqrt{2}+1/\sqrt{2})=18+18\sqrt{2}=43.5 \) V. Field by vector superposition; do not add magnitudes.

Checking Gauss numerically: flux of a point charge through a cube not centred on the charge is \( Q/\varepsilon_0 \) if the charge is inside, 0 if outside, and \( Q/(2\varepsilon_0) \) only for very special “charge in a face” limits that are not well-posed (the charge is not inside or outside). Do not assign \( Q/6\varepsilon_0 \) unless the charge is at the centre of a cube (by symmetry then each face \( Q/6\varepsilon_0 \)). Off-centre, faces are unequal; the total is still \( Q/\varepsilon_0 \).

Work to move \( q \) from A to B is \( q(V_B-V_A) \) for a positive test charge gaining PE when going to higher \( V \). The field does work \( q\int\mathbf{E}\cdot\mathrm{d}\mathbf{l}=q(V_A-V_B) \). Sign fights are usually this pair reversed.

Infinite line potential: \( V=-(\rho_L/(2\pi\varepsilon))\ln(\rho/\rho_0) \). Difference between 1 m and 2 m is \( (\rho_L/(2\pi\varepsilon))\ln 2 \), finite. Absolute \( V(\infty) \) is not.

When superposition of Gauss pieces: the field of a uniformly charged sphere plus a spherical cavity is the full sphere minus a sphere of the cavity’s charge density (equivalent to a superposition of \( +\rho \) and \( -\rho \)). The field in the cavity of a uniformly charged body with a spherical hole is uniform if the hole is carved from a uniform \(\rho_v\) of an otherwise uniform large body — a standard trick.

Exam speed: if the word “symmetry” appears, try Gauss before Coulomb. If “grounded plane” appears, image. If “between coaxial cylinders” appears, Laplace or Gauss with \( Q \) on the inner. If “find work”, use \(\Delta V\), not a path-by-path \(\mathbf{E}\cdot\mathrm{d}\mathbf{l}\) unless asked.
