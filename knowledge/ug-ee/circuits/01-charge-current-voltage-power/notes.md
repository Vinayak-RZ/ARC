# Charge, current, voltage, power, energy

Undergraduate electrical engineering starts with four linked quantities. Charge is the conserved stuff that moves. Current is how fast it moves through a branch. Voltage is the energy difference per unit charge between two nodes. Power is the instantaneous rate at which that energy is delivered or absorbed, and energy is the time integral of power. Every later circuit method is a bookkeeping scheme for these four. This unit is the language of Basic Electrical Sciences and of network theory: SI units, the passive sign convention, ideal sources and resistors as accounting devices, and the difference between a physical field picture and a lumped circuit model.

## Concepts

Electric charge \(Q\) is measured in coulombs. The elementary charge is \(e = 1.602176634 \times 10^{-19}\,\mathrm{C}\). In lumped circuits we almost never count electrons; we treat charge as a continuous real variable that is conserved at every node. Kirchhoff's current law is that conservation statement once we define current as the time derivative of charge through a surface. A current of one ampere means one coulomb of charge crosses a chosen surface each second. Conventional current is the flow of positive charge; in metals the mobile carriers are electrons, so conventional current is opposite electron drift. Circuit diagrams, Ohm's law, and all later theorems use conventional current unless a device-physics chapter says otherwise.

Current may be constant (DC), time-varying but unidirectional, or alternating. Instantaneous current \(i(t)\) is a function; average current over an interval is the net charge transferred divided by the duration. The lumped-circuit hypothesis says the wavelength of the signals of interest is much larger than the physical size of the network, so a single \(i(t)\) describes a whole branch and a single \(v(t)\) describes a node pair. If that hypothesis fails, we leave this pack and enter distributed EM.

Voltage is not a property of a single wire. It is the line integral of electric field from one node to another, equal to the work per unit charge to move a test charge between those nodes when magnetic induction around the path is negligible (again the lumped assumption). We pick a reference node called ground and report other node voltages relative to it. Polarity marks on a source or a resistor are not decoration: reversing them reverses the algebraic sign of \(v\) in every equation that uses that element. An ideal independent voltage source maintains a prescribed \(v(t)\) regardless of the current through it. An ideal independent current source maintains a prescribed \(i(t)\) regardless of the voltage across it. Neither exists in hardware; they are models valid inside a limited operating region.

Power into a two-terminal element is \(p = vi\) only when \(v\) and \(i\) obey the passive sign convention: current enters the terminal marked positive. With that convention, \(p > 0\) means the element absorbs energy (resistor, charging capacitor, motor acting as a load). \(p < 0\) means the element delivers energy (source, discharging capacitor, regenerating machine). If a problem draws current leaving the plus terminal, either flip the current arrow or put a minus into \(p = vi\). Energy from \(t_1\) to \(t_2\) is \(\int_{t_1}^{t_2} p(\tau)\,d\tau\). For a resistor \(R\), \(p = i^2 R = v^2/R\) is never negative, so a positive resistance cannot be a net source of energy. For a capacitor, stored energy is \(\frac12 C v^2\); for an inductor, \(\frac12 L i^2\). Those stored-energy formulas assume linear time-invariant elements starting from a zero-energy origin.

Ideal wires have zero resistance and the same potential at every point of a connected node. Real wires have small series resistance and some inductance; we lump those parasitics into explicit elements when they matter. An open circuit is \(i = 0\) with voltage unconstrained by that branch. A short circuit is \(v = 0\) with current unconstrained by that branch. Connecting an ideal voltage source across a short, or an ideal current source across an open, produces a model contradiction: the circuit as drawn cannot exist, and the numerical solver will fail. Dependent sources (VCVS, VCCS, CCVS, CCCS) belong to the same accounting language; their controlling variables are voltages or currents elsewhere in the same network.

Units must stay SI: A, V, Ω, W, J, C, s. Prefixes (mA, kΩ, µF, mH) are converted before substitution. Charge on a capacitor is \(q = Cv\) only for a linear capacitor. Instantaneous power is not the same as average power; for DC they coincide, for AC they do not, which is why later units introduce RMS and complex power. Polarity of energy flow in a DC lab is as important as the numerical value: a supply that is actually absorbing current is operating in the second quadrant and must be rated for that.

A practical measurement reminder: ammeters go in series and ideally have zero burden voltage; voltmeters go in parallel and ideally draw zero current. Inserting them changes the circuit unless the instrument is much more ideal than the resistances around it. Wattmeters and energy meters combine both. None of that changes the definitions, but it is how the four quantities become numbers on a bench.

## Equations

Charge–current: \( i = \frac{dq}{dt},\quad q(t) = q(t_0) + \int_{t_0}^{t} i(\tau)\,d\tau \).

Voltage–energy: \( v = \frac{dw}{dq} \) along the lumped path, so \( p = \frac{dw}{dt} = v i \) under the passive sign convention.

Ohm (linear resistor): \( v = Ri \). Conductance \( G = 1/R \), \( i = Gv \).

Power forms: \( p = vi = i^2 R = v^2/R \) (resistor, PSC). Source delivering \( P_\mathrm{del} = -vi \) if PSC is drawn on the source.

Energy: \( w(t_1,t_2) = \int_{t_1}^{t_2} p(\tau)\,d\tau \). DC constant \( P \): \( W = P\Delta t \). Capacitor: \( w_C = \frac12 C v^2 \). Inductor: \( w_L = \frac12 L i^2 \).

Linear capacitor and inductor (preview of later units): \( i_C = C\frac{dv}{dt} \), \( v_L = L\frac{di}{dt} \).

SI consistency: \( 1\,\mathrm{W} = 1\,\mathrm{J/s} = 1\,\mathrm{V\cdot A} \), \( 1\,\mathrm{A} = 1\,\mathrm{C/s} \), \( 1\,\mathrm{V} = 1\,\mathrm{J/C} \).

Average of a periodic \( p(t) \) of period \( T \): \( P_\mathrm{avg} = \frac1T \int_0^T p(t)\,dt \). For DC this is just \( VI \).

## Methods

Name every node and every branch current before writing a single number. Draw polarity marks on every voltage you will use. State whether each element's current arrow obeys the passive sign convention. Convert all prefixes to SI. If the task is “find power absorbed by the 18 Ω resistor,” compute \( i \) or \( v \) for that resistor, then \( p = i^2 R \), and report the sign explicitly as absorbed (positive) or delivered (negative).

If charge is given as a waveform, differentiate to get current; if current is given, integrate and apply the initial charge. If energy and charge through a source are given, voltage is energy per coulomb only when those quantities refer to the same two terminals. For piecewise-constant DC intervals, energy is the sum of \( VI\Delta t \) over intervals, watching for times when current reverses.

When an ideal source and a resistor are in series, the resistor voltage is \( IR \) with polarity following the current into the resistor's plus mark; KVL then relates the source voltage to that drop. When they are in parallel, they share voltage and the source current splits according to KCL. Do not compute “power of the voltage source” as \( V^2/R \) unless the source's terminal voltage really is \( V \) and the entire current \( V/R \) leaves the source into that resistor alone.

Dimensional checks catch most early errors: current times voltage must be watts; charge times voltage must be joules. A numerical answer of 3.7 A for a power question is the wrong quantity even if the arithmetic that produced 3.7 was correct.

## Mistakes

Treating voltage as a node property without a reference, then adding voltages that do not share a loop. Using \( p = vi \) with current leaving the plus terminal and calling a source a load. Mixing electron flow with conventional current in KCL signs. Forgetting that \( q = \int i\,dt \) needs a constant of integration. Reporting RMS or average power in a DC problem that asked for instantaneous power at a labeled instant. Using milliamps and kilohms together without converting, which silently drops a factor of one thousand. Claiming a capacitor “dissipates” \(\frac12 Cv^2\) as heat; that energy is stored, not dissipated, unless a resistor is present. Shorting an ideal voltage source or opening an ideal current source in a sketch and then trusting the solver. Copying textbook default polarities when the figure in the assignment used the opposite marks. Confusing energy in kilowatt-hours (utility billing) with energy in joules without the factor \( 1\,\mathrm{kWh} = 3.6\,\mathrm{MJ} \). Reporting a current as “flowing through a voltage” without naming the branch; current is a through variable of a branch, voltage is an across variable of a node pair, and mixing those words is how polarity errors start.
