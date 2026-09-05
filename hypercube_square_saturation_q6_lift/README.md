# A Q6 live-facet lift for square saturation

## Result

For every integer `d >= 6`,

```text
sat(Q_d,Q_2) >= 39270 d 2^d / (21779 d + 56761).   (1)
```

Consequently,

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 39270/21779.
```

This exceeds the preceding `39984/22175` constant by exactly
`714/482949325`.  The full finite bound also improves its predecessor for
every `d >= 6`.

## Dependency and exact target

The [preceding Q5 compatibility lemma][q5] proves that every nonempty
square-free edge set in a copy `K` of `Q5` satisfies

```text
delta_K := 34 S_K - 12 E_K >= 1,                 (2)
```

where `E_K` is its number of selected edges and `S_K` is the sum of the
inherited `Q3` slack over its 40 three-subcubes.  This note proves the next
structural lift, not a larger enumeration:

```text
102 S_L - 60 E_L >= E_L/11                       (3)
```

for every square-free edge set in a copy `L` of `Q6`.

## Live-facet support capacity

Call one of the twelve `Q5` facets of `L` *live* when it contains a selected
edge, and let `k` be the number of live facets.  Each `Q3` is contained in
three `Q5` facets and each edge in five.  Summing (2) over the live facets
therefore gives

```text
102 S_L - 60 E_L = sum_K delta_K >= k.            (4)
```

It remains to prove `E_L <= 11k`.  Group the twelve facets into the six
opposite pairs belonging to the six coordinates.  Let `(a,b,c)` count pairs
with respectively two, one, or zero live facets.  Thus

```text
a+b+c=6,    k=2a+b.
```

An edge in direction `i` belongs to one facet from every pair except pair
`i`.  Consequently the number `C(a,b,c)` of edges supported by a live-facet
set is exactly:

```text
c >= 2:  C(a,b,c) = 0;
c = 1:   C(a,b,c) = 2^a;
c = 0:   C(a,b,0) = a 2^(a-1) + b 2^a,
          with the first term zero when a=0.       (5)
```

For `c=1`, the edge direction must be the unique empty coordinate and every
single live pair fixes one position bit.  For `c=0`, a direction belonging to
a double pair leaves `a-1` free bits, while a direction belonging to a single
pair leaves `a` free bits.  This proves (5) without computation.

Maximizing (5) for fixed `k` gives:

```text
k:       0 1 2 3 4 5 6  7  8  9 10  11  12
max C:   0 0 0 0 0 1 6 11 20 36 64 112 192.
```

Hence `E_L <= 11k` for `k <= 11`.  For `k=12`, use the published exact
extremal value

```text
ex(Q6,C4)=132=11*12.                              (6)
```

Equations (4)--(6) give (3).  The value (6) is the one new external input:
H. Harborth and H. Nienborg, *Maximum number of edges in a six-cube without
four-cycles*, Bulletin of the ICA 12 (1994), 55--60.  An
[author-uploaded primary copy and record][hn] is available online.

## Global double count

From (3),

```text
S_L >= 661 E_L/1122.                              (7)
```

In `Q_d`, every `Q3` lies in `C(d-3,3)` six-subcubes and every edge lies in
`C(d-1,5)`.  Since

```text
C(d-1,5)/C(d-3,3) = (d-1)(d-2)/20,
```

summing (7) gives

```text
S >= 661 E(d-1)(d-2)/22440.                       (8)
```

The inherited square-saturation identities are

```text
B+3A = (d-1)E-3M,
B+3A >= M/2 + S/(d-2),
M = d 2^(d-1)-E.
```

Substitution of (8) yields

```text
21779(d-1)E >= 78540M,
(21779d+56761)E >= 78540 d 2^(d-1),
```

which is (1).  Direct cross-multiplication against the preceding finite bound
leaves the positive numerator `714(d-1)`.  The asymptotic difference is
`714/(21779*22175)=714/482949325`.

## Reproduction

CPython 3.11 or later is sufficient; there are no third-party dependencies.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The checker constructs all 192 edges, 240 squares, and twelve `Q5` facets of
`Q6`.  It compares the definition-level capacity with formula (5) for all
4,096 live-facet sets, hashes that entry-level audit, verifies the maximum
table, and checks all rational simplifications.

## Primary-source and overlap status

The exact extremal input (6) has primary status through the 1994
Harborth--Nienborg paper.  Searches before publication found no prior
inequality (3), no square-saturation use of its live-facet capacity formula,
and no occurrence of `39270/21779`.  The committed graph likewise had no
relevant `Q6` node and no incoming review on the Q5 dependency.  Concurrent
standing work on `R(5,5)` and Albertson's conjecture is disjoint.

## Trust boundary

The live-pair classification and the all-dimensional double count are human
proofs.  `verify.py` corroborates every one of the 4,096 finite support cases
and the exact arithmetic with CPython integers and `fractions.Fraction`.  It
does not reprove either the preceding Q5 lemma or the external theorem
`ex(Q6,C4)=132`; those are explicit cited dependencies.  No solver,
floating-point arithmetic, generated database, or hidden artifact is used.

[q5]: https://github.com/njallskarp/math_source_code_open/tree/main/hypercube_square_saturation_q5_compatibility
[hn]: https://www.researchgate.net/publication/244468901_Maximum_number_of_edges_in_a_six-cube_without_four-cycles
