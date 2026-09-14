# Displacement current and Maxwell’s equations

Maxwell’s completion of Ampère’s law with displacement current \(\mathbf{J}_d=\partial\mathbf{D}/\partial t\) makes the set consistent with charge continuity and allows electromagnetic waves. This unit writes the four equations in integral and differential form, in free space and in linear media, in the time domain and as phasors, plus the continuity equation, constitutive relations, and boundary conditions collected in one place. Plane waves, lines, and waveguides are applications in the following units.

## Concepts

The four equations (SI, macroscopic):
1. Gauss’s law for electricity: \(\nabla\cdot\mathbf{D}=\rho_v\) (free charge if \(\mathbf{D}\) is so defined).
2. Gauss’s law for magnetism: \(\nabla\cdot\mathbf{B}=0\).
3. Faraday: \(\nabla\times\mathbf{E}=-\partial\mathbf{B}/\partial t\).
4. Ampère–Maxwell: \(\nabla\times\mathbf{H}=\mathbf{J}+\partial\mathbf{D}/\partial t\).

Integral forms are Gauss surfaces for (1)(2), Faraday loops for (3), Ampère loops for (4) with the displacement current through the spanning surface. The spanning surface for Faraday and Ampère is not unique; Stokes requires that \(\nabla\cdot\mathbf{B}=0\) and continuity of charge make the choice irrelevant.

Why displacement current: take divergence of Ampère \(\nabla\times\mathbf{H}=\mathbf{J}\) and get \(\nabla\cdot\mathbf{J}=0\), which contradicts \(\nabla\cdot\mathbf{J}+\partial\rho_v/\partial t=0\) unless you add \(\partial\mathbf{D}/\partial t\). Between capacitor plates \(\mathbf{J}=0\) but \(\partial\mathbf{D}/\partial t\) carries the “current” so that \(\oint\mathbf{H}\cdot\mathrm{d}\mathbf{l}\) around the wire equals the same \( I \) whether the surface cuts the wire or passes between the plates. Magnitude \( I_d=C\mathrm{d}v/\mathrm{d}t \) for a capacitor, equal to conduction current in the leads in series.

Constitutive: \(\mathbf{D}=\varepsilon\mathbf{E}\), \(\mathbf{B}=\mu\mathbf{H}\), \(\mathbf{J}=\sigma\mathbf{E}\) (Ohm) in linear isotropic media. Free space \(\varepsilon_0,\mu_0,\sigma=0\). Good conductor: conduction current dominates displacement when \(\sigma\gg\omega\varepsilon\). Good dielectric: the reverse. The crossover is a material-and-frequency statement, not a moral one.

Continuity: \(\nabla\cdot\mathbf{J}+\partial\rho_v/\partial t=0\). Charge is conserved. Kirchhoff’s current law is the lumped, quasi-static, closed-surface integral of continuity when displacement current leaving a node is negligible (or is modelled as capacitors).

Phasor Maxwell (e^{j\omega t} convention, Ellingson’s): \(\nabla\cdot\tilde{\mathbf{D}}=\tilde{\rho}\), \(\nabla\cdot\tilde{\mathbf{B}}=0\), \(\nabla\times\tilde{\mathbf{E}}=-j\omega\tilde{\mathbf{B}}\), \(\nabla\times\tilde{\mathbf{H}}=\tilde{\mathbf{J}}+j\omega\tilde{\mathbf{D}}\). Time derivatives become \( j\omega \). Source-free linear medium: \(\nabla\times\tilde{\mathbf{E}}=-j\omega\mu\tilde{\mathbf{H}}\), \(\nabla\times\tilde{\mathbf{H}}=j\omega\varepsilon_c\tilde{\mathbf{E}}\) with complex permittivity \(\varepsilon_c=\varepsilon-j\sigma/\omega\).

Wave equations follow by taking curl of Faraday and substituting Ampère (unit 07). Potential formulation: \(\mathbf{B}=\nabla\times\mathbf{A}\), \(\mathbf{E}=-\nabla V-\partial\mathbf{A}/\partial t\), Lorenz gauge, inhomogeneous wave equations for \( V \) and \(\mathbf{A}\) (retarded potentials, radiation unit 10).

Boundary conditions (time-varying, no infinite \(\mathbf{K}\) unless a perfect conductor): tangential \(\mathbf{E}\) continuous, normal \(\mathbf{B}\) continuous, jump in tangential \(\mathbf{H}\) equal to free \(\mathbf{K}\), jump in normal \(\mathbf{D}\) equal to free \(\rho_S\). PEC: \( E_t=0 \), \( B_n=0 \), \(\mathbf{K}=\mathbf{n}\times\mathbf{H}\), \(\rho_S=\mathbf{n}\cdot\mathbf{D}\).

Poynting: \(\mathbf{S}=\mathbf{E}\times\mathbf{H}\), power into a volume \( -\oint\mathbf{S}\cdot\mathrm{d}\mathbf{A} \) equals increase of field energy plus Joule heat \(\mathbf{J}\cdot\mathbf{E}\) (Poynting’s theorem). Average phasor \(\mathbf{S}_{\mathrm{av}}=\frac12\mathrm{Re}(\tilde{\mathbf{E}}\times\tilde{\mathbf{H}}^*)\).

Quasi-static limits: if dimensions \(\ll c/f\), you may use circuit theory with lumped \( L,C,R \) that came from static field solutions. Displacement current in a 50 Hz power transformer is negligible; in a 3 GHz PCB via it is not.

Maxwell’s addition does not change magnetostatics of DC: \(\partial\mathbf{D}/\partial t=0\). It does change the statement “Ampère’s law always uses conduction current only.”

## Equations

Differential set:

\[
\nabla\cdot\mathbf{D}=\rho_v,\quad
\nabla\cdot\mathbf{B}=0,\quad
\nabla\times\mathbf{E}=-\frac{\partial\mathbf{B}}{\partial t},\quad
\nabla\times\mathbf{H}=\mathbf{J}+\frac{\partial\mathbf{D}}{\partial t}.
\]

Integral set:

\[
\oint\mathbf{D}\cdot\mathrm{d}\mathbf{S}=Q_{\mathrm{enc}},\quad
\oint\mathbf{B}\cdot\mathrm{d}\mathbf{S}=0,
\]
\[
\oint\mathbf{E}\cdot\mathrm{d}\mathbf{l}=-\frac{\mathrm{d}}{\mathrm{d}t}\int\mathbf{B}\cdot\mathrm{d}\mathbf{S},\quad
\oint\mathbf{H}\cdot\mathrm{d}\mathbf{l}=I_{\mathrm{cond}}+ \frac{\mathrm{d}}{\mathrm{d}t}\int\mathbf{D}\cdot\mathrm{d}\mathbf{S}.
\]

Continuity: \(\nabla\cdot\mathbf{J}+\partial\rho_v/\partial t=0\).

Free space wave speed \( c=1/\sqrt{\mu_0\varepsilon_0} \). Impedance of free space \( \eta_0=\sqrt{\mu_0/\varepsilon_0}\approx 377\,\Omega \).

Phasor Ampère: \(\nabla\times\tilde{\mathbf{H}}=(\sigma+j\omega\varepsilon)\tilde{\mathbf{E}}\).

Displacement vs conduction magnitudes: \( |J_d|/|J|=\omega\varepsilon/\sigma \) for linear Ohmic media.

Capacitor: \( I_d=\varepsilon A\mathrm{d}E/\mathrm{d}t=C\mathrm{d}V/\mathrm{d}t \).

## Methods

To check consistency of a proposed field, plug into all four (or the two curl equations plus continuity). Static problems: drop \(\partial/\partial t\). Time-harmonic: use phasors, restore \(\mathrm{Re}\{e^{j\omega t}\}\) at the end.

Between capacitor plates, compute \( I_d \) from \(\varepsilon A\mathrm{d}E/\mathrm{d}t\) and verify it equals the lead current.

To decide good conductor vs dielectric: compute \(\sigma/(\omega\varepsilon)\). Copper at 1 MHz is a conductor; seawater at 1 GHz is a judgement call (look up numbers).

Boundary: draw a tiny loop or pillbox; the time-derivative terms vanish as the loop shrinks if fields are finite, recovering the static BCs plus Faraday’s tangential \( E \).

## Mistakes

Ampère without \( I_d \) through a capacitor.

Using \(\nabla\times\mathbf{H}=\mathbf{J}\) in a displacement-current problem because “there is no wire there.”

Phasor \( +j\omega \) versus \( -j\omega \) mixed with the time convention.

\(\nabla\cdot\mathbf{B}=\rho_m\) (magnetic charge) in SI UG Maxwell.

Poynting \(\mathbf{E}\times\mathbf{B}/\mu\) forgotten versus \(\mathbf{E}\times\mathbf{H}\).

Continuity ignored so that a time-varying \(\rho_v\) has a solenoidal \(\mathbf{J}\).

PEC with nonzero \( E_t \).

Units: \( \mathbf{H} \) in A/m, \( \mathbf{B} \) in T, not interchangeable by dropping \(\mu_0\) in air for a 10% lab.

A capacitor walk-through: \( C=50 \) pF, \( v=10\cos(10^6 t) \) V, \( i=-50e-12\times 10\times 10^6\sin(10^6 t)=-0.500\sin(10^6 t) \) mA. That current is \( I_d \) between plates.

Between plates \( A=4 \) cm², \( d=1 \) mm, \(\varepsilon_0\), \( E=v/d \), \( I_d=\varepsilon_0 A\mathrm{d}E/\mathrm{d}t=C\mathrm{d}v/\mathrm{d}t \) with \( C=\varepsilon_0 A/d=3.54 \) pF.

Copper \(\sigma=5.8\times 10^7 \), \(\varepsilon=\varepsilon_0\), 50 Hz: \(\sigma/(\omega\varepsilon)=2\times 10^{16}\), conduction dominates. Distilled water \(\sigma=10^{-4}\), 1 GHz: \(\omega\varepsilon\approx 4.5\), comparable-ish depending on \(\varepsilon_r(f)\).

Phasor Faraday: \(\tilde{\mathbf{B}}=0.02\mathbf{a}_z\) e^{-j\beta x}, \(\omega=10^9\), \(\nabla\times\tilde{\mathbf{E}}=-j\omega\tilde{\mathbf{B}}\) so the E field of a plane wave is consistent with unit 07.

Ampère loop around a capacitor: 4 A in the wire, \( I_d=4 \) A through the plate surface, \( \oint H\cdot dl=4 \) A either way.

Free space: \(\nabla\times\mathbf{E}=-\mu_0\partial\mathbf{H}/\partial t\), \(\nabla\times\mathbf{H}=\varepsilon_0\partial\mathbf{E}/\partial t\), take curl, \(\nabla^2\mathbf{E}-\mu_0\varepsilon_0\partial^2\mathbf{E}/\partial t^2=0\) if \(\nabla\cdot\mathbf{E}=0\). Speed \( c=3.00\times 10^8 \) m/s.

Boundary PEC: incident + reflected E tangential cancel; surface current \(\mathbf{K}=\mathbf{n}\times\mathbf{H}_{\mathrm{total}}\).

Poynting in a coax TEM: \(\mathbf{E}\) radial, \(\mathbf{H}\) \(\phi\), \(\mathbf{S}\) along z, power \( =\frac12 V I^* \) for phasors — circuit power is field power.

Relaxation \(\tau=\varepsilon/\sigma\) from combining Gauss and continuity in a conductor: \(\rho_v(t)=\rho_v(0)e^{-t/\tau}\). Charge in a good conductor vanishes from the volume almost immediately and sits on the surface.


Charge conservation as a Maxwell identity: take divergence of the Ampère–Maxwell law, use \(\nabla\cdot(\nabla\times\mathbf{H})=0\) and Gauss, recover continuity. If a numerical solver’s fields violate continuity, they violate Maxwell. Circuit KCL including capacitor currents is continuity for a node with displacement current modelled as \( i_C \).

Integral Ampère with displacement: the “current” through a surface is \( I_{\mathrm{cond}}+\mathrm{d}\Psi/\mathrm{d}t \) with \(\Psi=\int\mathbf{D}\cdot\mathrm{d}\mathbf{S}\) the electric flux. For a capacitor, \(\Psi=Q_{\mathrm{free}}\) on one plate, \(\mathrm{d}\Psi/\mathrm{d}t=i\). For a charging coaxial cable, the same idea distributed along z becomes the telegrapher shunt \( C'\partial v/\partial t \) (unit 08).

Constitutive anisotropy and bi-anisotropy are out of scope. Dispersion: \(\varepsilon(\omega)\) in dielectrics, Kramers–Kronig; UG uses a constant \(\varepsilon_r\) plus a constant \(\sigma\).

Duality: \(\mathbf{E}\leftrightarrow\mathbf{H}\), \(\varepsilon\leftrightarrow\mu\), with sign conventions, maps some electrostatic solutions to magnetostatic ones. Magnetic charge does not exist, so the dual of Gauss’s law for \( B \) stays homogeneous.

Retarded time \( t_r=t-R/c \): nothing in Maxwell is instantaneous. Quasi-statics drops retardation when \( \ell\ll c\Delta t \). A 1 m circuit at 50 Hz is quasi-static (\( \lambda=6000 \) km). A 1 m circuit at 300 MHz is a transmission line (\( \lambda=1 \) m).

Boundary conditions derived: pillbox for normal \( D \) and \( B \), vanishing height, the \(\partial/\partial t\) terms’ volume integrals vanish. Tiny Stokes loop for tangential \( E \) and \( H \); Faraday’s \(\partial B/\partial t\) through the vanishing area vanishes, leaving \( E_t \) continuous; Ampère’s \( J \) through the vanishing area becomes \(\mathbf{K}\) if you allow a surface current, otherwise \( H_t \) continuous.

Perfect magnetic conductor (PMC) is a dual fiction used in antenna images: \( H_t=0 \), \( B_n \) can be nonzero in some statements. PEC is the practical wall.

Poynting paradox of a charging capacitor: \(\mathbf{S}\) points radially inward between plates, feeding the growing electric energy. Energy does not flow down the wire in that picture; it flows in the fields. Both pictures can be made consistent with a full Maxwell solution including the wire’s \(\mathbf{H}\).

Complex permittivity: loss tangent \(\tan\delta=\varepsilon''/\varepsilon'=\sigma/(\omega\varepsilon')\) in a simple model. Power factor of a dielectric, Schering bridge (measurements pack) measures this.

Gauge: Coulomb gauge is natural in magnetostatics; Lorenz gauge \(\nabla\cdot\mathbf{A}+\mu\varepsilon\partial V/\partial t=0\) is natural for waves. Physical \(\mathbf{E},\mathbf{B}\) are gauge invariant.

Worked continuity: \(\rho_v=5 e^{-t/10^{-6}}\) nC/m³ uniform in a blob (unphysical without boundary currents, but as a local statement) \(\partial\rho/\partial t=-\rho/\tau\), \(\nabla\cdot\mathbf{J}=\rho/\tau\). A uniform blob cannot have a divergence of \( J \) without a surface current story — the example exists to remind you that uniform \(\rho(t)\) in a finite volume implies current at the boundary.

Worked phasor Ampère in a dielectric: \(\tilde{\mathbf{E}}=10 e^{-j\beta z}\mathbf{a}_x \), \(\omega=10^9\), \(\varepsilon=4\varepsilon_0\), \(\sigma=0\). \(\tilde{\mathbf{H}}=\mathbf{a}_y (10/\eta) e^{-j\beta z}\) with \(\eta=188.5\,\Omega\), and \(\nabla\times\mathbf{H}=j\omega\varepsilon\mathbf{E}\) checks if \(\beta=\omega\sqrt{\mu\varepsilon}\).

Worked PEC boundary: incident \( E_x \) on \( z=0 \) wall, reflected \( -E_x \) so total \( E_x(0)=0 \). Magnetic \( H_y \) doubles. Surface current \( K_x=H_y^{\mathrm{total}} \) with \(\mathbf{n}=\mathbf{a}_z\) from PEC into the air, \(\mathbf{K}=\mathbf{n}\times\mathbf{H}\).

Maxwell’s equations are the end of the postulates in this pack. Plane waves, lines, Smith, waveguides, and dipoles are solutions plus engineering bookkeeping. If a later formula disagrees with \(\nabla\cdot\mathbf{B}=0\) or with Faraday, the later formula is being used outside its region (TEM assumed in a waveguide, quasi-static \( L\) at 10 GHz on a 20 cm loop, etc.).


Displacement current density between plates is uniform only if fringing is neglected, the same approximation as \( C=\varepsilon A/d \). Fringing makes \( I_d \) spread outside the geometric cylinder; Ampère loops just outside the plates still capture nearly all \( I_d \) if you take a large enough surface. That is the field version of “capacitor current returns through the circuit.”

The four Maxwell equations plus constitutive relations plus boundary and initial conditions determine the fields. There is no fifth equation of the same status; continuity is dependent. Ohm’s law is constitutive, not Maxwell. Kirchhoff is an approximation. Keep the hierarchy when a circuit formula and a field formula seem to fight: the fields win, the circuit was quasi-static.
