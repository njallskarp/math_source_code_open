# A scale-six semigroup theorem for the order-eight obstructions

## Canonical obstacle

Let `G8` be the partial tournament on vertices `0,...,7` with arcs

    0->1, 0->2, 0->3, 4->0, 6->0, 7->0,
    1->3, 1->4, 5->1, 1->6, 7->1, 2->3,
    2->4, 5->2, 6->2, 2->7, 3->5, 3->6,
    3->7, 4->5.

Its eight unoriented pairs are

    05, 12, 34, 46, 47, 56, 57, 67.

Exact enumeration of the 40,320 total orders gives two structural facts:

1. every total order predicts at most 13 of the 20 displayed arcs;
2. exactly 832 total orders attain 13.

The automorphism group of `G8` has order two.  The explicit permutation maps
in `g8_maps.txt` prove that every one of the 96 dual supports in
`certificate.txt` is a relabeling of this single partial tournament.

## All completions

There are `2^8=256` labeled tournament completions of `G8`.  The explicit
isomorphisms in `g8_maps.txt` map every completion to one of the 96
independently reviewed obstruction representatives, and reach all 96.  The
numbers of representatives hit by respectively 2, 4, and 6 labeled
completions are 72, 16, and 8.  Since the source representatives are
pairwise nonisomorphic, the 256 completions have exactly 96 isomorphism
classes: precisely the height-1669 order-eight one-summand obstructions.

This turns the earlier 96-row lower-bound phenomenon into one object: the
exceptional classes are exactly all tournament completions of `G8`.

## Exact integral ray

**Theorem.**  If `T` is any tournament completion of `G8`, then for every
integer `q>=1`,

    m(6q T) = 7q.                                        (1)

**Lower bound.**  Suppose a stabilizer of size `a` exists for `6qT`.
Reversing its `a` orders turns the stabilization identity into a profile of
`6q+2a` total orders that predicts every arc of `T` exactly `6q+a` times.
In particular its total number of predictions on the 20 `G8` arcs is

    20(6q+a).

But each order predicts at most 13 `G8` arcs, so

    20(6q+a) <= 13(6q+2a),

which simplifies to `a>=7q`.

**Upper bound.**  For each of the 96 representatives, `m6_profiles.txt`
gives a multiset of exactly 20 total orders that predicts each of all 28
arcs exactly 13 times.  Equivalently, in reference coordinates its sum is

    6 x(T) + 7*1.

Partition any 13 profile orders into `A` and call the remaining seven `R`.
If `B` consists of the reversals of the orders in `R`, then

    6 x(T) + B = A.

Thus `B` is a seven-summand TTD stabilizer and `m(6T)<=7`.  The explicit
completion isomorphisms transport these profiles to every labeled completion
of `G8`.  Summing `q` copies proves `m(6qT)<=7q`; the lower bound gives (1).

## Algebraic interpretation and scope

The 832 `G8`-tight orders generate an affine semigroup in degree and the 28
pair coordinates.  The theorem says that all 256 Boolean completion targets

    (20; 13 on every completed arc)

lie in its degree-20 fiber.  The dual functional "number of predicted G8
arcs" exposes this face and proves that degree 20 is optimal for the
scale-six target.  This is a saturation statement on one exposed semigroup
face, not a larger tournament census.

The result determines all multiples of six on the 96 exceptional rays.  It
does not determine `m(dT)` when `6` does not divide `d`, nor the full maximum
`m(8,k)` at finite `k`.

## Trust boundary

`verify_m6.py` uses only standard-library integer arithmetic.  It checks the
canonical `G8` maximum and tight-order count, all 96 support isomorphisms, all
256 completion isomorphisms, and all 2,688 arc-count equations in the 96
integral profiles.  The SciPy/HiGHS MILP generator discovered the profiles
but lies outside the correctness boundary.  Pairwise nonisomorphism and
exhaustiveness of the 96 source representatives are inherited from the
independently reviewed heights-1669/1675 classification.
