# Worked questions — phase-controlled converters

## Q1
### Given
A single-phase fully controlled bridge, ideal SCRs, \(v_s=230\sqrt{2}\sin\omega t\) V, highly inductive load, \(I_{dc}=16\,\mathrm{A}\), firing angle \(\alpha=40^\circ\). No source inductance.
### Find
Average DC voltage, DC power, and displacement factor in the ideal square-current model.
### Solution
\(V_m=325.27\,\mathrm{V}\). \(V_{dc}=(2V_m/\pi)\cos 40^\circ=207.1\times 0.7660=158.6\,\mathrm{V}\). \(P_{dc}=158.6\times 16=2538\,\mathrm{W}\). Displacement factor \(\cos\alpha=0.766\) lagging.
### Answer
\(V_{dc}=159\,\mathrm{V}\), \(P=2.54\,\mathrm{kW}\), \(\mathrm{DF}=0.766\) lag

## Q2
### Given
A single-phase semi-converter (half-controlled), same 230 V RMS source, \(\alpha=40^\circ\), constant \(I_{dc}=16\,\mathrm{A}\).
### Find
Average DC voltage and DC power.
### Solution
\(V_{dc}=(V_m/\pi)(1+\cos 40^\circ)=(325.27/\pi)(1+0.7660)=182.7\,\mathrm{V}\). \(P=182.7\times 16=2923\,\mathrm{W}\).
### Answer
\(V_{dc}=183\,\mathrm{V}\), \(P=2.92\,\mathrm{kW}\)

## Q3
### Given
Three-phase fully controlled bridge, \(V_{LL}=415\,\mathrm{V}\), \(\alpha=50^\circ\), \(I_{dc}=40\,\mathrm{A}\), \(L_s=0.70\,\mathrm{mH}\), 50 Hz. Continuous current.
### Find
Overlap drop, \(V_{dc}\), and overlap angle \(u\).
### Solution
\(V_{dc0}=(3\sqrt{2}/\pi)415\cos 50^\circ=560.2\times 0.6428=360.1\,\mathrm{V}\). Drop \(3\omega L_s I_{dc}/\pi=3\times 314.16\times 0.0007\times 40/\pi=8.40\,\mathrm{V}\). \(V_{dc}=351.7\,\mathrm{V}\). \(\cos\alpha-\cos(\alpha+u)=2\omega L_s I_{dc}/(\sqrt{2}V_{LL})=2\times 314.16\times 0.0007\times 40/(415\sqrt{2})=0.0302\). \(\cos(\alpha+u)=\cos 50^\circ-0.0302=0.6126\), \(\alpha+u=52.2^\circ\), \(u=2.2^\circ\).
### Answer
drop \(8.40\,\mathrm{V}\), \(V_{dc}=352\,\mathrm{V}\), \(u=2.2^\circ\)

## Q4
### Given
A three-phase fully controlled bridge should invert into a 415 V AC line. DC current \(I_{dc}=20\,\mathrm{A}\) is held by a machine. Required \(V_{dc}=-400\,\mathrm{V}\) (thyristor current still positive). No overlap, no extinction margin yet.
### Find
The firing angle \(\alpha\).
### Solution
\(V_{dc0}=1.3505\times 415=560.2\,\mathrm{V}\). \(\cos\alpha=V_{dc}/V_{dc0}=-400/560.2=-0.7140\). \(\alpha=135.6^\circ\).
### Answer
\(\alpha=136^\circ\)

## Q5
### Given
Inversion as in Q4, but now \(u=12^\circ\) and the required turn-off (extinction) angle is \(\gamma=8^\circ\).
### Find
Whether \(\alpha=135.6^\circ\) is legal, and the maximum \(\alpha\) allowed by \(\alpha+u+\gamma\le 180^\circ\).
### Solution
\(135.6+12+8=155.6^\circ\le 180^\circ\), so the angle is legal. Maximum \(\alpha=180-12-8=160^\circ\). Corresponding most-negative ideal voltage \(V_{dc}=560.2\cos 160^\circ=-526\,\mathrm{V}\) (overlap would reduce the magnitude slightly).
### Answer
Legal; \(\alpha_{\max}=160^\circ\)

## Q6
### Given
A DC motor armature is modelled as \(E_a=110\,\mathrm{V}\), \(R_a=0.40\,\Omega\), fed from a single-phase fully controlled bridge with \(V_{dc}=(2V_m/\pi)\cos\alpha\) and \(V_m=180\,\mathrm{V}\). Armature current \(50\,\mathrm{A}\) continuous.
### Find
The required \(\alpha\) (motoring).
### Solution
Needed \(V_{dc}=E_a+I_a R_a=110+20=130\,\mathrm{V}\). \(V_{dc0}=2\times 180/\pi=114.6\,\mathrm{V}\) wait: \(2\times 180/\pi=114.6\) which is less than 130 V — that source cannot motor at 50 A. Recompute: \(2V_m/\pi=114.6\,\mathrm{V}<130\,\mathrm{V}\). The converter cannot reach 130 V. Maximum at \(\alpha=0\) is 114.6 V, which would give \(I_a=(114.6-110)/0.40=11.5\,\mathrm{A}\) only. Report that \(\alpha=0\) is already insufficient.
### Answer
Infeasible at 50 A; \(V_{dc,\max}=115\,\mathrm{V}\) gives only \(I_a=11.5\,\mathrm{A}\)
