# NF-number of an all-width three-clique hub chain

## The theorem

Let `n,m,ell >= 3`.  Take pairwise disjoint sets `X,Y,Z` of sizes
`n,m,ell`, make each one a clique, distinguish vertices `x in X`, `y in Y`,
`z in Z`, and add exactly the bridge edges `xy` and `yz`.  Denote the
resulting graph by `H(n,m,ell)` and regard it as a one-dimensional simplicial
complex.  Then

```text
NF(H(n,m,ell)) = n + m + ell + 2.
```

The statement uses the usual first-return-up-to-isomorphism convention.  It
strictly generalizes the previously proved `K3--Km--K3` hub-chain ray: all
three clique widths now vary independently.

## Lossless type quotient

Write `X'=X-{x}`, `Y'=Y-{y}`, and `Z'=Z-{z}`.  Every iterate is invariant
under

```text
S_(n-1) x S_(m-1) x S_(ell-1).
```

A subset has type

```text
(a,i,b,j,c,k) in {0,1}x[0,n-1]x{0,1}x[0,m-1]x{0,1}x[0,ell-1],
```

where the bits record the hubs and the integers record ordinary vertices.
One representative of type `u` is contained in a representative of type `v`
if and only if `u <= v` coordinatewise.  The quotient therefore preserves
the NF operation and maximality exactly; it is not a sampling reduction.

For a type `u`, let `|u|` be the sum of its coordinates.  Equivalently, for a
subset `A` let `|A|` be its cardinality.  Define

```text
                 +1  if A contains X, Y, or Z, or contains xy or yz;
epsilon(A) =      -1  if A meets at most one of X,Y,Z and the first case fails;
                  0  otherwise,

kappa(A) = |A| + epsilon(A).
```

This statistic is invariant on type classes.  It is also strictly increasing
under proper inclusion: adding vertices never decreases `epsilon`, and it
increases cardinality.

For `2 <= s <= n+m+ell-2`, define the explicit antichain

```text
B_s = {A subset V : kappa(A)=s}
      union {Q in {X,Y,Z} : |Q|=s+1}.                         (1)
```

The second term fills the unique two-rank gap made by a whole clique: a block
`Q` of size `r` has `kappa(Q)=r+1`, while its proper subsets lying in that
block have `kappa <= r-2`.  Thus `Q` is placed in both `B_(r-1)` and
`B_(r+1)`.

## The exact all-parameter recurrence

Let `N=n+m+ell`, and let `[u]` denote the complete orbit of subsets of type
`u`.  Put `U=(1,n-1,1,m-1,1,ell-1)`.  The five startup antichains are as
follows; a displayed type stands for its complete type class.

```text
P_0:
110000 020000 001100 000200 000011 000002 101000 001010

P_1:
010101 010110 011001 100101 100110

P_2:
(0,0,1,m-1,1,ell-1)  (1,0,1,0,1,ell-1)
(1,n-1,0,0,1,ell-1)  (1,n-1,1,m-1,0,0)
(1,n-1,1,0,1,0).
```

Here the undelimited six-digit notation is used only when every entry is a
single digit.  The remaining two startup states are most compactly written
as complements from `U`:

```text
P_3 = { U-d : d in D_3 },
D_3 = {
  101000,100100,100010,100001,011000,
  010010,010001,001010,001001,000110
};

P_4 = { U-d : d in D_4 },
D_4 = {
  110000,101010,101001,100110,020000,
  011010,011001,010100,001100,000200,
  000101,000011,000002
}.
```

The complete labelled orbit is

```text
P_0 -> P_1 -> P_2 -> P_3 -> P_4
    -> B_(N-2) -> B_(N-3) -> ... -> B_3 -> B_2 -> P_0.       (2)
```

Thus (2) contains `5+(N-3)=N+2` states before return.  Formula (1), rather
than a table whose size grows with a clique width, describes every facet in
the arbitrarily long portion of the orbit.

## Proof of the recurrence

For an antichain `A` in a finite subset poset, the facets after one NF step
are

```text
D(A) = Max( 2^V - Up(A) ),                                  (3)
```

because a subset is allowed precisely when it contains no old facet.

It is useful to regard (1) as a multivalued rank.  Set

```text
Lambda(A) = {kappa(A)} union {|Q|-1 : A=Q in {X,Y,Z}}.
```

Then `B_s={A:s in Lambda(A)}`.  The following elementary rank-filling lemma
is the structural part of the proof.

**Rank-filling lemma.**  Let all three blocks have size at least three.

1. If `3 <= r <= min(kappa(T),N-2)`, some subset `A subset T` has
   `r in Lambda(A)`, with one exception: if `T` is itself a block of size
   `r`, rank `r` is absent below `T`.
2. If `kappa(T) <= r <= N-3`, some superset `C superset T` has
   `r in Lambda(C)`.

Here is a direct proof.  Away from a whole block, a set has one of three
forms: it lies in at most one block and has corrected size `|A|-1`; it meets
at least two blocks without a bridge and has corrected size `|A|`; or it
contains a bridge or a whole block and has corrected size `|A|+1`.

For the downward assertion, if `T` has correction `-1`, take `r+1`
vertices in its occupied block.  If its correction is zero, either take an
`r`-set meeting two occupied blocks, or, when one occupied block is large
enough, take an `r+1`-set inside that block.  If its correction is `+1` and a
bridge is present, retain that bridge and extend it to `r-1` vertices.  If
the positive correction comes only from a whole block `Q`, use an `r+1`
proper subset of `Q` for `r<=|Q|-2`, use the extra label on `Q` for
`r=|Q|-1`, and retain `Q` plus arbitrary vertices for `r>=|Q|+1`.  At
`r=|Q|`, replace one vertex of `Q` by a vertex of `T-Q`; choose the removed
vertex to be the hub if the added vertex is an adjacent hub.  This gives an
`r`-set meeting two blocks with no bridge.  That replacement is unavailable
exactly when `T=Q`, which is the stated exception.

For the upward assertion, a positive set stays positive, so extend it to
`r-1` vertices.  Starting from a zero-correction set, add vertices until
either positivity first appears (then extend the positive set to `r-1`
vertices) or cardinality `r` is reached while the correction remains zero.
At the final addition, a safe vertex exists: `r<=N-3` leaves at least four
vertices outside, while a bridge-free set can make at most three missing
vertices dangerous (the possible completion vertices and missing adjacent
hubs overlap whenever both kinds occur).  Finally, from a set lying in one
block `Q`, use an `r+1` proper subset of `Q`, the extra label of `Q`, or a
mixed `r`-set as `r` passes through `|Q|-2`, `|Q|-1`, and `|Q|`; above that
range, complete `Q` and extend a positive set to `r-1` vertices.  The
assumption `|Q|>=3` supplies the non-hub choice used in the mixed set.  These
cases exhaust the three possible corrections and prove the lemma.

Now fix `3 <= s <= N-2`.  If `T` is a block of size `s`, it contains no
member of `B_s`, but `T` itself belongs to `B_(s-1)`.  Otherwise, if
`kappa(T)>=s`, part 1 supplies a member of `B_s` below `T`; if
`kappa(T)<=s-1`, part 2 supplies a member of `B_(s-1)` above `T`.  The two
possibilities are disjoint by strict increase of `kappa`; the extra whole
blocks are also incomparable with the corresponding ordinary level.  Hence

```text
2^V - Up(B_s) = Down(B_(s-1)),
```

and (3) gives `D(B_s)=B_(s-1)`.

For the endpoint, `B_2` consists exactly of all triples inside one clique and
all cross-block pairs other than the two bridges.  A maximal subset avoiding
those facets is therefore either an edge inside a clique or one of the two
bridges.  Hence `D(B_2)=P_0`.

The four startup arrows and `D(P_4)=B_(N-2)` follow by direct substitution
in (3).  The lists above make this a finite six-coordinate calculation:
coordinatewise containment gives exactly the five types in `P_1`, the five
types in `P_2`, the ten deficits in `D_3`, the thirteen deficits in `D_4`,
and finally the corrected-cardinality layer `B_(N-2)`.  `verify.py` performs
this calculation independently at every tested parameter triple, in addition
to checking every cover of the type box and both directions of the
rank-filling lemma.

Finally, `P_0` is a graph.  Every other state in (2) has a facet of size at
least three (`B_2` already contains each clique triple), so no earlier state
is isomorphic to `P_0`.  This proves the first return up to isomorphism and
the theorem.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter; standard
library only.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --max-size 6 --rank-fill-max 5
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 compare_boolean.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected primary output:

```text
VERIFIED all-width hubbed three-clique recurrence; sizes=3..6; cases=64; transitions=992; facets_with_multiplicity=47040; kappa_covers=178848; rank_fill_checks=117504; NF(H_n,m,l)=n+m+l+2
ORBIT_SHA256=f743a35b3e64106de32f225bd70d6e3a5fba0ecb26bb06ef70e04f1e5f260704
```

Expected independent and entry-level outputs:

```text
INDEPENDENT VERIFIED Boolean-lattice hubbed three-clique orbits; cases=2; states=23; facets_with_multiplicity=1591; labelled_period=n+m+ell+2; no earlier isomorphic return
ORBIT_SHA256=3fca43e6c8eafafc712574b68bfb896a8c4a4380635ed77851864f461b1c08c1

MATCHED all-width type recurrence and Boolean facets entry-for-entry; cases=2; states=23; facets=1591
EXPANDED_ORBIT_SHA256=3fca43e6c8eafafc712574b68bfb896a8c4a4380635ed77851864f461b1c08c1
```

The primary checker uses the lossless symmetry quotient.  The independent
checker imports no orbit formula or type code: it constructs the labelled
graphs from their edges and applies the defining maximal-nonface operation to
every Boolean subset.  `compare_boolean.py` then expands every type class and
matches all 1,591 small-case facets entry-for-entry.

## Literature and novelty boundary

Hibi and Mahmood introduced the NF-number and proved formulas including two
disjoint cliques, not this graph:

<https://arxiv.org/abs/2005.01247>

Bilal--Ahmad--Mahmood--Binyamin prove `rn+2` for `r` disjoint equal copies of
`K_n`; their theorem has no bridges and requires equal clique widths:

<https://doi.org/10.1007/s11587-025-00987-5>

Rather's 2026 paper treats the first dumbbell iterates, complete split graphs,
and double stars, and explicitly names block graphs as a natural future
direction.  It does not state the family or recurrence above:

<https://arxiv.org/abs/2605.30781>

A targeted primary-source search on 2026-09-04 found no duplicate of this
theorem.  That is a search-relative novelty statement, not a claim of
historical priority.

## Trust boundary and scope

Universal validity rests on the explicit recurrence (1)--(2), the
rank-filling lemma, and the five finite startup identities.  Computations for
`3 <= n,m,ell <= 6` and the two Boolean-lattice replays are regression and
independent validation, not extrapolation.  Correctness trusts inspection of
the proof and CPython integer/set semantics.  There is no solver, floating
point, randomness, generated input, external dataset, omitted certificate,
or nonstandard dependency.

The theorem assumes all three clique widths are at least three and both
bridges use the same distinguished vertex of the middle clique.  It does not
cover a `K_2` block, distinct middle bridge endpoints, longer clique trees,
or arbitrary block graphs.
