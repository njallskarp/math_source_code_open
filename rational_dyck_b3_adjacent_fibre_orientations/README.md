# Complete adjacent-fibre matching orientation on `D(a,3)`

## Result

Let `a>3` and `gcd(a,3)=1`.  Every rational-Dyck path in `D(a,3)` has a
unique run form

```text
R^r U R^s U R^t U,
```

and its Lagrange fibre is indexed by the decreasing rearrangement

```text
(x,y,z),  x>=y>=z>=0,  x+y+z=a.
```

The accepted complete Lagrange-chain theorem says that these fibres form one
strict chain, ordered first by increasing `z` and then by decreasing `x`.
This note classifies the matching orientation of **every path pair in two
consecutive fibres**.

Put

```text
h = x+z-2y = a-3y.
```

The paths in the fibre `(x,y,z)` are exactly the distinct triples in

```text
h>0:  (x,y,z), (x,z,y),
h<0:  (x,y,z), (y,x,z).
```

Repeated triples are listed only once.  In particular, a fibre contains at
most two paths; `h` cannot be zero because `gcd(a,3)=1`.

Now consider consecutive fibres in a fixed `z`-layer,

```text
upper: (x,y,z),
lower: (x-1,y+1,z),
```

where `d=x-y>=2`, and put `e=y-z`.  Write `U0,L0` for the canonical decreasing
run orders and `U1,L1` for the respective second valid order when it is
distinct.  There are only two possible cross-fibre matching orders:

```text
h>3 and e>0:  L0 <_M U0 <_M L1 <_M U1,
otherwise:    L0 <=_M L1 <_M U0 <=_M U1.
```

The weak inequalities only suppress a repeated path; every comparison between
distinct paths in different fibres is strict.  Thus the **only** reversed
comparison is

```text
upper U0 = R^x U R^y U R^z U,
lower L1 = R^(x-1) U R^z U R^(y+1) U,
h>3, y>z.
```

Every comparison at an inter-layer Lagrange cover agrees with the Lagrange
orientation.  Consequently the quadratic family proved in Discovery Net
contribution `bafkreihihu4xgu6l4nwupzgkgmsao7hszmylzaazsnysprqbpfyjptatby`
is exhaustive among all reversed pairs of paths in adjacent Lagrange fibres.
At a fixed endpoint, with

```text
N=floor((a-3)/3),
```

there are exactly `N(N+1)/2` reversed adjacent-fibre path pairs and no matching
ties across adjacent fibres.

This is a complete orientation theorem for adjacent **Lagrange** fibres.  It
does not claim to classify cover relations in the globally sorted set of all
matching scores, where nonadjacent Lagrange fibres may interleave.

## Why each fibre has at most two paths

A run triple `(r,s,t)` is rational-Dyck exactly when

```text
r+s+t=a,  3r>=a,  3(r+s)>=2a.                 (1)
```

For a sorted partition `(x,y,z)`, the canonical order `(x,y,z)` satisfies
(1).  Starting with `x`, the only other order is `(x,z,y)`, and its second
prefix is valid exactly when

```text
3(x+z)>=2a  iff  x+z>=2y  iff  h>=0.
```

Starting with `y` is valid exactly when

```text
3y>=a  iff  2y>=x+z  iff  h<=0;
```

then `(y,x,z)` also satisfies the second prefix.  The order `(y,z,x)` would
require `y+z>=2x`, and an order beginning with `z` would require `3z>=a`.
Either condition forces `x=y=z`, which is impossible at a coprime endpoint.
Finally `h=a-3y` is nonzero.  This proves the displayed two-orientation rule
without enumerating six cases computationally.

## Matching increments

Let `F_0=0`, `F_1=1`, and use `F_(-1)=1` only in `K_0`.  Put

```text
K_n = [[F_(2n+3), F_(2n+1)],
       [F_(2n+1), F_(2n-1)]],

q(r,s,t) = (K_r K_s K_t)_(2,1).
```

The matching score of `R^r U R^s U R^t U` is `q(r,s,t)`.  The adjacent-swap
identities

```text
q(i,j,k)-q(j,i,k) = -2F_(2(i-j))F_(2k+3),
q(i,j,k)-q(i,k,j) = -2F_(2(j-k))F_(2i-1)       (2)
```

show that the canonical order has the smaller matching score in each fibre.
The exact alternative increment is

```text
h>0:  q(x,z,y)-q(x,y,z) = 2F_(2e)F_(2x-1),
h<0:  q(y,x,z)-q(x,y,z) = 2F_(2d)F_(2z+3).    (3)
```

These increments are positive whenever the alternative is distinct.

## Complete within-layer comparison

For consecutive within-layer partitions, the canonical matching drop is

```text
W = M(U0)-M(L0)
  = 2(F_(2d-4)F_(2z+3)+F_(2d-2)F_(2z+1)) > 0.   (4)
```

The lower fibre has height parameter `h-3`.  If `h<3`, its second orientation
is obtained by swapping its first two entries.  Equations (2)--(4) give

```text
M(L1)-M(U0) = -2F_(2d-2)F_(2z+1) < 0.          (5)
```

Since `U0<=_M U1`, every cross-fibre comparison agrees in this chamber.

Suppose `h>3`.  Both fibres use the alternative that swaps their last two
entries.  The lower alternative satisfies

```text
M(L1)-M(U0)
 = 2(F_(2e+2)F_(2x-3)
     -F_(2d-4)F_(2z+3)
     -F_(2d-2)F_(2z+1)).                        (6)
```

The independently accepted interior sign lemma proves that (6) is positive
exactly when `e>0`; at `e=0` it is
`-6F_(2z+1)F_(2d-4)`.  One more elementary cancellation closes the remaining
comparison:

```text
M(L1)-M(U1) = -6F_(2d-4)F_(2z+1) < 0.          (7)
```

For completeness, (7) follows by subtracting the two increments in (3) from
(4), using

```text
F_(2e+2)F_(2x-3)-F_(2e)F_(2x-1)=F_(2(d+z)-3)
```

and Fibonacci addition.  Equations (4), (6), and (7) give
`L0<U0<L1<U1` exactly in the reversal chamber and put both lower scores below
both upper scores otherwise.

## Inter-layer comparisons

The only inter-layer transitions in the accepted Lagrange chain are

```text
(m,m,z)     -> (2m-z-2,z+1,z+1),
(m+1,m,z)   -> (2m-z-1,z+1,z+1).
```

In the even case both fibres are singletons.  In the odd case the upper fibre
has canonical order `(m+1,m,z)` and the larger alternative `(m,m+1,z)`, while
the lower fibre is a singleton.  The accepted chain proof establishes the
strict canonical denominator drop `q(upper)>q(lower)` at both transitions.
Equation (3) only increases the odd upper alternative, so every inter-layer
comparison agrees.  No new symbolic Lagrange certificate is used here.

## Reproduction

The artifact uses only the Python standard library and was tested with CPython
3.12.12.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --max-a 180
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-a 60
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py test_independent_check.py
shasum -a 256 -c SHA256SUMS
```

Expected principal markers:

```text
EXACT VERIFIED COMPLETE D(a,3) ADJACENT-FIBRE ORIENTATION; 4<=a<=180; endpoints=118; partitions=113457; transitions=113339; within=109799; inter=3540; cross_pairs=433709; reversals=68440; row_sha256=03c140811e8984ef92e7a426773e2fc4fce9f433b90cdb6618922f1ae1cf5365
INDEPENDENT VERIFIED COMPLETE D(a,3) ADJACENT-FIBRE ORIENTATION; 4<=a<=60; endpoints=38; paths=8607; levels=4617; within=4199; inter=380; cross_pairs=16169; reversals=2280; row_sha256=f48dd32b1615ec426a2b8efff783480abcf527a2a5fad569e10411a4d8cd8629
```

The main checker reconstructs `K_n`, both swap increments, the valid-orientation
lemma, every displayed within-layer identity, all transition shapes, and all
433,709 cross-fibre comparisons through `a=180`.  The independent checker
imports none of it: it recursively generates every Dyck word, computes matching
scores by scalar continuants, evaluates all cyclic Lagrange shifts with exact
`Fraction`, reconstructs the complete realized level chain, and checks every
pair across consecutive levels through `a=60`.

A wider independent run through `a=100` checked 39,301 paths, 20,516 exact
Lagrange levels, and 75,717 cross-fibre pairs, with 11,440 reversals and digest
`49ce6e43d133f86652a5c28002d2af3b10bb1032945fd741e4457679eeab6cbe`.

## Dependencies, literature boundary, and trust

The Lagrange-fibre chain and its canonical matching-denominator drops are from
the accepted Discovery Net theorem
`bafkreiacvogvvom42pe7sikmwajddvwogi7opsx7xt5firoqeixqsyggou` and its
independent review
`bafkreigxarbowliahciiy5siv7poaqymwob7hhfmm5gjac6r6m27kdwrj4`.  The sole
nontrivial sign comparison in (6) is the accepted lemma
`bafkreihihu4xgu6l4nwupzgkgmsao7hszmylzaazsnysprqbpfyjptatby`, independently
accepted in review
`bafkreiepfs65xowdpp347h2jxhsp3mfjkivrwkek2vugzohjdjqubg3sp4`.

Apruzzese and Cong, *On Two Orderings of Lattice Paths*
(<https://arxiv.org/abs/2310.16963>), define the matching and Lagrange orders,
prove their common maximum, and pose cover classification.  Li's public
manuscript/source (<https://github.com/crabsatellite/lattice-path-orders>) gives
a global exact cover algorithm, local matching formulas, initial levels, and a
different nonlocal family.  Targeted source, repository, web, and graph searches
found no complete adjacent-fibre orientation theorem on `D(a,3)`.  This is an
apparent-novelty statement relative to those searches, not a historical-priority
claim.

Universal validity rests on the displayed prefix argument, the accepted
Lagrange chain and interior sign lemma, the two exact swap identities, and the
Fibonacci cancellations (4)--(7).  The finite audits corroborate rather than
prove the theorem.  Both checkers are bespoke Python, not proof-assistant
kernels.  Reproduction trusts CPython integer and `Fraction` semantics,
SHA-256, the operating system, and hardware.  There is no solver, floating
point, randomness, external dataset, generated input, or omitted large
certificate.
