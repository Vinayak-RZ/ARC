# Worked questions — JFET and MOSFET

## Q1
### Given
n-channel JFET, \(I_{DSS}=8.0\,\mathrm{mA}\), \(V_P=-4.0\,\mathrm{V}\), self-bias \(R_S=680\,\Omega\), gate grounded through \(R_G\), drain resistor \(R_D=2.2\,\mathrm{k}\Omega\), \(V_{DD}=15\,\mathrm{V}\).
### Find
\(I_D\), \(V_{GS}\), \(V_{DS}\). Confirm saturation.
### Solution
Shockley: \(I_D=8(1-V_{GS}/(-4))^2\,\mathrm{mA}\), \(V_{GS}=-I_D R_S=-0.68 I_D\) with \(I_D\) in mA. Let \(x=\sqrt{I_D/8}\), \(I_D=8x^2\), \(V_{GS}=-4(1-x)\). Also \(V_{GS}=-0.68\times 8x^2=-5.44 x^2\). So \(-4+4x=-5.44 x^2\), \(5.44 x^2+4x-4=0\). \(x=\frac{-4+\sqrt{16+87.04}}{10.88}=\frac{-4+10.15}{10.88}=0.565\). \(I_D=8(0.319)=2.55\,\mathrm{mA}\). \(V_{GS}=-0.68\times 2.55=-1.74\,\mathrm{V}\). \(V_{DS}=15-I_D(R_D+R_S)=15-2.55\times 2.88=7.66\,\mathrm{V}\). Pinch-off at drain requires \(V_{DS}\ge V_{GS}-V_P=-1.74-(-4)=2.26\,\mathrm{V}\). \(7.66>2.26\), saturation.
### Answer
\(I_D=2.55\,\mathrm{mA}\), \(V_{GS}=-1.74\,\mathrm{V}\), \(V_{DS}=7.66\,\mathrm{V}\) (saturation)

## Q2
### Given
Enhancement nMOS, \(V_t=0.70\,\mathrm{V}\), \(k_n'(W/L)=0.40\,\mathrm{mA/V^2}\), \(\lambda=0\). Drain-feedback bias: \(R_D=4.7\,\mathrm{k}\Omega\), \(R_G=2.2\,\mathrm{M}\Omega\), \(V_{DD}=10\,\mathrm{V}\).
### Find
\(I_D\) and \(V_{GS}\). Confirm saturation.
### Solution
\(I_G=0\) so \(V_{DS}=V_{GS}\). Square law: \(I_D=0.20(V_{GS}-0.70)^2\,\mathrm{mA}\) with \(I_D=(10-V_{GS})/4.7\,\mathrm{mA}\) if voltages in V and \(R_D\) in kΩ. Let \(v=V_{GS}\). \((10-v)/4.7=0.20(v-0.70)^2\). Try \(v=2.4\): RHS \(0.20(1.7)^2=0.578\), LHS \(1.617\) — too small \(I_D\) from square law. Higher \(v\) increases square-law current. Try \(v=3.2\): RHS \(0.20(2.5)^2=1.250\), LHS \(1.447\). Try \(v=3.35\): RHS \(0.20(2.65)^2=1.405\), LHS \(1.415\). Close: \(V_{GS}=3.35\,\mathrm{V}\), \(I_D=1.41\,\mathrm{mA}\). Saturation: \(V_{DS}=V_{GS}>V_{GS}-V_t\), always for \(V_t>0\).
### Answer
\(I_D=1.41\,\mathrm{mA}\), \(V_{GS}=V_{DS}=3.35\,\mathrm{V}\) (saturation)

## Q3
### Given
nMOS in saturation, \(I_D=0.80\,\mathrm{mA}\), \(k_n'(W/L)=1.00\,\mathrm{mA/V^2}\), \(V_t=0.50\,\mathrm{V}\), \(\lambda=0.05\,\mathrm{V}^{-1}\). Unbypassed source degeneration \(R_S=0\), \(R_D=10\,\mathrm{k}\Omega\), no external load.
### Find
\(V_{OV}\), \(g_m\), \(r_o\), and \(A_v=-g_m(R_D\parallel r_o)\).
### Solution
\(0.80=0.50 V_{OV}^2\Rightarrow V_{OV}=\sqrt{1.6}=1.265\,\mathrm{V}\). \(g_m=2I_D/V_{OV}=1.264\,\mathrm{mS}\). \(r_o=1/(0.05\times 0.80\times 10^{-3})=25\,\mathrm{k}\Omega\). \(R_D\parallel r_o=7.14\,\mathrm{k}\Omega\). \(A_v=-1.264\times 7.14=-9.03\).
### Answer
\(V_{OV}=1.26\,\mathrm{V}\), \(g_m=1.26\,\mathrm{mS}\), \(r_o=25\,\mathrm{k}\Omega\), \(A_v=-9.03\)

## Q4
### Given
nMOS used as a switch, \(V_{GS}=5.0\,\mathrm{V}\), \(V_t=0.80\,\mathrm{V}\), \(k_n'(W/L)=2.0\,\mathrm{mA/V^2}\), drain-source voltage small (deep triode).
### Find
\(r_{DS,on}\).
### Solution
\(r_{DS,on}=1/[k_n'(W/L)(V_{GS}-V_t)]=1/[2.0\times 10^{-3}\times 4.2]=119\,\Omega\).
### Answer
\(r_{DS,on}=119\,\Omega\)

## Q5
### Given
Voltage-divider nMOS: \(V_{DD}=12\,\mathrm{V}\), \(R_1=R_2=100\,\mathrm{k}\Omega\), \(R_S=1.5\,\mathrm{k}\Omega\), \(R_D=3.3\,\mathrm{k}\Omega\), \(V_t=1.0\,\mathrm{V}\), \(k_n'(W/L)=0.50\,\mathrm{mA/V^2}\), \(\lambda=0\), source-bulk tied.
### Find
\(I_D\) and whether the device is in saturation.
### Solution
\(I_G=0\Rightarrow V_G=6.0\,\mathrm{V}\). \(V_{GS}=6-I_D R_S\), \(I_D=0.25(V_{GS}-1)^2\,\mathrm{mA}\). Let \(I\) be mA: \(V_{GS}=6-1.5I\), \(I=0.25(5-1.5I)^2\). Let \(u=5-1.5I\), \(I=(5-u)/1.5\), \((5-u)/1.5=0.25 u^2\), \(5-u=0.375 u^2\), \(0.375 u^2+u-5=0\). \(u=\frac{-1+\sqrt{1+7.5}}{0.75}=\frac{-1+2.915}{0.75}=2.554\,\mathrm{V}=V_{OV}\). \(I_D=0.25(2.554)^2=1.63\,\mathrm{mA}\). \(V_S=1.5\times 1.63=2.45\,\mathrm{V}\), \(V_{GS}=3.55\,\mathrm{V}\). \(V_D=12-1.63\times 3.3=6.62\,\mathrm{V}\), \(V_{DS}=4.17\,\mathrm{V}\). Need \(V_{DS}\ge V_{OV}=2.55\,\mathrm{V}\): yes, saturation.
### Answer
\(I_D=1.63\,\mathrm{mA}\), saturation (\(V_{DS}=4.17\,\mathrm{V}\ge V_{OV}=2.55\,\mathrm{V}\))
