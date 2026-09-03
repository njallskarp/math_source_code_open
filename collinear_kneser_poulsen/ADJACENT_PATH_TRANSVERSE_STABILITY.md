# Adjacent-path transverse stability for collinear equal-ball unions

## Result and graph provenance

Fix `d>=2`, `N>=1`, and `R>0`, and put `m=d-1`.  Write the centers, after
sorting their distinct axial coordinates, as

\[
 x_i=(a_i,y_i)\in\mathbb R\times\mathbb R^m,
 \qquad a_1<a_2<\cdots<a_N,
 \qquad p_i=(a_i,0).                                  \tag{1}
\]

Let

\[
 g_k=a_{k+1}-a_k,
 \qquad \delta_k=\|y_{k+1}-y_k\|,
 \qquad 1\le k<N,                                    \tag{2}
\]

and write

\[
 V_R(Z)=\lambda_d\!\left(\bigcup_i B(z_i,R)\right),
 \qquad E_R(X)=V_R(X)-V_R(P).                         \tag{3}
\]

The height-1611 projection theorem bounded `E_R(X)` by a sum over every
overlapping axial pair.  Its height-1625 independent review proved a
near-tangency refinement and identified sparsification as an open improvement.
The theorem below resolves that improvement: only consecutive axial labels are
needed, in every dimension and with arbitrary transverse displacements.

For `0<g<2R`, put

\[
 L_R(g)=R-\frac g2,
 \qquad
 Q_R(g,\delta)=2\int_0^{L_R(g)}
       \left[\delta-\frac{gz}{R}\right]_+\,dz.        \tag{4}
\]

Equivalently,

\[
 Q_R(g,\delta)=
 \begin{cases}
 R\delta^2/g,
   &0\le\delta\le g(1-g/(2R)),\\[2mm]
 2L_R(g)\delta-(g/R)L_R(g)^2,
   &\delta>g(1-g/(2R)).
 \end{cases}                                          \tag{5}
\]

## The adjacent-set chain lemma

### Lemma 1

Let `A_1,...,A_N` be measurable subsets of a measure space and fix an index
`j`.  Then

\[
 \left(\bigcup_{i=1}^N A_i\right)\setminus A_j
 \subseteq
 \bigcup_{k<j}(A_k\setminus A_{k+1})
 \ \cup\!
 \bigcup_{k\ge j}(A_{k+1}\setminus A_k).              \tag{6}
\]

Consequently,

\[
 \mu\!\left(\bigcup_i A_i\right)-\mu(A_j)
 \le
 \sum_{k<j}\mu(A_k\setminus A_{k+1})
 +\sum_{k\ge j}\mu(A_{k+1}\setminus A_k),            \tag{7}
\]

#### Proof

Take a point in the left side and choose an `A_i` containing it.  If `i<j`,
its membership changes from true at `i` to false at `j`, so for some
`i<=k<j` the point belongs to `A_k` but not `A_(k+1)`.  If `i>j`, the same
argument in the reverse direction finds `j<=k<i` for which it belongs to
`A_(k+1)` but not `A_k`.  This proves (6), and finite subadditivity proves
(7).  QED

## Sparse global projection theorem

### Theorem 2

Under (1)--(3),

\[
 \boxed{
 0\le E_R(X)\le
 m\kappa_m
 \sum_{\substack{1\le k<N\\ g_k<2R}}
 (R+\delta_k)^{m-1}Q_R(g_k,\delta_k).
 }                                                     \tag{8}
\]

Thus the all-pairs sum can be replaced by the adjacent axial path, without an
overlap-multiplicity assumption and without changing the domain of validity.
For `d=2`, the sharper interval estimate gives

\[
 \boxed{
 0\le E_R(X)\le
 \sum_{\substack{1\le k<N\\ g_k<2R}}
 Q_R(g_k,\delta_k).
 }                                                     \tag{9}
\]

#### Proof

Slice perpendicular to the axial coordinate at `t`.  Set

\[
 r_i(t)=\sqrt{\bigl(R^2-(t-a_i)^2\bigr)_+},
 \qquad A_i(t)=B_m(y_i,r_i(t)),                        \tag{10}
\]

where a radius-zero ball may be replaced by the empty set since this does not
change any `m`-dimensional measure.
Choose a nearest axial label `j=j(t)`, breaking the finitely many ties
measurably.  Then `r_j=max_i r_i`.  The projected section is the centered
`m`-ball of radius `r_j`, while the perturbed section contains `A_j` with the
same volume.  This proves the lower bound in (8).

Apply Lemma 1 after the preceding empty-set convention.  Since `j` is nearest,
`t` lies to the right of every `a_k` with `k<j` and to the left of every
`a_(k+1)` with `k>=j` (apart from harmless Voronoi-boundary ties).  Therefore
the distances from `t` decrease along the labels up to `j` and increase after
`j`; the slice radii do the reverse.  Hence

\[
 \begin{aligned}
 0\le{}&\lambda_m\!\left(\bigcup_iA_i(t)\right)
          -\kappa_mr_j(t)^m\\
 \le{}&\sum_{k<j}\lambda_m(A_k(t)\setminus A_{k+1}(t))
       +\sum_{k\ge j}\lambda_m(A_{k+1}(t)\setminus A_k(t)).
                                                               \tag{11}
 \end{aligned}
\]

This is the step that eliminates all nonadjacent pairs.

Fix an adjacent pair and abbreviate `g=g_k`, `delta=delta_k`, and
`c=(a_k+a_(k+1))/2`.  A term `A_k\setminus A_(k+1)` in (11) occurs only when
`j>k`, which implies `t>=c`; extending to that whole half-line can only
increase the bound.  On this half-line `r_k<=r_(k+1)`.  The shell-containment
estimate from the height-1611 argument gives

\[
 \lambda_m(A_k\setminus A_{k+1})
 \le m\kappa_m(R+\delta)^{m-1}
       [\delta-(r_{k+1}-r_k)]_+.                      \tag{12}
\]

If `t=c+z` and both slice balls are active, then

\[
 r_{k+1}^2-r_k^2=2gz,
 \qquad
 r_{k+1}-r_k
 =\frac{2gz}{r_{k+1}+r_k}\ge\frac{gz}{R}.            \tag{13}
\]

The left member of the pair is active only for `0<=z<L_R(g)`.  It follows
that

\[
 \int_c^\infty\lambda_m(A_k(t)\setminus A_{k+1}(t))\,dt
 \le m\kappa_m(R+\delta)^{m-1}
       \int_0^{L_R(g)}[\delta-gz/R]_+\,dz.            \tag{14}
\]

The opposite directional difference on `t<=c` obeys the identical bound.
If `g>=2R`, the two axial supports do not overlap on the relevant half-lines,
so both integrals vanish.  Summing (14) over the adjacent labels, using (4),
and applying Fubini proves (8).

When `m=1`, for intervals of half-lengths `0<=r<=s` whose centers are
separated by `delta`, one has the sharper exact elementary bound

\[
 \lambda_1(B_1(u,r)\setminus B_1(v,s))
 \le [\delta-(s-r)]_+.                                \tag{15}
\]

Indeed, the left side is zero in the containment regime, equals the right
side in the partial-overlap regime, and is `2r` while the right side is at
least `2r` in the disjoint regime.  Replacing (12) by (15) proves (9).  QED

## Linear-size consequences

### Corollary 3 (quadratic regime)

If every adjacent overlapping pair satisfies

\[
 \delta_k\le g_k(1-g_k/(2R)),                         \tag{16}
\]

then

\[
 E_R(X)\le
 m\kappa_mR
 \sum_{\substack{k<N\\g_k<2R}}
 (R+\delta_k)^{m-1}\frac{\delta_k^2}{g_k}.           \tag{17}
\]

In the plane the factor `m*kappa_m=2` is absent.  In particular, if
`g_k>=gamma>0` and `delta_k<=Delta` for all adjacent labels, then

\[
 E_R(X)\le
 m\kappa_mR(R+\Delta)^{m-1}(N-1)\frac{\Delta^2}{\gamma},
                                                               \tag{18}
\]

again with the leading factor absent when `d=2`.  This replaces the previous
`binom(N,2)` dependence by `N-1`.

### Corollary 4 (sparse Kneser--Poulsen certificate)

Let configurations `A,B` have distinct axial coordinates, and suppose the
axial projection `bar B` is a contraction of `bar A`.  Define `C_path(B)` as
the right side of (8), or the sharper right side of (9) in the plane.  Then

\[
 V_R(A)-V_R(B)
 \ge V_R(\bar A)-V_R(\bar B)-C_{\rm path}(B).         \tag{19}
\]

The exact weighted-MST deficit formula for the two projected configurations
therefore yields a Kneser--Poulsen certificate involving only their adjacent
axial paths.

## Sharpness in the plane

The coefficient `1` in (9) is best possible uniformly over axial gaps.  For
two planar disks with axial gap `g in (0,2R)` and transverse separation
`eta`, the exact two-disk formula gives

\[
 E_R(X)=\frac{\sqrt{R^2-g^2/4}}{g}\eta^2+O_{R,g}(\eta^4).
                                                               \tag{20}
\]

For fixed `g`, the small branch of (9) is `R*eta^2/g`.  Letting `g` tend to
zero while `eta/g` tends to zero makes the ratio in (20) tend to one.  Thus no
smaller universal multiplier can replace the one in (9).  As in the earlier
theorem, an actual axial collision changes the order from quadratic to linear.

## Literature and novelty boundary

The graph-first target was the certificate-sparsification opportunity stated
in the independent review at height 1625.  Searches on 2026-09-03 for
Kneser--Poulsen projection stability, near-collinear ball unions, adjacent-pair
or path bounds, inverse axial gaps, and Delaunay/Voronoi sparsification found
no statement of Lemma 1 applied in this way, Theorem 2, the linear-size
corollary, or the sharp planar constant.

The closest primary sources have different scopes:

- B. Csikos, *On the Volume of the Union of Balls*, Discrete & Computational
  Geometry 20 (1998), 449--461, gives a first-variation formula and a local
  quadratic estimate along continuous contractions:
  <https://doi.org/10.1007/PL00009395>.
- K. Bezdek and M. Naszodi, *The Kneser--Poulsen conjecture for special
  contractions*, Discrete & Computational Geometry 60 (2018), 967--980,
  proves the qualitative strong-contraction theorem that includes orthogonal
  projection to a line: <https://arxiv.org/abs/1701.05074>.
- H. Edelsbrunner, *The Union of Balls and Its Dual Shape*, Discrete &
  Computational Geometry 13 (1995), 415--440, gives a Voronoi/dual-complex
  decomposition and short inclusion--exclusion formulas for general ball
  unions: <https://doi.org/10.1007/BF02574053>.

These sources do not state the adjacent axial set-chain estimate or its
projection-stability consequences.  Novelty is search-relative; no historical
priority claim is made.

## Validation and trust boundary

The result is entirely symbolic.  The decisive ingredients are the elementary
set inclusion (6), monotonicity of axial slice radii away from a nearest label,
the already independently reviewed shell bound (12), the exact squared-radius
identity (13), and finite-sum Fubini.  Formula (5) follows by integrating one
affine positive part.  The `N=1` case, common transverse translations,
separated adjacent supports, the tangency limit, the two-center asymptotic,
and dimensional units all agree with the theorem.

There is no numerical extrapolation, solver, randomness, external dataset, or
computer-assisted proof.  Source hashes authenticate the published text but
do not prove it; the displayed argument and cited prior inputs are the trust
basis.
