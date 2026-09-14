# Starting, cascade, V/f intro

A cage induction motor started at full voltage draws 5–8 times rated current and produces a starting torque that may or may not start the load. Supply authorities and shaft mechanics both care. This unit is reduced-voltage starting, wound-rotor resistance starting, cascade (concatenation) of two slip-ring machines, and the undergraduate introduction to constant V/f inverter control. The equivalent circuit and torque-slip curve of the previous unit are assumed.

The design tension is simple: starting torque must exceed load torque at every speed through the run-up, while line current stays inside a specified multiple of rated. High rotor resistance helps torque at \(s=1\) but hurts running efficiency. Deep-bar and double-cage rotors, already mentioned, are the cage designer’s compromise. The user-side compromise is a starter.

## Concepts

Direct-on-line (DOL) starting applies rated voltage. Current is the blocked-rotor current, typically 5–8 pu. Torque is \(T_\mathrm{st}\), often 1.5–2.5 pu on a Class B motor. DOL is fine on a stiff bus for small motors (local practice: tens of kW). Soft mechanical couplings still see a torque step.

Star-delta starting: a motor whose windings are rated delta at line voltage is first connected in star, so phase voltage is \(1/\sqrt{3}\) of rated, then switched to delta. Line current and starting torque both fall to 1/3 of DOL values (torque goes as \(V^2\); current per phase goes as \(V\), and line current in star is also the phase current, which works out to 1/3 of DOL line current). Only for motors with six terminals and a delta-rated winding. The open transition can produce a current spike.

Autotransformer starting: taps at fraction \(x\) of voltage (e.g. 60%, 80%). During start, motor voltage is \(x V\), motor current is \(x I_\mathrm{DOL}\), line current is \(x^2 I_\mathrm{DOL}\) because the autotransformer current ratio is \(x\) (neglecting magnetizing). Torque is \(x^2 T_\mathrm{DOL}\). Better than star-delta because \(x\) is choosable and line current is even smaller than motor current. Korndorfer connection reduces open-circuit transients.

Primary-resistance (or reactor) starting inserts impedance in the stator lines. Voltage at the motor is reduced by the divider of starter impedance and motor blocked impedance. Torque and current reductions are not as favorable as an autotransformer for the same line current. Cheap.

Wound-rotor (slip-ring) starting inserts three-phase resistance in the rotor. \(T_\mathrm{st}\) can be near \(T_\mathrm{max}\) while line current is moderated. As the motor accelerates, resistance is cut out in steps so that current and torque stay in a band, analogous to a DC starter. At run, rings shorted, low \(R_2\), good efficiency. Liquid starters and electronic rotor choppers exist. Rotor-resistance also gives speed control below \(n_s\) at the cost of slip power \(s P_g\) in the resistors. That waste is why Kramer and Scherbius recovered slip power historically; today a rotor-side converter (DFIG) does it on wind turbines — beyond this unit except as a pointer.

Cascade (concatenation): two slip-ring motors, the first’s rotor supplying the second’s stator (after a frequency/voltage match), shafts coupled. Effective poles add, synchronous speed \(120 f/(P_1+P_2)\) in cumulative cascade. Used historically for low-speed drives (mills). Differential cascade subtracts poles. Inefficient and bulky next to a gearbox or an inverter; still in some syllabi.

V/f (scalar) control: Faraday \(E\approx 4.44 f N k_w \Phi\). To keep \(\Phi\) rated from zero speed to base speed, \(V/f\) is held constant (with a voltage boost at low \(f\) to cover stator \(IR\), so \(E/f\) is constant). Torque capability stays near rated (constant torque region) because \(T\propto \Phi I_2\) and \(I_2\) is still current-limited. Above base frequency, voltage is clamped at rated; flux falls as \(1/f\), torque capability falls, power is roughly constant (field-weakening analogue). Slip in Hz, not in per-unit, is roughly constant for a given torque in the constant-flux region, so mechanical speed follows \(n\approx 120(f-f_\mathrm{slip})/P\).

An inverter (VSI, PWM) synthesizes variable \(f\) and \(V\). Harmonics add heating; PWM and filters mitigate. This unit does not design the inverter (power-electronics pack). The machines point is: the equivalent circuit’s frequencies all scale; reactances scale with \(f\); resistances do not; that is why boost is needed at low speed and why breakdown torque in pu changes with frequency if \(V/f\) is imperfect.

Soft starters (thyristor AC voltage controllers) ramp voltage at fixed \(f\). They reduce torque as \(V^2\) and are for pump/fan starts, not for holding full torque at low speed. V/f inverters can hold torque at low speed (with boost and current limit). Do not confuse them.

Plugging a three-phase motor (reverse two lines) puts \(s\approx 2\), large torque and huge rotor heat. Mechanical brakes or DC injection (stator fed with DC, rotor dissipates kinetic energy) are milder stopping methods.

Crawling (7th harmonic torque dip near \(1/7\) speed) and cogging (alignment at slot frequency, zero average start) are winding-design pathologies. Skewed rotors and pitch selection (next synchronous-winding ideas) reduce them.

## Equations

DOL: \(I_\mathrm{st}=I_\mathrm{br}\), \(T_\mathrm{st}=T(s=1)\) at rated \(V\).

Star-delta:

\[
I_{\mathrm{st,line}}=\frac{1}{3} I_{\mathrm{DOL,line}},\qquad T_\mathrm{st}=\frac{1}{3} T_\mathrm{DOL}.
\]

Autotransformer tap \(x\):

\[
I_\mathrm{motor}=x I_\mathrm{DOL},\qquad I_\mathrm{line}=x^2 I_\mathrm{DOL},\qquad T_\mathrm{st}=x^2 T_\mathrm{DOL}.
\]

Primary resistance: voltage divider, then \(T\propto V_m^2\).

Wound rotor, extra \(R_\mathrm{ext}'\): use torque formula with \(R_2'+R_\mathrm{ext}'\). Slip power in external resistors \(3 I_2'^2 R_\mathrm{ext}'\).

Cascade, cumulative, same \(f\):

\[
n_{s,\mathrm{cas}}=\frac{120 f}{P_1+P_2}.
\]

V/f, base frequency \(f_b\), rated voltage \(V_r\):

\[
V(f)\approx V_r \frac{f}{f_b}\quad (f\le f_b),\qquad V(f)=V_r\quad (f>f_b),
\]

plus boost: \(V(f)\approx I R_1 + (V_r-I R_1)f/f_b\) at a chosen current (often rated).

Approximate torque in constant-flux region: same \(T(s)\) shape versus slip in Hz.

## Methods

Starting-current limit from the utility: pick a method whose \(I_\mathrm{line}/I_\mathrm{rated}\) is under the cap, then check \(T_\mathrm{st}>T_\mathrm{load}(0)\) with margin for friction. For a fan, \(T_\mathrm{load}\propto n^2\), so reduced \(T_\mathrm{st}\) may still start; for a constant-torque conveyor it may not. Star-delta’s 1/3 torque fails many constant-torque loads.

Autotransformer: choose \(x=\sqrt{T_\mathrm{need}/T_\mathrm{DOL}}\) then verify line current \(x^2 I_\mathrm{DOL}\).

Wound-rotor step starter: same \(\gamma\)-ratio method as DC starters, using the rotor circuit resistance referred to slip rings (actual rotor ohms, not necessarily stator-referred). First step for \(T_\mathrm{st}\approx T_\mathrm{max}\): \(R_2+R_\mathrm{ext}\approx \sqrt{R_\mathrm{Th}^2+(X_\mathrm{Th}+X_2)^2}\) from the Thevenin formula.

V/f numerical: for a new frequency \(f\), set \(V=V_r f/f_b\) (or with boost). Scale all \(X\) by \(f/f_b\). Leave \(R\) unscaled. Compute torque at the slip that corresponds to the desired mechanical speed: \(s=(n_s(f)-n)/n_s(f)\). Do not keep the old 50 Hz slip of 0.04 at 25 Hz; that would be a different operating point.

Cascade: draw power flow. First machine as a motor at slip \(s_1\), rotor electrical power \(s_1 P_{g1}\) feeds the second stator. Second machine sees frequency \(s_1 f\). Coupled speed is common. The textbook result \(n=120 f/(P_1+P_2)\) is the no-load (small slip) cascade speed.

When comparing starters, make a table: \(I_\mathrm{line}\), \(T_\mathrm{st}\), smoothness, cost, terminals required. Do not claim star-delta reduces current to \(1/\sqrt{3}\); that is a frequent error.

## Mistakes

Saying star-delta starting current is \(1/\sqrt{3}\) of DOL. Line current is 1/3.

Using autotransformer \(I_\mathrm{line}=x I_\mathrm{DOL}\) instead of \(x^2 I_\mathrm{DOL}\).

Applying star-delta to a motor that is already wye-rated at line voltage with only three terminals.

Expecting a soft starter to provide rated torque at 5 Hz. Voltage-only control at fixed \(f\) cannot. Use V/f.

Holding \(s=0.04\) while changing \(f\) and calling it the same mechanical speed.

Omitting IR boost at low V/f, then wondering why torque collapsed at 5 Hz: all of \(V\) was dropped on \(R_1\), none left for \(E\) and flux.

Cascade with \(P_1=P_2=4\) poles claiming 1500 r/min. Cumulative cascade at 50 Hz is \(120\times 50/8=750\) r/min.

Cutting out rotor resistance too fast, exceeding current, or too slow, cooking the resistors.

Plugging without checking rotor energy \(s P_g\) with \(s\approx 2\).

Using DOL current as 1 pu. Blocked-rotor current is many pu; 1 pu is rated running current.

Treating V/f as vector control. Scalar V/f does not regulate rotor flux dynamically; it sets the steady-state \(E/f\). Field-oriented control is a later course.

Ignoring that reduced-voltage starting of a motor with a high-inertia load may stall in the saddle of a Class C/D curve or a harmonic dip (crawling) if torque never exceeds load plus acceleration.

A run-up energy check belongs next to the current-limit check. Rotor heat during a start is approximately the kinetic energy stored in the inertia if the load torque is small and DOL is used: \(\int P_\mathrm{cu2}\,\mathrm{d}t \approx \tfrac12 J\omega_s^2\) for a start from rest to near \(n_s\) on a free shaft. That identity is why frequent starting cooks a rotor even when steady running looks cool. Reduced-voltage starting lengthens the time but reduces torque and acceleration; the integral of rotor heat can still be on the order of the kinetic energy plus the work against load torque. Wound-rotor starting dumps much of that heat into external resistors, which is the point of the slip rings. Do not size those resistors on steady \(I^2 R\) at \(s=1\) forever; they are short-time rated unless the drive is a slip-power speed controller.

V/f boost is not an optional flourish. Write \(V = I_1 R_1 + E_1\) with \(E_1 \propto f\Phi\). At 5 Hz, \(R_1\) can eat most of a naive \(V=V_r f/f_b\). A boost that holds \(E_1/f\) (or \(V-I R\) over \(f\)) at a chosen current restores torque. Too much boost saturates the core at low speed (Faraday: \(\Phi \propto E/f\), and if you set \(V/f\) high while \(E\approx V\), \(B\) exceeds the knee). Current-limit in the inverter then fights the boost. Commissioning is a compromise: enough boost to lift a load at 2 Hz, not so much that no-load current looks like a fault.

Cascade is easiest to remember as pole addition. A 4-pole motor cascaded with a 4-pole motor is an 8-pole machine at 50 Hz (750 r/min), not a 4-pole machine with a mysterious extra slip. Power through the first rotor feeds the second stator; the second shaft (or the common shaft) produces the extra mechanical power. If the machines are not coupled mechanically, you do not have cascade, you have a variable-frequency supply for the second motor (a rotary frequency converter), which is a different syllabus item.
