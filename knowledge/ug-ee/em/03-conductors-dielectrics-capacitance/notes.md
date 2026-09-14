# Conductors, dielectrics, boundary conditions, capacitance

Inside a conductor in electrostatics, \(\mathbf{E}=0\), excess charge resides on the surface, and the surface is an equipotential. Dielectrics polarize: bound charge, \(\mathbf{D}=\varepsilon_0\mathbf{E}+\mathbf{P}\), and in linear media \(\mathbf{D}=\varepsilon\mathbf{E}\). Boundary conditions on \(\mathbf{E}\) and \(\mathbf{D}\) (and later \(\mathbf{B},\mathbf{H}\)) are how you join regions. Capacitance is the linear map \( Q=CV \) for a two-conductor system, computed from Gauss or from energy or from Laplace. This unit is the electrostatics of materials and of capacitors as used in a first EM course.

## Concepts

Perfect conductor (electrostatics): mobile charge cancels any interior field in a few \(\tau=\varepsilon/\sigma\) (for copper, \( 10^{-19} \) s — instantaneous for UG statics). \(\mathbf{E}=0\) inside, \(\rho_v=0\) inside, \( V=\mathrm{const} \) throughout a connected conductor. Just outside, \(\mathbf{E}\) is normal: \(\mathbf{D}\cdot\mathbf{n}=\rho_S\) with \(\mathbf{n}\) outward from the conductor. A cavity inside a conductor without enclosed charge has \(\mathbf{E}=0\) (Faraday cage). An electrostatic shield works that way.

Ohmic conductor with steady current is not electrostatic: \(\mathbf{J}=\sigma\mathbf{E}\), \(\nabla\cdot\mathbf{J}=0\) in DC, so Laplace for \( V \) still holds inside a homogeneous conductor (unit 06’s steady current). Surface charge can sit on interfaces to bend \(\mathbf{J}\). Do not mix “ \(\mathbf{E}=0\) in a conductor” (electrostatics, no current) with a resistor ( \(\mathbf{E}=J/\sigma\) ).

Dielectric: molecules form dipoles, polarization \(\mathbf{P}\) (dipole moment per volume). Bound volume charge \(\rho_b=-\nabla\cdot\mathbf{P}\), bound surface \(\rho_{bS}=\mathbf{P}\cdot\mathbf{n}\). Free charge is what you put on electrodes. Gauss for free charge: \(\nabla\cdot\mathbf{D}=\rho_{\mathrm{free}}\). Linear isotropic: \(\mathbf{P}=\varepsilon_0\chi_e\mathbf{E}\), \(\varepsilon_r=1+\chi_e\), \(\mathbf{D}=\varepsilon_0\varepsilon_r\mathbf{E}\). Anisotropic crystals have a tensor \(\overline{\varepsilon}\) — mention only. Breakdown when \( E \) exceeds dielectric strength (air ~3 kV/mm).

Boundary conditions, electrostatic: the tangential \(\mathbf{E}\) is continuous (\( \mathbf{n}\times(\mathbf{E}_1-\mathbf{E}_2)=0 \)) if no time-varying \(\mathbf{B}\) (Faraday). The normal \(\mathbf{D}\) jumps by free surface charge: \(\mathbf{n}\cdot(\mathbf{D}_1-\mathbf{D}_2)=\rho_{S,\mathrm{free}}\). If no free \(\rho_S\), \( D_{1n}=D_{2n} \). Across a dielectric-dielectric interface with no free charge, \( E_t \) continuous and \( D_n \) continuous, so the field lines kink: the denser dielectric takes more \( D \) for the same \( E_t \) story — actually \( E_1\sin\theta_1=E_2\sin\theta_2 \) wait: \( E_t \) same so \( E_1\sin\theta_1=E_2\sin\theta_2 \) if \(\theta\) from normal? Standard: \(\theta\) from the normal, \( E\sin\theta \) is tangential, so \( E_1\sin\theta_1=E_2\sin\theta_2 \) and \( \varepsilon_1 E_1\cos\theta_1=\varepsilon_2 E_2\cos\theta_2 \). Then \( \tan\theta_1/\tan\theta_2=\varepsilon_1/\varepsilon_2 \).

Capacitance of two conductors: \( C=Q/V \) with \( Q \) the charge on one and \( -Q \) on the other, \( V \) the potential difference. Multi-conductor systems have a capacitance matrix; UG two-body is enough. Isolated sphere: \( C=4\pi\varepsilon a \). Parallel plates: \( C=\varepsilon A/d \) (neglect fringing). Coax: \( C=2\pi\varepsilon/\ln(b/a) \) per metre. Two-wire line: \( C=\pi\varepsilon/\cosh^{-1}(d/(2a)) \) per metre. Energy \( W=\frac12 CV^2=\frac12 Q^2/C \). Series capacitors: same \( Q \), voltages add, \( 1/C=\sum 1/C_i \). Parallel: same \( V \), charges add.

Dielectric in a capacitor: if you fill the gap with \(\varepsilon_r\) and keep \( V \) fixed (battery connected), \( Q \) and \( C \) rise by \(\varepsilon_r\), energy \( \frac12 CV^2 \) rises (battery does work). If \( Q \) is fixed (battery disconnected), \( V \) falls, energy falls (the dielectric is pulled in). Partial fills: treat as series (slab filling the gap thickness-wise) or parallel (side-by-side) only when the interfaces match those BCs; a floating slab is a series sandwich of three capacitors.

Method of images still works with dielectrics in special geometries (charge above a dielectric half-space: two image charges, different formulas for the two half-spaces). Conducting sphere in a uniform field: dipole induced, \(\mathbf{p}=4\pi\varepsilon a^3\mathbf{E}_0\).

Current continuity and Kirchhoff are the lumped limit of these field BCs when dimensions \(\ll\lambda\).

## Equations

Conductor surface:

\[
\mathbf{E}_{\mathrm{inside}}=\mathbf{0},\qquad \mathbf{D}_{\mathrm{out}}\cdot\mathbf{n}=\rho_S,\qquad E_t=0\ \mathrm{on\ the\ surface}.
\]

Linear dielectric:

\[
\mathbf{D}=\varepsilon\mathbf{E}=\varepsilon_0\varepsilon_r\mathbf{E},\qquad \varepsilon_r=1+\chi_e.
\]

Interface, \(\mathbf{n}\) from 2 into 1:

\[
\mathbf{n}\times(\mathbf{E}_1-\mathbf{E}_2)=\mathbf{0},\qquad \mathbf{n}\cdot(\mathbf{D}_1-\mathbf{D}_2)=\rho_{S,\mathrm{free}}.
\]

Capacitance:

\[
C=\frac{Q}{V}=\frac{\varepsilon\oint E\cdot\mathrm{d}S}{\int\mathbf{E}\cdot\mathrm{d}\mathbf{l}}.
\]

Parallel plate / coax per length:

\[
C=\frac{\varepsilon A}{d},\qquad C'=\frac{2\pi\varepsilon}{\ln(b/a)}.
\]

Energy:

\[
W=\frac12 CV^2=\frac12\int\mathbf{D}\cdot\mathbf{E}\,\mathrm{d}v.
\]

Relaxation time: \( \tau=\varepsilon/\sigma \).

Refraction (no free \(\rho_S\)):

\[
\frac{\tan\theta_1}{\tan\theta_2}=\frac{\varepsilon_1}{\varepsilon_2}.
\]

## Methods

To find \( C \): (1) assume \( Q \), (2) find \(\mathbf{E}\) by Gauss or Laplace, (3) integrate \(\mathbf{E}\) for \( V \), (4) \( C=Q/V \). Or assume \( V \), solve Laplace, find \(\rho_S=\varepsilon E_n \), integrate charge.

Series dielectric slabs perpendicular to \(\mathbf{E}\): \( D \) the same (no free charge on the interface), \( V=\sum D d_i/\varepsilon_i \), \( C=Q/V \). Parallel slabs (interfaces parallel to \(\mathbf{E}\)): \( E \) the same, \( C=\sum\varepsilon_i A_i/d \).

Force on a dielectric slab: \( F=\mathrm{d}W/\mathrm{d}x \) at constant \( V \) or minus at constant \( Q \); get the sign by thinking whether the system wants to increase \( C \).

Spherical capacitor: \( C=4\pi\varepsilon ab/(b-a) \), isolated sphere is \( b\to\infty \).

## Mistakes

\( E=\sigma/(2\varepsilon_0) \) just outside a conductor.

Using \(\varepsilon_0\) in a filled coax.

Series/parallel dielectric guess without looking at whether \( E \) or \( D \) is common.

Forgetting fringing is neglected in \( \varepsilon A/d \) and then “proving” it on a 1 cm plate with 2 cm gap.

\(\mathbf{P}=\mathbf{D}\) or \(\mathbf{P}=\varepsilon\mathbf{E}\).

Applying \(\mathbf{E}=0\) inside a resistor carrying DC.

Image charge for a dielectric plane copied from the conducting-plane formula.

Energy \(\frac12\int\varepsilon E^2\) over the plates’ metal (where \( E=0 \)) instead of the gap.

A plate walk-through: \( A=0.040 \) m², \( d=1.0 \) mm, air, \( C=\varepsilon_0 A/d=354 \) pF. With \(\varepsilon_r=4\) filling, 1.42 nF. At 100 V, \( Q=142 \) nC, \( W=7.09 \) µJ.

Coax: \( a=5 \) mm, \( b=15 \) mm, polyethylene \(\varepsilon_r=2.25 \), \( C'=2\pi\varepsilon/\ln 3=90.5 \) pF/m.

Series slabs: two layers each \( d/2 \), \(\varepsilon_r=2\) and \( 4 \), same \( A \), \( D=Q/A \), \( V=D(d/2)(1/\varepsilon_1+1/\varepsilon_2) \), \( C=Q/V=2\varepsilon_0 A/(d(1/2+1/4))=8\varepsilon_0 A/(3d) \).

Isolated sphere \( a=2 \) cm, \( C=4\pi\varepsilon_0 a=2.22 \) pF. At 10 kV, \( Q=22.2 \) nC.

Conductor surface: \(\rho_S=8.00\) nC/m², \( E=\rho_S/\varepsilon_0=904 \) V/m normal out.

Relaxation: distilled water \(\varepsilon_r\approx 80\), \(\sigma\approx 10^{-4}\) S/m, \(\tau=7\) µs — not a static dielectric on DC for long. Glass \(\tau\) can be hours.

Boundary: \(\varepsilon_{r1}=2\), \(\varepsilon_{r2}=8\), no free charge, \(\mathbf{E}_1\) at \( 30^\circ \) from normal, \( E_1=100 \) V/m. \( E_{1t}=50 \), \( E_{1n}=86.6 \). \( E_{2t}=50 \), \( D_{1n}=D_{2n} \) so \( 2\varepsilon_0\times 86.6=8\varepsilon_0 E_{2n} \), \( E_{2n}=21.6 \), \( E_2=54.5 \) V/m, \(\theta_2=\tan^{-1}(50/21.6)=66.6^\circ \). Check \(\tan\theta_1/\tan\theta_2=(1/\sqrt{3})/2.28=0.25=\varepsilon_1/\varepsilon_2\).


Capacitance matrix sketch for three conductors: \( Q_i=\sum_j C_{ij} V_j \), \( C_{ii}>0 \), \( C_{ij}<0 \) for \( i\neq j \) (mutual). A two-conductor capacitor is \( C=C_{11}=C_{22}=-C_{12} \) when the reference is the other body. UG problems that say “the capacitance of the system” mean that two-body \( C \).

Coax with two dielectric layers, interface at \( c \), \( a<c<b \): \( D_\rho=Q'/(2\pi\rho) \) the same in both layers (Gauss, no free charge on the dielectric interface), \( E=D/\varepsilon(\rho) \), \( V=\int_a^b E\,\mathrm{d}\rho \), two logarithms. Series of two coaxial capacitances. If the split is longitudinal (two dielectrics side by side along \(\phi\)), that is not coaxial series; it is a harder mixed-BC problem, not \(\varepsilon A/d\).

Force on a parallel-plate battery-connected pair: \( F=\frac12 V^2\mathrm{d}C/\mathrm{d}x \). If plates separate, \( C \) drops, the battery-connected force is attractive. Constant-\( Q \): \( F=\frac12 Q^2\mathrm{d}(1/C)/\mathrm{d}x \) with the opposite looking derivative, still attractive. Compute one and keep the sign by physics: opposite charges attract.

Breakdown: \( E_{\max} \) in a coax is at the inner conductor, \( E_a=V/(a\ln(b/a)) \). For fixed \( b \), there is an \( a \) that minimizes \( E_a \) for given \( V \) (\( b/a=e \)). High-voltage coax geometry is not arbitrary.

Bound versus free: a linear dielectric between plates with a battery has free \(\rho_S\) on the metal and bound \(\rho_{bS}=P\) on the dielectric faces. \( D \) is set by free charge, \( E=D/\varepsilon \), smaller than the air-gap \( E \) at the same \( V \) only if you fill and keep \( V \) — wait: at the same \( V \), \( E\approx V/d \) still if the fill is complete (one dimension). Then \( D=\varepsilon E \) is larger, \( Q \) larger, \( C \) larger. The reduction of \( E \) at fixed \( Q \) is the other experiment. State which is held constant.

Ohmic conductors and capacitors together: a leaky dielectric is \( C \) parallel with \( R=d/(\sigma A) \). Time constant \( RC=\varepsilon/\sigma=\tau \), the same relaxation time. A “capacitor” of slightly conducting plastic discharges itself in \(\tau\).

Electrostatic pressure on a conductor surface \( \frac12 D E=\rho_S^2/(2\varepsilon) \) outward. That is why an isolated charged balloon of conducting paint wants to expand.

Uniqueness and the Faraday cage: a closed conducting shell, outer charge \( Q \), inner cavity empty: inner surface charge 0, outer surface \( Q \), cavity \( E=0 \). If you place \( q \) in the cavity, inner surface develops \(-q\), outer \( Q+q \) if the shell floated with net \( Q \). Lightning-rod UG: charge density high on sharp points, \( E \) large, corona.

Spherical capacitor numerical: \( a=4 \) cm, \( b=8 \) cm, oil \(\varepsilon_r=2.2 \), \( C=4\pi\varepsilon ab/(b-a)=19.6 \) pF. At 2 kV, \( Q=39.1 \) nC, \( E(a)=Q/(4\pi\varepsilon a^2)=3.99 \) kV/cm.

Two-wire line: \( C'=\pi\varepsilon/\cosh^{-1}(d/2a)\approx \pi\varepsilon/\ln(d/a) \) for \( d\gg a \). 2 mm wires 20 mm apart in air: \( C'\approx 9.1 \) pF/m. Twin-lead 300 Ω is a different \( \sqrt{L'/C'} \) story (unit 08) but the \( C' \) is this electrostatics.

Never apply \(\sigma/\varepsilon_0\) as the field inside a dielectric next to a conductor without using the local \(\varepsilon\). Just outside the metal, in the dielectric, \( D=\rho_{S,\mathrm{free}} \), \( E=\rho_S/\varepsilon \).

A floating conductor inserted between plates without touching: it becomes an equipotential, equivalent to two capacitors in series if it fills the footprint, increasing \( C \) (the metal is \(\varepsilon\to\infty\)). A floating dielectric slab of \(\varepsilon_r\) also increases \( C \) but less.

Exam: if they give \(\chi_e\), \(\varepsilon_r=1+\chi_e\). If they give \(\mathbf{P}\) and \(\mathbf{E}\), \(\chi_e=P/(\varepsilon_0 E)\). If they give \(\mathbf{D}\) and \(\mathbf{E}\), \(\varepsilon=D/E\). Do not mix the three formulas with the wrong pair.
