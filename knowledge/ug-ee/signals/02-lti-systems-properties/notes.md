# Linearity, time-invariance, memory, invertibility

A system maps an input signal \(x\) to an output signal \(y=\mathcal{S}\{x\}\). The map may be continuous-time or discrete-time, single-input or multi-input. Undergraduate signals courses classify systems by structural properties that decide which transforms and which convolution theorems apply. Linearity plus time-invariance yields an impulse response and a convolution representation. Causality, memory, stability, and invertibility further constrain that impulse response. This unit states the properties as tests on \(\mathcal{S}\), not as slogans.

## Concepts

A system is linear if superposition holds for every pair of inputs and every pair of scalars in the field (usually \(\mathbb{C}\) or \(\mathbb{R}\)):

\[
\mathcal{S}\{a x_1+b x_2\}=a\,\mathcal{S}\{x_1\}+b\,\mathcal{S}\{x_2\}.
\]

Homogeneity and additivity are often checked separately; both are required. A nonzero initial condition stored in a capacitor or a recursive register makes the zero-input response nonzero, which breaks homogeneity at the origin unless those states are treated as extra inputs. Affine maps \(y=Tx+c\) with \(c\neq 0\) are not linear. Incrementally linear systems can be written as a linear map plus a fixed zero-input signal; superposition still fails unless \(c=0\).

Time-invariance (shift-invariance) means that delaying the input delays the output by the same amount. If \(y(t)=\mathcal{S}\{x(t)\}\) and \(x_1(t)=x(t-t_0)\), then \(\mathcal{S}\{x_1\}(t)=y(t-t_0)\). In discrete time the shift is an integer. A system whose coefficients depend on time, such as \(y(t)=t x(t)\) or \(y[n]=n x[n]\), is time-varying. A modulator \(y(t)=x(t)\cos(\omega_c t)\) is linear and time-varying. A squarer \(y=x^2\) is time-invariant and nonlinear. A compressor \(y(t)=x(2t)\) is linear and time-varying: a delay of the input does not commute with the time scale.

Memoryless systems compute \(y(t)\) from \(x(t)\) at the same instant only (or \(y[n]\) from \(x[n]\) only). A resistor is memoryless; a capacitor is not. Any system whose output at time \(t\) depends on values of \(x\) at other times has memory. Finite memory means dependence on a bounded look-back (and possibly look-ahead). Infinite memory includes IIR filters and ideal integrators. Noncausal systems may still be memoryless (a gain) or may look ahead (an ideal zero-phase smoother that uses future samples).

Causality: the output at time \(t_0\) depends only on the input for \(t\le t_0\). In an LTI setting this is equivalent to \(h(t)=0\) for \(t<0\) (or \(h[n]=0\) for \(n<0\)). Causality is a property of the system, not of a particular input. A causal system can still be driven by a two-sided input; the output at time \(t\) then still uses only the past and present of that input. Real-time physical devices are causal. Offline filtering of a recorded file need not be.

Invertibility: distinct inputs produce distinct outputs, and there exists a system \(\mathcal{S}^{-1}\) such that \(\mathcal{S}^{-1}\{\mathcal{S}\{x\}\}=x\) for every \(x\) in the intended space. A differentiator is not invertible on all reasonably smooth signals because constants vanish. An integrator without a specified initial condition is not invertible. A delay is invertible (the inverse is an advance, which is noncausal). An ideal sampling operator is not invertible without a bandlimit hypothesis. Invertibility on a subspace (bandlimited functions, zero-mean sequences) is often the useful statement.

Stability in this unit is mentioned only as a named property; BIBO is developed fully in a later unit. Briefly, BIBO stability means every bounded input yields a bounded output. For LTI systems this is equivalent to an absolutely integrable (or summable) impulse response. A system may be linear, time-invariant, causal, and still unstable (an ideal integrator, an inverted pendulum linearized model with a right-half-plane pole).

Memory, causality, and invertibility are independent of linearity. Time-invariance is independent of linearity. The eight combinations of linear/nonlinear and time-invariant/time-varying all occur in circuits and DSP. LTI is the combination that diagonalizes in the complex-exponential basis.

An LTI system is completely characterized by its impulse response \(h=\mathcal{S}\{\delta\}\). That is a theorem, not a definition: it uses linearity to pass from \(\delta\) to a linear combination of shifts, then time-invariance to move those shifts onto \(h\), then a limiting argument for CT. Without both properties, \(\mathcal{S}\{\delta\}\) does not determine the response to other inputs. A linear time-varying system has a kernel \(h(t,\tau)\) with \(y(t)=\int h(t,\tau)x(\tau)\,d\tau\); a nonlinear system has no such kernel in general.

Fixed-point arithmetic, clipping, and slew-rate limits are nonlinear. Dead-zone and hysteresis are nonlinear with memory. Multiplication of two signals is bilinear as a map of the pair \((x_1,x_2)\) but nonlinear as a system in one input if the other signal is itself derived from that input.

Continuous-time LTI differential systems \(\sum a_k y^{(k)}=\sum b_m x^{(m)}\) are linear and time-invariant when the coefficients \(a_k,b_m\) are constant. Variable-coefficient ODEs are linear and time-varying. Nonlinear ODEs (products of \(y\) and \(\dot y\), \(\sin y\)) fail superposition. The same story holds for constant-coefficient linear recurrences in discrete time.

A system can be invertible yet not stably invertible: a differentiator inverted by an integrator is the classic pair, and the integrator is not BIBO stable. A system can be causal yet have an anticausal inverse (a delay of \(-1\) sample as inverse of a one-step advance, or a minimum-phase versus maximum-phase factorization in later DSP). These distinctions matter when one designs equalizers.

## Equations

Linearity test (must hold for all \(a,b,x_1,x_2\)):

\[
\mathcal{S}\{a x_1+b x_2\}=a\,\mathcal{S}\{x_1\}+b\,\mathcal{S}\{x_2\}.
\]

Time-invariance: with \(y=\mathcal{S}\{x\}\),

\[
\mathcal{S}\{x(\,\cdot\,-t_0)\}(t)=y(t-t_0).
\]

Memoryless CT: there exists a function \(f\) with \(y(t)=f\bigl(x(t)\bigr)\) for all \(t\). Memoryless DT: \(y[n]=f\bigl(x[n]\bigr)\).

Causal: if \(x_1(t)=x_2(t)\) for all \(t\le t_0\), then \(y_1(t_0)=y_2(t_0)\). Equivalent for LTI: \(h(t)=0\) for \(t<0\).

Convolution representation of CT LTI (developed in the next unit, stated here as the consequence of the two properties):

\[
y(t)=\int_{-\infty}^{\infty}h(\tau)x(t-\tau)\,d\tau=(h*x)(t), \qquad h=\mathcal{S}\{\delta\}.
\]

Discrete counterpart:

\[
y[n]=\sum_{k=-\infty}^{\infty}h[k]x[n-k].
\]

Eigenfunction property of CT LTI:

\[
\mathcal{S}\{e^{st}\}=H(s)\,e^{st},
\qquad
H(s)=\int_{-\infty}^{\infty}h(t)e^{-st}\,dt,
\]

when the integral converges. Discrete: \(\mathcal{S}\{z^n\}=H(z)z^n\) with \(H(z)=\sum h[n]z^{-n}\).

A static nonlinearity \(y=x^2\) fails linearity because \((x_1+x_2)^2\neq x_1^2+x_2^2\) in general. A modulator \(y(t)=x(t)c(t)\) with a fixed \(c\) is linear in \(x\) and time-varying unless \(c\) is constant.

Incrementally linear form:

\[
y=\mathcal{S}_{\mathrm{lin}}\{x\}+y_{\mathrm{zi}},
\]

where \(y_{\mathrm{zi}}\) does not depend on \(x\). Superposition of inputs does not superpose outputs unless \(y_{\mathrm{zi}}=0\).

## Methods

To test linearity, apply two inputs that are easy to compute, form \(a x_1+b x_2\), compute both sides, and look for a mismatch. Include a check with \(a=0\) to catch additive offsets. If the system is defined by a formula, substitute \(\alpha x\) and compare with \(\alpha y\).

To test time-invariance, compute \(y(t)\) from \(x(t)\), form \(x(t-t_0)\), run the system, and compare with \(y(t-t_0)\). A reliable shortcut: if every coefficient and every explicit time function multiplying the signals is constant, and the only time operations are convolutions, differentiations, and constant delays, the system is TI. If \(t\) or \(n\) appears as a multiplier, or a time scale \(x(at)\) with \(a\neq 1\), expect TV.

To test memorylessness, ask whether \(y\) at one instant can change when \(x\) at that instant is held fixed and the rest of the waveform is altered. If yes, there is memory. Integrals, delays, and FIR taps all fail this test.

To test causality, try an input that is zero up to time \(t_0\) and nonzero after, and see whether \(y(t_0)\) can be nonzero because of the future. For LTI systems, plot \(h\) and look left of the origin.

To test invertibility, hunt for a nonzero input that produces the zero output, or two inputs with the same output. If the system is LTI, zeros of \(H(s)\) (or \(H(z)\)) on the input class destroy invertibility; an inverse filter \(1/H\) may still exist as a formal transform but fail to be causal or stable.

When several properties are asked, table them. Do not infer causality from stability or linearity from time-invariance. Work an example for each claimed yes/no.

For circuits, write the differential equation first. Constant \(R,L,C\) with zero independent initial energy, taking the source as the input, typically gives a causal LTI map from source to a branch waveform. Nonzero initial capacitor voltage is a second input; hiding it produces an affine map.

## Mistakes

Calling \(y(t)=x(t)+1\) linear. The extra 1 is a bias; homogeneity fails.

Calling \(y(t)=x(t)\cos(\omega t)\) time-invariant because a cosine is a “standard signal.” The cosine is a coefficient that depends on time.

Calling \(y(t)=x(2t)\) time-invariant. Scaling time does not commute with delay.

Assuming every causal system is stable, or every stable system is causal. Neither implication holds.

Using \(h=\mathcal{S}\{\delta\}\) to predict outputs of a nonlinear or time-varying system. The convolution formula is LTI-only.

Confusing invertibility with stability of the inverse. A delay of \(-2\) samples inverts a delay of \(+2\) samples but is noncausal.

Testing linearity with one pair of numbers and declaring success. The identity must hold for all inputs in the class; a counterexample disproves, a few examples do not prove. When the formula is algebraic and clearly linear in \(x\), that algebraic identity is the proof; when the system is specified operationally, argue from the operations.

Treating a system with a switch that closes at \(t=0\) as time-invariant on \(-\infty<t<\infty\). The switch is a time-varying element unless the time origin is part of every input in a consistent way and you restrict the domain.

Claiming a differentiator is memoryless because it “uses only the present.” A derivative is a limit of neighboring values; it has memory in the classification used here, and it is not a static map \(f(x(t))\).

Declaring invertibility from “I can write an inverse formula” without specifying the signal space. An integrator inverse differentiates only on the subspace of outputs that came from the integrator, i.e. absolutely continuous signals with a prescribed value at \(-\infty\).

Using a single sinusoid to test time-invariance of a modulator. A delay of a cosine is another cosine of the same frequency, which can accidentally look invariant; use a pulse or a sum of two tones.

Ignoring that linearity is a statement about all pairs of inputs. Homogeneous maps that are not additive exist (and conversely) in pathological cases; in UG formulas, check both a scalar multiple and a sum.

Forgetting that discrete systems can look at \(x[n+1]\) and still be linear and TI. Causality is the property that fails, not LTI.
