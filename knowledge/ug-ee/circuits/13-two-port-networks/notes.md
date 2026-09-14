# z, y, h, ABCD parameters

A two-port network has a pair of terminals for input and a pair for output. Linear two-ports are summarized by 2×2 parameter matrices relating port voltages and currents. UG network theory lists z (open-circuit impedance), y (short-circuit admittance), h (hybrid, transistors), and ABCD (transmission, cascades). Reciprocity and symmetry cut the number of independent parameters. This is also the language of filters and transmission lines at UG depth.

## Concepts

Port condition: current into the plus of port 1 and into the plus of port 2 is the standard for z and y. For ABCD, I2 is often defined out of the network (toward the load), which inserts minus signs in conversions. Always state the current convention.

z-parameters: \( V_1 = z_{11} I_1 + z_{12} I_2 \), \( V_2 = z_{21} I_1 + z_{22} I_2 \). \( z_{11} \) is the input impedance with port 2 open. \( z_{21} \) is the open-circuit transfer impedance. Reciprocal networks: \( z_{12} = z_{21} \). Symmetric: \( z_{11} = z_{22} \) as well.

y-parameters: \( I_1 = y_{11} V_1 + y_{12} V_2 \), etc. \( y_{11} \) is the input admittance with port 2 shorted. Reciprocal: \( y_{12} = y_{21} \). Useful when short-circuit tests are easier (shunt elements).

h-parameters: \( V_1 = h_{11} I_1 + h_{12} V_2 \), \( I_2 = h_{21} I_1 + h_{22} V_2 \). \( h_{11} \) is short-circuit input impedance, \( h_{21} \) is short-circuit current gain (the transistor β in the CE hybrid-pi cousin). Reciprocal: \( h_{12} = -h_{21} \) only in a restricted sense; actually \( \det h = z \) relations differ. For reciprocal two-ports \( h_{12} = -h_{21} \) is not generally true; the reciprocity condition is \( h_{12} = -h_{21} \) wait: standard is \( h_{12} = -h_{21} \) for reciprocal? Let me recall: reciprocity is det(h) related... Actually for reciprocal networks, h12 = −h21. Yes that is the standard UG statement.

ABCD: \( V_1 = A V_2 + B (-I_2) \) with I2 out, or textbooks write \( V_1 = A V_2 + B I_2 \) with I2 into the load (out of the port). \( A = V_1/V_2 |_{I_2=0} \) open-circuit voltage ratio. Cascade: matrix multiply ABCD of stages. Reciprocal: \( AD - BC = 1 \).

Conversions exist among all four; do not memorize every entry, derive from simultaneous equations when needed. Series connection of two-ports adds z (if port currents still match). Parallel adds y. Cascade multiplies ABCD. Interconnecting without isolation can violate port conditions (a ground loop making the two ports not independent).

Terminated two-port: load ZL at port 2, then Zin = z11 − z12 z21/(z22+ZL), the same algebra as reflected impedance.

Elementary two-ports by inspection: a series impedance Zs in the top wire, bottom wires common, is z11=z22=z12=z21=∞ (open-circuit parameters blow up) because there is no shunt path; y-parameters exist: y11=y22=1/Zs, y12=y21=−1/Zs. A shunt impedance Zp across both ports in parallel is the dual: z11=z22=z12=z21=Zp, y blow up. A T of za, zb, zc (shunt) has finite z as in the equations section. A π of ya, yb, yc has finite y. Convert T to π with the same algebra as Y-Δ. These four pictures cover most UG ladders.

h-parameters and transistors: the CE hybrid model is hie, hre, hfe, hoe, which are h11, h12, h21, h22. hfe is β. Circuits courses introduce h so that electronics can use them. Reciprocity would require h12 = −h21, which a transistor does not satisfy (hre is tiny, hfe is 100). That is the point of dependent sources inside the two-port.

ABCD in power transmission: A and D are dimensionless, B is ohms, C is siemens. For a symmetric line A=D. For a series impedance only, A=1, B=Z, C=0, D=1. For a shunt admittance only, A=1, B=0, C=Y, D=1. A medium-length line π model is a cascade of those. The receiving-end voltage regulation uses V1 = A V2 + B I2 with I2 into the load. This pack does not do transmission-line hyperbolic functions; those live in power systems. The matrix multiply is the same.

Image impedance and iteration: older filter design matched Zimage so that cascading identical sections does not reflect. Modern UG may skip image parameters but still cascade ABCD. If two sections are connected, port conditions require that the output current of the first is the input current of the second and that the grounds are common. A balun or an isolation transformer is needed if the ports do not share a ground.

Finding parameters from measurements: apply a known I1, open port 2, measure V1 and V2 → z11, z21. Short port 2, measure I2 and V1 with a known I1 → related to y or h. Numerical example: 1 A into port 1, port 2 open, V1=16 V, V2=12 V as in the T of 4, 12, 6 Ω. That is already z11 and z21. Do not also short port 2 in the same sentence without a new experiment.

Determinant checks: det z = z11 z22 − z12² for reciprocal. If det z = 0 the two-port is degenerate (the ports are not independent, e.g. a direct through-connection of both plus terminals). Inversion to y fails. Physically there is still a network; you should use a different parameter set. Box the current convention (I2 in versus I2 out) on every ABCD numerical answer so a cascade multiply does not silently flip B and C.

## Equations

Open-circuit: \( z_{11} = V_1/I_1|_{I_2=0} \), \( z_{21} = V_2/I_1|_{I_2=0} \), etc.

Short-circuit: \( y_{11} = I_1/V_1|_{V_2=0} \).

Hybrid: \( h_{11} = V_1/I_1|_{V_2=0} \), \( h_{21} = I_2/I_1|_{V_2=0} \).

Transmission (I2 out): \( A = V_1/V_2|_{I_2=0} \), \( B = V_1/(-I_2)|_{V_2=0} \), \( C = I_1/V_2|_{I_2=0} \), \( D = I_1/(-I_2)|_{V_2=0} \).

Reciprocal: \( z_{12}=z_{21} \), \( y_{12}=y_{21} \), \( AD-BC=1 \).

Symmetric T: series za, zb and shunt zc give z11 = za+zc, z12 = zc, z22 = zb+zc.

## Methods

To measure z: open port 2, drive port 1, record V1, V2, I1. Repeat swapped. To measure y: short the unused port. Never leave a current source on an open if you meant a z-test with a voltage drive; follow the definition. For a ladder, nodal y-parameters are natural; for a series chain, ABCD.

When cascading, agree I2-out on every block. When a problem gives a T of three impedances, write z by inspection, then invert to y if asked (y = z^{-1}).

Check reciprocity if only resistors, L, C, M with bilateral coupling. Dependent sources generally break it. Check AD−BC=1 as an arithmetic test.

A conversion path that avoids memorizing sixteen formulas: from z, invert to y if det z ≠ 0. From z, h11 = det z / z22, h21 = −z21/z22, h12 = z12/z22, h22 = 1/z22 (with I2-into). From z, A = z11/z21, B = det z / z21, C = 1/z21, D = z22/z21 with the I2-out ABCD convention used in transmission (signs: textbooks differ; derive from V1 = z11 I1 + z12 I2 and I2 = −I_load). When in doubt, write the two port equations and eliminate. For a cascade of two T-networks, either multiply ABCD or merge the adjacent series arms and restamp z; both beat a wrong memorized identity. Terminate with ZL only at the end, after the matrix of the empty two-port is known.

## Mistakes

Mixing I2-in and I2-out in ABCD. Using z-parameters with port 2 shorted. Adding y-matrices of series-connected ports. Assuming all four h parameters are impedances. Forgetting units: z in ohms, y in siemens, h11 ohms, h21 dimensionless, h12 dimensionless, h22 siemens. Claiming a transistor hybrid-pi is reciprocal. Cascading in the wrong order (source nearest A of the first matrix). Using det z = 0 as a reciprocity test. Terminating with ZL but still quoting z11 as Zin. Using y12 without the minus that usually appears for a passive π (y12 is negative for a positive shunt). Cascading ABCD as BA instead of the source-to-load order. Measuring z21 with port 2 shorted. Assuming h12 = 1/h21. Mixing two-port current into port 2 with load current out of port 2 in the same equation without a minus. Treating a three-terminal network with a common ground as if the ports were isolated when they share a finite ground impedance (the port condition fails). Reporting ABCD A = 2 when the measurement was a loaded voltage ratio, not the open-circuit A. For a reciprocal T of resistors, z12 must equal z21 and both must equal the shunt arm; if they do not, the inspection was of the wrong arm. When converting, keep units: B in ohms times I2 in amperes is volts, matching V1. If a cascade result has AD−BC far from 1 on a reciprocal pair, the multiply used mixed I2 conventions. Re-derive A from V1/V2 open before trusting a memorized table. Open means I2 = 0, never a short. Shorted tests belong to B, y, and h21, not to A. Keep that sentence on the exam sheet as a reminder.
