# Arc live A/B, held-out sheets v1 (13 Nov 2026)

Solve every problem. For each, give the final numeric answer(s) with units, plus a short method note.
Write a JSON file `answers.json`: {"P1": {"answers": {...}, "method": "...", "confidence": 0-1}, ...}.
Use per-unit and SI exactly as stated. f = 50 Hz unless stated.

P1 (SMIB transient stability, CCT). A generator with H = 4.5 MJ/MVA delivers Pm = 0.8 pu to an infinite bus.
Pre-fault Pmax = 1.9 pu, during-fault Pmax = 0.35 pu, post-fault (one line tripped) Pmax = 1.4 pu.
Find (a) initial angle delta0 (deg), (b) critical clearing angle delta_cr (deg), (c) critical clearing time t_cr (s) by numerically integrating the swing equation (state your step size).

P2 (SMIB, clearing check). Same system as P1. The fault is cleared at t = 0.25 s. Is the system stable? Give the maximum rotor angle reached (deg) if stable, or state when delta exceeds 180 deg if unstable.

P3 (Economic dispatch with limits). Three units, cost Ci = ai + bi*Pi + ci*Pi^2 (Rs/h, P in MW):
U1: b=7.0, c=0.0040, 100<=P1<=500; U2: b=6.3, c=0.0060, 80<=P2<=250; U3: b=6.8, c=0.0050, 50<=P3<=300.
Ignore losses. Demand PD = 900 MW. Find P1, P2, P3 (MW) and lambda (Rs/MWh).

P4 (Two-area AGC, primary response only). Two identical areas, each: R = 0.05 pu (on own base), D = 1.0 pu MW/pu Hz... use beta_i = 1/R_i + D_i = 21 pu (on 1000 MW base, f0 = 50 Hz). Area 1 sees a step load increase of 50 MW; no secondary control. Find (a) steady-state frequency deviation (Hz), (b) steady-state tie-line flow change Delta P12 (MW) with sign convention P12 positive from area 1 to area 2.

P5 (Control, margins). Open loop L(s) = 40 / (s (s+2)(s+10)), unity negative feedback. Find gain crossover frequency (rad/s), phase margin (deg), phase crossover frequency (rad/s), and gain margin (dB).

P6 (Circuit transient). Series RLC driven by a 12 V DC step at t=0, R = 4 ohm, L = 0.5 H, C = 0.02 F, initially relaxed. Find (a) the damping type, (b) the peak capacitor voltage (V) and the time it occurs (s), (c) the 2% settling time (s).

P7 (Symmetrical components, SLG fault). A 33 kV bus, Thevenin sequence impedances (pu, 100 MVA base): Z1 = j0.20, Z2 = j0.20, Z0 = j0.30, Zf = 0. Bolted single-line-to-ground fault on phase a, prefault 1.0 pu. Find fault current magnitude in pu and in kA.

P8 (Induction motor). 3-phase, 415 V (line), 50 Hz, 4-pole, star-connected. Per-phase: R1 = 0.5, X1 = 1.2, R2' = 0.4, X2' = 1.2, Xm = 30 ohm (neglect core loss). At slip s = 0.04 find (a) rotor speed (rpm), (b) stator current (A), (c) developed (gross mechanical) torque (N m), using the exact equivalent circuit (not approximate). Also find (d) slip at maximum torque using the Thevenin equivalent.
