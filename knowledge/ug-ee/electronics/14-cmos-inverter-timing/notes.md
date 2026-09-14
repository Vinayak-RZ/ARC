# CMOS inverter: transfer curve, delay, and power

The CMOS inverter is the atom of digital VLSI and the last unit of this pack. Two complementary MOSFETs, one p, one n, share a gate (input) and a drain (output). The DC transfer curve, noise margins, RC delay, and \(CV^2f\) power are the UG core; they also explain why we do not draw TTL-style resistors in modern logic.

## Concepts

Circuit: pMOS source at \(V_{DD}\), nMOS source at ground, gates tied to \(v_{in}\), drains tied to \(v_{out}\). When \(v_{in}=0\), nMOS is off, pMOS is on (deep triode), output pulled to \(V_{DD}\) through \(r_{on,p}\). When \(v_{in}=V_{DD}\), pMOS off, nMOS on, output at 0. At no DC input except leakage do both devices sit in saturation conducting a large current — that is the mid-swing region, used in analog (push-pull amp) and avoided in digital because it dissipates.

Voltage-transfer characteristic (VTC). For \(v_{in}\) from 0 to \(V_{DD}\), five regions: (1) n off, p triode, \(v_{out}=V_{DD}\); (2) n sat, p triode; (3) both sat (steep inverter gain); (4) n triode, p sat; (5) n triode, p off, \(v_{out}=0\). The switching threshold \(V_M\) is where \(v_{out}=v_{in}\), usually designed near \(V_{DD}/2\) by ratioing \(\mu_n W_n\) against \(\mu_p W_p\). Because \(\mu_n\approx 2\mu_p\), a symmetric inverter uses \(W_p\approx 2 W_n\) for equal rise/fall and \(V_M\approx V_{DD}/2\).

Noise margins. \(V_{IL}\): point on the VTC where \(dv_{out}/dv_{in}=-1\) on the left. \(V_{IH}\): the right unity-gain point. \(V_{OL}=0\), \(V_{OH}=V_{DD}\) for static CMOS (ideal, ignoring leakage). \(NM_L=V_{IL}-V_{OL}\), \(NM_H=V_{OH}-V_{IH}\). A restoration argument: a valid \(0\) or \(1\) into a chain of inverters is pulled *closer* to the rail; that is why digital signalling is robust.

Delay. The load is capacitance: next-gate \(C_g\), drain diffusion \(C_{db}\), interconnect \(C_w\). A first-order model treats the on transistor as a resistor \(R_{eq}\) charging or discharging \(C_L\). \(t_{PHL}\approx 0.69 R_{eqn} C_L\), \(t_{PLH}\approx 0.69 R_{eqp} C_L\). Propagation delay \(t_p=(t_{PHL}+t_{PLH})/2\). The 0.69 is \(\ln 2\) for a 50 % RC step. \(R_{eq}\) is not \(r_{DS,on}\) at \(V_{GS}=V_{DD},V_{DS}=0\); it is an average over the swing, often taken as \(V_{DD}/I_{Dsat}\) times a fitting factor (\(\approx 1\) to \(4/3\) depending on the book). Logical effort (Harris/Sutherland) abstracts this: an inverter has logical effort 1, a 3-input NAND has a worse pull-down stack, so it is slower at the same \(C_{in}\). UG: stacked nMOS in NAND increase \(t_{PHL}\); compensate by widening the n-devices.

Fan-out: \(FO=C_{load}/C_{in}\). Delay grows with FO. A chain of inverters (buffer) driving a huge pad capacitance is sized with a taper, often near \(e\approx 2.7\) per stage in the logical-effort optimum (or 4 in some textbook rules). Driving 20 pF with a minimum inverter is a mistake; driving it with a 20-stage random chain is also a mistake.

Power. Dynamic: each full cycle of a node dumps \(C V_{DD}^2\) (charge \(C V_{DD}\) from the supply, then dump it to ground). \(P_{\mathrm{dyn}}=\alpha f C_L V_{DD}^2\) with activity factor \(\alpha\) (1 for a clock, \(\sim 0.1\) for typical data). Short-circuit (crowbar) power: during the input edge both devices conduct briefly; it grows if the input edge is slow. Static: subthreshold leakage \(I_{off}V_{DD}\), gate tunnelling, junction leakage. At 5 V HC CMOS, static is negligible at UG accuracy. At 1 V nanometer CMOS, leakage can rival dynamic — mention only.

Scaling. Constant-field scaling (Dennard): voltages and sizes shrink, delay shrinks, power density stays put — until leakage and interconnect say otherwise. For this unit: delay \(\propto C V/I\), \(C\propto L\), \(I\propto W/L\times V^2\) in square law so \(t_p\) improves as devices shrink and as \(V_{DD}\) *drops* only if you also accept the \(I\propto V^2\) (or \(V^{1.2}\) in short channel) loss. Low-power design lowers \(V_{DD}\) and pays in delay.

Ratioed vs ratioless. Static CMOS is ratioless in the sense that the output still reaches the rails for any finite \(W_p/W_n>0\); the ratio only sets \(V_M\) and delay balance. NMOS logic with a depletion load (historical) was ratioed: \(V_{OL}\) depended on the load/driver ratio and dissipated static power. That is why CMOS won.

Body effect in stacks: the upper nMOS in a NAND has \(V_{SB}\ne 0\) if the intermediate node is not at 0, raising \(V_t\) and slowing the pull-down. Transmission gates (n+p in parallel) pass a full rail without the \(V_t\) drop of a single pass transistor (unit 03).

Layout (qualitative): p-well / n-well, guard rings, minimum width, contacts, and the inverter as a standard cell with \(V_{DD}\) at the top rail and GND at the bottom. Latch-up: parasitic thyristor of the CMOS wells; prevent with tap spacing. ESD on pads.

Miller capacitance on a CMOS inverter is small-signal analog thinking applied at the mid-point. Digitally, \(C_{gd}\) is charged through a large voltage swing (Miller multiplied during the transition) and is already included in the extracted \(C_L\) if you used a datasheet \(C_{pd}\) (power dissipation capacitance) or a process \(C_{in},C_{out}\). UG: adding \(C_{gd}\) by hand and also using a lump \(C_L\) double-counts.

I/O standards (LVCMOS 3.3, 1.8, 1.2) are just \(V_{DD}\) and threshold contracts on the same inverter. Level shifters are two inverters on two rails, or a current-mirror translator. That sentence links this unit to unit 12.

## Equations

Square-law saturation current (nMOS):

\[
I_{Dn}=\frac12 k_n' \frac{W_n}{L}(V_{DD}-V_{tn})^2
\]

at \(v_{GS}=V_{DD}\), used to estimate \(R_{eqn}\approx V_{DD}/I_{Dn}\) (order of magnitude).

Switching threshold (both sat, \(\lambda=0\)):

\[
V_M=\frac{V_{tn}+\sqrt{(k_p/k_n)}\,(V_{DD}+V_{tp})}{1+\sqrt{k_p/k_n}}
\]

with \(V_{tp}<0\), \(k=\mu C_{ox} W/L\). If \(k_n=k_p\) and \(V_{tn}=-V_{tp}\), \(V_M=V_{DD}/2\).

Noise margins (definitions):

\[
NM_L=V_{IL}-V_{OL},\qquad NM_H=V_{OH}-V_{IH}.
\]

RC delay:

\[
t_{PHL}\approx 0.69 R_{eqn} C_L,\qquad t_p=\frac{t_{PHL}+t_{PLH}}{2}.
\]

Dynamic power:

\[
P_{\mathrm{dyn}}=\alpha C_L V_{DD}^2 f.
\]

Energy per (full) transition of a node: \(E=C_L V_{DD}^2\) per cycle (two transitions: charge and discharge), or \(\frac12 C V^2\) per single edge stored on \(C\); be consistent with the question's wording.

## Methods

1. DC region: compare \(v_{in}\) with \(V_{tn}\) and \(V_{DD}+V_{tp}\), then compare \(v_{out}\) with \(v_{in}-V_{tn}\) and \(v_{in}-V_{tp}\) to name triode vs sat for each device.
2. \(V_M\): set \(I_{Dn}=|I_{Dp}|\) with both saturated and \(v_{out}=v_{in}=V_M\). Solve. If the problem gives matched \(k\) and thresholds, skip to \(V_{DD}/2\).
3. Delay: compute \(C_L\), estimate \(R_{eq}\) from the on device, use 0.69 RC. Rise uses pMOS, fall uses nMOS. Stacked devices: add resistances (or use a 2× width rule).
4. Power: only capacitors that *toggle* contribute to \(\alpha C f V^2\). A node stuck at 1 still leaks, but UG dynamic-power questions usually want \(C_{load} V^2 f\) with a stated \(\alpha\).
5. Sizing for equal rise/fall: \(W_p/W_n\approx \mu_n/\mu_p\).

## Mistakes

- Drawing a collector resistor on a CMOS inverter. There is no \(R_C\); the other MOSFET *is* the load.
- Static current at \(v_{in}=0\) or \(V_{DD}\) treated as \(V_{DD}/(r_{on,n}+r_{on,p})\). One device is *off*.
- \(V_{OL}\) of CMOS taken as 0.2 V from TTL memory. Static CMOS \(V_{OL}\) is 0 V at DC.
- Using \(t=RC\) instead of \(0.69 RC\) for 50 % delay, or using 0.69 when the question defines delay as 10–90 % (that is 2.2 RC).
- Forgetting that \(t_{PLH}\) is set by the pMOS. Widening only the nMOS makes the falling edge fast and the rising edge unchanged.
- Power \(P=V I_{Dsat}\) as if the inverter sat in the mid-point. Digital power is \(CV^2f\) plus leakage.
- Activity: a 100 MHz clocked register whose Q never changes still burns clock-node power, but not \(C_Q V^2 f\) if Q is static. Name which capacitance toggles.
- Pass-nMOS outputting \(V_{DD}-V_t\) and calling it a CMOS inverter output. Different circuit.
- Latch-up ignored when a pin is driven below ground. Lab boards die that way.

Elmore delay (mention, do not derive at length): a ladder of RC segments approximating a long wire has delay \(\sum R_i C_{\mathrm{downstream},i}\). Interconnect delay dominates gate delay in nanometer CMOS; at UG 5 V HC, gates still dominate on a breadboard, and wires dominate on a sloppy long jumper at a few tens of megahertz. Transmission-line ringing on unterminated CMOS outputs is a lab surprise at those speeds (unit 12's edge-rate).

Ring oscillator: an odd number of inverters in a loop, period \(2 N t_p\). Used as a process monitor and as a crude VCO. Barkhausen is not the right tool; the delay model is. Five inverters at \(t_p=1\,\mathrm{ns}\) oscillate at 100 MHz.

Energy vs power. A node flipped once costs \(\frac12 C V^2\) from the supply to store, and another \(\frac12 C V^2\) dumped to ground on the fall, total \(C V^2\) from the supply per cycle. Low-power tricks: lower \(V_{DD}\) (quadratic in energy, linear-to-worse in delay), clock gating (\(\alpha\to 0\) on idle blocks), and not using huge \(C_L\). Sleep transistors cut leakage in advanced CMOS; skip at this depth.

The CMOS inverter is a pair of switches, an RC delay, and a capacitor that costs \(CV^2\) every time you flip it. Size the pMOS, count the load, and stay off the mid-point. If the output does not reach the rails, you are looking at a ratioed circuit, a pass transistor, or a damaged part — not a static CMOS inverter at DC. Ratioed NMOS with a depletion load is the historical counterexample: \(V_{OL}\) sat at a few tenths of a volt and the high level burned static current. CMOS ended that bargain.
