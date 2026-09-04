# Complete Lagrange-cover classification on `D(a,3)`

## Result

Let `a>3` and `gcd(a,3)=1`.  Every path in the rational-Dyck set
`D(a,3)` has a unique run form

```text
R^r U R^s U R^t U,
```

where

```text
r+s+t=a,   3r>=a,   3(r+s)>=2a.
```

Associate to the path the partition obtained by sorting `(r,s,t)`:

```text
(x,y,z),   x>=y>=z>=0,   x+y+z=a.
```

The Lagrange-score levels on `D(a,3)` are exactly the fibres of this
partition map.  From greatest score to least score, the partitions form the
single chain

```text
(x,y,z) before (x',y',z')
iff z<z', or z=z' and x>x'.
```

Consequently all Lagrange covers are explicit.  Every path in one level is
covered by every path in the preceding level.  The next lower partition is

```text
(x-1,y+1,z)                    if x-y>=2,
(a-2z-2,z+1,z+1)              if x-y is 0 or 1 and z<floor(a/3).
```

The final partition has no lower cover.  Thus the result completely solves
the Lagrange half of the cover-classification problem on the infinite
height-three family.  The theorem does not classify the matching covers on
`D(a,3)`.

## Exact reduction

Write

```text
T(c) = [[c,1],[1,0]],
D = T(2),
E = T(1)^2 = [[2,1],[1,1]].
```

An unequal adjacent pair of path steps contributes `D`; an equal pair
contributes `E`.  Closing the word cyclically adds an initial `D`.  For a
canonical run triple `(x,y,z)`, the cyclic period matrix is

```text
K_x K_y K_z,
K_n = [[F_(2n+3), F_(2n+1)],
       [F_(2n+1), F_(2n-1)]],
```

with `F_(-1)=1`, so `K_0=E`.  This follows from
`K_n=D E^(n-1) D` for `n>=1`; the same product also covers a zero run.

For any cyclic digit cut with product `[[p,r],[q,s]]`, the corresponding
quadratic fixed-point gap is

```text
sqrt(trace^2-4)/q.
```

Apruzzese--Cong's `{1,2}` periodic-maximum lemma shows that a maximizing cut
starts at a `2`.  Direct block inspection identifies the denominator at any
such cut with

```text
Q(i,j,k) = (K_i K_j K_k)_(2,1)
```

for one of the available permutations of `(x,y,z)`.  The adjacent-swap
identities

```text
Q(i,j,k)-Q(j,i,k) = -2 F_(2(i-j)) F_(2k+3),
Q(i,j,k)-Q(i,k,j) = -2 F_(2(j-k)) F_(2i-1)
```

show that the least denominator is

```text
Q=Q(x,y,z)
```

when `x>=y>=z`.  (When a run is zero, the actual cuts give a subset of the
same permutation list and still include the sorted cut.)  Because the `K_n`
are symmetric, cyclic trace invariance together with transposition makes
`trace(K_x K_y K_z)` invariant under all six permutations.  Hence all valid
permutations of one partition have the same Lagrange score.

Put

```text
T = trace(K_x K_y K_z),
A = F_(2y+1) F_(2(x-z)-2).
```

The Fibonacci recurrence and d'Ocagne identity give the key formula

```text
T = 3Q + 6A,
L(x,y,z)^2 = (T^2-4)/Q^2.
```

It remains to compare consecutive partitions.  In both kinds of transition
the proof establishes

```text
T_1>T_2,   Q_1>Q_2,   A_1/T_1>A_2/T_2.
```

The last inequality implies

```text
T_1/Q_1 = 3/(1-6A_1/T_1) > 3/(1-6A_2/T_2) = T_2/Q_2.
```

Together with `Q_1>Q_2`, this makes both terms in

```text
L^2 = (T/Q)^2 - 4/Q^2
```

strictly greater for the first partition.

### Within a fixed `z`

For `d=x-y>=2`, balancing the first two parts uses
`(x,y,z)->(x-1,y+1,z)`.  The exact identity

```text
K_x K_y - K_(x-1) K_(y+1)
 = 2 [[F_(2d-2), F_(2d)],
      [F_(2d-4), F_(2d-2)]]
```

proves the trace and denominator decreases after right multiplication by
`K_z`.  The `A/T` cross-product is the 11-term positive coefficient
certificate recorded in `CERTIFICATE.json` and reconstructed by `verify.py`.

### Between consecutive `z` layers

If `a-z=2h`, the boundary step is

```text
(h,h,z) -> (2h-z-2,z+1,z+1),   h-z>=2.
```

If `a-z=2h+1`, it is

```text
(h+1,h,z) -> (2h-z-1,z+1,z+1),   h-z>=1.
```

Set `lambda=phi^2`, where `phi=(1+sqrt(5))/2`.  In the even case substitute

```text
lambda^h = lambda^z lambda^2 (1+u),
```

and in the odd case substitute

```text
lambda^h = lambda^z lambda (1+u).
```

In both cases also set `lambda^z=1+v`; here `u,v>=0`.  After multiplication
by explicitly recorded positive Laurent monomials, each of

```text
T_1-T_2,   Q_1-Q_2,   A_1 T_2-A_2 T_1
```

has strictly positive coefficients in `Q(phi)[u,v]`.  The certificate has
seven polynomial records and 378 positive terms in total.  The verifier
reconstructs every matrix expression in `Q(phi)`, performs the substitutions,
checks exact coefficient signs under `phi=(1+sqrt(5))/2`, and compares
canonical coefficient-stream hashes with `CERTIFICATE.json`.  SymPy was used
only during discovery; it is not imported and is not part of the proof.

The within-layer and parity-boundary steps exhaust consecutive partitions,
so distinct partitions have strictly distinct scores in exactly the displayed
order.  This completes the classification.

## Reproduction

Tested with CPython 3.12.12; there are no third-party dependencies.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-a 60
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected principal markers:

```text
SYMBOLIC VERIFIED D(a,3) Lagrange partition chain; certificates=7; positive_terms=378; certificate_sha256=10da7d2ef006c68d53dbac3388d60e93255fc3927b7b6e4c4f866a21fd2df0a6
INDEPENDENT VERIFIED D(a,3) Lagrange levels from definitions; 4<=a<=60; endpoints=38; paths=8607; levels=4617; level_sha256=ac07eafcf4958ea8deb6924beee4f37b9f7b198804685e2e0b998806f122225e
```

Five unit tests pass.

`independent_check.py` does not import the symbolic verifier.  It recursively
generates the binary Dyck words, encodes adjacent steps literally, and computes
every cyclic Lagrange square with scalar continuants and `Fraction`.  It checks
the partition fibres and their complete order at every admissible endpoint
through the requested bound.

## Literature boundary

Apruzzese and Cong define the two score orders, prove the common maximum, and
pose the cover-classification problem:

- M. Apruzzese and T. Cong, *On Two Orderings of Lattice Paths*,
  <https://arxiv.org/abs/2310.16963>.

Li gives a general exact best-first cover algorithm, prefix certificates,
endpoint parity, local formulas, first matching levels, and a nonlocal matching
cover family, but does not state the partition-chain classification for
`D(a,3)`:

- K. Li, *Lagrange Collisions and Cover Relations for Rational Dyck Paths*,
  source inspected at commit
  `845a030e87c39f24990dce48e5aad2e48d569318`,
  <https://github.com/crabsatellite/lattice-path-orders>.

The committed Discovery Net neighborhood already contains a corrected exact
`D(10,9)` cover census, the uniform upper-coatom theorem, and the complete
`D(a,2)` chain.  This result is intended as the next family-level Lagrange
classification.  Apparent novelty is relative to the targeted primary-source,
repository-source, web, and committed-graph searches, not a historical-priority
claim.

## Trust boundary

Universal validity rests on the displayed reduction, Fibonacci identities,
Apruzzese--Cong's periodic-maximum lemma, and the exact positive-coefficient
certificates.  `verify.py` is a small bespoke symbolic checker over
`Q(phi)`; it is not a proof-assistant kernel.  The finite checker is independent
corroboration, not the proof of the universal statement.  Reproduction trusts
the inspected source, CPython exact integer and `Fraction` semantics, SHA-256,
the operating system, and hardware.  There is no solver, floating point,
randomness, external dataset, generated search input, or omitted large
certificate.
