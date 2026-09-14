# Worked questions — DC–DC choppers

## Q1
### Given
A CCM buck chopper has input \(V_{in}=96\,\mathrm{V}\) and duty ratio \(D=0.42\). Switches and diode are ideal. Load is such that inductor current stays continuous.
### Find
The average output voltage \(V_{out}\).
### Solution
Buck CCM conversion is \(V_{out}=D V_{in}=0.42\times 96=40.32\,\mathrm{V}\).
### Answer
\(V_{out}=40.3\,\mathrm{V}\)

## Q2
### Given
A CCM boost converter must produce \(V_{out}=36\,\mathrm{V}\) from \(V_{in}=12\,\mathrm{V}\). Ideal devices.
### Find
The required duty ratio \(D\).
### Solution
\(V_{out}/V_{in}=1/(1-D)=36/12=3\). Thus \(1-D=1/3\), \(D=2/3=0.667\).
### Answer
\(D=0.667\)

## Q3
### Given
An inverting CCM buck–boost, \(V_{in}=24\,\mathrm{V}\), \(D=0.55\). Ideal.
### Find
\(V_{out}\) (include sign) and the switch off-state voltage stress \(V_{in}+|V_{out}|\).
### Solution
\(V_{out}=-D/(1-D)\times 24=-(0.55/0.45)\times 24=-29.33\,\mathrm{V}\). Stress \(24+29.33=53.33\,\mathrm{V}\).
### Answer
\(V_{out}=-29.3\,\mathrm{V}\), stress \(53.3\,\mathrm{V}\)

## Q4
### Given
Buck, \(V_{in}=48\,\mathrm{V}\), \(V_{out}=18\,\mathrm{V}\) CCM, \(f_s=25\,\mathrm{kHz}\), \(L=220\,\mu\mathrm{H}\), \(R=6.0\,\Omega\).
### Find
Duty \(D\), average load current, inductor current ripple \(\Delta i_L\), and whether CCM holds.
### Solution
\(D=18/48=0.375\). \(I_{out}=18/6=3.00\,\mathrm{A}\). \(\Delta i_L=V_{out}(1-D)/(f_s L)=18\times 0.625/(25000\times 220\times 10^{-6})=2.045\,\mathrm{A}\). Half-ripple \(1.023\,\mathrm{A}<3.00\,\mathrm{A}\), so CCM holds.
### Answer
\(D=0.375\), \(I_{out}=3.00\,\mathrm{A}\), \(\Delta i_L=2.05\,\mathrm{A}\), CCM yes

## Q5
### Given
A first-quadrant (buck) DC chopper feeds a motor armature \(E_a=75\,\mathrm{V}\), \(R_a=0.50\,\Omega\). Bus \(V_{in}=110\,\mathrm{V}\). Armature current \(20\,\mathrm{A}\) continuous. Ideal switch and freewheel diode.
### Find
Required duty ratio and the average armature terminal voltage.
### Solution
\(V_t=E_a+I_a R_a=75+10=85\,\mathrm{V}\). \(D=V_t/V_{in}=85/110=0.773\).
### Answer
\(V_t=85.0\,\mathrm{V}\), \(D=0.773\)

## Q6
### Given
A bipolar PWM H-bridge chopper, \(V_{in}=200\,\mathrm{V}\), duty of the positive pair \(D=0.62\) (so the complementary pair has \(1-D\)). CCM-like averaging, ideal.
### Find
Average output voltage.
### Solution
\(V_{out}=(2D-1)V_{in}=(1.24-1)\times 200=48.0\,\mathrm{V}\).
### Answer
\(V_{out}=48.0\,\mathrm{V}\)
