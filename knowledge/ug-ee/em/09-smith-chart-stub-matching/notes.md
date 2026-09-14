# Smith chart and single-stub matching

The Smith chart is the complex plane of the reflection coefficient \(\Gamma\), labelled with the normalized impedance \( z=(1+\Gamma)/(1-\Gamma) \) as orthogonal circles. Moving along a lossless line is walking a constant-|\(\Gamma\)| circle through an electrical length \(\beta\ell\) (toward the generator, clockwise). Single-stub matching places a shorted or open stub a distance \( d \) from the load so that the admittance seen there plus the stub admittance equals \( 1+j0 \). This unit is graphical and algebraic matching at UG depth, not a full microwave CAD course.

## Concepts

Normalized \( z=Z/Z_0=r+jx \). \(\Gamma=(z-1)/(z+1)\). The chart’s outer rim is \( |\Gamma|=1 \) (pure reactance). The centre is \( z=1 \), match. Constant-\( r \) circles pass through \(\Gamma=1\). Constant-\( x \) arcs also through \(\Gamma=1\). The lower half is capacitive \( x<0 \), upper inductive \( x>0 \) (usual printed charts). Wavelengths toward generator (WTG) increase clockwise; toward load, counter-clockwise. A full lap is \( 0.5\lambda \) on the line (\( \Gamma \) repeats every \(\lambda/2 \), \( 4\pi \) in phase of \(\Gamma=|\Gamma|e^{-j2\beta\ell} \)).

Admittance chart: \( y=1/z \), which is \(\Gamma\) mapped through a 180° rotation (the same chart, read on the opposite point). Many stub problems are easier in \( y \): a shunt stub adds \( jb \) to \( y \). Series stubs add reactance to \( z \) and are less common in coax (harder to insert).

Single open or shorted shunt stub: (1) plot \( z_L \), (2) convert to \( y_L \), (3) rotate toward generator on the \(|\Gamma|\) circle until you hit the \( g=1 \) circle (there are two intersections), (4) that rotation is \( d/\lambda \), (5) at that point \( y=1+jb \), (6) the stub must present \( -jb \), (7) from the short (or open) on the chart, rotate until you read \( -jb \), that length is \(\ell_s\). Two solutions: the one with smaller \( d \) or smaller stub is often preferred (loss, bandwidth). Open stubs are convenient in microstrip (no via); shorted stubs in coax (plunger).

Quarter-wave transformer matches real loads only. A single stub matches a complex load using the extra degree of freedom \( d \). Double-stub matching (not required in every UG course) uses two fixed locations and varies both stubs — some loads remain forbidden.

VSWR is read from the \(|\Gamma|\) circle radius, or from the \( r \) where the circle crosses the real axis to the right of 1: that \( r_{\max}=s \).

Smith is a bilinear map: circles through circles. Impedance to admittance is a diameter flip. Adding a series \( jx \) moves you on a constant-\( r \) circle. Adding a shunt \( jb \) moves you on a constant-\( g \) circle on the admittance reading.

Numerical without a printed chart: compute \(\Gamma\), \( Z_{\mathrm{in}} \) from the tan formula, stub \( Z_{\mathrm{stub}}=j Z_0\tan\beta\ell \) or \( -j Z_0\cot \). The chart is the same arithmetic. Exams that forbid calculators still expect a sketched chart with labelled steps.

Bandwidth: a match at one frequency is not a match at another because \(\beta\ell\) and the load drift. Stub matches are narrower than a well-designed multi-section transformer. UG statement only.

## Equations

\[
\Gamma=\frac{z-1}{z+1},\qquad z=\frac{1+\Gamma}{1-\Gamma},\qquad y=1/z.
\]

Along a lossless line, toward generator a distance \(\ell\):

\[
\Gamma(\ell)=\Gamma_L e^{-j2\beta\ell}.
\]

Shunt combination: \( y_{\mathrm{tot}}=y_{\mathrm{line}}+y_{\mathrm{stub}} \). Match: \( y_{\mathrm{tot}}=1 \).

Shorted stub: \( y_{\mathrm{stub}}=-j\cot\beta\ell_s / Z_0 \) wait — normalized \( y_s=-j\cot\beta\ell \) for a shorted stub (because \( z_s=j\tan\beta\ell \), \( y_s=-j\cot\beta\ell \)). Open stub: \( z_s=-j\cot\beta\ell \), \( y_s=j\tan\beta\ell \).

Electrical length: \(\beta\ell=2\pi\ell/\lambda \). Chart rim is calibrated in \( \ell/\lambda \).

## Methods

Always state \( Z_0 \) and whether the stub is open or shorted. Normalize first. If using a chart, write down WTG readings as differences, not absolute labels, because charts differ in the zero of the scale (often a short is the left or the \(\Gamma=-1\) point).

Algebraic single-stub (shunt, shorted): require \(\mathrm{Re}\, y(d)=1\) for the admittance of the loaded line at \( d \), solve for \( d \), then \(\ell_s\) from \( \cot\beta\ell_s = -b \) (signs: \( y=1+jb \) needs stub \( -jb \)).

Check: after matching, \( |\Gamma| \) at the combination node is 0, VSWR=1 toward the generator. Between stub and load the VSWR is still that of \( Z_L \).

## Mistakes

Rotating toward the load when the problem asked input impedance (generator).

Reading \( z \) on an admittance problem without flipping 180°.

Shorted versus open stub formulas swapped (\( \tan \) vs \(\cot \)).

Adding stub length in metres without \(\lambda\) at the operating frequency.

Quarter-wave transformer on a complex \( Z_L \) without first cancelling the imaginary part.

Chart: using the “wavelengths toward load” scale while walking toward the generator.

Forgetting there are two \( g=1 \) intersections and reporting only one as “the” match.

A walk-through, algebraic, \( Z_0=50\,\Omega \), \( Z_L=100\,\Omega \) (real). \(\Gamma=(2-1)/(2+1)=1/3 \). VSWR=2. Single stub: \( y_L=0.5 \). Move \( d \) until \( g=1 \). For a real load \( r=2 \), the \( d \) to the \( g=1 \) circle is a standard result \( d=0.176\lambda \) or \( 0.324\lambda \) (from solving). Then \( b=\pm 0.5 \) roughly; a shorted stub of \( 0.176\lambda \) presents \( y=-j\cot(2\pi\times 0.176)=-j\cot 63.3^\circ=-j0.50 \). Verify with the tan formula in a numerical problem rather than memorizing 0.176.

Pure imaginary \( Z_L=j50 \), \( z=j \), \(\Gamma=j \), on the rim. A series \( -j50 \) would match; a shunt stub needs a length of line first to make \( g=1 \).

Input impedance: \( z_L=0.5-j0.5 \), 0.1\(\lambda\) toward generator. \( 2\beta\ell=72^\circ \), \(\Gamma_L=(z-1)/(z+1)\), multiply by \( e^{-j72^\circ} \), invert to \( z_{\mathrm{in}} \). That is the calculator path; the chart path is a 0.1λ clockwise slide.

Open stub \( \ell=\lambda/4 \): \( y_s=j\tan(\pi/2) \) blows up — a quarter-wave open is a short at the junction. Useful as a “ground” at RF.

50 Ω microstrip, stub 0.12\(\lambda\) open: \( y_s=j\tan(43.2^\circ)=j0.94 \). Cancels \( b=-0.94 \) of a line admittance.

Double-check power: matching is lossless (ideal stubs), so power into the matched port equals power into \( Z_L \) minus line/stub radiation and copper, which we set to zero.

Smith chart is not a field plot and not a Smiths of anything else. It does not replace Maxwell; it organizes \(\Gamma\).


Chart construction reminder: \(\Gamma_r+j\Gamma_i\), \( |\Gamma|\le 1 \) for passive \( r\ge 0 \). The bilinear map sends the right-half z-plane to the unit disk. Negative resistors (active, some tunnel-diode models) fall outside the chart; UG matching assumes passive loads.

Constant-Q contours and noise circles are RF-design extras. UG: r-circles, x-arcs, s-circles (constant VSWR), and the g=1 circle.

Single-stub algebraic outline for a real load \( r \) on a lossless line, shunt shorted stub. The admittance of a length \( d \) is \( y=\frac{r+j\tan\beta d}{1+jr\tan\beta d} \). Set real part 1, solve \(\tan\beta d\). Two real solutions in \( (0,\lambda/2) \). Then \( b=\mathrm{Im}(y) \), stub \(\cot\beta\ell=-b\) (shorted). This is what the chart is doing geometrically.

Double stub: two stubs a fixed \(\lambda/8\) or \( 3\lambda/8 \) apart. The forbidden region is a hole on the chart you cannot reach. If the load falls in the hole, add a line length or change spacing.

Lumped matching: L-section of one series and one shunt reactance. Two topologies depending on whether \( r_L>1 \) or \( <1 \). At one frequency this is equivalent to a stub of zero length plus a series element. Narrowband. Q of the match estimates bandwidth.

Microstrip open-stub end effect: the open is a bit longer electrically than the copper (fringing C). Design software compensates; a UG calculation using ideal \(\beta\ell\) is still the exam.

Worked chart-free match: \( Z_0=50 \), \( Z_L=50-j50 \), \( z=1-j \). \( y=1/z=0.5+j0.5 \). We need to walk until \( g=1 \). Use \( Z_{\mathrm{in}} \) formula as a function of \(\ell\), convert to y, seek \( g=1 \). At \(\ell=0\), \( g=0.5 \). At \(\ell=0.125\lambda \), \(\tan\beta\ell=1\), \( z_{\mathrm{in}}=\frac{(1-j)+j(1)}{1+j(1-j)}=\frac{1}{1+1+j}=0.5-j0.5 \) wait compute carefully on paper. The point is: do the arithmetic once slowly; the chart is a slide rule for that arithmetic.

Normalized current and voltage on the chart: some charts have overlay scales for \( V_{\min} \) location. A voltage minimum is where \( z \) is real and \( r=1/s \), the leftmost intersection of the VSWR circle with the real axis.

Toward generator clockwise is \( e^{-j2\beta\ell} \) on \(\Gamma\) if the printed chart’s angular scale matches. If your \(\Gamma\) rotation direction disagrees with a textbook figure, you used WTL instead of WTG.

A match does not change the load; it changes what the generator sees. The line between stub and load still has VSWR \( >1 \). High VSWR there means high peaks, possible breakdown or extra loss. Prefer the solution with smaller \( s \) on that segment if both matches are allowed — actually \( s \) on that segment is fixed by \( Z_L \); both solutions have the same \(|\Gamma_L|\). They differ in stub current and in bandwidth.

Cascade of two lines of different \( Z_0 \) is a bilinear chain; each junction has a \(\Gamma\). A quarter-wave transformer is one such junction pair. Binomial multi-section transformers flatten bandwidth (named only).

If the load is already \( 50\,\Omega \), the stub length for a shorted stub at the load would be 0 (no stub) or \(\lambda/2 \). Do not add a stub to a matched load “for luck.”

Smith chart is also a plot of impedance versus frequency if \( Z_L(f) \) traces a curve: that is a load-pull or crystal-resonator picture, out of UG scope except to say one frequency is one point.
