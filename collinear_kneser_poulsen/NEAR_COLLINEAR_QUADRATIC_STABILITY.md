# Quadratic transverse stability of collinear equal-ball unions

## Target and relation to the exact collinear formula

Fix `d>=2`, `N>=1`, and a ball radius `R>0`.  Write `m=d-1` and let
`kappa_m` be the volume of the unit ball in `R^m`.  Decompose the centers as

\[
 x_i=(a_i,y_i)\in\mathbb R\times\mathbb R^m,
 \qquad
 p_i=(a_i,0),                                         \tag{1}
\]

so `P=(p_i)` is the projection of `X=(x_i)` onto the distinguished line.
Assume throughout the main theorem that the axial coordinates `a_i` are
pairwise distinct, and put

\[
 g_{ij}=|a_i-a_j|>0,
 \qquad
 \delta_{ij}=\|y_i-y_j\|.                            \tag{2}
\]

For a center configuration `Z=(z_i)`, abbreviate

\[
 V_R(Z)=\lambda_d\!\left(\bigcup_i B(z_i,R)\right). \tag{3}
\]

The exact collinear weighted-MST theorem gives

\[
 V_R(P)=\kappa_dR^d+\operatorname{MST}_{\Phi}(P),    \tag{4}
\]

where

\[
 \Phi(s)=\kappa_m\int_0^{\min\{s,2R\}}
            (R^2-u^2/4)^{m/2}\,du.                  \tag{5}
\]

The question here is whether (4) remains quantitatively accurate under a
small transverse perturbation.  The answer is yes at quadratic order, with
an explicit finite-radius bound and no margin assumption at the tangency
threshold `2R`.

## Main theorem

### Theorem 1 (global projection bound, locally quadratic)

Under (1)--(3),

\[
 \boxed{
 0\le V_R(X)-V_R(P)
 \le
 m\kappa_m R
 \sum_{\substack{1\le i<j\le N\\ g_{ij}<2R}}
 \frac{(R+\delta_{ij})^{m-1}\delta_{ij}^{2}}{g_{ij}}.
 }                                                     \tag{6}
\]

Thus the exact rank-one formula has the error representation

\[
 V_R(X)=\kappa_dR^d+\operatorname{MST}_{\Phi}(P)+E_R(X),
 \qquad 0\le E_R(X)\le\text{the right side of (6)}.  \tag{7}
\]

There is no smallness condition on the transverse displacements.  For
`N>=2`, in the near-collinear regime, if

\[
 \gamma=\min_{i<j}g_{ij}>0,
 \qquad
 \Delta=\max_{i<j}\delta_{ij},                       \tag{8}
\]

then the simpler uniform consequence is

\[
 0\le E_R(X)
 \le m\kappa_mR(R+\Delta)^{m-1}
       \binom N2\frac{\Delta^2}{\gamma}.             \tag{9}
\]

If instead `max_i ||y_i||<=epsilon`, then `Delta<=2epsilon`, so the last
factor may be replaced by `4 epsilon^2/gamma` and `R+Delta` by
`R+2epsilon`.

### Lemma 2 (one-slice shell bound)

Let `0<=r<=s<=R` and `u,v in R^m`, and put `delta=||u-v||`.  Then

\[
 \lambda_m\bigl(B(u,r)\setminus B(v,s)\bigr)
 \le m\kappa_m(R+\delta)^{m-1}
       [\delta-(s-r)]_+,                             \tag{10}
\]

where `[z]_+=max(z,0)`.

#### Proof

The triangle inequality gives

\[
 B(u,r)\subseteq B(v,r+\delta).
\]

If `r+delta<=s`, the left side is zero.  Otherwise it is at most the
concentric-shell volume

\[
 \kappa_m\bigl((r+\delta)^m-s^m\bigr).
\]

The mean-value theorem bounds this by

\[
 m\kappa_m(R+\delta)^{m-1}(r+\delta-s),
\]

which proves (10).  QED

### Proof of Theorem 1

Slice perpendicular to the distinguished axis at coordinate `t`.  If
`|t-a_i|<=R`, the `i`-th ball has section

\[
 A_i(t)=B_m(y_i,r_i(t)),
 \qquad
 r_i(t)=\sqrt{R^2-(t-a_i)^2};                        \tag{11}
\]

otherwise its section is empty.  Whenever the slice is nonempty, choose an
index `j=j(t)` for which `|t-a_j|` is minimal among the centers having a
nonempty section.  Equivalently, `r_j(t)` is maximal.

The projected sections are concentric, so their union is
`B_m(0,r_j(t))`.  The perturbed union contains `A_j(t)`, which has the same
`m`-volume.  Therefore the slice excess is nonnegative and satisfies

\[
 \begin{aligned}
 0&\le
 \lambda_m\!\left(\bigcup_iA_i(t)\right)-\kappa_mr_j(t)^m\\
 &\le\sum_{i\ne j}
 \lambda_m\bigl(A_i(t)\setminus A_j(t)\bigr).        \tag{12}
 \end{aligned}
\]

Apply Lemma 2 to every summand, with `r=r_i(t)`, `s=r_j(t)`, and
`delta=delta_ij`.  It remains to integrate the positive parts in (10).

Fix a pair `i!=j`, write `g=g_ij`, and consider the half-line on which `j`
is axially at least as close as `i`.  If `z>=0` is the distance from `t` to
the midpoint `(a_i+a_j)/2` into this half-line, then, whenever both sections
are nonempty,

\[
 r_j(t)^2-r_i(t)^2=2gz.                              \tag{13}
\]

Since `r_i+r_j<=2R`,

\[
 r_j(t)-r_i(t)
 =\frac{2gz}{r_i(t)+r_j(t)}
 \ge\frac{gz}{R}.                                    \tag{14}
\]

Consequently, even after enlarging the actual Voronoi cell and overlap
interval to the whole half-line,

\[
 \int [\delta_{ij}-(r_j-r_i)]_+\,dt
 \le\int_0^\infty[\delta_{ij}-gz/R]_+\,dz
 =\frac{R\delta_{ij}^2}{2g}.                         \tag{15}
\]

For a fixed unordered pair, (15) applies once on each side of its axial
midpoint.  Hence its total contribution to the integral of (12) is at most

\[
 m\kappa_m(R+\delta_{ij})^{m-1}
 \frac{R\delta_{ij}^2}{g_{ij}}.                     \tag{16}
\]

If `g_ij>=2R`, the two axial sections never overlap except possibly on a
measure-zero slice, so that pair contributes nothing.  Sum (16) over the
remaining pairs and apply Fubini to obtain (6).  The lower bound follows
simultaneously from the first inequality in (12).  Equations (7) and (9)
then follow from (4) and the definitions.  QED

## Sharpness and the collision obstruction

The quadratic order and the inverse-gap degeneration are both genuine.
Take `N=2`, axial gap `g in (0,2R)`, and transverse separation `eta`.  The
actual center distance is `sqrt(g^2+eta^2)`, and the exact two-ball formula
(5) gives

\[
 \begin{aligned}
 V_R(X)-V_R(P)
 &=\Phi(\sqrt{g^2+\eta^2})-\Phi(g)\\
 &=\frac{\kappa_m(R^2-g^2/4)^{m/2}}{2g}\,\eta^2
   +O_{d,R,g}(\eta^4).                               \tag{17}
 \end{aligned}
\]

Thus neither a uniform `o(eta^2)` estimate nor removal of all inverse-gap
dependence is possible.

If the axial gap is zero, the behavior changes order.  Two coincident
projected centers separated transversely by `eta` satisfy

\[
 V_R(X)-V_R(P)=\Phi(\eta)
 =\kappa_mR^m\eta+O_{d,R}(\eta^3).                  \tag{18}
\]

Positive axial separation is therefore essential for a uniform quadratic
theorem.  This is the exact pivot obstruction anticipated in the research
milestone.  By contrast, no exclusion around `g=2R` is needed: a pair with
`g>=2R` has disjoint axial supports and contributes identically zero.

## A robust Kneser--Poulsen certificate

The projection estimate can be combined with the collinear deficit theorem.
Let

\[
 A_i=(a_i,u_i),\quad B_i=(b_i,v_i),\qquad
 \bar A_i=(a_i,0),\quad\bar B_i=(b_i,0),             \tag{19}
\]

with distinct axial coordinates in each configuration.  Suppose `bar B` is
a pairwise contraction of `bar A`.  Let `C_R(B)` denote the right side of
(6), formed from the `b_i,v_i`.  Then

\[
 V_R(A)-V_R(B)
 \ge V_R(\bar A)-V_R(\bar B)-C_R(B).                \tag{20}
\]

Indeed, Theorem 1 gives `V_R(A)>=V_R(bar A)` and
`V_R(B)<=V_R(bar B)+C_R(B)`.  Hence any exact or lower MST bound for the
projected collinear deficit that dominates `C_R(B)` certifies
`V_R(B)<=V_R(A)`.  In particular, if `B` is also a contraction of `A`, this
is an explicit sufficient condition for the Kneser--Poulsen conclusion in a
noncollinear neighborhood of the rank-one case.

## Validation and boundary checks

The argument is entirely symbolic; no numerical evidence is used.

- **Dimensions:** both sides of (6) have units `length^d`.
- **Common transverse translation:** if all `y_i` are equal, every
  `delta_ij=0`; `X` is a translate of `P`, and both sides of (6) vanish.
- **Planar case:** when `d=2`, `m=1`, the shell bound reduces to the exact
  one-dimensional fact that shifting a shorter interval can expose at most
  twice the excess shift beyond the radius difference.
- **Separated axial supports:** `g_ij>=2R` gives no common nonempty slice,
  justifying the restricted sum in (6).
- **Two-ball audit:** (17) follows independently by Taylor expansion of the
  exact center-distance formula and confirms quadratic order and `1/g`.
- **Degenerate audit:** (18) proves the theorem cannot extend uniformly to
  colliding axial projections.
- **No hidden tangency hypothesis:** the proof becomes easier, not singular,
  when an axial gap reaches `2R`.

## Literature scope

Csikos proved a general first-variation formula for unions of moving balls
and, in Lemma 5.2 of his 1998 paper, a local quadratic upper bound on a
*possible volume increase under a contraction* when all pairwise center
distances stay uniformly positive.  That lemma has the form
`V(Q,r)-V(P,r)<=c||P-Q||^2` when `Q` contracts `P`; it does not bound the
positive projection loss `V_R(X)-V_R(P)` treated here, nor give (6), its
pairwise inverse-gap weights, or the sharp transition (17)--(18).

Bezdek--Naszodi's strong-contraction theorem already implies the qualitative
inequality `V_R(P)<=V_R(X)` because projection to the axis is a coordinatewise
contraction.  The slice proof above recovers that direction directly and adds
the explicit upper estimate.

Targeted searches on 2026-09-03 found no statement of (6), (7), the sharp
inverse-gap asymptotic, or certificate (20).  Novelty is search-relative; no
historical priority claim is made.

Primary sources:

- B. Csikos, *On the Volume of the Union of Balls*, Discrete & Computational
  Geometry 20 (1998), 449--461, especially Lemma 5.2,
  <https://doi.org/10.1007/PL00009395>.
- K. Bezdek and M. Naszodi, *The Kneser--Poulsen conjecture for special
  contractions*, Discrete & Computational Geometry 60 (2018), 967--980,
  Theorem 1.3 and Section 4, <https://arxiv.org/abs/1701.05074>.

## Natural next boundary

The bound solves the nondegenerate transverse-stability milestone.  It is
already localized to the axial overlap graph `g_ij<2R`; the next structural
question is whether that graph can be replaced by the adjacent axial
Voronoi path or another sparse Delaunay-type subgraph without losing
validity.  That would change the possible `N^2` dependence rather than merely
optimize the dimensional constant.  A family in which every overlapping pair
contributes independently at quadratic order would be a decisive obstruction
and a reason to pivot to a new graph-first analytic target.
