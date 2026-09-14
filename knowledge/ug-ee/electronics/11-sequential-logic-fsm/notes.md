# Sequential logic: latches, flip-flops, counters, and FSMs

Sequential logic has memory: next outputs depend on present inputs *and* the present state. UG courses build from the SR latch through edge-triggered flip-flops to counters, shift registers, and finite-state machines (Moore and Mealy). Timing — setup, hold, clock skew — is the difference between a working board and a metastable mess.

## Concepts

A bistable is two inverters in a loop, or two NOR (NAND) gates cross-coupled. SR latch (NOR): Set and Reset are active-high; \(SR=11\) is forbidden because both outputs go 0 and the race after release is undefined. NAND SR (active-low \(\bar S\bar R\)): forbidden is \(00\). The latch is *level-sensitive*: while enable (or the S/R inputs) is asserted, the output follows.

Gated D latch (transparent latch): \(Q=D\) while \(EN=1\), holds while \(EN=0\). Used as a store between combinational clouds in two-phase latch pipelines; in UG, mostly a stepping stone to the flip-flop.

Flip-flop: edge-triggered. Master-slave: two latches in series with complementary enables, so the output changes once per clock, on the trailing (or leading) edge depending on the drawing. An edge-triggered D-FF samples \(D\) on the active clock edge and holds until the next. JK-FF: \(J=K=1\) toggles; it is a D-FF with \(D=J\bar Q+\bar K Q\). T-FF: toggle when \(T=1\), i.e. JK with \(J=K=T\), or D with \(D=T\oplus Q\). Conversion among FF types is a standard exercise: write the excitation table of the target, express \(D\) or \(J,K\) in terms of \(Q\) and the desired next state.

Timing parameters. Setup \(t_{su}\): \(D\) must be stable this long *before* the edge. Hold \(t_h\): \(D\) must remain stable this long *after* the edge. Clock-to-Q \(t_{cq}\) (max) and contamination \(t_{cd}\) (min). For a single-cycle path, \(t_{cq}+t_{pd,comb}+t_{su}\le T_{clk}-t_{skew}\). Hold: \(t_{cd,FF}+t_{cd,comb}\ge t_h+t_{skew}\). Hold failures cannot be fixed by slowing the clock. Metastability: if \(D\) violates setup/hold, \(Q\) may sit at a half-level for an unbounded (exponentially unlikely) time. Dual-rank synchronisers on async inputs buy MTBF.

Registers: n D-FFs sharing a clock. Shift register: serial-in serial-out (SISO), SIPO, PISO, PIPO, universal (74194). Ring counter: n-bit shift of a single 1, period n. Johnson (twisted-ring): invert the last bit back to the input, period \(2n\), Gray-like adjacent codes. Linear feedback shift register (LFSR): XOR taps, maximal period \(2^n-1\) for a primitive polynomial — used as a PRBS, not as a generic counter.

Counters. Asynchronous (ripple): T-FFs or JK toggles, clock of stage \(i+1\) is \(Q_i\). Simple, slow (ripple \(t_{pd}\)), nasty decoding glitches. Synchronous: all FFs share CLK; combinational next-state logic from present \(Q\). Binary up, down, up/down, modulo-\(N\) (detect \(N-1\) and clear, or design the state graph). BCD decade (74160/162). Load and enable pins. Deriving next-state bits: for a binary up-counter, \(D_0=\bar Q_0\), \(D_1=Q_1\oplus Q_0\), \(D_2=Q_2\oplus(Q_1Q_0)\), etc.

Finite-state machines. Moore: outputs are functions of state only. Mealy: outputs are functions of state *and* input (can be faster by one cycle, can glitch when inputs change). Design procedure: (1) word spec, (2) state diagram, (3) state table, (4) state assignment (binary, Gray, one-hot), (5) pick FF type, (6) excitation maps, (7) output maps, (8) implement, (9) check unused states (lock-out: do they enter the valid cycle?). One-hot: one FF per state, next-state logic is almost the diagram drawn in gates; uses more FFs, fewer gates, easy FPGA mapping.

Asynchronous sequential circuits (fundamental mode): no clock; inputs change one at a time; state is feedback through delay. Races, cycles, essential hazards. UG treatment is brief: avoid them unless you are building an SR latch on purpose. Synchronise external inputs to the clock.

Reset: asynchronous \(\overline{CLR}\) pin vs a synchronous reset term in the next-state logic. Power-on reset must put the FSM in a legal state. Unused states of a 3-FF machine that only uses 5 of 8 codes should be specified (recover to idle, or don't-care if you accept a possible lock-out).

Shift-register applications that exams like: serial adder (two shift registers, a full adder, a carry FF), sequence detector as an FSM or as a shift register plus combinational decode, and a ring counter as a one-hot state register. Time-division multiplexing of a 7-segment display is a counter plus a MUX; the counter is this unit, the MUX is the previous unit.

Clock-domain crossing in one paragraph: if two FFs have unrelated clocks, a single-bit signal must be synchronised (two FFs) on the receiving clock; a multi-bit bus must use a handshake or a FIFO with gray pointers. Do not sample a multi-bit async bus with one FF bank.

## Equations

Characteristic equations:

\[
Q^+=D\qquad\text{(D-FF)},
\]

\[
Q^+=J\bar Q+\bar K Q\qquad\text{(JK)},
\]

\[
Q^+=T\oplus Q\qquad\text{(T)}.
\]

Clock period (max-delay constraint):

\[
T_{clk}\ge t_{cq}+t_{pd,\mathrm{comb}}+t_{su}+t_{\mathrm{skew}}.
\]

Hold:

\[
t_{cd,FF}+t_{cd,\mathrm{comb}}\ge t_h+t_{\mathrm{skew}}.
\]

Synchronous binary up-counter next bit:

\[
D_i=Q_i\oplus \prod_{k=0}^{i-1} Q_k.
\]

Modulus of a Johnson counter of length \(n\): \(2n\). Maximal LFSR: \(2^n-1\).

Moore output: \(Y=g(Q)\). Mealy: \(Y=g(Q,X)\).

## Methods

1. Latch vs FF: if the question says "transparent" or "level", it is a latch. If it says "edge" or shows a triangle clock, it is a FF. Do not clock a latch's enable with the same edge you meant for a FF.
2. Excitation tables: from \(Q\to Q^+\) decide required \(D\) or \(J,K\) or \(T\). Don't-cares in JK (\(J\times\) when \(Q=1\) and we want 1) are the usual K-map gift.
3. Counter from spec: draw the cycle of states, assign codes, fill \(Q^+\) columns, K-map each \(D_i\) (or \(T_i\)).
4. FSM: prefer Moore if outputs must be glitch-free and aligned to the clock; Mealy if you need an output in the same cycle as an input. Never let a Mealy output drive a second FSM's clock.
5. Timing: identify the longest combinational path between FFs, including \(t_{cq}\) of the launching FF. For hold, identify the *shortest* path (often Q back to D of a neighbouring bit with almost no logic).
6. Unused states: for a self-starting requirement, map every unused code to a used state (usually idle).

## Mistakes

- Using \(SR=11\) on a NOR latch and then claiming a defined state.
- Calling a gated latch a flip-flop. A 7475 is a latch; a 7474 is an edge-triggered FF.
- JK toggle: forgetting that \(J=K=1\) toggles *per clock*, not continuously like an analog astable.
- Ripple counter decoded with combinational AND: the outputs are skewed, so the AND glitches. Use a synchronous counter, or strobe the decode.
- Hold time: adding wait states or slowing \(f_{clk}\) to "fix" a hold violation. That never helps.
- Metastability: "one FF will clean up an async input." One FF *samples* it; two in series (same clock) are the synchroniser.
- Mealy output used as a clock. Any input glitch clocks the next bank.
- State assignment: using binary count order on a machine whose transitions are not counting, then wondering why the next-state logic is huge. Gray or one-hot can shrink logic.
- Forgetting asynchronous reset polarity (\(\overline{CLR}\) active low).
- Mod-10 counter that counts 0–10 (eleven states). Mod-10 is 0–9.

State encoding trade-offs, with numbers. A 6-state Moore machine: binary encoding uses 3 FFs and typically messy next-state logic; Gray encoding of a nearly-linear sequence reduces toggling and sometimes literals; one-hot uses 6 FFs and next-state equations that look like the diagram (OR of predecessor-and-condition terms). FPGAs are FF-rich, so one-hot is the default in many RTL guides. Discrete TTL labs with four 7474s still use binary encoding.

Switching a ripple counter into a clock tree is a standard "why did my decode glitch" lab. The LSB FF changes first; the MSB last. A NAND that looks for 1111 sees 0111, 0011, etc. on the way. Synchronous design: all bits change from the same edge, so the decode is still combinational-hazard-prone *within* \(t_{pd}\) of that edge, but a following FF that samples after the decode has settled will not see the glitch if setup is met.

Debounce of a mechanical switch: an SR latch (cross-coupled NAND) with the SPDT switch as S and R is the hardware debounce. An RC plus Schmitt is the other. Sampling a bounce with a 1 kHz MCU poll is the firmware debounce. Do not clock a counter directly from a raw push-button.

Sequential logic is combinational logic plus a clock discipline. Write the next-state function, meet setup and hold, and specify every unused state. If an input is asynchronous, draw two FFs before you draw anything clever. If a path is too slow, cut combinational logic or slow the clock. If a path is too fast (hold), add delay on *that* path — never a slower clock. A lab counter that "skips" counts is often a hold-time failure on the LSB-to-next-bit path, not a Boolean error. Add a pair of inverters as delay on that path or use a part with a longer \(t_{cq,\min}\). Unused-state lock-out in a Johnson counter is a real lab: if two 1s appear after a glitch, the cycle is no longer 2n. A reset that loads 000...01 (ring) or 000...0 (Johnson) at power-up is the fix, not hope. Self-starting FSMs map every unused code; lazy don't-cares are allowed only if the question says so.
