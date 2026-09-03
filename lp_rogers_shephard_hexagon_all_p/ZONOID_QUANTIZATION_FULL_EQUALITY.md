# Full planar symmetric Firey equality by slope-measure quantization

## Theorem

Let `1<p<infinity`, let `q=p/(p-1)`, and put

```text
c_q=2 Gamma(1+1/q)^2/Gamma(1+2/q).
```

If `K` is any full-dimensional planar convex body with a center of symmetry
and `0 in K`, then

```text
|K +_p (-K)|=(2+c_q)|K|                           (1)
```

if and only if `K` is a parallelogram having the origin as a vertex.

The new ingredient beyond the finite-polygon case is a two-sided,
constant-area shadow that replaces an arbitrary planar zonoid generating
measure by a finite monotone quantization.  It avoids any product of
generator-deletion factors and reduces a hypothetical nonpolygonal equality
case directly to the already excluded three-generator hexagon.

## 1. Equality propagates under a constant-area shadow

Write

```text
Phi_p(L)=|L +_p (-L)|.
```

We use three established facts.

1. If `{L_t}` is a shadow system along one line, then
   `{L_t +_p (-L_t)}` is a shadow system along that line.
2. The area of a planar shadow system is convex in its parameter.
3. Every centrally symmetric planar body `L` containing zero satisfies

   ```text
   Phi_p(L)<=(2+c_q)|L|.                            (2)
   ```

Consequently, suppose `{L_t}` is a shadow system on an interval containing
`0` in its interior, every `L_t` is centrally symmetric and contains zero,
and `|L_t|` is constant.  If `L_0` is an equality case in (2), then
`Phi_p(L_t)` is a convex function bounded above by the same constant and
attaining that bound at an interior point.  It follows that both endpoint
values, and in fact every value, attain equality.

## 2. A one-sided zonoid normal form at a face endpoint

First suppose that the origin is an endpoint of an exposed face of `K`.
Every centrally symmetric planar convex body containing zero is an
asymmetric `L_1`-zonoid.  Thus there is a finite positive generating measure
`mu` on `S^1` such that

```text
h_K(u)=integral_(S^1) <u,v>_+ dmu(v),
K=integral_(S^1) [0,v] dmu(v).                      (3a)
```

Choose coordinates so that the supporting face through the origin is
horizontal and `K` lies in the upper half-plane.  Since

```text
h_K(-e_2)=integral_(S^1) <-e_2,v>_+ dmu(v)=0,       (3b)
```

we have `v_2>=0` for `mu`-almost every generator.  The tangent mass, if
nonzero, combines into one segment `[0,h e_1]` with `h>0`: if both horizontal
orientations had positive mass, the origin would lie in the relative
interior rather than at an endpoint of the exposed face.  For every remaining
generator `v=(x,y)` with `y>0`, put `r=x/y` and push `mu` forward with density
`y`.  Since `[0,v]=y[0,(r,1)]`, this gives

```text
K=[0,h e_1] + integral_R [0,(r,1)] dnu(r),          (3)
```

where `h>=0`, `nu` is a finite positive Borel measure on `R`,

```text
M=nu(R)>0,
integral_R (1+|r|) dnu(r)<infinity.                 (4)
```

For a finite atomic measure, the planar zonotope determinant formula gives

```text
A(nu):=1/2 integral_R integral_R |r-s| dnu(r)dnu(s),
|K|=A(nu)+hM.                                      (5)
```

The same identity for an arbitrary `nu` satisfying (4) follows by discrete
approximation: the support functions converge uniformly, planar area is
Hausdorff-continuous, and the double integral is continuous under first-moment
approximation.  Equivalently, (5) is the standard two-dimensional zonoid
mixed-area formula.

The normal form (3) is a parallelogram with the origin as a vertex exactly in
the following full-dimensional cases:

```text
h=0 and supp(nu) has exactly two points, or
h>0 and supp(nu) has exactly one point.             (6)
```

The one-point case with `h=0` is degenerate.

## 3. The monotone quantization lemma

We isolate the continuum-to-polygon bridge.

### Lemma

Let `nu` satisfy (4) and suppose that `A(nu)>0`.  Fix `k>=2` such that
`supp(nu)` contains at least `k` points.  There are bounded nondecreasing
Lipschitz functions `T_n:R->R` such that

```text
A((T_n)_#nu)=A(nu),                                 (7)
```

and `T_n` converges in `L^1(nu)` to a nondecreasing `k`-step function `T`
whose `k` level sets all have positive `nu`-mass and whose levels are
distinct.  In particular,

```text
integral_R [0,(T(r),1)] dnu(r)
```

is a `k`-generator origin-vertex zonotope.

### Proof

Choose `k-1` non-atomic cut points dividing `R` into ordered intervals
`I_1,...,I_k` with masses `m_j=nu(I_j)>0`.  Choose real numbers
`q_1<...<q_k` and let `Q=q_j` on `I_j`.  Then `Q` is nondecreasing and

```text
d=A(Q_#nu)=sum_(i<j) m_i m_j(q_j-q_i)>0.            (8)
```

Replace each jump of `Q` by a linear transition on an interval shrinking to
the cut point.  This gives bounded nondecreasing Lipschitz functions `Q_n`
with `Q_n->Q` in `L^1(nu)`.  The inequality

```text
|A(S_#nu)-A(R_#nu)|
 <= M integral_R |S-R| dnu                          (9)
```

shows that `d_n=A((Q_n)_#nu)->d`.  For all sufficiently large `n`, set

```text
D=A(nu),
gamma_n=D/d_n,
T_n=gamma_n Q_n.                                   (10)
```

Then (7) holds exactly.  Also `gamma_n->gamma=D/d>0`, so
`T_n->T=gamma Q` in `L^1(nu)`.  The limiting levels remain distinct, and
each has mass `m_j>0`.  This proves the lemma.

## 4. Every quantization sits at the end of a two-sided shadow

Fix one of the Lipschitz maps `T_n` from the lemma, and denote a Lipschitz
constant by `L_n`.  For

```text
-epsilon_n <= t <= 1,
epsilon_n=1/(2(1+L_n)),
S_(n,t)(r)=(1-t)r+tT_n(r),                          (11)
```

the map `S_(n,t)` is nondecreasing.  Indeed, for `r<s` and
`-epsilon_n<=t<=0`,

```text
S_(n,t)(s)-S_(n,t)(r)
 >= (1-t)(s-r)+t L_n(s-r)>0,                        (12)
```

because at `t=-epsilon_n` the coefficient is
`1+epsilon_n-epsilon_n L_n=(3+L_n)/(2(1+L_n))>0`.
Monotonicity for `0<=t<=1` follows because (11) is a convex
combination of two nondecreasing maps.

Define

```text
K_(n,t)=[0,h e_1]
       + integral_R [0,(S_(n,t)(r),1)] dnu(r).      (13)
```

This is a shadow system along `e_1`.  To see it directly, index its points by
`a in [0,1]` and measurable selectors `f:R->[0,1]`.  Such a point has the
form

```text
a h e_1 + integral f(r)(r,1)dnu(r)
 + t e_1 integral f(r)(T_n(r)-r)dnu(r),             (14)
```

so every indexed point moves affinely parallel to `e_1`.

Because all maps in (11) preserve order, (5), (7), and linearity inside the
absolute value of each ordered pair give

```text
A((S_(n,t))_#nu)
 =(1-t)A(nu)+tA((T_n)_#nu)
 =A(nu).                                            (15)
```

The horizontal generator contributes `hM`, independently of all slopes.
Thus

```text
|K_(n,t)|=A(nu)+hM=|K|                              (16)
```

throughout the full interval.  Each body in (13) is full dimensional,
centrally symmetric, contains zero, and `K_(n,0)=K`.  Crucially, zero is an
interior parameter because `epsilon_n>0`.

## 5. Direct reduction of a nonpolygonal equality case to a hexagon

Assume that `K` in the normal form (3) attains equality.

If `h=0` and `K` is not a parallelogram, then `supp(nu)` contains at least
three points.  Apply the quantization lemma with `k=3`.  If `h>0` and `K` is
not a parallelogram, then `supp(nu)` contains at least two points; apply it
with `k=2`.

For every `n`, Section 1 applied to the two-sided constant-area shadow (13)
shows that its endpoint

```text
K_(n,1)=[0,h e_1]
       + integral_R [0,(T_n(r),1)] dnu(r)           (17)
```

is also an equality case.  Since `T_n->T` in `L^1(nu)`, their support
functions converge uniformly:

```text
sup_(u in S^1)|h_(K_(n,1))(u)-h_(K_T)(u)|
 <= integral_R |T_n-T| dnu ->0,                    (18)
```

where

```text
K_T=[0,h e_1]+integral_R[0,(T(r),1)]dnu(r).         (19)
```

Hausdorff continuity of Firey addition and planar area therefore passes
equality to `K_T`.  If the level sets of `T` have masses `m_j`, then

```text
K_T=[0,h e_1]+sum_(j=1)^k [0,m_j(t_j,1)],          (20)
```

where `t_1<...<t_k` are the distinct levels.

In the case `h=0,k=3`, (20) is a genuine three-generator centrally symmetric
hexagon with the origin as a vertex.  In the case `h>0,k=2`, its horizontal
generator and the two finite-slope generators again give a genuine
origin-vertex centrally symmetric hexagon.  The strict all-`p>1` hexagon
theorem rules out equality in both cases.  Hence every equality body having
the origin at a face endpoint must be one of the parallelograms in (6).

This argument is insensitive to whether the original generating measure is
atomic, continuous, or mixed.  In particular, it does not infer strictness
from polygonal approximation; equality itself is first propagated through a
two-sided shadow, and only then is the polygonal limit taken.

## 6. Reduction of every origin placement to the endpoint case

Let the original equality body be arbitrary.

If the origin is in its interior, translate the body along a generic line
over the maximal interval for which it continues to contain zero.  The
original placement is an interior point of a constant-area translation
shadow.  Section 1 propagates equality to both boundary placements.

If the origin lies in the relative interior of a nontrivial exposed face,
translate parallel to that face until the origin reaches either endpoint.
This is again a constant-area shadow with the original placement at an
interior parameter, so equality propagates to the endpoints.  If the exposed
face is a singleton or the origin is already an endpoint, no translation is
needed.

Section 5 now shows that the underlying shape is a parallelogram.  For a
parallelogram, an edge-interior origin is strict: after affine normalization
to

```text
P_a=[-a,1-a] x [0,1],  0<a<1,
```

its exact Firey deficit is the positive strict-hexagon deficit
`Delta_p(1-a,a)`.  An interior origin is also impossible: choose a generic
translation direction whose boundary contacts lie in edge interiors;
equality would propagate to those already excluded placements.  Therefore
the original origin must be a vertex.

Conversely, the sharp parallelogram computation gives equality whenever the
origin is a vertex.  This proves the theorem.

## 7. Why the finite deletion-factor obstruction disappears

For a polygonal generator deletion, convexity only gives

```text
delta_current >= lambda/(1+lambda) delta_endpoint,
```

and a product of these factors can vanish as the number of generators grows.
The present argument never multiplies deletion factors.  It selects `k=2`
or `3` macroscopic ordered bins of the complete slope measure, rescales their
quantization once so that the Gini-area functional (5) is exact, and reaches
the forbidden hexagon as a single Hausdorff limit of equality endpoints.

## Literature and trust boundary

Fradelizi, Manui, Meyer, and Ndiaye,
*L_p-Rogers--Shephard type inequalities for L_p-zonoids and symmetric
bodies*, arXiv:2607.03582v1 (2026), Corollary 29, prove (2) and state its
full equality classification as Conjecture 5:

<https://arxiv.org/abs/2607.03582>

Their Section 4 records that every centrally symmetric planar body is an
asymmetric `L_1`-zonoid, defines shadow systems with an arbitrary index set,
and supplies Firey-shadow closure and volume convexity.  The proof above adds
the measure quantization (7)--(20) and uses the independently reviewed strict
hexagon base case.  Targeted primary-source searches on 2026-09-03 found no
measure-quantization equality reduction or subsequent proof of Conjecture 5;
this is search-relative evidence, not a priority claim.

The companion exact checker `verify_zonoid_quantization.py` uses only Python
`Fraction` arithmetic.  It verifies the Gini-area functional, exact rescaling,
two-sided monotonicity, and constant area for continuous uniform-measure
models of both branches (`h=0,k=3` and `h>0,k=2`).  Under CPython 3.12.12,

```sh
python3 verify_zonoid_quantization.py
```

ends with

```text
result_sha256=e0a90164ffd457f60d55c805af0ca31d1a038310b1ffad96fae7f8ed6cfed398
VERIFIED
```

The argument is symbolic and human-readable.  It trusts the standard planar
zonoid representation, the cited shadow-system theorems, the sharp inequality,
and the strict hexagon theorem.  The checker is corroborative and does not
prove the arbitrary-measure quantization lemma.  No numerical computation,
solver, external data set, or omitted certificate establishes the result.
