# A two-parameter family of reversed Lagrange covers on `D(a,3)`

## Result

Let `x,y` be integers satisfying

```text
y >= 1,   x >= 2y+3,   gcd(x+y,3)=1,
```

and put `a=x+y`.  Define two rational-Dyck paths

```text
P_(x,y) = R^x U R^y U^2,
Q_(x,y) = R^(x-1) U^2 R^(y+1) U.
```

Then `Q_(x,y) <_L P_(x,y)` is a cover in the Lagrange order, while

```text
M(Q_(x,y)) > M(P_(x,y)).
```

Thus this Lagrange cover has the opposite orientation in the matching order.
Writing `d=x-y` and using `F_0=0`, `F_1=1`, the exact matching reversal is

```text
M(Q_(x,y)) - M(P_(x,y))
 = 2 (F_(2y+2) F_(2x-3) - 2F_(2d-4) - F_(2d-2))
 >= 10 F_(2d-3) > 0.
```

Equality in the displayed lower bound holds exactly when `y=1`.

Equivalently, at every coprime endpoint `a>=7` this gives
`floor((a-3)/3)` explicit reversed Lagrange covers, one for each

```text
1 <= y <= floor((a-3)/3),   x=a-y.
```

The member `y=1` starts at the known extra Lagrange coatom.  Every member with
`y>=2` is genuinely below the coatom layer, so the theorem supplies infinitely
many non-coatom discrepancies and a number of discrepancies growing linearly
with the endpoint.

Here `X <_L Y` means `L(X)<L(Y)`, and a cover has no realized Lagrange-score
level strictly between its endpoints.

## Why both paths are admissible

For a run triple `(r,s,t)`, the path

```text
R^r U R^s U R^t U
```

lies in `D(a,3)` exactly when

```text
r+s+t=a,   3r>=a,   3(r+s)>=2a.
```

The triple of `P_(x,y)` is `(x,y,0)`.  Its second nonfinal up-step occurs only
after all `a=x+y` right-steps, so it is admissible.  The triple of `Q_(x,y)` is
`(x-1,0,y+1)`.  Its restrictive prefix is the second up-step at horizontal
coordinate `x-1`, and

```text
3(x-1) >= 2(x+y)
```

is exactly `x>=2y+3`.  Hence both named words are in the carrier.

## Lagrange-cover mechanism

The complete `D(a,3)` Lagrange classification associates to a run triple its
decreasing rearrangement `(X,Y,Z)`.  Its distinct score levels, from greatest
to least, are ordered first by increasing `Z` and then by decreasing `X`.
Within a fixed `Z`, the next lower partition is

```text
(X,Y,Z) -> (X-1,Y+1,Z)    when X-Y>=2.
```

For the two named paths the sorted triples are

```text
P_(x,y): (x,y,0),
Q_(x,y): (x-1,y+1,0).
```

The hypothesis gives `x-y>=y+3>=4`, so these are consecutive partition
levels.  Therefore `Q_(x,y) <_L P_(x,y)` is a cover.  The classification,
including its symbolic certificates, is available at

<https://github.com/njallskarp/math_source_code_open/tree/main/rational_dyck_b3_lagrange>

from verified source commit
`343fbb6ce0d09166218ebcefa73b27fc775ee97b` and is the one theorem dependency
of the Lagrange-cover assertion.  Discovery Net review
`bafkreigxarbowliahciiy5siv7poaqymwob7hhfmm5gjac6r6m27kdwrj4` accepts that
classification with high confidence and independently reproduces it through
`a=120`.

## Exact matching reversal

Put

```text
K_n = [[F_(2n+3), F_(2n+1)],
       [F_(2n+1), F_(2n-1)]],
```

where `F_(-1)=1`, so `K_0=[[2,1],[1,1]]`.  For a run triple `(r,s,t)`, let

```text
q(r,s,t) = (K_r K_s K_t)_(2,1).
```

The cyclic coefficient matrix is `D` times the finite coefficient matrix,
where `D=[[2,1],[1,0]]`.  Its lower-left entry is therefore the upper-left
entry of the finite matrix, which is Schiffler's matching number.  Consequently

```text
M(R^r U R^s U R^t U) = q(r,s,t).
```

Let `C` denote the canonical orientation with triple `(x-1,y+1,0)`.  The
within-layer matrix identity

```text
K_x K_y - K_(x-1) K_(y+1)
 = 2 [[F_(2d-2), F_(2d)],
      [F_(2d-4), F_(2d-2)]]
```

and right multiplication by `K_0` give

```text
M(P_(x,y)) - M(C)
 = 2 (2F_(2d-4) + F_(2d-2)).                 (1)
```

The exact adjacent-swap identity

```text
q(i,j,k)-q(i,k,j) = -2F_(2(j-k))F_(2i-1)
```

with `(i,j,k)=(x-1,y+1,0)` gives

```text
M(Q_(x,y)) - M(C) = 2F_(2y+2)F_(2x-3).       (2)
```

Subtracting (1) from (2) proves the exact gap formula.  For positivity, put
`d=x-y`.  Because `y>=1`, monotonicity of positive-index Fibonacci numbers
gives

```text
F_(2y+2) F_(2x-3) >= 3 F_(2d-1).
```

The Fibonacci recurrence then yields the exact simplification

```text
3F_(2d-1) - 2F_(2d-4) - F_(2d-2) = 5F_(2d-3).
```

After multiplication by `2`, this proves the lower bound and strict
positivity.  Both monotonicity inequalities are equalities exactly at `y=1`.

## Reproduction

The artifact uses only the Python standard library.  It was tested under
CPython 3.12.12.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-a 60
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected principal markers:

```text
EXACT VERIFIED D(a,3) LAGRANGE-COVER MATCHING REVERSALS; x<=250; pairs=10127; noncoatom_pairs=9963; row_sha256=393bf7e522bf38e505bc89bd3e9845754dc4674409e2b38d438abab443d2f07c
INDEPENDENT VERIFIED D(a,3) cover reversals from definitions; 7<=a<=60; endpoints=36; paths=8595; pairs=342; noncoatom_pairs=306; row_sha256=2fe6817cec57ed4441f7c2d8a5567cc978238ea8c2ec634ed882438e069d8650
```

Five unit tests pass.

`verify.py` reconstructs the displayed matrices, matching scores, exact gap,
and positive lower bound for 10,127 coprime parameter pairs through `x=250`.
`independent_check.py` imports none of that code.  It recursively generates
every rational-Dyck word at all admissible endpoints through `a=60`, computes
matching scores with a scalar continuant, computes squared Lagrange scores at
every cyclic cut with exact `Fraction`, and checks adjacency of the two score
levels against the entire carrier.  The finite checks corroborate the theorem;
they are not substitutes for the displayed uniform argument.

## Literature and graph boundary

Apruzzese and Cong define the matching and Lagrange orders, prove the common
maximum, and pose cover classification:

- P. J. Apruzzese and K. Cong, *On Two Orderings of Lattice Paths*,
  <https://arxiv.org/abs/2310.16963>.

Li gives a global exact cover algorithm, parity and local formulas, initial
matching levels, and a different nonlocal matching-cover family:

- K. Li, *Lagrange Collisions and Cover Relations for Rational Dyck Paths*,
  source inspected at commit
  `845a030e87c39f24990dce48e5aad2e48d569318`,
  <https://github.com/crabsatellite/lattice-path-orders/tree/845a030e87c39f24990dce48e5aad2e48d569318>.

The committed graph already contains the general upper-coatom theorem, the
complete `D(a,2)` coincidence theorem, corrected finite `D(10,9)` cover data,
and the complete `D(a,3)` Lagrange classification.  This family refines the
last two structural layers by showing that linearly many height-three
Lagrange covers contain an explicitly oriented matching reversal.  Targeted
primary-source, repository-source, web, and graph searches found no statement
of this family.  This is search-relative apparent novelty, not a historical
priority claim.

## Trust boundary

Universal validity rests on the displayed rational-Dyck prefix check, the
published `D(a,3)` Lagrange-level theorem at source commit `343fbb6c...`, the
two displayed Fibonacci matrix identities, and the elementary positivity
argument.  The dependency theorem was independently accepted, verified, and
reproduced in Discovery Net at height 1915.  That review notes an implicit
coprimality bridge for one odd inter-layer boundary; the present theorem uses
only within-layer `z=0` transitions, so its application of the dependency does
not encounter that boundary.  The checkers are bespoke exact Python programs,
not proof-assistant kernels.  Reproduction additionally trusts CPython integer
and `Fraction` semantics, SHA-256, the operating system, and hardware.  There
is no solver, floating point, randomness, external dataset, generated input,
or omitted large certificate.
