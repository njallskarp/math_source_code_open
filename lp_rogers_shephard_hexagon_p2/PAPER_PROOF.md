# The strict planar `p = 2` Rogers--Shephard bound for centrally symmetric hexagons

## Claim and scope

Let `K` be a full-dimensional centrally symmetric convex hexagon in
`R^2`, with the origin as a vertex.  If `⊕₂` denotes Firey addition,

```text
area(K ⊕₂ (-K)) < (π/2 + 2) area(K).
```

This proves Conjecture 5 of Fradelizi--Manui--Meyer--Ndiaye only in the
strict six-vertex regime and only for `p = 2`.  It is not a proof of the
general equality conjecture.

## 1. Normal form

The edge vectors of a centrally symmetric hexagon occur as
`u,v,w,-u,-v,-w`.  Because the origin is a vertex, the three positive edge
vectors lie in a common open half-plane.  Choose `u,w` as the two extreme
directions.  The middle vector is a positive linear combination of them.
An invertible linear map therefore sends the hexagon to

```text
K(a,b) = [0,e₁] + [0,(a,b)] + [0,e₂],    a>0, b>0.
```

Firey support functions commute with invertible linear maps and both areas
are multiplied by the absolute determinant.  It is enough to prove the
claim for `K(a,b)`.  Its vertices are

```text
0, e₁, e₁+(a,b), e₁+(a,b)+e₂, (a,b)+e₂, e₂,
```

and the shoelace formula gives

```text
area(K(a,b)) = 1+a+b.                                      (1)
```

Put `φ=arctan(b/a)`, so `0<φ<π/2`.

## 2. Support function and area formula

For `n(θ)=(cos θ,sin θ)`, write `h(θ)` for the support function of
`L=K(a,b)⊕₂(-K(a,b))`.  The segment support formula gives

```text
h_K(n)=max(n₁,0)+max(a n₁+b n₂,0)+max(n₂,0),
h(θ)^2=h_K(n(θ))^2+h_K(-n(θ))^2.                           (2)
```

Equation (2) also shows that `h(θ+π)=h(θ)`.  The standard planar support
formula, valid here for the piecewise smooth support function, is

```text
area(L)=1/2 ∫₀^{2π}(h²-(h')²)dθ
       =    ∫₀^π   (h²-(h')²)dθ.                           (3)
```

The sign changes in the upper half-circle occur at
`0, π/2, π/2+φ, π`.

For later use, on an interval where

```text
h(θ)^2 = (x·n(θ))²+(y·n(θ))²
```

with independent `x,y`, put `Q=xxᵀ+yyᵀ`.  Direct differentiation gives

```text
h²-(h')² = det(Q)/h² - (h h')'.                            (4)
```

If `M` has columns `x,y`, the argument of `Mᵀn(θ)` has derivative
`det(M)/h²`; hence the first term in (4) integrates to the absolute
determinant times the corresponding change of argument.  The endpoint term
`[h h']` must be retained.  Omitting it loses the polygonal contribution
and gives an incorrect area even for a square.

## 3. The three sectors

Let `A=1+a` and `B=1+b`.

### Sector I: `0<θ<π/2`

All three generator pairings are positive, so

```text
h(θ)=A cos θ+B sin θ.
```

Therefore

```text
∫₀^{π/2}(h²-(h')²)dθ = 2AB = 2(1+a)(1+b).                 (5)
```

### Sector II: `π/2<θ<π/2+φ`

Only the `e₁` pairing is negative, and

```text
h²=((a,b+1)·n)²+(e₁·n)².
```

The curvature term in (4) integrates to `(1+b)φ`.  At the two endpoints,

```text
h h' = -a(1+b), -a,
```

so `[h h']=ab`.  This sector contributes

```text
(1+b)φ-ab.                                                 (6)
```

### Sector III: `π/2+φ<θ<π`

Only the `e₂` pairing is positive, and

```text
h²=(e₂·n)²+((1+a,b)·n)².
```

The curvature term is `(1+a)(π/2-φ)`.  The endpoint values of `h h'` are
`b` and `b(1+a)`, again giving `[h h']=ab`.  The contribution is

```text
(1+a)(π/2-φ)-ab.                                          (7)
```

Summing (5)--(7), the `2ab` from Sector I cancels the two endpoint terms:

```text
area(L)
 = 2(1+a+b)+(1+b)φ+(1+a)(π/2-φ).                          (8)
```

## 4. Strict deficit

Using (1) and (8), exact algebra gives

```text
(π/2+2)area(K)-area(L)
  = a φ+b(π/2-φ).                                          (9)
```

Since `a,b,φ,π/2-φ` are all positive, (9) is strictly positive.  In the
finite closure of this parameter chart, a zero deficit can occur only on
`a=0` or `b=0`, where the middle generator is parallel to an extreme
generator and the hexagon degenerates to a parallelogram.

This finite-boundary statement must not be confused with a classification
of affine-normalized near-equality sequences.  For example, `a→∞` with
`b=1` gives `D(a,b)/(1+a+b)→0`; after an additional affine normalization,
an extreme generator collapses and the limiting body is again a
parallelogram.  More precisely, the independent review at Discovery Net
artifact `bafkreig77oiopn6zq4l37ahdoqqwucmuhevkhp7uqi5v5qet37oh3x5foi`
proves

```text
(π/2) min(a,b) ≤ D(a,b) < (1+π/2) min(a,b),
```

so normalized near-equality is equivalent to
`min(a,b)/(1+a+b)→0`.

## Trust boundary

The geometric proof above is presently a human proof.  Lean checks that the
actual set `[0,u]+[0,v]+[0,w]` has support equal to the sum of the positive
generator pairings and checks the resulting three-generator squared-support
identity.  For the normalized set it proves that this literal support and its
reflection restrict to the displayed Sector I, II, and III support squares
on the corresponding closed angular intervals.  It also checks `π`-periodicity
of the set-level squared support and agreement of the adjacent square formulas
at their shared endpoints.  For Sector II it checks
`h=√F`, its derivative, the
determinant decomposition (4), both endpoint values, and the exact integral
reduction to the curvature integral minus `ab`.  It proves that the phase
denominator `U=a cos θ+(1+b) sin θ` stays positive on the closed sector,
differentiates the branch-correct primitive
`-(1+b) arctan(cos θ/U)`, checks both endpoint phases, and therefore proves
the complete Sector II integral `(1+b)φ-ab`.  It then proves the exact
reflection identity under `η=3π/2-θ`, the complementary-angle formula
`arctan(a/b)=π/2-arctan(b/a)`, and derives the complete Sector III integral
`(1+a)(π/2-φ)-ab` by interval substitution and parameter exchange.  For
Sector I it differentiates `h=(1+a)cos θ+(1+b)sin θ`, proves an exact primitive
of the nonconstant density, and obtains `2(1+a)(1+b)`.  It then defines one
piecewise upper-half-circle density, proves interval integrability on all
three pieces, applies interval additivity at both sign changes, and checks the
complete scalar integral in (8).  Lean additionally checks the angle bounds,
the algebraic deficit identity, and strict positivity of the final expression.

Lean now also formalizes the canonical support-boundary construction
`gamma=h n+h' t`.  It proves `gamma'=(h+h'')t` and
`det(gamma,gamma')=h(h+h'')`, checks the Sector II and III second derivatives,
and identifies their actual oriented boundary densities with the curvature
terms in (4).  The corresponding arc integrals are `(1+b)φ` and
`(1+a)(π/2-φ)`.  Sector I is the constant boundary point `(1+a,1+b)` and has
zero arc density.  At the three upper-half sign boundaries, the one-sided
canonical boundary points are joined by segments whose checked determinants
are respectively `1+b`, `a+b`, and `1+a`.  Their sum is `2(1+a+b)`.  Hence
Lean proves that the arcs-plus-jumps oriented-boundary total is exactly the
already checked support-density integral in (8).  This formally accounts for
all polygonal endpoint contributions.

Lean additionally reproduces the source `p=2` Firey body as the exact
intersection of all vector halfspaces and checks that source exponent `1/2`
is the square root.  A global consequence of the three-positive-parts identity
shows that the full Firey support dominates the Sector II and III ellipsoidal
quadratic supports in every direction.  A formalized two-coordinate
Cauchy--Schwarz argument therefore places each ellipsoidal support point in the
exact body.  Lean proves these points identical to the canonical Sector II and
III arc points used above and proves support attainment at their normals.  The
literal subtype-supremum support of the halfspace body consequently equals the
prescribed Firey support throughout both curved sectors.  The fixed Sector I
vertex and its opposite also lie in the body; the body is convex; and all three
checked jump segments are subsets of it.

The pinned Mathlib has curve-integral infrastructure but no planar Green/Jordan
theorem, no convex support-function or mixed-area API, and no theorem
identifying the closed oriented integral of this piecewise smooth convex
boundary with twice its Lebesgue area.  Full exposed-face and boundary coverage
for the checked arcs and jump segments, followed by that boundary-to-area
identification, is now the precise smallest analytic-geometry bridge.  Lean
still does not check that bridge, the affine
normal-form theorem, the source-level Firey-sum/set equivalence, or the
end-to-end area theorem.
