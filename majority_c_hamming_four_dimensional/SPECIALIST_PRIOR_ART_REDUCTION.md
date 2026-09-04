# Specialist prior-art reduction for the Hamming star constructions

This note sharpens the literature boundary of the balanced-rectangle and
all-large three-box results.  It gives an exact specialization of a published
prescribed-centre star theorem, then identifies the established hyperstar
framework containing the three-box problem.

## 1. The anchored rectangle is a Cameron--Horsley corollary

Fix (sge2), (1le a,b<s), and put

\[
 M=s+a,\qquad N=s+b,\qquad ab=sq+\tau,
 \qquad 0\le\tau<s.
\]

Let

\[
 x=a+q,\qquad f=s-q.
\]

Choose arbitrarily (x) vertices on the (M)-side of (K_{M,N}), and
choose arbitrarily (	au) vertices on the (N)-side.  Prescribe

- one star of size (s) at each of the (x) chosen (M)-side vertices;
- one star of size (s+1) at each of the (	au) chosen (N)-side
  vertices; and
- one star of size (s) at every other (N)-side vertex.

No star is prescribed at the remaining (f=M-x=s-q) vertices on the
(M)-side.

Cameron and Horsley's Theorem 2 gives necessary and sufficient cut
inequalities for a multigraph to have a star packing with prescribed centres
and sizes.  In the present instance every active centre carries one star, so a
restriction function simply selects some active centres.  Suppose it selects

\[
 i\text{ of the }x\text{ row centres},\qquad
 j_1\text{ large column centres},\qquad
 j_0\text{ ordinary column centres},
\]

and write (j=j_0+j_1).  Its prescribed demand is

\[
 s(i+j)+j_1.
\]

The number of edges of (K_{M,N}) incident with at least one selected centre
is

\[
 iN+jM-ij.
\]

Thus the theorem's cut slack is

\[
 D=iN+jM-ij-s(i+j)-j_1
   =i(b-j)+aj-j_1.                                      \tag{1}
\]

If (j\le b), then

\[
 D\ge aj-j_1\ge j-j_1\ge0.
\]

If (j>b), the coefficient of (i) in (1) is negative and (i\le x), so

\[
\begin{aligned}
 D&\ge x(b-j)+aj-j_1\\
  &=(a+q)b-qj-j_1\\
  &=q(N-j)+\tau-j_1\ge0.                              \tag{2}
\end{aligned}
\]

The total prescribed demand is

\[
 xs+Ns+\tau
 =s(a+q+s+b)+\tau
 =(s+a)(s+b)=MN.
\]

Hence the packing supplied by Cameron--Horsley is a decomposition.  Every
edge incident with one of the (f\ge1) uncentred rows must lie in its column
star.  Consequently every column star contains every uncentred row.  In
particular, the size-(s+1) stars have a common transversal row.

This proves the anchored balanced-corner lemma used in the all-large
three-box construction.  It also strengthens its placement clause: the
(	au) large column centres can be **any prescribed (	au)-subset** of the
(N) columns, not merely a cyclic interval.  Exact (s)-strips recover the
arbitrary rectangle (m,n\ge s).

The conclusion is a scope correction.  Existence of the balanced and anchored
rectangle decomposition is a direct corollary of the published
prescribed-centre theorem.  The elementary cyclic marking algorithm remains a
useful closed-form witness, but the existence statement itself should not be
presented as candidate-new.

## 2. The three-box problem lies in Lonc's hyperstar framework

Let (X,Y,Z) be disjoint sets of sizes (m,n,p).  Identify a cell
((x,y,z)) with the hyperedge ({x,y,z}) of the complete three-partite
three-uniform hypergraph

\[
 \mathcal H=X\mathbin{\ast}Y\mathbin{\ast}Z.
\]

A coordinate-line part is exactly a hyperstar whose centre is one of the
pairs

\[
 \{x,y\},\qquad \{x,z\},\qquad \{y,z\}.
\]

Lonc's 1987 theorem, restated as Theorem 4.2 in Roberts' dissertation, gives
a Hall-type necessary-and-sufficient criterion for decomposing an arbitrary
hypergraph into hyperstars with a prescribed centre family
(mathcal C) and prescribed positive sizes (delta(C)).  With

\[
 \mathcal C\subseteq (X\times Y)\cup(X\times Z)\cup(Y\times Z),
\]

its three conditions specialize to:

1. every cell contains at least one candidate centre;
2. (sum_{C\in\mathcal C}\delta(C)=mnp); and
3. for every (mathcal T\subseteq\mathcal C), the number of cells all of
   whose candidate centres lie in (mathcal T) is at most
   (sum_{C\in\mathcal T}\delta(C)).

This is precisely Hall feasibility for assigning each cell to one eligible
pair-centre slot.  If (delta(C)) is a sum of allowed class sizes, the
assigned hyperstar at (C) can then be split arbitrarily into coordinate-line
parts of those sizes.

The theorem does **not** by itself select a centre family or capacities that
maximize the number of parts subject to the lower bound (s).  The
all-large three-box theorem supplies such a selection constructively: its
aligned donor exchange realizes every Euclidean carry while keeping every
part of size (s) or (s+1).  Thus the responsible candidate-new scope is
the universal quotient formula for (m,n,p\ge s), its closed-form cross-slab
witness, and the Hamming consequence--not a general hyperstar feasibility
criterion.

## 3. Consequences for the two immutable graph contributions

- Height 2057: the balanced and anchored rectangle *existence* statements
  are classical corollaries after the specialization (1)--(2).  The explicit
  cyclic certificate, sharp thin-coordinate optimum, boundary-crossing
  obstruction, and nonlinear Hamming separation remain the contribution's
  substantive content.
- Height 2077: the coordinate-line problem is an instance of Lonc's fixed-data
  hyperstar framework.  The universal all-large capacity choice and explicit
  carry exchange are not stated by that framework and remain the narrowly
  scoped candidate-new claims, pending independent review.

This note is a literature-scope correction and reduction, not an independent
review of either contribution.

## Primary sources

1. Rosalind A. Cameron and Daniel Horsley, *Decompositions of complete
   multigraphs into stars of varying sizes*, Journal of Combinatorial Theory,
   Series B 145 (2020), 32--64, Theorem 2,
   <https://arxiv.org/abs/1807.10738>.
2. Zbigniew Lonc, *Decompositions of hypergraphs into hyperstars*, Discrete
   Mathematics 66 (1987), 157--168,
   <https://doi.org/10.1016/0012-365X(87)90128-2>.
3. Dan Roberts, *Stars and Hyperstars*, Auburn University dissertation
   (2012), Theorem 4.2 and its Hall-theorem explanation,
   <https://holocron.lib.auburn.edu/handle/10415/3193>.

## Trust boundary

The reduction is a human proof using the exact published cut and Hall
criteria.  The accompanying checker exhausts all restriction-count types for
small corners and audits the extremal reduction of every cut inequality over a
larger range.  Exact integer computation corroborates (1)--(2); it neither
proves the cited theorems nor replaces the universal symbolic argument.
