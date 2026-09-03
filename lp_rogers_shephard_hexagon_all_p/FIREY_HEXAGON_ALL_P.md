# Strict Firey equality classification for centrally symmetric hexagons

## Statement

Let `1 < p < infinity`, let `q=p/(p-1)`, and put

```text
c_q = 2 Gamma(1+1/q)^2 / Gamma(1+2/q).
```

For convex bodies containing the origin, write `K +_p L` for the Firey
sum, defined by

```text
h_(K +_p L)(n)^p = h_K(n)^p + h_L(n)^p.
```

**Theorem.**  Let `K` be a full-dimensional centrally symmetric convex
hexagon in the plane having the origin as a vertex.  Then

```text
|K +_p (-K)| < (2+c_q)|K|.                         (1)
```

More precisely, an invertible linear map puts `K` in the form

```text
K(a,b) = [0,e_1] + [0,(a,b)] + [0,e_2],   a,b>0.  (2)
```

Set

```text
L=(a^p+b^p)^(1/p),  t=a/L,  u=b/L,
alpha=t^(p-1),       beta=u^(p-1),
Gamma_q={(x,y): x,y>=0 and x^q+y^q=1},
S=S_p(a,b)=integral_((1,0) to (alpha,beta)) (x dy-y dx),              (3)
```

where the last integral follows the first-quadrant `l_q` arc.  Then the
deficit in (1) is exactly

```text
Delta_p(a,b)
 := (2+c_q)|K(a,b)|-|K(a,b) +_p (-K(a,b))|
  = a+b-L(alpha+beta)+aS+b(c_q-S).                  (4)
```

For `p>=2`, it obeys the two-sided estimate

```text
c_q min(a,b) <= Delta_p(a,b) <= (c_q+4)min(a,b).    (5)
```

Since `1 <= c_q <= pi/2` in this range, (5) also gives the uniform bound

```text
min(a,b) <= Delta_p(a,b) <= (4+pi/2)min(a,b).       (6)
```

Consequently, even when `p` varies through `[2,infinity)`, a sequence of
normalized hexagons in the form (2) has relative deficit tending to zero if
and only if

```text
min(a,b)/(1+a+b) -> 0.                              (7)
```

This is an exact equality and normalized near-equality classification inside
the origin-vertex centrally symmetric hexagon class.  It is not a proof of
the equality conjecture for arbitrary centrally symmetric planar bodies.

## 1. Affine normal form

A centrally symmetric hexagon is a three-generator zonotope.  If the origin
is a vertex, its three edge generators lie in a pointed cone.  Taking the two
extreme generators as a basis, and rescaling their positive coefficients,
gives (2) with `a,b>0`.  Conversely, (2) is a full-dimensional centrally
symmetric hexagon for `a,b>0`.

Firey sums commute with invertible linear maps because support functions obey
`h_(TK)(n)=h_K(T^T n)`.  Both sides of (1) are multiplied by `|det T|`.
Thus the ratio and its equality status are unchanged by the normalization.
The zonotope area formula gives

```text
|K(a,b)| = det(e_1,(a,b))+det(e_1,e_2)+det((a,b),e_2)
          = b+1+a.                                  (8)
```

## 2. The coefficient arc

Suppose that in an open interval of normal directions the exposed points of
`K` and `-K` are the fixed vectors `X` and `Y`, and both support values are
positive.  Differentiating the Firey support function shows that the exposed
point of `K +_p (-K)` is

```text
xX+yY,
x=(<X,n>/h(n))^(p-1),  y=(<Y,n>/h(n))^(p-1).        (9)
```

The coefficients satisfy `x^q+y^q=1`, so they traverse an arc of `Gamma_q`.
Along that arc,

```text
det(xX+yY, d(xX+yY))
  = det(X,Y)(x dy-y dx).                            (10)
```

The full first-quadrant arc integral is

```text
integral_(Gamma_q) (x dy-y dx)
 = 2 area(B_q^2 intersect {x,y>=0})
 = 2 Gamma(1+1/q)^2/Gamma(1+2/q)
 = c_q.                                             (11)
```

Here the first equality is Green's formula, and the second is the standard
beta-integral evaluation of the `l_q`-ball area.

## 3. Complete half-boundary calculation

Write

```text
A=1+a,  B=1+b,  phi=arctan(b/a),
V=(A,B), X=(a,B), Y=(-1,0), X'=(0,1), Y'=(-A,-b).
```

For `n_theta=(cos(theta),sin(theta))` on the upper half-circle, the exposed
point pairs `(F(K,n_theta),F(-K,n_theta))` are constant on the following
three open sectors:

```text
0 < theta < pi/2:             (V,0),
pi/2 < theta < pi/2+phi:      (X,Y),
pi/2+phi < theta < pi:        (X',Y').              (12)
```

At `theta=pi/2+phi`, the two positive support values are proportional to
`a` and `b`.  Therefore the coefficient arc in the second sector runs from
`(1,0)` to `(alpha,beta)`, while the third-sector arc runs from
`(alpha,beta)` to `(0,1)`.  Between these arcs the exposed face runs from

```text
P=alpha X+beta Y  to  Q=alpha X'+beta Y'.           (13)
```

Indeed, at the intervening normal one has
`F(K)=[X',X]` and `F(-K)=[Y',Y]`.  The subdifferential chain rule for the
positive Firey support values gives the face
`alpha F(K)+beta F(-K)=[Q,P]`, since both summand faces are parallel to
`(a,b)`; positive boundary orientation is from `P` to `Q`.

The entire positively oriented half-boundary is consequently

```text
V -> X,
{xX+yY : (x,y) on Gamma_q from (1,0) to (alpha,beta)},
P -> Q,
{xX'+yY' : (x,y) on Gamma_q from (alpha,beta) to (0,1)},
Y' -> -V.                                           (14)
```

The Firey difference body is centrally symmetric: its support function is
unchanged by `n -> -n`.  Its area therefore equals the integral
`integral det(z,dz)` over the half-boundary (14); the usual factor `1/2` in
Green's formula cancels the two congruent halves.

The three segment contributions in (14) are

```text
det(V,X)=B,
J:=det(P,Q)=a alpha^2+(a+b)alpha beta+b beta^2,
det(Y',-V)=A.                                       (15)
```

Moreover,

```text
J=(alpha+beta)(a alpha+b beta)=L(alpha+beta),        (16)
```

because `a alpha+b beta=L(t^p+u^p)=L`.  Equations
(10)--(16) give the exact area identity

```text
|K(a,b) +_p (-K(a,b))|
 = A+B+J+B S+A(c_q-S).                              (17)
```

Subtracting (17) from `(2+c_q)(1+a+b)` proves (4).

## 4. Strict positivity for every `p>1`

The exact deficit is homogeneous in `(a,b)`.  Divide (4) by `L` and regard
the endpoint of the coefficient arc as a function of `beta`:

```text
alpha=(1-beta^q)^(1/q),
t=alpha^(q-1),  u=beta^(q-1),
D(beta)=Delta_p(a,b)/L
       =t+u-alpha-beta+tS+u(c_q-S).                 (18)
```

The arc integral has the remarkably simple derivative

```text
dS/d beta=alpha-beta d alpha/d beta=1/t.            (19)
```

Indeed, `d alpha/d beta=-u/t` and
`t alpha+u beta=alpha^q+beta^q=1`.  Using also

```text
dt/d beta=-(q-1)u/alpha,
du/d beta=(q-1)beta^(q-2),
```

all remaining terms cancel when (18) is differentiated:

```text
D'(beta)
 =(q-1)beta^(q-2)
   [(1+c_q-S)-(beta/alpha)(1+S)].                  (20)
```

As `beta` increases from `0` to `1`, `beta/alpha` increases strictly from
`0` to infinity.  At the same time, `S` increases strictly from `0` to
`c_q`, so `(1+c_q-S)/(1+S)` decreases strictly from `1+c_q` to
`1/(1+c_q)`.  Hence the bracket in (20) vanishes exactly once: `D` first
increases and then decreases.  Since `D(0)=D(1)=0`, it follows that
`D(beta)>0` for `0<beta<1`.  This proves (1) for every `1<p<infinity`.

## 5. Uniform stability for `p >= 2`

Since `p>=2` and `0<t,u<1`,

```text
a+b-J
 = L[(t-t^(p-1))+(u-u^(p-1))] >= 0.                (21)
```

Also `0<S<c_q`.  Formula (4) is therefore strictly positive when
`a,b>0`, and directly yields the lower bound in (5).

For the upper bound, symmetry permits us to assume `a>=b`, hence `u<=t`.
The bracketed difference in (21) satisfies

```text
u-u^(p-1) <= u,
t-t^(p-1) <= 1-t^(p-2) <= u^p <= u.                (22)
```

Indeed, `t^p=1-u^p`, and with `r=(p-2)/p` in `[0,1)` one has
`t^(p-2)=(1-u^p)^r >= 1-u^p`.  Thus `a+b-J<=2Lu=2b`.

Parametrize the initial coefficient arc by
`x=(1-y^q)^(1/q)`, `0<=y<=beta`.  Integration by parts gives

```text
S=2 integral_0^beta x dy-alpha beta <= 2 beta.      (23)
```

Consequently

```text
aS <= 2a beta
   = 2L t u^(p-1)
   <= 2Lu=2b,                                       (24)
```

while `b(c_q-S)<=bc_q`.  Combining (22)--(24) proves
`Delta_p(a,b)<=(4+c_q)b`.  Swapping the coordinate axes handles `b>=a`,
and proves (5).

Finally, for `1<q<=2` the planar balls satisfy
`B_1^2 subset B_q^2 subset B_2^2`.  Equation (11) gives
`1<=c_q<=pi/2`, hence (6).  Dividing (5) by (8), with constants independent
of `p`, proves (7).

## 6. Checks and boundary meaning

- At `p=2`, `q=2`, `c_q=pi/2`, `alpha=a/L`, `beta=b/L`, and
  `S=arctan(b/a)`.  Then `J=a+b`, so (4) becomes
  `Delta_2=a arctan(b/a)+b(pi/2-arctan(b/a))`, exactly the known circular-arc
  formula.
- If `a=0` or `b=0`, understood by continuity, the middle generator in (2)
  is collinear with an outer generator.  The hexagon becomes a parallelogram
  and (4) gives zero deficit.
- No numerical computation, optimizer, or unreported certificate is used.
  The proof depends only on the affine normal form, differentiating a support
  function on three sectors, Green's formula, and elementary inequalities.

## Literature boundary

Fradelizi, Manui, Meyer, and Ndiaye, *L_p-Rogers--Shephard type inequalities
for L_p-zonoids and symmetric bodies*, arXiv:2607.03582v1 (2026), Corollary 29,
prove the sharp planar inequality for all centrally symmetric bodies and show
that origin-vertex parallelograms attain equality.  Their Conjecture 5 asks
whether these are the only equality cases for `p>1`:

<https://arxiv.org/abs/2607.03582>

The result above settles the strict six-vertex, origin-vertex subcase for the
full conjectured range `1<p<infinity`, and adds an exact deficit there and a
uniform normalized stability criterion for `p>=2`.  Targeted searches on
2026-09-03 found no general-`p` three-generator formula or this hexagon
stability statement.  That is search-relative evidence, not a priority claim.

The contemporaneous paper arXiv:2606.07887 classifies equality for the
different unrestricted planar `L_p` Rogers--Shephard bound (whose extremizers
are origin-vertex triangles); it does not settle the improved centrally
symmetric constant or Conjecture 5:

<https://arxiv.org/abs/2606.07887>
