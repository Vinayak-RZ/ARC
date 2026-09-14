# Lead, lag, PID, and Ziegler–Nichols intro

Compensators add poles and zeros to \(L(s)\) so that a loop that cannot meet damping, bandwidth, and error-constant specs with a single gain \(K\) can meet them with a slightly richer \(C(s)\). UG design uses lead for phase margin / transient, lag for \(K_v\) / steady-state, lag–lead for both, and PID as the industrial parameterization of the same ideas. Ziegler–Nichols is a tuning recipe from an ultimate-gain experiment, not a substitute for a model-based lead design, but it is in every first course.

## Concepts

A lead network
\[
C_{\mathrm{lead}}(s)=K_c\alpha\frac{\tau s+1}{\alpha\tau s+1},\qquad 0<\alpha<1
\]
puts the zero to the right of the pole (zero at \(1/\tau\), pole at \(1/(\alpha\tau)\), pole farther left). It adds a positive phase bump with maximum
\[
\phi_m=\sin^{-1}\frac{1-\alpha}{1+\alpha}=\tan^{-1}\frac{1-\alpha}{2\sqrt{\alpha}}
\]
at \(\omega_m=1/(\tau\sqrt{\alpha})\). On Bode, magnitude rises \(+20\) dB/dec between zero and pole. Lead is used when PM is short: place \(\omega_m\) near the new gain crossover, choose \(\phi_m\) a few degrees above the PM deficit (because the magnitude rise moves \(\omega_g\) up, where the plant phase is worse). Root-locus view: a lead zero pulls the dominant branches left; the pole is farther left so it does not cancel that help.

A lag network uses \(\beta>1\) in
\[
C_{\mathrm{lag}}(s)=K_c\frac{\tau s+1}{(\tau/\beta)s+1}\qquad\text{(zero closer to the origin than the pole?)}
\]
Standard: pole closer to the origin than the zero, \(\beta>1\),
\[
C_{\mathrm{lag}}(s)=\frac{\tau s+1}{\beta\tau s+1},\qquad \beta>1,
\]
zero at \(1/\tau\), pole at \(1/(\beta\tau)\). Phase is negative (a PM penalty). Magnitude drops \(20\log_{10}\beta\) at high frequency relative to DC. Used after a gain is raised to meet \(K_v\): the lag restores the high-frequency gain (and thus \(\omega_g\) and PM) nearly to the old values while keeping the low-frequency gain high. Place the lag dipole a decade below the gain crossover so the phase lag at \(\omega_g\) is only about \(5^\circ\).

Lag–lead is a cascade of both, four parameters, designed in two steps: lead for PM at a chosen \(\omega_g\), lag for the remaining \(K_v\).

PID:
\[
C_{\mathrm{PID}}(s)=K_p+K_i/s+K_d s=K_p\bigl(1+1/(T_i s)+T_d s\bigr).
\]
PI is lag-like plus an extra integrator (type increase by 1, zero step error if the plant was type 0). PD is lead-like (zero, no extra pole unless a filter is added). PID is a zero pair and a free integrator. The derivative term is improper; implementations use \(T_d s/(1+T_d s/N)\) with \(N\sim 8\)–\(20\). Do not realize naked \(K_d s\) as a plant in simulation without that pole.

Ziegler–Nichols. Ultimate-sensitivity method: increase proportional gain until the loop oscillates steadily; record \(K_u\) and the period \(P_u=2\pi/\omega_u\). Then, in the classical table: P control \(K_p=0.5 K_u\); PI \(K_p=0.45 K_u\), \(T_i=P_u/1.2\); PID \(K_p=0.6 K_u\), \(T_i=P_u/2\), \(T_d=P_u/8\). The reaction-curve method uses a open-loop step’s apparent delay \(L\) and slope \(R\) (or time constant \(\tau\)) with another table. Ziegler–Nichols often gives aggressive, underdamped loops; it is a starting guess. \(K_u\) is exactly the Routh/Nyquist crossing gain of the looped plant with a proportional controller.

Design order that works: (1) plant model and specs (PM, \(t_s\), \(K_v\), type); (2) try \(K\) only; (3) if PM fails, lead or PD; (4) if \(K_v\) fails, lag or PI; (5) if both, lag–lead or PID; (6) verify by Bode + step, not by the table alone. Unstable plants need the Nyquist/root-locus version of lead (enough encirclements), not a PM recipe that assumed \(P=0\).

Integrator windup (saturation) is a nonlinear implementation issue: PI continues integrating while the actuator is pegged. Anti-windup is later; UG should still know that a huge \(K_i\) plus saturation yields overshoot that linear theory did not predict.

Notch filters cancel a resonant plant pair; they are not lead/lag. Cancellation of an undamped pair is fragile. Prefer to damp by inner-loop rate feedback when the resonance is a structure you can measure.

## Equations

Lead max phase:
\[
\sin\phi_m=\frac{1-\alpha}{1+\alpha},\qquad \omega_m=\frac{1}{\tau\sqrt{\alpha}}.
\]
Lead magnitude at \(\omega_m\): \(20\log_{10}(1/\sqrt{\alpha})\) relative to the low-frequency \(K_c\alpha\) if that parameterization is used — check the leading constant. A common form \(C=K_c(\alpha s+1)/(\alpha\tau s+\cdots)\) differs; always expand \(C(j\omega_m)\) once.

Lag high-frequency attenuation: \(1/\beta\) if DC gain is 1.

PI: \(C=K_p(s+z)/s\) with \(z=K_i/K_p\).

ZN ultimate (common table):
\[
\begin{array}{c|ccc}
 & K_p & T_i & T_d\\\hline
\mathrm{P} & 0.5 K_u & - & -\\
\mathrm{PI} & 0.45 K_u & P_u/1.2 & -\\
\mathrm{PID} & 0.6 K_u & P_u/2 & P_u/8
\end{array}
\]

\(K_u\) from Routh on \(1+K G_{\mathrm{plant}}=0\), or from a relay/ultimate experiment.

Error constants after compensator: \(K_v^{\mathrm{new}}=\lim s C(s)G(s)\) (unity \(H\)). A lag with DC gain \(\beta\) if written as \(C=\beta(\tau s+1)/(\beta\tau s+1)\) multiplies \(K_v\) by \(\beta\). Watch the form.

## Methods

Lead Bode recipe: (1) find \(K\) for the \(K_v\) spec, ignoring PM; (2) Bode of \(KG\), read PM deficit \(\Delta=\mathrm{PM}_{\mathrm{req}}-\mathrm{PM}+\varepsilon\) with \(\varepsilon\sim 5^\circ\)–\(12^\circ\); (3) \(\alpha\) from \(\sin\phi_m=(1-\alpha)/(1+\alpha)\) with \(\phi_m=\Delta\); (4) place \(\omega_m\) at the new crossover, estimated as the frequency where \(|KG|=-20\log_{10}(1/\sqrt{\alpha})\) dB (so after lead gain the crossover sits at \(\omega_m\)); (5) \(\tau=1/(\omega_m\sqrt{\alpha})\); (6) recompute PM.

Lag Bode recipe: (1) choose \(K\) for PM (or keep current \(\omega_g\)); (2) \(\beta=K_{v,\mathrm{needed}}/K_{v,\mathrm{now}}\); (3) put lag zero one decade below \(\omega_g\), pole at \(z/\beta\); (4) check the extra phase lag at \(\omega_g\).

Root-locus lead: measure angle defect at the desired dominant pole, solve for a real zero/pole pair that supplies that angle, then set \(K\) by magnitude. Prefer the pole left of the zero by a factor 5–15.

PID from ZN: measure \(K_u,P_u\), apply the table, then detune \(K_p\) if the step rings. Do not use ZN on a plant that cannot sustain a stable oscillation (no finite \(K_u\)).

Always close the loop in a calculation: write \(T=CG/(1+CG)\) and check Routh, or compute PM of \(CG\).

## Mistakes

Lead with \(\alpha>1\) (that is lag) while expecting phase lead.

Placing the lead \(\omega_m\) at the old \(\omega_g\) and then being surprised that PM is still short because crossover moved up.

Lag dipole straddling \(\omega_g\), dumping \(40^\circ\) of phase lag on the margin.

PI on a type-1 plant when the spec did not need type 2, adding a near-origin dipole that slows settling (long tail).

Using ZN \(K_p=0.6 K_u\) on an open-loop unstable plant without checking that a \(K_u\) oscillation exists in the same sense.

Realizing \(K_d s\) without a filter, then differentiating measurement noise.

Forgetting that PD changes \(K_p\) equivalent and thus \(K_v\) slightly; recompute error constants after the compensator.

Cancelling a RHP plant pole with a RHP zero of \(C\) (internal instability).

Applying the lead \(\alpha\) formula with \(\phi_m\) in radians in a \(\sin\) that expected degrees, or the reverse.

Designing lead from PM of an open-loop unstable \(L\) as if \(P=0\).

A numerical lead pass, the kind that should be in a lab notebook: plant \(G=4/[s(s+2)]\), spec \(K_v\ge 10\) and \(\mathrm{PM}\ge 50^\circ\). Uncompensated \(K\) for \(K_v\): \(L=K_c G\), \(K_v=2 K_c\), so \(K_c=5\) gives \(K_v=10\). Then \(L=20/[s(s+2)]\). Gain crossover from \(|L|=1\): \(20=\omega\sqrt{\omega^2+4}\), \(\omega^4+4\omega^2-400=0\), \(u=\omega^2=-2+\sqrt{404}\approx 18.10\), \(\omega_g\approx 4.25\). Phase \(-90-\tan^{-1}(4.25/2)=-90-64.8=-154.8^\circ\), \(\mathrm{PM}=25.2^\circ\), short by about \(25^\circ\). Add \(10^\circ\) safety: \(\phi_m=35^\circ\). \(\sin 35^\circ=0.574=(1-\alpha)/(1+\alpha)\), \(\alpha=0.271\). Magnitude bump of the lead at \(\omega_m\) is \(1/\sqrt{\alpha}\approx 1.92\) (\(5.7\,\mathrm{dB}\)). Find where uncompensated \(|L|\) is \(-5.7\,\mathrm{dB}\) (about 0.52) on the high side of the old crossover; that frequency becomes the new \(\omega_g\approx\omega_m\). Place zero \(1/\tau=\omega_m\sqrt{\alpha}\), pole \(1/(\alpha\tau)=\omega_m/\sqrt{\alpha}\). Recompute \(L_{\mathrm{new}}(j\omega)\) at the new crossover; if PM is 47° instead of 50°, increase \(\phi_m\) a few degrees and iterate once. Do not iterate five times on an exam; one correction is enough.

Lag pass on the same plant if the PM at \(K_c=1\) was already 50° but \(K_v\) was only 2: keep the high-frequency gain near \(K_c=1\), set \(\beta=10/2=5\), put the lag zero at \(\omega_g/10\), pole at that zero divided by 5. The Bode magnitude at high \(\omega\) is almost unchanged; \(K_v\) becomes 10; PM drops a few degrees from the lag’s residual phase.

PID as pole-zero arithmetic: \(K_p(1+1/(T_i s)+T_d s)=K_p T_d(s^2+(1/T_d)s+1/(T_i T_d))/s\). Two zeros and a pole at the origin. If the zeros are real, it is a PI cascade with a PD. If they are complex, it is a quadratic notch-like numerator, useful on a plant pair you want to cancel (only if that pair is well damped and well known). Ziegler–Nichols PID places those zeros at a fixed fraction of \(\omega_u\): \(T_i=P_u/2\) and \(T_d=P_u/8\) imply zeros of \(s^2+(4/P_u)s+16/P_u^2=(s+2/P_u)^2\), a repeated real zero at \(s=-2/P_u=-f_u\), i.e. at the ultimate frequency in rad/s divided by \(\pi\). That is why ZN rings: the compensator zeros sit relatively close to the plant’s \(j\omega\) crossing, not far into the LHP.

Derivative filter: replace \(T_d s\) by \(T_d s/(1+T_d s/N)\). The extra pole is at \(s=-N/T_d\). Choose \(N=10\) unless noise is terrible (\(N=4\)) or the sensor is clean and you need the full PD lead (\(N=20\)). Include that pole in the Bode of \(C(j\omega)\) when checking PM; omitting it overstates PM by the phase of a pole you actually have.

Windup in one paragraph: while \(u\) is clamped, \(\dot{\xi}=e\) still runs in a PI. When the clamp releases, \(\xi\) is huge and the output slams the other rail. Fix: stop integrating while clamped (clamping the integrator state), or back-calculate \(\xi\) from the achievable \(u\). UG design reports should mention the clamp; they need not implement back-calculation unless the lab asks.
