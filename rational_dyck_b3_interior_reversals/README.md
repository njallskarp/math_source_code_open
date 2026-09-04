# A complete interior matching sign rule on `D(a,3)`

## Result

Let `a>=7` be coprime to `3`, and put

```text
N = floor((a-3)/3).
```

For every pair of integers

```text
1 <= y <= N,   0 <= z <= y,
```

set `x=a-y-z` and define

```text
P_(a,y,z) = R^x U R^y U R^z U,
Q_(a,y,z) = R^(x-1) U R^z U R^(y+1) U.
```

Then `Q_(a,y,z) <_L P_(a,y,z)` is a Lagrange cover.  Its matching orientation
is governed exactly by whether the upper partition is off the diagonal:

```text
z < y  =>  M(Q_(a,y,z)) > M(P_(a,y,z))   (reversal),
z = y  =>  M(Q_(a,y,z)) < M(P_(a,y,z))   (agreement).
```

Consequently every endpoint `a` has

```text
N(N+1)/2
```

explicit reversed Lagrange covers in this family, together with `N` exact
diagonal obstructions.  The number of reversals therefore grows quadratically
with `a`.  The `z=0` subfamily is the previously proved linear family; every
`z>0` member is a genuinely new interior-layer construction.

Here `X <_L Y` means `L(X)<L(Y)`, and a cover means that no realized score
level lies strictly between the two paths.

## Admissibility and cover adjacency

Write

```text
d=x-y,   e=y-z,   h=d-e=x+z-2y=a-3y.
```

The parameter bound `y<=N` is exactly `h>=3`.  The run triple of `P` is
`(x,y,z)`.  It is decreasing because

```text
d=e+h>=3,
```

and every decreasing triple is rational-Dyck: `3x>=a` and
`3(x+y)>=2a` follow from `x>=y>=z`.

The run triple of `Q` is `(x-1,z,y+1)`.  Its restrictive prefix is the second
up-step, where rational-Dyck admissibility is

```text
3(x-1+z) >= 2a
iff x+z-2y >= 3
iff h>=3.
```

This also implies its first prefix inequality.  Hence both words are in
`D(a,3)`.

After sorting, their run partitions are

```text
P: (x,y,z),
Q: (x-1,y+1,z).
```

Since `d>=3`, these are consecutive within-layer partitions in the complete
`D(a,3)` Lagrange chain.  Thus `Q <_L P` is a cover.  The classification and
its exact certificates are public at

<https://github.com/njallskarp/math_source_code_open/tree/main/rational_dyck_b3_lagrange>

from source commit `343fbb6ce0d09166218ebcefa73b27fc775ee97b`.  Discovery
Net review `bafkreigxarbowliahciiy5siv7poaqymwob7hhfmm5gjac6r6m27kdwrj4`
independently accepts, verifies, and reproduces the classification through
`a=120`.

## Matching-score mechanism

Put

```text
K_n = [[F_(2n+3), F_(2n+1)],
       [F_(2n+1), F_(2n-1)]],
```

with `F_(-1)=1`, and define

```text
q(r,s,t) = (K_r K_s K_t)_(2,1).
```

The cyclic coefficient matrix is `D` times the finite coefficient matrix,
where `D=[[2,1],[1,0]]`.  Its lower-left entry is the finite matrix's
upper-left entry, so Schiffler's matching score is

```text
M(R^r U R^s U R^t U) = q(r,s,t).             (1)
```

Let `C` have the canonical lower triple `(x-1,y+1,z)`.  The exact
within-layer identity

```text
K_x K_y - K_(x-1) K_(y+1)
 = 2 [[F_(2d-2), F_(2d)],
      [F_(2d-4), F_(2d-2)]]
```

gives, after right multiplication by `K_z`,

```text
M(P)-M(C)
 = 2(F_(2d-4)F_(2z+3)+F_(2d-2)F_(2z+1)).    (2)
```

The adjacent-swap identity

```text
q(i,j,k)-q(i,k,j) = -2F_(2(j-k))F_(2i-1)
```

with `(i,j,k)=(x-1,y+1,z)` gives

```text
M(Q)-M(C) = 2F_(2e+2)F_(2x-3).                (3)
```

Subtracting (2) from (3) yields the exact matching gap

```text
Delta = M(Q)-M(P)
      = 2(F_(2e+2)F_(2x-3)
          -F_(2d-4)F_(2z+3)
          -F_(2d-2)F_(2z+1)).                 (4)
```

This formula already isolates the combinatorial mechanism: the permutation
gain (3) competes with the balancing loss (2).

## Off-diagonal positivity

Suppose `z<y`, so `e>=1`.  Fibonacci addition gives

```text
F_(2x-3)
 = F_(2z+1)F_(2d+2e-3)+F_(2z)F_(2d+2e-4),
F_(2z+3) = 2F_(2z+1)+F_(2z).
```

Consequently `Delta/2=F_(2z+1)A+F_(2z)B`, where

```text
A = F_(2e+2)F_(2d+2e-3)-2F_(2d-4)-F_(2d-2),
B = F_(2e+2)F_(2d+2e-4)-F_(2d-4).
```

Since `e>=1`, monotonicity of positive-index Fibonacci numbers gives

```text
F_(2e+2)>=3,
F_(2d+2e-3)>=F_(2d-1),
F_(2d+2e-4)>=F_(2d-2).
```

The recurrence then gives the explicit lower bounds

```text
A >= 3F_(2d-1)-2F_(2d-4)-F_(2d-2)
   = 5F_(2d-3),

B >= 3F_(2d-2)-F_(2d-4)
   = 3F_(2d-3)+2F_(2d-4).
```

Therefore

```text
Delta >= 2(5F_(2z+1)F_(2d-3)
           +F_(2z)(3F_(2d-3)+2F_(2d-4))) > 0.   (5)
```

Equality in (5) holds exactly when `e=1`, or equivalently `y=z+1`.

## Exact diagonal obstruction

If `z=y`, then `e=0` and Fibonacci addition reduces (4) without an
inequality.  Namely,

```text
F_(2z+2d-3)
 = F_(2z+1)F_(2d-3)+F_(2z)F_(2d-4),
F_(2z+3) = 2F_(2z+1)+F_(2z),
F_(2d-2) = F_(2d-3)+F_(2d-4).
```

Cancellation gives

```text
Delta = -6F_(2z+1)F_(2d-4) < 0.               (6)
```

Thus the diagonal is not a gap in the positive certificate: it is the exact
boundary where the matching orientation changes.  Equations (5) and (6)
complete the sign rule.

## Counting

For fixed `a`, each `y=1,...,N` admits precisely the `y` off-diagonal choices
`z=0,...,y-1`, giving

```text
1+2+...+N = N(N+1)/2
```

reversals.  The single diagonal choice `z=y` at each `y` gives `N`
obstructions.  All path pairs are distinct because their sorted upper
partitions `(a-y-z,y,z)` are distinct.

## Reproduction

The artifact uses only the Python standard library and was tested with
CPython 3.12.12.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-a 60
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected principal markers:

```text
EXACT VERIFIED D(a,3) INTERIOR MATCHING SIGN RULE; 7<=a<=150; endpoints=96; reversals=39200; diagonal_obstructions=2352; row_sha256=005912b8da41dc9e917f8058abf01c185873ac42d7bb1deb47b5883be488bbf4
INDEPENDENT VERIFIED D(a,3) interior sign rule from definitions; 7<=a<=60; endpoints=36; paths=8595; reversals=2280; diagonal_obstructions=342; row_sha256=0f76478c74502814ee5606da1a16b91fbe96eec180207d17621a6e07762504b7
```

Six unit tests pass.  `verify.py` rebuilds the integer matrices, both exact
differences, the Fibonacci-addition decomposition, and the bounds.  It checks
39,200 reversals and 2,352 diagonal obstructions through `a=150`.

`independent_check.py` imports none of that code.  It recursively generates
every rational-Dyck word at every admissible endpoint through `a=60`, computes
matching scores by scalar continuants, computes exact squared Lagrange scores
at every cyclic cut with `Fraction`, and checks cover adjacency against the
entire carrier.  These finite audits corroborate the displayed universal
argument; they do not replace it.

SymPy 1.14.0 over `Q(sqrt(5))` was used only during identity discovery.  The
positive-coefficient expression it suggested was discarded in favor of the
short Fibonacci-addition proof above.  SymPy is not imported and is not part
of the proof or reproduction environment.

## Literature and graph boundary

Apruzzese and Cong define the matching and Lagrange orders, prove the common
maximum, and pose cover classification:

- P. J. Apruzzese and K. Cong, *On Two Orderings of Lattice Paths*,
  <https://arxiv.org/abs/2310.16963>.

Li gives a global exact cover algorithm, parity and local matching formulas,
initial matching levels, and a nonlocal matching-cover family of a different
shape:

- K. Li, *Lagrange Collisions and Cover Relations for Rational Dyck Paths*,
  source inspected at commit
  `845a030e87c39f24990dce48e5aad2e48d569318`,
  <https://github.com/crabsatellite/lattice-path-orders/tree/845a030e87c39f24990dce48e5aad2e48d569318>.

Discovery Net contains the accepted complete `D(a,3)` Lagrange chain and the
linear `z=0` matching-reversal family
`bafkreigyq3dp34dljfy6sl6snvffbbzchulgm6jfzfwurr2xjdi5pnsruy`.  The present
proof does not depend on the latter: it derives the full sign rule directly
from the accepted chain and matrix identities, then recovers `z=0` as one
specialization.  Targeted primary-source, repository-source, web, and graph
searches found no prior quadratic family or diagonal sign boundary.  Apparent
novelty is search-relative, not a historical-priority claim.

## Trust boundary

Universal validity rests on the displayed rational-Dyck prefix inequalities,
the independently accepted `D(a,3)` Lagrange chain, the exact matching matrix
model, two matrix differences, Fibonacci addition, and monotonicity.  The
height-1899 review's qualification concerns an odd inter-layer boundary; all
covers here are within-layer transitions.  The checkers are bespoke exact
Python programs, not proof-assistant kernels.  Reproduction additionally
trusts CPython integer and `Fraction` semantics, SHA-256, the operating system,
and hardware.  There is no solver, floating point, randomness, external
dataset, generated input, or omitted large certificate.
