# Vector calculus for EE

Vector calculus in UG electrical engineering is the language of electromagnetic fields (the em pack) and of energy-flow arguments in circuits (Tellegen is discrete; Poynting is continuous). This unit is grad, div, curl, the three classical integral theorems, and the coordinate expressions used to compute them in Cartesian, cylindrical, and spherical systems. The physics of Coulomb and Faraday is not proved here; the operators that appear in Maxwell’s equations are.

A scalar field \(V(x,y,z)\) in this course is often electric potential (volts). A vector field \(\mathbf{E}\) or \(\mathbf{H}\) or \(\mathbf{J}\) carries a direction at each point. Line, surface, and volume integrals convert local field statements into the integral Maxwell equations used in Gauss’s and Ampère’s laws. The main intellectual move is to match the theorem to the unknown: path-independent line integrals of a conservative field, flux through a closed surface of a divergence, circulation around a loop of a curl.

## Concepts

The gradient \(\nabla V\) is the unique vector field such that the directional derivative of \(V\) in direction \(\hat{u}\) is \(\nabla V\cdot\hat{u}\). Equivalently, \(\nabla V\) points toward fastest increase of \(V\), and \(|\nabla V|\) is that rate. In electrostatics \(\mathbf{E}=-\nabla V\) (sign: field points toward decreasing potential). Level surfaces \(V=\mathrm{const}\) are orthogonal to \(\mathbf{E}\). In Cartesian coordinates \(\nabla V=(\partial V/\partial x,\partial V/\partial y,\partial V/\partial z)\). In cylindrical and spherical systems the orthonormal basis vectors themselves depend on position; the component formulae pick up metric coefficients (\(1/\rho\), \(1/r\), \(1/(r\sin\theta)\)). Using Cartesian component formulae with cylindrical component names is a standard error.

Divergence \(\nabla\cdot\mathbf{A}\) is the net outward flux per unit volume. Gauss’s theorem (divergence theorem)
\[
\iiint_V (\nabla\cdot\mathbf{A})\,dV = \oiint_S \mathbf{A}\cdot d\mathbf{S}
\]
converts a volume integral of charge density into a flux of \(\mathbf{D}\) (or \(\mathbf{E}\) in free space). If \(\nabla\cdot\mathbf{A}=0\) everywhere in a region, net flux through every closed surface in that region is zero: no net source. Incompressible flow and solenoidal \(\mathbf{B}\) (\(\nabla\cdot\mathbf{B}=0\)) are this statement. At a point charge the distributional divergence is a Dirac delta; ordinary calculus sees \(\nabla\cdot\mathbf{E}=0\) away from the charge and a flux \(Q/\varepsilon_0\) on any surface enclosing it.

Curl \(\nabla\times\mathbf{A}\) is the circulation per unit area. Stokes’s theorem
\[
\iint_S (\nabla\times\mathbf{A})\cdot d\mathbf{S} = \oint_{\partial S} \mathbf{A}\cdot d\mathbf{\ell}
\]
converts Faraday’s and Ampère’s laws between loop and surface forms. If \(\nabla\times\mathbf{E}=0\) in a simply connected region, \(\mathbf{E}\) is conservative there: the line integral between two points is independent of path and equal to \(V(a)-V(b)\) if \(\mathbf{E}=-\nabla V\). Around a changing magnetic flux, \(\nabla\times\mathbf{E}\neq 0\); voltages around a loop of an inductor are not a single-valued potential in that sense. That is why lumped circuit theory assigns a voltage to a two-terminal element only after the magnetic field is packed into \(L\), not left as a stray.

The Laplacian \(\nabla^2 V=\nabla\cdot\nabla V\) appears in Poisson’s equation \(\nabla^2 V=-\rho/\varepsilon\). In source-free regions Laplace’s equation \(\nabla^2 V=0\) holds. Uniqueness theorems (specify \(V\) on the boundary, or the normal derivative, or a mix) are the mathematics behind solving capacitance problems by assuming a potential and checking Laplace plus boundaries. Separation of variables in Cartesian, cylindrical, and spherical coordinates produces sines, Bessel functions, and Legendre polynomials; UG EE usually stops at the Cartesian 1-D and coaxial logarithmic potentials, and maybe a 2-D rectangular slot.

Vector identities used constantly:
\[
\nabla\times\nabla V=0,\qquad \nabla\cdot(\nabla\times\mathbf{A})=0,
\]
\[
\nabla\cdot(V\mathbf{A})=\nabla V\cdot\mathbf{A}+V\nabla\cdot\mathbf{A},
\]
\[
\nabla\times(\nabla\times\mathbf{A})=\nabla(\nabla\cdot\mathbf{A})-\nabla^2\mathbf{A}
\]
(the last in Cartesian components, or with a carefully defined vector Laplacian). The first identity says a gradient field is irrotational; the second says a curl field is solenoidal. Helmholtz’s theorem (under decay hypotheses) reconstructs a vector field from its divergence and curl plus boundary data — the reason Maxwell’s equations plus constitutive laws determine the fields.

Coordinate systems: Cartesian \((x,y,z)\); cylindrical \((\rho,\phi,z)\) with \(\rho=\sqrt{x^2+y^2}\); spherical \((r,\theta,\phi)\) with \(\theta\) the polar angle from \(z\) (physics convention, used in em books). Cylindrical \(\hat{\rho},\hat{\phi}\) rotate with \(\phi\). Differentiating a vector given in cylindrical components therefore produces extra terms: \(\partial\hat{\rho}/\partial\phi=\hat{\phi}\), \(\partial\hat{\phi}/\partial\phi=-\hat{\rho}\). Those terms are why \(\nabla\times\mathbf{A}\) in cylindrical coordinates is not the Cartesian curl with names replaced.

Surface orientation: \(d\mathbf{S}=\hat{n}\,dS\) with right-hand rule matching the boundary orientation in Stokes. For a closed surface, \(\hat{n}\) is outward in the divergence theorem. Flipping \(\hat{n}\) flips the sign of flux. In coaxial cable Gauss surfaces, \(\hat{\rho}\) is the outward direction for a cylinder enclosing the inner conductor.

Line integrals \(\int_C \mathbf{A}\cdot d\mathbf{\ell}\) parametrize the path \(\mathbf{r}(t)\), \(t\in[a,b]\), and integrate \(\mathbf{A}(\mathbf{r}(t))\cdot\mathbf{r}'(t)\,dt\). Conservative fields: pick any convenient path, or evaluate \(V\) at the endpoints. Nonconservative fields: the path is part of the problem (a specified contour around a wire).

The fundamental theorem for gradients:
\[
\int_a^b \nabla V\cdot d\mathbf{\ell} = V(b)-V(a)
\]
is the scalar potential version of Stokes with a degenerate surface. Green’s identities come from the divergence theorem applied to \(U\nabla V\) and are used in uniqueness proofs and in some numerical field solvers (method of moments). UG EE needs the statement more than the proof.

Units: \(\nabla\) carries \(1/\mathrm{m}\). Divergence of \(\mathbf{D}\) has units of C/m\(^3\). Mixing millimetres in a coordinate with SI constants without conversion is a computation error, not a theorem error.

## Equations

Cartesian operators:

\[
\nabla V=\hat{x}\partial_x V+\hat{y}\partial_y V+\hat{z}\partial_z V,
\]
\[
\nabla\cdot\mathbf{A}=\partial_x A_x+\partial_y A_y+\partial_z A_z,
\]
\[
\nabla\times\mathbf{A}=\begin{vmatrix}\hat{x}&\hat{y}&\hat{z}\\\partial_x&\partial_y&\partial_z\\A_x&A_y&A_z\end{vmatrix}.
\]

Cylindrical (physics/EE):

\[
\nabla V=\hat{\rho}\partial_\rho V+\hat{\phi}\frac{1}{\rho}\partial_\phi V+\hat{z}\partial_z V,
\]
\[
\nabla\cdot\mathbf{A}=\frac{1}{\rho}\partial_\rho(\rho A_\rho)+\frac{1}{\rho}\partial_\phi A_\phi+\partial_z A_z.
\]

Spherical:

\[
\nabla V=\hat{r}\partial_r V+\hat{\theta}\frac{1}{r}\partial_\theta V+\hat{\phi}\frac{1}{r\sin\theta}\partial_\phi V.
\]

Divergence theorem, Stokes, gradient theorem: as in Concepts.

Laplacian, Cartesian:

\[
\nabla^2 V=\partial_{xx}V+\partial_{yy}V+\partial_{zz}V.
\]

Cylindrical Laplacian (scalar):

\[
\nabla^2 V=\frac{1}{\rho}\partial_\rho(\rho\partial_\rho V)+\frac{1}{\rho^2}\partial_{\phi\phi}V+\partial_{zz}V.
\]

Product and identities: see Concepts. Vector triple product and scalar triple product are used in \(\mathbf{A}\times(\mathbf{B}\times\mathbf{C})\) expansions of Lorentz force bookkeeping.

Poynting (preview, not proved): \(\mathbf{S}=\mathbf{E}\times\mathbf{H}\); \(\nabla\cdot\mathbf{S}\) relates to energy decrease in the fields plus \(\mathbf{J}\cdot\mathbf{E}\) dissipation via Poynting’s theorem, which is a divergence-theorem statement on \(\mathbf{E}\times\mathbf{H}\).

## Methods

Identify the coordinate system that matches the boundaries: coaxial and infinite line → cylindrical; point charge or spherical shell → spherical; parallel plates → Cartesian. Write the unknown field with the components that symmetry allows (no \(\phi\) component for a static line charge along \(z\), and no \(\phi\) dependence). Apply the integral theorem on a surface that symmetry makes trivial (flux = field times area, circulation = field times length).

To compute \(\nabla V\) in cylindrical coordinates, use the cylindrical formula, not the Cartesian one. Convert a given \(V(x,y,z)\) to Cartesian if the Cartesian gradient is easier, then convert the vector to cylindrical components if asked.

To test conservativeness of \(\mathbf{F}\) on a simply connected region, compute \(\nabla\times\mathbf{F}\) and see if it is identically zero. If it is, find \(V\) by integrating \(dV=-F_x dx-\cdots\) one variable at a time, adding functions of the remaining variables, as in exact differentials.

For a flux integral, parametrize the surface or use a projection: \(\mathbf{A}\cdot d\mathbf{S}=A_z\,dx\,dy\) on \(z=g(x,y)\) with care for the \(\hat{n}\) tilt (multiply by \(\sqrt{1+g_x^2+g_y^2}\) or use \(\mathbf{A}\cdot\hat{n}\,dS\) consistently). Closed-surface problems in UG EE are usually Gauss pills: cylinder, sphere, or pillbox at an interface.

At an interface, the pillbox argument gives the jump of the normal component of \(\mathbf{D}\) equal to free surface charge. The Stokes pill (a tiny loop) gives the jump of the tangential \(\mathbf{H}\) equal to free surface current. Those are integral theorems shrunk to zero thickness, not new operators.

When evaluating a line integral of a curl-free field, ignore the complicated path and use endpoints. When the field is not curl-free, do not.

Check dimensions after a curl: if \(\mathbf{A}\) was Wb/m (vector potential), curl has T. If a factor \(1/\rho\) was forgotten, units fail.

For Laplace in 1-D coaxial geometry, \(\frac{1}{\rho}\frac{d}{d\rho}(\rho dV/d\rho)=0\) integrates to \(V=A\ln\rho+B\). Fit two Dirichlet radii. Capacitance per length follows from \(Q=\varepsilon E_\rho\cdot 2\pi\rho\) at any \(\rho\) in the dielectric, independent of \(\rho\) because divergence-free.

A uniqueness check after a candidate field is cheap: verify the PDE (Laplace or Poisson) in the interior, the boundary values, and the decay or jump conditions. If two candidates both satisfy them, they differ by at most a constant when only \(\mathbf{E}\) is needed. That constant is fixed by choosing a reference node or a grounded conductor.

## Mistakes

Using \(\nabla\cdot\mathbf{A}=\sum\partial A_i/\partial x_i\) in cylindrical coordinates on cylindrical components. The divergence includes \(\frac{1}{\rho}\partial(\rho A_\rho)/\partial\rho\), not merely \(\partial A_\rho/\partial\rho\).

Setting \(d\mathbf{\ell}=d\rho\,\hat{\rho}+d\phi\,\hat{\phi}+dz\,\hat{z}\) without \(\rho\,d\phi\). The physical \(\phi\) increment is \(\rho\,d\phi\).

Confusing \(\theta\) and \(\phi\) in spherical coordinates with the mathematics convention that swaps them. EE/physics: \(\theta\) polar, \(\phi\) azimuthal.

Applying Stokes with inconsistent orientation: right-hand rule violated, sign of circulation reversed, Faraday emf sign flipped (Lenz fights you twice).

Treating a line integral of \(\mathbf{E}\) around a loop as \(V\) of a node when magnetic flux through the loop is changing. That loop is an inductor; KVL as a gradient statement fails until \(d\lambda/dt\) is included.

Using \(\nabla\times\nabla V=0\) on a domain that is not simply connected, or across a branch cut of a multi-valued angle field. The azimuthal field of a line current has vanishing curl away from the wire but nonzero circulation around the wire; the domain with the wire removed is not simply connected.

Forgetting the minus in \(\mathbf{E}=-\nabla V\).

Evaluating flux as \(\int |A|\,dS\) without the cosine of the angle between \(\mathbf{A}\) and \(\hat{n}\), i.e. dropping the dot product.

Mixing \(\mathrm{mm}\) and \(\mathrm{m}\) in \(\rho\) while using \(\varepsilon_0=8.85\times 10^{-12}\) in SI.

Taking \(\nabla^2\mathbf{A}\) as the Laplacian of each curvilinear component. The vector Laplacian has extra curvature terms; prefer Cartesian components or \(\nabla(\nabla\cdot\mathbf{A})-\nabla\times(\nabla\times\mathbf{A})\).
