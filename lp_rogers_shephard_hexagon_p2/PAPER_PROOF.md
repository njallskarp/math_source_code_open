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

Since `a,b,φ,π/2-φ` are all positive, (9) is strictly positive.  Equality
can occur only on the parameter-space boundary `a=0` or `b=0`, precisely
where the middle generator is parallel to an extreme generator and the
hexagon degenerates to a parallelogram.

## Trust boundary

The geometric proof above is presently a human proof.  Lean checks the
three-generator squared-support identity, the angle bounds, the algebraic
deficit identity, and strict positivity of the final expression.  Lean does
not yet check the normal-form theorem, the support-function area formula,
or the three sector integrations.
