# Uniform plane waves, Poynting, polarization

A uniform plane wave (UPW) has fields that depend on only one Cartesian coordinate and time, with \(\mathbf{E}\) and \(\mathbf{H}\) transverse to the direction of propagation. It is the local model of a radio wave far from an antenna and the exact mode of an ideal parallel-plate TEM guide. This unit is the Helmholtz equation, intrinsic impedance, phase velocity, attenuation in a lossy medium, instantaneous and average Poynting vectors, and polarization (linear, circular, elliptical).

## Concepts

Source-free linear medium: both \(\mathbf{E}\) and \(\mathbf{H}\) satisfy the Helmholtz equation \((\nabla^2+k^2)\tilde{\mathbf{E}}=0\) with \( k=\omega\sqrt{\mu\varepsilon_c} \) and complex \(\varepsilon_c=\varepsilon-j\sigma/\omega\). A solution propagating in \( +z \) is \(\tilde{\mathbf{E}}=\mathbf{E}_0 e^{-\gamma z}\) with \(\gamma=\alpha+j\beta=\sqrt{j\omega\mu(\sigma+j\omega\varepsilon)}\). In a lossless medium \(\alpha=0\), \(\beta=\omega\sqrt{\mu\varepsilon}=2\pi/\lambda\), phase velocity \( v_p=\omega/\beta=1/\sqrt{\mu\varepsilon} \), group velocity equals \( v_p \) if \(\mu,\varepsilon\) are constant. Frequency \( f=\omega/2\pi \), wavelength \(\lambda=2\pi/\beta\).

TEM: \(\mathbf{E}\) and \(\mathbf{H}\) perpendicular to \(\mathbf{a}_z\) and to each other. For a wave \( \mathbf{E}=E_x(z)\mathbf{a}_x \), Faraday and Ampère force \(\mathbf{H}=(E_x/\eta)\mathbf{a}_y \) for \( +z \) travel, with intrinsic impedance \(\eta=\sqrt{j\omega\mu/(\sigma+j\omega\varepsilon)}\). Lossless: \(\eta=\sqrt{\mu/\varepsilon}\) real, \(\eta_0=377\,\Omega\). The ratio \( E/H=\eta \) is not a resistance you put in series with an antenna without a matching story; it is a field ratio.

Lossy dielectrics: small-loss approximation \(\alpha\approx \sigma\eta/2 \), \(\beta\approx\omega\sqrt{\mu\varepsilon}\). Good conductors: \(\delta=\sqrt{2/(\omega\mu\sigma)}\) skin depth, \(\alpha=\beta=1/\delta\), \(\eta=(1+j)/\sigma\delta \) (or \(\sqrt{j\omega\mu/\sigma}\)). Fields live in a skin; a thick shield works because \( e^{-t/\delta} \) is small.

Polarization is the time path of \(\mathbf{E}\) at a fixed point. Linear: \( E_x \) and \( E_y \) in phase (or 180°). Circular: equal amplitudes, \(\pm 90^\circ\) phase, sense IEEE “thumb in direction of propagation” for the fingers of \(\mathbf{E}\) rotation as seen looking in the direction of travel — check the convention the course uses (IEEE vs optics looking toward the source). Elliptical is the general case of two quadrature components. A single linearly polarized antenna receives the projection; a circularly polarized wave into a linear antenna loses 3 dB on average.

Reflection at normal incidence (preview of lines): a PEC wall has standing waves, \( E=0 \) on the wall, \( H \) doubles. Oblique incidence, Snell, Brewster, and total internal reflection belong with plane-wave boundaries; UG often parks them here or in a follow-on. This unit emphasizes the travelling UPW in an unbounded medium.

Poynting \(\mathbf{S}=\mathbf{E}\times\mathbf{H}\) instantaneous; for a lossless UPW it is \(\mathbf{a}_z E^2/\eta \) pulsing. Average \( S_{\mathrm{av}}=|E_0|^2/(2\eta) \) for a peak phasor \( E_0 \) (RMS form \( E_{\mathrm{rms}}^2/\eta \)). Units W/m². Intensity of a radio link uses this with spherical spreading (unit 10).

Standing wave: incident + reflected, VSWR language is unit 08. Here: nodes of \( E \) every \(\lambda/2\).

Phase: \( e^{-j\beta z} \) means phase delay as \( z \) increases (wave travels \( +z \)). Writing \( e^{+j\beta z} \) for a \( +z \) wave is the other Fourier convention; pick one and keep it.

## Equations

Lossless UPW, \( +z \):

\[
\mathbf{E}=\mathrm{Re}\{\hat{x} E_0 e^{j(\omega t-\beta z)}\},\qquad
\mathbf{H}=\frac{E_0}{\eta}\hat{y}\cos(\omega t-\beta z),
\]
\[
\beta=\omega\sqrt{\mu\varepsilon},\quad \eta=\sqrt{\mu/\varepsilon},\quad v_p=1/\sqrt{\mu\varepsilon}.
\]

Propagation constant:

\[
\gamma=\sqrt{j\omega\mu(\sigma+j\omega\varepsilon)}=\alpha+j\beta.
\]

Skin depth: \(\delta=1/\alpha=\sqrt{2/(\omega\mu\sigma)}\) (good conductor).

Average Poynting (peak phasors):

\[
\mathbf{S}_{\mathrm{av}}=\frac12\mathrm{Re}(\tilde{\mathbf{E}}\times\tilde{\mathbf{H}}^*)=\hat{z}\frac{|E_0|^2}{2\eta}\quad(\eta\ \mathrm{real}).
\]

Circular polarization (IEEE, \( +z \) wave, LH or RH depending on sign):

\[
\tilde{\mathbf{E}}=\frac{E_0}{\sqrt{2}}(\hat{x}\mp j\hat{y})e^{-j\beta z}.
\]

Lossy small-loss: \(\alpha\approx\sigma\sqrt{\mu/\varepsilon}/2\).

## Methods

Write the phasor with a direction, get \(\mathbf{H}=\hat{k}\times\mathbf{E}/\eta \) for a forward wave in a lossless medium (\(\hat{k}\) the propagation unit vector). Check \(\mathbf{E}\cdot\hat{k}=0\). Convert to time domain only if asked.

To classify polarization: look at the relative phase of \( E_x,E_y \). If one is zero, linear. If 90° and equal | |, circular. Plot \( E_x(t),E_y(t) \) at \( z=0 \).

Skin depth: if thickness \( t>5\delta \), the sheet is “thick.” At 50 Hz in copper \(\delta\approx 9\) mm; at 1 MHz, 66 µm.

Power through an area: \( \int S_{\mathrm{av}}\cdot\mathrm{d}\mathbf{A} \). For a uniform beam, \( S_{\mathrm{av}}\times A \).

## Mistakes

Using \(\eta_0\) inside a dielectric with \(\varepsilon_r\neq 1\).

\( H=E/\eta_0 \) but \(\mathbf{H}\) parallel to \(\mathbf{E}\).

Phase velocity faster than \( c \) in a waveguide (that can happen; here in a simple dielectric \( v_p\le c \)). Do not panic in unit 10; do not invent it here.

RMS versus peak in Poynting (factor 2).

Polarization sense without stating the viewing direction.

\(\beta=2\pi f/c\) in a dielectric without \( 1/\sqrt{\varepsilon_r} \).

\(\alpha\) in nepers/m treated as dB/m without \( 8.686 \).

A lossless walk-through: \( f=300 \) MHz, free space, \(\lambda=1.00 \) m, \(\beta=6.28 \) rad/m. \( E_0=2.00 \) V/m peak. \( H_0=5.31 \) mA/m. \( S_{\mathrm{av}}=2^2/(2\times 377)=5.31 \) mW/m².

Dielectric \(\varepsilon_r=4\), same \( f \): \( v_p=c/2 \), \(\lambda=0.50 \) m, \(\eta=188.5\,\Omega \). Same \( E_0 \), \( S_{\mathrm{av}}=E_0^2/(2\eta)=10.6 \) mW/m².

Copper 1 MHz: \(\delta=\sqrt{2/(\omega\mu\sigma)}=0.066 \) mm. \(\alpha=1/\delta=1.52\times 10^4 \) Np/m.

Linear pol: \(\mathbf{E}=\hat{x} 3\cos(\omega t-\beta z)+\hat{y} 4\cos(\omega t-\beta z)\), tilt \(\tan^{-1}(4/3)\).

Circular: \( E_y \) lags \( E_x \) by 90° for one sense: \(\mathbf{E}=\hat{x} E_0\cos(\omega t-\beta z)+\hat{y} E_0\sin(\omega t-\beta z)\).

Attenuation 0.1 Np/m is 0.868 dB/m. A 20 m path: 17.4 dB, power ratio \( 10^{-1.74}=0.018 \).

Standing wave against PEC at \( z=0 \): \( E_x=2 E_0\sin(\beta z)\sin(\omega t) \) form (nodes at \( z=n\lambda/2 \)).

Wave in seawater (sketch): high \(\alpha\), radio dies in metres at HF; ELF is a different story. Compute \(\sigma,\varepsilon_r\) before quoting a range.

Intrinsic impedance of a good conductor is small and complex: most of the incident power from air reflects (unit 08 language). A plane-wave model of a metal is a skin-effect surface impedance \( Z_s=(1+j)/(\sigma\delta) \).


Oblique incidence sketch (enough to not be surprised later). Snell: \( n_1\sin\theta_i=n_2\sin\theta_t \) with \( n=\sqrt{\varepsilon_r} \) for nonmagnetic media. Parallel (p, TM) and perpendicular (s, TE) polarizations have different Fresnel coefficients. Brewster angle for no p-reflection: \(\tan\theta_B=n_2/n_1\). Total internal reflection when going to a rarer medium above critical \(\theta_c=\sin^{-1}(n_2/n_1)\). A PEC normal-incidence reflection is \(\Gamma_E=-1\), standing wave, as already stated.

Good conductor interface from air: \(\Gamma_E\approx -1 \), a small skin-depth penetration, surface impedance \( Z_s=R_s(1+j) \), \( R_s=1/(\sigma\delta) \). Power loss per area \( \frac12 R_s |H_{\mathrm{tang}}|^2 \). Waveguide wall loss (unit 10) is this local.

Dispersive media: \( v_p=\omega/\beta(\omega) \) may exceed \( c \); group velocity \(\mathrm{d}\omega/\mathrm{d}\beta\) carries the envelope. Anomalous dispersion is a materials topic. In this unit, constant \(\varepsilon,\mu,\sigma\) suffice.

Inhomogeneous wave: \(\mathbf{E}\) not perpendicular to \(\mathrm{Re}\,\mathbf{k}\) in some lossy-media cases. UG uniform plane wave in a simple lossy medium still has a single \(\gamma\) along z and transverse \(\mathbf{E},\mathbf{H}\).

Polarization mismatch: a CP wave into a linear antenna, 3 dB. Opposite-sense CP into a CP antenna, theoretically zero (orthogonal). Rain and multipath depolarize; UG mention.

Doppler and moving media are out of scope.

Worked \(\gamma\) for seawater sketch \(\sigma=4\) S/m, \(\varepsilon_r=80\), 1 MHz: \(\sigma/(\omega\varepsilon)\approx 9\times 10^3 \), good-conductor-ish, \(\delta=0.25 \) m. 1 GHz: need the actual \(\varepsilon(\omega)\) of water; do not trust \(\varepsilon_r=80\) blindly at microwave.

Worked linear combination: two equal linear polarizations at 90° in space and 90° in time make CP. Two equal in-phase make linear at 45°. The Jones vector \((E_x,E_y)\) is the phasor pair.

Worked dB: \(\alpha_{\mathrm{dB/m}}=8.686\alpha_{\mathrm{Np/m}}\). A material with \(\alpha=0.01\) Np/m is 0.0869 dB/m, 8.69 dB/100 m.

Standing-wave ratio in a lossless medium in front of a PEC is infinite. In front of a dielectric interface \(|\Gamma|<1\), VSWR \(=(1+|\Gamma|)/(1-|\Gamma|)\) like a transmission line (the line is the analog of the 1-D wave).

Poynting of a circularly polarized wave of peak each \( E_0/\sqrt{2} \): average is still \( E_0^2/(2\eta) \) for the same \(|\mathbf{\tilde E}|^2/2\eta \) with \(|\mathbf{\tilde E}|^2=E_0^2 \). Do not double-count.

Group delay through a slab of thickness \(\ell\) is \(\ell/v_g\). For a lossless dielectric, \( v_g=v_p=c/\sqrt{\varepsilon_r} \). A 3 cm slab of \(\varepsilon_r=4\) delays 0.2 ns relative to air? Electrical length \( \sqrt{\varepsilon_r}\ell \), extra delay \( (\sqrt{\varepsilon_r}-1)\ell/c=0.1 \) ns. Useful for a quick phase-shift estimate: \(\beta\ell=2\pi \sqrt{\varepsilon_r}\ell/\lambda_0 \).

When the problem gives \( \mathbf{\tilde E}= (3\mathbf{a}_x-4\mathbf{a}_y)e^{-j2z} \) in free space, \( |\mathbf{E}|=5 \), linear polarization along that vector, \(\beta=2\), \( f=\beta c/(2\pi)=95.5 \) MHz, \( \mathbf{\tilde H}=\hat{z}\times\mathbf{\tilde E}/\eta \).

If \( e^{+j\beta z} \) appears with \( e^{j\omega t} \) implicit, that wave travels \(-z \). Reverse \(\mathbf{H}=\mathbf{E}/\eta\) cross product accordingly (\(\hat k=-\mathbf{a}_z\)).

This unit’s plane wave is infinite. Real beams spread (unit 10 dipole is a spherical wave). Use the plane-wave impedance and Poynting locally in a small region of a spherical wave far from the source (the radiation zone).


Polarization ellipse: axial ratio is the major/minor ratio of the E-locus. Linear is infinite AR (or 0 dB depending on definition — state it). Circular is 1 (0 dB AR). A wave with \( E_x=3 \), \( E_y=4 \), phase 30° is elliptical, not “almost linear.” Compute if asked; otherwise classify by the two special cases.

Loss tangent and \(\alpha\): for a slightly lossy dielectric \(\alpha\approx \pi f \sqrt{\mu\varepsilon}\,\tan\delta \) (nepers/m), equivalent to \(\sigma\eta/2\). PCB FR4 \(\tan\delta\sim 0.02\) at 1 GHz is about 0.6 dB per wavelength in the material, which is why cheap boards get warm in RF power paths.

A uniform plane wave does not exist globally, but it is exact in a parallel-plate TEM region and an excellent local model. When using it for a radio link, multiply \( S_{\mathrm{av}} \) by an effective aperture (unit 10). When using it for a shield, use skin depth and \(\Gamma\approx -1\).

If \(\mathbf{E}\) has a z-component and the wave is said to go in z, it is not a TEM UPW; it may be a waveguide mode (unit 10) or a mistake. Check transversality before computing \(\eta\).

Standing-wave nodes: \( E=0 \) planes every \(\lambda/2\) from a PEC. An inspector with a dipole probe finds nulls; that is a 1-D slotted line in free space. The same VSWR algebra as unit 08 applies with \( Z \) replaced by the wave impedance.
