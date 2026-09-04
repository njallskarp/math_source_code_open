# The simultaneous one-fat-level obstruction

## Setup

Let `p>=3` be prime, let `gcd(n,p)=1`, and identify

```text
Z/(np)Z = Z/nZ x Z/pZ.
```

For a subset `A`, its `j`-th level is

```text
A_j = {a in Z/nZ : (a,j) in A}.
```

A pair `(A,Lambda)` is spectral when the characters indexed by `Lambda` form
an orthogonal basis on `A`.

## Theorem 1: block-Gram obstruction

Suppose `(A,Lambda)` is a spectral pair and both coordinate projections

```text
pi_n(A), pi_n(Lambda) subset Z/nZ
```

are injective.  It is impossible for both `A` and `Lambda` to have level-size
multiset

```text
(r,1,1,...,1)                                           (1)
```

with one `r`-point level and `p-1` singleton levels, for any `r>=2`.

### Cross-level coefficient equality

Take two points `(b,u),(c,v)` of `Lambda` on different `p`-levels.  Put
`x=b-c`.  Projection injectivity gives `x!=0` in `Z/nZ`; let `d>1` be its
additive order.  Orthogonality, grouped by the levels of `A`, gives

```text
sum_(j in Z/pZ) zeta_p^((u-v)j) S_j(x) = 0,
S_j(x) = sum_(a in A_j) zeta_n^(x a).                   (2)
```

Every `S_j(x)` lies in `K=Q(zeta_d)`.  Since `gcd(d,p)=1`,

```text
[K(zeta_p):K]=p-1.
```

After permuting the exponents by the nonzero residue `u-v`, equation (2) is a
polynomial of degree at most `p-1` over `K` which vanishes at `zeta_p`.  The
minimal polynomial is

```text
Phi_p(X)=1+X+...+X^(p-1),
```

so all coefficients `S_j(x)` are equal.

Let the large level of `A` have first coordinates `a_1,...,a_r`, and choose
one singleton first coordinate `alpha`.  For every cross-level difference
`x=b-c` in `Lambda`, coefficient equality says

```text
sum_(i=1)^r zeta_n^(x(a_i-alpha)) = 1,                 (3)
zeta_n^(x(alpha_j-alpha)) = 1                          (4)
```

for every singleton coordinate `alpha_j` of `A`.

### Same-large-level differences

The `p-1` singleton levels of `Lambda` are nonempty.  Fix any point on one of
them.  If `(b,u),(c,u)` are two distinct points on the large level of
`Lambda`, each of `b` and `c` differs cross-level from the fixed singleton
coordinate.  Subtracting the two instances of (4) shows that `x=b-c` also
annihilates every singleton difference `alpha_j-alpha`.

Orthogonality now has no `p`-phase, and the `p-1` singleton levels of `A`
contribute the same normalized value.  Hence

```text
sum_(i=1)^r zeta_n^(x(a_i-alpha)) = -(p-1).            (5)
```

### The impossible Gram matrix

For every `(b,u) in Lambda`, define

```text
v_(b,u) = (zeta_n^(b(a_i-alpha)))_(i=1)^r in C^r.      (6)
```

Order these `r+p-1` vectors with the `r` points on the large level first and
the `p-1` singleton-level points second.  Equations (3), (5), and (6) force
their Gram matrix to be

```text
G = [ (r+p-1)I_r-(p-1)J_r       J_(r,p-1)       ]
    [       J_(p-1,r)       (r-1)I_(p-1)+J_(p-1)].     (7)
```

Indeed, its diagonal entries are `r`; off-diagonal entries in the large block
are `-(p-1)`; and every other off-diagonal entry is 1.

Restrict the quadratic form to vectors constant on each block.  Put

```text
a=p-1-r(p-2),  q=p-1,  delta=r+p-2.
```

In the basis `(1_r,0)` and `(0,1_q)`, its symmetric matrix is

```text
H = [ r a       r q   ]
    [ r q     q delta ].                                (8)
```

Its determinant is `r q` times

```text
a delta-rq=-(r-1)(p-2)(r+p-1)<0.                       (9)
```

Equivalently, put `k=r+p-1` and evaluate (7) on the real integer vector which
is `k-1` on the large block and `-r` on the singleton block.  The value is

```text
-r(k-1)(r-1)(p-2)k < 0.                               (10)
```

But a Gram matrix is positive semidefinite.  This contradiction proves
Theorem 1.

## Theorem 2: closed sub-double-prime interval

Let `(A,Lambda)` be spectral in `Z/(np)Z`, and put
`k=|A|=|Lambda|`.  If

```text
p < k <= 2p-1,                                         (11)
```

then at least one of `A,Lambda` has the `p`-descent property

```text
Phi_(dp) | m_E  implies  Phi_d | m_E   for every d|n.  (12)
```

Moreover, the projections of `A` and `Lambda` to `Z/nZ` are injective and
form a spectral pair there.  Thus spectral-to-tiling at cardinality `k`
downstairs implies spectral-to-tiling upstairs.

### Proof

The case `k<=2p-2` is the independently reviewed sub-double-prime Gram-descent
theorem.  At `k=2p-1`, we still have `p` not dividing `k`.  A collision in
either projection would give an order-`p` difference and force `Phi_p` to
divide the other mask; evaluation at 1 would then force `p|k`.  Thus both
projections are injective.

If both descent properties failed, the cuboid criterion and levelwise cuboid
identity used in the predecessor theorem would make all `p` levels of both
members nonempty.  Its rank argument further shows that the only surviving
level profile on either side is

```text
(p,1^(p-1)).                                           (13)
```

Theorem 1 with `r=p` rules out simultaneous profiles (13).  Hence one member
descends.  Somlai's projection lemma, applied directly or to the swapped
spectral pair, gives the projected spectral pair.  The standard graph lift of
a downstairs tiling then proves the last assertion.

## Corollary for `Z/2310Z`

Take `n=210` and `p=11`.  Fuglede's conjecture holds in `Z/210Z` by the
published four-prime theorem.  Theorem 2 therefore gives spectral-to-tiling
for every size 12 through 21 in `Z/2310Z`.

A translational tile has cardinality dividing 2310.  The divisors in this
interval are exactly

```text
14, 15, 21.
```

Cyclic subgroups realize all three sizes and are spectral.  Consequently the
exact spectral cardinalities in the closed interval are

```text
possible (and tiling): 14,15,21;
impossible:             12,13,16,17,18,19,20.
```

The new endpoint is size 21.  No assertion is made at size 22, where `p|k`
and the injectivity argument changes.
