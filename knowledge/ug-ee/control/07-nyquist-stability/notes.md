# Nyquist stability: encirclements and N=Z−P

The Nyquist criterion counts closed-loop RHP poles from the image of the standard D-contour under \(L(s)\). It is the frequency-domain theorem that justifies Bode margins, and it is the only UG tool that stays honest when the open loop is unstable or non-minimum phase. This unit is the contour, the argument principle, \(N=Z-P\), indentations around \(j\omega\) poles, and how to read \(N\) off a polar plot of \(L(j\omega)\).

## Concepts

Cauchy’s argument principle: as \(s\) traverses a simple closed contour \(\Gamma\) clockwise or counterclockwise once, the image \(F(\Gamma)\) encircles the origin \(Z-P\) times in the same sense, where \(Z\) and \(P\) are the numbers of zeros and poles of \(F\) inside \(\Gamma\) (multiplicities included), assuming no zeros or poles on \(\Gamma\). Control uses \(F=1+L\), whose zeros are closed-loop poles and whose poles are open-loop poles.

The Nyquist D-contour runs up the \(j\omega\) axis from \(-j\infty\) to \(+j\infty\), indented into the RHP around \(j\omega\)-axis poles of \(L\) (so those poles are not inside \(\Gamma\)), and closes with a large RHP semicircle \(|s|\to\infty\). For strictly proper \(L\), the large arc maps to 0. The contour is traversed so that the RHP is to the left in some books (counterclockwise D) and to the right in others; UG courses almost all use the D-contour that encloses the entire RHP in the clockwise sense or counterclockwise — **the sign of \(N\) must match the book’s sense**. The formula used here, and in most EE exam keys, is
\[
Z=P+N
\]
where \(N\) is the net number of clockwise encirclements of the critical point \(-1+j0\) by the image \(L(\Gamma)\), \(P\) is the number of open-loop RHP poles, and \(Z\) is the number of closed-loop RHP poles. (If a course counts counterclockwise encirclements as positive, then \(Z=P-N_{ccw}\).) Stability requires \(Z=0\).

Because \(L(\bar{s})=\overline{L(s)}\) for real-rational \(L\), the plot for \(\omega:-\infty\to 0\) is the conjugate mirror of \(\omega:0\to+\infty\). Sketch the \(\omega\ge 0\) polar plot, mirror it, and connect through the infinite arcs from indentations.

Type \(r\ge 1\): poles at the origin. Indent the D-contour around \(s=0\) with a small RHP semicircle \(s=\varepsilon e^{j\theta}\), \(\theta:-\pi/2\to+\pi/2\) (clockwise indentation if the D-contour avoids the origin by going into the RHP). Then \(L(s)\approx K/s^r\) maps that small arc to a large arc of angle \(-r\times 180^\circ\) (clockwise for \(K>0\)). Type 1: a large \(-180^\circ\) clockwise semicircle at infinity connecting the \(\omega=0^-\) and \(0^+\) ends. Type 2: a full \(-360^\circ\) clockwise circle at infinity, and so on. Missing that arc is the classic “my type-2 Nyquist looks stable” error.

The critical point is \(-1\), not the origin, because we plot \(L\) rather than \(1+L\); encirclements of 0 by \(1+L\) are encirclements of \(-1\) by \(L\).

Open-loop unstable plants (\(P>0\)) can be closed-loop stable if \(N=-P\) in the clockwise convention, i.e. the plot must encircle \(-1\) counterclockwise \(P\) times. A single RHP pole typically needs a counterclockwise loop around \(-1\). Bode PM>0 is not sufficient.

Gain change: plotting \(L=K G\) and asking whether \(-1\) is encircled is the same as plotting \(G\) and asking whether \(-1/K\) is encircled. Root-locus \(K_u\) is the gain at which the plot passes through \(-1\).

Margins on the Nyquist plot: \(\omega_g\) is where \(|L|=1\) (unit circle); PM is the angle above the negative real axis at that intersection. \(\omega_p\) is where the plot crosses the negative real axis; GM is \(1/|L|\) there. Multiple crossings: the relevant margins are the ones closest to instability (smallest GM, smallest PM), and for complicated plots one should not summarize by a single PM.

Conditional stability: increasing gain can stabilize then destabilize (or the reverse). The polar plot can encircle \(-1\) for a middle band of \(K\). Routh ranges match.

All-pass and delay: \(e^{-sT}\) wraps the high-frequency tail around 0 in an ever-tighter spiral (delay) and can create infinitely many crossings of \(-180^\circ\). UG sketches stop at the first crossing unless the problem is a delay-margin question.

## Equations

Argument principle for \(F=1+L\) on the D-contour:
\[
Z=P+N_{\mathrm{cw}}(-1)
\]
(clockwise \(N\) of the \(-1\) point by \(L(\Gamma)\)). Closed-loop stable \(\iff Z=0\iff N_{\mathrm{cw}}=-P\).

Indentation at a pole of multiplicity \(r\) on the axis: small semicircle in the RHP maps under \(K/s^r\) to a large arc of \(r\times 180^\circ\) clockwise (\(K>0\)).

Polar coordinates: \(L(j\omega)=U(\omega)+jV(\omega)\), \(M=\sqrt{U^2+V^2}\), \(\phi=\mathrm{atan2}(V,U)\).

Unit-circle intersection: \(M(\omega_g)=1\). Negative-real crossing: \(V(\omega_p)=0\), \(U(\omega_p)<0\).

## Methods

Count \(P\) from the open-loop poles (Routh on the open-loop denominator, or factor). Sketch \(L(j\omega)\) for \(\omega=0^+\to\infty\): start (type, \(L(0)\)), end (\(L(\infty)=0\) for strictly proper), real-axis crossings (set \(\mathrm{Im}\,L=0\)), and whether the plot goes left of \(-1\). Mirror, add infinite arcs from type and from other \(j\omega\) poles. Count clockwise encirclements of \(-1\). Compute \(Z=P+N\).

If the sketch is ambiguous (passes near \(-1\)), compute the real-axis crossing exactly. For \(L=K/[s(s+a)(s+b)]\), the crossing is the same calculation as Routh \(K_u\).

To decide the sense of an arc at infinity: follow \(\omega=0^-\) to the indentation to \(\omega=0^+\) as the D-contour is traversed upward, and map with \(\angle(1/s^r)=-r\angle s\).

Stability design: require \(Z=0\). For \(P=0\), require \(N=0\), i.e. do not encircle \(-1\). Then PM and GM positive on a simple plot coincide with \(N=0\).

When \(L\) is not strictly proper, the large \(|s|\) arc of the D-contour maps to a finite arc of \(D+C B/s+\cdots\); include it.

## Mistakes

Using \(Z=P-N\) while counting clockwise encirclements (or the reverse). State the convention in one clause, then count.

Omitting the infinite semicircle for type 1 or type 2, and concluding \(N=0\) when the connection through infinity actually wraps \(-1\).

Indenting into the LHP around \(s=0\), which puts the origin pole inside \(\Gamma\) and changes \(P\).

Counting encirclements of the origin instead of \(-1\).

Setting \(P\) equal to the number of closed-loop RHP poles (that is \(Z\)).

Applying Bode “PM>0 ⇒ stable” to an open-loop unstable plant.

Forgetting to mirror the \(\omega<0\) plot: a spiral that looks like half an encirclement may complete a full encirclement with its conjugate.

Treating a pass through \(-1\) as a valid \(N\). That is the stability boundary (\(j\omega\) closed-loop root); \(N\) is not an integer in the argument principle hypotheses (pole/zero on \(\Gamma\)).

Confusing clockwise in the \(s\)-plane D-contour with clockwise in the \(L\)-plane. \(N\) is counted on the image.

Using polar plot scales that cannot resolve whether the crossing is at \(-0.9\) or \(-1.1\). Compute the crossing.

Delay spirals: stopping the sketch too early and missing an encirclement that appears only at high \(\omega\).

Worked polar construction for \(L=K/[s(s+1)]\). Write \(L(j\omega)=K/[j\omega(1+j\omega)]=K/(-\omega^2+j\omega)\). Multiply by the conjugate of the denominator: \(L=K(-\omega^2-j\omega)/(\omega^4+\omega^2)= -K/(\omega^2+1) - j K/[\omega(\omega^2+1)]\). Real part is always negative for \(K>0\); imaginary part is always negative for \(\omega>0\). The \(\omega=0^+\) start is \(\mathrm{Re}= -K\), \(\mathrm{Im}=-\infty\) (because of the type-1 pole). As \(\omega\to\infty\), \(L\to 0\) from the third quadrant. The plot is a curve in \(\mathrm{Re}<0,\mathrm{Im}<0\) approaching the origin. Mirror for \(\omega<0\) fills \(\mathrm{Im}>0\). The type-1 indentation adds a large clockwise semicircle from the \(\mathrm{Im}=+\infty\) end to the \(\mathrm{Im}=-\infty\) end, which *does* go through the RHP of the \(L\)-plane and *does* enclose the whole finite plane including \(-1\), unless we are careful: actually that large semicircle connects \(+j\infty\) to \(-j\infty\) clockwise, passing through the *positive* real infinity for \(L\sim K/s\)? \(L\approx K/s\) on \(s=\varepsilon e^{j\theta}\), \(L=(K/\varepsilon)e^{-j\theta}\), \(\theta:-\pi/2\to\pi/2\), \(-\theta:\pi/2\to-\pi/2\), from \(+j\infty\) to \(-j\infty\) through *positive* real infinity (\(K/\varepsilon>0\)). The infinite semicircle is in the right half of the \(L\)-plane and does **not** enclose \(-1\). Hence \(N=0\) for all \(K>0\), matching Routh on \(s^2+s+K=0\). The picture that students draw — a D-shape to the left of the origin — looks like it might wrap \(-1\); the missing infinite *right* semicircle (not left) is why \(N=0\). Type 1 with three poles, \(L\sim K/s^3\) near zero, would swing the infinite arc through \(r\times 180^\circ=540^\circ\) and then \(-1\) can be enclosed.

Counting \(N\) without a pretty picture: walk the image in the direction of increasing \(\omega\) from \(0^+\) to \(\infty\), then the mirror from \(-\infty\) to \(0^-\), then the indent arc. Keep a running winding number about \(-1\). A crossing of the ray \((-\infty,-1)\) upward (Im going from − to + while Re < −1) is typically a counterclockwise contribution, but the only reliable exam method is to mark arrows and actually count. If the plot passes through \(-1\), stop: that \(K\) is the stability boundary; do not assign an integer \(N\).

Open-loop unstable example to keep: \(L=K(s+2)/(s-1)\). \(P=1\). Closed loop \(1+L=(s-1+Ks+2K)/(s-1)=((1+K)s+(2K-1))/(s-1)\). For \(K>1/2\) the closed-loop pole is negative (and the leading coefficient \(1+K\neq 0\)). So \(Z=0\) requires \(N=-1\). The polar plot of \((j\omega+2)/(j\omega-1)\) is a circle (linear fractional transform of the \(j\omega\) axis); it must enclose \(-1\) counterclockwise once when \(K\) is large enough. Bode PM of this \(L\) can be quoted but is not a standalone stability test until \(P\) is counted.

The identity \(S+T=1\) still holds. Nyquist of \(L\) enclosing \(-1\) is Nyquist of \(S=1/(1+L)\) enclosing infinity, i.e. an unstable closed loop. Complementary sensitivity \(T=L/(1+L)\) then has RHP poles too. Robustness: a multiplicative plant uncertainty \(\Delta\) with \(|\Delta|\) small is tolerated when \(|T|\) is not huge; that is a high-frequency roll-off requirement, visible as \(L\) approaching 0 without wrapping \(-1\) again.
