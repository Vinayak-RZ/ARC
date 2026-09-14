# Sensors, actuators, digital/analog I/O, and interlocks (study-level)

A PLC only sees voltages and currents. This unit is how UG EEE maps those electrical points to switches, 4–20 mA loops, contactors, and *study-level* interlocks. It is not a SIL certification, not a vendor I/O catalogue, and not live plant actuation (out of product).

## Concepts

**Discrete sensors** close or open a circuit. A **limit switch** is a mechanical NO or NC contact on a guard or end-of-travel. A **proximity** sensor (inductive for metal, capacitive for many dielectrics, ultrasonic for distance) is usually a three-wire DC device: +24 V, 0 V, and an output that is either **PNP (sourcing)** or **NPN (sinking)**. Sourcing output pulls the PLC input *up* to 24 V when true; the PLC input’s other side is 0 V. Sinking output pulls the PLC input *down* to 0 V; the input is tied to +24 V through the module. Mixing PNP sensors with a sinking-only card is a lab classic failure. Two-wire AC namur/proximity devices exist for 120/230 V inputs. **Photoelectric** (through-beam, retro, diffuse) detect boxes; through-beam is the most reliable, diffuse the cheapest. **Reed** and **Hall** sense cylinders’ magnets.

**Debounce.** A mechanical contact bounces for 1–20 ms. Digital filter: require \(N\) consecutive scans true, with \(N T_s\) longer than bounce but shorter than the shortest real pulse you must catch. TON debounce: the contact must stay true for PRE before the cleaned bit rises. Do not debounce an encoder A/B channel in software at 10 kHz; use an HSC.

**Analog sensors.** Process variables become **4–20 mA** (preferred on long runs: loop-powered, two-wire, live-zero so a broken wire is 0 mA not “0 percent”) or **0–10 V** (short, high-impedance, cheaper, more noise). 4 mA = 0 percent of span, 20 mA = 100 percent. Scaling
\[
x = x_{\min}+\frac{I-4}{16}(x_{\max}-x_{\min}).
\]
A 12 mA reading is mid-span. **0–20 mA** loses the live-zero. **HART** rides FSK on the 4–20 mA; name only. RTD and thermocouple usually hit a transmitter that *outputs* 4–20 mA; a PLC analog card can also take mV/RTD directly on some modules.

**ADC on analog input.** A 12-bit card over 4–20 mA (after a 250 Ω burden, 1–5 V) has \(4096\) counts on 0–full electrical range; only \(0.8\) of that range is the 4–20 mA live band if the card is 0–20 mA spanned. Resolution in engineering units: span divided by the number of counts in use. 16-bit cards are common; the *sensor* accuracy is often worse than 1 count.

**Actuators, discrete.** A PLC **output** drives an **interposing relay** or a **contactor coil** (230 V AC coils still exist; 24 V DC coils match the I/O supply). Inductive kick: a **freewheel diode** on DC coils, an RC or MOV on AC. **Triac** AC outputs leak a few mA — enough to glow an LED lamp or hold a tiny relay; use a bleeder or a relay output. **Solenoid valves** on pneumatics/hydraulics are the same electrical object as a coil with a diode. **Solid-state outputs** switch fast and silently; they leak and fail short more often than a relay fails open — for e-stop paths, a hard contact is the study-level default.

**Actuators, analog.** A 4–20 mA output positions a control valve or a VFD speed reference. 0–10 V into a drive analog input is common in labs. Isolation: analog outputs should not share a dirty motor ground; use isolated cards or signal isolators.

**Sinking/sourcing outputs** mirror the sensor story. A sourcing PLC output provides 24 V to a load returned to 0 V. Short-to-ground is then a fuse event. Follow the card’s diagram; do not assume.

**Isolation.** Optocouplers on digital cards, transformers or isolated DC/DC on analog, and a separate **PE** earth versus 0 V common. A 24 V PSU listed as PELV/SELV with the 0 V bonded to PE at one point is a usual panel practice. Ground loops on analog shields: bond the shield at one end.

**Interlocks (study-level).** An **interlock** is a condition that must be true before a hazardous output may energize. Examples: guard closed, two-hand, zero-speed, oil pressure OK, opposite direction’s contactor auxiliary NC (mechanical and electrical interlocking of reversing contactors). **E-stop** is a category above a regular Stop: it must be easy to hit, latch, and require a deliberate reset. **Fail-safe wiring:** the e-stop series string is **NC** contacts in a *energized-to-run* loop. A broken wire, a pulled connector, or a loss of 24 V de-energizes the loop and looks like a stop. An NO e-stop in software “if EStop==1 then stop” fails silent if the wire falls off (EStop stays 0). Dual-channel e-stop into a safety relay or safety PLC is what a real press uses; this course writes the *principle* and a single-channel teaching ladder, and says so.

**Hardwired vs software.** Software permissives in the ladder are easy to bypass with a force. A **safety relay** or **safety PLC** with monitored reset, redundant channels, and outputs that drop even if the standard CPU is wedged, is required where injury is plausible. UG numericals still draw a series NC e-stop in the *standard* ladder so you learn the Boolean; the report should add “not a SIL claim.”

**Motor branch:** MCB / fuses, contactor, overload relay (thermal or electronic), auxiliary contacts back to PLC inputs (`KM1_aux`, `OL_trip`). The overload should drop the contactor *even if* the PLC output is stuck on — that is hardwired, not only a ladder bit.

**4–20 mA break detection:** if \(I<3.6\,\mathrm{mA}\) (NAMUR NE43 region), treat as fault, not as “very low process.” If \(I>21\,\mathrm{mA}\), likewise.

**Panel hygiene (exam phrases):** ferrules, numbered wires, 24 V and 230 V segregated, no 230 V on the same terminal strip as dry PLC inputs without a barrier.

This unit’s exam jobs: scale 4–20 mA, pick PNP vs NPN, debounce count \(N\), NC fail-safe e-stop, and analog resolution. Do not energize a live actuator from this handbook.

## Equations

4–20 mA scale:
\[
x=x_{\min}+\frac{I_{\mathrm{mA}}-4}{16}(x_{\max}-x_{\min}),\qquad
I_{\mathrm{mA}}=4+16\frac{x-x_{\min}}{x_{\max}-x_{\min}}.
\]
0–10 V:
\[
x=x_{\min}+\frac{V}{10}(x_{\max}-x_{\min}).
\]
ADC step (counts \(2^n\), electrical span \(V_{\mathrm{span}}\)):
\[
\Delta V=\frac{V_{\mathrm{span}}}{2^n},\qquad \Delta x=\frac{x_{\max}-x_{\min}}{N_{\mathrm{counts\ in\ span}}}.
\]
Debounce:
\[
t_{\mathrm{deb}}=N T_s \ge t_{\mathrm{bounce}}.
\]
Live-zero fault:
\[
I<3.6\,\mathrm{mA}\ \text{or}\ I>21\,\mathrm{mA}\ \Rightarrow\ \text{fault, not a process value}.
\]

Fail-safe e-stop loop (study):
\[
\mathrm{OK}=\mathrm{ES1}\land \mathrm{ES2}\land \cdots \quad(\text{each ES a closed NC}).
\]

## Methods

To scale a transmitter: write 4 mA \(\leftrightarrow x_{\min}\), 20 mA \(\leftrightarrow x_{\max}\), linear interpolate. Invert when the PLC must *output* 4–20 mA for a setpoint.

To choose sensor polarity: read the PLC input schematic. “Current into the input terminal when true” \(\Rightarrow\) sourcing (PNP) sensor. Match 24 V commons.

To debounce: measure or assume bounce \(<10\,\mathrm{ms}\), scan \(5\,\mathrm{ms}\) \(\Rightarrow\) \(N=3\) or \(4\), or a 20 ms TON.

To interlock two directions: series NC of the opposite output (and of the opposite contactor auxiliary, hardwired). Add a TON of 200–500 ms so one contactor drops before the other pulls in (mechanical overlap).

To wire e-stop on paper: 24 V \(\to\) NC mushroom \(\to\) NC gate \(\to\) safety-relay input. Reset is a separate NO, monitored. PLC sees a *status* input, not the only path.

To size analog resolution: span / \(2^n\) if the card span equals the signal span; if 4–20 mA on a 0–20 mA card, usable counts \(\approx 0.8\times 2^n\).

To catch a 4–20 mA break: compare raw counts to a low limit before scaling, set a fault bit, do not drive a PID with \(x=x_{\min}\).

Study-only: complete the I/O list (tag, address, type, PNP/NPN, scale, fail-safe state) as a table. That table is the assignment deliverable, not a download.

## Mistakes

Treating 0 mA as 0 percent on a 4–20 mA loop (0 mA is broken).

Scaling \(x=(I/20)x_{\max}\) (wrong intercept).

PNP sensor into a card that expects NPN, then “the input is always on.”

Debounce longer than the pulse you must count.

Software-only e-stop as an NO contact.

Energize-to-run missing: using a latched output that survives a CPU crash without a hardwired drop-out.

Analog 0–10 V over 50 m of unshielded cable next to a VFD.

Triac output on a small relay without checking holding current / leakage.

Forgetting the overload’s hardwired series with the contactor coil.

Calling a teaching ladder a safety-rated system.

Live writes to plant I/O from this product — forbidden (`docs/CANNOT_DO.md` CD-PLC).

Worked 4–20 mA burden: a 250 \(\Omega\) resistor turns 4–20 mA into 1–5 V for a voltage-mode analog card. Power in the resistor at 20 mA is \(I^2 R=0.1\,\mathrm{W}\); a 0.25 W resistor is the lazy safe pick. If the transmitter needs a minimum compliance voltage, add the burden, the cable drop, and the card’s insertion drop, and keep the 24 V supply above that sum at 20 mA.

Reversing-motor interlock on paper: two contactors K1 (forward) and K2 (reverse). Hardwire K1’s NC auxiliary in series with K2’s coil and vice versa. In the ladder, the forward rung includes NC `K2_aux` and NC `Rev_cmd`; the reverse rung mirrors. A TON of a few hundred milliseconds after a direction change covers the mechanical overlap. Without that, a brief two-contactor close is a bolted line-to-line on the motor terminals.

Analog output to a VFD: 4–20 mA into the drive’s AI, 4 mA = 0 Hz (or minimum frequency), 20 mA = \(f_{\max}\). A broken analog wire should command *minimum* or *stop* if the drive is configured for live-zero fault, not 0 mA interpreted as a valid 0 percent that might still enable a coast. The PLC digital `Enable` and a hardwired e-stop to the drive’s STO (safe torque off) terminals are separate from the speed reference.

I/O list as the assignment artifact: columns Tag, Address, In/Out, Discrete/Analog, Range, Fail state, Drawing. Example: `ES_OK`, `%IX0.0`, In, Discrete, 24 V DC sink, 0 = stop, E-stop loop. Example: `TT1`, `%IW2`, In, Analog, 4–20 mA = 0–100 °C, fault if counts < 4 mA equivalent. That table, not a live download, is what this pack produces.
