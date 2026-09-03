# Exact weighted-MST formula and deficit bounds for collinear ball unions

## Target and scope

Fix integers `d>=1` and `N>=1`.  Let `B(x,R)` be the closed Euclidean ball
of radius `R>0` centered at `x in R^d`, and write `kappa_j` for the volume
of the unit ball in
`R^j`, with `kappa_0=1`.  The Kneser--Poulsen conjecture asserts that a
pairwise contraction of the centers of congruent balls cannot increase the
volume of their union.

This note treats configurations whose centers are collinear.  The qualitative
inequality in this case already follows from Bezdek--Naszódi's theorem for
strong contractions.  The new content pursued here is an exact representation
of the union volume by a truncated radial minimum-spanning-tree functional,
together with explicit two-sided deficit and equality criteria.

For `s>=0`, define the cutoff density

\[
 h_{d,R}(u):=
 \begin{cases}
 \kappa_{d-1}\left(R^2-u^2/4\right)^{(d-1)/2},&0\leq u<2R,\\
 0,&u>2R,
 \end{cases}                                         \tag{1}
\]

where its value at `u=2R` is immaterial, and put

\[
 \Phi_{d,R}(s)
 :=\int_0^s h_{d,R}(u)\,du
 =\kappa_{d-1}\int_0^{\min\{s,2R\}}
       \left(R^2-\frac{u^2}{4}\right)^{(d-1)/2}\,du.  \tag{2}
\]

Equivalently,

\[
 \Phi_{d,R}(s)
 =2\kappa_{d-1}\int_0^{\min\{s/2,R\}}
       (R^2-v^2)^{(d-1)/2}\,dv.                       \tag{3}
\]

This function is nondecreasing, strictly increasing on `[0,2R]`, constant
on `[2R,infinity)`, and

\[
 \Phi_{d,R}(0)=0,
 \qquad
 \Phi_{d,R}(2R)=\kappa_dR^d.                          \tag{4}
\]

For a labelled finite configuration `x=(x_1,...,x_N)`, let

\[
 \operatorname{MST}_{\Phi}(x)
 :=\min_T\sum_{\{i,j\}\in E(T)}
       \Phi_{d,R}(\|x_i-x_j\|),                       \tag{5}
\]

where the minimum is over all spanning trees on the labels.  Repeated centers
are allowed and simply create zero-weight edges.

## Exact representation theorem

### Theorem 1

If `x_1,...,x_N` lie on a line in `R^d`, then

\[
 \boxed{
 \operatorname{vol}_d\!\left(\bigcup_{i=1}^N B(x_i,R)\right)
 =\kappa_dR^d+\operatorname{MST}_{\Phi}(x).
 }                                                     \tag{6}
\]

More explicitly, choose scalar coordinates and sort them with repetitions as

\[
 a_1\le a_2\le\cdots\le a_N.
\]

Then

\[
 \operatorname{vol}_d\!\left(\bigcup_iB(x_i,R)\right)
 =\kappa_dR^d+\sum_{j=1}^{N-1}\Phi_{d,R}(a_{j+1}-a_j), \tag{7}
\]

and the adjacent-label path is a minimum spanning tree for the weights (5).

#### Proof: analytic cross-sections

Identify the line of centers with the first coordinate axis.  At axial
coordinate `t`, every ball has a `(d-1)`-dimensional centered-ball section;
because these sections have the same center in the perpendicular hyperplane,
their union is the largest one.  Thus the section of the full union has volume

\[
 f_{d,R}(\operatorname{dist}(t,A)),
 \qquad
 f_{d,R}(v):=
 \begin{cases}
 \kappa_{d-1}(R^2-v^2)^{(d-1)/2},&0\leq v<R,\\
 0,&v>R,
 \end{cases}                                         \tag{8}
\]

where `A={a_1,...,a_N}`.  This also covers `d=1` with
`kappa_0=1`; endpoint values have measure zero.

On the two exterior rays, the nearest-center distance runs once from `R` to
zero and once from zero to `R`.  Their combined contribution is

\[
 2\int_0^R f_{d,R}(v)\,dv=\kappa_dR^d.                \tag{9}
\]

In a gap of length `g=a_(j+1)-a_j`, the nearest-center distance rises from
zero to `g/2` and falls back to zero, with values beyond `R` contributing
nothing.  Hence this gap contributes

\[
 2\int_0^{\min\{g/2,R\}}f_{d,R}(v)\,dv=\Phi_{d,R}(g). \tag{10}
\]

Fubini's theorem and summation over the gaps prove (7).  Repeated centers have
`g=0` and make no contribution.

#### Proof: the spanning-tree identification

It remains to show that the adjacent path minimizes the transformed edge
weights.  For the prefix cut

\[
 \{a_1,\ldots,a_j\}\mid\{a_{j+1},\ldots,a_N\},
\]

every crossing edge has Euclidean length at least `a_(j+1)-a_j`.  Since
`Phi_(d,R)` is nondecreasing, the adjacent edge is a light edge of this cut.

For completeness, begin with any spanning tree.  If the `j`-th adjacent edge
is absent, add it and consider the resulting cycle.  The rest of the cycle
contains another edge crossing the prefix cut.  Replacing that edge by the
adjacent edge does not increase weight.  It cannot remove an adjacent edge
previously installed for a different prefix cut, because no such edge crosses
this cut.  Iterating over `j=1,...,N-1` converts the tree to the adjacent path
without increasing weight.  Therefore that path is an MST, and (6) follows
from (7).  QED

## Quantitative contraction theorem

Let `p=(p_1,...,p_N)` and `q=(q_1,...,q_N)` be two labelled collinear
configurations, not necessarily on the same line, and suppose `q` is a
pairwise contraction of `p`:

\[
 b_{ij}:=\|q_i-q_j\|\le
 a_{ij}:=\|p_i-p_j\|\qquad(1\le i,j\le N).            \tag{11}
\]

For an edge `e={i,j}`, put

\[
 D_e:=\Phi_{d,R}(a_{ij})-\Phi_{d,R}(b_{ij})
 =\int_{b_{ij}}^{a_{ij}}h_{d,R}(u)\,du.               \tag{12}
\]

### Theorem 2 (MST deficit sandwich)

Let `T_p` be any MST for the `p`-weights in (5), and `T_q` any MST for the
`q`-weights.  Then

\[
 \boxed{
 \sum_{e\in E(T_p)}D_e
 \ \le
 \operatorname{vol}_d\!\left(\bigcup_iB(p_i,R)\right)
 -\operatorname{vol}_d\!\left(\bigcup_iB(q_i,R)\right)
 \ \le
 \sum_{e\in E(T_q)}D_e.
 }                                                     \tag{13}
\]

In particular, the middle term is nonnegative, proving Kneser--Poulsen for
arbitrary contractions between collinear configurations in every dimension.

#### Proof

Write `w_p(T)` and `w_q(T)` for the two transformed tree weights.  Pairwise
contraction and monotonicity of `Phi` imply `w_q(T)<=w_p(T)` for every tree.
By Theorem 1,

\[
 V(p)-V(q)=w_p(T_p)-w_q(T_q).                          \tag{14}
\]

The minimizing properties give

\[
 w_q(T_q)\le w_q(T_p),
 \qquad
 w_p(T_p)\le w_p(T_q).                                \tag{15}
\]

Substituting the first inequality into (14) gives the lower bound in (13),
and substituting the second gives the upper bound.  Formula (12) is the
integral definition (2).  QED

### Corollary 3 (linear stability in the overlap regime)

If every edge of some `p`-MST has original length at most `L<2R`, then

\[
 V(p)-V(q)
 \geq
 \kappa_{d-1}\left(R^2-\frac{L^2}{4}\right)^{(d-1)/2}
 \sum_{\{i,j\}\in E(T_p)}(a_{ij}-b_{ij}).             \tag{16}
\]

Indeed, the density in (12) is decreasing on `[0,2R]`, so it is bounded
below by its value at `L` along every relevant integration interval.  The
coefficient is positive.  Consequently the volume loss is strict whenever at
least one edge of that `p`-MST contracts strictly.

The complementary universal upper estimate is

\[
 V(p)-V(q)
 \leq \kappa_{d-1}R^{d-1}
 \sum_{\{i,j\}\in E(T_q)}(a_{ij}-b_{ij}),             \tag{17}
\]

since the density in (12) is at most `kappa_(d-1)R^(d-1)`.

### Corollary 4 (equality criterion)

Fix a `p`-MST `T_p`.  Equality `V(p)=V(q)` holds if and only if

1. `T_p` is also an MST for the `q`-weights; and
2. for every edge `{i,j}` of `T_p`, either `a_ij=b_ij` or `b_ij>=2R`.

To see this, decompose the nonnegative difference as

\[
 V(p)-V(q)
 =\bigl[w_p(T_p)-w_q(T_p)\bigr]
  +\bigl[w_q(T_p)-w_q(T_q)\bigr].                    \tag{18}
\]

Both brackets vanish exactly under the two stated conditions, because
`Phi` is strictly increasing below `2R` and constant from `2R` onward.

When a single labelled tree is an MST for both configurations, both sides of
(13) agree and the deficit is exactly the sum (12).  In particular this occurs
for order-preserving collinear contractions when the common adjacent-label
path is used, so the deficit bound is attained by a broad family rather than
only in a limiting case.

## Boundary and consistency checks

The proof is symbolic and uses no numerical inference.  Several limiting
cases independently audit the normalization:

- `d=1`: `Phi_(1,R)(s)=min(s,2R)`, so (7) is the standard length formula
  for a union of equal intervals.
- Coincident centers: every gap has length zero and (7) gives one ball,
  `kappa_d R^d`.
- Pairwise separated adjacent centers: if every gap is at least `2R`, each
  gap contributes `kappa_d R^d`, giving `N` disjoint balls.
- `N=2,d=3`: for `0<=s<=2R`,

  \[
  \Phi_{3,R}(s)=\pi\left(R^2s-\frac{s^3}{12}\right),
  \]

  so (6) gives
  `4*pi*R^3/3 + pi*(R^2*s-s^3/12)`, the usual two-sphere union formula.
- Differentiating (7) in an unsaturated ordered gap gives exactly the
  `(d-1)`-volume of the perpendicular midpoint section, as required by the
  geometric first variation.

## Literature and novelty status

Bezdek and Naszódi prove Kneser--Poulsen for strong contractions of translates
of unconditional convex bodies.  After independently aligning the two center
lines with one coordinate axis, every contraction between collinear
configurations is a strong contraction; therefore the qualitative consequence
of Theorem 2 is known.  Their proof uses one-dimensional sections and Fubini,
but does not state the exact collinear gap formula, the transformed-MST
identity, the deficit sandwich, or the equality/stability consequences above.

Targeted primary-source searches on 2026-09-03 for collinear Kneser--Poulsen,
minimum spanning trees, exact union-volume formulas, quantitative deficits,
and stability found no such formulation.  The exact quantitative theorem is
therefore graph-new and apparently literature-new relative to those searches;
no historical priority claim is made.

Primary sources:

- Károly Bezdek and Márton Naszódi, *The Kneser--Poulsen conjecture for
  special contractions*, Discrete & Computational Geometry 60 (2018),
  967--980, Theorem 1.3 and Section 4:
  <https://arxiv.org/abs/1701.05074>.
- Károly Bezdek, *Selected topics from the theory of intersections of balls*,
  Discrete Applied Mathematics 382 (2026), 60--82.
- James Melbourne, Tomasz Tkocz, and Błażej Tkocz, *Kneser--Poulsen phenomena
  for entropy*, International Mathematics Research Notices 2025(12), rnaf140:
  <https://doi.org/10.1093/imrn/rnaf140>.

## Natural next boundary

The identity relies on all perpendicular ball sections being concentric, which
is exactly the rank-one geometry of collinear centers.  For centers near a
line, the sections cease to be nested and the MST representation acquires
overlap-interaction errors.  A meaningful next analytic frontier would be a
dimension-uniform perturbative estimate controlling those errors by the
squared transverse displacement.  Merely extending the present proof to
other already-known strong contractions would duplicate the qualitative
literature rather than advance the graph.
