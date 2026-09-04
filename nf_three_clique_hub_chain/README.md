# NF-number of a hubbed three-clique chain

## The graph and theorem

For `m >= 3`, let `H_m` have three pairwise disjoint vertex sets

```text
X={x_0,x_1,x_2},  Y={y_0,...,y_(m-1)},  Z={z_0,z_1,z_2}.
```

Put a clique on each of `X`, `Y`, and `Z`, and add precisely the two bridge
edges `x_0 y_0` and `y_0 z_0`.  Thus both bridges use the same distinguished
vertex of the middle clique.  Regard the graph as a one-dimensional
simplicial complex.  With the convention that the NF-number is the first
positive return up to simplicial-complex isomorphism, the result is

```text
NF(H_m) = m + 8  for every m >= 3.
```

The proof is computer-assisted only in a finite, parameter-independent part:
an exact 72-cell product-poset certificate checks nine activation transitions,
15 clipping regimes, and five endpoint identities.  The arbitrarily long
part of the orbit follows from a strictly order-reversing weight invariant.

## Lossless symmetry quotient

Put `q=m-1`.  The group

```text
S_2(X-{x_0}) x S_q(Y-{y_0}) x S_2(Z-{z_0})
```

acts on every NF iterate.  A subset orbit has type

```text
(a,i,b,j,c,k) in {0,1} x [0,2] x {0,1} x [0,q] x {0,1} x [0,2],
```

where the bits record the three distinguished vertices and the integers
record the ordinary vertices in the corresponding clique.  One representative
of a type can be contained in a representative of another type exactly when
all six coordinates compare.  Consequently this quotient preserves both the
NF operation and maximality; it is not a sampling reduction.

Suppress the variable middle coordinate and write

```text
z=(a,i,b,c,k) in P={0,1}x[0,2]x{0,1}x{0,1}x[0,2].
```

The poset `P` has 72 elements and 204 cover relations.  If an invariant facet
antichain is `E`, then the largest allowed middle height over `z` in its next
NF complex is exactly

```text
h_E(z) = min({j-1 : (u,j) in E and u <= z} union {q}).              (1)
```

Delete negative heights and retain the coordinatewise-maximal fibre tops.
Formula (1) is simply the definition of the Stanley--Reisner complex of the
facet ideal: a type is allowed precisely when it contains no old facet type.

## Exact orbit recurrence

The file `verify.py` contains nine explicit affine type antichains
`P_0,...,P_8`, written in unpacked `base:height` form.  Here `P_0` is exactly
the edge set of `H_m`.  Direct substitution in (1) gives

```text
P_0 -> P_1 -> ... -> P_8 -> A_(q+2).                               (2)
```

For `q>=9`, every entry in (2) is either constant or `q-r`; the checker proves
all nine arrows by exact affine inequalities.  The seven values `q=2,...,8`
exhaust every possible lower clip and are checked entry-for-entry.  This is an
all-parameter split, not a finite extrapolation.

To define the wave, index each local end type `(a,i)` by `3a+i`.  Let
`w(a,i,b,c,k)` be minus the corresponding entry of the following matrix,
using the first matrix when `b=0` and the second when `b=1`:

```text
b=0                                      b=1
0 2 3 2 3 5                              1 3 4 4 5 6
2 3 4 3 4 6                              3 4 5 5 6 7
3 4 5 4 5 7                              4 5 6 6 7 8
2 3 4 3 4 6                              4 5 6 5 6 7
3 4 5 4 5 7                              5 6 7 6 7 8
5 6 7 6 7 8                              6 7 8 7 8 9
```

Thus `w` takes values from `-9` through `0`.  Define

```text
A_s = Max{(z,s+w(z)) : 0 <= s+w(z) <= q}.
```

The 204 cover checks prove that `w(z)>w(z')` whenever `z` is covered by
`z'`.  Hence surviving wave tops never dominate one another.  Applying (1)
gives

```text
A_s -> A_(s-1)  for 5 <= s <= q+2.                                 (3)
```

There are only 15 possible clipping patterns in (3).  Indeed the lower test
depends on whether `s` is `5,6,7,8`, or at least `9`, because `min(w)=-9`;
the upper test depends on whether `q-s` is `-2`, `-1`, or nonnegative.  A
simultaneous translation of `s` and `q` preserves a pattern and every height
difference.  The checker applies (1) to one exact representative of every one
of these 5-by-3 regimes.

The final state is the following 14-top antichain `T`, again in
`base:height` notation (the height-3 top is clipped when `q=2`):

```text
00000:3 00001:1 00010:1 00012:0 00100:2 00101:0 01000:1
01001:0 01010:0 01100:0 10000:1 10001:0 10010:0 12000:0
```

The endpoints are

```text
A_4 -> T -> P_0.                                                    (4)
```

For the first arrow, `q=2,3` are the only upper clips and `q>=4` is stable.
For the second, `q=2` is checked separately and a single exact affine
calculation proves every `q>=3` case.  Combining (2)--(4), the labelled orbit
is

```text
P_0,...,P_8,A_(q+2),A_(q+1),...,A_4,T,P_0.
```

It contains

```text
9 + (q-1) + 1 = q+9 = m+8
```

states before return.

This is also the first return up to isomorphism.  The initial state is a graph,
so all its facets have size two.  Every other displayed state has a facet of
size at least three.  Explicit witnesses for `P_1,...,P_8` are visible in the
prefix table.  In the wave, use a weight `-2` base at `s=q+2`, the weight `-1`
base at `s=q+1`, and the weight-zero base when `s<=q`.  State `T` has a
three-element facet even at `q=2`.  Facet cardinalities are isomorphism
invariants, excluding every earlier unlabelled return.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter; standard
library only.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --max-m 80
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-m 6
PYTHONDONTWRITEBYTECODE=1 python3 compare_boolean.py --max-m 6
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected primary result:

```text
VERIFIED hubbed K3--Km--K3 all-parameter NF recurrence; m=3..80; cases=78; transitions=3861; symbolic_prefix=9; small_prefix=63; weight_covers=204; wave_regimes=15; endpoints=5; NF(H_m)=m+8
ORBIT_SHA256=2d3ab0e6e0ef6a4fb069154dd085dbb1f477a81d092e423fdb02977ac2be91bc
```

Expected independent result:

```text
INDEPENDENT VERIFIED Boolean-lattice hubbed K3--Km--K3 orbits; m=3..6; cases=4; states=50; facets_seen_with_multiplicity=7820; labelled_period=m+8; no earlier isomorphic return
ORBIT_SHA256=78d7f9828d768235a50023b65fd77eb823f63c76c6c9468ae0c47ef8c45a9397
```

Expected entry-level bridge:

```text
MATCHED type and Boolean facets entry-for-entry; m=3..6; cases=4; states=50; facets=7820
EXPANDED_ORBIT_SHA256=78d7f9828d768235a50023b65fd77eb823f63c76c6c9468ae0c47ef8c45a9397
```

All five unit tests pass.

`verify.py` uses the lossless orbit-type quotient and separately distinguishes
the finite symbolic proof from the optional `m<=80` stress regression.
`independent_check.py` imports no target code or orbit types: it constructs the
labelled graph from edges, enumerates every Boolean subset, and applies the
defining maximal-nonface operation directly.  `compare_boolean.py` is a
separate bridge that expands every type orbit and matches all 7,820 small-case
facets entry-for-entry, rather than comparing only aggregate periods.

## Literature and graph boundary

Hibi and Mahmood introduced the NF-number and proved the `n+m+2` formula for a
disjoint union of two cliques, not this three-clique bridge tree:

<https://arxiv.org/abs/2005.01247>

Rather's 2026 paper treats the first two dumbbell iterates, complete split
graphs, and double stars.  Its conclusion explicitly names block graphs as a
natural open candidate for structured NF dynamics, but it does not state this
family or formula:

<https://arxiv.org/abs/2605.30781>

The Discovery Net height-1885 review of the complete dumbbell classification
independently identified trees of clique blocks as the next conjectural
extension.  A graph refresh through height 1894 and targeted primary-source
searches on 2026-09-04 found no duplicate of this theorem.  This is a
search-relative novelty statement, not a historical-priority claim.

## Trust boundary and scope

Universal validity rests on the coordinatewise fibre lemma, the unpacked
affine prefix certificate, strict order reversal on the complete 204-cover
base poset, the exhaustive 15 wave-clipping regimes, and the endpoint checks.
The `m<=80` run and small Boolean replay are regression and independent
validation; they are not the induction step.  Correctness trusts inspection of
the finite certificate and CPython integer/set semantics.  There is no solver,
floating point, randomness, generated input, external dataset, omitted large
certificate, or unlisted dependency.

The theorem covers only the three-block family with triangular end cliques and
both bridges incident to one middle distinguished vertex.  It does not cover
arbitrary end widths, distinct middle bridge endpoints, or general block
graphs.
