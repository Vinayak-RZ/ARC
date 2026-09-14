# Questions — Lightning, switching, insulation coordination

Original numbers.

## Q1

### Given

Overhead line \(Z_c=400\,\Omega\), stroke current \(I=20\,\mathrm{kA}\) to a phase conductor, line long in both directions. \(V=I Z_c/2\).

### Find

Surge voltage on the conductor (before flashover).

### Solution

\[
V=\frac{20\times 10^{3}\times 400}{2}=4.00\,\mathrm{MV}.
\]

### Answer

\(4.00\,\mathrm{MV}\)

## Q2

### Given

Junction: overhead \(Z_1=360\,\Omega\) into cable \(Z_2=45\,\Omega\). Incoming step \(v^+=900\,\mathrm{kV}\) on the overhead.

### Find

Voltage reflection coefficient, transmitted voltage into the cable, and reflected voltage wave.

### Solution

\[
\Gamma_v=\frac{45-360}{45+360}=\frac{-315}{405}=-0.778,\qquad T_v=1+\Gamma_v=0.222,
\]
\[
v_{\mathrm{trans}}=0.222\times 900=200\,\mathrm{kV},\qquad v_{\mathrm{refl}}=-0.778\times 900=-700\,\mathrm{kV}.
\]

Check: junction voltage \(900-700=200\,\mathrm{kV}\).

### Answer

\(\Gamma_v=-0.778\), \(v_{\mathrm{t}}=200\,\mathrm{kV}\), \(v_{\mathrm{r}}=-700\,\mathrm{kV}\)

## Q3

### Given

Transformer BIL \(650\,\mathrm{kV}\). Arrester residual voltage \(U_p=280\,\mathrm{kV}\) at the coordinating current. Margin \(M=U_{\mathrm{BIL}}/U_p-1\).

### Find

Coordination margin.

### Solution

\[
M=\frac{650}{280}-1=1.321-1=0.321\quad(32.1\%).
\]

### Answer

\(0.321\) (\(32\%\))

## Q4

### Given

Lossless line, travel time \(\tau=250\,\mu\mathrm{s}\), open receiving end, sending end a step \(E=150\,\mathrm{kV}\) from a matched source (\(R_s=Z_c\)).

### Find

Receiving-end voltage for \(\tau<t<3\tau\).

### Solution

The forward step \(150\,\mathrm{kV}\) arrives at \(t=\tau\). Open-end \(\Gamma=1\), so \(v_r=300\,\mathrm{kV}\). The reflected wave returns to the matched source at \(t=2\tau\) and is absorbed (\(\Gamma_s=0\)). No further wave hits the receiving end until a later event that does not exist here. Thus \(v_r=300\,\mathrm{kV}\) throughout \(\tau<t<3\tau\).

### Answer

\(300\,\mathrm{kV}\)

## Q5

### Given

Capacitive transfer at a transformer: \(C_{HL}=2.0\,\mathrm{nF}\), \(C_{LV}=8.0\,\mathrm{nF}\) (LV to earth). HV surge \(400\,\mathrm{kV}\) at \(t=0^+\).

### Find

LV terminal voltage at \(t=0^+\) (capacitive divider, LV open).

### Solution

\[
V_{LV}=400\times\frac{2.0}{2.0+8.0}=80.0\,\mathrm{kV}.
\]

### Answer

\(80.0\,\mathrm{kV}\)

## Q6

### Given

Tower footing \(R_f=25\,\Omega\), stroke \(I=12\,\mathrm{kA}\) to the tower (ignore \(L di/dt\)). Insulator CFO \(450\,\mathrm{kV}\).

### Find

Tower-top voltage and whether backflashover is expected on this crude \(IR_f\) test.

### Solution

\[
V=I R_f=12\times 10^{3}\times 25=300\,\mathrm{kV}.
\]

\(300<450\): no backflash on this test (footing only).

### Answer

\(300\,\mathrm{kV}\); no backflashover (\(IR_f\) only)
