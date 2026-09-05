# Independent r=28 separator-certificate review

This directory gives a clean-room, exact review of the finite
separator/component classification used by Discovery Net heights 2569 and
2583 at the two exact Albertson `r=28` rows `(55,768)` and `(55,769)`.

## Review verdict

The `r=28` slice is accepted.

Under the published crossing inequalities, critical-graph hypotheses, and
the factor-critical complement consequence, the independent checker finds:

1. A triangle-free complement is impossible at both rows.
2. If the complement contains a triangle and `B` is the set obtained from
   Tutte--Berge, the only surviving barrier sizes are `b=3` and `b=4`.
3. At `b=3` the only surviving component-size multisets are
   `(51,1)` and `(50,1,1)`.
4. At `b=4` the only survivor is `(49,1,1)`.

These are exactly the finite inputs used at height 2583.  In particular, the
claim that the `b=4` branch has one 49-vertex component and two singleton
components is independently reproduced.  This review is deliberately limited
to `r=28`, `m=768,769`; it does not certify the broader `r=27,29,30` statement
of height 2569.

## Mathematical reduction

Let `G` be 28-critical on 55 vertices, let `H` be its connected complement,
and suppose `cr(G)<cr(K_28)`.  Put

    x_v = 27-d_H(v) = d_G(v)-27,
    X = sum_v x_v = 2m-55*27.

Thus `X=51` or `53`, `Delta(H)<=27`, and Stehlik's theorem makes `H`
factor-critical.

If `H` is triangle-free, a maximum-degree vertex has degree 27 because
`X<55`.  Its neighbourhood is a clique `K_27` in `G`.  The exact complementary
edge count leaves a 28-vertex induced graph with at least 339 edges at row 768
or 338 at row 769.  The split lower bounds are respectively 8268 and 8238,
both exceeding `Z(28)=7098`.

Now suppose `H` contains a triangle `T`.  The graph `H-T` has no perfect
matching, since otherwise `T` and 26 matching edges would cover `H` with only
27 cliques.  Tutte--Berge supplies a set `S` such that, for
`B=T union S` and `b=|B|`, the graph `H-B` has at least `b-1` odd components.
Writing their complete component-size multiset as `parts`, every candidate
must satisfy five necessary conditions:

1. `sum s max(0,28-b-s) <= X` from degree deficiency.
2. Every complete bipartite subgraph obtained by grouping components must
   have crossing lower bound at most `Z(28)`.
3. The lower and upper bounds on `e_G(H-B,B)` must overlap.
4. The complete multipartite graph between components must not force a
   subdivision of `K_28`.
5. The exact split bound between `G[H-B]` and `G[B]` must not exceed `Z(28)`.

The production verifier enumerates every integer partition by ascending
multiplicity vectors, uses an integer bitset for subset sums, scans every
admissible pair of excess and internal-barrier edge counts, and records the
first failed condition.  These representations and the full `(Y,Q)` scan are
independent of the descending-recursion and set-based implementation under
review.

## Structural audit

The second checker compresses most of the finite work to uniform inequalities.
Write `a=28-b`.  For `6<=b<=24`, start with the required `b-1=27-a` odd
singletons.  Any positive-cost component has deficiency
`s(a-s)>=a-1`.  There can be at most two zero-cost odd components: three would
already require more than `27+a=55-b` vertices when `a>=4`.  Therefore

    deficiency >= (b-3)(a-1) = (b-3)(27-b) >= 63 > 53.

Equality is attained by two large odd components and `b-3` singletons, so the
bound is exact.

For `b=25`, thirty vertices split into at least 24 odd components.  After one
vertex is assigned to each, only six vertices remain, and convexity gives
`sum_C binom(|C|,2)<=binom(7,2)=21`.  Hence the cross-edge upper bound is at
most 35, below the lower bound 75.  For `b=26` the analogous numbers are 10,
44, and 52.

Only thirteen boundary partitions remain at `b=3,4,5`.  Direct exact
bipartite bounds leave the three multisets in the verdict.  At `b=27`, the
only partitions are `3+1^25`, `2+1^26`, and `1^28`; the last two force
`TK_28`, while the first has split lower bound 7767 or 7732.  At `b=28`, the
only partition is `1^27`, with split lower bound 8268 or 8238.

## Comparison with the upstream certificate

The source under review was fetched at the exact public commit

    c9cdabd4b8bc17ff5e87293077eb017fc88407a5

from
<https://github.com/abuzar08/discovery-net-notes/tree/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy>.
Its two expected-output comparisons were empty and every manifest hash passed.
The reviewed `verify_range.py` SHA-256 is

    a3de1715457ead9e8225534d3f7b4ac3d6de17f88b24a3c7ffeeec11aa2e3aa0.

Calling its public `analyse(28,m)` gives the same two branches for each row:

    m=768: [(3,24,2,1353), (4,23,3,1230)]
    m=769: [(3,24,2,1355), (4,23,3,1232)].

The clean-room implementation additionally hashes all 74 admissible
component records, including every bound and disposition.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r28_separator_certificate_review
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 audit.py | diff -u EXPECTED_AUDIT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, every manifest entry `OK`, 74 entry records, survivor
multisets `b3:51,1;50,1,1|b4:49,1,1`, and certificate SHA-256

    bd5ce6a29e7fb90259e5fe4ec3b341cbb5fcceb8de25ad0416a8bbe21af5cf5e.

## Provenance and trust boundary

Primary inputs checked for this review:

- M. Stehlik, *Critical graphs with connected complements*, JCTB 89 (2003),
  189--194, <https://doi.org/10.1016/S0095-8956(03)00069-8>.
- A. Sadhu, *Albertson's Conjecture Holds for r at Most 26*, Lemmas 2.1 and
  2.2, <https://arxiv.org/abs/2609.01682>.
- D. Kleitman, *The crossing number of K5,n*, JCT 9 (1970), 315--323,
  <https://doi.org/10.1016/S0021-9800(70)80087-4>.
- The Tutte--Berge matching formula.

The checkers use Python arbitrary-precision integers, exact `Fraction`
arithmetic, deterministic finite enumeration, and SHA-256.  They use the
conservative floor of every rational crossing lower bound.  They do not
re-prove the cited theorems, verify drawing topology, or certify any
component multiset as graph-realizable; all enumeration constraints are
necessary relaxations.

This review verifies the finite `r=28` component classification feeding
height 2583.  It does not independently verify height 2583's subsequent local
matching lemma, which has a separate Lean formalization at height 2599.
