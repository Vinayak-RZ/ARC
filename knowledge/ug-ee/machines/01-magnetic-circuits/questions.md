# Questions — B-H, reluctance, inductance from energy

Original numbers. SI throughout.

## Q1

### Given

A magnetic core has mean steel path \(\ell_c=0.40\ \mathrm{m}\), net iron area \(A_c=16\times 10^{-4}\ \mathrm{m}^2\), and a uniform air gap \(\ell_g=1.0\ \mathrm{mm}\) of area \(A_g=A_c\). Relative permeability of the steel is constant \(\mu_r=2500\). A coil of \(N=250\) turns carries \(i=2.0\ \mathrm{A}\). Neglect leakage and fringing.

### Find

Flux \(\Phi\) in the gap and flux density \(B_g\).

### Solution

Reluctances:

\[
\mathcal{R}_c = \frac{\ell_c}{\mu_0\mu_r A_c} = \frac{0.40}{(4\pi\times 10^{-7})(2500)(16\times 10^{-4})} = 7.958\times 10^4\ \mathrm{A/Wb}.
\]

\[
\mathcal{R}_g = \frac{\ell_g}{\mu_0 A_g} = \frac{0.001}{(4\pi\times 10^{-7})(16\times 10^{-4})} = 4.974\times 10^5\ \mathrm{A/Wb}.
\]

\[
\mathcal{R} = \mathcal{R}_c+\mathcal{R}_g = 5.770\times 10^5\ \mathrm{A/Wb}.
\]

MMF \(\mathcal{F}=Ni=500\ \mathrm{AT}\). Flux:

\[
\Phi = \frac{\mathcal{F}}{\mathcal{R}} = \frac{500}{5.770\times 10^5} = 8.666\times 10^{-4}\ \mathrm{Wb}.
\]

\[
B_g = \frac{\Phi}{A_g} = \frac{8.666\times 10^{-4}}{16\times 10^{-4}} = 0.542\ \mathrm{T}.
\]

The gap takes about 86% of the MMF.

### Answer

\(\Phi=8.67\times 10^{-4}\ \mathrm{Wb}\), \(B_g=0.542\ \mathrm{T}\)

## Q2

### Given

The linear magnetic circuit of Q1 (same \(\mathcal{R}\), \(N=250\)).

### Find

Coil inductance \(L\) and stored energy at \(i=2.0\ \mathrm{A}\).

### Solution

\[
L = \frac{N^2}{\mathcal{R}} = \frac{250^2}{5.770\times 10^5} = 0.1083\ \mathrm{H}.
\]

Alternatively \(L=N\Phi/i = 250(8.666\times 10^{-4})/2.0 = 0.1083\ \mathrm{H}\).

\[
W = \tfrac12 L i^2 = 0.5(0.1083)(4) = 0.217\ \mathrm{J}.
\]

### Answer

\(L=0.108\ \mathrm{H}\), \(W=0.217\ \mathrm{J}\)

## Q3

### Given

A rectangular air gap \(20\ \mathrm{mm}\times 30\ \mathrm{mm}\) with length \(\ell_g=2.0\ \mathrm{mm}\). Use the first-order fringing correction \(A_g=(a+\ell_g)(b+\ell_g)\). Steel reluctance is negligible. \(N=400\) turns, \(i=3.0\ \mathrm{A}\).

### Find

Gap flux \(\Phi\) with fringing, and the percent increase relative to no-fringing \(A=20\times 30\ \mathrm{mm}^2\).

### Solution

No fringing: \(A=6.0\times 10^{-4}\ \mathrm{m}^2\), \(\mathcal{R}_0=\ell_g/(\mu_0 A)=2.653\times 10^6\ \mathrm{A/Wb}\).

With fringing:

\[
A_g = (0.020+0.002)(0.030+0.002)=7.04\times 10^{-4}\ \mathrm{m}^2,
\]

\[
\mathcal{R}_g = \frac{0.002}{(4\pi\times 10^{-7})(7.04\times 10^{-4})} = 2.261\times 10^6\ \mathrm{A/Wb}.
\]

\[
\Phi = \frac{Ni}{\mathcal{R}_g} = \frac{1200}{2.261\times 10^6} = 5.308\times 10^{-4}\ \mathrm{Wb}.
\]

Without fringing \(\Phi_0 = 1200/2.653\times 10^6 = 4.523\times 10^{-4}\ \mathrm{Wb}\). Increase: \((5.308-4.523)/4.523 = 17.4\%\).

### Answer

\(\Phi=5.31\times 10^{-4}\ \mathrm{Wb}\) (17% higher than no-fringing)

## Q4

### Given

A singly excited linear plunger has \(L(x)=4.0\times 10^{-3}/x\) henries with \(x\) in metres (\(2\ \mathrm{mm}\le x\le 10\ \mathrm{mm}\)). Current is held at \(i=5.0\ \mathrm{A}\). Instantaneous gap \(x=4.0\ \mathrm{mm}\).

### Find

Electromagnetic force \(f_e\) (sign: positive if it tends to increase \(x\)).

### Solution

Coenergy \(W'=\tfrac12 L(x) i^2\). Force at constant current:

\[
f_e = \frac{\partial W'}{\partial x} = \tfrac12 i^2 \frac{\mathrm{d}L}{\mathrm{d}x} = \tfrac12 (25)\left(-\frac{4.0\times 10^{-3}}{x^2}\right).
\]

At \(x=0.004\):

\[
\frac{\mathrm{d}L}{\mathrm{d}x} = -\frac{4.0\times 10^{-3}}{(0.004)^2} = -250\ \mathrm{H/m},
\]

\[
f_e = 12.5\times(-250) = -3125\ \mathrm{N}.
\]

The negative sign means attraction (gap wants to close). Magnitude 3.13 kN.

### Answer

\(f_e=-3.13\ \mathrm{kN}\) (attractive)

## Q5

### Given

A toroidal core, no gap, mean length \(0.25\ \mathrm{m}\), net area \(5.0\times 10^{-4}\ \mathrm{m}^2\). The DC magnetization curve is linear up to \(B=1.2\ \mathrm{T}\) with \(\mu_r=4000\), then perfectly flat (hard saturation). Coil \(N=200\) turns.

### Find

Current \(i\) needed for \(B=1.2\ \mathrm{T}\), and the apparent inductance \(\lambda/i\) if someone forces \(B=1.5\ \mathrm{T}\) while still using the unsaturated \(\mu_r\) by mistake versus the saturated reality (\(H\) from Ampere with \(B\) clamped at 1.2 T cannot reach 1.5 T). Report \(i\) at the knee and state whether \(B=1.5\ \mathrm{T}\) is possible in this model.

### Solution

Unsaturated, \(B=1.2\ \mathrm{T}\):

\[
H = \frac{B}{\mu_0\mu_r} = \frac{1.2}{(4\pi\times 10^{-7})(4000)} = 238.7\ \mathrm{A/m},
\]

\[
i = \frac{H\ell}{N} = \frac{238.7\times 0.25}{200} = 0.298\ \mathrm{A}.
\]

In the hard-saturation model \(B\) cannot exceed 1.2 T at any finite \(H\). Requesting 1.5 T is inconsistent: extra current only increases \(H\), not \(B\). Apparent inductance at the knee:

\[
L=\frac{N B A}{i}=\frac{200(1.2)(5.0\times 10^{-4})}{0.298}=0.403\ \mathrm{H}.
\]

Beyond the knee, \(\mathrm{d}\lambda/\mathrm{d}i=0\) in this idealization, so incremental inductance collapses.

### Answer

\(i=0.298\ \mathrm{A}\) at \(B=1.2\ \mathrm{T}\); \(B=1.5\ \mathrm{T}\) is impossible in this model

## Q6

### Given

Two identical air gaps in parallel share a pole flux \(\Phi=1.2\times 10^{-3}\ \mathrm{Wb}\). Each gap: \(\ell_g=1.5\ \mathrm{mm}\), \(A_g=8.0\times 10^{-4}\ \mathrm{m}^2\). Steel MMF drop is 80 AT. Coil has \(N=150\) turns.

### Find

Coil current \(i\).

### Solution

One gap: \(\mathcal{R}_g=\ell_g/(\mu_0 A_g)=1.5\times 10^{-3}/((4\pi\times 10^{-7})(8.0\times 10^{-4}))=1.492\times 10^6\ \mathrm{A/Wb}\).

Two identical gaps in parallel: \(\mathcal{R}_\mathrm{eq}=\mathcal{R}_g/2=7.460\times 10^5\ \mathrm{A/Wb}\).

Gap MMF: \(\mathcal{R}_\mathrm{eq}\Phi=(7.460\times 10^5)(1.2\times 10^{-3})=895.2\ \mathrm{AT}\).

Total MMF \(895.2+80=975.2\ \mathrm{AT}\). Current \(i=975.2/150=6.50\ \mathrm{A}\).

### Answer

\(i=6.50\ \mathrm{A}\)
