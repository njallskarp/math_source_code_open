# Planar second variation at a collinear equal-disk configuration

## Statement

Fix `R>0`, distinct real numbers

`a_1<...<a_N`,

and transverse offsets `y=(y_1,...,y_N) in R^N`.  Let

`D_i(y_i)={(x,z) in R^2:(x-a_i)^2+(z-y_i)^2<=R^2}`

and write

`A(y)=area(union_i D_i(y_i))`.

Put `g_i=a_(i+1)-a_i`, and let

`I={i: g_i<2R}`.

The graph on `{1,...,N}` with edge set `I` is a disjoint union of paths; call
its connected components the strict-overlap blocks.  Then `A` is real
analytic in a neighborhood of `0 in R^N`, it is even under simultaneous
reflection `y -> -y`, and

`A(y)=A(0)+sum_(i in I) w_i (y_(i+1)-y_i)^2+O(||y||^4),`                 (1)

where

`w_i=sqrt(R^2-g_i^2/4)/g_i>0`.                                         (2)

In particular, for every fixed `b in R^N`,

`A(epsilon b)=A(0)+epsilon^2 sum_(i:g_i<2R)
 sqrt(R^2-g_i^2/4) (b_(i+1)-b_i)^2/g_i+O(epsilon^4).`                  (3)

Thus the Hessian at the collinear configuration is twice the weighted path
Laplacian:

`D^2 A(0)[b,b]=2 sum_(i in I) w_i(b_(i+1)-b_i)^2`.                     (4)

Its kernel consists exactly of the vectors which are constant on every
strict-overlap block.  Gaps equal to `2R` correctly carry zero interaction:
transverse motion can only separate the tangent disks.

This is a local theorem at a fixed configuration.  The size of the analytic
neighborhood and the constant hidden in (1) may depend on `R`, the axial
coordinates, and `N`; no uniform assertion is made as a positive gap tends to
zero or to `2R`.

## Proof

### 1. Separation into strict-overlap blocks

If `g_i>2R`, the horizontal projections of disks with labels at most `i` and
at least `i+1` are disjoint.  If `g_i=2R`, those projections meet in only one
point, and the corresponding disks are tangent when their transverse offsets
agree and disjoint otherwise.  In either case the two sides have area-additive
unions for every `y`.  It is therefore enough to treat one block

`p,...,q`, with `g_i<2R` for `p<=i<q`.

For `x in [a_i-R,a_i+R]`, set

`r_i(x)=sqrt(R^2-(x-a_i)^2)`.

The vertical section of `D_i(y_i)` at `x` is the interval

`J_i(x,y_i)=[y_i-r_i(x),y_i+r_i(x)]`.

For a fixed adjacent pair in the block, on the compact common horizontal
support of the two disks the continuous function `r_i+r_(i+1)` has a strictly
positive minimum.  Indeed, it is positive in the interior, while at either
endpoint its nonzero summand equals `sqrt(g_i(2R-g_i))`.  Consequently there
is a neighborhood `U` of `0 in R^N` such that

`|y_(i+1)-y_i|<r_i(x)+r_(i+1)(x)`                                     (5)

whenever both adjacent disks are active at `x`.

At each `x`, the active labels in a block form a consecutive interval of
integers: if the horizontal supports of labels `i<k` contain `x`, so do the
supports of all intermediate labels.  Inequality (5) makes every two
consecutive active vertical intervals intersect.  Hence their union is a
single interval.  This is the point which permits an exact envelope formula,
rather than an outer-span bound.

### 2. The envelope formula

Let `X=[a_p-R,a_q+R]`, and interpret a maximum below as taken only over labels
whose horizontal support contains `x`.  Define

`M_y(x)=max_(p<=i<=q) (r_i(x)+y_i),`

`F(y)=integral_X M_y(x) dx`.

By the interval conclusion above, the upper endpoint of the union section is
`M_y(x)`.  The negative of its lower endpoint is

`max_i(r_i(x)-y_i)=M_(-y)(x)`.

Cavalieri's principle therefore gives the exact identity

`A_block(y)=F(y)+F(-y)`                                                (6)

throughout `U`.

At `y=0`, maximizing `r_i(x)` is the same as choosing the nearest axial
center.  The maximizer changes from `i` to `i+1` at

`c_i=(a_i+a_(i+1))/2`.

Only those two functions tie there, and their crossing is transverse.  If

`rho_i=sqrt(R^2-g_i^2/4),`

then

`r_i'(c_i)=-g_i/(2rho_i),    r_(i+1)'(c_i)=g_i/(2rho_i),`              (7)

so the derivative of their difference is `-g_i/rho_i`.

The implicit-function theorem supplies a real-analytic switch point `t_i(y)`
near `c_i`, characterized by

`r_i(t_i)+y_i=r_(i+1)(t_i)+y_(i+1)`.                                  (8)

These remain the only switches when `y` is sufficiently small.  For
completeness, away from small disjoint neighborhoods of the finitely many
`c_i`, the unperturbed winning radius has a positive margin over every other
active radius by compactness.  Near `c_i`, all nonadjacent radii retain a
positive deficit and the transverse crossing (7) gives the unique local
switch.  Shrinking `U` preserves the order of the switch points.  Thus, with
fixed exterior endpoints `t_(p-1)=a_p-R` and `t_q=a_q+R`, one has

`F(y)=sum_(i=p)^q integral_(t_(i-1)(y))^(t_i(y)) (r_i(x)+y_i) dx`.     (9)

The moving endpoints in (9) are analytic and stay away from the circle
endpoints.  The two square-root endpoint integrals are fixed constants plus
affine terms in `y`.  Hence `F`, and then (6), are real analytic near zero.

### 3. Computing the Hessian

It suffices to restrict to an arbitrary line `y=epsilon b`.  Write
`F_b(epsilon)=F(epsilon b)` and `t_i(epsilon)=t_i(epsilon b)`.  Differentiating
(9), the moving-boundary terms cancel pairwise because of (8), giving

`F_b'(epsilon)=sum_(i=p)^q b_i(t_i(epsilon)-t_(i-1)(epsilon)).`        (10)

A second differentiation gives

`F_b''(0)=sum_(i=p)^(q-1)(b_i-b_(i+1))t_i'(0).`                       (11)

Implicit differentiation of (8), followed by (7), yields

`t_i'(0)=rho_i(b_i-b_(i+1))/g_i`.                                    (12)

Substitution into (11) proves

`F_b''(0)=sum_(i=p)^(q-1) rho_i(b_i-b_(i+1))^2/g_i`.                 (13)

Equation (6) says

`A_block(epsilon b)=F_b(epsilon)+F_b(-epsilon)`.

All odd Taylor terms cancel.  Analyticity and (13) therefore give

`A_block(epsilon b)=A_block(0)+epsilon^2 sum_(i=p)^(q-1)
 rho_i(b_i-b_(i+1))^2/g_i+O(epsilon^4).`                             (14)

Summing (14) over the area-disjoint blocks proves (1)--(4).  Finally, every
weight in (2) is positive, so the quadratic form vanishes precisely when each
edge difference vanishes, equivalently when `b` is constant on each block.

## Checks and sharp features

1. **Two disks.**  For two centers at distance
   `s=sqrt(g^2+epsilon^2(b_2-b_1)^2)`, the exact union-area derivative with
   respect to `s` is `2sqrt(R^2-s^2/4)`.  Since
   `s-g=epsilon^2(b_2-b_1)^2/(2g)+O(epsilon^4)`, its quadratic coefficient is
   exactly `sqrt(R^2-g^2/4)(b_2-b_1)^2/g`, agreeing with (3).

2. **Translations.**  If `b` is constant on a block, that entire union is
   translated vertically and its area is unchanged.  Formula (4) detects
   exactly these modes.

3. **Tangency.**  When `g=2R`, transverse displacement changes the distance
   from `2R` to `sqrt(4R^2+epsilon^2 Delta b^2)>=2R`; no overlap is created.
   Treating tangencies as separators is therefore essential.

4. **Nonadjacent centers.**  They do not disappear by an estimate.  Rather,
   stability of the one-dimensional nearest-center envelope shows that they
   are not exposed at first or second order.  The resulting Hessian is sparse
   for a geometric reason.

## Literature context

The following primary sources were checked on 2026-09-03 after selecting the
target from the committed Discovery Net graph.

- B. Csikos, *On the Volume of the Union of Balls*, Discrete & Computational
  Geometry 20 (1998), 449--461,
  <https://doi.org/10.1007/PL00009395>, gives a first-variation formula for a
  smoothly moving union as a nonnegative linear combination of pair-distance
  derivatives.
- H. Edelsbrunner, *The Union of Balls and Its Dual Shape*, Discrete &
  Computational Geometry 13 (1995), 415--440,
  <https://doi.org/10.1007/BF02574053>, develops the Voronoi/dual-complex
  representation and metric formulas for finite ball unions.
- K. Bezdek and R. Connelly, *Pushing disks apart -- the Kneser--Poulsen
  conjecture in the plane*, Journal fur die reine und angewandte Mathematik
  553 (2002), 221--236, <https://arxiv.org/abs/math/0108098>, proves the
  qualitative planar union-area monotonicity under arbitrary expansions.

Those results provide the variation, dual-complex, and monotonicity context.
Targeted searches for an exact collinear transverse second variation, its
weighted path-Laplacian form, or the componentwise kernel classification did
not locate this statement.  This is only a search-relative novelty report, not
a priority claim.

## Trust boundary

The result is symbolic.  It uses elementary slice geometry, compactness,
Cavalieri's principle, the implicit-function theorem, and differentiation of
a finite moving-boundary integral.  No numerical experiment, solver, external
dataset, private state, or omitted certificate is used as evidence for the
universal statement.
