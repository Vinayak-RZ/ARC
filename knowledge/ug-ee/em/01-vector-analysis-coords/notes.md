# Vector analysis and coordinate systems

Electromagnetics is vector calculus with physical units. Before Coulomb or Faraday, you need points, unit vectors, dot and cross products, gradient, divergence, curl, and the three coordinate systems a first course actually uses: Cartesian, cylindrical, and spherical. This unit is the toolkit. Identities are not decoration: Gauss’s and Stokes’s theorems are how Maxwell’s equations switch between integral and differential form (unit 06). Orthogonal curvilinear scale factors are how you compute a line integral on a circular arc without inventing a new algebra.

## Concepts

A vector field \(\mathbf{A}(x,y,z)\) assigns a vector to each point. Scalars (potential, temperature) assign a number. Unit vectors in Cartesian \(\mathbf{a}_x,\mathbf{a}_y,\mathbf{a}_z\) are constant; in cylindrical \(\mathbf{a}_\rho,\mathbf{a}_\phi,\mathbf{a}_z\) the \(\mathbf{a}_\rho\) and \(\mathbf{a}_\phi\) change with \(\phi\); in spherical \(\mathbf{a}_r,\mathbf{a}_\theta,\mathbf{a}_\phi\) all but the idea of \(\mathbf{a}_\phi\) “around z” change with position. Differentiating a cylindrical vector field therefore hits extra terms: \(\partial\mathbf{a}_\rho/\partial\phi=\mathbf{a}_\phi\), \(\partial\mathbf{a}_\phi/\partial\phi=-\mathbf{a}_\rho\). If you treat \(\mathbf{a}_\rho\) as constant you will drop the \(A_\phi/\rho\) pieces of divergence and curl.

Position vector \(\mathbf{r}=x\mathbf{a}_x+y\mathbf{a}_y+z\mathbf{a}_z=\rho\mathbf{a}_\rho+z\mathbf{a}_z=r\mathbf{a}_r\). Displacement \(\mathrm{d}\mathbf{l}\) is the thing you integrate for work and for Faraday loops: Cartesian \(\mathrm{d}x\mathbf{a}_x+\mathrm{d}y\mathbf{a}_y+\mathrm{d}z\mathbf{a}_z\); cylindrical \(\mathrm{d}\rho\mathbf{a}_\rho+\rho\mathrm{d}\phi\mathbf{a}_\phi+\mathrm{d}z\mathbf{a}_z\); spherical \(\mathrm{d}r\mathbf{a}_r+r\mathrm{d}\theta\mathbf{a}_\theta+r\sin\theta\mathrm{d}\phi\mathbf{a}_\phi\). Surface elements: \(\mathrm{d}\mathbf{S}=\mathbf{n}\,\mathrm{d}S\) with \(\mathrm{d}S\) the scale-factor product (e.g. \(\rho\,\mathrm{d}\phi\,\mathrm{d}z\) on a cylinder). Volume \(\mathrm{d}v=\mathrm{d}x\,\mathrm{d}y\,\mathrm{d}z=\rho\,\mathrm{d}\rho\,\mathrm{d}\phi\,\mathrm{d}z=r^2\sin\theta\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}\phi\).

Dot product \( \mathbf{A}\cdot\mathbf{B}=AB\cos\psi \) is a scalar; work \( \mathrm{d}W=q\mathbf{E}\cdot\mathrm{d}\mathbf{l} \). Cross product \(\mathbf{A}\times\mathbf{B}\) is perpendicular to both, right-handed, magnitude \( AB\sin\psi \); Lorentz force \( q\mathbf{v}\times\mathbf{B} \). Scalar triple product \(\mathbf{A}\cdot(\mathbf{B}\times\mathbf{C})\) is the parallelepiped volume; it is the determinant of components in an orthonormal basis.

Gradient \(\nabla f\) points toward fastest increase of \( f \); \( \mathrm{d}f=\nabla f\cdot\mathrm{d}\mathbf{l} \). Equipotentials are perpendicular to \(\nabla f\). Divergence \(\nabla\cdot\mathbf{A}\) is outward flux per volume; positive divergence is a source. Curl \(\nabla\times\mathbf{A}\) is circulation per area; the direction is the normal of a small paddle wheel that would spin in the field. Laplacian \(\nabla^2 f=\nabla\cdot\nabla f\). Vector Laplacian \(\nabla^2\mathbf{A}=\nabla(\nabla\cdot\mathbf{A})-\nabla\times\nabla\times\mathbf{A}\) (the identity used in the wave equation).

Gauss (divergence) theorem: \(\int_V(\nabla\cdot\mathbf{A})\,\mathrm{d}v=\oint_S\mathbf{A}\cdot\mathrm{d}\mathbf{S}\). Stokes: \(\int_S(\nabla\times\mathbf{A})\cdot\mathrm{d}\mathbf{S}=\oint_C\mathbf{A}\cdot\mathrm{d}\mathbf{l}\). If \(\nabla\cdot\mathbf{A}=0\) everywhere in a region, net flux through any closed surface in that region is zero (solenoidal). If \(\nabla\times\mathbf{A}=0\), the field is conservative on a simply connected region and \(\mathbf{A}=-\nabla f\) for a scalar \( f \). Helmholtz theorem (UG statement): a vector field that vanishes at infinity is determined by its divergence and curl.

Cylindrical coordinates \((\rho,\phi,z)\): \(\rho=\sqrt{x^2+y^2}\), \(\phi=\mathrm{atan2}(y,x)\), \( z=z \). Spherical \((r,\theta,\phi)\): \( r=|\mathbf{r}| \), \(\theta\) from \( +z \) (polar, \( 0\le\theta\le\pi \)), \(\phi\) azimuth. Do not swap \(\theta\) and \(\phi\) with the physics convention used in some maths books (where \(\theta\) is azimuth). EE electromagnetics uses \(\theta\) polar.

Singularities: \(\nabla\cdot(\mathbf{a}_r/r^2)=4\pi\delta(\mathbf{r})\) in the distributional sense — that is Gauss’s law for a point charge in one line. Naive componentwise divergence of \(\mathbf{a}_r/r^2\) is zero for \( r\neq 0 \). You must treat the origin separately (a pillbox or a distribution).

Del identities used constantly: \(\nabla\times\nabla f=0\), \(\nabla\cdot(\nabla\times\mathbf{A})=0\), \(\nabla\cdot(f\mathbf{A})=f\nabla\cdot\mathbf{A}+\mathbf{A}\cdot\nabla f\), \(\nabla\times(f\mathbf{A})=f\nabla\times\mathbf{A}+\nabla f\times\mathbf{A}\), \(\nabla(A\cdot B)\) and \(\nabla\times(\mathbf{A}\times\mathbf{B})\) expansions. Product rules are how you go from Maxwell plus constitutive laws to Poynting’s theorem.

Distance \( R=|\mathbf{r}-\mathbf{r}'| \) between field point \(\mathbf{r}\) and source \(\mathbf{r}'\). \(\nabla(1/R)=-\mathbf{a}_R/R^2\) where \(\nabla\) acts on \(\mathbf{r}\), and \(\nabla'(1/R)=+\mathbf{a}_R/R^2\). That pair is the engine of Coulomb and Biot–Savart.

Orthogonal curvilinear: scale factors \( h_1,h_2,h_3 \) so \(\mathrm{d}\ell_i=h_i\mathrm{d}u_i \). Cartesian all \( h=1 \). Cylindrical \( h_\rho=1 \), \( h_\phi=\rho \), \( h_z=1 \). Spherical \( h_r=1 \), \( h_\theta=r \), \( h_\phi=r\sin\theta \). Divergence and curl formulas in tables are just the curvilinear expressions; you can re-derive the cylindrical divergence from flux through a \(\Delta\rho,\Delta\phi,\Delta z\) box.

Phasors (later units): a time-harmonic vector field is the real part of \(\tilde{\mathbf{A}}e^{j\omega t}\). Curl and div pass onto the phasor. Do not take the magnitude of a complex vector as if it were a 3-vector RMS without defining polarization.

## Equations

Cartesian gradient, divergence, curl:

\[
\nabla f=\frac{\partial f}{\partial x}\mathbf{a}_x+\frac{\partial f}{\partial y}\mathbf{a}_y+\frac{\partial f}{\partial z}\mathbf{a}_z,
\]
\[
\nabla\cdot\mathbf{A}=\frac{\partial A_x}{\partial x}+\frac{\partial A_y}{\partial y}+\frac{\partial A_z}{\partial z},
\]
\[
\nabla\times\mathbf{A}=\begin{vmatrix}\mathbf{a}_x&\mathbf{a}_y&\mathbf{a}_z\\ \partial_x&\partial_y&\partial_z\\ A_x&A_y&A_z\end{vmatrix}.
\]

Cylindrical divergence and z-component of curl (the ones people drop):

\[
\nabla\cdot\mathbf{A}=\frac{1}{\rho}\frac{\partial(\rho A_\rho)}{\partial\rho}+\frac{1}{\rho}\frac{\partial A_\phi}{\partial\phi}+\frac{\partial A_z}{\partial z},
\]
\[
(\nabla\times\mathbf{A})_z=\frac{1}{\rho}\frac{\partial(\rho A_\phi)}{\partial\rho}-\frac{1}{\rho}\frac{\partial A_\rho}{\partial\phi}.
\]

Spherical:

\[
\nabla\cdot\mathbf{A}=\frac{1}{r^2}\frac{\partial(r^2 A_r)}{\partial r}+\frac{1}{r\sin\theta}\frac{\partial(\sin\theta A_\theta)}{\partial\theta}+\frac{1}{r\sin\theta}\frac{\partial A_\phi}{\partial\phi}.
\]

Line, surface, volume elements as above. Laplacian in Cartesian \( \nabla^2 f=f_{xx}+f_{yy}+f_{zz} \). In spherical, radial-only: \( \nabla^2 f=\frac{1}{r^2}\frac{\partial}{\partial r}(r^2\partial f/\partial r) \).

Identities:

\[
\nabla\times\nabla f=0,\qquad \nabla\cdot(\nabla\times\mathbf{A})=0,\qquad
\nabla\times\nabla\times\mathbf{A}=\nabla(\nabla\cdot\mathbf{A})-\nabla^2\mathbf{A}.
\]

Stokes and Gauss as stated. Solid angle: \( \oint\mathbf{a}_R\cdot\mathrm{d}\mathbf{S}/R^2=4\pi \) around a point inside.

Conversion: \( x=\rho\cos\phi=r\sin\theta\cos\phi \), \( y=\rho\sin\phi=r\sin\theta\sin\phi \), \( z=r\cos\theta \).

## Methods

Pick coordinates that match the boundaries: infinite line → cylindrical; point or sphere → spherical; planes and rectangular boxes → Cartesian. Write \(\mathrm{d}\mathbf{l}\) before integrating; many “I cannot set up the integral” failures are a missing scale factor \(\rho\mathrm{d}\phi\).

To test conservative: compute curl (if it exists and is zero on a simply connected domain). To test solenoidal: divergence. To evaluate a closed line integral of a conservative field: zero, do not grind.

When transforming a vector, transform components, not by substituting \( x=\rho\cos\phi \) into \( A_x\mathbf{a}_x \) and keeping \(\mathbf{a}_x\). Project: \( A_\rho=A_x\cos\phi+A_y\sin\phi \), etc.

Singular points: if a formula blows up at the origin, apply Gauss/Stokes to a small excluded surface and take a limit.

Unit-vector derivatives: when differentiating \(\mathbf{A}=A_\rho\mathbf{a}_\rho\) with respect to \(\phi\), include \( A_\rho\partial\mathbf{a}_\rho/\partial\phi \).

## Mistakes

Using \(\mathrm{d}\ell=\mathrm{d}\phi\) on a circle of radius \( a \) instead of \( a\mathrm{d}\phi \).

Spherical \(\theta\) versus cylindrical \(\phi\).

\(\nabla\cdot(\mathbf{a}_r/r^2)=0\) everywhere including the origin.

Taking curl in cylindrical with Cartesian formulas.

Writing \(\mathbf{a}_\rho\cdot\mathbf{a}_x=1\).

Path independence claimed in a region that wraps a line current (curl is zero off the line, but the domain is not simply connected: \(\oint\mathbf{B}\cdot\mathrm{d}\mathbf{l}=\mu_0 I\)).

Mixing \(\nabla\) acting on source versus field coordinates in \( R=|\mathbf{r}-\mathbf{r}'| \).

Treating \(\nabla^2\mathbf{A}\) componentwise in cylindrical as if it were Cartesian.

A gradient walk-through: \( V=10\rho\sin\phi \) (cylindrical). \(\nabla V=10\sin\phi\mathbf{a}_\rho+(10/\rho)\rho\cos\phi\mathbf{a}_\phi=10\sin\phi\mathbf{a}_\rho+10\cos\phi\mathbf{a}_\phi\). At \( (3, \pi/2, 0) \), \(\nabla V=10\mathbf{a}_\rho\).

Divergence: \(\mathbf{A}=3\rho\mathbf{a}_\rho\). \(\nabla\cdot\mathbf{A}=\frac{1}{\rho}\partial(\rho\cdot 3\rho)/\partial\rho=6\). Flux out of a cylinder \(\rho\le 2\), \( 0\le z\le 1 \): \( 6\times\text{volume}=6\times 4\pi=24\pi \). Direct flux: only the outer wall, \( A_\rho=6 \), area \( 2\pi\times 2\times 1=4\pi \), flux \( 24\pi \).

Curl of \(\mathbf{A}=(-y\mathbf{a}_x+x\mathbf{a}_y)/\rho^2 \) is zero for \(\rho\neq 0\) but Stokes on a loop around the z-axis is \( 2\pi \): the 2D dipole/vortex example parallel to \(\nabla\phi\).

Line integral of \(\mathbf{E}=-2r\mathbf{a}_r\) from \( r=1 \) to \( r=3 \) along any radial path: \( \int_1^3 -2r\,\mathrm{d}r=-8 \) V if \(\mathbf{E}\) is V/m. Angular paths at fixed \( r \) contribute nothing. Field is conservative (\(\nabla\times\mathbf{E}=0\) off origin, and we did not encircle a forbidden point in a way that matters here because we stayed on a simply connected radial-ish region not wrapping a line charge along \(\phi\)).

Scale-factor check: length of the equator of a sphere of radius \( a \) is \( \int_0^{2\pi} a\sin(\pi/2)\,\mathrm{d}\phi=2\pi a \), not \( 2\pi \).


Coordinate-system drills that should be automatic. Convert \(\mathbf{A}=3\mathbf{a}_x-4\mathbf{a}_y\) at the point \((0,2,0)\) to cylindrical. There \(\rho=2\), \(\phi=90^\circ\), \(\mathbf{a}_\rho=\mathbf{a}_y\), \(\mathbf{a}_\phi=-\mathbf{a}_x\), so \(A_\rho=-4\), \(A_\phi=-3\), \(A_z=0\). If you leave it as \(3\mathbf{a}_x-4\mathbf{a}_y\) while writing \(\rho,\phi\) limits on an integral, the integrand is in mixed bases and the integral is meaningless. Always project before integrating a vector in curvilinear coordinates.

Surface integrals: on \(\rho=a\), \(\mathrm{d}\mathbf{S}=a\,\mathrm{d}\phi\,\mathrm{d}z\,\mathbf{a}_\rho\). On \(z=\mathrm{const}\), cylindrical \(\mathrm{d}\mathbf{S}=\rho\,\mathrm{d}\rho\,\mathrm{d}\phi\,\mathbf{a}_z\). On a sphere \(r=a\), \(\mathrm{d}\mathbf{S}=a^2\sin\theta\,\mathrm{d}\theta\,\mathrm{d}\phi\,\mathbf{a}_r\). The most common missing factor is \(\sin\theta\) on a sphere or \(\rho\) on a disk. Compute the area as a check: sphere \(4\pi a^2\), disk \(\pi a^2\), cylinder side \(2\pi a h\).

Gradient in cylindrical of \(f=\rho^2\phi\) is \(2\rho\phi\mathbf{a}_\rho+\rho\mathbf{a}_\phi\), not \(2\rho\phi\mathbf{a}_\rho+\rho^2\mathbf{a}_\phi\) — the \(\phi\) derivative is divided by \(h_\phi=\rho\). That single scale factor is the difference between a correct \(\mathbf{E}=-\nabla V\) and a field that fails \(\nabla\times\mathbf{E}=0\).

Laplacian of \(1/r\) is zero for \(r\neq 0\) and \(-4\pi\delta(\mathbf{r})\) in the distributional sense (or \(-\delta(\mathbf{r})/\varepsilon_0\) stories depending on the \(4\pi\) convention). Poisson \(\nabla^2 V=-\rho/\varepsilon\) with a point charge is the same fact. If a problem asks \(\nabla^2(1/r)\) at a point not the origin, the answer is 0. If it asks the integral of \(\nabla^2(1/r)\) over a volume containing the origin, the answer is \(-4\pi\).

Stokes hygiene: the orientation of \(C\) and \(\mathbf{n}\) on \(S\) are right-handed. Reversing the loop sign-flips the circulation. For Faraday (later) that minus sign is already in the law; do not reverse the loop “to make Lenz work” on top of that.

Del acting on products in components is safer in Cartesian. In cylindrical, expand using the known identities rather than inventing \(\nabla\times(A_\rho\mathbf{a}_\rho)\) by treating \(\mathbf{a}_\rho\) as constant. A one-line check: the field \(\mathbf{A}=\rho\mathbf{a}_\phi\) has curl \(2\mathbf{a}_z\), the 2-D analog of rigid rotation; \(\oint A\cdot dl=2\times\mathrm{area}\) on a circle.

Unit-vector inner products: \(\mathbf{a}_r\cdot\mathbf{a}_\rho=\sin\theta\), \(\mathbf{a}_r\cdot\mathbf{a}_z=\cos\theta\), \(\mathbf{a}_\theta\cdot\mathbf{a}_z=-\sin\theta\). A spherical field \(\mathbf{a}_r\) is not purely radial in cylindrical \(\rho\). Decompose if you must mix systems; better not to mix.

Path independence test in practice: pick two paths, or compute curl. If curl is zero except on a line you enclosed, the line integral can be \(2\pi\) times a residue (the \(\nabla\phi\) / line-current prototype). Simply connected is a topology word with a physics meaning: you can shrink the loop to a point without leaving the region where the field is curl-free.

Numerical hygiene: \(\mathrm{atan2}(y,x)\) for \(\phi\), not \(\tan^{-1}(y/x)\) which loses the quadrant. \(\theta=\cos^{-1}(z/r)\) is unique in \([0,\pi]\). Points on the z-axis have undefined \(\phi\); do not evaluate \(\mathbf{a}_\phi\) there.

When an exam gives \(\mathbf{A}\) in mixed coordinates (“\(A_x=3\rho\)”), rewrite everything in one system before differentiating. Partial derivatives of \(\rho\) with respect to \(x\) are \(x/\rho\), not zero.

This unit’s job is that every later integral in the pack can be set up. If you cannot write \(\mathrm{d}\mathbf{l}\) on a circular arc, you cannot do Faraday on a loop. If you cannot write \(\mathrm{d}\mathbf{S}\) on a cylinder, you cannot do Gauss on a line charge. The identities \(\nabla\times\nabla f=0\) and \(\nabla\cdot(\nabla\times\mathbf{A})=0\) are why electrostatics has a scalar potential and magnetostatics a vector potential. Memorizing twelve curl formulas without a scale-factor derivation is how the \(\phi\) component of \(\nabla\times\mathbf{A}\) gets dropped under time pressure.
