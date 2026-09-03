# Firey equality classification for every centrally symmetric polygon

## Theorem

Let `1<p<infinity`, let `q=p/(p-1)`, and set

```text
c_q=2 Gamma(1+1/q)^2/Gamma(1+2/q).
```

Let `K` be a full-dimensional centrally symmetric convex polygon in the
plane and suppose that `0 in K`.  Then

```text
|K +_p (-K)|=(2+c_q)|K|                           (1)
```

if and only if `K` is a parallelogram having the origin as a vertex.
Equivalently, every other placement or finite-sided shape satisfies the sharp
planar symmetric Firey Rogers--Shephard inequality strictly.

The proof uses the exact strict-hexagon theorem as its base case, an explicit
edge-placement calculation for parallelograms, and the same shadow-system
convexity that proves the underlying non-strict inequality.  It does not
assert the equality classification for nonpolygonal bodies.

## 1. Minimal zonotope representation at a vertex

Suppose that `K` has `2m` sides.  Traverse its boundary from the origin to
the opposite vertex and denote the successive edge vectors by
`v_1,...,v_m`.  Central symmetry supplies the remaining edge vectors
`-v_1,...,-v_m`, so

```text
K=sum_(i=1)^m [0,v_i].                             (2)
```

This is the minimal planar zonotope representation: the generator directions
are pairwise distinct and occur in their circular order.  Because the origin
is a vertex, they lie in a pointed cone.  An invertible linear map taking the
two extreme rays to the coordinate rays puts them in the form

```text
v_1=e_1,
v_i=(x_i,y_i),  x_i,y_i>0       for 2<=i<m,
v_m=(0,y_m),    y_m>0.                             (3)
```

Neither the equality in (1) nor the number of generator directions changes
under this normalization.

## 2. An explicit constant-area deletion shadow

Assume `m>=3`, and define

```text
Y=sum_(i=2)^m y_i,
Q=sum_(2<=i<j<=m) det(v_i,v_j),
lambda=Q/Y.                                        (4)
```

The ordered, distinct directions in (3) give `Y>0` and `Q>0`, so
`lambda>0`.  For

```text
-1/lambda <= s <= 1
```

put

```text
w_1(s)=(1+lambda s)e_1,
w_i(s)=((1-s)x_i,y_i)       for 2<=i<=m,
K_s=sum_(i=1)^m [0,w_i(s)].                         (5)
```

Every subset sum of the generators in (5) moves affinely on a line parallel
to `e_1`.  Since a zonotope is the convex hull of its subset sums, `{K_s}` is
a shadow system along `e_1` and `K_0=K`.

All determinants remain nonnegative on this interval, and

```text
det(w_1(s),w_i(s))=(1+lambda s)y_i,
det(w_i(s),w_j(s))=(1-s)det(v_i,v_j)  (2<=i<j<=m).
```

The planar zonotope area formula and `lambda Y=Q` therefore give

```text
|K_s|=(1+lambda s)Y+(1-s)Q=Y+Q.                   (6)
```

Thus the area is exactly constant, not merely affine.

At the right endpoint, all `w_i(1)` for `i>=2` are positive multiples of
`e_2`, so `K_1` is a parallelogram with the origin as a vertex.  At the left
endpoint `w_1(-1/lambda)=0`; the common positive rescaling of the horizontal
coordinates of `w_2,...,w_m` preserves their distinct ordered directions.
Consequently

```text
K_-=K_(-1/lambda)
```

is a full-dimensional origin-vertex centrally symmetric polygon with exactly
`2(m-1)` sides.

## 3. Equality propagates to the deletion endpoint

A standard closure theorem for shadow systems under Firey addition implies
that

```text
C_s=K_s +_p (-K_s)
```

is also a shadow system along `e_1`.  Hence

```text
F(s)=|C_s|                                          (7)
```

is convex on `[-1/lambda,1]`.  The sharp planar symmetric Firey
Rogers--Shephard inequality applies to every `K_s`; by (6),

```text
F(s)<=(2+c_q)(Y+Q)                                 (8)
```

throughout the interval.

If `K=K_0` attained equality, then `F(0)` would attain the common upper bound
in (8) at an interior parameter.  A convex function bounded above on an
interval cannot attain its maximum at an interior point unless it is
constant.  Therefore `F(-1/lambda)` also attains the bound, and `K_-` is an
equality case with one fewer generator direction.

This implication is the decisive step:

```text
equality for an m-generator origin-vertex polygon
  ==> equality for an (m-1)-generator origin-vertex polygon.          (9)
```

No strict-convexity theorem for shadow volumes is required.

## 4. Classification when the origin is a vertex

For `m=2`, (2) is a parallelogram with the origin as a vertex, and equality
is known to hold.

For `m=3`, (2) is a genuine centrally symmetric hexagon.  The exact
three-generator boundary calculation proves

```text
|K +_p (-K)|<(2+c_q)|K|                            (10)
```

for every `p>1`.

Now suppose `m>=4` and that equality holds.  Iterating (9) produces an
equality case with exactly three generator directions, contradicting (10).
Thus equality is impossible for every `m>=3`, while it holds for `m=2`.
This proves the origin-vertex part of the theorem.

## 5. A parallelogram with the origin inside an edge is strict

It remains important to distinguish the shape from the placement of the
origin.  By affine invariance, every parallelogram having the origin in the
relative interior of an edge has the form

```text
P_a=[-a,1-a] x [0,1],       0<a<1.                 (11)
```

Put `A=1-a`,

```text
L=(A^p+a^p)^(1/p),  t=A/L,  u=a/L,
alpha=t^(p-1),      beta=u^(p-1),                  (12)
```

and let `S` be the oriented `x dy-y dx` integral on the first-quadrant
`l_q` unit arc from `(1,0)` to `(alpha,beta)`.

There are two mixed sectors on the upper half-boundary of
`P_a +_p (-P_a)`.  The exposed point pairs are

```text
((A,1),(a,0))       in the first quadrant,
((-a,1),(-A,0))     in the second quadrant.        (13)
```

The coefficient arc in the first sector runs from `(alpha,beta)` to `(1,0)`;
its determinant and oriented arc integral are respectively `-a` and `-S`,
so it contributes `aS`.  The second arc runs from `(1,0)` to
`(beta,alpha)` and contributes `A(c_q-S)`.  The top face contributes `1`.
At the left horizontal normal, the closing vertical face contributes
`L(alpha+beta)`.  Green's formula on this half-boundary therefore gives

```text
|P_a +_p (-P_a)|
 =1+L(alpha+beta)+aS+A(c_q-S).                     (14)
```

Since `|P_a|=1`, its deficit is

```text
(2+c_q)-|P_a +_p (-P_a)|
 =1-L(alpha+beta)+A S+a(c_q-S).                    (15)
```

The right side of (15) is exactly the strict hexagon deficit
`Delta_p(A,a)` from the three-generator theorem.  Both `A` and `a` are
positive, so (15) is strictly positive for every `p>1`.  At `a=0` or `a=1`
it vanishes by continuity, precisely when the origin is a vertex.

## 6. Translation shadows finish all polygonal placements

Suppose first that the origin lies in the relative interior of an edge of a
centrally symmetric polygon `K`.  Translate `K` parallel to that edge over
the maximal interval for which the origin remains on the edge.  The original
placement is an interior parameter and the two endpoint placements have the
origin at a vertex.  The area of `K` is constant; Firey addition preserves
the translation shadow and its Firey area is convex.

If the original placement were an equality case, convexity and the common
sharp upper bound would force both endpoint placements to be equality cases.
Section 4 then forces the shape to be a parallelogram.  But (15) says that an
edge-interior placement of a parallelogram is strict, a contradiction.

Now suppose that `0` lies in the interior of `K`.  Choose a translation
direction whose first boundary contact is in the relative interior of an
edge; avoiding the finitely many directions leading to vertices guarantees
this.  On the maximal translation interval keeping `0` in the body, the
original placement is an interior parameter.  Equality there would again
force equality at the chosen edge-interior endpoint, which the preceding
paragraph rules out.

The only remaining placements are vertices.  Section 4 classifies those,
and the known parallelogram calculation supplies the converse.  This proves
the full polygonal theorem.

## 7. Scope, dependencies, and checks

- The construction (5) is the planar specialization of the generator shadow
  used by Fradelizi--Manui--Meyer--Ndiaye to prove their sharp inequality.
  Here the constant `lambda=Q/Y`, preservation of area, and both endpoint
  types are written explicitly.
- The use of the global sharp inequality in (8) is essential.  Convexity
  alone would not force an interior equality value to propagate.
- Minimality of (2) prevents a hidden loss of more than one side pair at the
  left endpoint.  The common horizontal scaling preserves every slope among
  `v_2,...,v_m`.
- At the right endpoint multiple vertical generators combine into one
  segment, giving exactly a parallelogram; this endpoint is not needed for
  the induction but confirms the reduction geometry.
- Formula (15) prevents the translation argument from confusing a
  parallelogram shape with the required origin-at-a-vertex placement.
- No numerical computation, solver, external data set, or omitted
  certificate is used in the proof.

## Literature boundary

Fradelizi, Manui, Meyer, and Ndiaye,
*L_p-Rogers--Shephard type inequalities for L_p-zonoids and symmetric
bodies*, arXiv:2607.03582v1 (2026), Corollary 29, prove (8) for every planar
centrally symmetric body and state the full equality classification as
Conjecture 5.
Their proof records the generator shadow, its constant volume, closure under
Firey addition, and convexity of the resulting volume:

<https://arxiv.org/abs/2607.03582>

The new argument combines that established deformation with the strict
six-sided base case and the exact edge-placement identity (15) to classify
every finite-sided equality case, for every placement of the origin.  It does
not claim the limiting nonpolygonal step.
Targeted searches on 2026-09-03 found no such finite-sided induction; this is
search-relative evidence, not a priority claim.
