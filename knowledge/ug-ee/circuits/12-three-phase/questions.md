# Questions — Balanced and unbalanced three-phase

Original pedagogical numbers.

## Q1

### Given

Balanced abc source, VL = 415 V RMS, 50 Hz. Balanced Y load Z = 24 + j12 Ω per phase. Four-wire.

### Find

Phase voltage, line current, P, Q, and In.

### Solution

\( V_P = 415/\sqrt{3} = 239.6\,\mathrm{V} \). \( Z = 26.83\angle 26.57^\circ\,\Omega \). \( I_L = I_P = 239.6/26.83 = 8.930\,\mathrm{A} \). \( \mathrm{pf} = 0.894 \) lag. \( P = \sqrt{3}\times 415\times 8.930\times 0.894 = 5745\,\mathrm{W} \). \( Q = \sqrt{3}\times 415\times 8.930\times \sin 26.57^\circ = 2873\,\mathrm{var} \). \( I_n = 0 \).

### Answer

VP = 240 V; IL = 8.93 A; P = 5.75 kW; Q = 2.87 kvar; In = 0.

## Q2

### Given

Same 415 V source, Δ load 36 + j18 Ω per branch, balanced.

### Find

Derive Iphase, IL, and P.

### Solution

Each Δ branch sees 415 V. \( Z = 40.25\angle 26.57^\circ \). \( I_\mathrm{ph} = 415/40.25 = 10.31\,\mathrm{A} \). \( I_L = \sqrt{3}\,I_\mathrm{ph} = 17.86\,\mathrm{A} \). \( P = 3 I_\mathrm{ph}^2 R = 3(10.31)^2(36) = 11480\,\mathrm{W} \), also \( \sqrt{3} V_L I_L \cos\theta = 1.732\times 415\times 17.86\times 0.894 = 11480\,\mathrm{W} \). Equivalent ZY = ZΔ/3 = 12+j6, IL = 239.6/13.42 = 17.86 A, same.

### Answer

Iph = 10.3 A; IL = 17.9 A; P = 11.5 kW.

## Q3

### Given

Design three Δ-connected capacitors to correct the Q1 load to unity pf on a 415 V 50 Hz bus.

### Find

C per branch.

### Solution

Q to cancel = 2873 var total, 958 var per Δ capacitor. Each capacitor sees 415 V. \( C = Q/(\omega V^2) = 958/(2\pi 50 \times 415^2) = 17.7\,\mu\mathrm{F} \) per branch. (If Y-connected, each would see 240 V and C would be 3 times larger.)

### Answer

17.7 µF per Δ branch.

## Q4

### Given

A student computes P = 3 × 415 × 8.93 × 0.894 for the Y load of Q1.

### Find

Explain the error and the factor they used wrongly.

### Solution

The balanced formula is \( \sqrt{3} V_L I_L \cos\theta \) or \( 3 V_P I_P \cos\theta \). Using 3 VL IL overstates by \( \sqrt{3} \). They mixed the 3 from three phases with line voltage instead of phase voltage.

### Answer

Wrong 3 VL IL; correct is √3 VL IL, giving 5.75 kW not 9.95 kW.

## Q5

### Given

Three-wire Y, source balanced VP = 120 V RMS, Za = 10 Ω, Zb = 10 Ω, Zc = ∞ (open). Source-neutral reference.

### Find

Load-neutral voltage Vn and Ia (approximate by nodal).

### Solution

Yc = 0, Ya = Yb = 0.1 S. \( V_n = (V_a + V_b) Ya / (Ya+Yb) = (V_a+V_b)/2 \). \( V_a = 120\angle 0 \), \( V_b = 120\angle -120 \), sum = 120(1 − 0.5 − j0.866) = 60 − j103.9 = 120\angle -60°, so Vn = 60∠−60° V. Then Va − Vn = 120∠0 − 60∠−60 = 120 − 30 + j51.96 = 90 + j51.96 = 103.9∠30°. Ia = (Va−Vn)/10 = 10.39∠30° A. Ib = −Ia because In must be 0 and Ic = 0, so two-phase current loop. Check: Vb−Vn = 120∠−120 − 60∠−60 = −60 − j103.9 − 30 + j51.96 = −90 − j51.96 = 103.9∠−150°, Ib = 10.39∠−150° = −10.39∠30°, yes.

### Answer

Vn = 60∠−60° V; Ia = 10.4∠30° A; Ib = −Ia; Ic = 0.
