# Rectangular waveguides and Hertzian dipole intro

A hollow metal pipe cannot support TEM; the lowest mode of a rectangular waveguide is TE10, with a cutoff frequency set by the wide dimension \( a \). Below cutoff the mode is evanescent. Radiation from a short current element (Hertzian dipole) is the first antenna: far-field \( 1/r \), radiation resistance, pattern \(\sin^2\theta\). This unit is UG intro only: cutoff, \(\lambda_g\), dominant-mode fields, and the Hertzian dipole formulas, not a full antenna-theory course.

## Concepts

Boundary conditions in a PEC pipe: \( E_t=0 \) on walls. Maxwell plus those BCs yield discrete modes TE\(_{mn}\) and TM\(_{mn}\). Rectangular guide, interior \( a\times b \) with \( a>b \): cutoff \( k_c=\sqrt{(m\pi/a)^2+(n\pi/b)^2} \), \( f_c=k_c/(2\pi\sqrt{\mu\varepsilon}) \). For air-filled, \( f_c=c k_c/(2\pi) \). TE10: \( m=1,n=0 \), \( f_c=c/(2a) \). Standard X-band WR-90 has \( a\approx 0.9 \) inch, \( f_c\approx 6.56 \) GHz. Dominant mode is TE10 because it has the lowest \( f_c \). TM modes need both \( m,n\ge 1 \), so TM11 is higher. Operate between \( f_c^{\mathrm{TE10}} \) and the next mode (often TE20 at \( c/a \) or TE01 at \( c/(2b) \)) for single-mode bandwidth.

Dispersion: \(\beta=\sqrt{k^2-k_c^2}\) with \( k=\omega\sqrt{\mu\varepsilon} \). Phase velocity \( v_p=\omega/\beta > c \). Group velocity \( v_g=\mathrm{d}\omega/\mathrm{d}\beta=c^2/v_p < c \) (filled with \(\varepsilon_0\)). Guide wavelength \(\lambda_g=2\pi/\beta > \lambda_0 \). Wave impedance TE: \( Z_{\mathrm{TE}}=\eta k/\beta \), TM: \( Z_{\mathrm{TM}}=\eta\beta/k \). Attenuation from wall loss ~ \( R_s \) times wall \(|H|^2\); UG qualitative: rises near cutoff and at high frequency (skin). Below cutoff \(\beta\) is imaginary, fields decay as \( e^{-\alpha z} \), \(\alpha=\sqrt{k_c^2-k^2}\), a waveguide below cutoff is an attenuator.

Fields of TE10: \( E_y \propto \sin(\pi x/a) e^{-j\beta z} \), \( H_x,H_z \) companions, \( E_x=E_z=H_y=0 \). No variation in \( y \). Current on the broad wall is longitudinal at the centre. A probe (coax inner) along \( E_y \) near \( x=a/2 \) excites TE10. A slot radiator cuts wall current.

Circular guides, cavities, and dielectric waveguides are named, not developed. Optical fibre is a dielectric waveguide at another course’s scale.

Hertzian dipole: length \(\ell\ll\lambda\), uniform current \( I_0 \) (idealization). Retarded vector potential along z, far field (\( kr\gg 1 \), and \( r\gg\ell \)):

\[
E_\theta = j\eta \frac{k I_0\ell \sin\theta}{4\pi r} e^{-jkr},\qquad
H_\phi=E_\theta/\eta.
\]

Radiation intensity \( U\propto\sin^2\theta \). Directivity of a short dipole \( D=1.5 \) (1.76 dB). Radiation resistance \( R_r=80\pi^2 (\ell/\lambda)^2 \) ohms, small: a 1 cm rod at 30 MHz is a terrible radiator (\( \ell/\lambda\sim 0.001 \)). Real antennas use half-wave dipoles with \( R_r\approx 73\,\Omega \). Pattern nulls on the axis, max in the equatorial plane. Polarization linear, \(\mathbf{E}\) along \(\mathbf{a}_\theta\).

Near field of a dipole has \( 1/r^2,1/r^3 \) terms (reactive). Far field is \( 1/r \). The boundary is loosely \( r=2L^2/\lambda \) for a larger antenna of size \( L \); for a Hertzian, \( kr\sim 1 \) is already “starting to be far.”

Friis (mention): \( P_r=P_t G_t G_r \lambda^2/((4\pi r)^2) \) in free space, polarization matched. Connects this unit to a radio link. Not a full radar course.

## Equations

Cutoff and guide wave number:

\[
f_c=\frac{1}{2\pi\sqrt{\mu\varepsilon}}\sqrt{\left(\frac{m\pi}{a}\right)^2+\left(\frac{n\pi}{b}\right)^2},\qquad
\beta=\sqrt{k^2-k_c^2}.
\]

TE10: \( f_c=1/(2a\sqrt{\mu\varepsilon}) \). \(\lambda_g=\lambda/\sqrt{1-(f_c/f)^2} \). \( v_p=c/\sqrt{1-(f_c/f)^2} \), \( v_g=c\sqrt{1-(f_c/f)^2} \) (air-filled).

Hertzian:

\[
R_r=80\pi^2\left(\frac{\ell}{\lambda}\right)^2,\qquad
D=1.5,\qquad
U=U_{\max}\sin^2\theta.
\]

Far \( E_\theta \) as above. Average Poynting \( \frac12\mathrm{Re}(E_\theta H_\phi^*) \).

## Methods

For a rectangular guide: identify \( a \) (longer), compute \( f_c^{\mathrm{TE10}} \), check \( f>f_c \) and \( f \) below the next mode. Then \(\beta,\lambda_g,Z_{\mathrm{TE}}\). Do not use TEM \( Z_0 \) of a coax on a waveguide.

Dipole: if \(\ell/\lambda\) is not \(\ll 1 \), do not use Hertzian \( R_r \). Use the short-dipole formulas only when the problem says short or Hertzian.

Units: \( a \) in metres in \( c/(2a) \). Inches to metres: 0.0254.

Pattern: plot \( \sin^2\theta \) or \( |E_\theta| \) in a polar plot; half-power at \(\sin\theta=1/\sqrt{2}\), \(\theta=45^\circ\) and \( 135^\circ \) from the z-axis — wait, \(\sin\theta=0.707\), \(\theta=45^\circ\) and \( 135^\circ \), the beamwidth of a short dipole is 90° in that elevation sense. Do not confuse with a half-wave dipole’s slightly different pattern.

## Mistakes

TEM in an empty rectangular pipe.

Using \( f_c=c/(2b) \) for TE10 with \( b \) the short side.

\( v_p>c \) implying information faster than light (group velocity is the energy velocity here).

Hertzian \( R_r=73\,\Omega \).

Far-field \( 1/r^2 \) for \( E \) (that is power density).

Ignoring the \(\sin\theta\) null and claiming isotropic.

Waveguide below cutoff treated as a transmission line with real \( Z_0 \).

A WR-90-ish walk-through: \( a=22.86 \) mm, \( b=10.16 \) mm, air. \( f_c^{\mathrm{TE10}}=6.56 \) GHz, \( f_c^{\mathrm{TE20}}=13.1 \) GHz, \( f_c^{\mathrm{TE01}}=14.8 \) GHz. At 10 GHz, \( f/f_c=1.52 \), \(\lambda_0=3.00 \) cm, \(\lambda_g=\lambda_0/\sqrt{1-0.430}=4.00 \) cm. \( \beta=157 \) rad/m. \( Z_{\mathrm{TE}}=377/\sqrt{1-(f_c/f)^2}=500\,\Omega \) (not 50).

Cutoff check: 5 GHz in that guide is below 6.56 GHz, evanescent, \(\alpha=\sqrt{k_c^2-k^2}=90.7 \) Np/m, a 5 cm plug is 19.7 dB if you trust the ideal formula.

Hertzian: \(\ell=2 \) cm, \( f=100 \) MHz, \(\lambda=3 \) m, \(\ell/\lambda=0.00667 \), \( R_r=80\pi^2 (0.00667)^2=0.0351\,\Omega \). \( I_0=1 \) A peak, \( P=\frac12 I_0^2 R_r=17.6 \) mW. Tiny.

At \( r=100 \) m, \(\theta=90^\circ \), \( |E_\theta|=\eta k I_0\ell /(4\pi r) \) with \( k=2.09 \) m^{-1}, \( I_0\ell=0.02 \), \( |E|=377\times 2.09\times 0.02/(4\pi\times 100)=12.5 \) mV/m peak.

Directivity 1.5 means max power density is 1.5 times that of an isotropic radiator with the same total \( P \).

Cavity sketch: a guide closed with two shorts, length \( p\lambda_g/2 \), resonant. TE101 box is the lowest rectangular cavity. UG mention.

Why waveguides at high power: no inner conductor to arc, walls take heat, \( Q \) of cavities is high. Why not at 50 Hz: \( a \) would be 3000 km. Coax and two-wire own the low-frequency world; waveguides own centimetre waves in radar plumbing; microstrip owns PCBs.


Mode indices: m is half-waves along \( a \), n along \( b \). TE10 looks like a half-cosine of \( E_y \) across the width. Power flows in z, stored energy sloshes in x as well (the \( H_z \) of TE). TM has \( E_z \). You cannot have TE00 or TM10 in a rectangle: the BCs kill them.

Why no TEM in a hollow pipe: TEM needs a potential difference between two conductors, a unique \( V \) in the cross-section. One conductor (the pipe) cannot support a TEM voltage. A coax has two conductors and does support TEM down to DC.

Cavity quality: \( Q=\omega\times \) stored energy / power loss. Waveguide cavities as klystron tanks, filter cavities. UG: resonant length \( p\lambda_g/2 \).

Excitation: a coax probe, a loop (magnetic), a slot. Matching the probe depth is a Smith-chart problem in the waveguide’s \( Z_{\mathrm{TE}} \), not 50 Ω of the coax — an iris or a quarter-wave transformer in guide may sit in between.

Hertzian dipole near field: \( H_\phi \) has \( 1/r^2 \) (induction) and \( 1/r \) (radiation); \( E_r \) is \( 1/r^3 \) and \( 1/r^2 \). Reactive power dominates near; real radiated power is the \( 1/r \) Poynting, integral \( \frac12 I_0^2 R_r \). Do not compute radiated power by integrating the near-field Poynting without the full complex \(\mathbf{S}\).

Array sketch: two Hertzian dipoles spaced \(\lambda/2 \), phase 0, pattern \(\cos((\pi/2)\cos\theta)\) extra factor in the plane of the array — named so you recognize interference. Not a full array-factor course.

Radar range equation is Friis with a target RCS. Out of scope except as a pointer.

Safety: waveguide flanges leak; high-power microwave burns are real. Shorting plates and dummy loads exist.

Worked TE10 field: \( a=3 \) cm, \( f=8 \) GHz, \( f_c=5 \) GHz, \( E_{y0}=10^4 \) V/m peak at the centre. Power \( P=\frac12 |E_0|^2 ab /(2 Z_{\mathrm{TE}}) \) with the usual TE10 factor \( 1/2 \) from the sine-squared average: \( P=|E_0|^2 a b /(4 Z_{\mathrm{TE}}) \). \( Z_{\mathrm{TE}}=\eta/\sqrt{1-(f_c/f)^2}=377/0.781=483\,\Omega \). \( P=10^8 \times 0.03\times 0.015 /(4\times 483)=23.3 \) W.

Worked dipole pattern: \( U/U_{\max}=\sin^2\theta \). Fraction of power in \( 60^\circ<\theta<120^\circ \): integrate \(\sin^3\theta\,\mathrm{d}\theta\) over that band versus 0 to \(\pi\). The \(\sin^3\) integral is a standard \( \int\sin^3= -\sin^2\cos/3-2\cos/3 \). Getting a number (~0.65 or so) is a calculus drill, not a new EM law.

Half-wave dipole (preview): current \( I_0\cos(kz) \) on a \(\lambda/2\) wire, \( R_r\approx 73\,\Omega \), slightly sharper than \(\sin^2\theta \). Do not use Hertzian \( R_r \) for a \(\lambda/2\) antenna.

Image of a vertical Hertzian dipole over a PEC ground: the image is in the same direction, doubling \( E_\theta \) on the horizon relative to free space (4× power density, 3 dB? 6 dB in field-squared). Horizontal dipole image reverses. Antenna over ground is this.

Waveguide-to-coax adapters exist because instruments are 50 Ω coax and high-power plumbing is waveguide. The adapter is a matching network (unit 09) between \( Z_{\mathrm{TE}} \) and 50 Ω plus a mode launcher.

If a problem gives a circular waveguide, the dominant mode is TE11, cutoff \( 1.841 c/(\pi D) \). One formula to recognize, not to re-derive Bessel functions in a first course.

The Hertzian dipole is also the Green’s function building block: a general antenna’s far field is an integral of Hertzian elements. UG stops before that integral (the radiation integral). What you must leave with: cutoff of TE10, \(\lambda_g\), why \( v_p>c \), and \( E_\theta\propto\sin\theta/r \) with a tiny \( R_r \) for short wires — hence do not expect a 2 cm stub at 1 MHz to radiate a kilowatt.
