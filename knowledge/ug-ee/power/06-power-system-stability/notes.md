# Power-system stability: swing equation and equal-area criterion

Stability asks whether synchronous machines remain in synchronism after a disturbance. Undergraduate power courses treat the classical one-machine-infinite-bus (OMIB) model: a constant internal voltage behind \(X_d'\) or \(X\), a mechanical power that is constant during the short interval of interest, and the swing equation. The equal-area criterion (EAC) converts that second-order nonlinear ODE into a statement about areas on the \(P\)–\(\delta\) diagram without solving the differential equation. Multi-machine eigenvalues, PSS design, and detailed excitation models are later courses. Voltage stability (QV, unit 12) is a different mechanism and must not be mixed into EAC.

## Concepts

A synchronous machine connected through a reactance to an infinite bus produces electrical power \(P_e=P_{\max}\sin\delta\) in the lossless classical model, with \(\delta\) the angle of the internal voltage relative to the infinite bus and \(P_{\max}=E V/X\). Mechanical power \(P_m\) from the turbine is nearly constant on a 0.1–1 s fault time scale (governor valves have not moved much). If \(P_m=P_e\), \(\delta\) is constant: equilibrium. If a fault drops \(P_e\) (electrically the generator cannot export), \(P_m>P_e\) and the rotor accelerates, \(\delta\) increases. After the fault is cleared, \(P_e\) jumps back toward a postfault \(P_{\max}^{\mathrm{post}}\sin\delta\) (often smaller than prefault if a line is out). The rotor is then typically above the new equilibrium angle and decelerates if \(P_e>P_m\). Whether it stops before the unstable saddle angle is the stability question.

The swing equation in SI form (one machine) is

\[
J\omega_m\frac{d\omega_m}{dt}=T_m-T_e,
\]

more often written with inertia constant \(H\) in MW·s/MVA (or MJ/MVA):

\[
\frac{2H}{\omega_s}\frac{d^2\delta}{dt^2}=P_m-P_e
\]

when \(P\) is in pu on the machine base, \(\delta\) in electrical radians, \(\omega_s=2\pi f\) in electrical rad/s. Some texts write \(M=2H/\omega_s\) as the inertia coefficient. \(H\) is typically 2–10 s for large machines: it is the stored kinetic energy at rated speed divided by rated VA. A larger \(H\) means slower swings, more time for relays and more kinetic buffer.

Electrical radians versus mechanical: \(\delta_{\mathrm{elec}}=(p/2)\delta_{\mathrm{mech}}\) for \(p\) poles. UG problems usually give \(\delta\) as electrical and \(H\) already in electrical form. Frequency: rotor speed \(\omega=d\delta/dt+\omega_s\). During a swing, frequency at the machine is not exactly 50/60 Hz; COI frequency of a multi-machine island is the inertia-weighted mean.

Classifications (UG language):

- Steady-state stability: small slow changes; the criterion \(dP_e/d\delta>0\) at the operating point, i.e. \(\delta<90^\circ\) on the simple sinusoid. The theoretical maximum \(P_{\max}\) is the pull-out power. Steady-state limit is reduced by resistance, saliency, and excitation limits; the simple \(90^\circ\) is a start.
- Transient stability: large disturbances (faults, line switching) on a 0.1–few-second scale. EAC and time-domain swing simulation.
- Dynamic/small-signal: hunting, damping, PSS — mentioned, not designed here.

Equal-area: plot \(P_e(\delta)\) prefault, during fault, and postfault. Accelerating area \(A_1=\int (P_m-P_e^{\mathrm{fault}})d\delta\) from the prefault \(\delta_0\) to the clearing angle \(\delta_c\). Decelerating area \(A_2=\int (P_e^{\mathrm{post}}-P_m)d\delta\) from \(\delta_c\) to the maximum angle \(\delta_m\). Critical is when \(A_2\) available up to the unstable equilibrium \(\delta_u=\pi-\delta_{\mathrm{post}}\) equals \(A_1\). If the needed \(A_2\) exceeds that area, the machine loses synchronism. Critical clearing angle \(\delta_{\mathrm{cr}}\) is the \(\delta_c\) that makes \(A_1=A_{2,\mathrm{max}}\). Critical clearing time needs the swing ODE or an approximate \(\delta(t)=\delta_0+(\omega_s P_m t^2)/(4H)\) if \(P_e^{\mathrm{fault}}=0\) (bolted fault at the terminals, no electrical output).

Three-phase fault at the generator terminals: \(P_e=0\) during the fault, maximum acceleration. A remote fault leaves some \(P_e=P_{\max,f}\sin\delta\). Unbalanced faults have sequence-network \(P_e\) that is not zero; UG EAC problems almost always use a three-phase fault with a specified during-fault \(P_{\max}\) or zero.

Damping: \(P_e\) plus a \(K_d\omega\) term. EAC ignores damping (conservative if damping is positive). Resistance in the network adds a little damping and a cosine term in \(P_e(\delta)\).

Infinite bus is a voltage that never moves. A true second machine has a relative swing \(\delta_1-\delta_2\) and a reduced inertia \(H_{\mathrm{eq}}=H_1 H_2/(H_1+H_2)\) on a common base for a two-machine equivalent. UG may give that equivalent.

Multi-machine: \(n\) swing equations, \(n-1\) relative angles. Stability of a case is decided by numerical integration in production studies (PSSE, PowerFactory). This unit’s hand method is OMIB/EAC.

Voltage during the fault affects \(P_{\max}=EV/X\). A deep voltage dip kills \(P_e\). Fast excitation can raise \(E\) after clearing (beneficial, not in classical constant-\(E\)). Impedance-based \(X\) increases if a line trips, lowering postfault \(P_{\max}\) and shrinking the decelerating area — that is why some faults that clear still lose stability if the postfault network is too weak.

Autoreclosing: a temporary fault, reclose, restore prefault \(P_{\max}\). EAC can include a second switching. Out of UG core unless asked.

Frequency stability (load-generation mismatch in an island) is not EAC. It is a different unit of power-system dynamics: \(2H f_0^{-1} df/dt = P_m-P_L\). Do not apply equal-area to frequency collapse.

Critical clearing time from the \(\delta=\delta_0+\frac12 \alpha t^2\) law is valid only while \(P_e\) is constant (including zero) and \(\omega\) starts at \(\omega_s\). After clearing, that parabola does not continue; the rotor is on a different \(P_e(\delta)\) curve and EAC takes over without needing \(t(\delta)\) on the decelerating side if you only want a stable/unstable verdict. If you need the actual maximum angle versus time, integrate the swing equation (Euler, RK4). One Euler step of size 0.01 s on a 0.2 s fault is a legitimate UG numerical: \(\omega_{k+1}=\omega_k+(\omega_s/2H)(P_m-P_e)h\), \(\delta_{k+1}=\delta_k+\omega_k^{\mathrm{dev}} h\) with consistent electrical rad/s.

Classical model assumptions, listed so they can be relaxed later: constant mechanical power, constant internal voltage behind a constant \(X\), neglect of damper windings (no \(K_d\)), neglect of AVR, single machine or OMIB reduction, first-swing only. A case that is first-swing stable can still lose synchronism on the second swing if damping is negative (excitation-induced). A case that is first-swing unstable is not saved by a PSS. Relays that trip on apparent impedance during a stable swing (zone-3) are a protection/stability interface: power-swing blocking is the keyword.

Transfer reactance \(X\) in \(P_{\max}=EV/X\) is the reduced reactance from internal node to infinite bus. Prefault, two parallel lines \(X_a\parallel X_b\) plus \(X_d'\) of the machine. During a mid-line three-phase fault, a star-delta reduction often leaves a small but nonzero \(P_{\max,f}\). Postfault, one line may be out, so \(X\) is larger. Compute three numbers, \(P_{\max}^{\mathrm{pre}},P_{\max}^{f},P_{\max}^{\mathrm{post}}\), before touching areas. Skipping the during-fault \(P_{\max}\) and writing \(P_e=0\) is correct only if the fault is at the generator bus or the reduction truly gives infinite transfer reactance.

Inertia on a common base: \(H_{\mathrm{sys}}=\sum H_i S_i / S_{\mathrm{base}}\). A 500 MVA, \(H=4\ \mathrm{s}\) machine on a 100 MVA study base has \(H=20\ \mathrm{s}\). Using 4 s in the swing equation on 100 MVA pu power is an under-inertia error by 5.

Equal-area is necessary and sufficient for first-swing of the classical OMIB without damping. With damping, it is slightly conservative. For two machines, reduce to relative \(\delta\) and \(H_{\mathrm{eq}}\) first; do not write two EAC plots. If \(P_m>P_{\max}^{\mathrm{post}}\), no postfault equilibrium exists and the case is unstable for every clearing time — fast valving or tripping a unit would have to change \(P_m\), which is outside the classical constant-\(P_m\) model. Report that clearly rather than forcing a \(\delta_{\mathrm{cr}}\). Governor action on a several-second scale can still change \(P_m\) after the first swing, which is why EAC is a first-swing tool, not a five-second verdict.

## Equations

Swing (pu on machine base, \(\delta\) elec rad, \(P\) pu):

\[
\frac{2H}{\omega_s}\frac{d^2\delta}{dt^2}=P_m-P_{\max}\sin\delta.
\]

Power-angle:

\[
P_e=\frac{EV}{X}\sin\delta=P_{\max}\sin\delta.
\]

Prefault equilibrium: \(P_m=P_{\max}^{\mathrm{pre}}\sin\delta_0\), \(\delta_0=\arcsin(P_m/P_{\max}^{\mathrm{pre}})\).

Unstable postfault equilibrium: \(\delta_u=\pi-\arcsin(P_m/P_{\max}^{\mathrm{post}})\).

EAC critical clearing (fault with \(P_e=0\), postfault \(P_{\max}\)):

\[
\int_{\delta_0}^{\delta_{\mathrm{cr}}} P_m\,d\delta=\int_{\delta_{\mathrm{cr}}}^{\delta_u}(P_{\max}\sin\delta-P_m)\,d\delta.
\]

Closed form often:

\[
\cos\delta_{\mathrm{cr}}=\frac{P_m(\delta_u-\delta_0)+P_{\max}\cos\delta_u}{P_{\max}}\quad\text{(check derivation for \(P_e=0\) during fault)}.
\]

Derive from first principles in the exam rather than memorizing the cosine formula with the wrong sign.

If \(P_e=0\) during fault, approximate clearing time from rest at \(\delta_0\):

\[
\delta_c=\delta_0+\frac{\omega_s P_m}{4H}t_c^2 \quad (\delta\text{ in rad, }P_m\text{ pu}).
\]

## Methods

1. Convert to pu, find \(P_{\max}\) pre, during, post from \(E,V,X\) of each network configuration.
2. Find \(\delta_0\) from \(P_m=P_{\max}^{\mathrm{pre}}\sin\delta_0\). Find \(\delta_u\) from \(P_m=P_{\max}^{\mathrm{post}}\sin\delta_u\) in \((\pi/2,\pi)\).
3. Sketch \(P(\delta)\). Shade \(A_1,A_2\).
4. For a given \(t_c\), get \(\delta_c\) from the swing approximation or from a stated \(\delta_c\), then compare \(A_1\) to available \(A_2\) up to \(\delta_u\).
5. For \(\delta_{\mathrm{cr}}\), set \(A_1=A_{2,\mathrm{max}}\) and solve for \(\delta_{\mathrm{cr}}\).

Checks: \(\delta_0<90^\circ\); \(\delta_u>90^\circ\); \(P_m<P_{\max}^{\mathrm{post}}\) or there is no postfault equilibrium and the case is first-swing unstable for any clearing (unless \(P_m\) is reduced by fast valving, not classical). Areas in pu·radian.

Worked caution: convert degrees to radians inside integrals \(\int P\,d\delta\) because \(\delta\) in the swing equation is radians. Mixing \(H\) in MJ/MVA with \(P\) in MW without using pu is a factor-of-rating error.

## Mistakes

Using \(P=EV/X\) without \(\sin\delta\). Taking \(\delta_u=90^\circ\) always. Integrating in degrees while using \(H\) formulas that assume radians (a \(180/\pi\) disaster). Using \(H\) of one machine on a system MVA base without converting \(H_{\mathrm{new}}=H_{\mathrm{old}}S_{\mathrm{old}}/S_{\mathrm{new}}\). Applying EAC to voltage collapse. Assuming a fault at a remote bus has \(P_e=0\). Forgetting that clearing a line raises \(X\) and lowers \(P_{\max}^{\mathrm{post}}\). Using mechanical degrees with electrical \(P_{\max}\). Setting \(P_m=0\) during the fault. Comparing areas visually on a sketch whose \(P_{\max}\) curves were not to scale. Using \(f=50\ \mathrm{Hz}\) in \(\omega_s\) when the problem is 60 Hz. Writing \(\delta(t)=\frac12 at^2\) with \(a\) in deg/s² but \(t\) then converted inconsistently. Claiming damping always destabilizes (usually it helps first-swing a little).
