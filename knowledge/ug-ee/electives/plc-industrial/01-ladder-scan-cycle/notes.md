# PLC scan cycle, ladder logic, timers and counters

A programmable logic controller is a rugged computer that repeatedly reads field inputs, evaluates a Boolean program, and writes field outputs. This unit is the scan, ladder contacts and coils, and the standard timer/counter types as taught in a UG EEE elective. It is study-level: paper ladders and scan arithmetic. It is not a vendor certification, not IEC 61131-3 copied from the standard, and not a live write to plant hardware (out of product).

## Concepts

A PLC cycle is **scan**: (1) copy physical inputs into an input image table, (2) execute the user program from top to bottom (or as the IEC task model says, one evaluation of the POU), (3) copy the output image table to physical outputs, (4) housekeeping / communications. Some platforms insert a “force” table or a watchdog kick. The **scan time** \(T_s\) is the duration of one pass. A 1 ms scan on a small brick PLC is common; a large program plus analog math can be 20–100 ms. I/O that changes faster than \(T_s\) can be missed (aliasing of a pulse). Input filters (hardware RC or a digital debounce of several scans) deliberately ignore sub-millisecond bounce.

**Watchdog:** if a scan exceeds a configured limit (infinite loop, overloaded Ethernet), the CPU faults and typically de-energizes outputs to a programmed fail-safe. That is why scan-time budgets belong in the design, not only in the exam.

**Ladder logic** is a graphic Boolean language that looks like a relay schematic. Power rails left and right. A **normally open** (NO) contact of tag `Start` conducts when the tag is 1. A **normally closed** (NC) contact of `Stop` conducts when `Stop` is 0. Series contacts are AND; parallel rungs or parallel branches are OR. A **coil** on the right sets an output bit for this scan (and thus the physical output at the end of scan, unless immediate I/O is used). Rung example: motor seal-in
\[
(\mathrm{Start}\lor \mathrm{Run})\land \lnot\mathrm{Stop}\land \mathrm{OK}\ \Rightarrow\ \mathrm{Run}.
\]
`Start` is a momentary pushbutton; `Run` feeds back so the motor stays on after Start is released; `Stop` is usually an NC contact in the ladder (and often an NC *field* device — see the next unit on fail-safe). Order of rungs matters: a coil used as a contact later in the same scan sees the *new* value; a coil used above sees the previous scan’s value. That is the PLC analog of sequential Boolean evaluation, not simultaneous circuit physics.

**Output types:** coil `-() -` sets the bit to the rung condition (unconditional rewrite every scan — do not also set it on another rung without understanding last-wins). **Set/latch** `- (S) -` and **reset/unlatch** `- (R) -` are sticky: S turns on and stays on until R, even if the S rung goes false. Two rungs fighting S and R in the same scan: last instruction wins. **One-shot / rising-edge** (ONS, PLS, `P` contact): true for one scan when the condition rises. Use it to increment a counter from a maintained level, or to run a state once.

**Immediate I/O** instructions read or write a physical point mid-scan, skipping the image table. They break the “all inputs frozen” model; use them for a fast abort bit, not for every contact.

IEC 61131-3 also names FBD, ST, IL, SFC. UG EEE exams still draw ladders. SFC (sequential function chart) is the clean way to write a cycle of states; a ladder with a dozen latches is the messy way. Mention SFC; write ladders here.

**Timers.** Time bases 1 ms, 10 ms, 100 ms, 1 s depending on the family. **TON** (on-delay): when the in-rung (IN) is true, ACC increments by scan or by a clock; when ACC \(\ge\) PRE, the done bit DN is true. If IN goes false, ACC and DN clear (non-retentive). The output coil of a motor-start delay sits on DN. **TOF** (off-delay): DN is true while IN is true *and* for PRE after IN falls; used to keep a fan running after a motor stops. **RTO** (retentive on-delay): ACC holds across IN false; a separate reset (RES) clears it. Use RTO for “run hours” or a delay that must survive a momentary IN dip.

Timer resolution versus scan: ACC typically updates once per scan or on a time-base tick. A TON with PRE \(=1.000\,\mathrm{s}\) and \(T_s=8\,\mathrm{ms}\) done-flag appears between 1.000 and \(1.000+T_s\) after IN. Do not promise 1.000000 s on a 8 ms scan. If PRE is not an integer number of time bases, the firmware rounds.

**Counters.** **CTU** counts rising edges of CU up to PRE, then DN. **CTD** counts down. **CTUD** both. RES clears ACC. Overflow/underflow bits on some platforms. A CTU on a field photocell with bounce will over-count unless a one-shot plus debounce is used. High-speed counter (HSC) hardware on the CPU counts pulses far above \(1/T_s\) (encoders); ordinary CTU cannot.

**Compare and math:** `ACC >= PRE` is already DN; extra GE/LE boxes compare integers or analog scaled values. Do not use floating compare for “equals” on a process variable.

**Interlocks in ladder (preview of unit 02):** a coil that starts a motion should include series NC contacts of the opposing motion, a guard-closed NO, and an NC e-stop already in the input image. Software interlocks *supplement* hardwired safety; they do not replace a safety relay or a SIL-rated loop on a press.

**Memory:** bits (I, Q, M, or vendor I/O addresses like `%IX0.0`, `I:1/0`), timers/counters as structures (EN, TT, DN, ACC, PRE), retentive vs non-retentive files. After a power cycle, retentive bits and RTO ACC come back; non-retentive coils do not. That is why a dangerous actuator should not be retentive-on.

Scan versus real time: a ladder is not a continuous differential equation. A PID instruction (if present) is a discrete controller with \(T=T_s\) or a periodic task. That link is the digital-control pack; here, just remember that TON is not an analog RC.

This unit’s exam jobs: write a seal-in, pick TON vs TOF vs RTO, compute scans in a delay \(N=\mathrm{PRE}/T_s\), CTU DN after PRE edges, and state that live plant writes are out of scope for this handbook.

## Equations

Scan budget:
\[
T_s=T_{\mathrm{in}}+T_{\mathrm{prog}}+T_{\mathrm{out}}+T_{\mathrm{house}}.
\]
Missed-pulse risk: a pulse narrower than \(T_s\) (plus input filter) may not appear in the image.

TON done time:
\[
t_{\mathrm{DN}}\in[\mathrm{PRE},\ \mathrm{PRE}+T_s]
\]
after IN rises (time-base quantization extra). Number of scans in a delay:
\[
N=\mathrm{ceil}(\mathrm{PRE}/T_s).
\]

Seal-in:
\[
\mathrm{Run}^+=( \mathrm{Start}\lor \mathrm{Run})\land \overline{\mathrm{Stop}}\land \mathrm{Permissives}.
\]
(The \(+\) means next image.)

CTU:
\[
\mathrm{ACC}\leftarrow\mathrm{ACC}+1\text{ on rising CU},\quad \mathrm{DN}=(\mathrm{ACC}\ge\mathrm{PRE}).
\]

Watchdog fault if \(T_s>T_{\mathrm{WD}}\).

## Methods

To interpret a ladder: evaluate left to right, top to bottom, using the input image and any coils already assigned *this* scan. Write a truth table for a 2–3 contact rung if stuck.

To build a start/stop station: NO Start in parallel with Run, both in series with NC Stop (and permissives), coil Run. Stop must dominate: if both buttons are pressed, Stop’s NC is open (if Stop is 1). Confirm the field Stop is wired so that a broken wire looks like Stop=1 or like a de-energized loop — next unit.

To pick a timer: delay on start \(\to\) TON. Delay on stop \(\to\) TOF. Accumulate run time \(\to\) RTO + RES. Convert PRE to the time base (1.5 s with 10 ms base \(\to\) PRE=150).

To count boxes on a conveyor: debounce the photoeye (TON 20 ms or a 4-scan filter), then a rising one-shot into CTU. PRE = batch size; DN starts the next state.

To estimate whether a 5 ms pulse is visible: if \(T_s=8\,\mathrm{ms}\) and no HSC, it may be missed. Solution: hardware latch, HSC, or faster task.

To avoid double-coil: search the program for the same Q address. Last rung wins; the first coil is a ghost.

When documenting: tag names, PRE values, and the scan time belong on the drawing. A ladder without PRE is not a specification.

Study-only execution: draw the ladder, simulate scan-by-scan on paper with a table of bits versus scan index. Do not download to a live motor from this product.

## Mistakes

Thinking all contacts on a rung see simultaneous physics like a relay schematic. They see the image and sequential assignment.

Using a TON as if PRE were analog-RC accurate to microseconds on a 10 ms scan.

TOF with PRE measured from IN *rising* (it is from falling).

RTO without a RES, then wondering why the second cycle finishes immediately.

CTU on a level (not edge): ACC races through PRE in a few scans.

Two coils of the same output on two rungs.

Seal-in with Stop as an NO contact in series (the motor then runs only while Stop is pressed).

Retentive coil on a hydraulic solenoid: after power-up the actuator moves.

Immediate writes sprinkled everywhere, then non-reproducible races.

Watchdog disabled “so the program can be long.”

IEC ST `IF` without an `ELSE` that clears a coil — the coil then sticks like a forgotten latch.

Treating this handbook as permission to actuate a plant. Live PLC writes are out of Arc (`docs/CANNOT_DO.md` CD-PLC).
