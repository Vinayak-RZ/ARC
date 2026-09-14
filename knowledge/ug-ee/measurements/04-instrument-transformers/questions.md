# Questions — CT/PT ratio and phase errors

Original pedagogical numbers.

## Q1

### Given

A 200/5 A CT. Primary current 160.0 A, secondary current 3.92 A.

### Find

Nominal ratio \( K_n \) and current (ratio) error \( \varepsilon_i=(K_n I_s-I_p)/I_p \).

### Solution

\( K_n=40 \). \( K_n I_s=156.8 \) A. \( \varepsilon_i=(156.8-160)/160 = -0.020 = -2.00\% \).

### Answer

\( K_n=40 \); \( \varepsilon_i=-2.00\% \).

## Q2

### Given

CT rated 5 A, 10 VA. Secondary leads and meters total \( 0.280\,\Omega \).

### Find

Actual burden VA at rated current, and whether it exceeds 10 VA.

### Solution

\( S=I^2 R=25\times 0.280=7.00 \) VA, below 10 VA.

### Answer

\( 7.00 \) VA; within rating.

## Q3

### Given

PT 6.6 kV/110 V. When the primary is 6.60 kV the secondary is 109.5 V.

### Find

Nominal ratio and ratio error \( (K_n V_s-V_p)/V_p \).

### Solution

\( K_n=60 \). \( K_n V_s=6570 \) V. \( \varepsilon_v=(6570-6600)/6600=-0.455\% \).

### Answer

\( K_n=60 \); \( \varepsilon_v=-0.455\% \).

## Q4

### Given

Lagging load, \( \mathrm{PF}=0.500 \), CT and PT ratio errors negligible, CT phase error \( \beta=+15.0' \), PT phase error \( \gamma=0 \). Use \( \Delta P/P\approx(\beta-\gamma)\tan\phi \) with angles in radians.

### Find

Approximate percent error in measured power.

### Solution

\( \phi=60^\circ \), \( \tan\phi=\sqrt{3} \). \( \beta=15\times\pi/(180\times 60)=0.004363 \) rad. \( \Delta P/P=0.004363\times\sqrt{3}=0.00756=0.756\% \).

### Answer

\( +0.756\% \) (with the stated sign convention).

## Q5

### Given

Metering CT 100/5 A, class 0.5, 15 VA. A student disconnects the 5 A ammeter but leaves the primary carrying 80 A, secondary open.

### Find

What happens to the secondary voltage and what must be done.

### Solution

With \( I_s=0 \), primary ampere-turns magnetize the core; flux and secondary voltage rise to a dangerous value, core may saturate and retain remanence. De-energize the primary; never leave a CT secondary open under load. Short the secondary before removing the meter.

### Answer

Dangerously high secondary voltage; de-energize; never open a live CT secondary.

## Q6

### Given

Wattmeter on CT 50/5 and PT 11 kV/110 V reads 80.0 W on the secondary-side coils (already the electrical watts in those coils).

### Find

Primary power using nominal ratios.

### Solution

\( K_i=10 \), \( K_v=100 \), \( P=K_i K_v \times 80 = 80000 \) W \( =80.0 \) kW.

### Answer

\( 80.0 \) kW.
