# Worked questions — regulators and power amps

## Q1
### Given
Zener-follower regulator: \(V_Z=6.2\,\mathrm{V}\), \(V_{BE}=0.70\,\mathrm{V}\), \(\beta=80\), \(R_s=180\,\Omega\) from \(V_{in}=12.0\,\mathrm{V}\) to the Zener (base). Load \(I_L=80\,\mathrm{mA}\).
### Find
\(V_{out}\) and \(I_Z\). Confirm the Zener still conducts.
### Solution
\(V_{out}=6.2-0.70=5.50\,\mathrm{V}\). \(I_B=I_L/(\beta+1)=80/81=0.988\,\mathrm{mA}\). Current in \(R_s\): \((12.0-6.2)/180=32.22\,\mathrm{mA}\). \(I_Z=32.22-0.988=31.2\,\mathrm{mA}>0\).
### Answer
\(V_{out}=5.50\,\mathrm{V}\), \(I_Z=31.2\,\mathrm{mA}\) (in breakdown)

## Q2
### Given
7805-style loop, \(V_{out}=5.00\,\mathrm{V}\), \(I_L=1.20\,\mathrm{A}\), \(V_{in}=9.0\,\mathrm{V}\), \(\theta_{JA}=25^\circ\mathrm{C/W}\) with the intended heatsink, \(T_a=45^\circ\mathrm{C}\), \(T_{j,\max}=125^\circ\mathrm{C}\). Quiescent IC current neglected.
### Find
\(P_D\), \(T_j\), and whether the thermal budget is OK. Efficiency \(\eta\).
### Solution
\(P_D=(9.0-5.0)\times 1.20=4.80\,\mathrm{W}\). \(T_j=45+4.80\times 25=165^\circ\mathrm{C}>125^\circ\mathrm{C}\), not OK. \(\eta=5/9=55.6\,\%\).
### Answer
\(P_D=4.80\,\mathrm{W}\), \(T_j=165^\circ\mathrm{C}\) (fails \(T_{j,\max}\)), \(\eta=55.6\,\%\)

## Q3
### Given
Class-B complementary emitter followers, \(\pm 18\,\mathrm{V}\) rails, \(R_L=8.0\,\Omega\), full-swing sine with \(V_m=16\,\mathrm{V}\) (allowing 2 V for \(V_{BE}\) and saturation). Ideal except finite swing.
### Find
Load power, DC supply power from both rails, efficiency, and dissipation per output transistor.
### Solution
\(P_L=V_m^2/(2R_L)=256/16=16.0\,\mathrm{W}\). \(P_{dc}=2 V_{CC} V_m/(\pi R_L)=2\times 18\times 16/(\pi\times 8)=22.92\,\mathrm{W}\). \(\eta=16.0/22.92=69.8\,\%\). \(P_{D,\mathrm{each}}=(22.92-16.0)/2=3.46\,\mathrm{W}\).
### Answer
\(P_L=16.0\,\mathrm{W}\), \(P_{dc}=22.9\,\mathrm{W}\), \(\eta=69.8\,\%\), \(P_{D,\mathrm{each}}=3.46\,\mathrm{W}\)

## Q4
### Given
Class-A CE, \(V_{CC}=20\,\mathrm{V}\), \(R_C=100\,\Omega\) (resistive load, no transformer), Q-point \(I_C=100\,\mathrm{mA}\), \(V_{CE}=10\,\mathrm{V}\). Maximum symmetric AC swing along the DC load line, \(R_L=R_C\).
### Find
Maximum AC load power and efficiency at that swing. Compare with the 25 % ceiling.
### Solution
Load line from \((I_C,V_{CE})=(0,20\,\mathrm{V})\) to \((200\,\mathrm{mA},0)\). Symmetric swing about Q is \(V_m=10\,\mathrm{V}\), \(I_m=100\,\mathrm{mA}\). \(P_L=V_m I_m/2=0.50\,\mathrm{W}\). \(P_{dc}=V_{CC} I_C=2.0\,\mathrm{W}\). \(\eta=25\,\%\), which is the resistive-load ceiling.
### Answer
\(P_L=0.50\,\mathrm{W}\), \(\eta=25\,\%\)

## Q5
### Given
\(V_{BE}\) multiplier, \(V_{BE}=0.70\,\mathrm{V}\), \(R_1=1.0\,\mathrm{k}\Omega\) (between base and emitter of the multiplier transistor), \(R_2=1.8\,\mathrm{k}\Omega\) (between collector and base). Used as class-AB bias between complementary bases.
### Find
\(V_{\mathrm{bias}}\) and the idle \(V_{BE}\) budget per output transistor if they share it equally.
### Solution
\(V_{\mathrm{bias}}=0.70(1+1.8/1.0)=1.96\,\mathrm{V}\). Each output device is biased at \(0.98\,\mathrm{V}\), so both are slightly on (class AB) if they are silicon parts with \(V_{BE}\approx 0.70\,\mathrm{V}\). Idle current needs the output devices' \(I_C(V_{BE})\) curve; this problem only asks for the bias voltage.
### Answer
\(V_{\mathrm{bias}}=1.96\,\mathrm{V}\) (\(0.98\,\mathrm{V}\) per complementary base)
