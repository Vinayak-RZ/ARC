# Block reduction and Mason gain

Classical loop algebra is bookkeeping: series, parallel, and feedback of transfer functions, plus a small set of block-diagram moves that keep the same \(Y/U\). When the diagram grows loops inside loops, signal-flow graphs and Mason’s gain formula compute the same TF without drawing twenty equivalent diagrams. This unit is those reductions, the associated sign conventions, and the mistakes that swap a minus into a plus and invert a stability conclusion.

## Concepts

A block \(G(s)\) is a directed SISO operator on Laplace signals, \(Y=GU\), valid at zero state. A summing junction outputs the algebraic sum of incoming signals with the signs written on the arrows. A takeoff (pickoff) copies a signal to two destinations without loading: unlike a circuit node, a takeoff does not split current; both copies equal the original. That is why block diagrams are not circuit diagrams.

Three primitive connections, all with compatible dimensions (UG: scalars):

Series (cascade): \(G_2\) after \(G_1\) gives \(G_2 G_1\). In SISO the product commutes as functions of \(s\), but the drawing order is still \(G_1\) then \(G_2\). In MIMO, \(G_2 G_1\neq G_1 G_2\) in general.

Parallel: two blocks driven by the same input, outputs summed, give \(G_1+G_2\) (watch the summing signs).

Negative unity feedback around a forward \(G\) with a feedback \(H\) gives the closed-loop
\[
T=\frac{G}{1+GH}
\]
from reference to output if the summer is \(E=R-HY\). Positive feedback is \(1-GH\) in the denominator. UG default is negative feedback; a missing minus sign on the summer is the most expensive error in the course.

Moving a summing junction past a block, or a takeoff past a block, requires inserting extra copies of that block or its inverse so that every path still sees the same operators. Example: moving a summer from the output side of \(G\) to the input side replaces an added \(D\) at the output by an added \(G^{-1}D\) at the input, which is legal only if \(G\) is invertible (biproper, minimum-phase in the rational sense). Prefer not to invert plants; move takeoffs in the direction that multiplies by \(G\), not by \(1/G\).

Unity-feedback reduction: any \(H\) in the return path can be absorbed by defining \(L=GH\) and redrawing as unity feedback around \(L\) with a prefilter \(1/H\) if the output is still \(Y\), or by keeping \(T=G/(1+GH)\) and stopping. Do not “replace \(H\) by 1” without adjusting \(G\).

Inner loops first. A minor-loop rate feedback inside a position loop is reduced to one equivalent forward block, then the outer loop is closed. Nested reduction is ordinary algebra if each inner closed loop is well-defined (no algebraic loop with loop gain 1 at \(s=\infty\)). Algebraic loops occur when a loop of biproper blocks has no delay: the equation for the loop signal is implicit. Strictly proper plants break algebraic loops. PID in cascade with a strictly proper plant is well-posed; two biproper blocks in a loop may not be.

Signal-flow graphs (SFG): nodes are signals, directed branches are TFs. A source node has only outgoing branches. Mason’s rule sums over forward paths from input node to output node, each weighted by a cofactor of the graph determinant. The graph determinant is
\[
\Delta=1-\sum L_i+\sum L_i L_j-\sum L_i L_j L_k+\cdots
\]
where \(L_i\) are loop gains, and the products run over pairwise nontouching loops (no shared node), then triples, and so on. The cofactor \(\Delta_k\) of forward path \(k\) is \(\Delta\) with every loop touching that path deleted. Then
\[
T=\frac{1}{\Delta}\sum_k P_k\Delta_k.
\]
A loop gain is the product of branch TFs around a closed directed cycle, including the summing signs (a negative branch is a factor \(-1\)). Touching is about nodes, not about crossing on a messy drawing.

Mason and block reduction must agree. Use Mason when there are several overlapping loops; use elementary reduction when the diagram is a single loop or a cascade of obvious series/parallel pieces. Do not mix a half-reduced diagram with a half-Mason sum.

Load disturbance and reference are different inputs. The TF from \(R\) to \(Y\) is \(T=G_c G/(1+G_c G H)\) in the usual 1-dof loop. The TF from a disturbance adding at the plant output is \(1/(1+G_c G H)\). Sensitivity \(S=1/(1+L)\) and complementary sensitivity \(T=L/(1+L)\) with \(L=G_c G H\) satisfy \(S+T=1\) for this loop. That identity is a reduction check: if your two TFs do not add to 1, a sign or a missing loop is wrong.

Two-degree-of-freedom: a prefilter \(F\) on the reference and a feedback \(H\) give \(Y=F G/(1+GH) R\) in the simplest split. Do not absorb \(F\) into \(G\) if a later question asks for the disturbance TF, which does not see \(F\).

Positive vs negative: if the physics of the plant already includes a minus (inverting amplifier, 180° of process), the summer may be drawn as \(+\). Stability formulas still use the loop gain as actually connected. Write \(L\) as the product around the loop including every minus, then the characteristic equation is \(1-L_{\mathrm{open\,around}}=0\) in SFG language, or \(1+G_cG=0\) in the standard negative-unity-feedback language. Name which convention you are in.

## Equations

Series: \(G_{\mathrm{eq}}=G_2 G_1\). Parallel: \(G_{\mathrm{eq}}=G_1+G_2\).

Negative feedback:
\[
\frac{Y}{R}=\frac{G}{1+GH},\qquad \frac{E}{R}=\frac{1}{1+GH},\qquad L=GH.
\]
Positive feedback: replace \(+\) by \(-\) in the denominator.

Sensitivity / complementary:
\[
S=\frac{1}{1+L},\qquad T=\frac{L}{1+L},\qquad S+T=1.
\]

Mason:
\[
T=\frac{\sum_k P_k\Delta_k}{\Delta},\qquad
\Delta=1-\sum_i L_i+\sum_{i,j}^{\mathrm{nontouch}} L_i L_j-\cdots.
\]
\(\Delta_k=\Delta\) with loops touching \(P_k\) removed.

Characteristic equation of a well-defined loop: \(1+L(s)=0\) (negative unity-feedback convention).

Moving a takeoff after \(G\) to before \(G\): the extra branch must be multiplied by \(G\). Moving a summer from before \(G\) to after \(G\): the added signal is multiplied by \(G\).

## Methods

Label every signal once. Write the summer equation at each junction (\(E=R-Y\), \(U=G_c E\), \(Y=G U+D\), …). Eliminate algebraically. That is always legal and often faster than pictorial moves for a 6-block exam figure.

Pictorial recipe: (1) reduce inner cascades and parallels; (2) close the innermost loop; (3) repeat outward; (4) as a last resort, move a takeoff or summer, inserting \(G\) or \(G^{-1}\). Never move a summer through a takeoff without redrawing both.

SFG recipe: (1) one node per labelled signal; (2) branch TF equal to the block, with a \(-1\) branch for a subtracting input; (3) list every forward path product \(P_k\); (4) list every loop \(L_i\); (5) mark touching; (6) form \(\Delta\) and \(\Delta_k\); (7) sum. Count loops twice if you draw both a plus and a minus path that close; they are the same loop only if they use the same nodes.

Check by a special case: set every block to 1, read \(T\) off the diagram by thinking, and compare to the formula. For unity negative feedback with \(G=H=1\), \(T=1/2\). For two parallel forward paths of 1 with no loop, \(T=2\). For a single loop of gain \(L\) and one forward path equal to that loop’s open chain, Mason must return \(L/(1-L)\) in SFG signs (positive convention) or \(G/(1+G)\) in textbook negative feedback. Reconcile the sign of \(L\) before trusting a number.

Disturbance paths: put a source node on \(D\) and rerun Mason, or substitute in the labelled equations. Do not reuse \(Y/R\) for \(Y/D\).

When a block is a number \(K\), keep it symbolic until the last line. Cancelling a \(K\) in numerator and denominator of \(T\) can hide that \(K=0\) opens the loop.

For multi-loop diagrams from process control (inner flow loop, outer composition), reduce the inner loop to \(T_{\mathrm{inner}}(s)\) treating its set-point as the input, then that \(T_{\mathrm{inner}}\) is the “plant” of the outer loop. Sampling and delay in digital loops wait for unit 11; here every block is a rational (or \(e^{-sT}\) left intact).

If two answers are required, \(Y/R\) and \(U/R\), compute \(U=G_c E=G_c(R-HY)\) after \(Y\) is known, or keep \(U\) as a node in Mason.

## Mistakes

Writing \(G/(1-GH)\) for a diagram whose summer is drawn with a minus on the feedback triangle. Read the arrow sign, not the word “feedback.”

Treating a takeoff as a current divider. Both outgoing copies equal the source signal.

Moving a summer past a block and forgetting to multiply the added signal by that block, or multiplying by the inverse when the move did not require an inverse.

Using Mason with \(\Delta=1-\sum L_i\) but including products of touching loops in the next term. Touching loops do not enter the pairwise sum.

Dropping the minus on a feedback branch when forming a loop gain. A standard negative loop has \(L_{\mathrm{SFG}}=-GH\), then \(\Delta=1-(-GH)=1+GH\), and \(T=G/\Delta\). If you already put the minus in \(L=GH\) and also write \(\Delta=1-L\), you double the convention and get \(1-GH\).

Cancelling a pole of \(H\) against a zero of \(G\) inside \(L=GH\) and then using the reduced \(L\) to claim closed-loop pole locations. The closed-loop characteristic polynomial is \(1+GH\) times cancelled factors that still sit in the plant realization.

Adding the TFs of two cascaded blocks instead of multiplying.

Using \(S+T=1\) on a 2-dof controller with a prefilter and concluding the prefilter is 1. The identity is for the loop \(L\) as seen by the output complementary pair, not for \(Y/R\) when a prefilter sits outside.

Algebraic loop: closing \(K\) around a biproper \(C(s)\) with \(C(\infty)K=-1\) is ill-posed. If the exam diagram has only proper plants, you are safe; if it has \(D\neq 0\) blocks in a loop, check well-posedness.

Reporting the open-loop \(G\) as the closed-loop answer after a page of reduction. Box the requested TF (\(Y/R\), \(Y/D\), or \(E/R\)) in the last line.
