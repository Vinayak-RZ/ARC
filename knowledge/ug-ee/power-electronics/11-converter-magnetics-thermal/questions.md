# Worked questions — converter magnetics and thermal

## Q1
### Given
CCM buck, \(V_{out}=15\,\mathrm{V}\), \(D=0.40\), \(f_s=40\,\mathrm{kHz}\), allowed \(\Delta i_L=0.80\,\mathrm{A}\).
### Find
The inductance \(L\).
### Solution
\(L=V_{out}(1-D)/(f_s\Delta i)=15\times 0.60/(40000\times 0.80)=281\,\mu\mathrm{H}\).
### Answer
\(L=281\,\mu\mathrm{H}\)

## Q2
### Given
That inductor carries \(I_{\mathrm{dc}}=3.0\,\mathrm{A}\) plus the 0.80 A peak-to-peak ripple. Core \(A_e=1.2\,\mathrm{cm}^2\), \(N=24\) turns.
### Find
Peak current and flux-density swing \(\Delta B\) on the on-interval of the buck (use \((V_{in}-V_{out})D T_s=N A_e\Delta B\) with \(V_{in}=V_{out}/D=37.5\,\mathrm{V}\)).
### Solution
\(I_{\mathrm{pk}}=3.0+0.40=3.40\,\mathrm{A}\). \(T_s=25\,\mu\mathrm{s}\), \(t_{\mathrm{on}}=10\,\mu\mathrm{s}\). \(\int v dt=(37.5-15)\times 10\times 10^{-6}=225\,\mu\mathrm{V\cdot s}\). \(A_e=1.2\times 10^{-4}\,\mathrm{m}^2\). \(\Delta B=225\times 10^{-6}/(24\times 1.2\times 10^{-4})=0.0781\,\mathrm{T}\).
### Answer
\(I_{\mathrm{pk}}=3.40\,\mathrm{A}\), \(\Delta B=0.078\,\mathrm{T}\)

## Q3
### Given
IGBT loss \(P_D=35\,\mathrm{W}\), \(\theta_{JC}=0.50\,\mathrm{K/W}\), \(\theta_{CS}=0.25\,\mathrm{K/W}\), \(T_A=40^\circ\mathrm{C}\), \(T_{J,\max}=125^\circ\mathrm{C}\).
### Find
The maximum allowed \(\theta_{SA}\).
### Solution
Budget \(125-40=85\,\mathrm{K}\). \(85/35=2.429\,\mathrm{K/W}\) total. \(\theta_{SA}\le 2.429-0.50-0.25=1.68\,\mathrm{K/W}\).
### Answer
\(\theta_{SA}\le 1.68\,\mathrm{K/W}\)

## Q4
### Given
Flyback CCM, \(V_{in}=48\,\mathrm{V}\), \(V_{out}=12\,\mathrm{V}\), diode drop 0.7 V, \(N_s/N_p=1/3\), ideal otherwise.
### Find
Duty ratio \(D\).
### Solution
\(V_{out}+V_F=(N_s/N_p) V_{in} D/(1-D)\). \(12.7=(1/3)\times 48\times D/(1-D)=16 D/(1-D)\). \(12.7-12.7 D=16 D\), \(12.7=28.7 D\), \(D=0.443\).
### Answer
\(D=0.443\)

## Q5
### Given
Forward converter, 1:1 reset winding, \(V_{in}=160\,\mathrm{V}\), \(D=0.45\), \(f_s=50\,\mathrm{kHz}\).
### Find
On-time and whether the simple \(D\le 0.5\) reset rule is satisfied. Magnetizing reset time at \(V_{in}\) on the reset winding.
### Solution
\(T_s=20\,\mu\mathrm{s}\), \(t_{\mathrm{on}}=9.0\,\mu\mathrm{s}\). Reset needs \(t_{\mathrm{reset}}\ge t_{\mathrm{on}}=9\,\mu\mathrm{s}\). Off-time \(11\,\mu\mathrm{s}>9\,\mu\mathrm{s}\), so yes. Margin \(2\,\mu\mathrm{s}\).
### Answer
\(t_{\mathrm{on}}=9.0\,\mu\mathrm{s}\); reset OK (\(11\,\mu\mathrm{s}\) available)

## Q6
### Given
Boost CCM inductor, \(V_{in}=24\,\mathrm{V}\), \(D=0.60\), \(f_s=25\,\mathrm{kHz}\), \(\Delta i_L=2.0\,\mathrm{A}\). Then \(V_{out}=V_{in}/(1-D)\).
### Find
\(L\), \(V_{out}\), and energy \(\tfrac12 L I_{\mathrm{pk}}^2\) if \(I_{L,\mathrm{avg}}=8.0\,\mathrm{A}\).
### Solution
\(L=V_{in} D/(f_s\Delta i)=24\times 0.60/(25000\times 2)=288\,\mu\mathrm{H}\). \(V_{out}=24/0.40=60\,\mathrm{V}\). \(I_{\mathrm{pk}}=8+1=9.0\,\mathrm{A}\). \(E=0.5\times 288\times 10^{-6}\times 81=11.7\,\mathrm{mJ}\).
### Answer
\(L=288\,\mu\mathrm{H}\), \(V_{out}=60\,\mathrm{V}\), \(E=11.7\,\mathrm{mJ}\)
